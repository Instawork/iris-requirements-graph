"""Load the Iris requirements graph from disk into one in-memory object.

Every tool reads the graph through `load_graph` so they all agree on what the files mean.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

LAYER_ORDER = ["user-interface", "product", "platform"]
PHASES = ["MVP", "P2", "P3"]
ROLES = ["INSTAWORK_ADMIN", "PROGRAM_USER", "UNIT_USER", "AGENCY_USER", "SYSTEM"]
SCALAR_TYPES = {"uuid", "text", "int", "decimal", "money", "date", "time", "timestamp", "bool", "json"}
IMPLICIT_FIELDS = {"id": "uuid", "created_at": "timestamp", "updated_at": "timestamp"}
CATALOG_ENUMS = {"settings": "SettingKey", "notifications": "NotificationType", "upload-types": "UploadType"}

REQUIREMENT_ID = re.compile(r"^REQ-([A-Z][A-Z0-9-]*[A-Z0-9])-(\d{4})$")
REQUIREMENT_ID_IN_TEXT = re.compile(r"\bREQ-[A-Z][A-Z0-9-]*-\d{4}\b")


@dataclass
class Graph:
    root: Path
    layers: list = field(default_factory=list)
    modules: dict = field(default_factory=dict)
    requirements: dict = field(default_factory=dict)
    paths: dict = field(default_factory=dict)
    entities: dict = field(default_factory=dict)
    enums: dict = field(default_factory=dict)
    data_model_files: dict = field(default_factory=dict)
    sources: dict = field(default_factory=dict)
    decisions: dict = field(default_factory=dict)
    conflicts: dict = field(default_factory=dict)
    inputs: dict = field(default_factory=dict)
    terms: list = field(default_factory=list)
    capabilities: dict = field(default_factory=dict)
    features: dict = field(default_factory=dict)
    settings: dict = field(default_factory=dict)
    notifications: dict = field(default_factory=dict)
    upload_types: dict = field(default_factory=dict)
    reviewers: dict = field(default_factory=dict)
    retired: dict = field(default_factory=dict)
    load_errors: list = field(default_factory=list)

    def depends_on(self, requirement_id: str) -> list[str]:
        doc = self.requirements.get(requirement_id) or {}
        return [
            edge.get("requirement_id")
            for edge in (doc.get("edges") or [])
            if isinstance(edge, dict) and edge.get("edge_type") == "DEPENDS_ON"
        ]

    def dependency_closure(self, requirement_id: str) -> set[str]:
        """Every requirement reachable by DEPENDS_ON from this one, not including itself."""
        seen: set[str] = set()
        stack = list(self.depends_on(requirement_id))
        while stack:
            current = stack.pop()
            if current in seen or current not in self.requirements:
                continue
            seen.add(current)
            stack.extend(self.depends_on(current))
        return seen

    def dependents(self, requirement_id: str) -> list[str]:
        return sorted(rid for rid in self.requirements if requirement_id in self.depends_on(rid))

    def feature_phase(self, feature_id: str) -> str | None:
        feature = self.features.get(feature_id)
        if not feature:
            return None
        capability = self.capabilities.get(str(feature.get("capability_id")))
        return capability.get("phase") if capability else None

    def enum_values(self, enum_name: str) -> list[str]:
        enum = self.enums.get(enum_name) or {}
        return [value.get("value") for value in (enum.get("values") or []) if isinstance(value, dict)]

    def module_layer(self, module_id: str) -> str | None:
        module = self.modules.get(module_id)
        return module["layer"] if module else None


def parse_type(type_text: str):
    """Split a data-model type into (kind, target). kind is scalar, ref, enum, or list."""
    if not isinstance(type_text, str) or not type_text:
        return None
    if type_text in SCALAR_TYPES:
        return ("scalar", type_text)
    if type_text.startswith("ref:"):
        return ("ref", type_text[4:])
    if type_text.startswith("enum:"):
        return ("enum", type_text[5:])
    if type_text.startswith("list:"):
        inner = parse_type(type_text[5:])
        if inner is None or inner[0] == "list":
            return None
        return ("list", inner)
    return None


def type_targets(type_text: str):
    """The (kind, name) pairs a type points at: refs to entities and enums."""
    parsed = parse_type(type_text)
    if parsed is None:
        return []
    if parsed[0] == "list":
        parsed = parsed[1]
    if parsed[0] in ("ref", "enum"):
        return [parsed]
    return []


def _read_yaml(path: Path, graph: Graph):
    try:
        with path.open() as handle:
            return yaml.safe_load(handle)
    except Exception as exc:  # noqa: BLE001
        graph.load_errors.append((str(path.relative_to(graph.root)), f"cannot parse YAML: {exc}"))
        return None


def _list(doc, key):
    if not isinstance(doc, dict):
        return []
    value = doc.get(key)
    return value if isinstance(value, list) else []


def load_graph(root: Path | str = REPO_ROOT) -> Graph:
    root = Path(root)
    graph = Graph(root=root)
    graph_dir = root / "graph"

    layers_doc = _read_yaml(graph_dir / "layers.yaml", graph)
    for layer in _list(layers_doc, "layers"):
        graph.layers.append(layer)
        for module in layer.get("modules") or []:
            module_id = module.get("module_id")
            if module_id in graph.modules:
                graph.load_errors.append(("graph/layers.yaml", f"module {module_id} is listed twice"))
            graph.modules[module_id] = {**module, "layer": layer.get("layer")}

    for path in sorted((graph_dir / "requirements").glob("**/*.yaml")):
        doc = _read_yaml(path, graph)
        if not isinstance(doc, dict):
            graph.load_errors.append((str(path.relative_to(root)), "requirement file is not a mapping"))
            continue
        requirement_id = doc.get("requirement_id")
        if requirement_id in graph.requirements:
            graph.load_errors.append((str(path.relative_to(root)), f"duplicate requirement_id {requirement_id}"))
            continue
        graph.requirements[requirement_id] = doc
        graph.paths[requirement_id] = path

    for path in sorted((root / "data-model").glob("*.yaml")):
        doc = _read_yaml(path, graph)
        if not isinstance(doc, dict):
            continue
        module_id = doc.get("module")
        graph.data_model_files[str(path.relative_to(root))] = doc
        for enum in _list(doc, "enums"):
            name = enum.get("enum")
            if name in graph.enums:
                graph.load_errors.append((str(path.relative_to(root)), f"enum {name} is defined twice"))
            graph.enums[name] = {**enum, "module": module_id, "file": str(path.relative_to(root))}
        for entity in _list(doc, "entities"):
            name = entity.get("entity")
            if name in graph.entities:
                graph.load_errors.append((str(path.relative_to(root)), f"entity {name} is defined twice"))
            fields = {}
            for item in entity.get("fields") or []:
                if isinstance(item, dict) and item.get("name"):
                    if item["name"] in fields:
                        graph.load_errors.append(
                            (str(path.relative_to(root)), f"{name}.{item['name']} is defined twice")
                        )
                    fields[item["name"]] = item
            graph.entities[name] = {
                **entity,
                "module": module_id,
                "file": str(path.relative_to(root)),
                "field_map": fields,
            }

    for key, target in (
        ("sources", "sources"),
        ("decisions", "decisions"),
        ("conflicts", "conflicts"),
        ("inputs", "inputs"),
    ):
        doc = _read_yaml(graph_dir / f"{key}.yaml", graph)
        id_key = {"sources": "source", "decisions": "decision_id", "conflicts": "conflict_id", "inputs": "input_id"}[key]
        for item in _list(doc, key):
            getattr(graph, target)[item.get(id_key)] = item

    graph.terms = _list(_read_yaml(graph_dir / "terms.yaml", graph), "terms")
    for item in _list(_read_yaml(graph_dir / "scope" / "capabilities.yaml", graph), "capabilities"):
        graph.capabilities[str(item.get("capability_id"))] = item
    for item in _list(_read_yaml(graph_dir / "scope" / "features.yaml", graph), "features"):
        graph.features[item.get("feature_id")] = item
    for item in _list(_read_yaml(graph_dir / "catalogs" / "settings.yaml", graph), "settings"):
        graph.settings[item.get("key")] = item
    for item in _list(_read_yaml(graph_dir / "catalogs" / "notifications.yaml", graph), "notifications"):
        graph.notifications[item.get("type")] = item
    for item in _list(_read_yaml(graph_dir / "catalogs" / "upload-types.yaml", graph), "upload_types"):
        graph.upload_types[item.get("type")] = item
    for item in _list(_read_yaml(graph_dir / "reviewers.yaml", graph), "reviewers"):
        graph.reviewers[item.get("reviewer_id")] = item
    for item in _list(_read_yaml(graph_dir / "retired.yaml", graph), "retired"):
        graph.retired[item.get("requirement_id")] = item

    catalog_values = {
        "settings": list(graph.settings),
        "notifications": list(graph.notifications),
        "upload-types": list(graph.upload_types),
    }
    for enum in graph.enums.values():
        catalog = enum.get("catalog")
        if catalog in catalog_values:
            enum["values"] = [{"value": value, "meaning": f"See graph/catalogs/{catalog}.yaml"} for value in catalog_values[catalog]]

    return graph
