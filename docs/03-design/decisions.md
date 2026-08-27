# Design Decisions Log

Record of stage-specific DECISIONs made during 03-design, each with rationale and
date, per [CLAUDE.md](../../CLAUDE.md) rule 7. Project-level decisions (D-1 … D-14)
stay in [docs/00-project/decisions.md](../00-project/decisions.md); this file is for
decisions made within the design stage itself, referenced from
[UX.md](UX.md) by their UX-n number.

**Superseded in scope by [D-15](../00-project/decisions.md)** (2026-08-26): every
entry below (UX-15 … UX-20) was made against the prior 27-screen `UX.md`. The
screens, fields and workflows they decide (Cameras site sketch, Case two-axis
state model, S-21 Measurement, dismissal-cause capture on suppression, S-01
lockout/recovery) belong to screens cut from the current five-screen build. Kept
as the historical record, not rewritten — the current `UX.md` carries forward
only what each entry's rationale still supports at five-screen scope (e.g. the
UX-14 suppression-duration pattern, which survives in [UX.md](UX.md) S-04).

Use this format per entry:

```
## YYYY-MM-DD — Short title

**DECISION:** ...
**Rationale:** ...
**Status:** proposed | accepted | superseded by <link>
```

---

## 2026-08-26 — UX-15: A static site sketch on the Cameras list, not a map

**DECISION:** `S-11` (Cameras) may carry one operator-supplied, non-interactive site
image with hand-placed camera markers, for at-a-glance orientation only — no
coordinates, no GPS, no geospatial layer, no viewshed modelling.

**Rationale:** [international-border-surveillance-platforms.md](../01-research/competitors/international-border-surveillance-platforms.md)
(F15) found every documented platform above one site provides some spatial reference
for its cameras. MVP.md's single-site boundary (D-13(a)) rules out a full common
operating picture, which stays excluded — a plain static image is a different, far
cheaper object and was previously omitted only by oversight, not by decision.

**Reference:** [UX.md](UX.md), DQ-11, §6 (S-11), §8 (S-02).

**Status:** accepted

---

## 2026-08-26 — UX-16: Operator-assigned impact grade, distinct from any computed score

**DECISION:** A human may record an optional impact/severity grade when assessing an
Alert (`S-05`) or recording a Case outcome (`S-09`). IBVAP never computes, suggests, or
defaults this value; it is always labelled as the assessor's own judgement, never as a
system finding.

**Rationale:** [international-border-surveillance-platforms.md](../01-research/competitors/international-border-surveillance-platforms.md)
(F2, §6 module 3) found every well-documented border event object carries a grade
allocated by a human on the reporting side, which a downstream C2 consumer may need to
prioritise. This is a different object from the computed threat/risk score UX-10
already, correctly, bans — the ban on a computed score stands unchanged.

**Reference:** [UX.md](UX.md), DQ-12, §9 (S-04, S-05).

**Status:** accepted

---

## 2026-08-26 — UX-17: Case-association exempts bound evidence from its retention clock

**DECISION:** While an Event's evidence is bound to a Case that has not been closed, it
is exempt from its class retention clock (`S-26`). The clock resumes, on the class's
configured schedule, from the Case's **closure** — an explicit administrative act,
separate from recording the Case's outcome — not from the evidence's original capture
time. Evidence never attached to a Case, or detached from one, is unaffected.

**Rationale:** [international-border-surveillance-platforms.md](../01-research/competitors/international-border-surveillance-platforms.md)
(F6, §9 row 13) found real border-surveillance platforms preserve evidence by case
association and overwrite by default otherwise — the opposite of a design where an open
Case's own evidence can expire out from under it, a foreseeable failure against J-D
("make this survive handover") and B4 (P0, MVP.md). FR-38 does not forbid this
construction; it simply did not require it until now.

**Reference:** [UX.md](UX.md), DQ-13, §10 (S-08/S-09, S-07), §17 (S-26).

**Status:** accepted

---

## 2026-08-26 — Egress classification/release-filter field: considered, deferred

**DECISION:** No classification, ownership or release-filter field is added to the
outbound event schema (`S-22`, FR-53) in MVP.

