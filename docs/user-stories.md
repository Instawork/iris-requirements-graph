# Iris user stories: MVP

Iris is Instawork's vendor management system for Compass. Compass locations order temporary staff, approved staffing Agencies fill the Shifts with their own Workers, and Iris checks rates, credentials, and hours along the way.

This document lists what each kind of user needs from the MVP, as user stories grouped by journey. Each story ends with the requirements in the [requirements graph](../README.md) that it covers, where the full detail lives.

**Status: draft.** No requirement behind these stories is approved yet, and the stories assume answers to open questions that Compass and Instawork have not yet given. The ones most likely to change a story are listed at the end.

## Who uses Iris

| User | Who they are | What they do in Iris |
| --- | --- | --- |
| Unit User | A Compass operator at one or more locations, such as Soldier Field | Books Shifts, sends them to Agencies, approves hours, rates Workers |
| Agency User | Staff at a staffing Agency | Answers Shifts sent to the Agency, assigns Workers, submits hours, keeps rates and Credentials |
| Program User | Compass's program team | Sets up the org, Agencies, rates, and Credential rules, and watches spend |
| Instawork Admin | Instawork staff | Keeps reference data and invites the first Program User |

## Words used

- **Unit:** a Compass location that orders Shifts, such as a stadium or a hospital. Each Unit belongs to a **Company**, such as Soldier Field Concessions. A **Department** is a cost center inside a Unit, such as suites or concessions.
- **Request:** one booking of one or more **Shifts**. A Shift is one Position at one Unit, from a start time to an end time, for a headcount.
- **Release:** part or all of a Shift's headcount sent to one Agency, and that Agency's answer.
- **Rate Line:** an Agency's regular, overtime, and double-time Pay Rates and Bill Rates for one Position in one Market or at one Unit, from an effective date. The **Pay Rate** is what the Agency pays the Worker; the **Bill Rate** is what Compass pays the Agency; the **Markup** is the Bill Rate minus the Pay Rate, as a percentage of the Pay Rate.
- **Peer Rate:** the average regular Bill Rate other Agencies hold for the same Position and Market. A **Rate Review** asks an Agency to lower or justify a rate above it.
- **Credential:** a document proving a Worker meets a **Credential Type**, such as a food handler card. A **Credential Requirement** says where a type is required. An **Attestation** is the Agency's statement that a Worker meets a type.
- **Timesheet:** the hours one Worker billed for one Shift, or for one part of a Shift split by role.
- **Approval Tolerance:** how far billed times may differ from the schedule and still be approved automatically. **Lock Window:** how long after a Shift ends that its approved Timesheet locks.
- **Work Week:** a Unit's seven-day week, starting on its own day, used for overtime and weekly reporting.
- **Event:** a named occasion at a Unit, such as a banquet, that groups Shifts so their cost is seen as one.
- **Tip Pool:** tips for a Unit and date, or for one Shift or Event, split across Workers by minutes worked.
- **Spend:** approved spend plus pending spend. **Approved spend** is the hours on approved Timesheets at their Bill Rates, plus their tips and approved Expenses. **Pending spend** is the hours on Timesheets not yet approved for Shifts that have ended: the hours entered, or the scheduled hours as an estimate until both clock times are in, with no tips or Expenses. A Shift that has not ended, a cancelled Shift, and a no-show add no hours.
- **Proposal:** changes Iris prepared from a file or a message, which a person approves before anything is saved.

## Journeys

