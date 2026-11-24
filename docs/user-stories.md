# Iris user stories: MVP

Iris is Instawork's vendor management system for Compass. Compass locations order temporary staff, approved staffing Agencies fill the Shifts with their own Workers, and Iris checks rates, credentials, and hours along the way.

This document lists what each kind of user needs from the MVP, as user stories grouped by journey. Each story ends with the requirements in the [requirements graph](../README.md) that it covers, where the full detail lives.

**Status: draft.** No requirement behind these stories is approved yet, and the stories assume answers to open questions that Compass and Instawork have not yet given. The ones most likely to change a story are listed at the end.

## Who uses Iris

| User | Who they are | What they do in Iris |
| --- | --- | --- |
| Unit User | A Compass manager at a location, such as Soldier Field | Books Shifts, sends them to Agencies, approves hours, rates Workers |
| Agency User | Staff at a staffing Agency | Answers Shifts sent to the Agency, assigns Workers, submits hours, keeps rates and credentials |
| Program User | Compass's program team | Sets up the org, Agencies, rates, and credential rules, and watches spend |
| Instawork Admin | Instawork staff | Keeps reference data and invites the first Program User |

## Words used

- **Unit:** a Compass location that orders Shifts, such as a stadium or a hospital. A **Department** is a cost center inside it, such as suites or concessions.
- **Request:** one booking of one or more **Shifts**. A Shift is one Position at one Unit, from a start time to an end time, for a headcount.
- **Release:** part or all of a Shift's headcount sent to one Agency, and that Agency's answer.
- **Rate Line:** an Agency's regular, overtime, and double-time Pay Rates and Bill Rates for one Position in one Market or at one Unit. The **Pay Rate** is what the Agency pays the Worker; the **Bill Rate** is what Compass pays the Agency; the **Markup** is the gap between them.
- **Peer Rate:** the average regular Bill Rate other Agencies hold for the same Position and Market. A **Rate Review** asks an Agency to lower or justify a rate above it.
- **Credential:** a document proving a Worker meets a requirement, such as a food handler card. An **Attestation** is the Agency's statement that a Worker meets one.
- **Timesheet:** the hours one Worker billed for one Shift.
- **Event:** a named occasion at a Unit, such as a banquet, that groups Shifts so their cost is seen as one.
- **Tip Pool:** tips for a Unit and date, or for one Shift or Event, split across Workers by hours worked.
- **Proposal:** changes Iris prepared from a file or a typed request, which a person approves before anything is saved.

## Journeys

