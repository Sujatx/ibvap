# Investigative and Case-Management Platforms

**Stage:** 01 — Research → Competitors
**Date:** 2026-08-26
**Scope:** How platforms that already run high-consequence human triage — Palantir
Gotham, SOC/SIEM triage consoles, police records systems, and the alarm-management
standard that governs control rooms — measure their own alert quality, capture why an
alert was dismissed, model a case's lifecycle, and handle authentication for people who
must act fast.

This document records what real triage and case-handling systems do about four things
IBVAP's UX has named but not yet specified: a measurement surface that shows alert
volume and nuisance rate per camera and per rule (S-21); a way to capture *why* a human
called an alert not real; a lifecycle for a Case that survives handover; and an
authentication model for a remote single-operator site with no help desk. It is a
companion to
[international-border-surveillance-platforms.md](international-border-surveillance-platforms.md),
which established the border-domain workflows — the Frontex categorise → validate →
assign-handler → log → final report → administratively close lifecycle, CBP's staffed
"quality analysis" step, and TAK's field tier. This pass goes *inside* those steps: the
field-level, screen-level, state-level detail that the border literature does not carry.

The evidence here is better than in the border pass, and unevenly so. Two sources are
unusually strong: **ANSI/ISA-18.2-2016**, an American National Standard that specifies
alarm performance metrics, nuisance-alarm definitions and a shelving lifecycle as
normative requirements; and **NIST SP 800-63B**, which specifies session and
authenticator behaviour as a public standard. SOC product documentation from Splunk and
Microsoft is vendor-written but is *operator documentation* — it names exact field
values, exact state lists and exact defaults, which no border-platform vendor document
does. Palantir Gotham is the weakest of the named platforms relative to its
prominence, and [§3.1](#31-palantir-gotham--what-is-and-is-not-publicly-documented)
records precisely where its documentation stops.

Per [CLAUDE.md](../../../CLAUDE.md) §4, nothing found in this pass is SIH- or
SSB-specific. Everything below is either general to intelligent video analytics
anywhere or general to any system where a human decides whether a machine observation
is real.

## Contents

1. [Executive Summary](#1-executive-summary)
2. [Research Scope](#2-research-scope)
3. [Platforms Studied](#3-platforms-studied)
4. [Findings — Measurement and alert-analytics dashboards](#4-findings--measurement-and-alert-analytics-dashboards)
5. [Findings — Dismissal and false-positive reason capture](#5-findings--dismissal-and-false-positive-reason-capture)
6. [Findings — Case and investigation lifecycle](#6-findings--case-and-investigation-lifecycle)
7. [Findings — Authentication and session design](#7-findings--authentication-and-session-design)
8. [Cross-Platform Patterns and Disagreements](#8-cross-platform-patterns-and-disagreements)
9. [Recommendations for IBVAP's UX](#9-recommendations-for-ibvaps-ux)
10. [Open Questions](#10-open-questions)
11. [References](#11-references)

---

## 1. Executive Summary

The single most useful structural finding is that **three independent triage platforms
separate the administrative state of an alert from the analytical judgement about it,
and capture them in different fields at different moments.** Splunk Enterprise Security
documents this explicitly: adding a disposition lets an analyst classify a finding and
"separate the false positives without impacting the status of the finding, such as New,
In-progress, Closed" `[S6]`. Microsoft Sentinel makes the same split — status is New /
Active / Closed, and a *classification* is demanded only at the moment of closing, where
"Selecting a classification is mandatory" `[S8]`. Chicago Police Department's fielded
case-status vocabulary encodes the same two axes into compound names — *Cleared open*
and *Cleared closed*, *Exceptionally cleared open* and *Exceptionally cleared closed*
`[S17]` — which is the outcome axis and the workflow axis multiplied out. This
corroborates, from an entirely different evidence base, the Frontex finding already
recorded in the border pass: **closure is a separate administrative act from the
substantive conclusion.**

The reason vocabulary is remarkably consistent and remarkably short. Sentinel offers
five values on close: *True Positive – suspicious activity*, *Benign Positive –
suspicious but expected*, *False Positive – incorrect alert logic*, *False Positive –
incorrect data*, *Undetermined* `[S8]`. Splunk offers the same five plus *Other* and
*Testing*, with *Undetermined* as the default `[S6]`. Two things stand out. First,
**"benign positive" is a separate value from "false positive"** — the system saw
something real that was not a threat, which is a different fact about the detector than
a detector that fired on nothing. Second, **the two false-positive values distinguish
bad rule logic from bad input data**, which is a distinction about *where the fault
lies*, not about what was in the scene.

Neither platform requires the reason at first touch. Splunk's disposition defaults to
*Undetermined* and an administrator may "select the Required toggle to mandate entering
a disposition before closing a finding" `[S6]` — the requirement is configurable, it
attaches to *closing*, and it never blocks the initial triage keystroke. IBM QRadar's
close-offence dialog works the same way, with a predefined reason list an administrator
can extend `[S9]`. **The one-second decision and the reason-for-the-decision are
deliberately not the same interaction.**

For measurement, the strongest source is not a product at all. **ANSI/ISA-18.2-2016
defines a nuisance alarm as an "alarm that annunciates excessively, unnecessarily, or
does not return to normal after the operator action is taken"** `[S10]`, and specifies
a metric set in Table 7 with target values: ~6 annunciated alarms per hour per operator
console as "very likely to be acceptable" and ~12 as "maximum manageable"; fewer than
~1% of ten-minute periods containing more than ten alarms; the top ten most frequent
alarms contributing "~<1% to 5% maximum"; chattering and fleeting alarms at "Zero,
action plans to correct any that occur"; stale alarms "less than 5 present on any day";
and a priority distribution of ~80% low, ~15% medium, ~5% high `[S10]`. The standard
also separates metric *audiences*: performance metrics for operations management,
diagnostic metrics for whoever fixes specific alarms, deployment metrics for programme
progress, and **audit metrics whose named contents are "number and nature of
unauthorized alarm changes" and "number and nature of unauthorized alarm suppression"**
`[S11]`. A measurement screen in this tradition is four different screens' worth of
content aimed at four different readers, and IBVAP's S-21 currently names only the first.

The standard also settles, from outside the product world, the shape IBVAP's suppression
already has. ISA-18.2 makes shelving **a required function**, and requires the shelving
function to provide "a time limit for shelving," "access control for shelving of
individual alarms," "the ability to unshelve alarms," "a record of each alarm shelved,"
and a display listing every shelved alarm showing "the shelved time remaining or the time
and date the alarm was shelved" `[S10]`. Automatic unshelving is normative: "The time
limit is a function that unshelves the alarm when the time period expires" `[S10]`. And
for a shelving that outlasts a defined limit, the record **shall** include "the reason
for shelving" `[S10]`. UX-14 and FR-30 are, on this evidence, not an IBVAP invention —
they are the control-room standard, and the one element the standard adds that IBVAP does
not yet have is a captured *reason*.

On authentication, the mature standards disagree with each other in a way that matters
for a one-person site. **NIST SP 800-63B rev 4 (26 August 2025) sets AAL2's overall
reauthentication timeout at a SHOULD of no more than 24 hours and inactivity at a SHOULD
of no more than 1 hour** `[S13]`; the older rev-3 text, still restated verbatim inside
criminal-justice policy, made both a SHALL at 12 hours and 30 minutes `[S15]`. On failed
attempts the gap is wider still: rev 4 says the verifier "SHALL limit consecutive failed
authentication attempts … to no more than 100 by disabling that authenticator" and
recommends progressive delays and other throttling `[S13]`, while CJIS policy mandates a
hard limit of five consecutive invalid attempts and an automatic lock "for a ten (10)
minute time period unless released by an administrator" `[S15]`. At a post with one
operator and no help desk, a five-attempt lockout is a self-inflicted denial of service;
NIST rev 4's throttling posture is the one that survives contact with that deployment.

The most directly transferable authentication finding is an exemption, not a rule. CJIS
policy requires a session lock after at most 30 minutes of inactivity, and then names
three device categories that are **exempt** "in the interest of safety" — devices in a
criminal justice conveyance, dispatch devices inside a physically secure location, and
"terminals designated solely for the purpose of receiving alert notifications (i.e.,
receive only terminals or ROT) used within physically secure location facilities that
remain staffed when in operation" `[S15]`. That third category is a receive-only
annunciator in a staffed secure room, exempted from session lock precisely because it
cannot act. It is an official, citable precedent for IBVAP's Annunciator mode (S-03a)
and for **UX DECISION UX-12** — the read-only display needs no session, and the price of
that exemption is that it offers no controls.

Finally, the honest negative. **Palantir Gotham does not publicly document a case object
with a lifecycle, a dismissal reason vocabulary, a session timeout, a lockout state, or
a credential-recovery flow.** Its published service-definition document is detailed at
application level and silent at state level `[S1]`; its public security pages describe a
philosophy of fine-grained access control and mandatory markings without a single time
value `[S2]`; and the leaked law-enforcement user manual reported in 2019 documents
screens while covering, per the reporting, no alerting, permissions, audit or retention
material `[S4]`. Everything below that Gotham does contribute is real and cited; nothing
below reconstructs a Gotham screen that was not documented.

---

## 2. Research Scope

The objective was to fill four named gaps in [UX.md](../../03-design/UX.md) with
evidence rather than invention: what a nuisance-rate measurement surface contains and
how it is organised (S-21); how a dismissal reason is captured without turning a
one-second decision into a form; what states a real investigative case moves through and
who moves it; and how session, lockout and recovery are designed where every action is
consequential and there is nobody to call.

Source priority followed the house rule: published standards and government documents
first, then official product documentation written for operators, then vendor marketing,
then credible secondary reporting. Two standards were retrieved as PDFs and read in the
relevant clauses in full — ANSI/ISA-18.2-2016 `[S10]` and, via a state adoption whose
text restates it clause by clause, the criminal-justice security policy `[S15]`. NIST SP
800-63B rev 4 was read directly on NIST's own site `[S13]`. Palantir's G-Cloud 14 service
definition, filed with the UK Crown Commercial Service's Digital Marketplace, was
retrieved as a 24-page PDF and read in full `[S1]`; it is vendor-written but filed into a
government procurement framework, which is the closest thing to an official Gotham
specification that exists publicly.

Several intended sources could not be retrieved. The FBI's own copy of the CJIS Security
Policy returned an HTML error page rather than the PDF, so criminal-justice requirements
are cited from a state governing board's adoption of the same policy, which restates the
clause numbers and text `[S15]`. IBM i2's product documentation sits behind Cloudflare
Access and returned an authentication redirect, so i2 iBase is recorded here at product-
page level only and contributes almost nothing `[S18]`. IBM QRadar's documentation pages
returned HTTP 403 to the fetch tool, so QRadar's close-reason behaviour is recorded from
search summaries of its own documentation and should be treated as the weakest product
claim in this document `[S9]`. Mark43's case-lifecycle material is marketing prose with
no state list `[S19]`.

One category was searched for and is genuinely absent: **no source retrieved in this pass
publishes a scene-cause taxonomy for a video false positive.** Nobody documents a preset
list containing wind, animal, shadow, glare, rain, insects or headlights. ISA-18.2's
nuisance taxonomy is *behavioural* — chattering, fleeting, stale — and the SOC platforms'
taxonomies are about *fault location* — bad logic versus bad data. The scene-cause list
IBVAP's cause histogram needs has no external precedent found here, which is recorded as
a gap rather than filled by guessing.

Deliberately out of scope: incident-response orchestration and playbook automation
(SOAR), which is a large adjacent category IBVAP has already ruled out via NG-9; and
evidence-management products, already covered by the border pass's chain-of-custody
findings.

---

## 3. Platforms Studied

| # | Platform | Type | Evidence quality |
|---|---|---|---|
| **C1** | **Palantir Gotham** | Intelligence/investigation platform | **Moderate at application level, absent at state level.** G-Cloud service definition read in full `[S1]`; public security pages `[S2]`; leaked cop manual via reporting `[S4]`. See [§3.1](#31-palantir-gotham--what-is-and-is-not-publicly-documented) |
| **C2** | **Splunk Enterprise Security** | SOC alert-triage and investigation console | **Strong.** Operator and administrator documentation naming exact field values, defaults and roles `[S5][S6][S7]` |
| **C3** | **Microsoft Sentinel** | Cloud SIEM incident console | **Strong.** Microsoft Learn operator documentation with the exact closing-classification list `[S8]` |
| **C4** | **IBM QRadar** | SIEM with an offence model | **Weak.** Documentation pages returned 403; recorded from search summaries of IBM's own docs `[S9]` |
| **C5** | **ANSI/ISA-18.2-2016 + ISA-TR18.2.5** | American National Standard for alarm systems | **Strongest source in this document.** Normative clauses on shelving, suppression and performance metrics, read in full `[S10][S11]` |
| **C6** | **NIST SP 800-63B (rev 4 and rev 3)** | US federal digital identity standard | **Strong.** Rev 4 read directly `[S13]`; rev 3 session clause read `[S14]` |
| **C7** | **CJIS Security Policy** (via a state adoption) | Government security policy binding police systems | **Strong for clause text.** 190-page PDF extracted and read in the relevant clauses `[S15]` |
| **C8** | **US police records/case management** | Fielded investigative case lifecycles | **Moderate.** One published department policy `[S16]`; one department's status definitions released to media `[S17]` |
| **C9** | **IBM i2 iBase / Analyst's Notebook** | Investigative database and link analysis | **Very weak.** Documentation behind an access gate `[S18]` |
| **C10** | **Mark43 RMS** | Public-safety records and case management | **Vendor marketing only** `[S19]` |

### 3.1 Palantir Gotham — what is and is not publicly documented

Gotham was searched by name across procurement records, published product documentation,
API references, and press coverage of leaked material. What follows is what was actually
found, separated from what was not.

**Documented, from Palantir's own filing with a government procurement framework
`[S1]`.** Gotham's data model is an *Ontology* of objects and properties "that represent
real concepts (such as people, organisations, places, documents, and events) and the
relationships that connect them," described as "fully adaptable." Named applications
are enumerated with a paragraph each: **Browser** (view and edit objects, "add notes, and
view a history of changes that were made to the object"), **Custom Object Views**
(configurable per-object dashboards whose tabs "can be locked down so that only users
with the required permissions are able to see it"), **Object Explorer** (top-down
filtering and aggregation with histogram tooling), **Inbox** (alert aggregation),
**Chat**, **Slides**, **Dossier** (collaborative report authoring), **Graph**, **Gaia**
(geospatial), and **Video**. The document also states plainly that further applications
exist for "targeting, fires control and execution, ISR, and ISINT analysis which are not
listed here" — an explicit acknowledgement that the public catalogue is partial.

**Documented on alerting.** Inbox "centralises results, notifications, and alerts in an
inbox-style interactive operational interface" and lets users "view and triage alerts
from across the platform in a single, unified view." Alerting is **subscription-based**:
"Notifications are only generated when a user subscribes to an alert, and they remain in
Inbox unless a user manually archives the message." Four subscription types are named —
search feeds, object watch feeds, geofence alerts, and sharing alerts. Users "can
interact with and resolve alerts directly in the application," including "viewing what
actions need to take place to resolve an alert" `[S1]`.

**Documented on machine detections — the closest Gotham comes to gap 2.** In the Video
application, "Detections are surfaced to users for confirmation or dismissal, and users
can provide live feedback to directly improve model accuracy," and a figure caption
states that "Quality control steps can be applied to ensure the analyst's assessment of
the detection and link validity are well-considered" `[S1]`. This is a confirm/dismiss
binary with a feedback loop into the model. **No reason vocabulary, no reason field, and
no description of what "quality control steps" consist of appears anywhere in the
document.**

**Documented on access control `[S1][S2].`** Access restrictions "can be applied at the
level of the individual attributes that describe an object (e.g., a building's address,
a vehicle's model)." Permission degrees are named as "ownership, write, read, discovery
and no access." Security is "guaranteed through a combination of mandatory and
discretionary controls," with *markings* as the mandatory control applied to data
"that require special protection." All interactions "are recorded in audit logs" which
"can additionally be configured to be tamper-evident." Palantir states that security
audit logging is not subject to "gating, pay-walling, or upselling" `[S2]`. Single sign-on
and multi-factor authentication are supported, and MFA is "mandatory for all our managed
Software as a Service (SaaS) platform customers" `[S1][S2]`. Note that the most detailed
object- and property-level security documentation Palantir publishes is written for
**Foundry**, not Gotham `[S3]`; Gotham's own pages describe the same philosophy in less
detail, and the G-Cloud document states Gotham "incorporates and leverages Palantir
Foundry's capabilities" `[S1]`, which makes the Foundry material indicative rather than
authoritative for Gotham.

**Not documented anywhere retrieved.** No Case or Investigation object with named
lifecycle states. No open/assigned/closed/reopened vocabulary. No ownership or handover
mechanic beyond Dossier's statement that "work is preserved even if one or more Dossier
contributors switch out to focus on other tasks" `[S1]`. No dismissal reason list. No
session timeout, inactivity timeout, lockout threshold, lockout duration, or credential
recovery flow — the word *session* appears once in the entire service definition, in the
sentence "users can open multiple instances of any application from within the same
session" `[S1]`. No alert-quality or false-positive metric of any kind. No screen layout
or interaction specification.

The 2019 reporting on a leaked *Palantir Law Enforcement* user manual confirms the shape
of this gap from the other side: the reporting describes the search and visualisation
tools and "Virtual Dossiers" that centralise investigation analysis, and states that the
manual does **not** address alerting, permissions structures, audit logging, or retention
`[S4]`. A cop-facing manual that omits all four is consistent with those being
deployment-configured rather than product-fixed — but that is an inference, not something
any source states.

**The honest conclusion: Gotham is useful to IBVAP as evidence about object models,
subscription-based alerting, per-attribute access control, and human confirmation of AI
detections. It is not usable as evidence about case states, dismissal reasons, session
behaviour or measurement, because Palantir does not publish those.**

---

## 4. Findings — Measurement and alert-analytics dashboards

### 4.1 The metric taxonomy is stratified by reader, not by object

ISA-TR18.2.5 organises alarm-system analysis into five categories, each with a named
audience `[S11]`:

| Category | Audience | Named contents |
|---|---|---|
| **Performance metrics** | Operations management | Average alarm rate; percent of time in flood; quantity and listing of out-of-service alarms; alarm priority or type distribution |
| **Diagnostic metrics** | Whoever fixes specific alarms | Listing and quantity of the most frequent alarms; listing and quantity of chattering alarms; listing of stale alarms; **listing of shelved alarms with shelving duration**; listing of out-of-service alarms with durations; listing of alarms shown to be potentially redundant |
| **Deployment metrics** | Programme owners | Percent of alarms rationalized; percent monitored; priority distribution of rationalized alarms |
| **Scaling metrics** | Not reported directly | Number of configured alarms; number of alarm occurrences — used to compute the others |
| **Audit metrics** | System owners and operations | **"Number and nature of unauthorized alarm changes"; "number and nature of unauthorized alarm suppression"** |

The split that matters for S-21 is **performance versus diagnostic**. A performance
metric is a rate against a target and answers *is this system behaving*. A diagnostic
metric is a *ranked list of named offenders* and answers *which specific thing do I fix
first*. IBVAP's FR-49 describes the first and its cause histogram gestures at the second,
but S-21 as currently written does not distinguish them, and the standard's structure
suggests they are different views for different readers rather than two panels of one
chart.

### 4.2 The target values, and the caveat the standard itself attaches

ISA-18.2 Table 7 is reproduced here because it is the only published, standardised set of
alert-load targets found in either research pass `[S10]`:

| Metric | Target |
|---|---|
| Annunciated alarms per hour per operator console | ~6 average ("very likely to be acceptable"); ~12 average ("maximum manageable") |
| Annunciated alarms per 10 minutes per operator console | ~1 average; ~2 maximum manageable |
| Percentage of 10-minute periods containing more than 10 alarms | ~<1% |
| Maximum number of alarms in a 10-minute period | ≤10 |
| Percentage of time the alarm system is in a flood condition | ~<1% |
| Percentage contribution of the **top 10 most frequent alarms** to overall load | "~<1% to 5% maximum, with action plans to address deficiencies" |
| Quantity of chattering and fleeting alarms | "Zero, action plans to correct any that occur" |
| Stale alarms (annunciated continuously >24 h) | "Less than 5 present on any day, with action plans to address" |
| Annunciated priority distribution | ~80% low, ~15% medium, ~5% high |

Three properties of this table are worth carrying forward independently of the numbers.
First, **the metrics are computed over at least 30 days of data** — the standard states
this twice, and it means a measurement surface has a *minimum honest window* below which
it should say so rather than draw a line `[S10]`. Second, several targets are stated not
as a number but as a number *plus an obligation* — "with action plans to address" — which
makes the metric a work queue rather than a score. Third, the standard undercuts its own
table: "The target metrics described below are approximate and depend upon many
factors… Maximum acceptable numbers could be significantly lower or perhaps slightly
higher depending upon these factors. **Alarm rate alone is not an indicator of
acceptability**" `[S10]`.

That last caution is amplified by practitioner criticism. One alarm-management paper
argues at length that converting "one alarm per ten minutes" into "six alarms per hour"
is illegitimate, that average rates conceal the distribution that actually harms
operators, and that response-time averages are meaningless when stale, fleeting and
chattering alarms are included in the denominator `[S12]`. The paper is an individual
practitioner's opinion piece rather than a standard, and is recorded here as a
well-argued dissent rather than as settled fact — but the specific point that **an
average rate hides the peaks that break an operator** is consistent with the standard's
own insistence on reporting peak alarm rate alongside average, and on reporting "the
number of intervals exceeding 10 alarms, and the magnitude of the highest peaks"
`[S10]`.

### 4.3 The named nuisance vocabulary

ISA-18.2's definitions are normative and precise `[S10]`:

- **Nuisance alarm** — "alarm that annunciates excessively, unnecessarily, or does not
  return to normal after the operator action is taken," with chattering, fleeting and
  stale alarms given as the examples.
- **Chattering alarm** — "repeatedly transitions between the active state and the not
  active state in a short period of time," where "the transition is not due to the result
  of operator action."
- **Fleeting alarm** — a similar short-duration alarm "that do[es] not immediately
  repeat."
- **Stale alarm** — annunciated continuously for an extended duration, "e.g., longer than
  24 hours."
- **Frequently occurring alarms** — the standard observes that "relatively few individual
  alarms (e.g., 10 to 20 alarms) often produce a large percentage of the total alarm
  system load (e.g., 20% to 80%)," and that these "should be reviewed at regular
  intervals (e.g., daily, weekly, or monthly)."

The last is the practical heart of the whole clause: fixing the ten noisiest sources
usually fixes most of the noise. Independent SOC practice appears to have converged on
the same tactic — vendor and practitioner writing describes dashboards showing the top
rules by false-positive volume with a weekly review of the noisiest, and describes
false-positive rate *per rule* as the core detection-quality metric `[S20]`. That
material is blog-quality and is recorded as corroborating practice rather than as
verified fact; the standard is the citable source.

### 4.4 Where suppression appears in measurement

Both places ISA-18.2 puts suppression into measurement are relevant to IBVAP. As a
*diagnostic* metric, the required listing is "shelved alarms with shelving duration"
`[S11]` — not a count, a list with a clock. As an *audit* metric, the required content is
"number and nature of unauthorized alarm suppression" `[S11]`, and clause 16.5 states
that "alarm state transitions to suppressed states and from suppressed states should be
recorded," that uncontrolled suppression "should be detected and reported," and that
"there should be no alarms that are suppressed without authorization" `[S10]`. Clause
16.6 adds that unauthorized *attribute* changes "shall be detected and resolved by
comparison of actual alarm attributes against rationalization information," with "the
target value for unauthorized changes to alarms is zero" `[S10]`.

Measured suppression is therefore not one number on a dashboard. It is a live list with
remaining time, plus an audit finding whose target is zero.

### 4.5 What the SOC platforms add

Splunk and Sentinel document the *inputs* to alert measurement more than the dashboards
themselves. The important contribution is that disposition is a queryable field
independent of status, which is what makes a per-rule false-positive rate computable at
all `[S5][S6]`. Splunk documents sorting notables by disposition as a named workflow for
reducing alert volume, and the "Required" toggle exists precisely so that the disposition
field is populated densely enough to be worth aggregating `[S6]`. **The measurement
surface and the dismissal-reason capture are the same design problem seen from two ends**
— which is exactly the relationship between IBVAP's gap 1 and gap 2.

---

## 5. Findings — Dismissal and false-positive reason capture

### 5.1 The three-platform convergence

| | Splunk ES `[S5][S6]` | Microsoft Sentinel `[S8]` | IBM QRadar `[S9]` |
|---|---|---|---|
| Field name | Disposition | Classification | Reason for Closing |
| When captured | Any time; optionally required before an end status | **On close only** | On close |
| Mandatory? | Configurable — "Required" toggle | **Yes** — "Selecting a classification is mandatory" | Required from a list |
| Default | *Undetermined* | none preselected | site-defined |
| Preset list | 7 values | 5 values | predefined plus admin-added custom reasons |
| Free text | Separate comment field | Separate **Comment** field, recommended not required | Notes field |
| Independent of status? | **Yes**, explicitly | Yes | Yes |
| Extensible? | "You can also add a custom disposition" | not documented as extensible | **Yes** — custom close reasons are an administrator feature |

The convergence is strong enough to be treated as a genuine pattern rather than
coincidence: **a short closed list of preset reasons, an explicit "undetermined" escape
hatch, a separate optional free-text comment, capture at closure rather than at first
touch, and site-level extensibility of the list.**

### 5.2 The exact vocabularies

Splunk Enterprise Security's default dispositions, with the documentation's own
definitions `[S6]`:

- **Undetermined** — "Finding does not have a valid disposition due to an error." (the
  default)
- **True Positive - Suspicious Activity** — "Finding indicates suspicious threat
  activity."
- **Benign Positive - Suspicious But Expected** — "Finding was initially suspicious but
  then classified as harmless and expected."
- **False Positive - Incorrect Analytic Logic** — "…classified as harmless due to
  incorrect analytic logic."
- **False Positive - Inaccurate Data** — "…classified as harmless due to inaccurate
  data."
- **Other** — "A catchall category for findings that are not classified."
- **Testing** — "Category for testing field inputs and drilldown searches."

Microsoft Sentinel's list is the same minus *Other* and *Testing* `[S8]`. Microsoft's
supporting material defines a benign positive as an action "that is real, but not
malicious," giving a penetration test or an approved application as examples, and defines
*false positive – incorrect alert logic* as the case where "the Analytics Rule logic that
triggered the alert was configured incorrectly."

Three structural observations, all transferable to a video analytic:

1. **"Real but not a threat" is a distinct outcome from "not real."** A person walking
   inside a zone at a permitted time is a benign positive; a shadow that triggered a
   person class is a false positive. These carry entirely different implications for
   whether the detector or the rule needs changing, and a two-value real/not-real
   assessment cannot express the difference. IBVAP's `unsure` is a *confidence* escape,
   not this axis.
2. **The false-positive values split by fault location, not by scene content.** "Bad
   rule logic" versus "bad input data" is a question about which part of the pipeline to
   fix. A wind-versus-animal-versus-glare taxonomy is a question about the physical
   world. These are orthogonal, and no surveyed platform captures the second.
3. **"Undetermined" is a first-class default, not a punishment.** Splunk ships it as the
   default value with an explicit definition; Sentinel lists it alongside the others.
   This parallels IBVAP's treatment of `unsure` as first-class under F-3.

### 5.3 The precedent for a reason on suppression rather than on dismissal

ISA-18.2 does not require a reason for acknowledging an alarm. It **does** require a
reason for shelving one: for each shelved alarm extending beyond a time limit set in the
alarm philosophy, the record shall contain "the tag name for alarm," "the tag description
or alarm description for alarm," and "**the reason for shelving**" `[S10]`. It further
recommends that "shelved alarms extending beyond a single operating shift should be
reviewed," with the review procedure documented `[S10]`, and for highly managed alarm
classes requires that shelving "follow authorization and reauthorization requirements,"
with documentation "including approval, interim alarms and procedures, and
reauthorization details" `[S10]`.

This is a materially different design position from the SIEM one and it is worth stating
plainly: **the standard puts the reason where the consequence is.** Dismissing one alarm
costs nothing; silencing a class of alarms for hours costs something, and that is where a
justification becomes mandatory. For IBVAP, whose F-2 forbids turning assessment into a
form but whose FR-30 already makes suppression a deliberate, recorded, reversible act,
this is the reconciling precedent.

### 5.4 What Gotham contributes here

Only the interaction shape: AI detections in Gotham's Video application "are surfaced to
users for confirmation or dismissal," with live feedback flowing back to model accuracy,
and unspecified "quality control steps" available to make the analyst's assessment
"well-considered" `[S1]`. Confirm/dismiss as a binary on a video detection is
corroborated. A reason vocabulary is not documented, and none should be attributed to
Gotham.

---

## 6. Findings — Case and investigation lifecycle

### 6.1 Two axes, not one

The clearest evidence in this pass is Chicago Police Department's fielded case-status
list, released to a news organisation in 2019 and reproduced here in its own words
`[S17]`:

| Status | Definition (verbatim, abridged) |
|---|---|
| **Open unassigned** | "Case/report comes in and is being reviewed but has not yet been assigned to a detective." |
| **Open assigned** | "Case has been opened and assigned to a detective." |
| **Suspended** | "…the detective began the investigation but there are no additional investigative leads at this time… **If a victim follows back up with police at a later time, the case will be re-opened.**" |
| **Cleared open** | "At least one person is being prosecuted but there may be more offenders." |
| **Cleared closed** | "Offender has been taken into custody and charged. Case will move on to prosecution." |
| **Exceptionally cleared open** | "The case is considered cleared but a detective has requested to keep it open for some reason." |
| **Exceptionally cleared closed** | "The case was cleared by exceptional means" — a known suspect the case cannot proceed against. |
| **Closed non-criminal** | "The case was investigated, and the crime may have occurred but there is insufficient evidence." |
| **Unfounded** | "During the course of an investigation, police found the incident did not happen as the person reported it." |

Read as a table, this is one vocabulary. Read as a grid it is two: an **outcome** axis
(unassigned / under investigation / cleared / exceptionally cleared / non-criminal /
unfounded) crossed with a **workflow** axis (open / closed / suspended). The department
has flattened the grid into compound names because the underlying records system needed a
single status code — which is a design constraint worth noticing rather than copying.

A published university police department policy documents the same vocabulary with
different labels and adds the procedural machinery `[S16]`: *Warrant(s) Obtained*,
*Closed by Arrest* ("cleared by arrest when at least one person is arrested and
charged"), *Closed by Exception* ("the offender has been identified, there is sufficient
information to support an arrest, and there is some reason outside our control that
prevents us from arresting"), *Closed by Other Means* ("no resolution (i.e. Leads
Exhausted)"), *Inactive* ("not further leads or… few or no solvability factors"), and
*Unfounded*. The status codes themselves are stated to conform to codes "established by
the North Carolina State Bureau of Investigation" — **the vocabulary is externally
mandated, not chosen by the department.**

### 6.2 Who moves a case, and how it reopens

From the same policy `[S16]`:

- **Screening before assignment.** Cases are screened against solvability factors, and a
  named role — the Support Services Commander — "reviews reports to determine active
  versus inactive status." Certain offence types (homicide, armed robbery, rape,
  kidnapping, arson and others) bypass screening entirely and are always assigned. The
  triage decision is a named person's, against written criteria — the same structure the
  border pass found in Frontex's SIR SOP, where categorisation "is a decision made by a
  named role against written criteria, not a dropdown the reporter picks."
- **Who clears.** "Assigned detectives clear investigations by filing supplemental or
  arrest reports with appropriate status codes." Closure is effected by *filing a
  document*, not by flipping a field.
- **Standing supervisory review.** The commander "ensures the open investigation page is
  kept up to date" and reviews cold-case-eligible cases annually.
- **Reopening.** Cases may be reopened when "information becomes available that may
  further the investigation," with named considerations — forensic testing availability,
  witness availability, and victim or family willingness. Reopening is a *criteria-based
  decision*, not a button.

CPD's *Suspended* definition adds the most operationally common reopen trigger: an
external party makes contact again `[S17]`. Both sources agree that **a case in the
not-currently-worked state is not a terminal state** — it is a parked state with a
documented route back.

### 6.3 The SOC platforms' state machines

Splunk Enterprise Security's default statuses, with its own definitions `[S5]`:

| Status | Definition |
|---|---|
| **New** | "Default status. The event has not been reviewed." |
| **In Progress** | "An owner is investigating the event." |
| **Pending** | "The assignee must take an action." |
| **Resolved** | "The owner has addressed the cause of the event and is waiting for verification." |
| **Closed** | "The resolution of the event has been verified." |
| **Unassigned** | "Used by Enterprise Security when an error prevents the notable from having a valid status assignment." |

Two features of this list are more interesting than the names. First, **Resolved and
Closed are different states separated by a verification step performed by someone other
than the owner** — the same separation of substantive conclusion from administrative
closure found in Frontex's SIR SOP and in CPD's *cleared open* versus *cleared closed*.
Second, *Unassigned* exists as an explicit error state rather than as an absence, and
Splunk documents that transitions *into* the default statuses from Unassigned are
possible while transitions *to* Unassigned are not `[S7]`.

The state machine itself is configurable. Splunk documents an **End Status** flag applied
when "adding an additional Closed status… such as False Positive," and documents that
administrators may restrict which roles may make which transitions, "so that you have
more control over managing the operations of your SOC." By default "an investigation in
any status can be changed to any other status" `[S7]` — meaning **reopening a closed item
is permitted unless someone deliberately forbids it.** Status-change ability is
role-gated to `ess_analyst` and `ess_admin` by default `[S7]`.

Sentinel is simpler: New / Active / Closed, ownership assigned from a dropdown with
recently-used users at the top, tags and comments on the same pane, and a required
classification on close `[S8]`. Microsoft's documentation is explicit that triage happens
"right from the details pane on the Incidents page, without having to enter the
incident's full details page," and supports bulk edit across selected or all matching
incidents — as does Splunk, which documents "Edit all selected" and "Edit all ##
matching events" `[S5][S8]`.

### 6.4 Ownership and handover

- **Assignment is one control, with a self-assign shortcut.** Splunk: "Select an Owner to
  assign the notable. Or, click Assign to me." Owners "are unassigned by default," and
  assignment is restricted to users holding specific roles `[S5]`. Sentinel: assign from
  the Owner dropdown on the details pane, to a user *or a group* `[S8]`.
- **Exactly one handler is the norm in the investigative sources.** Frontex assigns
  exactly one SI-Handler (border pass, §4.2); the police policies assign a case to a
  detective `[S16]`. Sentinel's ability to assign to a group is the only shared-ownership
  mechanic documented in this pass `[S8]`.
- **Handover out of the system is a document, not a state.** The police policy describes
  the case file as containing "all records of the investigation, including statements of
  witnesses and suspects, results of examinations of physical evidence, case status
  reports, and other reports and records needed for investigative purposes" `[S16]`.
  Nothing in the surveyed platforms models the receiving prosecutor as an actor. This
  matches the border pass's F6 and W-F: the pack leaves, and the system's job ends at
  producing something that survives the journey.
- **Gotham's only documented handover property** is Dossier's statement that "work is
  preserved even if one or more Dossier contributors switch out to focus on other tasks,"
  and that dossiers can be exported to Word or PDF "for dissemination to partners"
  `[S1]`. There is no assignment field, no owner, and no state.

---

## 7. Findings — Authentication and session design

### 7.1 The timeout numbers, and the fact that they moved

NIST SP 800-63B rev 4, published 26 August 2025, sets reauthentication limits per
assurance level `[S13]`:

| Level | Overall timeout | Inactivity timeout |
|---|---|---|
| **AAL1** | SHOULD be no more than **30 days** | MAY be applied but is not required |
| **AAL2** | SHOULD be no more than **24 hours** | SHOULD be no more than **1 hour** |
| **AAL3** | **SHALL** be no more than **12 hours** | SHOULD be no more than **15 minutes** |

At AAL2, after an inactivity timeout but before the overall timeout, the verifier "MAY
allow the subscriber to reauthenticate using only a successful password or biometric
comparison" in conjunction with the session secret `[S13]` — a *soft* reauthentication
that does not demand the second factor again.

**These values are a relaxation of the previous revision, and the older values are still
in force in places.** Criminal-justice security policy restates rev-3's AAL2 criteria
verbatim as binding requirements: "Reauthentication of the subscriber SHALL be repeated
at least once per 12 hours during an extended usage session" and "SHALL be repeated
following any period of inactivity lasting 30 minutes or longer" `[S15]`. The same policy
separately requires a **session lock "after a maximum of 30 minutes of inactivity"**
which "remains in effect until the user reestablishes access using appropriate
identification and authentication procedures," and a **network disconnect** "at the end
of the session or after one (1) hour of inactivity" `[S15]`.

So the honest statement of the state of the art is: **for a high-consequence system, the
defensible inactivity window is somewhere between 30 minutes and 1 hour and the
defensible overall session length is somewhere between 12 and 24 hours, and which end of
each range applies is a policy choice the deploying force makes, not a fact the standard
settles.** Rev 3 and rev 4 genuinely disagree, and a criminal-justice deployment may be
bound to the stricter, older text regardless of what the current standard says.

### 7.2 The exemption that matches an unattended display

CJIS policy names three categories exempt from the 30-minute session lock "in the
interest of safety" `[S15]`:

> i. part of a criminal justice conveyance.
> ii. used to perform dispatch functions and located within a physically secure location.
> iii. terminals designated solely for the purpose of receiving alert notifications (i.e.,
> receive only terminals or ROT) used within physically secure location facilities that
> remain staffed when in operation.

The third is precisely the design of a read-only annunciator. The exemption is granted
because the terminal *receives only* — it cannot act, so there is nothing an unattended
session could be used to do. Note also what the policy says immediately before: "A
session lock is not a substitute for logging out of the information system," and users
"shall directly initiate session lock mechanisms to prevent inadvertent viewing when a
device is unattended" `[S15]`. The lock is about shoulder-surfing; the logout is about
attribution.

### 7.3 Lockout: the standards disagree, and the disagreement matters

| | NIST SP 800-63B rev 4 `[S13]` | CJIS policy `[S15]` |
|---|---|---|
| Failed-attempt limit | "SHALL limit consecutive failed authentication attempts… to no more than **100** by disabling that authenticator" | "no more than **five (5)** consecutive invalid access attempts" |
| Consequence | Authenticator disabled; requires rebinding to reactivate | "automatically lock the account/node for a **ten (10) minute** time period unless released by an administrator" |
| Preferred mitigations | Bot-detection challenges, **progressive delays**, risk-based decisions | not specified |
| Reset on success | "When the subscriber successfully authenticates, the verifier SHOULD disregard any previous failed attempts" | not specified |

NIST's posture is that throttling and progressive delay are the primary defence and hard
lockout is the last resort at a very high threshold; CJIS's is a hard, low-threshold
lockout with an administrator override. For a site with one operator and no
administrator to call, the CJIS shape has an obvious failure mode — the operator locks
themselves out of an alerting system and there is nobody to release it. **The mitigation
CJIS itself provides, an administrator release, is exactly the resource the deployment
does not have.** This is a real, unresolved tension, not a solved problem, and no source
retrieved in this pass addresses lockout at an unstaffed or single-staffed site.

### 7.4 Recovery when there is nobody to call

The standards are unusually prescriptive here, and what they prescribe is *not*
self-service `[S13][S15]`:

- **Security questions are prohibited.** "Verifiers SHALL NOT prompt subscribers to use
  specific types of information (e.g., 'What was the name of your first pet?') when
  choosing memorized secrets" `[S15]`.
- **Password hints are prohibited.** Verifiers "SHALL NOT permit the subscriber to store a
  'hint' that is accessible to an unauthenticated claimant" `[S15]`.
- **Adding a new authenticator requires authenticating first.** "Before adding a new
  authenticator to a subscriber's account, the CSP SHALL first require the subscriber to
  authenticate at AAL2 (or a higher AAL) at which the new authenticator will be used"
  `[S15]`.
- **Losing every factor means starting over.** If a subscriber "loses all authenticators
  of a factor necessary to complete multi-factor authentication and has been identity
  proofed at IAL2, that subscriber SHALL repeat the identity proofing process." If one
  factor survives, it "SHALL" be used "to confirm binding to the existing identity"
  `[S15]`.
- **Recovery forces a new secret immediately.** "Require immediate selection of a new
  password upon account recovery" `[S15]`.
- **Recovery codes are the documented backstop.** Rev 4 names look-up secrets — recovery
  codes — as backup authenticators for account recovery when primary authenticators are
  lost `[S13]`.
- **Periodic password change is forbidden.** Rev 4: verifiers "SHALL NOT require
  subscribers to change passwords periodically," with a forced change only "if there is
  evidence that the authenticator has been compromised" `[S13]`. Composition rules are
  also forbidden ("SHALL NOT impose other composition rules"), with minimum lengths of 15
  characters for single-factor and 8 for multi-factor passwords, and a maximum of at
  least 64.

The consistent answer these give to "who resets the password at a site with no IT" is
**a locally held administrative capability plus pre-issued recovery codes** — not a
self-service reset flow, and emphatically not knowledge-based questions. The border
pass's F10 supplies the organisational half of the same answer: the field tier is a peer
client with its own administration, not a thin view of a control room that may not exist.

### 7.5 Fast action versus authenticated action

No source retrieved resolves this by weakening authentication. The three mechanisms
documented for making an authenticated action fast are:

1. **Triage without navigation.** Sentinel: act "right from the details pane on the
   **Incidents** page, without having to enter the incident's full details page" `[S8]`.
   Splunk: status, owner and disposition are all set from the Incident Review list
   `[S5]`. The saving comes from collapsing the screen count, not the auth count.
2. **Bulk action.** Both platforms document editing many items at once, including "all
   ## matching events" `[S5][S8]`. Where alerts arrive in correlated bursts, one
   authenticated action can dispose of many.
3. **Soft reauthentication.** NIST AAL2 permits reauthenticating after inactivity "using
   only a successful password or biometric comparison" alongside the retained session
   secret `[S13]` — the resumption cost is one factor, not two.

Gotham's contribution is the "multiple instances of any application from within the same
session" property `[S1]` — one session, many working contexts — which is the same
instinct as (1).

---

## 8. Cross-Platform Patterns and Disagreements

**P-A. Outcome and administrative state are separate fields, everywhere.** Splunk says so
explicitly `[S6]`; Sentinel captures classification at the close transition `[S8]`; CPD
multiplies the two axes into compound status names `[S17]`; Frontex separates the
handler's final report from the Situation Centre's administrative closure (border pass
§4.2). No surveyed system collapses them, and the one that came closest — CPD — did so
apparently because a single status code field forced it.

**P-B. Reason lists are short, closed, extensible and carry an explicit "don't know."**
Five to seven values; *Undetermined* present in every SIEM list; custom values addable by
an administrator in Splunk and QRadar `[S6][S9]`. Nobody uses free text as the primary
capture; everybody offers free text alongside.

**P-C. The reason is demanded at the consequential moment, not the first touch.** SIEMs
demand it at close `[S6][S8][S9]`; ISA-18.2 demands it at shelving `[S10]`. Nothing
demands it at acknowledgement.

**P-D. Suppression is legitimate, required, time-limited and audited.** ISA-18.2 makes
shelving a required function with a mandatory time limit, mandatory access control,
mandatory record, and an automatic unshelve on expiry `[S10]`; and makes "unauthorized
alarm suppression" a named audit metric with an implied target of zero `[S10][S11]`.

**P-E. Not-currently-worked is a parked state with a documented route back, not a
terminal state.** *Suspended* `[S17]`, *Inactive* `[S16]`, *Pending* `[S5]`. Splunk
permits any-to-any transitions by default `[S7]`; the police policies gate reopening on
named criteria `[S16][S17]`.

**P-F. Assignment is one control with a self-assign shortcut, and one handler is the
norm.** `[S5][S8][S16]`, and Frontex's single SI-Handler in the border pass.

**P-G. Speed comes from removing navigation, not from removing authentication.**
`[S5][S8][S13]`.

### Disagreements worth recording rather than resolving

**D-i. Session timeouts.** NIST rev 4 says AAL2 SHOULD be ≤24 h overall and ≤1 h
inactive `[S13]`; rev 3, as restated in binding criminal-justice policy, says SHALL be
≤12 h and ≤30 min `[S15]`. Both are current in the sense that both bind somebody today.

**D-ii. Lockout.** NIST rev 4 tolerates up to 100 failed attempts and prefers progressive
delays `[S13]`; CJIS mandates five and a ten-minute lock `[S15]`. The gap is a factor of
twenty, and neither addresses a site with no administrator.

**D-iii. Is the average alert rate a meaningful metric at all?** ISA-18.2 publishes
targets and then warns that "alarm rate alone is not an indicator of acceptability"
`[S10]`; a practitioner critique argues the averaging itself is misleading and that peak
distribution is what matters `[S12]`. The standard partially agrees with its own critic
by requiring peak reporting alongside average.

**D-iv. Should a dismissal reason ever be mandatory?** Sentinel: yes, always, on close
`[S8]`. Splunk: only if an administrator turns it on `[S6]`. ISA-18.2: not for
acknowledgement, yes for prolonged shelving `[S10]`. There is no consensus, and IBVAP's
F-2 sits on the permissive end of a genuinely contested question.

**D-v. Can a closed item be reopened?** Splunk: yes by default, restrictable `[S7]`.
Police policy: yes, on named criteria, as a supervisory decision `[S16][S17]`. Sentinel
and Gotham: not documented either way.

---

## 9. Recommendations for IBVAP's UX

Nothing below is a decision. Each item is a concrete, traceable option for the design
pass that will specify these screens, and each names the finding it comes from. Where a
recommendation collides with an existing UX decision, the collision is stated rather than
smoothed over.

### 9.1 S-21 Measurement

**R-1. Split S-21 into a rate view and a ranked-offender view, not two charts on one
page.** ISA-18.2 separates *performance* metrics (rates against targets, for whoever owns
the site) from *diagnostic* metrics (named lists of the specific worst contributors, for
whoever fixes them) `[S11]`. IBVAP's readers are frequently the same person, but the two
questions — *is this system behaving* and *what do I fix first* — are asked at different
moments. Traces to [§4.1](#41-the-metric-taxonomy-is-stratified-by-reader-not-by-object).

**R-2. Lead the diagnostic view with a top-N noisiest camera+rule pairs list.** The
standard's observation that ten to twenty alarms often produce 20–80% of total load, and
its target that the top ten contribute under ~5%, make "the top ten and what share of all
alerts they caused" the single highest-value number on the screen `[S10]`. Traces to
[§4.3](#43-the-named-nuisance-vocabulary).

**R-3. Report peak alongside average, and never average alone.** ISA-18.2 requires
reporting "the number of intervals exceeding 10 alarms, and the magnitude of the highest
peaks" beside the mean, and states that alarm rate alone is not an indicator of
acceptability `[S10]`. A practitioner critique goes further and argues averages actively
mislead `[S12]`. For IBVAP a defensible minimum is: alerts per hour per camera+rule
(mean), plus the worst hour in the window, plus how many hours exceeded a stated
threshold. Traces to [§4.2](#42-the-target-values-and-the-caveat-the-standard-itself-attaches).

**R-4. State the measurement window on the screen and refuse to draw a trend below it.**
ISA-18.2 states twice that at least 30 days of data is desirable for these metrics
`[S10]`. IBVAP already commits under AC-P7 to labelling every number as measured on this
deployment's own footage; adding *over what window, from what date* completes the claim,
and gives the screen an honest empty state during the first weeks of a deployment —
which §18's state families already require it to distinguish from "nothing happened."
Traces to [§4.2](#42-the-target-values-and-the-caveat-the-standard-itself-attaches).

**R-5. Do not ship ISA-18.2's target numbers as IBVAP's targets.** They are process-plant
values for a continuously staffed console, and the standard itself says maximum
acceptable numbers "could be significantly lower or perhaps slightly higher" depending on
context `[S10]`. What transfers is the *metric list and its structure*, not ~6/hour. This
is the same caution NFR-4 already applies to setting numbers before measuring them.
Traces to [§4.2](#42-the-target-values-and-the-caveat-the-standard-itself-attaches).

**R-6. Give suppression its own panel on S-21: a live list with remaining time, plus a
count of suppressions that expired without reconfirmation.** ISA-18.2 makes "shelved
alarms with shelving duration" a required diagnostic listing and "number and nature of
unauthorized alarm suppression" a required audit metric `[S10][S11]`. IBVAP already has
the underlying states from UX-14 — offered, active, reconfirmation due, expired — and
S-21 is where their aggregate belongs. Traces to
[§4.4](#44-where-suppression-appears-in-measurement).

**R-7. Carry the day/night split through every metric, not only the headline rate.** This
is IBVAP-specific and has no external precedent — none of the surveyed platforms has a
diurnal dimension at all — but FR-49 and AC-7.3/7.4 already require it, and the
implication of R-1 and R-2 is that the split must reach the ranked lists too, or the
night-time bad actors will be averaged into invisibility.

### 9.2 The alert-dismissal flow (S-04 / S-05)

**R-8. Keep assessment one action, and attach the cause to the *consequential* act rather
than to the assessment.** ISA-18.2 requires no reason to acknowledge an alarm but requires
"the reason for shelving" when a suppression outlasts a defined limit `[S10]`; the SIEMs
require their reason at *close*, never at first touch `[S6][S8]`. IBVAP already has a
consequential act in exactly the right place: **the per-camera-per-rule suppression
offered after a `not real` assessment (FR-30).** Making the cause a required field on
*applying or reconfirming a suppression* — where a human is already choosing to silence a
class of alerts and where UX-14 already demands attribution — preserves F-2 intact and
still populates the cause histogram from the alerts that matter most to it. Traces to
[§5.3](#53-the-precedent-for-a-reason-on-suppression-rather-than-on-dismissal).

**R-9. Where a cause is offered at assessment time, make it one optional tap on a short
preset list with an explicit "don't know," never free text and never blocking.** Every
surveyed platform uses a closed list of five to seven values with an explicit
*Undetermined* and a separate optional comment `[S6][S8][S9]`. A `not real` tap that
reveals a small row of cause chips, any of which is optional and any of which completes
the interaction, is the closest fit to both the evidence and F-2. Traces to
[§5.1](#51-the-three-platform-convergence) and
[§5.2](#52-the-exact-vocabularies).

**R-10. Consider adding a "real but not of interest" outcome distinct from `not real`.**
Every SIEM surveyed separates *benign positive — suspicious but expected* from *false
positive* `[S6][S8]`, because they carry opposite implications: one says the detector
worked and the rule is wrong, the other says the detector fired on nothing. IBVAP's
current three outcomes cannot express the difference, and a nuisance-rate figure that
conflates "the camera saw a real cow" with "the camera saw a shadow it called a person"
is measuring two different faults as one. **This is a product decision, not a design
one** — it changes FR-29's outcome vocabulary and therefore MVP scope, and it is recorded
here as an evidenced option rather than a recommendation to adopt. Traces to
[§5.2](#52-the-exact-vocabularies).

**R-11. Make the cause list site-extensible and treat its contents as an open product
question.** Splunk and QRadar both let an administrator add reasons to the preset list
`[S6][S9]`. More importantly, **no source in this pass publishes a scene-cause taxonomy
for video** ([§2](#2-research-scope)) — wind, animal, shadow, glare and rain have no
external precedent found here, so whatever list IBVAP ships is an unvalidated first
attempt and should be structured to be revised from its own data. Traces to
[§5.1](#51-the-three-platform-convergence).

### 9.3 The Case state model (S-08 / S-09)

**R-12. Model the Case on two axes and show both: an administrative state and a recorded
outcome.** This is the strongest single finding in the document — Splunk states the
separation as a design principle `[S6]`, Sentinel enforces it as a required field on a
state transition `[S8]`, CPD encodes it in compound status names `[S17]`, and Frontex
separates the handler's conclusion from the Situation Centre's administrative closure
(border pass §4.2). IBVAP already has half of it: UX-17 makes closure "a separate
administrative act from recording the outcome." Making that explicit as **two visible
fields with independent values** completes it. Traces to
[§6.1](#61-two-axes-not-one).

**R-13. Add the missing administrative states: `open unassigned` at creation, and a
parked state that is not closure.** All three case sources distinguish a case that exists
from a case someone is working — *Open unassigned* / *Open assigned* `[S17]`, Splunk's
*New* / *In Progress* `[S5]` — and all three provide a not-currently-worked state
(*Suspended*, *Inactive*, *Pending*) that is explicitly not an ending `[S5][S16][S17]`.
IBVAP's current *open → outcome recorded → exported → closed* has neither. Traces to
[§6.1](#61-two-axes-not-one) and
[§6.3](#63-the-soc-platforms-state-machines).

**R-14. Make `reopened` a real state with a recorded trigger, and permit it by default.**
Splunk permits any-to-any transitions unless an administrator restricts them `[S7]`; the
police sources permit reopening on named criteria — new information, renewed contact from
a complainant, newly available forensic testing `[S16][S17]`. For IBVAP the consequence is
concrete and already half-specified: UX-17 starts the bound evidence's retention clock at
closure, so **reopening a Case must visibly suspend that clock again**, and the reopen
must be attributed and audited to the standard NFR-14 already sets for override, export
and deletion. Traces to [§6.2](#62-who-moves-a-case-and-how-it-reopens).

**R-15. Add an explicit owner field with a self-assign shortcut, and allow it to be
empty.** Splunk's owners "are unassigned by default" with an *Assign to me* action
alongside the picker `[S5]`; Sentinel assigns to a user or a group from a dropdown
`[S8]`. At a single-operator site the owner field is trivially satisfied — which is
exactly why it costs nothing to carry, and why it is the field that makes handover
expressible when a second person eventually exists. This must not import a hierarchy:
S-23's prohibition on an assumed rank structure or org model stands, and *owner* here is
a person reference, not a role in a chain of command. Traces to
[§6.4](#64-ownership-and-handover).

**R-16. Keep the outcome vocabulary plain and resist the clearance vocabulary.** The
police vocabularies — *cleared by arrest*, *exceptionally cleared*, *unfounded* — are
legally freighted terms mandated by external statistical reporting regimes `[S16]`, and
importing them would have IBVAP asserting legal classifications that NG-12 and S-09's
"must NOT show" rule forbid. What transfers is the *shape* (a small closed outcome list
recorded separately from state), not the words. Traces to
[§6.1](#61-two-axes-not-one).

**R-17. Treat "closed" as verified rather than merely finished, if a second person
exists.** Splunk separates *Resolved* ("the owner has addressed the cause… and is waiting
for verification") from *Closed* ("the resolution of the event has been verified")
`[S5]`. This is the same two-step Frontex uses. At a one-person site the two collapse,
and forcing them apart would repeat the failure mode UX-13 already avoided when it
rejected two-person approval for overrides. The recommendation is therefore conditional:
carry the distinction in the model, collapse it in the interface when one person holds
both permissions. Traces to [§6.3](#63-the-soc-platforms-state-machines).

### 9.4 S-01 Sign in, and session behaviour

**R-18. Make the inactivity and overall session timeouts configurable, with defaults in
the evidenced range, and never hard-code them.** The standards genuinely disagree — 30
minutes and 12 hours under the older text that still binds criminal-justice deployments
`[S15]`, 1 hour and 24 hours under NIST rev 4 `[S13]`. IBVAP already treats mandated
retention as configurable-because-unknown (FR-38, OQ-9); session length is the same kind
of unknown and deserves the same treatment. Traces to
[§7.1](#71-the-timeout-numbers-and-the-fact-that-they-moved).

**R-19. Cite the receive-only-terminal exemption as the standing justification for
Annunciator mode.** CJIS exempts from session lock "terminals designated solely for the
purpose of receiving alert notifications… used within physically secure location
facilities that remain staffed when in operation" `[S15]`. That is UX-12's Annunciator
mode almost word for word, and it supplies the missing rationale: **the exemption exists
because the terminal cannot act.** S-03a's prohibition on any assessment control is not a
limitation of the decision — it is the condition that earns the exemption. Traces to
[§7.2](#72-the-exemption-that-matches-an-unattended-display).

**R-20. Prefer progressive delay over hard lockout, and make any lockout self-clearing.**
NIST rev 4 tolerates up to 100 consecutive failures with throttling, progressive delays
and a reset of the counter on success `[S13]`; CJIS's five-attempt, ten-minute lock
depends on an administrator release `[S15]` that a one-operator post does not have. A
lockout that clears itself after a stated interval, states the interval on screen, and is
recorded in the audit log satisfies both the security intent and AC-P9's requirement that
every state be sayable in one sentence over a radio. Traces to
[§7.3](#73-lockout-the-standards-disagree-and-the-disagreement-matters).

**R-21. Design recovery as pre-issued recovery codes plus a locally held administrative
reset — never security questions, never a hint, never an email round-trip.** NIST and
CJIS both forbid knowledge-based questions and stored hints `[S13][S15]`; rev 4 names
look-up secrets as the documented recovery backstop `[S13]`; and FR-61 forbids any
outbound internet dependency, which rules out email or SMS recovery outright. Recovery
codes issued at commissioning, held on paper by the post, and consumed once are the only
mechanism found in this pass that works on an isolated network with nobody to call.
Traces to [§7.4](#74-recovery-when-there-is-nobody-to-call).

**R-22. Make disabled, expired and locked visibly different states with different
sentences.** S-23 already has *person disabled*; S-25 already distinguishes *current /
expiring / expired / revoked* for authority records. The sign-in surface needs the same
discipline, and §18's rule that no state family wears another's clothes applies directly:
"wrong password," "locked for N minutes after too many attempts," "this account was
disabled by an administrator," and "your session ended after N minutes of inactivity" are
four different sentences and four different remedies. Traces to
[§7.1](#71-the-timeout-numbers-and-the-fact-that-they-moved) and
[§7.3](#73-lockout-the-standards-disagree-and-the-disagreement-matters).

**R-23. Buy back the seconds by collapsing navigation, not by weakening the session.**
Sentinel triages from the list pane without opening the incident `[S8]`; Splunk sets
status, owner and disposition from Incident Review `[S5]`; NIST permits one-factor
resumption after inactivity within the overall window `[S13]`. IBVAP already assesses in
one action from S-04's list. The remaining lever the evidence supports and IBVAP has not
taken is **bulk assessment of a correlated burst** — both SIEMs document editing all
matching items at once `[S5][S8]` — which is worth a product decision, since a burst of
alerts from one cause is precisely the case F-1's one-event-per-firing rule does not
cover. Traces to [§7.5](#75-fast-action-versus-authenticated-action).

**R-24. Do not add password expiry or composition rules.** NIST rev 4 forbids periodic
rotation and forbids composition rules outright, setting only length minimums `[S13]`.
At an unattended post, a forced expiry is a scheduled outage.

---

## 10. Open Questions

**Highest priority — these would most change the four designs.**

- **Q-1. What scene causes does a border camera's nuisance stream actually contain, in
  what proportion?** No source in this pass publishes a scene-cause taxonomy for video
  false positives ([§2](#2-research-scope)). Whatever list IBVAP ships is a hypothesis,
  and the honest way to establish it is the ≥7-day unattended run (Gate 3), with a
  free-text escape whose contents are read afterwards to build the real list.
- **Q-2. Does the benign-positive/false-positive distinction survive contact with a
  border operator?** The SIEM split is between "real but expected" and "not real"
  `[S6][S8]`. Whether an assessor at a BOP finds that distinction natural, or finds it an
  extra decision in a one-second window, is untested and is a usability question a
  validation session could answer cheaply.
- **Q-3. What is the actual disposition-completion rate when the reason is optional?**
  Splunk ships *Undetermined* as the default and lets administrators make disposition
  required `[S6]`, which strongly implies that optional capture is often left empty — but
  no source publishes the rate. If it is low, R-9's optional cause chip will not populate
  the histogram and R-8's suppression-time capture becomes the primary source rather than
  the backstop.
- **Q-4. Is IBVAP's assessment the same object as a SIEM's disposition, or the same object
  as its status?** IBVAP's `real / not real / unsure` currently does both jobs — it is the
  analytical judgement *and* the thing that marks an alert as handled. Every platform
  surveyed splits these ([§8](#8-cross-platform-patterns-and-disagreements), P-A). Whether
  IBVAP should is a product decision that R-10 and R-12 both depend on.

**High priority.**

- **Q-5.** What session and lockout policy will the deploying force actually mandate? The
  standards range from 30 min to 24 h and from 5 attempts to 100 `[S13][S15]`, and
  nothing establishes which regime binds this deployment. This is the same class of
  unknown as OQ-9 (retention).
- **Q-6.** Does anyone operate a lockout policy at a genuinely unstaffed or
  single-staffed site, and what do they do when the one person is locked out? Not
  addressed by any source retrieved.
- **Q-7.** How does a Case behave when it is reopened after its bound evidence's retention
  clock has already run? UX-17 starts the clock at closure; R-14 suspends it on reopening;
  neither addresses the case where the media is already gone. This is a real state IBVAP
  can enter and no surveyed platform models it, because none of them own the media.
- **Q-8.** Should S-21's numbers be visible to a role that cannot change rules? ISA-18.2
  aims different metric categories at different audiences `[S11]`, but IBVAP's permission
  sets are configurable by design (D-4) and the measurement screen is also the honesty
  surface (J-G) — which argues for wide visibility and against audience-gating.

**Medium priority — validate assumptions made here.**

- **Q-9.** Does Palantir publish case-lifecycle or session material anywhere not
  retrieved in this pass — in a classified-deployment manual, a US GSA schedule
  description, or congressional testimony? Searches across procurement records, public
  documentation and reporting found none ([§3.1](#31-palantir-gotham--what-is-and-is-not-publicly-documented)),
  but absence from these sources is not proof it does not exist.
- **Q-10.** What does IBM i2 iBase actually specify about per-record security and audit?
  Its documentation is behind an access gate `[S18]` and the product could not be assessed
  in this pass; it is the most likely place to find a second investigative-platform
  account of case data lifecycle.
- **Q-11.** Do any of the surveyed platforms publish a measured alert-quality figure for
  their own detections? None found. This mirrors Q-4 in the border pass — the industry
  measures nothing publicly, in either domain, which is precisely the gap FR-49 and AC-P7
  are built to occupy.
- **Q-12.** Is bulk assessment safe? Both SIEMs offer it `[S5][S8]`, but IBVAP's
  assessments are attributable evidential acts under NFR-14, and one action disposing of
  forty events may be defensible for tuning and indefensible in a case file. Unresolved.

---

## 11. References

Retrieved 2026-08-26 unless otherwise noted. **G** marks an official government,
agency, legislative or standards-body source. **P** marks a primary document whose text
was read directly rather than through a summary. **M** marks manufacturer or vendor
documentation. **I** marks an independent, academic or press source.

### Palantir Gotham

- `[S1]` **M, P** — Palantir Technologies UK Ltd, *Palantir Platform: Gotham — Service
  Definition Document*, prepared for the G-Cloud 14 Framework, dated 26 November 2024.
  PDF, 24 pages, text extracted and read in full. Vendor-written but filed into the UK
  Crown Commercial Service's Digital Marketplace, which makes it the most specific
  publicly-filed description of Gotham found. Source of the application catalogue, the
  Inbox alerting description, the Video confirm/dismiss statement, and the security
  summary.
  https://assets.applytosupply.digitalmarketplace.service.gov.uk/g-cloud-14/documents/92736/801146272055049-service-definition-document-2024-11-26-1253.pdf
- `[S2]` **M** — Palantir, *Security — Overview* (Gotham documentation).
  Source of the markings/mandatory-controls description and the statement that MFA is
  mandatory for managed SaaS customers.
  https://www.palantir.com/docs/gotham/security/overview
- `[S3]` **M** — Palantir, *Object permissioning* documentation (object security
  policies, managing object security). **Written for Foundry, not Gotham**, and used here
  only as indicative of the object- and property-level security model Gotham is stated to
  incorporate.
  https://www.palantir.com/docs/foundry/object-permissioning/overview
- `[S4]` **I** — Vice/Motherboard, "Revealed: This Is Palantir's Top-Secret User Manual
  for Cops" (2019), reporting on a leaked *Palantir Law Enforcement* user manual obtained
  via a public-records request. The manual itself was not retrieved; what is recorded
  here is the reporting's description of its contents and, importantly, of what it omits.
  https://www.vice.com/en/article/revealed-this-is-palantirs-top-secret-user-manual-for-cops/

### Alert triage and SIEM platforms

- `[S5]` **M, P** — Splunk, *Triage notables on Incident Review in Splunk Enterprise
  Security*, ES 7.3 user guide. Source of the six notable statuses with their
  definitions, the ownership mechanics, the disposition list, and the bulk-edit wording.
  https://help.splunk.com/en/splunk-enterprise-security-7/user-guide/7.3/incident-review/triage-notables-on-incident-review-in-splunk-enterprise-security
- `[S6]` **M, P** — Splunk, *Configure dispositions for findings in Splunk Enterprise
  Security*, ES 8.0 administration guide. Source of the seven default dispositions with
  definitions, the "Required" toggle, custom dispositions, and the explicit statement
  that disposition is independent of status.
  https://help.splunk.com/en/splunk-enterprise-security-8/administer/8.0/investigations/configure-dispositions-for-findings-in-splunk-enterprise-security
- `[S7]` **M, P** — Splunk, *Configure the status of findings and investigations in Splunk
  Enterprise Security*, ES 8.0 administration guide. Source of the End Status concept,
  role-gated status transitions, and the default that any status may change to any other.
  https://help.splunk.com/en/splunk-enterprise-security-8/administer/8.0/investigations/configure-the-status-of-findings-and-investigations-in-splunk-enterprise-security
- `[S8]` **M, P** — Microsoft, *Basic incident tasks for Microsoft Sentinel incidents in
  the Azure portal*, Microsoft Learn (page dated 2 July 2026, updated 8 August 2026).
  Source of the five closing classifications, the statement that classification is
  mandatory, the triage-from-the-details-pane wording, and ownership assignment.
  https://learn.microsoft.com/en-us/azure/sentinel/incident-navigate-triage
- `[S9]` **M** — IBM, *Custom offense close reasons* / *Adding a custom offense close
  reason*, QRadar documentation. **Not retrieved** — IBM's documentation host returned
  HTTP 403 to the fetch tool; recorded from search summaries of IBM's own pages and
  treated as the weakest product claim in this document.
  https://www.ibm.com/docs/en/qradar-on-cloud?topic=tasks-custom-offense-close-reasons

### Alarm management standards

- `[S10]` **G, P** — ANSI/ISA-18.2-2016, *Management of Alarm Systems for the Process
  Industries*. PDF, 82 pages, text extracted; clauses 3.1 (definitions), 5.3 (alarm
  states), 11.7 (alarm shelving), 14.3 (shelving records), 15.3 (out-of-service alarms)
  and 16 (monitoring and assessment, including Tables 5, 6 and 7) read in full. Copy
  retrieved from a third-party mirror rather than from ISA directly; the clause
  numbering, table numbering and wording are internally consistent and match ISA's own
  published summaries, but the provenance of this particular copy is not independently
  verified.
- `[S11]` **I, P** — Kim Van Camp, *Alarm System Performance Metrics* (presentation to
  ISA Ireland), summarising ISA-TR18.2.5-2012 *Alarm System Monitoring, Assessment, and
  Auditing*. PDF, 35 pages, text extracted and read. Source of the five metric categories
  and their audiences, the "listing of shelved alarms with shelving duration" diagnostic
  metric, and the "unauthorized alarm suppression" audit metric. Secondary to the
  technical report itself, which was not retrieved.
  https://isa.ie/wp-content/uploads/2016/06/Alarm_System_Performance_Metrics_Kim_Van_camp.pdf
- `[S12]` **I, P** — ProcessVue, *The Sense and Nonsense of Alarm System Performance
  KPIs*. PDF, 12 pages, text extracted and read in part. An individual practitioner's
  critique arguing that average alarm-rate KPIs mislead; recorded as a reasoned dissent,
  not as a standard.
  https://www.processvue.com/downloads/Alarm_system_performance_KPIs_V1_0.pdf

### Identity, session and security policy

- `[S13]` **G, P** — NIST Special Publication 800-63B revision 4, *Digital Identity
  Guidelines: Authentication and Authenticator Management*, 26 August 2025. Read directly
  on NIST's own site. Source of the AAL1/AAL2/AAL3 reauthentication values, the
  100-attempt rate-limiting requirement, the password composition and rotation rules, and
  the recovery-code provision.
  https://pages.nist.gov/800-63-4/sp800-63b.html
- `[S14]` **G** — NIST SP 800-63B revision 3, §7 *Session Management*, from the NIST
  GitHub source. Source of the session-secret entropy requirement, the rule that a
  session "SHALL NOT be extended past the guidelines" on presentation of the session
  secret alone, and the per-AAL reauthentication factor requirements. The rev-3 numeric
  timeouts sit in §§4.1.3/4.2.3/4.3.3 rather than in §7 and are cited here through `[S15]`,
  which restates them verbatim.
  https://github.com/usnistgov/800-63-3/blob/nist-pages/sp800-63b/sec7_session.md
- `[S15]` **G, P** — *CJIS-CT Information Security Policy* version 2.0 (Connecticut
  Criminal Justice Information System Governing Board), a state adoption restating the
  FBI CJIS Security Policy clause by clause. PDF, 190 pages, text extracted; §§5.2.3
  (unsuccessful login attempts), 5.2.5 (session lock and its exemptions), 5.8.5–5.8.6
  (authenticator management, reauthentication, memorized secrets) and 5.17.6 (network
  disconnect) read in full. **The FBI's own copy of the CJIS Security Policy was
  unreachable** — fbi.gov returned an HTML error page in place of the PDF — so all CJIS
  clause text here is cited through this state adoption.
  https://portal.ct.gov/-/media/CJIS/CISS/Related_Docs_Publications/CT_CJIS_Security_Policy_Final.pdf

### Investigative case management

- `[S16]` **G** — UNC Greensboro Police Department, policy 3-1.2 *Case Management*,
  published on PowerDMS. Source of the clearance vocabulary, the solvability-factor
  screening, the named commander role, the case-file contents, and the cold-case reopening
  criteria. Status codes are stated to conform to those "established by the North Carolina
  State Bureau of Investigation, Division of Criminal Information."
  https://public.powerdms.com/UNCPD/documents/1282919
- `[S17]` **G/I, P** — Chicago Police Department case status definitions, released to CBS
  Chicago in 2019 and hosted by the broadcaster. PDF, 1 page, text extracted and read in
  full. A department's own operational definitions rather than a policy document; the
  provenance is a news organisation's copy.
  https://assets1.cbsnewsstatic.com/i/cbslocal/wp-content/uploads/sites/15116062/2019/05/cpd-case-status-definitions.pdf
- `[S18]` **M** — i2 Group, *i2 iBase* product page, and IBM i2 documentation at
  docs.i2group.com. **The documentation is behind Cloudflare Access** and returned an
  authentication redirect; only the public product page was readable, and it contributes
  almost nothing to this document.
  https://i2group.com/i2-ibase
- `[S19]` **M** — Mark43, *RMS — Case Management and Investigations* product pages.
  Marketing prose describing accelerated assignment and closure; **no case state list,
  ownership model or lifecycle is published**, and no claim from these pages is relied on
  here.
  https://mark43.com/rms/case-management-investigations/

### Practice literature

- `[S20]` **I** — Assorted SOC-metrics practitioner and vendor writing on per-rule
  false-positive rate, signal-to-noise ratio, alert fidelity/precision, and weekly review
  of the noisiest detections. Blog-quality, commercially interested, and unverified;
  recorded only as corroborating that per-rule false-positive dashboards are common
  practice, never as a source for a number. The benchmark figures such writing quotes
  (world-class FP rate under 10%, signal-to-noise above 20%) have no published methodology
  behind them and are deliberately not reproduced as findings.
