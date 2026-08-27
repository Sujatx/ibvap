# Vision and Scope

**Source:** derived only from the official problem statement in
[problem.md](problem.md). No content beyond that statement is introduced
here — scoping and prioritization happen later, in `docs/02-product/` (see
[PRD.md](../02-product/PRD.md)), per the workflow in
[CLAUDE.md](../../CLAUDE.md).

IBVAP (Intelligent Border Video Analytics Platform) is the possible project
name given in the official problem statement for Problem Statement ID
26187.

## Contents

1. [Vision statement](#vision-statement)
2. [Why](#why-per-problem-statement)
3. [Required capabilities](#required-capabilities-per-problem-statement)
4. [Required outcomes](#required-outcomes-per-problem-statement)
5. [Constraints](#constraints-per-problem-statement)

---

## Vision statement

Transform existing IP-based CCTV infrastructure at Border Out Posts (BOPs),
check posts, border roads, and other strategic locations into an
intelligent surveillance network — through an AI-driven software platform,
not dedicated FRS/ANPR/smart-camera hardware — so that border security
forces gain real-time, AI-powered situational awareness and faster
response to security incidents and intrusions, without the cost and
deployment difficulty of specialized surveillance hardware in remote
border areas.

## Why (per problem statement)

- Conventional CCTV today provides only video recording and live
  monitoring, requiring continuous human observation.
- Advanced surveillance functions (FRS, ANPR, intrusion detection, object
  tracking) typically require specialized hardware and proprietary
  solutions, making large-scale deployment costly and difficult in remote
  border areas.
- A software-defined platform can extract this functionality from existing
  camera infrastructure instead.

## Required capabilities (per problem statement)

The solution should provide capabilities such as:

1. Human detection and tracking
2. Vehicle detection and classification
3. Face detection
4. Automatic Number Plate Recognition (ANPR)
5. Virtual fence intrusion detection
6. Suspicious activity detection
7. Night-time movement detection
8. Real-time alert generation and event logging

## Required outcomes (per problem statement)

The solution should:

1. Eliminate dependence on expensive dedicated surveillance hardware.
2. Enable intelligent monitoring through AI-powered video analytics.
3. Provide real-time alerts for security incidents and border intrusions.
4. Support facial recognition, vehicle identification, and behavioral
   analytics through software.
5. Improve situational awareness and response time for border security
   forces.
6. Support integration with existing command and control systems.
7. Be cost-effective, scalable, and suitable for deployment across remote
   border locations and strategic installations.

## Constraints (per problem statement)

- Must ingest live video streams from standard IP-based CCTV cameras
  (existing infrastructure).
- Must NOT require dedicated FRS, ANPR, or smart-camera hardware.
- Must use Artificial Intelligence, Machine Learning, Computer Vision, and
  Video Analytics techniques.
