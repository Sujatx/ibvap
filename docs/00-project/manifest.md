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
- [PRD.md](../02-product/PRD.md) — **Rewritten 2026-08-26** to the Atlassian/Confluence PRD structure (exec summary, background, goals/non-goals/success criteria, users, requirements, roadmap, risks, open questions, references). ~350 lines, down from 1519. The FACT/ASSUMPTION/HYPOTHESIS/UNKNOWN/DECISION/PRODUCT-MODEL label system and bracket scope-tags are removed entirely, including from plain prose — uncertainty now lives only in Risks and Open Questions, stated plainly.
- [MVP.md](../02-product/MVP.md) — **Rewritten 2026-08-26** to the five-screen scope per D-15: the 8 SIH capabilities mapped to Live View / Rules / Alerts & Events / Integration, the end-to-end loop, what's explicitly cut (Case, evidence export, recognition matching, audit/authority/roles, measurement/health dashboards), and demo acceptance criteria. ~230 lines, down from 1822. Frozen, current build scope.

## 03-design
- [UX.md](../03-design/UX.md) — **Rewritten 2026-08-26 to five screens** (Sign in, Live View, Rules, Alerts & Events, Integration), per [D-15](decisions.md). Detection classes (human/vehicle/face/plate/night) are overlays and filters within Live View and Alerts & Events, not separate screens. Case management, evidence export, recognition-matching, and the audit/authority/roles/measurement/health screens are cut entirely (§8 of UX.md), not merged. **Proposed**, not approved. The prior 27-screen version (with UX-1…UX-20 decisions) is preserved in git history and in [decisions.md](../03-design/decisions.md) below.
- [decisions.md](../03-design/decisions.md) — design-stage decisions log for the prior 27-screen UX.md (UX-1…UX-20). Superseded in scope by [D-15](../00-project/decisions.md) but kept as the historical record — not rewritten.
