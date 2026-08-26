# Doc Manifest

One line per file: what it holds, so it can be found without opening it. Update
whenever a doc is added, renamed, or its status changes. Not a summary of
content — just where to look.

## Contents
- [00-project](#00-project)
- [01-research](#01-research)
- [02-product](#02-product)
- [03-design](#03-design)

## 00-project
- [problem.md](problem.md) — official SIH problem statement, verbatim, immutable.
- [vision.md](vision.md) — vision statement, derived only from problem.md.
- [goals.md](goals.md) — required capabilities named in problem.md, unscoped.
- [decisions.md](decisions.md) — project-level DECISION log (D-1…D-14 live here).

## 01-research
- [domain/domain-research.md](../01-research/domain/domain-research.md) — generic border-CCTV surveillance domain (BSF/CIBMS-weighted).
- [domain/ssb-operational-context.md](../01-research/domain/ssb-operational-context.md) — SSB org, mandate, BOPs, CCTV/monitoring workflow, legal/evidentiary constraints.
- [domain/ssb-operational-workflow.md](../01-research/domain/ssb-operational-workflow.md) — SSB org hierarchy + incident workflow from primary sources (companion/correction to domain-research.md).
- [technology/technical-feasibility.md](../01-research/technology/technical-feasibility.md) — what's physically/technically deliverable on existing IP CCTV, no dedicated hardware.
- [competitors/competitive-landscape.md](../01-research/competitors/competitive-landscape.md) — global VMS/VCA market survey, vendor claims vs. verified.
- [competitors/international-border-surveillance-platforms.md](../01-research/competitors/international-border-surveillance-platforms.md) — real operational border-surveillance platforms (EUROSUR, CBP, TAK, Frontex SOPs), country-agnostic, differences from generic VMS. Complete.
- [competitors/investigative-case-management-platforms.md](../01-research/competitors/investigative-case-management-platforms.md) — Palantir Gotham (public docs only), ISA-18.2 alarm mgmt, NIST/CJIS auth standards, SIEM triage patterns. Grounds the S-21/dismissal-reason/Case-lifecycle/S-01 UX fixes. Complete.
- [users/product-discovery.md](../01-research/users/product-discovery.md) — synthesis of all above into users, needs, jobs-to-be-done. Complete, feeds 02-product.

## 02-product
- [PRD.md](../02-product/PRD.md) — full product requirements. **Draft** — items marked [NEEDS APPROVAL] not yet adopted.
- [MVP.md](../02-product/MVP.md) — frozen MVP scope, derived from PRD + accepted decisions D-1…D-14.

## 03-design
- [UX.md](../03-design/UX.md) — IA, screens, journeys, states for the frozen MVP. **Proposed**, not approved scope. Revised 2026-08-26 twice: (1) against international platform research (site sketch, operator impact grade, case-association retention; UX-15/16/17); (2) against investigative-case-management research (S-21 Measurement spec, dismissal-cause capture, two-axis Case model, S-01 sign-in/session spec; UX-18/19/20, UX-17 extended). Also renamed "Camera Passport" → "Camera Spec Sheet" throughout.
- [decisions.md](../03-design/decisions.md) — design-stage decisions log (UX-15…UX-20 accepted, UX-17 revised; UX-14 resolved in-stage after two revisions — suppression is an operator-chosen duration, notification-snooze style).