**Rationale:** B8's data classification is itself UNKNOWN (OQ-10). Inventing a value
set now would mean guessing a structure that FR-53's own required schema versioning
would likely have to redo once OQ-10 is actually answered by the force — the cost of
building this now is not engineering effort (trivial) but the risk of encoding a wrong
answer to a question that has not been asked yet. Revisit once OQ-10 resolves.

**Reference:** [UX.md](UX.md), note following DQ-13, §16 (S-22).

**Status:** accepted (deferred)

---

## 2026-08-26 — UX-17 revised: the Case gets a real two-axis state model

**DECISION:** UX-17 (case-association retention) is extended, not replaced. The Case
now carries two independent, always-visible fields — an **administrative state** (open
— unassigned, open — assigned, parked, closed, reopened) and a **recorded outcome**
(apprehension / seizure / nothing found / handed over / no action, unchanged) — plus an
**owner** field, a person reference, empty by default, with a self-assign shortcut.
Reopening a closed Case re-suspends the retention clock UX-17 already established.

**Rationale:** [investigative-case-management-platforms.md](../01-research/competitors/investigative-case-management-platforms.md)
(R-12 through R-17) found this two-axis separation is the single strongest convergent
pattern across every case-management system surveyed — stated as a design principle in
one, enforced as a required field in another, encoded in compound status names in a
third. IBVAP already had half of it (closure as separate from outcome, from the original
UX-17); this completes it. The outcome vocabulary deliberately does not import
legally-freighted terms ("cleared by arrest," "unfounded") that other case systems use,
since NG-12 already forbids IBVAP asserting a legal classification.

**Reference:** [UX.md](UX.md), DQ-13 (revised), §10 (S-08/S-09).

**Status:** accepted

---

## 2026-08-26 — UX-18: S-21 Measurement — rate view + ranked-offender view, no targets

**DECISION:** `S-21` shows two separate views — a rate view (mean, peak, hours-over-threshold)
and a ranked-offender view (top-N noisiest camera+rule pairs by share of total alerts) —
both split day/night throughout, with the measurement window stated on screen and no
trend drawn below it. A suppression panel shows active suppressions and how many expired
unreconfirmed. No target or "acceptable rate" number is ever displayed.

**Rationale:** [investigative-case-management-platforms.md](../01-research/competitors/investigative-case-management-platforms.md)
(R-1 through R-7) found the real alarm-management standard this maps to (ISA-18.2)
separates performance metrics from diagnostic metrics because they answer different
questions for different readers; that a ranked top-N list is the standard's own
highest-value diagnostic panel; that alarm rate without peak is explicitly not treated as
meaningful; and that the standard's numeric targets are process-plant values that should
not transfer as IBVAP's targets, consistent with NFR-4's existing caution.

**Reference:** [UX.md](UX.md), DQ-14, §11 (S-21).

**Status:** accepted

---

## 2026-08-26 — UX-19: dismissal cause captured on suppression, not on assessment

**DECISION:** The cause behind a `not real` assessment is captured when a human applies
or reconfirms the per-camera-per-rule suppression (FR-30) — never on the one-action
assessment itself. Capture is one optional tap on a short, site-extensible preset list
(e.g. wind, animal, shadow, glare, rain, other, don't know); never free text, never
blocking.

**Rationale:** [investigative-case-management-platforms.md](../01-research/competitors/investigative-case-management-platforms.md)
(R-8, R-9, R-11) found alarm-management and SIEM practice converge on capturing a reason
at the consequential act (shelving, suppression, closure), never at first
acknowledgement, using a short closed list with an explicit "undetermined." This
preserves F-2 (assessment stays one action) while still populating FR-49's required cause
histogram. No source found publishes a scene-cause taxonomy for video, so the shipped
list is recorded as an unvalidated first attempt.

**Reference:** [UX.md](UX.md), DQ-15, §9 (S-04/S-05), §11 (S-15), §17 (S-26).

**Status:** accepted

---

## 2026-08-26 — UX-20: session, lockout and recovery for a one-person, no-IT site

**DECISION:** Session timeouts are configurable, never hard-coded. Failed sign-in
triggers progressive delay rather than an administrator-cleared lockout; any lockout is
self-clearing after a stated, on-screen interval. Recovery is a pre-issued, single-use
recovery code plus a locally held administrative reset — never a security question, a
hint, or an email/SMS round-trip. No password expiry or composition rule beyond a stated
minimum length. Disabled, expired and locked are three distinct states with three
distinct sentences.

**Rationale:** [investigative-case-management-platforms.md](../01-research/competitors/investigative-case-management-platforms.md)
(R-18 through R-22) found the governing standards (NIST SP 800-63B, CJIS Security
Policy) genuinely disagree on timeout numbers by design, that the standard lockout
mechanism assumes an administrator a single-operator post does not have, and that both
standards explicitly forbid security questions and stored hints — while FR-61
independently rules out email/SMS recovery. The research also found a standing,
citable exemption for receive-only terminals that remain staffed, which supplies the
missing rationale for UX-12's Annunciator mode (already decided, not changed by this
entry).