1. [Sign in and find your way](#1-sign-in-and-find-your-way)
2. [Home and to-dos](#2-home-and-to-dos)
3. [Set up the program](#3-set-up-the-program)
4. [Rates](#4-rates)
5. [Order labor](#5-order-labor)
6. [Send Shifts to Agencies](#6-send-shifts-to-agencies)
7. [Answer and staff Shifts](#7-answer-and-staff-shifts)
8. [Workers and Credentials](#8-workers-and-credentials)
9. [Hours and Timesheets](#9-hours-and-timesheets)
10. [Tips and Expenses](#10-tips-and-expenses)
11. [Reports](#11-reports)
12. [The assistant and uploads](#12-the-assistant-and-uploads)

---

## 1. Sign in and find your way

### 1.1 Sign in

**As any user**, I want to sign in with my email and password, **so that** I reach my work in Iris.

- One sign-in page serves every role and never asks which role I am.
- A failed sign-in shows one message that does not say whether the email, the password, or a deactivated account was the cause, and keeps the email I typed.
- There is no sign-up: an account exists only when someone invites me, or, for an Instawork Admin, when Instawork sets it up.
- Opening any page that needs a sign-in while signed out shows the sign-in page.

*Covers: REQ-SHELL-0004*

### 1.2 Set my password from an invite or a reset link

**As any user**, I want to set my password from the link I was emailed, **so that** I can accept an invite or get back in when I forget it.

- The sign-in page links to a reset page that takes my email and always shows the same message, whether or not the email has an account.
- A valid link shows my email, which I cannot change, and asks for a new password of at least 12 characters.
- A link works once and for 72 hours. A used, expired, or unknown link, or one for a deactivated account, says it no longer works and offers a new reset.
- Once the password is saved, I am sent to sign in.

*Covers: REQ-SHELL-0005*

### 1.3 Choose the role I am acting in

**As a user with more than one role or Agency**, I want to pick which one I am working in and switch without signing out, **so that** I see the right screens and records for the job in hand.

- I act in one context at a time: all my Unit access together, each Agency on its own, or the whole program.
- With only one such choice I go straight in; with several (for example, two Agencies) I choose at each sign-in and can switch from any page.
- Choosing or switching opens that role's Home and menu, and changes no record.
- Every page shows the role I am acting in and its scope: the parts of the org my Unit access was granted on (such as a District or a Unit), the Agency's name, or the whole program.
- If none of my access is current, I see a page saying I have no access, with only sign out.

*Covers: REQ-SHELL-0002*

### 1.4 See only the screens my role can use

**As any user**, I want a menu with only my role's screens, **so that** I never land on work that is not mine.

- Every signed-in page has the same frame: the menu, the page name, and an account menu with my name, email, my profile, and sign out.
- The menu lists, in order:
  - Unit User: Home, Shifts, Timesheets, Tips, Workers, Agencies, Events, Reports, Uploads, Setup.
  - Agency User: Home, Shifts, Workers, Timesheets, Rate Card, Uploads, Users.
  - Program User: Home, Shifts, Workers, Rates, Credentials, Agencies, Org, Users, Reports, Uploads, Settings.
  - Instawork Admin: Home, Positions, Markets, Labor rules, Account team, Outside ids.
- Opening a screen or record outside my access shows a refusal and a link to Home, and nothing of the record.
- After 12 hours without activity, or when my account is deactivated, I am returned to the sign-in page.

*Covers: REQ-SHELL-0009, REQ-SHELL-0006, REQ-UNIT-WEB-0001, REQ-AGENCY-WEB-0001, REQ-PROGRAM-WEB-0001, REQ-ADMIN-WEB-0001*

### 1.5 Narrow my screens to one Unit

**As a Unit User who covers several Units**, I want to narrow every Unit screen to one Unit, **so that** I can focus on one location.

- I see all my Units together by default.
- Picking one Unit narrows every Unit screen to it, and the choice stays until I change it or sign out.

*Covers: REQ-UNIT-WEB-0001*

### 1.6 Work from my phone

**As any user**, I want every page to work in my phone's browser, **so that** I can work on the go with no app to install.

- Every page, including sign-in and the password pages, works in a phone browser.
- No page scrolls sideways at a width of 360 px; a wide table scrolls inside its own area.
- The menu folds behind one button, and every desktop action is still available.
- I can send a file from my phone, including a photo of a paper sign-in sheet.

*Covers: REQ-SHELL-0001*

### 1.7 Keep my profile up to date

**As any user**, I want to see my profile and change my name and phone, **so that** my details are right.

- The account menu opens my profile, which shows my name, email, phone, and each role I hold with its scope.
- I can change my name and phone; my email is shown but cannot be changed.
- Change password emails me a reset link.
- I cannot change my own roles or deactivate myself.

*Covers: REQ-SHELL-0006*

### 1.8 Read my notifications

**As any user**, I want an inbox of my in-app notifications, **so that** I can catch up on what happened and go straight to it.

- Every page shows how many in-app notifications I have not read.
- The inbox lists my notifications for every role I hold, newest first; email and text messages are not listed.
- Opening one marks it read and opens the page for the record it is about in the role I am acting in; if that role has no page for it, nothing else opens.
- A notification about a record outside the role or Agency I am acting in does not switch me: the record is refused, as any record outside my access is, until I switch to the role it belongs to.

*Covers: REQ-SHELL-0007*

### 1.9 Download any table

**As any user**, I want to download any table as a CSV file, **so that** I can work with the data elsewhere.

- Every table has a download that holds exactly the rows and columns I see, with my filters and sort, across every page of results.
- A column my role may not see, such as a Pay Rate for a Unit User, is never in the file.

*Covers: REQ-SHELL-0010*

### 1.10 See who changed a record

**As a Unit User, an Agency User, or a Program User**, I want to see a record's change history, **so that** I know who changed what, when, and why.

- History appears on the screens that include it, and each of those screens names which roles see it.
- Entries are listed newest first; each shows when, who (or Iris for an automatic change), how the change came in, each field's old and new value, and any reason. An entry saved from a Proposal says so.
- The history can only be read.
- A field my role may not see, such as a Pay Rate, is left out.

*Covers: REQ-SHELL-0011*

### 1.11 Every screen behaves the same way

**As any user**, I want refusals, empty lists, times, and money to look the same on every screen, **so that** I do not have to relearn each one.

- When Iris refuses an action, the reason shows beside it and what I typed is kept.
- I am only offered actions my role may take on a record in its current state.
- Where a reason is required, I cannot confirm until I give one.
- An empty list says so, says when my filters are the cause, and offers to clear them.
- Dates and times of a Shift, Release, Timesheet, or Tip Pool show in the Unit's own time zone, and money shows in dollars to the cent.

*Covers: REQ-SHELL-0013*

### 1.12 Be told when something needs me

**As any user**, I want Iris to tell me when something happens that I need to know about, **so that** I do not have to keep checking.

- Each notification goes in the app, and by email or text where listed here, to every active user it is meant for, except the person whose action caused it.
- Every Agency User of the Agency is told:
  - by email, text, and in the app, when a Shift is sent to the Agency or headcount is added to one it holds;
  - by email and in the app, when a Release is withdrawn or its Shift cancelled, and when the date, times, headcount, or site instructions of a Shift the Agency holds change;
  - by email and in the app, when a Timesheet is sent back, with the reason; when a Unit User changes the hours, break, or no-show of a Timesheet that was submitted; and whenever a Unit User sets or clears a no-show;
  - by email and in the app, when one of its Workers stops being eligible for a Shift or is taken off one because the Unit blocked them, when a verified Credential is about to expire (8.5), when a Program User asks for a Rate Review, and when a Unit reports a Worker issue;
  - in the app, when an assignment or entered hours add overtime for one of its Workers, and when site instructions cannot reach an assigned Worker who has no email or phone.
- Every Unit User over the Shift's Unit is told:
  - in the app, when a Worker is assigned; by email and in the app, when a Worker is taken off the Shift or stops being eligible for it;
  - by email and in the app, when an Agency changes the hours, break, or no-show of a Timesheet that was submitted;
  - in the app, when a Timesheet change leaves part of a Tip Pool or a cashier PIN tip with no one to credit, and once per pool when a share locks while another Worker's hours are still missing.
- When an assignment or entered hours add overtime for a Worker, the Unit Users over the Shift's Unit and over each Unit where the overtime grows are told in the app.
- The Unit User who sent a Shift is told each Agency's answer by email and in the app; the one who reported a Worker issue is told in the app when it is resolved.
- Every Program User is told in the app when an Agency submits a rate; the one who asked for a Rate Review is told in the app when it is answered.
- Whoever submitted a rate is told by email and in the app when it is approved or sent back; whoever uploaded a Credential is told in the app when it is verified or rejected.
- Workers have no account: Iris sends them a Shift's site instructions by email and text (7.3).
- Invites and password resets come by email only (1.2).

*Covers: REQ-MESSAGING-0001*

---

## 2. Home and to-dos

### 2.1 Start from my to-do list

**As a Unit User, an Agency User, or a Program User**, I want my Home page to open on what I need to do next, **so that** nothing waits on me unnoticed.

- Home has one line for each kind of task, with how many are waiting and what is at stake: a dollar amount, the oldest one's age, or the nearest deadline.
- Each line opens the screen where the work is done, filtered to exactly those records.
- A record leaves the count as soon as its task is done; a task with nothing waiting shows no line, and when no line is left the list says there is nothing to do.
- The Home item in the menu shows the total waiting, and no number when it is zero.
- Home opens on the to-do list when anything is waiting, and otherwise on the section below it, where my role has one.
- Counts cover only the records my role and scope can see, and are worked out afresh each time the page loads.

*Covers: REQ-SHELL-0003*

### 2.2 Unit User Home

**As a Unit User**, I want my Home to show my to-dos and how spend is tracking, **so that** I can act on the day and keep within budget.

- To-dos: Timesheets to review, with their total billed amount and how many are late; Shifts that have not started and still have headcount to send to an Agency, with the time until the earliest starts; and badge requests to issue at secured Units, with the oldest one's age.
- Below the to-dos, a spend summary shows the month to date against the whole month's budget and the whole prior month, and the Work Week to date against the whole prior Work Week, each split into approved and pending spend.
- The summary links to the Reports screen for the breakdowns.

*Covers: REQ-UNIT-WEB-0014, REQ-UNIT-WEB-0001*

### 2.3 Agency User Home

**As an Agency User**, I want my Home to list everything the Agency must do next, **so that** we answer, staff, and bill on time.

- Seven to-dos: Releases to answer, Releases to staff, Timesheets to submit, Timesheets sent back, Credentials to renew, Rate Reviews to answer, and Worker issues to resolve.
- Releases show the time until the earliest Shift starts; Timesheets show the oldest one's age and how many are late; Credentials show the earliest expiry date; Rate Reviews and Worker issues show the oldest one's age.
- Each line opens the matching screen filtered to those records.
- Agency Home has nothing below the to-dos, so the list shows even when nothing is waiting.

*Covers: REQ-AGENCY-WEB-0011, REQ-AGENCY-WEB-0001*

### 2.4 Program User Home

**As a Program User**, I want my Home to show my approvals and which Units are spending most, **so that** I can keep the program on contract and spot Units spending above their normal level.

- To-dos: Credentials to review and Agency rate changes to approve, each with the oldest one's age; and rates above their peers that have never had a Rate Review, with the largest gap in dollars.
- Below the to-dos, every Unit is ranked by this month's spend, highest first, with approved and pending spend, spend as a percentage above or below the Unit's normal level, the average of its prior full calendar months, up to three (none where it has no prior full month), and how many of its Releases this month were off-contract or went to a non-contracted Agency.
- The ranking can be narrowed to one Sector, Region, or District, and selecting a Unit opens its Shifts.

*Covers: REQ-PROGRAM-WEB-0013, REQ-PROGRAM-WEB-0001*

---

## 3. Set up the program

### 3.1 Get the program started

**As an Instawork Admin**, I want to see what reference data is loaded and invite the first Program User, **so that** Compass can take over its own setup.

- Home shows how many active Positions, how many Markets, and how many labor rules in effect today are loaded.
- Whenever no active Program User has accepted an invite, Home offers an invite for one, and lists unaccepted invites with Send invite again and Revoke.
- Once a Program User has accepted, Home says one is in place and offers no invite. While exactly one active Program User holds the role, Home names them and offers Revoke, after a confirmation, so that a replacement can be invited.
- Home lists the other Instawork Admins and lets me deactivate or reactivate them.

*Covers: REQ-ADMIN-WEB-0001, REQ-PROGRAM-WEB-0007*

### 3.2 Keep the Position catalog

**As an Instawork Admin**, I want to add, rename, and deactivate Positions, **so that** every Shift, Rate Line, and Credential Requirement names a Position from one list.

- Positions are listed with whether each is active.
- A name another Position already has is refused.
- Before deactivating, I am told the Position can no longer be chosen for new Shifts or Rate Lines but stays on existing records.

*Covers: REQ-ADMIN-WEB-0002*

### 3.3 Keep Markets and their ZIP codes

**As an Instawork Admin**, I want to keep Markets and the ZIP codes in each, **so that** every Unit is priced in the right Market.

- Markets are listed by state and city, with how many ZIP codes each has.
- I add and rename a Market by city and state; a city and state another Market already has is refused.
- I add or remove a Market's ZIP codes; a ZIP code another Market already holds is refused.
- Adding a ZIP code to a Market moves every Unit with that ZIP code into it; removing one changes no Unit.

*Covers: REQ-ADMIN-WEB-0003*

### 3.4 Keep state and local labor rules

**As an Instawork Admin**, I want to keep the break, minimum wage, and overtime rules for each state and city, **so that** Iris checks Shifts and hours against the law where they are worked.

- Rules are listed by state, city, and kind, with their values and the dates they apply, and filter by state and kind.
- I add, change, and end a rule.
- A new rule for the same state, city, and kind is refused until the earlier one is ended.
- In MVP Iris checks one meal break and the minimum wage, and uses the overtime rules to class hours. Rest-break rules can be kept but are not checked, and a second meal break in one Shift is not checked.

*Covers: REQ-ADMIN-WEB-0004*

### 3.5 Name Instawork's account team

**As an Instawork Admin**, I want to name the Account Manager, Account Owner, and Support Lead for the program or any part of the org, **so that** every Unit knows whom at Instawork to contact.

- The screen shows the program-wide team, then each part of the org with its own assignments.
- I assign a role to an active Instawork Admin, for the whole program or one part of the org; this replaces whoever held it there, and removing one asks for confirmation.
- Opening a Unit shows who it resolves to for each role, and where that assignment comes from.
- A Unit User sees their Unit's account team, with names, emails, and phones, on the Setup screen.

*Covers: REQ-ADMIN-WEB-0005, REQ-UNIT-WEB-0011*

### 3.6 Keep the ids other systems use

**As an Instawork Admin**, I want to record the Fieldglass, SAP, and MyStaff ids of Units, Departments, Companies, Agencies, and Positions, **so that** Iris records can be matched to those systems when their integrations arrive.

- Nothing in MVP needs or reads these ids; uploads still find records by name.
- I pick a system and a record type and see every record with its id there, or none.
- I can search by name, code, or id, and show only records with no id yet.
- An id another record already holds is refused, naming that record.

*Covers: REQ-ADMIN-WEB-0006*

### 3.7 Build the org tree

**As a Program User**, I want to keep Compass's org as a tree of Sectors, Regions, Districts, and Units, **so that** access, rules, and reports follow how Compass is organised.

- The Org screen shows the tree, with whether each part is active.
- I add, rename, deactivate, and reactivate Sectors, Regions, and Districts; a name already used under the same parent is refused.
- A Sector, Region, or District can be deactivated only when everything beneath it is inactive, and reactivated only while its parent is active.

*Covers: REQ-PROGRAM-WEB-0002*

### 3.8 Add and change Units and Departments

**As a Program User**, I want to add Units with their Departments and keep their details, **so that** Shifts can be booked, priced, and charged to the right cost center.

- A new Unit, added under an active District, takes its name, address, Company (a new name adds the Company), Work Week start day, optional time zone, whether it is a secured site, its default site instructions (parking, entrance, directions, site contact, attire), and at least one Department.
- Iris sets the Unit's Market from its ZIP code, and its time zone too when I leave it empty, and shows both. A ZIP code in no Market is refused.
- A Unit name another Unit already has, anywhere in the program, is refused. So is a Department name already used in its Unit, or a cost center code another Department has.
- Each Unit lists its Departments with their cost center codes, addresses, and whether active; I add, rename, and deactivate them. A Unit's last active Department cannot be deactivated while the Unit is active.
- A new Department starts with the Unit's address and site instructions, which I can change. Changing the Unit's later does not change its Departments' copies.
- I can change or deactivate a Unit; an inactive Unit takes no new Request.
- A Unit's page shows its account team and its primary operator, picked from the Unit Users who cover it.

*Covers: REQ-PROGRAM-WEB-0002*

### 3.9 Upload Units from a file

**As a Program User**, I want to upload a file of Units and Departments, **so that** I can set up many locations at once.

- Upload Units on the Org screen opens the upload step with the Units file type already picked.
- The file has one row per Department. Iris checks each row and saves the accepted Units and Departments once I approve them.
- A row that names a Sector, Region, or District not yet in the tree offers to add it.
- A row for a Unit already in Iris is dropped: the file adds Units and never changes one.

*Covers: REQ-PROGRAM-WEB-0014*

### 3.10 Add Agencies and approve where they work

**As a Program User**, I want to add Agencies and approve each one for parts of the org, **so that** Iris knows which Agencies are contracted for each Unit and can flag or block Shifts sent to any other.

- Agencies are listed with whether each is active and how many parts of the org it is approved at, and I can search by name.
- A new Agency takes its name and a first contact, who is invited as its first Agency User. A name another Agency already has is refused.
- I can rename or deactivate an Agency; an inactive Agency receives no new Shifts.
- I approve an Agency at a Sector, Region, District, or Unit where it has no approval yet. Its page lists each approval with who made it and when, and each removed approval with who removed it and when.
- Before removing an approval, I am told that Shifts already sent do not change.

*Covers: REQ-PROGRAM-WEB-0006*

### 3.11 Upload Agencies from a file

**As a Program User**, I want to upload a file of Agencies, **so that** I can add many Agencies, their first contacts, and their approvals at once.

- Upload Agencies on the Agencies screen opens the upload step with the Agencies file type already picked.
- Iris saves the accepted Agencies and their approvals once I approve them, and invites each contact as that Agency's first Agency User.
- A row for an Agency already in Iris is dropped: the file adds Agencies and never changes one.

*Covers: REQ-PROGRAM-WEB-0015*

### 3.12 Manage users and their roles

**As a Program User**, I want to invite users and grant or revoke their roles, **so that** the right people have the right access.

- The Users screen lists every user with their roles and scopes, whether their invite was accepted, and their last sign-in, and filters by role, Agency, part of the org, and active or inactive.
- An invite takes the person's name, email, optional phone, and one role: Program User, Unit User for a part of the org, or Agency User for one Agency. Instawork Admin is never offered.
- Picking a Unit User scope says it covers every Unit at or below that point.
- I can add a role, revoke or restore one, resend an invite until it is accepted, and deactivate or reactivate any user except an Instawork Admin.

*Covers: REQ-PROGRAM-WEB-0007*

### 3.13 Manage my Agency's own users

**As an Agency User**, I want to invite colleagues and remove their access, **so that** my Agency controls who works in Iris for it.

- The Users screen lists everyone given access to my Agency, with whether they accepted their invite, their last sign-in, and whether their access is revoked or they are inactive.
- I can invite a colleague only as an Agency User for my Agency, resend an invite, and revoke or restore access.
- I can deactivate or reactivate a colleague only if they hold no access beyond my Agency.

*Covers: REQ-AGENCY-WEB-0010*

### 3.14 Change Settings for the program or part of it

**As a Program User**, I want to change Settings for the whole program and override them for parts of the org, **so that** rules such as the Approval Tolerance and the Lock Window fit how each part of Compass works.

- Every Setting is listed with what it means, its program default, whether that default was set by a Program User, and any overrides by Sector, Region, District, or Unit.
- I change a program default, or add an override at a Sector, Region, District, or Unit; a value is a whole number, on or off, or soft or hard, depending on the Setting.
- The Settings and their defaults are: the Approval Tolerance (15 minutes); the Lock Window (48 hours); the off-contract rate gate and the non-contracted Agency gate (soft lets the send go ahead with a reason and flags it, hard refuses it; both soft); the overtime block (off); the Peer Rate threshold (15%); and the Credential expiry warning (30 days).
- The Peer Rate threshold and the Credential expiry warning apply program-wide and take no override.
- Removing an override, or a program default I set, shows the value that now applies instead.
- Picking a Unit shows the value of every Setting in force there.

*Covers: REQ-PROGRAM-WEB-0008*

### 3.15 Keep my Unit's site instructions

**As a Unit User**, I want to keep the default site instructions for my Unit and its Departments, **so that** Agencies and Workers know where to park, enter, and report.

- The Setup screen shows the Unit's default parking, entrance, directions, site contact, and attire, and each Department's, and I can change them.
- Changing the Unit's defaults does not change a Department's; a Shift uses its Department's.
- The Unit's address, time zone, Company, Work Week start, and secured-site flag, and each Department's name, cost center code, and address, are shown read-only.
- The Setup screen also shows the Unit's primary operator.

*Covers: REQ-UNIT-WEB-0011*

---

## 4. Rates

### 4.1 See every Agency's rates

**As a Program User**, I want one list of every Agency's rates that I can filter and sort, **so that** I can compare rates without lining Agencies up side by side.

- Each Rate Line shows its Agency, Position, Market or Unit, all six rates, the Markup as a percentage, its dates, and its status.
- The list opens on approved lines in effect today, filters by Market, Position, Agency, Unit, and status, and sorts by any rate.
- A History tab lists every line ever entered, including replaced, pending, and sent-back ones, each with its change history.

*Covers: REQ-PROGRAM-WEB-0003*

### 4.2 Enter, change, and end rates

**As a Program User**, I want to enter and change rates for any Agency, **so that** contracted rates are in Iris before Shifts are sent.

- A rate I enter is approved at once.
- A line is refused, naming the check, when a rate is zero or less, a Bill Rate is below its Pay Rate, an overtime rate is below the regular rate, or a double-time rate is below the overtime rate. A line whose six rates match the line already in effect is refused as unchanged.
- Changing a line takes a reason and a start date and adds a new approved line. The old line ends on the new line's start date, so the new rates apply from that date; the old line is never edited and stays in the history.
- A send takes the rate in effect on the Shift's date. A Shift already sent keeps the Bill Rates it was sent at, and so do its Timesheets, even when a later change covers its date.
- I can end a line with an end date and a reason.

*Covers: REQ-PROGRAM-WEB-0003*

### 4.3 Upload a rate card

**As a Program User**, I want to upload a rate card file for any Agency, **so that** I can enter many rates at once.

- Upload rates on the Rates screen opens the upload step with the rate card file type already picked.
- Each row names its Agency, and each accepted row is saved as an approved Rate Line.

*Covers: REQ-PROGRAM-WEB-0016*

### 4.4 Keep my Agency's rate card

**As an Agency User**, I want to see my Agency's rates and submit new or changed ones, **so that** Compass pays us the rates we agreed.

- The Rate Card lists my Agency's lines with their Pay Rates, Bill Rates, Markup as a percentage, dates, and status. It never shows the Peer Rate or another Agency's rates.
- A new or changed line, by form or by file, waits as pending until a Program User approves it or sends it back; the current line stays as it is meanwhile.
- A line sent back shows the reason and can be submitted again.
- A History tab lists every line my Agency ever submitted, with its change history.

*Covers: REQ-AGENCY-WEB-0005*

### 4.5 Approve Agency rate changes

**As a Program User**, I want to approve or send back each rate an Agency submits, **so that** no rate takes effect without Compass's say.

- The approval queue lists pending lines, oldest first, each beside the line it would replace, the change in each rate, and the Agency's reason.
- A Market line also shows the Peer Rate and whether its regular Bill Rate would be flagged above it.
- Approve makes the line approved: it applies from its start date, and the line it replaces ends on that date. Shifts already sent keep the Bill Rates they were sent at. Send back requires a reason.
- A line dated before the one it would replace cannot be approved, only sent back.

*Covers: REQ-PROGRAM-WEB-0009*

### 4.6 Spot rates above their peers and ask for a review

**As a Program User**, I want rates above their peers highlighted, and to ask the Agency to lower or justify them, **so that** Compass does not overpay.

- Each Market rate in effect today shows its Peer Rate, and a line above it by the threshold (15% by default) or more is highlighted with the gap in dollars and percent.
- A line with no Peer Rate is never highlighted.
- A highlighted line offers Send Rate Review; a line under review shows the review's status instead.
- A Rate Reviews tab lists every review, open ones first, with the Agency's answer.

*Covers: REQ-PROGRAM-WEB-0009*

### 4.7 Answer a Rate Review

**As an Agency User**, I want to see when Compass questions one of our rates and answer it, **so that** we can keep the rate with a reason or lower it.

- Open reviews show above the Rate Card, each with the line under review and a statement that its rate is above its peers.
- Keep the rate requires a reason; Lower the rate opens the form for a new, lower line.
- A review answered with a reason closes as kept. One answered with a lower line stays open until that line is approved, then closes as lowered; if the line is sent back, I can answer again.

*Covers: REQ-AGENCY-WEB-0005*

### 4.8 See which Agencies I can use and what they charge

**As a Unit User**, I want to see the Agencies my Unit can use and their Bill Rates, **so that** I know my options before I send a Shift.

- For one Unit at a time, every active Agency is listed, those approved for the Unit first, each marked approved or non-contracted.
- Opening an Agency shows its approved Bill Rates for the Unit, current and upcoming, by Position. Where a Unit rate and a Market rate both apply, the Unit rate is marked as the contracted rate.
- A Position view lists each Agency's contracted regular Bill Rate, lowest first.
- I see Bill Rates only, never Pay Rates or Markup, and I cannot change anything here.

*Covers: REQ-UNIT-WEB-0005*

---

## 5. Order labor

### 5.1 Book a Request

**As a Unit User**, I want to book one Request with a line for each Position, **so that** I can order a whole crew in one go.

- New Shift on the Shifts list opens the form, and after booking the Shifts list opens on the new Shifts.
- The form takes one Unit and one or more lines. Each line needs a Position, Department, date, start and end time, and headcount, and can take a planned break. The Unit, Position, and Department are picked from active records in my scope.
- Each line's site instructions start from its Department's defaults and can be changed for that line.
- An end time before the start asks me to confirm the Shift ends the next day.
- Each line can be sent to an Agency as I book it, or left unsent.
- Break and minimum-wage flags show on the line for its times and the Agency picked, and never stop the booking.
- If a line is refused, nothing is booked and the line shows why. If the booking succeeds but a send is refused, that Shift stays unsent and shows why.

*Covers: REQ-UNIT-WEB-0002*

### 5.2 Book from a template

**As a Unit User**, I want to keep templates for the Requests I book often, **so that** I can book a regular crew in a few clicks.

- The Setup screen lists my Unit's templates with their lines, and I create, change, and delete them.
- A template line takes a Position, headcount, start and end time, and optionally a Department and a planned break; it has no date.
- Book on a template, or Start from template on the booking form, fills the lines for the date I pick, and I can change any line before I book.
- I can set a default Department for each Position, which fills in when I pick that Position.

*Covers: REQ-UNIT-WEB-0011*

### 5.3 Repeat a Request every week

**As a Unit User**, I want a Request to repeat on chosen weekdays, **so that** recurring Shifts are booked once.

- The booking form takes the weekdays, how many weeks apart, and an end date no more than 52 weeks after the line's date, which must fall on one of those weekdays.
- The Shifts of a repeating line show as a series.
- A multi-week assignment is booked this way, as one repeating Request. Each of its Shifts is still sent, answered, and staffed on its own.
- I can send the Shifts I choose from a series to one Agency in one step. Each is sent on its own, and any Shift whose send was refused is listed.
- Editing or cancelling a Shift in a series asks whether to apply it to this Shift or to every Shift in the series not yet started.

*Covers: REQ-UNIT-WEB-0017*

### 5.4 Overbook a Shift

**As a Unit User**, I want to book more Workers than I need and record how many I need, **so that** no-shows do not leave me short.

- Each booking line takes a needed headcount below its headcount.
- The Shift's page shows both numbers, and I can change the needed headcount there.
- The needed headcount is a record only: sending and filling use the headcount booked, every Worker who works is billed, and no report uses it.

*Covers: REQ-UNIT-WEB-0018*

### 5.5 Upload Shifts from a file

**As a Unit User**, I want to upload a file of Shifts, **so that** I can create or change many Shifts at once.

- Upload Shifts on the Shifts list opens the upload step with the Shifts file type already picked.
- A row with no Shift id creates a Shift, and a row with one changes that Shift. Iris checks each row and saves the accepted rows once I approve them.
- A row that names an Agency also sends the new Shift's whole headcount to it at the contracted rate.

*Covers: REQ-UNIT-WEB-0019*

### 5.6 See my Shifts by date

**As a Unit User**, I want to see my Units' Shifts by date with how full each is, **so that** I know where I am still short.

- Shifts are grouped by date: Shifts that have not ended first, soonest first, then ended Shifts, newest first.
- Each Shift shows its Position, Unit, Department, times, Workers assigned against headcount, the Agencies holding it, and its status.
- A Shift that has not started and has headcount not yet sent shows how much.
- The list filters by Unit, dates, Position, Agency, status, and unsent headcount. Cancelled Shifts stay listed, marked cancelled.
- The list's CSV download carries each Shift's id, so its rows can be changed and uploaded again.

*Covers: REQ-UNIT-WEB-0007*

### 5.7 Follow and change one Shift

**As a Unit User**, I want one page per Shift showing who is coming and letting me change it, **so that** I can manage the Shift until it ends.

- The page shows the Shift's details and site instructions; each Agency it was sent to with the headcount sent, its answer, the Bill Rates sent, any reasons given, and whether the send was off-contract or to a non-contracted Agency; and each assigned Worker by name, photo, and Agency, with any open places.
- Each assigned Worker shows whether they are eligible for the Shift and, once it has started, whether they were eligible at its start.
- Workers taken off the Shift are listed with the reason and time.
- Until the Shift ends I can edit its headcount, date, times, break, and site instructions; headcount cannot go below what Agencies already hold.
- On a Shift that has not started, changing the date or times checks every assigned Worker's eligibility again at once, and Iris also checks each morning. A Worker who is no longer eligible comes off the Shift, and the Agency and my Unit are told why (1.12).
- Until it starts I can cancel it after confirming, which cancels every Release still unanswered or accepted and takes its Workers off.
- Once the Shift has ended, edit, cancel, and send are gone.
- The page shows the Shift's change history.

*Covers: REQ-UNIT-WEB-0008*

### 5.8 Group Shifts into Events and see what each costs

**As a Unit User**, I want to group Shifts under a named Event and see its projected and actual cost, **so that** I know what each Event really cost.

- I create and rename Events for a Unit, and attach Shifts to an Event when booking, from the Shift's page, or from the Event; I can also move or detach them. A Shift belongs to at most one Event, of its own Unit.
- The Events screen lists each Event with its dates, number of Shifts, projected cost, actual cost, and the difference.
- Actual cost shows approved and pending spend, with any estimated part labelled as an estimate.
- From an Event I can open the Timesheets screen filtered to it and approve them together.

*Covers: REQ-UNIT-WEB-0010*

### 5.9 Order by email, text, or phone

**As a Unit User**, I want to book or change Shifts by email, text, or a phone call, **so that** I can order labor without opening Iris.

- Iris has an email address, a text number, and a phone line answered by an AI voice agent. It knows me by the email or phone on my account; a message it cannot match to exactly one user creates nothing, and a caller it does not recognize is told so.
- Iris drafts what I ask as the assistant does (12.2), and asks first for anything it needs, such as which Unit or which Agency.
- Times, Department, and Agency I leave out are filled from my Unit's most recent Shift for that Position that was not cancelled, and the draft marks each value filled that way. The Agency is filled only when that Shift went to one Agency.
- The draft comes back on the channel I used, and nothing is booked until I approve it: by replying yes in the same email or text thread, or by saying yes on the call. Replying or saying no rejects it. Any other reply is taken as an answer or a change.
- Approving by reply accepts every line. When a line needs a decision, or the thread has more than one open draft, Iris tells me to decide it in the app, where it stays open.
- On approval the Shifts are booked and each line with an Agency is sent.
- A message asking to change a Shift's headcount or times, or to cancel it, is drafted and approved the same way.

*Covers: REQ-ORDERING-0010, REQ-MESSAGING-0002*

---

## 6. Send Shifts to Agencies

### 6.1 Pick an Agency and send a Shift

**As a Unit User**, I want to pick an Agency at its contracted rate and send it a Shift's headcount, **so that** the Shift gets staffed at the agreed price.

- The send step lists the Agencies approved for my Unit with their contracted rate for the Shift, lowest first, then any non-contracted Agencies.
- Picking an Agency fills in its contracted rate and the unsent headcount, which I can lower.
- Before I send, I see whether the send needs a reason or would be refused, and which rule refuses it.
- If the Agency already holds this Shift, the headcount is added to its Release at the rates already sent, and the Release keeps its answer: an accepted one stays accepted.
- A refused send saves nothing.

*Covers: REQ-UNIT-WEB-0009*

### 6.2 Send at another rate or to a non-contracted Agency

**As a Unit User**, I want to send at a rate other than the contracted one, or to an Agency not contracted for my Unit, when I give a reason, **so that** I can still fill a Shift when the usual options fall short.

- I can type another regular Bill Rate, and must when there is no contracted rate; either way a reason is required, and the send is refused where Compass's settings do not allow off-contract rates.
- Iris sets the overtime and double-time Bill Rates from the rate I type: in proportion to the contracted ones, or 1.5 and 2 times it when there is no contracted rate.
- Sending to a non-contracted Agency asks for its own reason, separate from any rate reason, where Compass's settings allow it, and is refused where they do not.
- Adding headcount to a Shift an Agency already holds is checked again against today's contract: I am asked only for reasons it does not already have, and the add is refused where a setting refuses it.
- By default both kinds of send are allowed with a reason (3.14).
- A send that goes ahead with a reason is marked off-contract or non-contracted on the Shift's page, with the reason.

*Covers: REQ-UNIT-WEB-0009, REQ-UNIT-WEB-0008*

### 6.3 See when a rate is above its peers

**As a Unit User**, I want to be warned when the rate I am about to send is above what other Agencies charge, **so that** I can choose a better-priced Agency.

- The send step flags a regular Bill Rate that is above the Peer Rate by Compass's threshold or more.

*Covers: REQ-UNIT-WEB-0020*

### 6.4 Send more headcount or withdraw a Release

**As a Unit User**, I want to send remaining headcount from the Shift's page and withdraw a Release an Agency has not answered, **so that** I can react as plans change.

- Unsent headcount shows on the Shift's page with Send.
- After the Shift starts, I can send more only to Agencies that already accepted it.
- A Release the Agency has not answered yet offers Withdraw; its headcount becomes unsent again and can be sent to another Agency.
- Headcount an Agency declines, or that expires unanswered, becomes unsent again in the same way.

*Covers: REQ-UNIT-WEB-0008, REQ-UNIT-WEB-0009*

### 6.5 Ask for Workers by name

**As a Unit User**, I want to ask an Agency for particular Workers, **so that** people who know my site come back.

- When sending, or later on the Shift's page, I can name Workers from the Agency's active Workers, with my Unit's favourites first and Workers my Unit blocked left out.
- The Shift's page shows each Worker I asked for, and whether the Agency said they are unavailable and why.
- I can withdraw a request until the Shift starts.

*Covers: REQ-UNIT-WEB-0021*

---

## 7. Answer and staff Shifts

### 7.1 See the Shifts sent to my Agency

**As an Agency User**, I want to see every Shift sent to my Agency with what it pays and where to go, **so that** I can decide what to take on.

- The Shifts screen lists each Release sent to us, one row per Release, with its Unit, Position, date, times, headcount, Workers assigned, and status, grouped by date. Headcount a Unit adds to a Release we still hold raises that row's headcount, adds no row, and keeps its answer and rates: one we accepted stays accepted at the larger headcount.
- It opens on unanswered and accepted ones whose Shifts have not ended, soonest first; a second tab lists every other one, newest first. Both tabs filter by status, Unit, Position, and dates.
- Opening one shows the Unit's name and address, the Shift's times and break, our headcount, and our regular, overtime, and double-time Bill Rates.
- While it is unanswered or accepted, it also shows the site instructions.
- It shows our headcount beside the Shift's total, and whether other Agencies hold the Shift and how much in total, never their names, rates, answers, or Workers.
- The list's CSV download carries each Shift's id.

*Covers: REQ-AGENCY-WEB-0002*

### 7.2 Accept or decline a Shift

**As an Agency User**, I want to accept or decline each Shift, one at a time or several at once, **so that** the Unit knows quickly whether we can staff it.

- Until the Shift starts, I can accept a Shift we have not answered. Accept takes the whole headcount we were sent, and the Shift can then be staffed.
- Decline requires a reason, and is possible after accepting until the Shift starts; I am first told how many assigned Workers will come off it and asked to confirm.
- I can select several unanswered Shifts, such as a run of days, and answer them in one step; each is answered on its own, and any that cannot be answered are listed.
- A Release we have not answered when its Shift starts expires, and can no longer be accepted or declined.
- A Release that was declined, withdrawn, cancelled, or expired stays listed under its status, with any decline reason, and no action.

*Covers: REQ-AGENCY-WEB-0002*

### 7.3 Assign Workers to a Shift

**As an Agency User**, I want to pick Workers from our roster to fill an accepted Shift, **so that** the Unit sees who is coming.

- Assign is offered on an accepted Shift until it ends, while any of our headcount is open.
- The assign list holds our active Workers, those who can be assigned first.
- A Worker who cannot be assigned shows why: already on the Shift, blocked by the Unit, not eligible (naming the Credential Types not met), or, where a Unit's setting blocks overtime, adding overtime.
- I can pick no more Workers than the open headcount. Each picked Worker is assigned on their own; one refused at that point stays unassigned and shows why.
- If an assignment adds overtime, I see each Work Week and Unit where the Worker's overtime grows, and my Agency and the Units concerned get an overtime alert (1.12).
- Iris sends each assigned Worker the Shift's site instructions by email and text, whichever they have, and again whenever the Unit changes them. Each assigned Worker shows when they were sent; for a Worker with no email or phone, I am told to pass them on myself.

*Covers: REQ-AGENCY-WEB-0006*

### 7.4 Swap or remove Workers

**As an Agency User**, I want to swap or remove assigned Workers until the Shift ends, **so that** I can cover call-offs.

- Swap replaces one Worker with another in one step; Remove reopens the place.
- Workers taken off are listed with the reason.
- After the Shift ends, the Workers are listed and cannot be changed here; a Worker who worked without being assigned is added from the hours upload (9.5).

*Covers: REQ-AGENCY-WEB-0006*

### 7.5 See the Workers a Unit asked for

**As an Agency User**, I want to see which Workers a Unit asked for by name and say when one cannot work, **so that** the Unit knows early.

- An unanswered or accepted Shift lists the Workers the Unit asked for.
- I can mark one unavailable with a reason.
- Requested Workers are marked and listed first when I assign, and I can still assign other Workers.

*Covers: REQ-AGENCY-WEB-0014*

### 7.6 Upload Worker assignments from a file

**As an Agency User**, I want to upload a file naming which Workers go on which Shifts, **so that** I can staff many Shifts at once.

- Upload assignments on the Shifts screen opens the upload step with the Shifts file type already picked.
- Each row names a Shift by its id and a Worker. A Worker can go only on a Shift we accepted. Iris finds the Worker by email, then phone; a row that matches only by name asks me to confirm that Worker or add a new one, a row that matches none of our Workers is proposed as a new Worker, and a row the assign list would refuse shows why.
- Iris assigns the Workers the accepted rows name, once I approve them.

*Covers: REQ-AGENCY-WEB-0012*

---

## 8. Workers and Credentials

### 8.1 Keep my Agency's Worker roster

**As an Agency User**, I want to keep a roster of my Agency's Workers, **so that** I can assign them to Shifts.

- The roster lists our Workers by last name with their name, email, phone, city, Positions, and whether active; it filters by active or inactive and by Position, and searches by name, email, or phone.
- Adding a Worker takes a first and last name and, optionally, email, phone, city, Positions, and a photo. An email or phone another of our Workers already has is refused.
- I can edit a Worker and deactivate or reactivate them; an inactive Worker is marked as one who cannot be assigned, and before deactivating I am warned they will come off Shifts that have not started.

*Covers: REQ-AGENCY-WEB-0003*

### 8.2 Upload Workers from a file

**As an Agency User**, I want to upload a file of Workers, **so that** I can add or change many at once.

- Upload Workers on the roster opens the upload step with the Workers file type already picked.
- A row with the email, or else the phone, of one of our Workers changes that Worker. A row that matches a Worker only by first and last name is never matched automatically: I pick that Worker or add a new one. Any other row adds a Worker.
- Iris saves the accepted rows once I approve them.

*Covers: REQ-AGENCY-WEB-0013*

### 8.3 Upload a Worker's Credentials

**As an Agency User**, I want to upload my Workers' Credential documents, **so that** they can work Shifts that require them.

- A Worker's page lists their Credentials by type, newest first, with the issuer, number, dates, status, the reason for that status or the reviewer's note, and the document.
- Uploading takes the Credential Type, the document, its expiry date where the type expires, and optionally the issuer, number, and issue date.
- A document sent without details is read by Iris, and I confirm or correct what it found. A document that names none of our Workers is flagged for me to fix; a Credential upload never adds a Worker.
- After upload Iris checks the document's expiry date, the issuer it names, and signs of editing, and verifies it, rejects it, or passes it to a Program User. A fourth check, with the issuer or a public registry, is skipped at launch because none is connected.
- Until it is verified a Credential does not count towards a Shift's requirements, and a verified one counts for a Shift only when it does not expire before the Shift's date.
- A saved Credential cannot be edited or deleted; a correction or renewal is uploaded as a new one.
- I can upload many Credentials at once from the roster, one file per Credential.

*Covers: REQ-AGENCY-WEB-0007*

### 8.4 Record an Attestation

**As an Agency User**, I want to state that a Worker meets a Credential Type, **so that** they can work where Compass accepts our word.

- Attesting takes the Credential Type, a statement, and optionally a date it is valid until; it adds a new Attestation and earlier ones stay listed, each with who attested and when.
- Only the latest Attestation of each type counts, and it is marked current or, after its valid-until date, lapsed.
- For a type that needs a verified document, the page says an Attestation alone does not make the Worker eligible.

*Covers: REQ-AGENCY-WEB-0007*

### 8.5 See which Workers need Credentials renewed

**As an Agency User**, I want to see which Workers have Credentials that need action or are in review, **so that** I renew them before Shifts are lost.

- Each roster row shows how many of the Worker's Credentials need action (rejected, expired, or expiring within the warning period, unless a newer one of that type exists) and how many are in review (still being checked by Iris or waiting for a Program User), and the roster filters to Workers counted in either.
- On a Worker's page, a verified Credential is labelled expired once past its expiry date, expiring when within the Credential expiry warning Setting (30 days by default), and replaced when a newer one of its type exists.
- When a verified Credential comes within the warning period, Iris warns every Agency User of my Agency once, by email and in the app, naming the Worker, the Credential Type, and the expiry date. No warning is sent for a Credential a newer one has replaced.
- The Worker's page also shows how many Shifts they have worked, each Unit's rating and review of them, which I cannot change, and the issues Units reported, each with its category and status.

*Covers: REQ-AGENCY-WEB-0007*

### 8.6 Decide which Credentials are required where

**As a Program User**, I want to define Credential Types and require them by part of the org, by Position, or both, **so that** only qualified Workers are assigned.

- Each type has a name and says whether an Attestation is enough or only a verified document counts, and whether it expires.
- A type can be deactivated and reactivated, not deleted; an inactive type stops being required and keeps its Credentials and Attestations.
- Credential Requirements list their type, the part of the org or every Unit, and the Position or every Position; I add or remove them, and one set on part of the org applies to every Unit under it.
- Before I add or remove a Credential Requirement, I am told eligibility is checked again, so Workers already assigned may come off Shifts that have not started.
- Picking a Unit and a Position shows every Credential Type a Shift there would require.

*Covers: REQ-PROGRAM-WEB-0004*

### 8.7 Decide Credentials Iris could not settle

**As a Program User**, I want to verify or reject each Credential Iris's checks could not settle, **so that** no Worker is held up or let through by mistake.

- The review queue lists those Credentials, oldest upload first, with the Worker, Agency, type, expiry, and why each needs review.
- Opening one shows the document beside the details the Agency gave, each check that failed or could not finish, and any registry reference.
- Verify and Reject each require a note, and I am told the decision is final.

*Covers: REQ-PROGRAM-WEB-0010*

### 8.8 Audit Agencies' Attestations

**As a Program User**, I want to see every Attestation every Agency made, **so that** I can check what they vouched for.

- Every Attestation is listed, including replaced ones, newest first, with the Worker, Agency, type, statement, valid-until date, who made it, and when, and filters by Agency, Worker, and type.
- The latest for each Worker and type is marked current or lapsed.
- I cannot add, change, or remove an Attestation.

*Covers: REQ-PROGRAM-WEB-0010*

### 8.9 See every Worker in the program

**As a Program User**, I want to see every Agency's Workers with the state of their Credentials, **so that** I can spot compliance gaps.

- Workers are listed by Agency, with counts of Credentials needing action and in review (as in 8.5); they filter by Agency, type, those counts, and active or inactive, and search by name.
- Opening a Worker shows their Credentials, Attestations, and each Unit's rating; a Credential waiting for a Program User's decision links to the review queue.
- The screen is read-only.

*Covers: REQ-PROGRAM-WEB-0012*

### 8.10 Rate the Workers who come to my Unit

**As a Unit User**, I want to rate Workers as favourite, okay to return, or blocked, **so that** I get the people I want back and not the ones I don't.

- The Workers screen lists everyone assigned to or rated by my Units, with their name, photo, Agency, Shifts worked at my Unit, my Unit's rating and review, and open issues, favourites first; it never shows a Worker's email or phone.
- Add a Worker finds any active Worker by Agency and name, so I can rate someone who has not yet been assigned to my Unit.
- A rating is for one Unit, takes an optional review, and replaces that Unit's earlier rating; I can give it at any time, from the roster or the Shift's page.
- Blocking first warns that the Worker comes off my Unit's Shifts that have not started and cannot be assigned or requested there. The Worker's Agency is told when a block takes them off a Shift.

*Covers: REQ-UNIT-WEB-0004*

### 8.11 Report an issue with a Worker

**As a Unit User**, I want to report an issue with a Worker to their Agency, **so that** the Agency deals with it.

- A report takes a category (conduct, safety, quality, or no-show), a description, and optionally the Shift, and can be made from the roster or the Shift's page.
- The Issues tab lists my Units' reports, open ones first, with the Agency's resolution.

*Covers: REQ-UNIT-WEB-0004*

### 8.12 Resolve issues Units report

**As an Agency User**, I want to see and resolve each issue a Unit reports about our Workers, **so that** the Unit sees we acted.

- The Issues tab lists each issue with the Worker, Unit, category, description, Shift, and date, open ones first.
- Resolve requires a note the Unit can read; a resolved issue shows who resolved it and when, and offers no further action.

*Covers: REQ-AGENCY-WEB-0008*

### 8.13 Issue badges at a secured Unit

**As a Unit User at a secured site**, I want to track each Worker's badge request, **so that** I know who still needs a badge and who has one.

- Iris raises a badge request when a Worker is first assigned at my secured Unit, and requests a revoked one again the next time that Worker is assigned there; I do not create one, and a badge's status never stops a Worker being assigned.
- A Badges tab, shown only when one of my Units is a secured site, lists badge requests, those still to issue first, with the Worker, Agency, status, and when it was requested.
- I mark a requested badge issued, or revoke a requested or issued one; the row then shows who did it and when.
- Each assigned Worker's badge status shows on the Shift's page.

*Covers: REQ-UNIT-WEB-0013*

---

## 9. Hours and Timesheets

### 9.1 See my Agency's Timesheets

**As an Agency User**, I want to see a Timesheet for each of our Workers on every ended Shift, **so that** I know what still needs submitting.

- Timesheets are listed by Shift, with the Worker, Unit, times, break, hours, tips, Expenses, and status, and open on those still to submit or sent back.
- A Timesheet sent back shows the Unit's reason; one still unapproved when its Lock Window closed is marked late until it is approved.
- A submitted or approved one shows any exceptions; an approved one shows whether Iris or the Unit approved it; a locked one shows a lock mark.

*Covers: REQ-AGENCY-WEB-0004*

### 9.2 Enter a Worker's hours

**As an Agency User**, I want to enter the clock times and break a Worker billed, **so that** the Timesheet is right before I submit it.

- While a Timesheet is a draft or sent back and is not marked a no-show, I can change its clock-in, clock-out, and break. Once it is submitted or approved, the whole page is read-only. The Bill Rates are never editable.
- The page shows the scheduled times beside the billed ones, the regular, overtime, and double-time hours, and the Bill Rate and amount for each.
- A Timesheet sent back shows the Unit's reason above the hours until I submit it again.
- Every change shows in its history, and each correction the Unit made shows its reason.
- When I change the hours, break, or no-show of a Timesheet that was sent back, or split it, the Unit is told by email and in the app (1.12).

*Covers: REQ-AGENCY-WEB-0009*

### 9.3 Mark a no-show or split hours by role

**As an Agency User**, I want to mark a Worker as a no-show or split their hours when they changed role mid-Shift, **so that** we bill what really happened.

- While a Timesheet is a draft or sent back, I can mark a no-show, and clear a mark an Agency User set; a mark the Unit set says so and only the Unit can clear it.
- Marking a no-show clears the clock times and break, so no hours are charged, and hours cannot be entered again until the mark is cleared.
- While a Timesheet is a draft or sent back, Split by role takes the switch time and the new Position, Department, or both, and can move some break minutes to the new part.
- Each part then shows its own rates, and the two parts' break minutes always add up to the original break.

*Covers: REQ-AGENCY-WEB-0009*

### 9.4 Submit Timesheets

**As an Agency User**, I want to submit Timesheets one by one or for a whole Shift, Event, or work date, **so that** the Unit can approve them as soon as the work ends.

- Each draft or sent-back Timesheet can be submitted, even with a missing clock time, which is marked.
- Submit all works for one Shift, one Event, or one work date at a Unit.
- After a bulk submit, any Timesheet left unsubmitted is listed with the reason.

*Covers: REQ-AGENCY-WEB-0004*

### 9.5 Load hours from a file or a sign-in sheet

**As an Agency User**, I want to upload hours from a template or a photo of a paper sign-in sheet, **so that** I do not retype them.

- Upload hours opens the upload step with the Timesheets file type picked, and takes the template, or a PDF, CSV, spreadsheet, or photo in any layout.
- Iris shows every line it read as a Proposal; the lines I accept are saved to draft and sent-back Timesheets, and no Timesheet is submitted.
- A line for one of our Workers who worked the Shift but was not assigned offers to add them to it, even beyond our headcount, and to add them to our roster if they are new. This is the only way to add a Worker after a Shift ends. Their Timesheet is flagged as added after the Shift, so it goes to the Unit's exception list instead of being approved automatically.

*Covers: REQ-AGENCY-WEB-0004*

### 9.6 Review Timesheets by exception

**As a Unit User**, I want clean Timesheets approved automatically and only the exceptions put in front of me, **so that** I review what matters.

- Iris approves a submitted Timesheet itself when its billed times are within the Approval Tolerance of the schedule (15 minutes by default) and it has no other exception; every other one stays submitted and shows on my exception list with its reasons.
- The Timesheets screen opens on that exception list, those outside the Approval Tolerance first, then the oldest Shift first. Other tabs list drafts and sent-back ones, approved ones, and locked ones.
- Each row shows the Worker, Agency, Shift, Position, Department, scheduled times beside billed times, break, regular, overtime, and double-time hours, Bill Rates, amount, tips, and Expenses. Each Timesheet opens its change history.
- Hours are never refused for overtime, and overtime alone does not stop automatic approval; I get an overtime alert instead (1.12).
- Each exception says what caused it, such as the minutes outside the Approval Tolerance or a short break.
- A Timesheet billed at a rate other than the contracted one shows both rates, the difference, and the reason given when the Shift was sent.
- An approved Timesheet locks once its Lock Window has passed (48 hours after the Shift ends by default), and never sooner than 24 hours after it was approved. One not yet approved does not lock.
- The parts of a split Timesheet show together; one still unapproved after its Lock Window closed is marked late on every tab; a locked one shows when it locked and allows no change.
- Once a Shift has ended, its page links to its Timesheets.

*Covers: REQ-UNIT-WEB-0003, REQ-UNIT-WEB-0016*

### 9.7 Approve Timesheets

**As a Unit User**, I want to approve Timesheets one at a time or for a whole Shift, Event, or work date, **so that** approval takes minutes, not hours.

- Approve is unavailable, with the reason, while a Timesheet has missing times or an Expense I have not decided.
- Approve all approves every submitted Timesheet shown for one Shift, one Event, or one work date at a Unit, then lists any left unapproved with the reason.

*Covers: REQ-UNIT-WEB-0003*

### 9.8 Correct or send back a Timesheet

**As a Unit User**, I want to correct a Timesheet's hours or send it back to the Agency, **so that** we pay only for the time worked.

- Correct changes the clock times and break of a submitted or approved Timesheet that has not locked, and requires a reason.
- For one outside the Approval Tolerance, Use scheduled times corrects it in one step, still with a reason.
- A corrected approved Timesheet stays approved; a corrected submitted one is checked again and may then be approved automatically.
- Reject sends a submitted Timesheet back to the Agency with a required reason, and is not offered on an approved one. The Agency is told by email and in the app, with my reason. It is also told of each correction or split I make, and whenever I set or clear a no-show, even on a draft (1.12).
- I can upload corrections from a file, with a reason on each row.

*Covers: REQ-UNIT-WEB-0015*

### 9.9 Mark a no-show or split hours as the Unit

**As a Unit User**, I want to mark a no-show or split hours by role myself, **so that** I can fix the record without waiting for the Agency.

- I can set or clear a no-show on any Timesheet that has not locked, including a draft or sent-back one and a mark the Agency set, with a reason.
- On a submitted or approved Timesheet that has not locked, Split by role takes the switch time, the new Position, Department, or both, any break minutes to move, and a reason. I cannot split a draft or sent-back one.

*Covers: REQ-UNIT-WEB-0015*

---

## 10. Tips and Expenses

### 10.1 Enter a Worker's tip

**As an Agency User**, I want to enter a tip for a Worker on their Timesheet, **so that** it reaches the Worker.

- While a Timesheet is a draft or sent back, I can enter, change, or remove a tip on it, and am told that it stops the Timesheet being approved automatically.
- Tips from a Tip Pool or a cashier PIN show with their source and cannot be changed by me.
- Tips pass through at the amounts entered: no state's tip tax rule is applied until Compass names the rules.

*Covers: REQ-AGENCY-WEB-0009, REQ-TIPS-0003*

### 10.2 Claim Expenses

**As an Agency User**, I want to add Expenses such as parking or background checks to a Timesheet, **so that** the cost is passed through to the Unit.

- An Expense takes a kind (parking, background check, or other), an amount, and a note, which "other" requires.
- While the Timesheet is a draft or sent back, I can add an Expense and change or delete one still pending. A decided Expense shows as approved, or rejected with the Unit's reason, and cannot be changed.
- I can upload Expenses from a file.

*Covers: REQ-AGENCY-WEB-0009, REQ-AGENCY-WEB-0004*

### 10.3 Decide Expenses and see tips

**As a Unit User**, I want to approve or reject each Expense and see each Timesheet's tips, **so that** we pay only what we agreed.

- Each pending Expense on a submitted Timesheet shows its kind, amount, and note with Approve and Reject; Reject requires a reason, and a decision cannot be changed.
- Tips show with their source: a Tip Pool share, a cashier PIN tip, or a tip the Agency entered.

*Covers: REQ-UNIT-WEB-0016*

### 10.4 Enter a Tip Pool

**As a Unit User**, I want to enter a day's tips for my Unit, a Shift, or an Event and have Iris split them, **so that** every Worker gets a fair share.

- A Tip Pool takes a Unit, a work date, an amount, and optionally one Shift or one Event, never both.
- Iris splits a pool across every Timesheet it covers by minutes worked, whatever the Agency. Scheduled minutes less the planned break count until hours are entered, and a no-show counts nothing. Shares are split again as hours change. A share is fixed once its Timesheet locks, and only the rest of the pool is split again among the Timesheets not yet locked. The shares add up to the pool, unless none of those Timesheets has minutes to count; the rest then shows as unallocated.
- Opening a pool shows each Worker's share and the minutes counted, marked as scheduled where hours are not yet entered, and any amount left unallocated.
- I am told in the app when a Timesheet change leaves part of a pool with no one to credit, and once per pool when a share locks while another Worker's hours are still missing.
- A pool can be changed or deleted until a Timesheet it covers locks, after which it shows as fixed; an open pool shows the last time it can be changed. A new pool or a change that would cover a locked Timesheet is refused, and says so.
- I can also upload tips from a file, or type a pool in the assistant and approve the split it proposes.

*Covers: REQ-UNIT-WEB-0012*

### 10.5 Credit cashier PIN tips

**As a Unit User**, I want tips entered under a cashier PIN to go to the Worker behind it, **so that** those tips reach the right Worker.

- A PIN tip takes a Unit, a work date, a cashier PIN, and an amount, and goes whole to that PIN's Worker.
- A PIN tip can be changed or deleted until the Timesheet it is on locks. One is refused when the PIN has no mapping for that Unit and date, or the Worker has no Timesheet there that is neither a no-show nor locked.
- If the Worker is later marked a no-show, the PIN tip stays on the Timesheet, counts as zero, and I am told in the app.
- A PIN map lists each PIN with its Unit, Worker, and dates; I add mappings and end them, but cannot change their PIN, Worker, or start date.

*Covers: REQ-UNIT-WEB-0012*

---

## 11. Reports

### 11.1 See my Unit's spend and compliance

**As a Unit User**, I want spend, labor cost, and Timesheet compliance reports for my Units, **so that** I can manage cost and catch problems.

- The Reports screen opens on a spend dashboard for my Units, or the one I picked: the month to date against the whole month's budget and the whole prior month, and the Work Week to date against the whole prior Work Week, each split into approved and pending spend, with the hours and headcount behind it.
- Tables break the month's spend down by Agency, with each Agency's average Bill Rate, by Position, and by Unit.
- Labor cost shows as a percentage of sales for a chosen period, counting spend and sales only on dates that have sales, and says not available when no date has any.
- Compliance shows, for a period, Timesheets with a missed break and Timesheets not approved by the end of their Lock Window, grouped as I choose. One approved after that still counts as late.
- A period is one Work Week, one calendar month, or a range of dates.
- My saved reports are listed here, and I can ask a question in the assistant.

*Covers: REQ-UNIT-WEB-0006*

### 11.2 See program-wide reports

**As a Program User**, I want to rank Agencies, Events, and Units by spend and see trends, **so that** I know where the money goes and how Agencies perform.

- For a period I pick, Agencies, Events, and Units are ranked by spend, highest first; each Agency also shows its fill rate and no-show rate.
- A trend chart shows spend, or another measure, by Work Week or calendar month.
- Compliance counts Timesheets with a missed break and Timesheets not approved by the end of their Lock Window, grouped as I choose; one approved after that still counts as late. Labor cost against sales shows for each Unit and for the Units together, counting only dates that have sales. Each Event shows its projected cost, its actual cost with any estimated part labelled as an estimate, and the difference.
- Every view can be narrowed to one Sector, Region, or District, and a figure with nothing to measure shows as not available.
- My saved reports are listed here, and I can ask a question in the assistant.

*Covers: REQ-PROGRAM-WEB-0005*

### 11.3 Load budgets and sales

**As a Program User**, I want to upload budgets and sales figures, **so that** spend can be measured against them.

- Upload sales and Upload budgets open the upload step with that file type picked.
- A sales row is one Unit and date; a budget row is one Unit and a range of dates. Iris checks each row and saves the accepted rows once I approve them.
- A data view lists what was loaded, by Unit and date, with the file it came from.

*Covers: REQ-PROGRAM-WEB-0005*

### 11.4 See every Shift in the program

**As a Program User**, I want to see every Shift at every Unit with its Agencies, Workers, and Timesheets, **so that** I can check how the program runs without changing anything.

- The Shifts screen lists every Shift by date, with its Unit, Position, times, headcount, Workers assigned, status, and the Agencies holding it. It opens on Shifts that have not ended, soonest first, and filters by part of the org, Agency, status, and dates.
- A flags filter finds Shifts sent off-contract or to a non-contracted Agency, or billed at a rate that differs from the contract.
- Opening a Shift shows each Agency's Bill Rates, the contracted rate and the difference, any reason given, its Workers, and its Timesheets.
- The screen is read-only.

*Covers: REQ-PROGRAM-WEB-0011*

### 11.5 Ask a question about spend or labor

**As a Unit User or a Program User**, I want to ask a question in plain words and get a chart or table, **so that** I get answers without building a report.

- The answer shows as a chart or table, or a dashboard for several measures, and says which measures, groupings, filters, and dates it used.
- When the question is unclear, Iris asks which measure or period I mean before showing numbers.
- Answers cover only my Units, or the whole program for a Program User, and never show a Pay Rate or a Markup.
- I can save an answer as a report and download its tables.
- A measure with nothing to measure shows as not available, never as zero or blank.
- An Agency User who asks is told reports are for Unit Users and Program Users.

*Covers: REQ-ASSISTANT-0004*

### 11.6 Keep my saved reports

**As a Unit User or a Program User**, I want to reopen, rename, and delete the reports I saved, **so that** I can check the same numbers again.

- My saved reports are listed newest first with their measures and period.
- Reopening one recomputes it from current data; a relative period, such as last month, shows the dates it covers today.
- With no saved reports, I am told I can save an answer from the assistant.

*Covers: REQ-SHELL-0012*

---

## 12. The assistant and uploads

### 12.1 Open the assistant from any page

**As a Unit User, an Agency User, or a Program User**, I want a chat panel on every page where I can type a request or attach a file, **so that** I can get work done without hunting for the screen.

- The panel opens over the page without leaving it.
- It opens with starters for my role, such as book a Shift or approve recent Timesheets for a Unit User, or upload Workers for an Agency User.
- An attached file is handled like an upload; if Iris cannot tell its type it asks, and if my role may not send it, it says who can.
- The panel lists my open Proposals each time it opens. The conversation lasts for my session; my uploads and open Proposals stay after I sign out.

*Covers: REQ-ASSISTANT-0001*

### 12.2 Ask Iris to make a change

**As a Unit User or an Agency User**, I want to type what I need, such as "book 4 servers Saturday", and get it prepared for me, **so that** routine work is quick.

- For a Unit User, Iris prepares bookings, changes to a Shift's headcount or times, cancellations of Shifts, Timesheet edits and approvals, and Tip Pools.
- For a booking, Iris asks for what I left out: which Unit, when I cover several, and which Agency should get each line, listing the Agencies approved for my Unit with their contracted Bill Rates. The Proposal shows each line's Agency and Bill Rate. Approving it books the Shifts and sends each line that has an Agency, at the contracted rate only; a non-contracted Agency needs a reason I add to the line.
- For an Agency User, Iris prepares Timesheet edits and submissions, a Worker's tip, Expenses, and Worker assignments.
- A Unit User or a Program User can also ask a question about spend or labor (11.5). No typed change is prepared for a Program User.
- The assistant itself saves nothing: each change comes back as a Proposal for me to approve.
- When my request is unclear or missing a detail, Iris asks before preparing anything.
- When my role cannot make the change, Iris says who can; when it cannot make the change at all, it says so.

*Covers: REQ-ASSISTANT-0003*

### 12.3 Approve what Iris prepared

**As a Unit User, an Agency User, or a Program User**, I want to review each change Iris prepared before it is saved, **so that** nothing happens without my say.

- A Proposal shows how many items are ready and how many need review; each problem shows the field, what is wrong, and a suggested fix, or the matching records to pick from when a name fits several, or fits a Worker by name alone.
- On an item that needs review I accept the fix, edit the values, or reject it, and I can accept every undecided item at once. An item with no problem can also be edited or rejected.
- Apply says how many items it will save and is disabled while a problem is undecided; Reject all saves nothing.
- After apply, I see how many were saved, a link to the screen that lists them, and any that failed a final check, with the reason. A decided Proposal is read-only; I retry a failed item by sending the file or request again.
- Only the person a Proposal was made for can open it.

*Covers: REQ-ASSISTANT-0002*

### 12.4 Send files and follow my uploads

**As a Unit User, an Agency User, or a Program User**, I want one page to send files, get templates, and follow what became of each upload, **so that** I always know where my data stands.

- I pick an upload type my role may send, download its template as CSV or Excel where the type has one, and send a file, or let Iris detect the type.
- The upload log lists every file I sent, however I sent it: on this page, in the assistant, or attached to an email or text. In MVP only a Unit User can send files by email or text.
- An upload awaiting review opens its Proposal; a saved or discarded one opens its Proposal read-only; one whose type is unclear asks me to pick it; a failed one shows why.
- Other screens open this step with the type already picked, and the Uploads menu item shows how many uploads need me.

*Covers: REQ-SHELL-0008*

---

## Open questions behind these stories

These stories assume answers that Compass and Instawork have not yet confirmed. If an answer differs, the stories named here change.

| Question | What the stories assume | Stories |
| --- | --- | --- |
| Can one Shift go to more than one Agency? | Yes, by hand: a Unit User sends each part of the headcount to one Agency. Automatic sending to several Agencies comes later. | 5.1, 6.1, 6.4, 7.1 |
| Do break and minimum-wage checks at booking flag a Shift or block it? | They flag it. Only overtime can be set to block. | 5.1 |
| Who can change a Timesheet, and when? | The Agency edits drafts and sent-back Timesheets; the Unit corrects submitted and approved ones until they lock, and a corrected approved one stays approved; on a draft or sent-back one the Unit may change only the no-show mark; nobody changes a locked one. | 9.2 to 9.9, 10.1, 10.2 |
| Who verifies Workers' Credentials? | Iris checks each document automatically; a Program User decides what the checks cannot settle and sets, per Credential Type, whether an Attestation is enough. | 2.4, 8.3 to 8.9 |
| What happens to a Timesheet still unapproved when its Lock Window closes? | It stays open and shows as late to the Unit and the Agency until it is approved. Only an approved Timesheet locks. | 2.2, 2.3, 9.1, 9.6, 11.1, 11.2 |
| Who manages users? | Program Users manage everyone; Agency Users manage their own Agency's users. Every account except an Instawork Admin's exists only by invite. | 1.1, 1.7, 3.10 to 3.13 |
| Who may change a live rate? | Agencies and Program Users submit new lines; a Program User approves Agency lines, and their own need no second approval. | 2.4, 4.2 to 4.5, 4.7, 4.8 |
| Can a rate be set for one Unit? | Yes: a Rate Line can price a Position at one Unit, and it wins over the Market rate for that Agency. This waits on a Foodbuy decision. | 4.1, 4.8 |
| Who acts on rates flagged above their peers or off the contract? | Program Users see every flag and send Rate Reviews; Unit Users see the flags on their own Shifts and Timesheets. | 2.4, 4.5, 4.6, 6.3, 9.6, 11.4 |
| How is overtime counted when a Worker works at several Units or for several Agencies? | Per Worker per Agency: hours at every Unit that Agency sends them to count together, and hours with other Agencies are not combined. | 7.3, 9.6 |
| Who keeps Positions, Markets, and labor rules? | Instawork Admins, who are set up from the deployment configuration, never by invite. | 3.1 to 3.4, 3.12 |
| Who keeps the org, Units, Agencies, and Settings after launch? | Program Users only. A Unit User may change only the default site instructions of a Unit they cover and of its Departments. | 3.7 to 3.11, 3.14, 3.15 |
| Which tip tax rules apply at launch? | None until Compass names them; tips pass through at the amounts entered. This question is blocking. | 10.1, 10.3 to 10.5 |

The full list of open questions, by who must answer each, comes from `python tools/list_decisions.py --markdown`.
