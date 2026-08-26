# International Border-Surveillance Platforms

**Stage:** 01 — Research → Competitors
**Date:** 2026-08-26
**Scope:** Operational border-surveillance software actually fielded by states and
agencies — national and supranational border situational-awareness frameworks,
border command-and-control platforms, and integrated sensor/video systems — and
what such a system contains.

This document records what real operational border-surveillance software is made
of: which modules exist, which information objects it manages, which workflows it
runs, which echelons it serves, and how it is deployed. It is a companion to
[competitive-landscape.md](competitive-landscape.md), which surveys the
commercial VMS/VCA market; this pass deliberately covers the layer *above* that
market — the frameworks and command systems that consume video alongside radar,
ground sensors, patrol positions and intelligence, and turn them into an
intervention.

The evidence is uneven by design of the domain rather than of this pass.
Frameworks created by law — EUROSUR above all — are documented in unusual depth,
because the legislature had to write down what the system does. Programmes run by
a single agency are documented mainly through privacy and audit instruments,
which describe data flows and retention precisely and describe screens not at all.
Systems sold by defence primes are documented at brochure level. **Operator
manuals, screen designs, alerting logic and measured detection performance for
national border systems are, with few exceptions, not public**, and several
specific gaps are named where they occur rather than filled by inference. Where a
platform could not be documented from a source worth citing, it is recorded as
undocumented rather than described.