**Reference:** [UX.md](UX.md), DQ-16, §17 (S-01, new).

**Status:** accepted

---

## 2026-08-26 — UX-14 (second revision): suppression works like a notification snooze

**DECISION:** Applying a suppression means the human picks its duration — a short
preset (1 hour / 1 day / 1 week) or "until I turn it off" (indefinite). If a duration
was chosen, the suppression ends automatically when it elapses and the rule resumes
alerting — the operator's own choice, not a product-picked schedule. It can also be
reversed early by a human at any time. Still per-camera-per-rule, still visible (count
and end time, on `S-02`, `S-15` and `S-21`), still reversible.

**Rationale:** The entry directly below dropped timing entirely in favour of pure
visibility, which is safe but forgoes a pattern every user already understands (a
notification's mute/snooze options) and leaves a permanently-affected camera suppressed
forever with nothing prompting a review. Letting the operator choose the duration each
time keeps FR-30 fully satisfied, invents no product-side number (the objection to the
original version), and needs nothing new to learn.

**Reference:** [UX.md](UX.md), DQ-6, UX-14.

**Status:** accepted

---

## 2026-08-26 — UX-14 (first revision, superseded): suppression does not expire; visibility replaces the timer

**DECISION:** None retained — **superseded by the entry above.** This entry originally
made a suppression stay active until a human reverses it, with no auto-expiry, relying
on persistent visibility (`S-02`, `S-15`, `S-21`) as the sole safeguard against one
accumulating unnoticed.

This revised the entry below it (flagged for elevation). A gap audit had found the
original `UX-14` ("time-bounded or requires periodic reconfirmation") introduced a
system behaviour no frozen FR required, and never set a duration — a placeholder number
regardless. Removing the timer fixed that, but on further discussion an operator-chosen
duration (see the entry above) fixes the same problem while keeping a timer, using a
pattern users already know.

**Reference:** [UX.md](UX.md), DQ-6, UX-14.

**Status:** superseded by the entry above

---

## 2026-08-26 — UX-14 (original, superseded): suppression auto-expiry/reactivation, flagged for elevation

**DECISION:** None — this entry recorded a flag, not a resolution. **Superseded by the
entry above.**

A gap audit against [international-border-surveillance-platforms.md](../01-research/competitors/international-border-surveillance-platforms.md)
found that the original `UX-14` ("suppression is time-bounded or requires periodic
reconfirmation," [UX.md](UX.md) DQ-6) introduced a **system behaviour** — a rule
reactivating on a clock — that no frozen FR requires. Per [UX.md](UX.md) §0.3's own
test, a capability not traceable to problem.md, MVP.md, PRD.md or an accepted D-number
is a defect in the document, and `UX-14` did not pass that test; it was written as a *UX
DECISION* (a presentation choice) when it was closer to a product decision.

**Rationale:** The underlying risk (R3/T2's "silently self-muting system") is real, but
whether suppression should auto-expire at all, and on what schedule, was a call for
whoever owns `docs/00-project/decisions.md` — not something that should be settled
inside a design document by default. On review, the better resolution turned out to be
not requiring an expiry at all (see the entry above), which sidesteps the escalation
rather than completing it.

**Reference:** [UX.md](UX.md), DQ-6, UX-14.

**Status:** superseded by the entry above