1. [Sign in and find your way](#1-sign-in-and-find-your-way)
2. [Home and to-dos](#2-home-and-to-dos)
3. [Set up the program](#3-set-up-the-program)
4. [Rates](#4-rates)
5. [Order labor](#5-order-labor)
6. [Send Shifts to Agencies](#6-send-shifts-to-agencies)
7. [Answer and staff Shifts](#7-answer-and-staff-shifts)
8. [Workers and credentials](#8-workers-and-credentials)
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
- There is no sign-up: an account exists only when someone invites me.
- Opening any page while signed out shows the sign-in page.

*Covers: REQ-SHELL-0004*

### 1.2 Set my password from an invite or a reset link

**As any user**, I want to set my password from the link I was emailed, **so that** I can accept an invite or get back in when I forget it.

- The sign-in page links to a reset page that takes my email and always shows the same message, whether or not the email has an account.
- A valid link shows my email, which I cannot change, and asks for a new password of at least 12 characters.
- A used, expired, or unknown link, or one for a deactivated account, says it no longer works and offers a new reset.
- Once the password is saved, I am sent to sign in.

*Covers: REQ-SHELL-0005*

### 1.3 Choose the role I am acting in

**As a user with more than one role**, I want to pick which role I am working in and switch without signing out, **so that** I see the right screens and records for the job in hand.

- I act in one role at a time: all my Unit access together, each Agency on its own, or the whole program.
- With one role I go straight in; with several I choose at each sign-in and can switch from any page.
- Every page shows the role I am acting in and its scope, such as the Agency's name or the Units I cover.
- If none of my access is current, I see a page saying I have no access, with only sign out.

*Covers: REQ-SHELL-0002*

### 1.4 See only the screens my role can use

**As any user**, I want a menu with only my role's screens, **so that** I never land on work that is not mine.

- Every signed-in page has the same frame: the menu, the page name, and an account menu with my name, email, and sign out.
- The menu lists, in order:
  - Unit User: Home, Shifts, Timesheets, Tips, Workers, Agencies, Events, Reports, Uploads, Setup.
  - Agency User: Home, Shifts, Workers, Timesheets, Rate Card, Uploads, Users.
  - Program User: Home, Shifts, Workers, Rates, Credentials, Agencies, Org, Users, Reports, Uploads, Settings.
  - Instawork Admin: Home, Positions, Markets, Labor rules, Account team, Outside ids.
- Opening a record outside my access shows a refusal and a link to Home, and nothing of the record.
- When my session ends or my account is deactivated, I am returned to the sign-in page.

*Covers: REQ-SHELL-0009, REQ-UNIT-WEB-0001, REQ-AGENCY-WEB-0001, REQ-PROGRAM-WEB-0001, REQ-ADMIN-WEB-0001*

### 1.5 Narrow my screens to one Unit

**As a Unit User who covers several Units**, I want to narrow every Unit screen to one Unit, **so that** I can focus on one location.

- I see all my Units together by default.
- Picking one Unit narrows every Unit screen to it, and the choice stays until I change it or sign out.

*Covers: REQ-UNIT-WEB-0001*

### 1.6 Work from my phone

**As a Unit User or an Agency User**, I want every page to work in my phone's browser, **so that** I can work on the go with no app to install.

- Every page, including sign-in, works in a phone browser.
- No page scrolls sideways on a small phone; a wide table scrolls inside its own area.
- The menu folds behind one button, and every desktop action is still available.
- I can send a file from my phone, including a photo of a paper sign-in sheet.

*Covers: REQ-SHELL-0001*

### 1.7 Keep my profile up to date

**As any user**, I want to see my profile and change my name and phone, **so that** my details are right.

- My profile shows my name, email, phone, and each role I hold with its scope.
- I can change my name and phone; my email is shown but cannot be changed.
- Change password emails me a reset link.
- I cannot change my own roles or deactivate myself.

*Covers: REQ-SHELL-0006*

### 1.8 Read my notifications

**As any user**, I want an inbox of my in-app notifications, **so that** I can catch up on what happened and go straight to it.

- Every page shows how many notifications I have not read.
- The inbox lists my notifications for every role I hold, newest first.
- Opening one marks it read and opens the record it is about.

*Covers: REQ-SHELL-0007*

### 1.9 Download any table

**As any user**, I want to download any table as a CSV file, **so that** I can work with the data elsewhere.

- Every table has a download that holds exactly the rows and columns I see, with my filters and sort, across every page of results.
- A column my role may not see, such as a Pay Rate for a Unit User, is never in the file.

*Covers: REQ-SHELL-0010*

### 1.10 See who changed a record

**As a Unit User, an Agency User, or a Program User**, I want to see a record's change history, **so that** I know who changed what, when, and why.

- Each entry shows when, who (or Iris for an automatic change), how the change came in, each field's old and new value, and any reason.
- The history can only be read.
- A field my role may not see, such as a Pay Rate, is left out.

*Covers: REQ-SHELL-0011*

### 1.11 Every screen behaves the same way

**As any user**, I want refusals, empty lists, times, and money to look the same on every screen, **so that** I do not have to relearn each one.

- When Iris refuses an action, the reason shows beside it and what I typed is kept.
- I am only offered actions my role may take on a record in its current state.
- Where a reason is required, I cannot confirm until I give one.
- An empty list says so, says when my filters are the cause, and offers to clear them.
- Shift, Timesheet, and tip times show in the Unit's own time zone, and money shows in dollars to the cent.

*Covers: REQ-SHELL-0013*

---

## 2. Home and to-dos

### 2.1 Start from my to-do list

**As a Unit User, an Agency User, or a Program User**, I want my Home page to open on what I need to do next, **so that** nothing waits on me unnoticed.

- Home has one line for each kind of task, with how many are waiting and what is at stake: a dollar amount, the oldest one's age, or the nearest deadline.
- Each line opens the screen where the work is done, filtered to exactly those records.
- A record leaves the count as soon as its task is done, and a task with nothing waiting shows no line.
- The Home item in the menu shows the total waiting.
- Counts cover only the records my role and scope can see.

*Covers: REQ-SHELL-0003*

### 2.2 Unit User Home

**As a Unit User**, I want my Home to show my to-dos and how spend is tracking, **so that** I can act on the day and keep within budget.

- To-dos: Timesheets to review, with their total billed amount and how many are late; headcount not yet sent to an Agency, with the time until the earliest Shift starts; and badge requests to issue at secured Units.
- Below the to-dos, a spend summary shows the month to date against budget and the prior month, and the week to date against the prior week, each split into approved and pending spend.
- The summary links to the Reports screen for the breakdowns.

*Covers: REQ-UNIT-WEB-0014, REQ-UNIT-WEB-0001*

### 2.3 Agency User Home

**As an Agency User**, I want my Home to list everything the Agency must do next, **so that** we answer, staff, and bill on time.

- Seven to-dos: Releases to answer, Releases to staff, Timesheets to submit, Timesheets sent back, Credentials to renew, Rate Reviews to answer, and Worker issues to resolve.
- Releases show the time until the earliest Shift starts; Timesheets show the oldest one's age and how many are late; Credentials show the earliest expiry date.
- Each line opens the matching screen filtered to those records.

*Covers: REQ-AGENCY-WEB-0011, REQ-AGENCY-WEB-0001*

### 2.4 Program User Home

**As a Program User**, I want my Home to show my approvals and which Units are spending most, **so that** I can keep the program on contract and on budget.

- To-dos: Credentials to review, Agency rate changes to approve, and rates above their peers that have never been reviewed, with the largest gap in dollars.
- Below the to-dos, every Unit is ranked by this month's spend, with approved and pending spend, spend against the Unit's normal level, and how many Shifts went off-contract or to a non-contracted Agency.
- The ranking can be narrowed to one Sector, Region, or District, and selecting a Unit opens its Shifts.

*Covers: REQ-PROGRAM-WEB-0013, REQ-PROGRAM-WEB-0001*

---

## 3. Set up the program

### 3.1 Get the program started

**As an Instawork Admin**, I want to see what reference data is loaded and invite the first Program User, **so that** Compass can take over its own setup.

- Home shows how many active Positions, Markets, and labor rules in effect today are loaded.
- Until a Program User is in place, Home offers an invite for one, and lists unaccepted invites with Send again and Revoke.
- Once a Program User has accepted, Home names them and offers no further invite.
- Home lists the other Instawork Admins and lets me deactivate or reactivate them.

*Covers: REQ-ADMIN-WEB-0001, REQ-PROGRAM-WEB-0007*

### 3.2 Keep the Position catalog

**As an Instawork Admin**, I want to add, rename, and deactivate Positions, **so that** every Shift, rate, and credential rule names a Position from one list.

- Positions are listed with whether each is active.
- A name another Position already has is refused.
- Before deactivating, I am told the Position can no longer be chosen for new Shifts or rates but stays on existing records.

*Covers: REQ-ADMIN-WEB-0002*

### 3.3 Keep Markets and their ZIP codes

**As an Instawork Admin**, I want to keep Markets and the ZIP codes in each, **so that** every Unit is priced in the right Market.

- Markets are listed by state and city, with how many ZIP codes each has.
- I add and rename a Market by city and state, and add or remove its ZIP codes.
- A ZIP code another Market already holds is refused.

*Covers: REQ-ADMIN-WEB-0003*

### 3.4 Keep state and local labor rules

**As an Instawork Admin**, I want to keep the break, minimum wage, and overtime rules for each state and city, **so that** Iris checks Shifts and hours against the law where they are worked.

- Rules are listed by state, city, and kind, with their values and the dates they apply, and filter by state and kind.
- I add, change, and end a rule.
- A new rule for the same state, city, and kind is refused until the earlier one is ended.

*Covers: REQ-ADMIN-WEB-0004*

### 3.5 Name Instawork's account team

**As an Instawork Admin**, I want to name the Account Manager, Account Owner, and Support Lead for the program or any part of the org, **so that** every Unit knows whom at Instawork to contact.

- The screen shows the program-wide team, then each part of the org with its own assignments.
- Assigning a role at a place replaces whoever held it there; removing one asks for confirmation.
- Opening a Unit shows who it resolves to for each role, and where that assignment comes from.
- A Unit User sees their Unit's account team, with names, emails, and phones, on the Setup screen.

*Covers: REQ-ADMIN-WEB-0005, REQ-UNIT-WEB-0011*

### 3.6 Keep the ids other systems use

**As an Instawork Admin**, I want to record the Fieldglass, SAP, and MyStaff ids of Units, Departments, Companies, Agencies, and Positions, **so that** files and data from those systems match the right Iris records.

- I pick a system and a record type and see every record with its id there, or none.
- I can search, and show only records with no id yet.
- An id another record already holds is refused, naming that record.

*Covers: REQ-ADMIN-WEB-0006*

### 3.7 Build the org tree

**As a Program User**, I want to keep Compass's org as a tree of Sectors, Regions, Districts, and Units, **so that** access, rules, and reports follow how Compass is organised.

- The Org screen shows the tree, with whether each part is active.
- I add, rename, deactivate, and reactivate Sectors, Regions, and Districts.
- A Sector, Region, or District can be deactivated only when everything beneath it is inactive.

*Covers: REQ-PROGRAM-WEB-0002*

### 3.8 Add and change Units and Departments

**As a Program User**, I want to add Units with their Departments and keep their details, **so that** Shifts can be booked, priced, and charged to the right cost center.

- A new Unit takes its name, address, Company, Work Week start day, optional time zone, whether it is a secured site, its default site instructions (parking, entrance, directions, site contact, attire), and at least one Department.
- Iris sets the Unit's Market and time zone from its ZIP code and shows them.
- Each Unit lists its Departments with their cost center codes, addresses, and whether active; I add, rename, and deactivate them.
- A new Department starts with the Unit's address and site instructions, which I can change.
- I can change or deactivate a Unit; an inactive Unit takes no new Request.
- A Unit's page shows its account team and its primary operator, picked from its Unit Users.

*Covers: REQ-PROGRAM-WEB-0002*

### 3.9 Upload Units from a file

**As a Program User**, I want to upload a file of Units and Departments, **so that** I can set up many locations at once.

- Upload Units on the Org screen opens the upload step with the Units file type already picked.
- Iris checks each row and saves the accepted Units and Departments once I approve them.

*Covers: REQ-PROGRAM-WEB-0014*

### 3.10 Add Agencies and approve where they work

**As a Program User**, I want to add Agencies and approve each one for parts of the org, **so that** Units send Shifts only to Agencies Compass has contracted.

- A new Agency takes its name and a first contact, who is invited as its first Agency User.
- I can rename or deactivate an Agency; an inactive Agency receives no new Shifts.
- I approve an Agency at a Sector, Region, District, or Unit, and its page lists each approval with who made it and when.
- Before removing an approval, I am told that Shifts already sent do not change.

*Covers: REQ-PROGRAM-WEB-0006*

### 3.11 Upload Agencies from a file

**As a Program User**, I want to upload a file of Agencies, **so that** I can add many Agencies, their first contacts, and their approvals at once.

- Upload Agencies on the Agencies screen opens the upload step with the Agencies file type already picked.
- Iris saves the accepted Agencies, contacts, and approvals once I approve them.

*Covers: REQ-PROGRAM-WEB-0015*

### 3.12 Manage users and their roles

**As a Program User**, I want to invite users and grant or revoke their roles, **so that** the right people have the right access.

- The Users screen lists every user with their roles and scopes, whether their invite was accepted, and their last sign-in, and filters by role, Agency, part of the org, and active or inactive.
- An invite takes the person's name, email, optional phone, and one role: Program User, Unit User for a part of the org, or Agency User for one Agency.
- Picking a Unit User scope says it covers every Unit at or below that point.
- I can add a role, revoke or restore one, resend an invite, and deactivate or reactivate a user.

*Covers: REQ-PROGRAM-WEB-0007*

### 3.13 Manage my Agency's own users

**As an Agency User**, I want to invite colleagues and remove their access, **so that** my Agency controls who works in Iris for it.

- The Users screen lists everyone with access to my Agency, whether they accepted their invite, and their last sign-in.
- I can invite a colleague only as an Agency User for my Agency, resend an invite, and revoke or restore access.
- I can deactivate a colleague only if they hold no access beyond my Agency.

*Covers: REQ-AGENCY-WEB-0010*

### 3.14 Change Settings for the program or part of it

**As a Program User**, I want to change Settings for the whole program and override them for parts of the org, **so that** rules such as the Timesheet approval tolerance and lock window fit how each part of Compass works.

- Every Setting is listed with what it means, its program default, and any overrides by Sector, Region, District, or Unit.
- Some Settings, such as the Peer Rate threshold and the credential expiry warning, apply program-wide and take no override.
- Removing an override shows the value that now applies instead.
- Picking a Unit shows the value of every Setting in force there.

*Covers: REQ-PROGRAM-WEB-0008*

### 3.15 Keep my Unit's site instructions

**As a Unit User**, I want to keep the default site instructions for my Unit and its Departments, **so that** Agencies and Workers know where to park, enter, and report.

- The Setup screen shows the Unit's default parking, entrance, directions, site contact, and attire, and each Department's, and I can change them.
- The Unit's address, time zone, Company, Work Week start, secured-site flag, and Departments are shown read-only.

*Covers: REQ-UNIT-WEB-0011*

---

## 4. Rates

### 4.1 See every Agency's rates

**As a Program User**, I want one list of every Agency's rates that I can filter and sort, **so that** I can compare rates without lining Agencies up side by side.

- Each Rate Line shows its Agency, Position, Market or Unit, all six rates, the Markup, its dates, and its status.
- The list opens on rates in effect today, filters by Market, Position, Agency, Unit, and status, and sorts by any rate.
- A History tab lists every line ever entered, including replaced and rejected ones, each with its change history.

*Covers: REQ-PROGRAM-WEB-0003*

### 4.2 Enter, change, and end rates

**As a Program User**, I want to enter and change rates for any Agency, **so that** contracted rates are in Iris before Shifts are sent.

- A rate I enter is approved at once.
- Changing a line adds a new line from its start date, which ends the old one; history is kept.
- I can end a line with an end date and a reason.

*Covers: REQ-PROGRAM-WEB-0003*

### 4.3 Upload a rate card

**As a Program User**, I want to upload a rate card file for any Agency, **so that** I can enter many rates at once.

- Upload rates on the Rates screen opens the upload step with the rate card file type already picked.
- Each row names its Agency, and each accepted row is saved as an approved rate.

*Covers: REQ-PROGRAM-WEB-0016*

### 4.4 Keep my Agency's rate card

**As an Agency User**, I want to see my Agency's rates and submit new or changed ones, **so that** Compass pays us the rates we agreed.

- The Rate Card lists my Agency's lines with their Pay Rates, Bill Rates, Markup, dates, and status. It never shows the Peer Rate or another Agency's rates.
- A new or changed line, by form or by file, waits as pending until a Program User approves it or sends it back; the current line stays as it is meanwhile.
- A line sent back shows the reason and can be submitted again.
- A History tab lists every line my Agency ever submitted, with its change history.

*Covers: REQ-AGENCY-WEB-0005*

### 4.5 Approve Agency rate changes

**As a Program User**, I want to approve or send back each rate an Agency submits, **so that** no rate takes effect without Compass's say.

- The approval queue lists pending lines, oldest first, each beside the line it would replace, the change in each rate, and the Agency's reason.
- A Market line also shows the Peer Rate and whether its regular Bill Rate would be flagged above it.
- Approve makes the line live; Send back requires a reason.
- A line dated before the one it would replace cannot be approved, only sent back.

*Covers: REQ-PROGRAM-WEB-0009*

### 4.6 Spot rates above their peers and ask for a review

**As a Program User**, I want rates above their peers highlighted, and to ask the Agency to lower or justify them, **so that** Compass does not overpay.

- Each Market rate in effect today shows its Peer Rate, and a line above it by the threshold or more is highlighted with the gap in dollars and percent.
- A line with no Peer Rate is never highlighted.
- A highlighted line offers Send Rate Review; a line under review shows the review's status instead.
- A Rate Reviews tab lists every review, open ones first, with the Agency's answer.

*Covers: REQ-PROGRAM-WEB-0009*

### 4.7 Answer a Rate Review

**As an Agency User**, I want to see when Compass questions one of our rates and answer it, **so that** we can keep the rate with a reason or lower it.

- Open reviews show above the Rate Card, each with the line under review and a statement that its rate is above its peers.
- Keep the rate requires a reason; Lower the rate opens the form for a new, lower line.
- A review answered with a lower line closes as lowered once that line is approved.

*Covers: REQ-AGENCY-WEB-0005*

### 4.8 See which Agencies I can use and what they charge

**As a Unit User**, I want to see the Agencies my Unit can use and their Bill Rates, **so that** I know my options before I send a Shift.

- For one Unit at a time, every active Agency is listed, those approved for the Unit first, each marked approved or non-contracted.
- Opening an Agency shows its current and upcoming Bill Rates for the Unit by Position, with the contracted rate marked where a Unit rate and a Market rate both apply.
- A Position view lists each Agency's contracted regular Bill Rate, lowest first.
- I see Bill Rates only, never Pay Rates or Markup, and I cannot change anything here.

*Covers: REQ-UNIT-WEB-0005*

---

## 5. Order labor

### 5.1 Book a Request

**As a Unit User**, I want to book one Request with a line for each Position, **so that** I can order a whole crew in one go.

- Each line takes a Position, Department, date, start and end time, headcount, and optionally a planned break, from active records in my scope.
- Each line's site instructions start from its Department's defaults and can be changed for that line.
- An end time before the start asks me to confirm the Shift ends the next day.
- Each line can be sent to an Agency as I book it, or left unsent.
- Break and minimum-wage concerns show as flags on the line but never stop the booking.
- If a line is refused, nothing is booked and the line shows why. If the booking succeeds but a send is refused, that Shift stays unsent and shows why.

*Covers: REQ-UNIT-WEB-0002*

### 5.2 Book from a template

**As a Unit User**, I want to save Requests I book often as templates, **so that** I can book a regular crew in a few clicks.

- The Setup screen lists my Unit's templates with their lines, and I create, change, and delete them.
- Book on a template, or Start from template on the booking form, fills the lines for the date I pick.
- I can set a default Department for each Position, which fills in when I pick that Position.

*Covers: REQ-UNIT-WEB-0011*

### 5.3 Repeat a Request every week

**As a Unit User**, I want a Request to repeat on chosen weekdays, **so that** recurring Shifts are booked once.

- The booking form takes the weekdays, how many weeks apart, and an end date.
- The Shifts of a repeating line show as a series.
- I can send the whole series to an Agency in one step, and see any Shift whose send was refused.
- Editing or cancelling a Shift in a series asks whether to apply it to this Shift or to every Shift in the series not yet started.

*Covers: REQ-UNIT-WEB-0017*

### 5.4 Overbook a Shift

**As a Unit User**, I want to book more Workers than I need and record how many I need, **so that** no-shows do not leave me short.

- Each booking line takes a needed headcount below its headcount.
- The Shift's page shows both numbers, and I can change the needed headcount there.

*Covers: REQ-UNIT-WEB-0018*

### 5.5 Upload Shifts from a file

**As a Unit User**, I want to upload a file of Shifts, **so that** I can create or change many Shifts at once.

- Upload Shifts on the Shifts list opens the upload step with the Shifts file type already picked.
- Iris checks each row and saves the accepted Shifts once I approve them.

*Covers: REQ-UNIT-WEB-0019*

### 5.6 See my Shifts by date

**As a Unit User**, I want to see my Units' Shifts by date with how full each is, **so that** I know where I am still short.

- Shifts are grouped by date: upcoming ones first, soonest first, then past ones.
- Each Shift shows its Position, Unit, Department, times, Workers assigned against headcount, the Agencies holding it, and its status.
- An upcoming Shift with headcount not yet sent shows how much.
- The list filters by Unit, dates, Position, Agency, status, and unsent headcount. Cancelled Shifts stay listed, marked cancelled.

*Covers: REQ-UNIT-WEB-0007*

### 5.7 Follow and change one Shift

**As a Unit User**, I want one page per Shift showing who is coming and letting me change it, **so that** I can manage the Shift up to the day.

- The page shows the Shift's details and site instructions, each Agency it was sent to with its answer and rates, and each assigned Worker by name, photo, and Agency, with any open places.
- Each assigned Worker shows whether they are eligible for the Shift.
- Workers taken off the Shift are listed with the reason and time.
- Until the Shift ends I can edit its headcount, date, times, break, and site instructions; until it starts I can cancel it after confirming.
- Once the Shift has ended, edit, cancel, and send are gone.
- The page shows the Shift's change history.

*Covers: REQ-UNIT-WEB-0008*

### 5.8 Group Shifts into Events and see what each costs

**As a Unit User**, I want to group Shifts under a named Event and see its projected and actual cost, **so that** I know what each event really cost.

- I create and rename Events for a Unit, and attach Shifts to an Event when booking, from the Shift's page, or from the Event.
- The Events screen lists each Event with its dates, number of Shifts, projected cost, actual cost, and the difference.
- Actual cost shows approved and pending spend, with any estimated part labelled as an estimate.
- From an Event I can open the Timesheets screen filtered to it and approve them together.

*Covers: REQ-UNIT-WEB-0010*

---

## 6. Send Shifts to Agencies

### 6.1 Pick an Agency and send a Shift

**As a Unit User**, I want to pick an Agency at its contracted rate and send it a Shift's headcount, **so that** the Shift gets staffed at the agreed price.

- The send step lists the Agencies approved for my Unit with their contracted rate for the Shift, lowest first, then any non-contracted Agencies.
- Picking an Agency fills in its contracted rate and the unsent headcount, which I can lower.
- Before I send, I see whether the send would be refused and why.
- If the Agency already holds this Shift, the headcount is added to what it holds, at the rates already sent.
- A refused send saves nothing.

*Covers: REQ-UNIT-WEB-0009*

### 6.2 Send at another rate or to a non-contracted Agency

**As a Unit User**, I want to send at a rate other than the contracted one, or to an Agency not contracted for my Unit, when I give a reason, **so that** I can still fill a Shift when the usual options fall short.

- I can type another regular Bill Rate, and must when there is no contracted rate; either way a reason is required, and the send is refused where Compass's settings do not allow off-contract rates.
- Sending to a non-contracted Agency asks for a second reason where Compass's settings allow it, and is refused where they do not.
- When I add headcount to a Shift an Agency already holds, I am asked only for reasons it does not already have.

*Covers: REQ-UNIT-WEB-0009*

### 6.3 See when a rate is above its peers

**As a Unit User**, I want to be warned when the rate I am about to send is above what other Agencies charge, **so that** I can choose a better-priced Agency.

- The send step flags a regular Bill Rate that is above the Peer Rate by Compass's threshold or more.

*Covers: REQ-UNIT-WEB-0020*

### 6.4 Send more headcount or pull a Shift back

**As a Unit User**, I want to send remaining headcount from the Shift's page and withdraw a Shift an Agency has not answered, **so that** I can react as plans change.

- Unsent headcount shows on the Shift's page with Send.
- After the Shift starts, I can send more only to Agencies that already accepted it.
- An Agency that has not answered yet can have its Shift withdrawn.

*Covers: REQ-UNIT-WEB-0008, REQ-UNIT-WEB-0009*

### 6.5 Ask for Workers by name

**As a Unit User**, I want to ask an Agency for particular Workers, **so that** people who know my site come back.

- When sending, or later on the Shift's page, I can name Workers from the Agency's active Workers, with my favourites first and Workers I blocked left out.
- The Shift's page shows each Worker I asked for, and whether the Agency said they are unavailable and why.
- I can withdraw a request until the Shift starts.

*Covers: REQ-UNIT-WEB-0021*

---

## 7. Answer and staff Shifts

### 7.1 See the Shifts sent to my Agency

**As an Agency User**, I want to see every Shift sent to my Agency with what it pays and where to go, **so that** I can decide what to take on.

- The Shifts screen lists each Shift sent to us with its Unit, Position, date, times, headcount, Workers assigned, and status, grouped by date. It opens on open and accepted Shifts that have not ended, soonest first, and filters by status, Unit, Position, and dates.
- Opening one shows the Unit's name and address, the Shift's times and break, our headcount, and our regular, overtime, and double-time Bill Rates.
- While it is open or accepted, it also shows the site instructions.
- It shows our headcount beside the Shift's total, and how much other Agencies hold, never their names.

*Covers: REQ-AGENCY-WEB-0002*

### 7.2 Accept or decline a Shift

**As an Agency User**, I want to accept or decline each Shift, one at a time or several at once, **so that** the Unit knows quickly whether we can staff it.

- Accept takes the whole headcount we were sent.
- Decline requires a reason, and is possible after accepting until the Shift starts; I am first told how many assigned Workers will come off it.
- I can select several open Shifts, such as a run of days, and answer them in one step; any that cannot be answered are listed.
- A Shift that was declined, withdrawn, cancelled, or expired stays listed under its status, with no action.

*Covers: REQ-AGENCY-WEB-0002*

### 7.3 Assign Workers to a Shift

**As an Agency User**, I want to pick Workers from our roster to fill an accepted Shift, **so that** the Unit sees who is coming.

- The assign list holds our active Workers, those who can be assigned first.
- A Worker who cannot be assigned shows why: already on the Shift, blocked by the Unit, missing a required credential, or, where Compass blocks it, going into overtime.
- I can pick no more Workers than the open headcount.
- If an assignment adds overtime, I see each week and Unit where the Worker's overtime grows.
- Each assigned Worker shows when site instructions were sent to them; for a Worker with no email or phone, I am told to pass them on myself.

*Covers: REQ-AGENCY-WEB-0006*

### 7.4 Swap or remove Workers

**As an Agency User**, I want to swap or remove assigned Workers until the Shift ends, **so that** I can cover call-offs.

- Swap replaces one Worker with another in one step; Remove reopens the place.
- Workers taken off are listed with the reason.
- After the Shift ends, the Workers are listed with no changes allowed.

*Covers: REQ-AGENCY-WEB-0006*

### 7.5 See the Workers a Unit asked for

**As an Agency User**, I want to see which Workers a Unit asked for by name and say when one cannot work, **so that** the Unit knows early.

- An open or accepted Shift lists the Workers the Unit asked for.
- I can mark one unavailable with a reason.
- Requested Workers are marked and listed first when I assign.

*Covers: REQ-AGENCY-WEB-0014*

### 7.6 Upload Worker assignments from a file

**As an Agency User**, I want to upload a file naming which Workers go on which Shifts, **so that** I can staff many Shifts at once.

- Upload assignments on the Shifts screen opens the upload step with the Shifts file type already picked.
- Iris assigns the Workers the accepted rows name, once I approve them.

*Covers: REQ-AGENCY-WEB-0012*

---

## 8. Workers and credentials

### 8.1 Keep my Agency's Worker roster

**As an Agency User**, I want to keep a roster of my Agency's Workers, **so that** I can assign them to Shifts.

- The roster lists our Workers with their contact details, city, Positions, and whether active, and filters and searches by name, email, phone, and Position.
- Adding a Worker takes a first and last name and, optionally, email, phone, city, Positions, and a photo.
- I can edit and deactivate a Worker; I am first warned they will come off Shifts that have not started.

*Covers: REQ-AGENCY-WEB-0003*

### 8.2 Upload Workers from a file

**As an Agency User**, I want to upload a file of Workers, **so that** I can add or change many at once.

- Upload Workers on the roster opens the upload step with the Workers file type already picked.
- Iris saves the accepted rows once I approve them.

*Covers: REQ-AGENCY-WEB-0013*

### 8.3 Upload a Worker's credentials

**As an Agency User**, I want to upload my Workers' credential documents, **so that** they can work Shifts that require them.

- A Worker's page lists their credentials by type, newest first, with the issuer, number, dates, status, any review note, and the document.
- Uploading takes the credential type, the document, its expiry date where the type expires, and optionally the issuer, number, and issue date.
- A document sent without details is read by Iris, and I confirm or correct what it found.
- A saved credential cannot be edited or deleted; a correction or renewal is uploaded as a new one.
- I can upload many credentials at once from the roster, one file per credential.

*Covers: REQ-AGENCY-WEB-0007*

### 8.4 Record an Attestation

**As an Agency User**, I want to state that a Worker meets a requirement, **so that** they can work where Compass accepts our word.

- Attesting takes the credential type, a statement, and optionally a date it is valid until; earlier statements stay listed.
- Only the latest statement of each type counts, marked current or lapsed.
- For a type that needs a verified document, the page says a statement alone is not enough.

*Covers: REQ-AGENCY-WEB-0007*

### 8.5 See which Workers need credentials renewed

**As an Agency User**, I want to see which Workers have credentials expiring, expired, rejected, or in review, **so that** I renew them before Shifts are lost.

- Each roster row shows how many of the Worker's credentials need action and how many are in review, and the roster filters to those Workers.
- On a Worker's page, a credential is labelled expired, expiring soon, or replaced.
- The Worker's page also shows how many Shifts they have worked, each Unit's rating of them, and the issues Units reported, which I cannot change.

*Covers: REQ-AGENCY-WEB-0007*

### 8.6 Decide which credentials are required where

**As a Program User**, I want to define credential types and require them by part of the org, by Position, or both, **so that** only qualified Workers are assigned.

- Each type says whether it needs a verified document or an Attestation, and whether it expires.
- A type can be deactivated, not deleted; it then stops being required and keeps its records.
- Requirements list their type, place, and Position, and I add or remove them.
- Before I change a requirement, I am told eligibility is checked again, so Workers already assigned may come off upcoming Shifts.
- Picking a Unit and a Position shows every credential a Shift there requires.

*Covers: REQ-PROGRAM-WEB-0004*

### 8.7 Decide credentials Iris could not settle

**As a Program User**, I want to verify or reject each credential Iris's checks could not settle, **so that** no Worker is held up or let through by mistake.

- The review queue lists those credentials, oldest first, with the Worker, Agency, type, expiry, and why it needs review.
- Opening one shows the document beside the details the Agency gave and each check that failed or could not finish.
- Verify and Reject each require a note, and I am told the decision is final.

*Covers: REQ-PROGRAM-WEB-0010*

### 8.8 Audit Agencies' Attestations

**As a Program User**, I want to see every Attestation every Agency made, **so that** I can check what they vouched for.

- Every Attestation is listed, including replaced ones, newest first, with who made it and when, and filters by Agency, Worker, and type.
- The latest for each Worker and type is marked current or lapsed.
- I cannot add, change, or remove an Attestation.

*Covers: REQ-PROGRAM-WEB-0010*

### 8.9 See every Worker in the program

**As a Program User**, I want to see every Agency's Workers with the state of their credentials, **so that** I can spot compliance gaps.

- Workers are listed by Agency, with counts of credentials needing action and in review, and filter by Agency, type, those counts, and active or inactive.
- Opening a Worker shows their credentials, Attestations, and each Unit's rating; a credential awaiting review links to the review queue.
- The screen is read-only.

*Covers: REQ-PROGRAM-WEB-0012*

### 8.10 Rate the Workers who come to my Unit

**As a Unit User**, I want to rate Workers as favourite, okay to return, or blocked, **so that** I get the people I want back and not the ones I don't.

- The Workers screen lists everyone assigned to or rated by my Units, with their Agency, Shifts worked, my Unit's rating and review, and open issues, favourites first.
- I can rate a Worker at any time, including before their first Shift, from the roster or the Shift's page.
- Blocking first warns that the Worker comes off my Unit's upcoming Shifts and cannot be assigned or requested there.

*Covers: REQ-UNIT-WEB-0004*

### 8.11 Report an issue with a Worker

**As a Unit User**, I want to report an issue with a Worker to their Agency, **so that** the Agency deals with it.

- A report takes a category, a description, and optionally the Shift.
- The Issues tab lists my Units' reports, open ones first, with the Agency's resolution.

*Covers: REQ-UNIT-WEB-0004*

### 8.12 Resolve issues Units report

**As an Agency User**, I want to see and resolve each issue a Unit reports about our Workers, **so that** the Unit sees we acted.

- The Issues tab lists each issue with the Worker, Unit, category, description, Shift, and date, open ones first.
- Resolve requires a note the Unit can read; a resolved issue shows who resolved it and when.

*Covers: REQ-AGENCY-WEB-0008*

### 8.13 Issue badges at a secured Unit

**As a Unit User at a secured site**, I want to track each Worker's badge request, **so that** only badged Workers get in.

- A Badges tab lists badge requests, open ones first, with the Worker, Agency, and status.
- I mark a badge issued or revoked, and the row shows who did it and when.
- Each assigned Worker's badge status shows on the Shift's page.

*Covers: REQ-UNIT-WEB-0013*

---

## 9. Hours and Timesheets

### 9.1 See my Agency's Timesheets

**As an Agency User**, I want to see a Timesheet for each of our Workers on every ended Shift, **so that** I know what still needs submitting.

- Timesheets are listed by Shift, with the Worker, Unit, times, break, hours, tips, Expenses, and status, and open on those still to submit or sent back.
- A Timesheet sent back shows the Unit's reason; one still unapproved when its lock window closed is marked late.
- A submitted or approved one shows any exceptions, and whether Iris or the Unit approved it.

*Covers: REQ-AGENCY-WEB-0004*

### 9.2 Enter a Worker's hours

**As an Agency User**, I want to enter the clock times and break a Worker billed, **so that** the Timesheet is right before I submit it.

- While a Timesheet is a draft or sent back, I can change its clock-in, clock-out, and break; the Bill Rates are never editable.
- The page shows the scheduled times beside the billed ones, the hours in each pay class, and the amount for each.
- A Timesheet sent back shows the Unit's reason above the hours until I submit it again.
- Every change, including corrections the Unit made, shows in its history with the reason.

*Covers: REQ-AGENCY-WEB-0009*

### 9.3 Mark a no-show or split hours by role

**As an Agency User**, I want to mark a Worker as a no-show or split their hours when they changed role mid-Shift, **so that** we bill what really happened.

- While a Timesheet is a draft or sent back, I can mark a no-show, and clear a mark I set; a mark the Unit set says so.
- Split by role takes the switch time and the new Position, Department, or both, and can move some break minutes to the new part.
- Each part then shows its own rates, and the two parts keep the original total.

*Covers: REQ-AGENCY-WEB-0009*

### 9.4 Submit Timesheets

**As an Agency User**, I want to submit Timesheets one by one or for a whole Shift, Event, or day, **so that** the Unit can approve them as soon as the work ends.

- Each draft or sent-back Timesheet can be submitted, even with a missing clock time, which is marked.
- Submit all works for one Shift, one Event, or one day at a Unit.
- After a bulk submit, any Timesheet left unsubmitted is listed with the reason.

*Covers: REQ-AGENCY-WEB-0004*

### 9.5 Load hours from a file or a sign-in sheet

**As an Agency User**, I want to upload hours from a template or a photo of a paper sign-in sheet, **so that** I do not retype them.

- Upload hours opens the upload step with the Timesheets file type picked, and takes a template, a PDF, or a photo.
- Iris fills in the hours it accepts, once I approve them, without submitting any Timesheet.

*Covers: REQ-AGENCY-WEB-0004*

### 9.6 Review Timesheets by exception

**As a Unit User**, I want clean Timesheets approved automatically and only the exceptions put in front of me, **so that** I review what matters.

- The Timesheets screen opens on the submitted Timesheets that need me, those outside tolerance first, then the oldest Shift first. Other tabs list drafts, sent back, approved, and locked ones.
- Each row shows the Worker, Agency, Shift, Position, Department, scheduled times beside billed times, break, hours, Bill Rates, amount, tips, and Expenses.
- Each exception says what caused it, such as the minutes outside tolerance or a short break.
- A Timesheet billed at a rate other than the contracted one shows both rates, the difference, and the reason given when the Shift was sent.
- The parts of a split Timesheet show together; a late one is marked late; a locked one shows when it locked and allows no change.
- Once a Shift has ended, its page links to its Timesheets.

*Covers: REQ-UNIT-WEB-0003*

### 9.7 Approve Timesheets

**As a Unit User**, I want to approve Timesheets one at a time or for a whole Shift, Event, or day, **so that** approval takes minutes, not hours.

- Approve is unavailable, with the reason, while a Timesheet has missing times or an Expense I have not decided.
- Approve all approves every submitted Timesheet shown for one Shift, one Event, or one day, then lists any left unapproved with the reason.

*Covers: REQ-UNIT-WEB-0003*

### 9.8 Correct or send back a Timesheet

**As a Unit User**, I want to correct a Timesheet's hours or send it back to the Agency, **so that** we pay only for the time worked.

- Correct changes the clock times and break of a submitted or approved Timesheet that has not locked, and requires a reason.
- For one outside tolerance, Use scheduled times corrects it in one step, still with a reason.
- Reject sends a submitted Timesheet back to the Agency with a required reason.
- I can upload corrections from a file, with a reason on each row.

*Covers: REQ-UNIT-WEB-0015*

### 9.9 Mark a no-show or split hours as the Unit

**As a Unit User**, I want to mark a no-show or split hours by role myself, **so that** I can fix the record without waiting for the Agency.

- I can set or clear a no-show on any Timesheet that has not locked, with a reason.
- Split by role takes the switch time, the new Position, Department, or both, any break minutes to move, and a reason.

*Covers: REQ-UNIT-WEB-0015*

---

## 10. Tips and Expenses

### 10.1 Enter a Worker's tip

**As an Agency User**, I want to enter a tip for a Worker on their Timesheet, **so that** it reaches the Worker.

- I can enter, change, or remove a tip on a Timesheet, and am told that it stops the Timesheet being approved automatically.
- Tips from a Tip Pool or a cashier PIN show with their source and cannot be changed by me.

*Covers: REQ-AGENCY-WEB-0009*

### 10.2 Claim Expenses

**As an Agency User**, I want to add Expenses such as parking or background checks to a Timesheet, **so that** we are reimbursed.

- An Expense takes a kind (parking, background check, or other), an amount, and a note, which "other" requires.
- I can change or delete an Expense until the Unit decides it; a rejected one shows the Unit's reason.
- I can upload Expenses from a file.

*Covers: REQ-AGENCY-WEB-0009, REQ-AGENCY-WEB-0004*

### 10.3 Decide Expenses and see tips

**As a Unit User**, I want to approve or reject each Expense and see each Timesheet's tips, **so that** we pay only what we agreed.

- Each pending Expense shows its kind, amount, and note with Approve and Reject; Reject requires a reason.
- Tips show with their source: a Tip Pool share, a cashier PIN tip, or a tip the Agency entered.

*Covers: REQ-UNIT-WEB-0016*

### 10.4 Enter a Tip Pool

**As a Unit User**, I want to enter a day's tips for my Unit, a Shift, or an Event and have Iris split them, **so that** every Worker gets a fair share.

- A Tip Pool takes a Unit, a date, an amount, and optionally one Shift or one Event, never both.
- Opening a pool shows each Worker's share and the minutes counted, marked as scheduled where hours are not yet entered, and any amount left unallocated.
- A pool can be changed or deleted until a Timesheet it covers locks, and shows the last time it can be changed.
- I can also upload tips from a file, or type a pool in the assistant and approve the split it proposes.

*Covers: REQ-UNIT-WEB-0012*

### 10.5 Credit cashier PIN tips

**As a Unit User**, I want tips entered under a cashier PIN to go to the Worker behind it, **so that** card tips reach the right person.

- A PIN tip takes a Unit, a date, a cashier PIN, and an amount, and goes whole to that PIN's Worker.
- A PIN map lists each PIN with its Unit, Worker, and dates; I add mappings and end them, but cannot change their PIN, Worker, or start date.

*Covers: REQ-UNIT-WEB-0012*

---

## 11. Reports

### 11.1 See my Unit's spend and compliance

**As a Unit User**, I want spend, labor cost, and Timesheet compliance reports for my Units, **so that** I can manage cost and catch problems.

- The Reports screen opens on a spend dashboard for my Units, or the one I picked, with breakdowns by Agency, Position, and Unit.
- Labor cost shows as a percentage of sales for a chosen period, and says not available when there are no sales figures.
- Compliance shows missed breaks and late Timesheets for a period, grouped as I choose.
- A period is one week, one month, or a range of dates.
- My saved reports are listed here, and I can ask a question in the assistant.

*Covers: REQ-UNIT-WEB-0006*

### 11.2 See program-wide reports

**As a Program User**, I want to rank Agencies, Events, and Units by spend and see trends, **so that** I know where the money goes and how Agencies perform.

- For a period I pick, Agencies, Events, and Units are ranked by spend; each Agency also shows its fill rate and no-show rate.
- A trend chart shows spend, or another measure, by week or month.
- Compliance, labor cost against sales, and each Event's projected against actual cost are shown too.
- Every view can be narrowed to one Sector, Region, or District, and a figure with nothing to measure shows as not available.

*Covers: REQ-PROGRAM-WEB-0005*

### 11.3 Load budgets and sales

**As a Program User**, I want to upload budgets and sales figures, **so that** spend can be measured against them.

- Upload sales and Upload budgets open the upload step with that file type picked.
- A data view lists what was loaded, by Unit and date, with the file it came from.

*Covers: REQ-PROGRAM-WEB-0005*

### 11.4 See every Shift in the program

**As a Program User**, I want to see every Shift at every Unit with its Agencies, Workers, and Timesheets, **so that** I can check how the program runs without changing anything.

- Shifts are listed by date, with the Agencies holding each, and filter by part of the org, Agency, status, and dates.
- A flags filter finds Shifts sent off-contract or to a non-contracted Agency, or billed at a rate that differs from the contract.
- Opening a Shift shows each Agency's rates, the contracted rate and the difference, any reason given, its Workers, and its Timesheets.
- The screen is read-only.

*Covers: REQ-PROGRAM-WEB-0011*

### 11.5 Ask a question about spend

**As a Unit User or a Program User**, I want to ask a question in plain words and get a chart or table, **so that** I get answers without building a report.

- The answer shows as a chart or table, or a dashboard for several measures, and says which measures, groupings, filters, and dates it used.
- When the question is unclear, Iris asks which measure or period I mean before showing numbers.
- I can save an answer as a report and download its tables.
- A measure Iris cannot compute says not available, never zero.
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

**As a Unit User, an Agency User, or a Program User**, I want to type what I need, such as "book 4 servers Saturday", and get it prepared for me, **so that** routine work is quick.

- Iris prepares bookings, changes and cancellations of Shifts, Timesheet edits and approvals, tips, Expenses, and Worker assignments, and answers spend questions.
- The assistant itself saves nothing: each change comes back as a Proposal for me to approve.
- When my request is unclear or missing a detail, Iris asks before preparing anything.
- When my role cannot make the change, Iris says who can; when it cannot make the change at all, it says so.

*Covers: REQ-ASSISTANT-0003*

### 12.3 Approve what Iris prepared

**As a Unit User, an Agency User, or a Program User**, I want to review each change Iris prepared before it is saved, **so that** nothing happens without my say.

- A Proposal shows how many items are ready and how many need review; each problem shows the field, what is wrong, and a suggested fix.
- I accept the fix, edit the values, or reject each item, or accept every undecided item at once.
- Apply says how many items it will save and is disabled while a problem is undecided; Reject all saves nothing.
- After apply, I see how many were saved and any that failed a final check, with the reason.
- Only the person a Proposal was made for can open it.

*Covers: REQ-ASSISTANT-0002*

### 12.4 Send files and follow my uploads

**As a Unit User, an Agency User, or a Program User**, I want one page to send files, get templates, and follow what became of each upload, **so that** I always know where my data stands.

- I pick an upload type my role may send, download its template as CSV or Excel, and send a file, or let Iris detect the type.
- The upload log lists every file I sent, however I sent it: on this page, in the assistant, or by email or text.
- An upload awaiting review opens its Proposal; one whose type is unclear asks me to pick it; a failed one shows why.
- Other screens open this step with the type already picked, and the Uploads menu item shows how many uploads need me.

*Covers: REQ-SHELL-0008*

---

## Open questions behind these stories

These stories assume answers that Compass and Instawork have not yet confirmed. If an answer differs, the stories named here change.

| Question | What the stories assume | Stories |
| --- | --- | --- |
| Can one Shift go to more than one Agency? | Yes, by hand: a Unit User sends each part of the headcount to one Agency. Automatic sending to several Agencies comes later. | 6.1, 6.4, 7.1 |
| Do break and minimum-wage checks at booking flag a Shift or block it? | They flag it. Only overtime can be set to block. | 5.1, 7.3 |
| Who can change a Timesheet, and when? | The Agency edits drafts and sent-back Timesheets; the Unit corrects submitted and approved ones until they lock; nobody changes a locked one. | 9.2 to 9.9 |
| Who verifies Workers' credentials? | Iris checks each document; a Program User decides what the checks cannot settle and sets, per type, whether an Attestation is enough. | 8.3 to 8.7 |
| Who manages users? | Program Users manage everyone; Agency Users manage their own Agency's users. Accounts exist only by invite. | 3.12, 3.13 |
| Who may change a live rate? | Agencies and Program Users submit new lines; a Program User approves Agency lines, and their own need no second approval. | 4.2, 4.4, 4.5 |
| Who keeps Positions, Markets, and labor rules? | Instawork Admins. | 3.2 to 3.4 |
| Who keeps the org, Units, Agencies, and Settings after launch? | Program Users. A Unit User may change only their Unit's site instructions. | 3.7 to 3.15 |
| Which tip tax rules apply at launch? | None until Compass names them. This question is blocking. | 10.1 to 10.5 |

The full list of open questions, by who must answer each, comes from `python tools/list_decisions.py --markdown`.