Per [CLAUDE.md](../../../CLAUDE.md) §4, findings are tagged in
[§10](#10-key-findings-for-ibvap) by whether they are specific to this problem
statement, general to border surveillance in any country, general to intelligent
video analytics anywhere, or a market-specific factor.

## Contents

1. [Executive Summary](#1-executive-summary)
2. [Research Scope](#2-research-scope)
3. [Platforms Studied](#3-platforms-studied)
4. [Platform-by-Platform Findings](#4-platform-by-platform-findings)
5. [Cross-Platform Comparison](#5-cross-platform-comparison)
6. [Common Modules](#6-common-modules)
7. [Common Operational Workflows](#7-common-operational-workflows)
8. [Common Deployment Patterns](#8-common-deployment-patterns)
9. [Important Differences from Generic VMS/IVA](#9-important-differences-from-generic-vmsiva)
10. [Key Findings for IBVAP](#10-key-findings-for-ibvap)
11. [Open Questions](#11-open-questions)
12. [References](#12-references)

---

## 1. Executive Summary

A real border-surveillance system is not a video system with a map bolted on. In
every platform documented here, **video is one sensor category among five to ten**,
and the primary operator surface is a geo-referenced situational picture rather
than a wall of camera tiles. The European Commission's own EUROSUR Handbook lists
cameras alongside radar, active range-gated cameras, radio-frequency direction
finders and hydrophones as a single category — "fixed and mobile sensors" — and
describes what a camera contributes as "pictures, videos, time, direction,
image-processed data" `[S1]`. CBP's official definition of its Common Operating
Picture describes a hub that receives data from tower units which "automatically
detect and track items of interest," and hands the operator "the data, video and
geospatial location of selected items of interest to identify and classify them"
`[S7]`. Video is the identification step, not the detection step.

The object model is consistently richer than a VMS's. Across EUROSUR, CBP, and the
Leonardo and Cybernetica system architectures, the recurring information objects
are an **event/incident**, a **track or target**, an **own asset** (patrol,
vehicle, vessel, aircraft, with position, type and readiness), a **border section**
or area of responsibility, an **operation or mission**, an **intelligence/analysis
product**, and a **case or report with a named handler and an administrative
closure state** `[S1][S5][S7][S11][S14]`. Two of those — the own-asset layer and
the risk-graded border section — have no counterpart in any product surveyed in
[competitive-landscape.md](competitive-landscape.md).

The most striking structural feature, and the one the generic VMS survey did not
reveal at all, is that **geography carries a risk grade that creates obligations
with clocks on them.** EUROSUR divides external borders into border sections with
unique identifiers, attributes low/medium/high impact levels to each using the
CIRAM risk model, and attaches concrete timelines: an NCC forwards incident
information to the Agency "no later than four hours" after receiving it from the
local centre; at medium impact a regional centre ensures the local centre receives
additional resources "within two weeks"; at high impact the national centre does so
"within three weeks" and the Agency answers a support request "within five working
days" `[S1]`. Reaction capability is itself a modelled, planned and evaluated
property, split into physical and procedural components, and measured as reaction
time "starting at the moment of detection, and ending when all assets are in place"
`[S1]`.

Alerting is dominated by **cross-cueing rather than by classification accuracy**.
Radar or a ground sensor detects; a camera is slewed automatically to the
detection; a human identifies. PureTech advertises "Automated continuous
Slew-to-Cue: Radar, UGS, GPS" as a headline capability `[S13]`; Spain's SIVE is
described as orienting cameras immediately when radar identifies an unexpected echo
`[S18]`; CBP's unattended ground sensors "trigger or queue large platform
surveillance" `[S7]`. In this architecture the video analytic's job is narrower
than the commercial market assumes — it confirms and classifies something another
sensor already found, in a scene an operator has been pointed at.

Command structure is explicit and layered, and appears with almost identical shape
in independent sources. Leonardo documents a four-tier structure — National
Operations C2 Centre, Local Operations C2 Centre, Site Control Post, Area of
Responsibility — with distinct tasks at each `[S11]`; EUROSUR documents Local,
Regional and National Coordination Centres plus an International Coordination
Centre for joint operations, with each tier's tasks enumerated `[S1]`. Leonardo
further names four operator roles at a control centre — supervisor, surveillance
operator, reaction operator, and an unmanned configuration console whose entire job
is checking network status, sub-system operative status and sub-system health
`[S11]`. **System health is a staffed position, not a settings page.**

Information handling is governed to a degree no commercial VMS documentation
approaches. EUROSUR assigns ownership of every artefact to the node that supplied
it, requires the owner to validate before publishing, requires explicit procedures
to stop manually-entered information duplicating automated feeds, handles EU
classified information up to RESTREINT UE/EU RESTRICTED, marks own-asset artefacts
as classified regardless of what the originator marked, and requires the national
centre to guarantee that **no personal data other than ship identification numbers**
crosses from the national picture into the European one `[S1]`. CBP's model is
different but equally deliberate: surveillance recordings "are automatically
overwritten unless an authorized BSS user determines the recording is needed for an
approved purpose," and anything retained inherits the retention schedule of the case
file it is attached to `[S7]`.

Two findings should temper any assumption that these systems work as designed.
Frontex's own 2015 report on EUROSUR's functioning states that "data introduced to
Eurosur is lacking consistency in its structure and format and does not provide a
solid basis for the assessment," and that "there is no established automatic
mechanism that links the impact level assigned to specific border sections to the
Frontex operational response directly" `[S4]`. A legislated, funded,
continent-scale situational-awareness framework had, two years in, a data-quality
problem and a broken link between its risk grading and its response. That is the
most useful single data point in this document, and it is an official
self-assessment rather than a critic's claim.

Finally, and directly relevant to the SIH problem statement: **CBP's Integrated
Fixed Towers are documented as recording border incursion activity at 0.5 to 7
miles "without facial recognition capability"** `[S7]`. The largest fielded
land-border tower programme in the world explicitly does not attempt identity
analytics on its wide-area cameras — which is the same conclusion the pixel-density
physics in [competitive-landscape.md](competitive-landscape.md) §4.3 reaches from
the other direction.

---

## 2. Research Scope

The objective was to establish what an operational border-surveillance software
system contains beyond a generic CCTV/VMS: which modules, which screens, which
information objects, which workflows, which echelons, and which deployment
patterns. The eighteen dimensions checked for each platform were primary users;
operational hierarchy and workflow; live video monitoring; camera management;
maps/geospatial view; sensor integration; AI/video analytics; events and alerts;
incident management; investigation and history; evidence; search and filter;
command and control; communications and integration; system health; multi-site
monitoring; mobile and field interfaces; and the named software modules or screens.

Source priority was government and agency material first, then official programme
and procurement documentation, then manufacturer technical documentation, then
credible case studies. Four documents were retrieved as PDFs and read in full and
are the strongest evidence here: the European Commission's EUROSUR Practical
Handbook `[S1]`, Frontex's report on the functioning of EUROSUR `[S4]`, Frontex's
Serious Incident Reporting standard operating procedure `[S5]`, and the DHS
privacy impact assessments for CBP Border Surveillance Systems `[S7][S8]` and the
Team Awareness Kit `[S9]`. Leonardo's border-control capability brochure `[S11]`
was also read in full and is the single most useful manufacturer document found,
because it enumerates command echelons and operator roles rather than adjectives.

Several intended sources could not be retrieved. The EUR-Lex full texts of
Regulation (EU) No 1052/2013 and Commission Implementing Regulation (EU) 2021/581
returned empty documents to the fetch tool, so both are recorded here at the level
their citing sources establish — the Handbook cites 1052/2013 article by article
`[S1]`, and 2021/581's structure is known only from summaries `[S3]`. GAO's
reports on CBP surveillance technology were unreachable at the host and are
recorded from search summaries only `[S10]`. Anduril's own product pages returned
titles without body content, so Lattice is documented from trade press and
secondary description `[S15]`.

Whole classes of system are absent because they are not publicly documented. No
operational manual, screen specification, alert-handling procedure or measured
detection/false-alarm figure was retrieved for **any** national border-surveillance
system in this pass. Israeli, Turkish, Chinese, Russian, Gulf and most Asian
national border systems are represented, at best, by press coverage of contract
awards. This is a property of the domain — these are law-enforcement and defence
systems whose operating procedures are protected — and absence of documentation is
recorded here as absence of documentation, never as absence of the capability.

Border *control* software at crossing points — traveller processing, document
inspection, biometric entry/exit, watchlist screening — is a large adjacent
category and is deliberately out of scope, except where a surveillance platform
hands off to it.

---

## 3. Platforms Studied

| # | Platform / programme | Type | Evidence quality |
|---|---|---|---|
| **P1** | **EUROSUR** — European Border Surveillance System (EU/Frontex + 30 national coordination centres) | Supranational situational-awareness and information-exchange framework | **Strong.** Commission Handbook and Frontex functioning report read in full `[S1][S4]` |
| **P2** | **JORA + Serious Incident Reporting** (Frontex) | Operational incident-reporting application and its SOP | **Strong for the SOP** `[S5]`; the application itself documented only externally `[S6]` |
| **P3** | **CBP Border Surveillance Systems (BSS)** — IFT, RVSS, aerostats, NiSI/UGS, CBTT, maritime radar (US) | National border-surveillance programme with a sensor-alarm dispatch core | **Strong on data flow and retention** `[S7][S8]`; nothing on screens |
| **P4** | **ICAD** — Intelligent Computer Assisted Detection (US Border Patrol) | Sensor-alarm, dispatch and incident-record system | **Moderate.** Described only within the BSS assessments `[S7][S8]` |
| **P5** | **TAK / ATAK** (DHS, US Border Patrol) | Field/mobile situational-awareness client and server | **Strong** `[S9]` |
| **P6** | **Leonardo border-control architecture** — PSMS + ANTEO C2 | Manufacturer integrated border C2 architecture | **Strong for a brochure**; enumerates echelons and operator roles `[S11]` |
| **P7** | **Elbit TORCH-X Borders** | Manufacturer border C4ISR suite | **Vendor marketing only** `[S12]` |
| **P8** | **PureTech PureActiv / AlertView** | Manufacturer border C2 + geospatial video analytics | **Vendor marketing only** `[S13]` |
| **P9** | **Cybernetica Border & Coastal Surveillance** | Manufacturer national border/coastal surveillance system | **Vendor marketing only** `[S14]` |
| **P10** | **Anduril Sentry + Lattice** (US CBP) | Autonomous tower programme with proprietary C2 | **Weak.** Vendor pages unreadable; trade press only `[S15]` |
| **P11** | **Senstar/Magal FORTIS4G + Symphony** | PSIM + VMS pairing sold into border and critical-site work | **Vendor/press only** `[S16]` |
| **P12** | **PSIM as a category** | The software category border C2 platforms are usually built from | **Secondary** `[S17]` |
| **P13** | **SIVE** — Sistema Integrado de Vigilancia Exterior (Spain) | National maritime/land border surveillance system | **Secondary.** Press, vendor and ministry funding pages `[S18]` |
| **P14** | **Northern Border Security programme** (Saudi Arabia, Airbus) | National border-security programme | **Trade press only** `[S19]` |
| **P15** | **CIBMS / BOLD-QIT** (India, BSF) | National integrated border management system | **Government press release plus secondary** `[S20]` |

Platforms actively looked for and **not** documented to a citable standard in this
pass: Israel's border C2 (beyond Elbit marketing); Türkiye's integrated border
system; any Chinese or Russian national border platform; Hungary's, Poland's,
Bulgaria's or Greece's national surveillance systems as distinct software; and
Frontex's "EUROSUR 2.0"/Advanced Border Surveillance as a named product, which
appears in a research paper `[S21]` but not in retrievable Frontex documentation.

---

## 4. Platform-by-Platform Findings

### 4.1 P1 — EUROSUR

EUROSUR is the best-documented border-surveillance system in the world, and the
reason is structural: it was created by regulation, so its contents had to be
written down. It is a framework rather than a product — it defines what pictures
exist, who owns them, what goes in each layer, and what each echelon must do —
and national systems plug into it.

**Framework components**, per the regulation as cited by the Handbook: national
coordination centres; national situational pictures; a communication network; a
European situational picture; a common pre-frontier intelligence picture; and a
common application of surveillance tools `[S1][S2]`.

**Primary users.** The National Coordination Centre (NCC), staffed by
representatives of every national authority responsible for external border
surveillance working together "on a permanent basis," operating 24/7 with at
minimum a duty officer or shift commander present `[S1]`. Around it: local
coordination centres (LCC) responsible for a border section, regional or functional
coordination centres (RCC), the Agency, and an International Coordination Centre
(ICC) when a joint operation is hosted. The Handbook enumerates the national
authorities the NCC must exchange with — coastguard, police/gendarmerie, customs,
national guard, armed forces, maritime rescue coordination centre, migration and
asylum authorities — and a longer optional list including prosecutors, veterinary
services, civil protection, intelligence services and authorities responsible for
trafficking-victim referral `[S1]`.

**Operational hierarchy and workflow.** LCC → RCC → NCC → Agency, with tasks
enumerated per tier. The LCC does detailed planning and implementation, keeps
personnel and resources "in readiness for tracking, identification and
interception," chooses actions "in close-to-real time," and ensures the patrol or
LCC passes incident information to the NCC "in near-real time." The RCC monitors,
redistributes resources between border sections, and summarises and analyses LCC
information for the NCC. The NCC coordinates nationally and forwards incidents to
the Agency `[S1]`.

**Live video monitoring.** Present but subordinate. The operational layer "may
include… real-time images provided by video cameras, the area covered by cameras"
alongside patrol positions and asset distribution `[S1]`. Video is a contributor to
the picture, not the picture.

**Camera management.** Not a EUROSUR concern. Cameras are owned and managed by the
national border surveillance system, to which the NCC has "direct and real-time
access" `[S1]`. This division — the framework never touches the device — is itself
a design finding.

**Maps/geospatial.** Central. The operational layer includes "a visualisation of
the areas of responsibility of subordinate structures on a geo-referenced map, the
position and itinerary of patrols, the distribution and type of assets… and the
position and coordinates of patrol vessels" `[S1]`.

**Sensor integration.** Nine documented source categories: national surveillance
systems; fixed and mobile sensors (radar; cameras; active range-gated cameras;
radio-frequency direction systems; hydrophones); patrols; local/regional centres;
other authorities and liaison officers; the Agency's fusion services; other NCCs;
third countries; and ship reporting systems (AIS, VMS, SafeSeaNet, LRIT) `[S1]`.

**AI/video analytics.** Not specified at framework level. What EUROSUR does specify
is analytic *services*: the Agency's fusion services include "anomaly detection
(allowing the detection of suspicious or atypical behaviour by vessels)," drifting
models, an incident detection time service, and a vessel traffic service combining
terrestrial and satellite AIS with radar `[S1]`. The analytics are maritime
behaviour analytics over tracks, not video analytics over pixels.

**Events and alerts.** The events layer has four documented sub-layers:
unauthorised border crossings; cross-border crime; crisis situations (natural or
man-made disasters, accidents, humanitarian or political crises); and other events,
covering "unidentified and suspect vehicles, vessels and other craft and persons
present at, along, or in the proximity of the external borders" `[S1]`. Two rules
matter more than the taxonomy: **every event is assigned to a border section**, and
**the NCC allocates an impact level to every event it reports**, which the Agency
may not change `[S1]`.

**Incident management.** All events in the national picture must be made available
to the European picture "without delay." A validation mechanism makes the NCC
responsible for final validation before publication, and explicit procedures are
required to prevent manually uploaded information duplicating what automated and
semi-automated feeds already supplied `[S1]`.

**Investigation and history / evidence.** Weakly specified at framework level;
handled nationally. The analysis layer preserves reports, imagery and geodata; the
Handbook requires that where the national picture contains personal data,
"processing of such data should be logged to provide an audit trail" `[S1]`.

**Command and control.** Explicitly *not* EUROSUR's job — a footnote records that
"the relevant national authority is responsible for the command and control of
assets and resources. The NCC has a coordinating and strategic role" `[S1]`. The
separation of a situational-awareness layer from a command layer is deliberate and
recurs elsewhere.

**Communications/integration.** The EUROSUR Communication Network is "a network of
nodes," each node being "a complete set of hardware and software delivered by the
Agency" to an NCC; the member state supplies an internet link of at least 10 Mbps.
The network handles EU classified information up to RESTREINT UE/EU RESTRICTED.
A "node integration interface" exists where national authentication applies rather
than EUROSUR's own `[S1]`. Direct communication between the NCC and patrol assets
over TETRA is called out as considerably improving reaction capability `[S1]`.

**System health / multi-site.** Node IT administrators, a technical point of
contact per NCC, a change advisory board, formal change management and business
continuity planning are all specified `[S1]`. Multi-site is the entire premise: 30
national nodes plus the Agency.

**Border sections, impact levels and reaction.** Each member state divides its
external borders into sections corresponding to a local or regional centre's area
of responsibility; the Agency assigns each a unique identifier. Impact levels are
assessed using CIRAM's three risk components — threat, vulnerability, impact — and
are revisable at any time by either side, with tacit approval after a deadline and
a caveat recorded when approval was tacit or dissenting `[S1]`. The consequences are
concrete: at medium impact the RCC ensures the LCC receives additional resources
"within two weeks"; at high impact the NCC does so "within three weeks," designates
an officer responsible for that section, may launch an emergency task force, and
may request Agency support, to which the Agency replies "within five working days";
and the NCC forwards incident information to the Agency "no later than four hours
after having received it from the LCC" `[S1]`.

**Effect measurement.** The NCC "supports the regular measuring of the effects of
national border surveillance activities," producing an overview of events and
response activities "including their effectiveness and the resources and personnel
used" `[S1]`. Reaction time is defined as "the time needed to process an alert, move
assets to the hot spot, and prepare to counter the border violation, starting at
the moment of detection, and ending when all assets are in place" `[S1]`.

**What the operational record shows.** Frontex's own functioning report gives the
scale and the honest caveats. In the period covered, 117,721 events were entered
into the EUROSUR network application — 52,903 by member states, 463 by Schengen
associated countries and 64,355 by the Frontex node — of which over 90,000 were
irregular migration, over 20,000 related cross-border crime, and just 123 crisis
`[S4]`. The Frontex Positioning System tracks assets in joint operations,
transmitting "time, position, speed, course, height, type" over GPS/satellite/GSM
and also calculating running costs `[S4]`. And the two candid findings: data
entered into EUROSUR "is lacking consistency in its structure and format and does
not provide a solid basis for the assessment," and "there is no established
automatic mechanism that links the impact level assigned to specific border
sections to the Frontex operational response directly" `[S4]`. Whether either has
since been fixed is not established by anything retrieved; Implementing Regulation
2021/581 appears to be the standardisation response, since it is summarised as
standardising the information required in each report and defining single event
reports, indicators, confidence levels and impact attribution `[S3]`.

### 4.2 P2 — JORA and the Serious Incident Reporting SOP

JORA — the Joint Operations Reporting Application — is the system that carries
incidents from Frontex-coordinated operations into the European picture; Frontex
records that integration between JORA and the EUROSUR application was prioritised
early specifically so incidents were not reported twice `[S4]`. Externally it is
described as the main system holding all border-related incidents from joint
operations, with reporting done largely at coordination centres rather than by
officers on patrol assets, and with incidents cross-checked and validated before
they count `[S6]`. The application's own screens and data model are not publicly
documented.

The **Serious Incident Reporting SOP is public and is the clearest incident-case
lifecycle found anywhere in this research** `[S5]`:

1. **Categorisation.** Three categories: potential violations of fundamental rights
   or international protection obligations (1); potential violations of codes of
   conduct (2); serious actual or potential negative implications on core tasks (3).
   A report may carry more than one.
2. **Initial information.** Reportable "by phone, email or directly in JORA," with a
   phone report always followed by an email or JORA record.
3. **Validation and assessment.** The Situation Centre assesses categories 2 and 3
   against four named elements; the decision at that level is taken "by the Shift
   Leader or in his/her absence by the Senior Duty Officer on duty." Category 1 is
   assessed by the Fundamental Rights Officer. Either may decide the procedure is
   not launched, and must then inform the reporter.
4. **Distribution and handler assignment.** The Situation Centre distributes the
   report and assigns exactly one **SI-Handler**, determined by category; handling
   transfers to that person.
5. **Running log.** Updates are inserted into JORA by the handler or the Situation
   Centre "with the aim of ensuring that the JORA Log contains the most complete and
   up-to-date information."
6. **Closure.** A final report containing description, conclusions, proposals and
   lessons learned, due **within one month**; the procedure closes on its
   submission, and the Situation Centre then "administratively closes the SI report
   in JORA."
7. **Escalation.** If the final impact level is assessed as critical, crisis
   management procedures take over.

Two properties are worth naming. Categorisation is a decision made by a named role
against written criteria, not a dropdown the reporter picks. And **closure is a
separate administrative act from the substantive conclusion** — the handler
finishes the work, the Situation Centre closes the record.

### 4.3 P3/P4 — CBP Border Surveillance Systems and ICAD

**Primary users.** Border Patrol agents in the field; Sector Enforcement
Specialists at sector dispatch centres, who monitor sensor alarms; COP operators at
a local sector facility; the Air and Marine Operations Center for air/maritime radar
`[S7]`.

**What BSS is.** A deliberately heterogeneous inventory rather than a product:
"fixed and mobile video surveillance systems, range finders, thermal imaging
devices, radar, ground sensors, and radio frequency sensors," extended in the 2018
update with tethered aerostats, portable and counter-mortar radars, seismic and
imaging sensors, tunnel-detection sensor networks, maritime radar, and commercially
purchased location data used as a sensor `[S7]`. Individual systems are
commissioned and decommissioned continuously — the same document lists three
systems retired since 2014 `[S7]`.

**Common Operating Picture — the official definition.** "A central hub that
receives data from one or multiple tower units. The tower systems automatically
detect and track items of interest, and provide the COP operator(s) with the data,
video and geospatial location of selected items of interest to identify and
classify them" `[S7]`. Detection and tracking are automatic and happen at the tower;
identification and classification are the human's job at the COP; the COP is
described as aggregating towers, i.e. as multi-camera and multi-site by
construction.

**Integrated Fixed Towers.** Day and night cameras, radar and laser illuminators on
a fixed tower, monitored from a local sector facility, with "remote pan and tilt,
zoom and focus capabilities," recording "border incursion activity (from a distance
between 0.5 to 7 miles range, **without facial recognition capability**)" `[S7]`.
IFT shares geospatial data and still images with a Tracking, Sign-cutting and
Modeling tool — that is, with a system for reading physical trail evidence `[S7]`.

**ICAD — the alarm-to-dispatch core.** Unattended ground sensors "automatically
detect persons or vehicles and transmit activity reports or images via
radio-frequency or satellite communications to the CBP ICAD system"; the tunnel
programme's "alarms and sensor data will appear on an Intelligent Computer Aided
Detection (ICAD) system display, allowing the operators to identify where the alarm
occurred and **perform quality analysis** before notifying USBP Agents in the field
to respond" `[S7]`. The 2014 assessment describes ICAD as operating the sensor and
camera network, recording "the date, time, and location of the activity, as well as
details input by the Border Patrol Agent investigating the incident," with agents
entering identity details of people encountered, and the record retrievable by date,
time or those details `[S8]`. Sensors also "trigger or queue large platform
surveillance" — one sensor tasking another `[S7]`.

**The workflow this describes**, end to end: sensor activation → ICAD display at
sector dispatch → specialist performs quality analysis (an explicit human
false-alarm filter) → agent notified in their area of responsibility → agent
responds and investigates → if an incursion occurred, interdiction → outcome and
person details written back into the same incident record → apprehension details
into the e3 enrolment system, and video potentially linked to a TECS case file
`[S7][S8]`.

**Evidence and retention.** BSS data "may be used as evidence if the apprehension of
the individual results in criminal or administrative proceedings" `[S7]`. Recordings
"are automatically overwritten unless an authorized BSS user determines the
recording is needed for an approved purpose"; retained recordings inherit the
retention period of the case file, and the case management system's schedule governs
once the case closes `[S7]`. CBP "follows chain of custody procedures to ensure the
integrity of the records when records are used as evidence and therefore linked
directly to a case or person" `[S7]`. **Retention is a function of case association,
not of a days-of-storage setting.**

**Audit and accountability.** Audit trails record "at a minimum: user name, access
date and time, and functions and records addressed"; only authorised users can
extract material; annual security and privacy training is mandatory `[S7]`. The 2006
ICAD policy makes a named officer — the Sector Assistant Chief Patrol Agent —
responsible for "reviewing and evaluating reports for data accuracy and consistency"
and for recommending disciplinary action for non-compliance `[S7]`. Data quality has
an owner with a rank.

**Data quality as a documented weakness.** GAO's reporting, available here only in
summary, records that Border Patrol was deploying surveillance technology but needed
to improve data quality and assess effectiveness, and that towers were to transmit
into a centralised COP staffed at all times `[S10]`. This aligns with the EUROSUR
self-assessment: the recurring failure in this domain is the quality and consistency
of what gets recorded, not the sensing.

### 4.4 P5 — TAK / ATAK

The most completely documented **field** client found. TAK is a government-off-the-
shelf geospatial situational-awareness application with Android, iOS and Windows
clients plus a server, adapted by DHS for CBP, ICE and the Secret Service `[S9]`.

Documented capabilities: near-real-time position and status of friendly forces and
assets (blue-force tracking); terrain and environmental attributes; sensor data in
near real time; and, depending on the component, "live video feeds, image sharing,
navigation, and chat" `[S9]`. In the CBP appendix specifically, a launching agent
sees other TAK users, CBP assets, tactical operating centres, tactical
infrastructure, shared images and chats, and **receives sensor alarms from those
assets**, with filtering by characteristics `[S9]`. Data on the server is retained
for two years, encrypted at rest and in transit, access-controlled and audited, and
governed by written rules of behaviour with mandatory training for standard users
and administrators `[S9]`.

Two details are unusually informative. First, CBP states it may use TAK data "to
measure agent response times to sensor alarms and rescues" — the field client is
also the instrument for measuring reaction time `[S9]`. Second, CBP notes it does
not hold subject identity data in TAK but may share photos showing "recent travel by
foot, landmarks, or other perishable intelligence, which may later be associated
with an individual in another enforcement system" `[S9]`. The field tier deliberately
holds perishable observations and defers identity to the system of record.

### 4.5 P6 — Leonardo: PSMS and ANTEO C2

The most structurally explicit manufacturer document retrieved `[S11]`.

**Echelons.** Four, with tasks per tier:

| Tier | Documented tasks |
|---|---|
| **NOCC** — National Operations C2 Centre | Global situational awareness; recovery management; mission planning; sectors coordination |
| **LOCC** — Local Operations C2 Centre | Local situational understanding; resources management; intervention coordination |
| **SCP** — Site Control Post | Surveillance; recognition/identification; interdiction |
| **AoR** — Area of Responsibility | Short, medium and long range sensors |

**Named software.** *Physical Security Management System (PSMS)* — "designed to
provide global situational awareness to NOCC/LOCC for alarm management reaction
based on our state-of-the-art event correlation engine," integrating perimeter
protection, access control and video surveillance, and including "a correlation
engine, video content analysis and event and workflow management" `[S11]`.
*ANTEO C2* — "designed for use by both local surveillance operators and
national/regional headquarters," with "dedicated functionalities for the generation
of the tactical picture, real-time identification and classification of targets and
continuous monitoring of all threats within the border area," plus mission planning
and intervention management `[S11]`.

**Operator roles at a control centre** — the clearest role decomposition found
anywhere in this research `[S11]`:

- **Supervisor:** check the whole COP; **authenticate alarms**; coordinate logistic
  and mission activities.
- **Surveillance operator:** check all sensor alarms in the COP; check radar and
  electro-optical tracks; monitor and control the alarm zone with electro-optics;
  monitor and control CCTV video.
- **Reaction operator:** check the COP; manage sensors and vehicles (UGV/UAS/UAV);
  manage resources and communications.
- **Configuration (unmanned) console:** check communications network status; check
  operative status of all sub-systems; check **health status of all sub-systems**.

**Video handling.** Manages "ONVIF compliant cameras and equipment, legacy cameras
via digital converters and thermal cameras"; every stream can be "instantly replayed
and recorded for later investigation purposes"; video content analysis covers
"temporal, spatial or more complex events (i.e. virtual fences, objects tracking,
people counting, etc.)" `[S11]`. Notably, the ability to take **legacy cameras via
digital converters** is stated by a defence prime as a normal requirement — the
inherited-estate problem is not unique to any one force.

**Other modules.** An ANPR product for "access gates or during patrolling";
unattended ground sensors forming a self-maintaining wireless mesh to remote
operation centres; microphonic and fibre-optic sensing; buoy-based underwater
surveillance; radars; electro-optical families; UAS `[S11]`. Communications are
treated as part of the platform, not an assumption: TETRA and DMR with location-based
services, HF/VHF/UHF and SATCOM, and specifically "target position, geo-referenced
on a suitable map, to share with intercepting vehicles" `[S11]`.

### 4.6 P7 — Elbit TORCH-X Borders

Vendor documentation only; a brochure PDF was retrieved but contained no extractable
text. From the product page: an open-architecture C4ISR application integrating
sensors and tactical elements across "fixed, deployed and mobile platforms," fusing
electro-optical cameras, radars, acoustic, SIGINT and ELINT sensors, and autonomous
aerial and ground vehicles; supporting "simultaneous video streaming from numerous
channels and imagery data exploitation"; automatically classifying and prioritising
threats and recommending "the optimal interception methods"; recommending tasks "in
accordance with the rules of engagement"; providing "common situational awareness and
operational language among different forces" with "record and replay capabilities";
and installable on coastal, mobile and naval command platforms `[S12]`.

Two claims are worth isolating because no commercial VMS makes them: **rules of
engagement as a configured input to the software's recommendations**, and
**sensor-to-interceptor** as a named capability — the system closes the loop to the
responding unit, not to an operator's screen. Neither is independently verified;
both are vendor claims. Command echelons, patrol client design and mission-planning
workflow are not documented on the retrieved page.

### 4.7 P8 — PureTech PureActiv

Vendor documentation only, but unusually specific about the geospatial surface
`[S13]`. Documented: "Geospatial AI-boosted Video Analytics" performing detection,
classification and tracking, with a claimed range of up to six miles; **"Automated
continuous Slew-to-Cue: Radar, UGS, GPS"**; GIS map display of camera and radar
locations with their fields of view, alarm events and target tracks; camera and radar
**viewshed mapping**; point-and-click camera steering to a map coordinate;
**tower deflection compensation** (a sway-correction problem no enterprise VMS has);
long-range camera auto-tracking; automated drone dispatch to a target location; laser
rangefinder, illuminator and spotlight control; loud-hailer integration for deterrence;
alarm management; live and recorded playback; and forensic video analysis. Named
deployment: US Border Patrol mobile video surveillance systems `[S13]`.

Range and accuracy figures are vendor claims with no retrieved methodology, and
should be treated exactly as the vendor claims in
[competitive-landscape.md](competitive-landscape.md) are.

### 4.8 P9 — Cybernetica Border & Coastal Surveillance

Vendor documentation only, but it names the module decomposition explicitly `[S14]`:
a sensorics suite (radar, EO/IR, AIS, VHF/UHF, acoustic); a control centre with
"automated failover, full system health monitoring, and audit-ready logging";
operator workstations with "multi-screen layouts, customisable dashboards,
geospatial visualisation, alert management panels"; a data processing and fusion
layer producing a common operational picture; and **browser-based remote access
workstations**. Functional claims include automated anomaly detection using machine
learning (loitering, unexpected course changes), tiered alerts, historical playback
"for after-action reviews or incident investigations," mission management fusing
live data, communications and tasking, and an optional analytics and reporting module
with scheduled reports, customisable KPIs and historical trends `[S14]`. A 200 km
NATO/EU eastern-border deployment in Estonia is named `[S14]`.

Three of these are notable because the commercial VMS survey found nothing
equivalent: health monitoring and audit-ready logging listed as *control centre*
properties rather than admin features; **tiered alerts** as a first-class concept;
and a reporting module whose output is KPIs for the operation rather than clips.

### 4.9 P10 — Anduril Sentry and Lattice

The weakest evidence in this document relative to the programme's importance.
Anduril's own Lattice pages returned no body content to the fetch tool, so what
follows is trade press and secondary description and should be treated accordingly
`[S15]`. Lattice is described as an operating system that fuses sensor data,
controls autonomous assets and provides a real-time command layer, built on an open
architecture with a published SDK and language bindings, using edge computing and a
decentralised mesh that distributes data and tasks between sensors, effectors and
command posts "even over long distances and in contested environments" `[S15]`. The
Sentry towers autonomously scan, classify and track objects of interest and surface
them to agents `[S15]`. Deployment scale and contract values are recorded in
[competitive-landscape.md](competitive-landscape.md) §4.2 and are not repeated here.

The architecturally interesting claims — decentralised mesh, edge autonomy,
disconnected operation, an open SDK — are precisely the ones that could not be
verified from primary documentation in this pass, and they are exactly the claims
that would matter most to a bandwidth-poor deployment.

### 4.10 P11/P12 — FORTIS4G, Symphony and PSIM as a category

Magal/Senstar market a pairing that is representative of how border C2 is usually
assembled commercially: FORTIS4G, described as a fourth-generation **PSIM**,
integrating perimeter intrusion detection systems and Symphony, a VMS with native
video analytics; integration works by displaying graphical maps, linking perimeter
alarms to cameras, and triggering rules from perimeter events `[S16]`.

PSIM as a category is described consistently across secondary sources as four
layers: data collection from every connected sensor, alarm and access point;
**correlation engines that link events across systems using time, location and
identity relationships**; **situation management workflows that guide operators
through standardised response procedures**; and reporting tools producing compliance
documentation, incident timelines and performance analytics `[S17]`.

This is the single most useful category-level finding for understanding what a
border platform is: **the border command layer is a PSIM, not a VMS.** The
correlation engine and the SOP-driven situation-management workflow are the two
functions that a VMS does not have and that every border platform documented here
does — Leonardo's PSMS names both explicitly `[S11]`, EUROSUR's fusion, validation
and reaction-level procedures are the same two functions at national scale `[S1]`,
and CBP's specialist performing "quality analysis" before dispatching an agent is
the human form of the same step `[S7]`.

### 4.11 P13/P14/P15 — SIVE, Northern Border Security, CIBMS

These three are national programmes documented only well enough to establish shape,
not software. They are included because the shape is consistent.

**SIVE (Spain).** Sensor stations with long-range cameras and radar plus optronic
(infrared and visible) sensors, repeater stations, and a command-and-control centre
at the Guardia Civil's command centre; the control centre collects and processes
station information, controls the stations remotely, and coordinates emergency
response; cameras are oriented immediately when radar identifies an unexpected echo;
the system interconnects with the force's existing communications networks and with
neighbouring provinces' SIVE installations `[S18]`. The camera is subordinate to the
radar, and cross-provincial linking is a designed feature.

**Northern Border Security (Saudi Arabia).** Reported as ~900 km covered by a berm
and three fences with 40 surveillance towers carrying radar and day/night cameras,
38 communications towers, **seven C2 centres, 32 response stations, 240 response
vehicles and 10 surveillance reconnaissance vehicles**, connected to the C2 centres,
a National HQ and the Ministry of Interior over fibre `[S19]`. The ratio is the
finding: forty sensor towers against 32 response stations and 240 response vehicles.
The sensing is a small fraction of the programme; the response capability is the
programme.

**CIBMS / BOLD-QIT (India).** Described in an official government release and
secondary coverage as three components — sensors, detectors, cameras, radar,
micro-aerostats and lasers; a dedicated wired and wireless communication system; and
a centralised command-and-control system — with feeds reaching control rooms on the
border and enabling quick reaction teams to intercept `[S20]`. The riverine
Brahmaputra deployment covers roughly 61 km where physical fencing was not possible
`[S20]`. Software modules, screens and any measured performance are not publicly
documented, and prior analysis of CIBMS recorded in this project's domain research
names false alarms and sensor malfunction as leading technical issues.

---

## 5. Cross-Platform Comparison

Coverage of the eighteen dimensions. **Y** = documented in a source cited here.
**P** = partially documented or implied. **—** = not documented in this pass, which
is never evidence of absence. **n/a** = outside that platform's role by design.

| Dimension | EUROSUR | JORA/SIR | CBP BSS + ICAD | TAK | Leonardo | Elbit | PureActiv | Cybernetica | Anduril |
|---|---|---|---|---|---|---|---|---|---|
| 1. Primary users | Y `[S1]` | Y `[S5]` | Y `[S7]` | Y `[S9]` | Y `[S11]` | P `[S12]` | P `[S13]` | Y `[S14]` | — |
| 2. Operational hierarchy/workflow | Y `[S1]` | Y `[S5]` | Y `[S7]` | P `[S9]` | Y `[S11]` | — | — | P `[S14]` | — |
| 3. Live video monitoring | P `[S1]` | — | Y `[S7]` | Y `[S9]` | Y `[S11]` | Y `[S12]` | Y `[S13]` | Y `[S14]` | P `[S15]` |
| 4. Camera management | n/a | n/a | Y (PTZ) `[S7]` | — | Y `[S11]` | — | Y `[S13]` | P `[S14]` | — |
| 5. Maps/geospatial | Y `[S1]` | P | Y `[S7]` | Y `[S9]` | Y `[S11]` | Y `[S12]` | Y `[S13]` | Y `[S14]` | Y `[S15]` |
| 6. Sensor integration | Y `[S1]` | — | Y `[S7]` | Y `[S9]` | Y `[S11]` | Y `[S12]` | Y `[S13]` | Y `[S14]` | Y `[S15]` |
| 7. AI / video analytics | P (track anomaly) `[S1]` | — | P (auto detect+track) `[S7]` | — | Y (VCA) `[S11]` | Y `[S12]` | Y `[S13]` | Y `[S14]` | Y `[S15]` |
| 8. Events / alerts | Y `[S1]` | Y `[S5]` | Y `[S7]` | Y `[S9]` | Y `[S11]` | Y `[S12]` | Y `[S13]` | Y (tiered) `[S14]` | P |
| 9. Incident management | Y `[S1]` | Y `[S5]` | Y (ICAD) `[S7]` | — | Y (workflow) `[S11]` | — | — | P `[S14]` | — |
| 10. Investigation / history | P `[S1]` | Y (log) `[S5]` | Y `[S8]` | P `[S9]` | Y (replay) `[S11]` | Y `[S12]` | Y `[S13]` | Y `[S14]` | — |
| 11. Evidence | P `[S1]` | — | Y (custody) `[S7]` | — | P `[S11]` | — | — | P (audit log) `[S14]` | — |
| 12. Search / filter | P `[S1]` | P `[S5]` | Y `[S8]` | Y `[S9]` | — | — | — | P `[S14]` | — |
| 13. Command / control | n/a (explicit) `[S1]` | n/a | Y (dispatch) `[S7]` | P `[S9]` | Y (ANTEO) `[S11]` | Y `[S12]` | P `[S13]` | Y `[S14]` | Y `[S15]` |
| 14. Comms / integration | Y `[S1]` | Y `[S4]` | Y `[S7]` | Y `[S9]` | Y `[S11]` | Y `[S12]` | — | Y `[S14]` | Y `[S15]` |
| 15. System health | Y `[S1]` | — | — | — | Y (console) `[S11]` | — | — | Y `[S14]` | — |
| 16. Multi-site monitoring | Y `[S1]` | Y `[S4]` | Y (COP hub) `[S7]` | Y `[S9]` | Y `[S11]` | Y `[S12]` | Y `[S13]` | Y `[S14]` | Y `[S15]` |
| 17. Mobile / field | P (TETRA) `[S1]` | — | Y (via TAK) `[S9]` | Y `[S9]` | Y (TETRA/DMR) `[S11]` | P `[S12]` | — | Y (browser) `[S14]` | — |
| 18. Named modules / screens | Y `[S1]` | P `[S5]` | Y `[S7]` | Y `[S9]` | Y `[S11]` | P `[S12]` | P `[S13]` | Y `[S14]` | P `[S15]` |

The empty cells cluster in two places, and both clusters are informative. **Evidence
handling and search/filter are the least documented dimensions across manufacturer
sources** — the defence vendors describe detection and interception thoroughly and
prosecution barely at all, while the government sources describe evidence and
retention thoroughly and screens barely at all. And **system health is documented
only where a source describes a control room in staffing terms** (Leonardo's
unmanned configuration console, Cybernetica's control-centre health monitoring,
EUROSUR's node administrators and change board) — suggesting it is universal but
usually invisible in marketing.

---

## 6. Common Modules

Modules that appear in three or more independently sourced platforms, ordered by how
consistently they appear.

1. **Geospatial common operating picture.** Present in every platform without
   exception. Sensor positions, fields of view, tracks, events, own assets and areas
   of responsibility on one map `[S1][S7][S11][S13][S14]`. This, not a video wall, is
   the primary surface.
2. **Multi-sensor fusion / correlation layer.** A named component whose job is to
   merge sensor outputs into tracks and to correlate events across systems by time,
   location and identity `[S11][S12][S14][S17]`. EUROSUR's equivalent operates at
   information rather than signal level — filtering, fusion, evaluation and
   validation as named steps of its intelligence process `[S1]`.
3. **Event / alarm management.** With, in the better-documented cases, a grading
   attribute — EUROSUR's per-event impact level `[S1]`, Cybernetica's tiered alerts
   `[S14]`, Elbit's automatic prioritisation `[S12]`.
4. **Own-assets / blue-force layer.** Position, type, status, readiness and
   operational area of patrols, vehicles, vessels and aircraft, maintained as a peer
   layer to events `[S1][S4][S9][S11]`. EUROSUR requires an overview of all available
   assets "including the assets' level of readiness, type and use" `[S1]`.
5. **Sensor cross-cueing / slew-to-cue.** Automatic camera tasking from a radar,
   ground-sensor or GPS detection `[S7][S13][S18]`; CBP's sensors also "trigger or
   queue large platform surveillance" `[S7]`.
6. **Video subsystem.** Live view, PTZ control, recording, instant replay, and video
   content analysis for zones, lines, tracking and counting `[S7][S11][S13]`. Present
   everywhere; primary nowhere.
7. **Incident / case record with lifecycle and named handler.** `[S5][S7][S8]`, and
   as "event and workflow management" in Leonardo's PSMS `[S11]`.
8. **Intelligence / analysis layer.** Distinct from the live picture, holding
   analytical products, imagery, geodata and risk assessments `[S1]`; the commercial
   equivalent is the reporting/KPI module `[S14][S17]`.
9. **Environmental layer.** Terrain, weather, and in maritime contexts
   oceanographic data and drift models, as a standing sub-layer rather than a widget
   `[S1]`.
10. **Communications integration.** TETRA/DMR/HF/SATCOM with location services, and
    the ability to push a geo-referenced target position to an intercepting unit
    `[S1][S11]`.
11. **Mission / operation management.** Planning, tasking, monitoring and
    after-action review of a named operation `[S11][S12][S14]`; EUROSUR's operational
    layer carries an operations sub-layer with mission statements, deployment and
    patrolling schedules, operational areas and periodic situational reports `[S1]`.
12. **System health and configuration.** Sub-system status, communications-network
    status, failover, and audit logging `[S11][S14]`; at framework level, node
    administration, change management and business continuity `[S1]`.
13. **Reporting and effect measurement.** Scheduled reports and KPIs `[S14]`; at
    framework level, mandatory effect measurement covering events, responses,
    effectiveness, resources and personnel `[S1]`.
14. **Access control, classification and audit.** Need-to-know permissions, security
    clearance gating, classification marking, ownership of information, and audited
    access `[S1][S7][S9]`.
15. **Field/mobile client.** Blue-force tracking, map, chat, image sharing, sensor
    alarms `[S9][S11]`.

---

## 7. Common Operational Workflows

Six workflows recur. They are described here as observed patterns across sources,
not as a design proposal.

**W-A. Detect → cross-cue → identify → assess → dispatch → resolve → record.** The
core loop. A non-video sensor detects; a camera is cued; a human identifies and
classifies; a human assesses whether it is real and worth acting on; a responder is
dispatched with a geo-referenced position; the responder resolves it on the ground;
the outcome is written back onto the same record `[S7][S13][S18]`. CBP's version
inserts an explicit named step — the dispatch specialist performs "quality analysis"
before notifying an agent `[S7]`. **The human false-alarm filter is a documented,
staffed position in a real border system, not an admission of failure.**

**W-B. Report → categorise → validate → assign a handler → log updates → final
report → administratively close.** The incident-case lifecycle, documented in full
in Frontex's SIR SOP `[S5]` and visible in outline in ICAD's record structure `[S8]`
and Leonardo's "event and workflow management" `[S11]`. Categorisation is performed
by a named role against written criteria; closure is a separate act from conclusion.

**W-C. Assess risk → grade the geography → allocate resources → measure the
response.** EUROSUR's reaction-capability cycle: assess each border section under
CIRAM, attribute an impact level, plan and pre-position resources per level, and
evaluate using reaction time from detection to assets in place `[S1]`. Reaction
capability is planned separately for low, medium and high, with a described procedure
for what changes when the level changes `[S1]`.

**W-D. Collect → evaluate → collate → analyse → generate → disseminate.** The
intelligence cycle, specified in EUROSUR as seven numbered steps including
management of the analysis layer, source-reliability evaluation, filtering, fusion,
and product generation `[S1]`. This is a distinct workflow from live monitoring, run
by different people on a different cadence, producing named product types (key
developments, briefing notes, analytical monitors, earth-observation reports)
`[S1]`.

**W-E. Escalate across echelons on a clock.** LCC → RCC → NCC → Agency, with
timelines attached at each hop and reinforcement obligations that trigger on the
impact level `[S1]`. The escalation is contractual, not discretionary.

**W-F. Attach to a case → preserve → hand over.** Recordings are transient by
default and preserved only by association with a case; preserved material inherits
the case's retention schedule and chain-of-custody handling; the case may be handed
to another organisation entirely `[S7]`.

A seventh pattern is implied everywhere and specified nowhere retrievable: how a
camera or sensor is **commissioned** into one of these systems — what is measured,
who signs it off, what is recorded about its coverage. Only PureTech's viewshed
mapping and tower-deflection compensation hint at the problem `[S13]`, and only
EUROSUR's requirement to know "the area covered by cameras" hints at the data object
`[S1]`. This is a real documentation gap, and it happens to sit exactly where
IBVAP's Camera Spec Sheet sits.

---

## 8. Common Deployment Patterns

1. **Three or four tiers, always.** Sensor/site → local centre → regional or sector
   centre → national centre, with an operation-specific coordination centre bolted in
   when a joint operation runs `[S1][S11]`. The tiers differ in what they decide, not
   only in how much they see: local tiers choose actions in close-to-real time,
   regional tiers redistribute resources between sections, national tiers plan and
   request external support `[S1]`.
2. **The border is divided into named, identified sections that are also
   organisational units.** A EUROSUR border section corresponds to a local or
   regional centre's area of responsibility and carries a unique identifier assigned
   centrally `[S1]`. Leonardo's AoR is the same construct `[S11]`.
3. **The framework does not own the devices.** EUROSUR requires the NCC to have
   "direct and real-time access to the relevant parts of the national border
   surveillance system, including sub-systems set up at local/regional level and
   surveillance systems managed by other national authorities," and to combine
   information when two systems cover the same section — but the national system
   remains the national system's `[S1]`. The border layer is additive over existing
   infrastructure by construction.
4. **Multi-agency by default, single-agency never.** Every documented platform serves
   several authorities with distinct legal mandates, and the software carries
   ownership, release and classification rules to make that possible `[S1][S7]`.
   EUROSUR explicitly requires the NCC to respect each authority's "responsibilities
   and autonomy (e.g. command and control functions)" `[S1]`.
5. **Response capability outweighs sensing in the programme's mass.** Saudi Arabia's
   northern border programme fields 40 surveillance towers against 32 response
   stations and 240 response vehicles `[S19]`; CIBMS is framed as "integration of
   manpower, sensors and command and control" `[S20]`; EUROSUR devotes an entire
   chapter to reaction capability and none to camera specification `[S1]`.
6. **Communications are inside the system boundary.** Fibre, microwave, TETRA, DMR,
   satellite and HF are specified as part of the platform, with the bandwidth stated
   where it matters — EUROSUR's node requires at least 10 Mbps to the internet `[S1]`;
   CIBMS names microwave, optical fibre and digital mobile radio as a component
   `[S20]`.
7. **Field tier as a first-class client.** TAK is deployed to nearly all Border
   Patrol agents `[S9]`; Leonardo pushes geo-referenced target positions to
   intercepting vehicles `[S11]`; EUROSUR names direct NCC-to-patrol communication as
   a reaction-capability improvement `[S1]`.
8. **Security accreditation as a deployment gate.** The EUROSUR network required
   provisional authority to operate and then full accreditation before classified
   information could flow, a process running over years `[S1][S4]`.
9. **Long-lived programmes with continuous churn of sensor types.** CBP's 2018
   assessment adds seven system families and retires three relative to 2014 `[S7]`;
   SIVE has been maintained and extended by multiple contractors across two decades
   `[S18]`. The platform outlives its sensors, which is an argument for treating
   sensor types as pluggable.

---

## 9. Important Differences from Generic VMS/IVA

These are the differences that [competitive-landscape.md](competitive-landscape.md)
could not have surfaced, because they exist above the layer that document surveys.

| # | Border-surveillance platform | Generic enterprise VMS/IVA |
|---|---|---|
| 1 | **Video is one sensor category among many**; radar and ground sensors typically detect first `[S1][S7][S18]` | Video is the system; other sensors are inputs to video rules |
| 2 | **The map is the primary surface**; camera tiles open from the map `[S7][S11][S13]` | The camera grid is the primary surface; a map is a plugin |
| 3 | **Geography is graded by risk and that grade creates timed obligations** `[S1]` | No concept of a risk-graded site with resourcing consequences |
| 4 | **Own assets — patrols, vehicles, vessels — are a first-class layer** `[S1][S9][S11]` | No responder layer at all |
| 5 | **Reaction capability is modelled, planned and measured** (physical vs procedural; reaction time from detection to assets in place) `[S1]` | Response is out of scope; the product ends at the notification |
| 6 | **A standing environmental layer** — terrain, weather, oceanography, drift models `[S1]` | Weather is, at most, a camera-health nuisance |
| 7 | **A separate intelligence/analysis layer with a formal cycle and product types** `[S1]` | Analytics dashboards; no intelligence process, no source-reliability grading |
| 8 | **Information ownership, validation, classification and release control** — including hard rules on what may not cross a boundary `[S1]` | Multi-tenant permissions; no classification, no originator control, no release filter |
| 9 | **Escalation across echelons with contractual clocks** (4 hours, 2 weeks, 3 weeks, 5 working days, 1 month) `[S1][S5]` | Alarm acknowledgement, optionally with an SLA timer |
| 10 | **Incident case lifecycle with a named handler and administrative closure** `[S5]` | Alarm acknowledged/cleared; a bookmark |
| 11 | **Cross-cueing is the core automation**; the analytic confirms what another sensor found `[S7][S13][S18]` | The analytic *is* the detection; there is nothing to cue from |
| 12 | **A human quality-analysis step is designed in** `[S7]` | Automated false-alarm filtering is the sales pitch |
| 13 | **Retention driven by case association** — overwrite by default, preserve on attachment, inherit the case's schedule `[S7]` | Retention is days-of-storage per camera |
| 14 | **Chain of custody and cross-organisation handover as a designed function** `[S7]` | Evidence lock and export, usually a premium tier |
| 15 | **A staffed, named system-health role** `[S11][S14]` | A settings page and an email alert |
| 16 | **Field/mobile is a peer client with blue-force tracking, chat and inbound sensor alarms** `[S9]` | A mobile app for viewing cameras |
| 17 | **Interoperability is with other agencies and other countries**, not with other buildings `[S1]` | Federation across sites of one organisation |
| 18 | **Identity analytics deliberately absent on wide-area cameras** — IFT documented "without facial recognition capability" `[S7]` | Face recognition and ANPR marketed as headline capabilities |
| 19 | **Effect measurement and attribution are obligations** `[S1][S9]` | No vendor surveyed publishes a false-alarm rate at all |
| 20 | **Deterrence and interaction are in scope** — loud hailers, illuminators, spotlights `[S13]` | Audio talk-down exists but is a retail/perimeter feature, not a mission |

---

## 10. Key Findings for IBVAP

Nothing below is a requirement; converting any of it into scope is a
`docs/02-product/` decision. Each finding is tagged per
[CLAUDE.md](../../../CLAUDE.md) §4 — `[BORDER]` for what holds for border
surveillance in any country, `[GLOBAL]` for what holds for intelligent video
analytics anywhere, `[MARKET:xx]` for factors that vary by jurisdiction.

**No finding in this pass is `[SIH/SSB]`-specific, and that is itself a result.**
Fifteen entries spanning EU, US, Spanish, Saudi, Estonian and Indian programmes and
four manufacturers' reference architectures converge on the same shape, the same
information objects and the same workflows. The Indian programme in the set is described in exactly the terms the
others are — sensors, dedicated communications, centralised command and control,
control rooms, reaction teams `[S20]` — which supports treating the SIH context as a
validation setting rather than a distinct problem shape (D-2).

**F1 — The system a border force actually operates is a PSIM, and video analytics is
a supplier to it.** `[BORDER]` The recurring architecture is a correlation
engine plus SOP-driven situation management plus a geospatial picture, into which
sensors — video among them — feed events `[S11][S17]`. A product that emits
well-formed, geo-referenced, graded events into that layer fits the documented
architecture; a product that assumes it *is* the operator's primary surface does
not. This is direct corroboration of the emitter posture already recorded as D-5,
from an entirely different evidence base than the VMS market.

**F2 — Every event object in real border systems carries attributes IBVAP's Event
does not yet obviously carry.** `[BORDER]` Specifically: a **border section
or area-of-responsibility identifier**, an **impact/severity grade allocated by the
reporting side**, and a **confidence or reliability attribution** `[S1][S3]`. In
EUROSUR the grading is allocated by the originating NCC and cannot be overridden by
the receiving side `[S1]`.

**F3 — Detection is usually not the video's job; identification is.** `[BORDER]`
Radar, ground sensors and RF sensors detect; the camera is cued and the human
identifies `[S7][S13][S18]`. This lowers the accuracy bar a video analytic must clear
to be operationally useful and raises the value of *being cueable* — accepting an
external cue with a position and returning the corresponding view.

**F4 — The largest fielded land-border tower programme explicitly does not do face
recognition on its wide-area cameras.** `[BORDER]` CBP documents IFT
recording at 0.5–7 miles "without facial recognition capability" `[S7]`. This is
independent official corroboration of the pixel-density conclusion in
[competitive-landscape.md](competitive-landscape.md) §4.3, and it is a strong,
citable precedent for declaring an analytic ineligible on a camera rather than
offering it degraded.

**F5 — A human quality-analysis step between alarm and dispatch is normal
practice, not a workaround.** `[BORDER]` CBP's dispatch specialists
"perform quality analysis" on sensor alarms before notifying agents `[S7]`;
Leonardo's supervisor role "authenticates alarms" `[S11]`. An assessment step
between an Event and a response is what the domain already does.

**F6 — Retention in real border systems is a function of case association, not of
storage days.** `[BORDER]` / `[MARKET:xx]` Recordings overwrite
automatically unless attached to a case, and then inherit the case's schedule and
chain-of-custody handling `[S7]`. The retention *policy* is market-specific; the
*model* — transient by default, preserved by attachment — is general.

**F7 — Reaction capability is measured, and the measure is time from detection to
assets in place.** `[BORDER]` EUROSUR defines it precisely `[S1]`, and CBP
uses its field client to measure "agent response times to sensor alarms and rescues"
`[S9]`. Any claim that a video-analytics layer improves response time is testable
against an existing, defined metric — and measurable through the field tier rather
than the control room.

**F8 — Data quality, not sensing, is the documented failure mode of legislated
border systems.** `[BORDER]` Frontex's own assessment: EUROSUR data "is
lacking consistency in its structure and format and does not provide a solid basis
for the assessment," and no automatic mechanism links a section's impact level to
operational response `[S4]`. CBP assigns data accuracy and consistency to a named
officer by policy `[S7]`, and GAO's summarised findings point the same way `[S10]`.
A machine-generated, schema-stable, consistently structured event stream addresses a
documented, officially admitted weakness — which is a more defensible claim than
detection-accuracy leadership.

**F9 — Own assets and their readiness are a first-class layer everywhere, and IBVAP
has no such object.** `[BORDER]` EUROSUR requires an overview of all
available assets with readiness, type and use `[S1]`; TAK's core function is
blue-force tracking `[S9]`. This is not an argument to build one — it is an argument
that the layer above IBVAP already has one, and that IBVAP's events must be
consumable *alongside* it, geo-referenced and time-stamped to match.

**F10 — The field tier is a peer client, not a phone view of the control room.**
`[BORDER]` TAK gives an agent the map, other agents' positions, shared
images, chat and **inbound sensor alarms** on a government device, deployed to
nearly all agents, with two-year server retention and audited access `[S9]`. Where a
force has no control room, this tier is the whole system — which is exactly the
condition D-3 designs for, and there is now a documented precedent for it working
that way in a large force.

**F11 — Communications capability is inside the system boundary in every real
programme.** `[BORDER]` TETRA, DMR, HF, satellite, fibre and microwave are
specified as components, and target positions are pushed to intercepting units
`[S1][S11][S20]`. A product that assumes IP connectivity as a given is assuming away
something these programmes budget for explicitly.

**F12 — System health is a staffed role with its own console.** `[BORDER]`
Leonardo's unmanned configuration console exists to check network status, sub-system
operative status and sub-system health `[S11]`; Cybernetica lists health monitoring
and audit-ready logging as control-centre properties `[S14]`. Health reporting is not
an add-on in this domain, and reporting *degraded analytic capability* — which
nothing in either survey addresses — would land in an existing, staffed workflow.

**F13 — Classification, ownership and release control are ordinary features, and
egress filtering can be a hard requirement.** `[BORDER]` /
`[MARKET:xx]` EUROSUR assigns ownership per node, requires owner validation
before publication, marks own-asset artefacts classified regardless of originator
intent, and requires member states to guarantee that **no personal data other than
ship identification numbers** leaves the national picture `[S1]`. A published event
schema that cannot express classification, ownership and a release filter may be
unusable in exactly the deployments it targets. Which rules apply is market-specific;
that *some* apply is general.

**F14 — Multi-agency information sharing, not multi-site scaling, is the hard
integration problem.** `[BORDER]` EUROSUR enumerates eight mandatory and
fourteen optional partner authority types and four escalating cooperation modes —
information sharing, cooperation, assistance, integration `[S1]`. The egress problem
named in [competitive-landscape.md](competitive-landscape.md) §4.6 is therefore
sharper than it appeared: the consumer may be another organisation with its own
legal mandate, not another console.

**F15 — Commissioning and coverage documentation is a genuine gap in this
literature.** `[GLOBAL]` Only viewshed mapping `[S13]` and EUROSUR's passing
requirement to know "the area covered by cameras" `[S1]` touch it. No source
retrieved describes how a camera's fitness for a given analytic is established,
recorded or re-checked. That the gap survives into government-documented systems, not
just commercial ones, strengthens rather than weakens the case for per-camera
capability disclosure.

**F16 — Deterrence and on-scene interaction are in scope for border platforms.**
`[BORDER]` Loud hailers, illuminators and spotlights are controlled from the
C2 surface `[S13]`. This is outside IBVAP's stated scope and is recorded so it is
recognised as a normal expectation in this market rather than mistaken for a gap.

**F17 — Nothing in this pass is India-specific, and the India-specific programme is
the least documented of the fifteen.** `[MARKET:xx]` CIBMS/BOLD-QIT is
described in a government press release at component level only, with no software
documentation, no screens and no published performance `[S20]`. The architecture it
describes — sensors, dedicated communications, centralised command and control,
feeds to control rooms, quick reaction teams — is the same architecture as every
other programme here.

---

## 11. Open Questions

**Highest priority — these would most change how IBVAP's outputs are shaped.**

- **Q-1. What is the actual field-level schema of a border event?** Regulation
  2021/581 standardises single event reports, indicators, confidence levels and
  impact attribution `[S3]`, but its full text was not retrieved. Obtaining it would
  give a real, legislated event schema to compare an emitted contract against.
- **Q-2. Does any of these platforms publish an ingest contract a third-party
  analytic can emit into?** Anduril claims an open SDK `[S15]`; Leonardo, Elbit,
  Cybernetica and PureTech document integration as a service they perform. If a
  documented open ingest exists anywhere, it is the highest-value integration target
  in this domain.
- **Q-3. What replaced or fixed the EUROSUR data-consistency problem?** Frontex
  recorded it in 2015 `[S4]`; 2021/581 looks like the response `[S3]`. Whether it
  worked is unestablished and would be the strongest available evidence about what
  event standardisation actually buys.
- **Q-4. What is the measured false-alarm rate of any fielded border sensor
  system?** Not published by any source in this pass. ICMPD names sensors'
  susceptibility to false positives as a known limitation and AI filtering as a
  future direction `[S21]`; the 90% figure for the retired SBInet programme remains
  the only concrete number in this project's evidence base, and it is a decade old.

**High priority — shape the picture.**

- **Q-5.** How is a camera commissioned into a national border system — what is
  measured, recorded and re-verified? Undocumented in everything retrieved
  ([§7](#7-common-operational-workflows), pattern seven).
- **Q-6.** What does a border C2 operator's screen actually look like? No screen
  specification, layout or interaction description was retrieved for any platform.
- **Q-7.** Do national border platforms carry an evidence/export function at all, or
  is prosecution handled entirely in a separate case system? CBP's answer is the
  latter (e3, TECS) `[S7]`; nobody else documents it.
- **Q-8.** How do these platforms behave when a site is disconnected? Anduril claims
  a decentralised mesh working "over long distances and in contested environments"
  `[S15]`; Cybernetica claims automated failover `[S14]`; EUROSUR mandates business
  continuity planning `[S1]`. None publishes a degraded-mode specification. This is
  the same decisive unknown recorded as Q-3 in
  [competitive-landscape.md](competitive-landscape.md).
- **Q-9.** Is there a documented land-border analogue of EUROSUR's maritime anomaly
  detection — behaviour analytics over land tracks rather than vessel tracks? None
  found.
- **Q-10.** What is the staffing ratio of a border control centre — how many
  cameras, sensors and kilometres per operator? Leonardo names four roles `[S11]` but
  no source gives a ratio.

**Medium priority — validate assumptions made here.**

- **Q-11.** Are Elbit's, PureTech's and Anduril's capability claims independently
  verified anywhere? Nothing independent was retrieved for any of the three.
- **Q-12.** Do Israeli, Turkish, Chinese or Russian national border platforms have a
  materially different architecture? Unknown; not publicly documented in any language
  searched in this pass, and the recurring-architecture finding in
  [§8](#8-common-deployment-patterns) is therefore drawn from a Western-plus-India
  sample and should be treated as such.
- **Q-13.** Does the four-tier echelon structure hold for forces without a national
  operations centre, or does it collapse to two tiers? Every source here describes a
  force that has one.
- **Q-14.** How much of a border programme's cost is software? Saudi Arabia's asset
  mix `[S19]` suggests very little; no source breaks it out.

---

## 12. References

Retrieved 2026-08-26 unless otherwise noted. **G** marks an official government,
agency or legislative source. **P** marks a primary document whose text was read in
full. **M** marks manufacturer documentation or marketing. **I** marks an
independent, academic or third-party source.

### EU / EUROSUR / Frontex

- `[S1]` **G, P** — European Commission, *Practical Handbook for implementing and
  managing the European Border Surveillance System (EUROSUR Handbook)*,
  C(2015) 9206 final ANNEX 1, 15 December 2015; circulated as Council of the
  European Union document 15407/15 ADD 1. PDF, 60 pages, text extracted and read in
  full. Copy retrieved from Statewatch.
  https://www.statewatch.org/media/documents/news/2015/dec/eu-com-eurosur-handbook-com-9206-Annex-15.pdf
- `[S2]` **G** — Regulation (EU) No 1052/2013 establishing the European Border
  Surveillance System (EUROSUR). Cited here **only through `[S1]`**, which
  references it article by article; the EUR-Lex full text returned an empty document
  to the fetch tool and was not read directly.
  https://eur-lex.europa.eu/eli/reg/2013/1052/oj/eng
- `[S3]` **G** — Commission Implementing Regulation (EU) 2021/581 of 9 April 2021 on
  the situational pictures of EUROSUR. **Full text not retrieved**; structure
  recorded here from search summaries and secondary descriptions only, and should be
  treated as the weakest EU source in this document.
  https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32021R0581
- `[S4]` **G, P** — Frontex, *Report on the functioning of Eurosur* (December 2015).
  PDF, 20 pages, text extracted and read. Copy retrieved from Statewatch.
  https://www.statewatch.org/media/documents/news/2016/mar/eu-frontex-report-on-eurosur-functioning-12-2015.pdf
- `[S5]` **G, P** — Frontex, *Serious Incident Reporting — Standard Operating
  Procedure*. PDF, 23 pages, text extracted and read.
  https://www.frontex.europa.eu/assets/Key_Documents/SIR_SOP.pdf
- `[S6]` **I** — External descriptions of JORA: Asseco Poland, "Joint Operations
  Reporting Application" (supplier page); Oxford Border Criminologies, "Validating
  Border Violence on the Aegean: Frontex's Internal Records" (2021); Frontex Public
  Register of Documents entries for JORA incident forms. Search summaries only; the
  application's own documentation is not public.

### United States / DHS / CBP

- `[S7]` **G, P** — DHS/CBP/PIA-022(a), *Privacy Impact Assessment Update for the
  Border Surveillance Systems (BSS)*, 21 August 2018. PDF, 19 pages, text extracted
  and read in full.
  https://www.dhs.gov/sites/default/files/publications/privacy-pia-cbp022-bss-september2018.pdf
- `[S8]` **G, P** — DHS/CBP/PIA-022, *Privacy Impact Assessment for the Border
  Surveillance Systems (BSS)*, August 2014. PDF, 18 pages, text extracted; the ICAD
  description is taken from this document.
  https://www.dhs.gov/sites/default/files/publications/privacy_pia_CBP_BSS_August2014.pdf
- `[S9]` **G, P** — DHS/ALL/PIA-090, *Privacy Impact Assessment for the Team
  Awareness Kit (TAK)*, July 2021, including Appendix A (U.S. Customs and Border
  Protection). PDF, 15 pages, text extracted and read.
  https://www.dhs.gov/sites/default/files/publications/privacy-pia090-dhs-atak-july2021.pdf
- `[S10]` **G** — U.S. Government Accountability Office, *Southwest Border Security:
  Border Patrol Is Deploying Surveillance Technologies but Needs to Improve Data
  Quality and Assess Effectiveness* (GAO-18-119) and *Arizona Border Surveillance
  Technology* (GAO-12-22). **Not retrieved** — the host was unreachable from this
  environment; recorded from search summaries only.
  https://www.gao.gov/products/gao-18-119

### Manufacturer documentation

- `[S11]` **M, P** — Leonardo S.p.A., *Border Control* capability brochure,
  MM08482, 2017. PDF, text extracted and read in full. Contains the NOCC/LOCC/SCP/AoR
  echelon diagram, the PSMS and ANTEO C2 descriptions, and the four control-centre
  operator role definitions.
  https://electronics.leonardo.com/documents/16277707/18368839/body_Border_Control_LQ_mm08482_.pdf
- `[S12]` **M** — Elbit Systems, *Torch-X™ Borders* product page.
  https://www.elbitsystems.com/homeland-security/integrated-solutions/border-defence-systems/torch-x-borders
  (A UK-hosted brochure PDF was also retrieved but contained no extractable text.)
- `[S13]` **M** — PureTech Systems, *Border Security* / PureActiv AlertView C2.
  https://www.puretechsystems.com/border-security
- `[S14]` **M** — Cybernetica, *Border & Coastal Surveillance* solution page.
  https://cyber.ee/solutions/border-surveillance/
- `[S15]` **M/I** — Anduril Sentry and Lattice. Anduril's own Lattice pages
  (https://www.anduril.com/lattice/command-and-control) returned no body content to
  the fetch tool; recorded from trade press and secondary description, principally
  ExecutiveBiz, FedScoop and Inside Unmanned Systems. Treat all capability claims
  here as unverified.
- `[S16]` **M/I** — Senstar/Magal: Senstar Symphony Common Operating Platform press
  release and FORTIS4G PSIM descriptions.
  https://senstar.com/press-releases/senstar-introduces-the-senstar-symphony-common-operating-platform-with-sensor-fusion-engine/

### Category and programme sources

- `[S17]` **I** — Physical Security Information Management as a category: Wikipedia,
  "Physical security information management"; Everbridge, "What is PSIM?"; Noggin,
  "Physical Security Information Management (PSIM) Explained". Secondary; used only
  for the four-layer description, which is consistent across all three.
- `[S18]` **I/G** — SIVE (Sistema Integrado de Vigilancia Exterior, Spain): Indra
  press release on the Tarragona deployment; Spanish Ministry of the Interior
  European-funds project page "Mejora de las capacidades del SIVE"; Spanish-language
  encyclopaedic and trade coverage. No official system documentation was retrieved.
  https://fondoseuropeosparaseguridad.interior.gob.es/es/detalle/proyecto/MEJORA-DE-LAS-CAPACIDADES-DEL-SIVE/
- `[S19]` **I** — Northern Border Security programme, Saudi Arabia (Airbus Defence
  and Space): Shephard Media, UPI and GlobalSecurity coverage of the 2014
  inauguration. Trade press only; no programme documentation retrieved.
- `[S20]` **G/I** — CIBMS and BOLD-QIT, India: Press Information Bureau release on
  the launch of smart fencing on the Indo-Bangladesh border (March 2019), plus
  secondary Indian coverage.
  https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=1567516
- `[S21]` **I, P** — ICMPD, *Advances in Border Management: Digitalisation trends and
  emerging technologies*, Working Paper, January 2025. PDF, 36 pages, text extracted
  and read in part. Source for the "EUROSUR 2.0"/Advanced Border Surveillance
  reference, Maritime Aerial Surveillance, and the statement that surveillance-sensor
  limitations include susceptibility to false positives.
  https://research.icmpd.org/wp-content/uploads/2025/02/Advances-in-Border-Management-Digitilisation-trends-and-emerging-technologies.pdf
- `[S22]` **I** — ICMPD/European Commission, *Guidelines for Integrated Border
  Management in European Commission External Cooperation* (2010); OSCE Border
  Security and Management National Focal Point Network and Border Management Staff
  College materials. Search summaries only; used for the six-area IBM framing and the
  interagency-cooperation framing, both of which are corroborated in detail by `[S1]`.
