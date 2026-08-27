# Doc Manifest

One line per file: what it holds, so it can be found without opening it. Update
whenever a doc is added, renamed, or its status changes. Not a summary of
content — just where to look.

## Contents
- [00-project](#00-project)
- [01-research](#01-research)
- [02-product](#02-product)
- [03-design](#03-design)
- [adr](#adr)

## 00-project
- [problem.md](problem.md) — official SIH problem statement, verbatim, immutable.
- [vision-and-scope.md](vision-and-scope.md) — vision statement plus required capabilities/outcomes/constraints, derived only from problem.md, unscoped. **Merged 2026-08-27** from the former separate `vision.md` and `goals.md` (which restated the same seven outcomes twice).

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
- [PRD.md](../02-product/PRD.md) — Atlassian/Confluence PRD structure (exec summary, background, goals/non-goals/success criteria, users, requirements, current build/MVP scope, roadmap, risks, open questions, references). **Merged 2026-08-27 (D-16)** with the former `MVP.md` (now §6: capability mapping, workflow, out-of-scope, acceptance criteria, known limitations — one document, not two kept in sync by hand). No FACT/ASSUMPTION/HYPOTHESIS/UNKNOWN/DECISION labels or bracket scope-tags anywhere, including in prose — uncertainty lives only in Risks and Open Questions.

## 03-design
- [UX.md](../03-design/UX.md) — **Rewritten 2026-08-26 to five screens** (Sign in, Live View, Rules, Alerts & Events, Integration), per [ADR 0016](../adr/0016-mvp-ui-cut-to-five-screens.md). Detection classes (human/vehicle/face/plate/night) are overlays and filters within Live View and Alerts & Events, not separate screens. Case management, evidence export, recognition-matching, and the audit/authority/roles/measurement/health screens are cut entirely (§8 of UX.md), not merged. **Proposed**, not approved. Its per-screen content format is a house convention, not a real UX/wireframe artifact — see the format caveat in UX.md §9.

## adr
- [README.md](../adr/README.md) — index of all 29 Architecture Decision Records, one file per decision, Nygard/MADR format. Supersedes the former `docs/00-project/decisions.md` and `docs/03-design/decisions.md` (see [ADR 0029](../adr/0029-decision-log-restructured-as-one-adr-per-file.md)). New decisions of any kind go here, never into a running log.
