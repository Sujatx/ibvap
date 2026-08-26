# IBVAP — Intelligent Border Video Analytics Platform

Smart India Hackathon 2026. Problem Statement ID: 26187.

## 1. Project Purpose

Build IBVAP according to the exact SIH problem statement recorded in
[docs/00-project/problem.md](docs/00-project/problem.md).

The goal is an AI-driven software platform that transforms existing IP-based CCTV
infrastructure at Border Out Posts (BOPs), check posts, and border roads into an
intelligent surveillance network — without requiring dedicated FRS, ANPR, or
smart-camera hardware — by performing real-time video analytics using AI and
computer vision.

## 2. Development Workflow

Work proceeds strictly in this order:

```
Research → Product → Design → Architecture → Engineering → Testing → Demo
```

- **Research** (`docs/01-research/`) — domain, users, competitors, technology.
  Establishes facts and constraints before anything is decided.
- **Product** (`docs/02-product/`) — defines what IBVAP will do, scoped to the
  problem statement, informed by research.
- **Design** (`docs/03-design/`) — UX/UI and interaction design for defined
  product features.
- **Architecture** (`docs/04-architecture/`) — system/technical architecture and
  major technical decisions, informed by research and product scope.
- **Engineering** (`docs/05-engineering/`) — implementation.
- **Testing** — verification of implemented features.
- **Demo** (`docs/06-demo/`) — demo materials and scripts.

Do not skip ahead a stage before the stage(s) before it are complete for the
relevant feature or decision.

## 3. Rules

1. The official SIH problem statement in
   [docs/00-project/problem.md](docs/00-project/problem.md) is immutable. Do not
   rewrite, simplify, reinterpret, remove, or add to it.
2. Do not invent requirements. Every product feature must trace back to the
   official problem statement.
3. Do not implement product features before they are defined in
   `docs/02-product/`.
4. Do not make major technical decisions before research (`docs/01-research/`)
   supports them.
5. Keep research, product decisions, design, architecture, and implementation
   separate — each lives in its own `docs/` stage and is not mixed with another.
6. Preserve the existing CCTV access/testing setup (`dvr.py`, `dvr.env`,
   `backups/`, `requirements.txt`). These belong to the developer's home CCTV
   setup used for development and testing. Do not modify, replace, refactor, or
   delete them.
7. In every research/product/design/architecture document, make clear which
   claims are verifiable/sourced fact, which are unverified assumptions, and
   which are hypotheses still to be tested — through plain, naturally hedged
   wording (e.g. "is inferred from...", "not independently verified",
   "plausibly"), not repeated inline labels or a legend. A **DECISION** is
   different: it is a choice actually made, and must be recorded explicitly
   with rationale and date in `docs/00-project/decisions.md` or the relevant
   stage's own decisions log.
8. Any document of more than a few sections opens with a short, positive
   statement of what it is and records — not a paragraph or blockquote of
   what it is not or does not do — followed by a `## Contents` list linking
   to its top-level headings. State a genuine scope boundary once, in plain
   prose, where it matters; don't restate it as a standalone disclaimer.

## 4. Scope

**IBVAP is not India-specific.**

The SIH problem statement and the SSB research define the **initial validation
context** for SIH 2026. They do **not** constrain the eventual product market.

All research, product, design, and architecture work must distinguish:

- **SIH/SSB-specific requirements** — true only for this problem statement or
  this force.
- **Border-security-specific requirements** — true for border/frontier
  surveillance generally, in any country.
- **Globally applicable product capabilities** — true for intelligent video
  analytics on existing CCTV anywhere, security or otherwise.
- **Market-specific considerations** — legal, procurement, connectivity,
  pricing, or regulatory factors that vary by country or market.

Do not assume IBVAP is limited to India or to SSB.
