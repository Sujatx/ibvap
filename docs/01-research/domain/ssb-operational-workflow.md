# SSB Operational Workflow — Discovery Pass

**Stage:** 01 — Research → Domain
**Date:** 2026-08-24
**Scope:** A dedicated attempt to establish, from primary and authoritative
sources, **the real SSB organisational hierarchy and the real
surveillance / CCTV / incident workflow** — as opposed to reconstructing one.

> **This document does not design anything.** It does not propose an IBVAP user
> hierarchy, does not recommend a product workflow, and is not a PRD. Per
> [CLAUDE.md](../../../CLAUDE.md) §2, product scoping happens in `docs/02-product/`
> and only after research supports it.

**Companion documents**
- [domain-research.md](domain-research.md) — generic border-CCTV domain, BSF/CIBMS-weighted.
- [ssb-operational-context.md](ssb-operational-context.md) — the earlier SSB layer.
  This document **corrects three findings** in it (see [§0.2](#02-corrections-to-ssb-operational-contextmd)).
- [product-discovery.md](../users/product-discovery.md) — user/job discovery that
  depends on the questions this pass tried to answer.

---

## 0. How to read this document

### 0.1 Labels

Per [CLAUDE.md](../../../CLAUDE.md) §3.7, every substantive statement carries one of:

| Label | Meaning |
|---|---|
| **FACT** | Verifiable and sourced. The source is cited as `[Wn]` (this pass) or `[Nn]`/`[Sn]` (earlier passes). A FACT is a fact *about what the cited source says*. |
| **UNKNOWN** | An identified gap. No source retrieved answers it. |
| **INFERENCE** | A conclusion drawn by this project from the evidence. **An inference never becomes a fact.** Each inference states what it rests on and what would falsify it. |

Where a source is news, trade press, a foreign academic study, or a secondary
compilation rather than an Indian primary government document, this is noted at
the point of use.

**An important distinction used throughout:** *absence of evidence* is recorded
as **UNKNOWN**, never as a FACT of absence. Where this pass searched hard and
found nothing, the search itself is recorded as a FACT (§7 records exactly what
was searched), and the conclusion drawn from that silence is an **INFERENCE**.

### 0.2 Corrections to `ssb-operational-context.md`

Three findings in the earlier SSB pass are corrected by primary sources retrieved here.

| # | Earlier claim | Correction | Source |
|---|---|---|---|
| **C-1** | "**SIMS — Seizure Incident Management System** — SSB's own real-time digital seizure/incident register with a centralised database", recorded as "the only credible candidate found for 'existing command and control systems' on this border" (§8.1, §9, §14.10) | **SIMS is not an SSB system.** It is **"Seizure Information Management System"**, an **e-portal launched by MHA in 2019** for **"digitization of pan-India drug seizure data for all the drug law enforcement agencies under the mandate of the Narcotics Drugs and Psychotropic Substances Act, 1985."** SSB is one of several NDPS-empowered agencies that would feed it, alongside BSF, Indian Coast Guard, RPF and NIA. It is an **NDPS drug-seizure database**, not an SSB register and not a C2 system. | `[W5]` — MHA, Lok Sabha USQ 459, answered 20.07.2021 **(primary, full text)** |
| **C-2** | "SSB's operational achievement table contains **no intrusion or infiltration category at all**" (§14.3), based on MHA AR 2023-24 | In **MHA Annual Report 2024-25**, the SSB achievements table (01.01.2023–31.12.2024) **does** contain **"Illegal Infiltrators (Foreigner)" — 24 cases, 30 arrested**, alongside "Militants/Terrorists — 1 case, 1 arrested". The substantive point survives — 24 infiltration cases against **3,649** prohibited/contraband cases and **1,026** narcotics cases — but the categorical claim does not. | `[W3]` — MHA AR 2024-25 §7.52 **(primary, full text)** |
| **C-3** | "**92,541 personnel** (31.03.2024)"; "the official SSB website … returned no navigable content" (§27) | Posted strength is **94,202 as on 31.12.2024** `[W3]`. The official SSB website **is** reachable and serves a public JSON API; §1 and §6 of this document are built from it. Frontier count (6), Sector count (18) and Battalion count (73) are unchanged in AR 2024-25. | `[W3]`, `[W4]` |

Additionally, **SQ-26** (retrieve the SSB Act and SSB Rules), **SQ-27** (retrieve
the official SSB website) and **SQ-28** (retrieve a later MHA Annual Report) from
`ssb-operational-context.md` §15 are **closed by this pass**.

### 0.3 The status of "the primary user"

The earlier framing — *"the primary user may not exist"* — is withdrawn as too
strong. The accurate status, and the one this document holds to, is:

> **The exact surveillance/CCTV operational workflow has not yet been
> sufficiently validated from our sources.**

What this pass establishes is that the **organisational hierarchy is now well
evidenced at the statutory level** (§1), the **surveillance responsibilities are
now evidenced at the statutory level** (§2), and the **CCTV/control-room and
incident workflows remain unevidenced** (§3, §4) after a deliberate, documented
search (§7).

---

## 1. A. Verified organisational hierarchy

### 1.1 What is statutory

Two documents govern. Both were retrieved in full in this pass.

**FACT** — The **Sashastra Seema Bal Act, 2007 (Act No. 53 of 2007)**, assented
20.12.2007, is *"An Act to provide for the constitution and regulation of an
armed force of the Union for ensuring the security of the borders of India and
for matters connected therewith."* `[W1]`

**FACT** — The **Sashastra Seema Bal Rules, 2009** were made under section 155 of
the Act. `[W2]`

**FACT** — SSB Act §4(1): *"There shall be an armed force of the Union called the
Sashastra Seema Bal for ensuring the security of the borders of India and
performing such other duties as may be entrusted to it by the Central
Government."* `[W1]`

**FACT** — SSB Act §5(1): *"The general superintendence, direction and control of
the Force shall vest in, and be exercised by, the **Central Government** and
subject thereto … the **command and supervision** of the Force shall vest in an
officer to be appointed by the Central Government as the **Director-General**."*
§5(2): the DG is assisted by *"such number of Additional Directors-General,
Inspectors-General, Deputy Inspectors-General, **Additional Deputy
Inspectors-General**, Commandants and other officers, as may be appointed."* `[W1]`

#### Statutory rank structure — SSB Rules, 2009, Rule 8(1)

**FACT** — The complete statutory rank classification: `[W2]`

| Category | Ranks, in order |
|---|---|
| **(a) Officers** | Director-General · Additional Director-General · Inspector-General · Deputy Inspector-General · Commandant · Second-in-Command · Deputy Commandant · Assistant Commandant |
| **(b) Subordinate Officers** | Subedar Major · Inspector · Sub-Inspector · Assistant Sub-Inspector |
| **(c) Under Officers** | Head Constable · Naik · Lance Naik |
| **(d) Enrolled persons other than Under Officers** | Constable · Enrolled followers |

**FACT** — "**Additional Deputy Inspector-General**" is defined in the Act
(§2(g)) and named in §5(2), but **does not appear in the Rule 8(1) rank list**.
`[W1][W2]`

**FACT** — Rule 8(3)–(4): the DG may grant an officer or Inspector a **local
rank**, whose holder *"shall exercise the command and be vested with the powers
of an officer holding that rank"* but is not entitled to extra pay or seniority.
`[W2]`

#### Statutory command responsibility — SSB Rules, 2009, Rule 9(2) and Rule 10

**FACT** — Rule 9(2) assigns *"the responsibility for the command, discipline,
administration, morale and training"* as follows: `[W2]`

| Rank | Responsibility extends to |
|---|---|
| **Additional Director-General** | all battalions, units, headquarters, establishments and Force personnel **placed under him and within the area that may be assigned to him** |
| **Inspector-General** | all battalions, units, headquarters, establishments and Force personnel placed under him and within the area assigned |
| **Deputy Inspector-General** | battalions, units and other personnel placed under him and within the area assigned |
| **Commandant** | **the battalion or unit** placed under him and within the area assigned |

**FACT** — Rule 9(4): command of battalions, units and establishments **not**
placed under a DIG or an IG *"shall be carried out by such officers and in such
manner as may be laid down by the Director-General from time to time."* `[W2]`

**FACT** — Rule 10(1): *"An officer appointed to command shall have the power of
command over all officers and men, **irrespective of seniority**, placed under
his command."* Rule 10, Explanation: except in sub-rule (2), *"the word 'officer'
shall include a subordinate officer and an under officer."* `[W2]`

**FACT** — Rule 10(2): if the appointed officer cannot exercise command it
devolves to the Second-in-Command; failing that to an officer appointed to
officiate by the immediate superior; failing that to the senior-most officer
present — and the assumption of command *"shall be **immediately reported to the
next higher authority** by the officer who has assumed command."* `[W2]`

#### Statutory definitions that matter for hierarchy

**FACT** — SSB Act §2: `[W1]`
- **§2(b)** *"'battalion' means a unit of the Force **constituted as a battalion by the Central Government**"*
- **§2(e)** *"'commanding officer' means a Commandant **or any officer for the time being in command of the unit or any separate portion of the Force** to which such person belongs or is attached"*
- **§2(y)** *"'unit' includes (i) any body of officers and other members of the Force for which a **separate authorised establishment** exists; (ii) any separate body of persons subject to this Act employed on any service and not attached to a unit as aforesaid; (iii) any other separate body of persons … **specified as a unit by the Central Government**"*
- **§2(w)** *"'superior officer' … means any member of the Force **to whose command such person is for the time being subject in accordance with the rules**"*

### 1.2 Sub-battalion echelons: what the statute actually says

This is the single most important hierarchy finding of this pass, because
`ssb-operational-context.md` §3.2 rested on a Nepali master's thesis for it.

**FACT** — SSB Act **§56(3)**: *"a **Deputy Commandant or an Assistant
Commandant, commanding a company or a detachment or an outpost**, shall have the
power to proceed against a person subject to this Act, other than an officer or a
subordinate officer, who is charged with an offence under this Act …"* `[W1]`

**FACT** — SSB Act **§56(4)**: *"A **subordinate officer not below the rank of
Sub-Inspector who is commanding a detachment or an outpost** shall have the
powers to proceed against a person subject to this Act, other than a subordinate
officer or an under-officer …"* `[W1]`

**FACT** — SSB Act §56(2): if a unit, training centre or establishment is
temporarily commanded by a **Second-in-Command or Deputy Commandant**, that
officer has full commanding-officer powers. `[W1]`

**INFERENCE** — **Statutorily, an outpost may be commanded either by a Deputy
Commandant / Assistant Commandant, or by a subordinate officer of Sub-Inspector
rank or above** (i.e. SI, Inspector or Subedar Major). The thesis-sourced claim
that a BOP is commanded by a Sub-Inspector `[N8]` is therefore **consistent with
the statute but not fixed by it** — the statute sets a floor (not below SI), not
a norm. *Rests on: §56(3)–(4) `[W1]`. Falsified by: any SSB establishment table,
Standing Order or MHA statement fixing the sanctioned rank of a BOP in-charge.*

**UNKNOWN** — The **normal** (as opposed to permitted) rank of a BOP in-charge,
of a check-post in-charge, and of a platoon commander; and whether it varies by
frontier, terrain or BOP category.

### 1.3 What is *not* statutory

**FACT** — The words **"Frontier", "Sector", "Company", "Platoon" and "Border Out
Post"** do **not** appear as constituted formations anywhere in the SSB Act, 2007
or the SSB Rules, 2009. The only formations the statute constitutes are the
**"battalion"** (§2(b)) and the **"unit"** (§2(y)). `[W1][W2]`

**FACT** — The operational vocabulary the statute *does* use, in the offences
chapter and in the definition of "active duty", is: **picket, patrol, guard,
sentry, post, party, detachment, outpost, company, camp, quarters, Force lines**.
Examples: §2(a)(ii) active duty includes a unit *"operating at a **picket** or
engaged on **patrol** or other **guard duty** along the borders of India"*; §22(g)
*"in time of action leaves his commanding officer or other superior officer or his
**post, guard, picket, patrol or party** without being regularly relieved"*; §30(a)
*"when in command of a **guard, picket, patrol, detachment or post** …"* `[W1]`

**INFERENCE** — **Frontier, Sector, Company, Platoon and BOP are administrative
and deployment constructs created under the DG's Rule 9(4) authority, not
statutory echelons.** They can therefore be reorganised without amending the Act
or Rules, and their definition lives in internal SSB orders that are not public.
*Rests on: the absence of these terms from `[W1][W2]` combined with Rule 9(4)'s
open grant to the DG. Falsified by: a Central Government notification constituting
Frontiers or Sectors, or an SSB Standing Order in the public domain.*

### 1.4 The administrative structure, from SSB's own publications

**FACT** — MHA Annual Report 2024-25 §7.51: SSB is deployed on the **Indo-Nepal
border (1,751 km)** and the **Indo-Bhutan border (699 km)**, with a **posted
strength of 94,202** (as on 31.12.2024). The Force comprises: `[W3]`

| Formation | Count |
|---|---|
| Force Headquarters | 1 |
| **Frontiers** | **6** |
| **Sectors** | **18** |
| **Battalions** | **73** |
| Recruit Training Centres | 4 |
| Central Training Centres | 2 |
| SSB Academy | 1 |
| **Wireless & Telecom Training Centre** | 1 |
| Dog Training & Breeding Centre | 1 |
| Composite Hospitals | 3 |
| Central Store Depot & Workshop | 1 |
| Sub-CSDs | 3 |
| Medical Training Centre | 1 |
| Counter Insurgency & Jungle Warfare School | 1 |
| "G" School | 1 |

Unchanged from AR 2023-24 `[N1]` in every formation count.

**FACT** — **The six Frontiers, named**, from SSB's own website API: `[W4]`

| # | Frontier HQ |
|---|---|
| 1 | **Ranikhet** |
| 2 | **Lucknow** |
| 3 | **Patna** |
| 4 | **Siliguri** |
| 5 | **Guwahati** |
| 6 | **Tezpur** |

*(This is new. `ssb-operational-context.md` recorded the count but not the names.
Note that widely circulated tertiary sources still assert "three frontier
headquarters — Lucknow, Patna, Guwahati", which is out of date.)*

**FACT** — Force Headquarters address: **Directorate General SSB, SSB Hqrs, East
Block-V, R.K. Puram, New Delhi – 110066**. `[W6]` A **Directorate-General** and an
**IG (Admn)** are named in SSB-signed MoUs on the SSB site. `[W6]`

**FACT** — An **IG (Operations), SSB** post exists at FHQ: a BPRD/MHA project
report records that *"**IG (Ops), SSB** has furnished the details of cases booked
with respective different types of trans border crimes on Indo-Nepal Border."*
The same report's proposed structure refers to *"Addl. DsG, In-charge of
operations of BSF and SSB."* `[W7]`

**FACT** — Frontier commanders hold the rank of **Inspector-General**: SSB's own
circulars name *"Shri Nishit Kumar Ujjwal (IPS), **Inspector General, Sashastra
Seema Bal, Frontier Patna**."* `[W4]`

**FACT** — Sector commanders hold the rank of **Deputy Inspector-General**: PTI
quotes *"**Deputy Inspector General, Sashastra Seema Bal, Gorakhpur**, Akhileshvar
Singh."* `[W8]` *(news; corroborates Rule 9(2)(c)'s DIG-over-battalions
responsibility)*

**FACT** — **Frontier → Sector HQ → Battalion → BOP** is visible as a real
addressing scheme in SSB's own tender and circular feed. Verbatim examples: `[W4]`

- *"Consultancy Services for Permanent Office Building & Barrack at **BOP Jiti, SHQ Jalpaiguri**"*
- *"Construction of chain link fencing … at **BOP Bongling of 38 Bn SSB Tawang under FTR Hqrs SSB [Tezpur]**"*
- *"Construction of chain link fencing … at **BOP Tsamstesekhang of 67 Bn SSB Lungla under FTR HQ [Tezpur]**"*
- *"infrastructure … at **BOP Kothiyaghat of the 70th Battalion, SSB, Lakhimpur Kheri**"*
- *"Construction of permanent building at **BOP Kataiya of 45 Battalion Birpur**"*
- *"Repairing and Up-gradation of 06 Nos Off-grid Solar Power Plant at BOPs under **57th Bn SSB, Sitarganj**", tender authority "**Executive Engineer, SHQ, SSB, Pilibhit**"* `[W9]`

**FACT** — Battalions and their stations observable in SSB's own feed for
Oct 2025 – Aug 2026 include: 3 & 70 (Lakhimpur Kheri), 6 (Ranighuli, under SHQ
Bongaigaon, FTR Guwahati), 18 (Rajnagar), 23 (Lalpool), 25 (Ghitorni, Delhi),
27 (Howly), 30 (Derang), 31 (Gossaigaon), 37 (Mangaldoi), 38 (Tawang), 45
(Birpur), 52 (Araria), 56 (Bathnaha), 57 (Sitarganj), 67 (Lungla), plus 9, 10,
11, 12, 13, 14, 17, 20, 34, 36, 39, 42, 43, 46, 53, 55, 59, 62, 68, 69 and 73.
`[W4][W9]`

**FACT** — **Platoons exist as a deployment unit with a "Commander."** A Delhi
District Court order records *"Commander, Sh. S. Murup of the **SSB Platoon**
which guards the R&AW training institute campus, Gurgaon."* `[W10]` *(court
record; incidental to the case, and the deployment is an internal-security guard
task, not a border task)*

**UNKNOWN** — The authoritative Frontier → Sector → Battalion order of battle;
which Frontier holds which Sectors; which Sectors hold which battalions; and
which battalions sit on the Nepal border versus the Bhutan border versus internal
security deployments in J&K, Assam, Chhattisgarh, Jharkhand and Bihar `[W3]`.

**UNKNOWN** — Whether the widely quoted "7 companies per battalion, 3 BOPs per
company" `[N6]` is a sanctioned establishment or a tertiary-source
generalisation. Nothing in `[W1][W2][W3][W4]` states it.

### 1.5 Cadres — who is technically qualified, structurally

**FACT** — SSB's own recruitment-rules index enumerates its cadres: `[W4]`

**GD** (General Duty) · **Communication** · **Veterinary** · **Tech (Armament)** ·
**Ministerial** · **MT** (Motor Transport) · **Engineering** · **Tradesman** ·
**Judge Attorney (JAG)** · **Hindi Translator** · **Medical** · **Mountaineering** ·
**Ordnance** · **CIOA**

**FACT** — The **Communication cadre** is combatised and runs from Group 'A' down
to Constable: *"RRs of Communication Gp. 'A'-2013"*, *"Gazette Notification of
SSB Combatised Communication Cadre **Inspector Communication and Sub Inspector
Communication** Group B Posts Recruitment Rules 2024"*, *"G.S.R. 32 Recruitment
Rules 2024 … **ASI/Commn. and HC/Commn.** Group C posts"*, *"RRs of Inspector
(Tele)"*. `[W4]` It is supported by a standing **Wireless & Telecom Training
Centre** `[W3]`.

**FACT** — **No IT, computer, cyber, data, video, surveillance or electronics
cadre appears in the list.** The nearest cadres are Communication (wireless /
telecom) and Tech (Armament). `[W4]`

**INFERENCE** — **If any SSB cadre is structurally responsible for installing,
operating and maintaining IP video infrastructure at a post, it is the
Communication cadre**, whose training establishment is a wireless-and-telecom
school rather than an IT school. *Rests on: the cadre inventory `[W4]` and the
formation list `[W3]`. Falsified by: evidence of an IT/EDP cell, a contracted O&M
vendor, or the Engineering cadre owning this. Note that BSF, by contrast, has a
visible `edpdte@bsf.nic.in` (EDP Directorate) address `[W11]`; no SSB equivalent
was found.*

**FACT** — SSB has sent personnel for **Drone Pilot Training** at a
DGCA-approved institute and for **Special Communication Equipment Training at
BSF** `[N3]` — i.e. SSB has, at least once, gone to BSF for communications
training.

---

## 2. B. Verified surveillance responsibilities

### 2.1 The statutory charter — SSB Rules, 2009, Rule 9(1)

This supersedes the thesis-derived charter used in
`ssb-operational-context.md` §1.2.

**FACT** — Rule 9(1), verbatim: *"For the purpose of sub-section (1) of section
4, the Force shall **in area of its responsibility** — (i) **safeguard the
security of assigned borders of India and promote sense of security among the
people living in border area**; (ii) **prevent trans-border crimes, smuggling and
any other illegal activity**; (iii) **prevent unauthorised entry into or exit from
the territory of India**; (iv) to **carry out civic action programme** in the area
of responsibility; (v) to perform **any other duty assigned by the Central
Government**."* `[W2]`

**FACT** — Rule 9(5): every member of the Force is liable to perform any duties
connected with the task in Rule 9(1), and *"any order given in this behalf by a
superior officer shall be a **lawful command** for the purpose of the Act."* `[W2]`

**Two features of this charter bear directly on any surveillance product and are
recorded here as findings, not as design input:**

1. **FACT** — Rule 9(1)(i) pairs border security with *"promote sense of security
   among the people living in border area"*, and Rule 9(1)(iv) makes **civic
   action** a statutory task. The border population is, by statute, a
   constituency to be reassured — not only a population to be watched. `[W2]`
2. **FACT** — Rule 9(1) contains **no mention of observation, surveillance,
   monitoring, sensors, cameras, or recording**. The statutory verbs are
   *safeguard, promote, prevent, carry out, perform*. `[W2]`

### 2.2 Who performs which function — what is evidenced

| Function | Who performs it | Evidence | Label |
|---|---|---|---|
| **Border surveillance** | Not statutorily assigned to any named role. In practice, described across sources as post-based and patrol-based: BOPs, observation posts, check posts, joint check posts, naka | `[W1][W2]` for the statutory silence; `[N8][N23]` for practice | **FACT** (statutory silence); practice is **secondary-sourced** |
| **Patrolling** | Statutorily recognised: "active duty" includes a unit *"operating at a picket or engaged on patrol or other guard duty along the borders of India"* `[W1]` §2(a)(ii). Area domination patrols and joint patrols with APF Nepal (5,841 in FY 080/81) `[N8]` | `[W1]` primary for the concept; `[N8]` for volumes | **FACT** |
| **Checking / frisking** | Manned naka and check posts; **female personnel deployed at border check posts** for checks of female travellers `[N8]`; metal detectors installed at **Sonauli and Thuthibari outposts** `[W8]` | `[N8]`; `[W8]` news quoting DIG SSB Gorakhpur | **FACT** |
| **Intelligence gathering** | SSB is **Lead Intelligence Agency** for the Indo-Nepal and Indo-Bhutan borders; intelligence wing of ~650 field and staff agents `[N19]`; **25 Border Interaction Teams** in civilian attire on high-risk routes `[N8]`; "Know Your Area" programme `[N8]` | `[N8][N19]` | **FACT** (existence); volumes are secondary |
| **Incident reporting** | **No SSB reporting instrument for a border incident was located.** What *is* statutory is internal: Rule 10(2)(d) requires assumption of command to be *"immediately reported to the next higher authority"*; Rule 176 requires a **Court of Inquiry** for unnatural deaths, disabling injuries, financial losses, **loss of secret documents**, and injuries/damage to private persons — with, for unnatural deaths, *"an immediate report … sent **through the messenger** to the officer-in-charge of the police station"* `[W2]` | `[W2]` primary | **FACT** for the internal instruments; **UNKNOWN** for border incidents |
| **Incident assessment** | **UNKNOWN.** No source describes who assesses a border event, against what criteria, or in what time | — | **UNKNOWN** |
| **Escalation** | Statutorily, command runs outpost/detachment → company → **Commandant (battalion)** → DIG → IG → ADG → DG → Central Government (Rule 9(2), §5) `[W1][W2]`. Whether an *operational* alert escalates on this same chain is not stated anywhere | `[W1][W2]` for the command chain | **FACT** (command chain); **UNKNOWN** (alert chain) |
| **Response coordination** | Cases are **handed over to the local police**: *"The Border Guarding Forces, i.e., BSF, ITBP, SSB and Assam Rifles, after carrying out apprehension of trans border criminals and / or seizure of contrabands like FICN, drugs, etc. **hand them over to the local police for investigation and further disposal, as per existing laws and procedures**"* `[W7]` | `[W7]` BPRD/MHA project report | **FACT** |
| **Cross-border coordination** | Scheduled, not event-driven: DG/IG annual→semi-annual, DIG quarterly, Battalion monthly, **Company/BOP fortnightly** `[N8]`. Reaffirmed at national level: the **14th India-Nepal Joint Working Group on Border Management**, Dehradun, 20–21 August 2026 `[W12]` | `[N8]`; `[W12]` | **FACT** |
| **Narcotics interdiction** | SSB is **empowered under the NDPS Act, 1985** alongside BSF, Indian Coast Guard, RPF and NIA *"for making interdiction of"* drug trafficking | `[W5]` **primary** | **FACT** |

### 2.3 A documented capability gap in SSB's own reporting

**FACT** — BPRD's project report records, of an attempt to obtain case-outcome
data from the border guarding forces: *"It is seen that **only BSF has developed
a system of monitoring, supervising and following up with the local Police** with
regard to criminal cases registered on their complaints. … **IG (Ops), SSB has
furnished the details of cases booked** with respective different types of trans
border crimes on Indo-Nepal Border and also given figures of criminal arrested
and seizure made. **However, SSB could not provide data with respect to the
present status of the cases** … **SSB is now in the process of developing systems
and procedures for monitoring progress of investigation and trial** in cases
booked by local Police on their operations."* `[W7]` *(BPRD project report,
approved 09.02.2021; the data request is dated to the 2018 period)*

**INFERENCE** — As of the 2018–2021 period, **SSB could report cases, arrests and
seizure quantities, but could not report what happened to a case after handover**,
and was building that capability. This is consistent with, and is the first
primary-adjacent evidence for, the earlier characterisation of SSB's reporting as
an **outcome ledger rather than an event log**. *Rests on: `[W7]`. Falsified by:
evidence of a completed SSB case-tracking system, or a later BPRD/MHA statement.*

**UNKNOWN** — Whether the case-monitoring system BPRD says SSB was developing
was built, what it is called, and whether it is the same thing as anything named
in §5.

---

## 3. C. Verified CCTV / control-room workflow

**This section is short because almost nothing is verified. That is the finding.**

### 3.1 What is established about SSB and cameras

**FACT** — MHA, Lok Sabha USQ 488, answered 03.02.2026: SSB *"has procured the
Unmanned Aerial Vehicles, Micro Unmanned Aerial Vehicles, Hand Held Thermal
Imager, **CCTV Surveillance Setup with Automatic Face Recognition System with
Auto Number Plate Recognition** and Satellite phones for surveillance and
modernization of the Force."* `[N3]` — **primary; procurement only. It states
neither where the setup is deployed, nor how many, nor who operates it.**

**FACT** — MoS Home Shri Bandi Sanjay Kumar, on SSB: *"Modern technologies such
as **drones, CCTV systems, thermal imagers, night-vision equipment, GPS-based
patrolling, secure digital communication systems and GIS-based planning** are
being utilized to enhance operational effectiveness."* `[W13]` *(news reporting a
ministerial statement; a capability list, not a workflow)*

**FACT** — India and Nepal, at the **14th Joint Working Group on Border
Management** (Dehradun, 20–21 August 2026; Indian delegation led by Ms. Pausumi
Basu, Joint Secretary (BM-I), MHA; Nepali delegation led by Mr. Ananda Kafle,
Joint Secretary, MoHA Nepal), *"agreed to enhance security surveillance at
sensitive locations in the border areas through the use of modern and latest
technologies, **including CCTV cameras and other advanced equipment**"*, and to
*"strengthen coordination and **real-time information sharing**."* `[W12]`
*(news; multiple outlets, consistent wording, three days before this document's
date)*

**FACT** — MHA Annual Report 2024-25 §3.20 defines **CIBMS** as *"the integration
of manpower, sensors, networks, intelligence and **command control solutions** to
improve situational awareness **at different levels of hierarchy** to facilitate
prompt and quick response to emerging situations"* — and places it explicitly on
the **India-Pakistan and India-Bangladesh borders only** (§3.20), with pilots of
2 × 5 km in Jammu and 61 km at Dhubri (§3.21) and hybrid-surveillance pilots on
the India-Myanmar border (§3.23). `[W3]`

**FACT** — In the same Annual Report, the **India-Nepal Border** paragraphs
(§3.26–3.27) and the **India-Bhutan Border** paragraph (§3.28) contain **only**
the border length, the *"main challenges … to check **misuse of the open border**
by terrorists and criminals"*, approved road construction, and the BOP counts
(**539** Nepal, **195** Bhutan). **No technology, no sensors, no surveillance
programme, no command-and-control item appears for either border.** `[W3]`

**FACT** — MHA lists ICP infrastructural facilities including **CCTV**; ICPs are
operated by the **Land Ports Authority of India**, not by the border guarding
force. Raxaul (03.06.2016) and Jogbani (15.11.2016) are the operationalised
India-Nepal ICPs. `[W3]`

### 3.2 What is not established

**UNKNOWN — the central gap** — **Whether SSB monitors live video anywhere, at
any echelon.** No control room, operations room, video wall, monitoring roster,
shift pattern, operator establishment, or cameras-per-operator figure for SSB was
found in any source in this pass or the previous one.

**UNKNOWN** — Where the procured FRS/ANPR CCTV setup `[N3]` is installed, how
many sites, whose product it is, whether it is one stack or many, and whether it
exposes streams or APIs.

**UNKNOWN** — Whether ordinary BOPs have cameras at all, or whether cameras exist
only at check posts, ICPs and "key crossing points".

**UNKNOWN** — Who owns and monitors the CCTV at ICP Raxaul and ICP Jogbani —
LPAI, Customs, Immigration, or SSB — and whether SSB has access to those feeds.

**UNKNOWN** — Retention period, storage location, and export procedure for any
SSB video.

**UNKNOWN** — Where drone/UAV video goes, who watches it, and whether it is
recorded or retained.

### 3.3 The proposal that implies the absence

**FACT** — BPRD / National Police Mission (Micro Mission 06), project report
*"Integrated Border Management and National Security"* (Project No. 05/MM:06,
approved 09.02.2021, project leader Shri Santosh Mehra, IPS, ADG BPRD),
**proposes** creating **Integrated Law Enforcement Centres (ILECs)** *"stationed
at existing and proposed Integrated Check Posts (ICPs)"*, co-locating Customs,
NCB, NIA, DRI, ED, local police and anti-trafficking cells, IB, Special Bureau
(R&AW) and the Wildlife/Biodiversity Wing alongside *"personnel from border
guarding forces of the area"*. `[W7]`

**FACT** — That proposal includes a **"Situation Room"**: *"The Integrated Law
Enforcement Centres will establish a Situation Room, where on the basis of
collected, collated and analysed information from various sources, **near
real-time situation of the borders will be built-up**; and on the basis of
continuous inflows of information, such situation will be updated. On the basis of
time-series data, **the trends of border-crimes in a particular sector of border
will be analyzed and utilized for planning routine operations by Border Guarding
Forces**."* `[W7]`

**FACT** — In the same report's proposed ILEC equipment schedule, **CCTV appears
once, as *"CCTV with monitor — For **Camp security** — 6 — Pooled"***, alongside a
*"Digital Camera with still & video — For operations and investigation"*. `[W7]`

**INFERENCE** — In a 2021 government report written specifically to design
integrated border management, **a border "Situation Room" is described in the
future tense as something to be established**, and **CCTV is budgeted as camp
security rather than as a border-surveillance instrument**. This is
circumstantial but consistent evidence that, at least on the borders and ICPs
this report addressed, **no equivalent facility existed to be described in the
present tense**. *Rests on: `[W7]`. Falsified by: any government document
describing an existing border situation room, control room or joint monitoring
centre on the SSB borders.*

---

## 4. D. Verified incident / alert workflow

### 4.1 What is verified — and it is all internal or judicial, not operational

**FACT** — **Handover is the terminal step.** Border guarding forces *"after
carrying out apprehension of trans border criminals and / or seizure of
contrabands … hand them over to **the local police** for investigation and further
disposal, as per existing laws and procedures."* The same source records that
*"these cases find sub-optimum level of priority and seriousness in investigation
and disposal. Almost all such cases are investigated by state police, who have
**neither the resources nor adequate professional expertise** to handle them
properly."* `[W7]`

**FACT** — **A statutory reporting duty exists for unnatural deaths**, and its
default transport is a person: Rule 176(2)(a)(i) requires *"an immediate report
… sent **through the messenger** to the officer-in-charge of the police station
within whose jurisdiction the place of such unnatural death exists"*; and
176(2)(a)(ii), *"In cases when such report cannot, for any reasons be delivered
within a reasonable time, the Commanding Officer or the senior most officer of
the unit present shall prepare a report in the Form set out in **Appendix XIII**."*
`[W2]`

**FACT** — A **Court of Inquiry** is mandatory for: all unnatural deaths within
Force lines; all disabling injuries; all financial irregularities, losses, theft
and misappropriation of Force property; **all losses of secret documents or
material of secret-or-above classification** (to be ordered by an authority
superior to the Commanding Officer holding the material); and all injuries to
private persons or damage to their property likely to give rise to a claim
against the Government. `[W2]` Rule 176(1): a Court of Inquiry may be held *"to
inquire into any disciplinary matter or **any other matter of importance**."* `[W2]`

**FACT** — **"Alarm" is a statutory concept, and it is a human act.** SSB Act
§22(f) and §23(e) make it an offence to *"intentionally or through neglect
occasion a **false alarm** in camp or quarters, or spread or cause to be spread
reports calculated to create unnecessary alarm or despondency."* `[W1]`

**FACT** — Command-change events must be reported upward *"immediately … to the
next higher authority"* (Rule 10(2)(d)). `[W2]`

**FACT** — **Evidence law that applies unchanged:** Section 63 of the Bharatiya
Sakshya Adhiniyam, 2023 governs electronic records, requiring a certificate with
a hash value signed by the device custodian and an expert `[S29]` — carried
forward from [domain-research.md](domain-research.md) §3.5 and confirmed in
[ssb-operational-context.md](ssb-operational-context.md) §11.5 as force-agnostic.
SSB's own site publishes the new criminal laws under
`assets/document/Laws/{BNS,BNSS,BSA}` `[W4]`, indicating force-wide dissemination
of the 2023 codes.

### 4.2 What is not verified

**UNKNOWN — blocking** — The **detection → assessment → escalation → response**
sequence for a border event at an SSB BOP or check post. Nothing retrieved
describes it. The BSF/BOLD-QIT chain (sensor → Control Room → QRT →
interception) recorded in [domain-research.md](domain-research.md) §2.1–§3.2 is
**explicitly forbidden to be carried across**
([ssb-operational-context.md](ssb-operational-context.md) §16 item 7), and this
pass found nothing to replace it with.

**UNKNOWN** — Whether SSB has a **Quick Reaction Team** construct at all, or
whether response is by the patrol/naka already in the field.

**UNKNOWN** — **What carries an operational alert** from the person who notices
to the person who responds: radio net, mobile phone, landline, runner. The only
transport the statute names for any report is *"through the messenger"* `[W2]`,
and that is for the police, for a death.

**UNKNOWN** — Whether any written **SOP or Standing Order** governs border-event
assessment and escalation, and whether any part of it is public. *(SSB's public
site uses the phrase "SOP" only for recruitment and for dependent I-cards
`[W3][W4]`.)*

**UNKNOWN** — Response-time expectations from detection to interception; whether
any such target exists.

**UNKNOWN** — Whether any event that produces **no seizure and no arrest** is
recorded anywhere at all.

**INFERENCE** — **SSB's evidenced reporting instruments are outcome-shaped and
discipline-shaped, not detection-shaped.** Everything verified above records
either a *result* (a case, an arrest, a seizure quantity, a handover) or an
*internal irregularity* (a death, a loss, a change of command). No verified
instrument records a *detection*. *Rests on: `[W1][W2][W3][W7]`. Falsified by:
any SSB reporting instrument that counts detections, alarms, sightings or
crossings.*

---

## 5. E. Existing systems relevant to IBVAP

| System | What it actually is | Owner | Source | Confidence |
|---|---|---|---|---|
| **SIMS — Seizure Information Management System** | **An MHA e-portal launched in 2019 for digitization of pan-India drug seizure data for all drug law enforcement agencies under the NDPS Act, 1985.** A national NDPS seizure/offender database. **Not an SSB system, not a C2 system, and not an incident register.** SSB, being NDPS-empowered `[W5]`, is one contributing agency among many | MHA / NCB | `[W5]` **primary** | **High** — and it removes SIMS from the C2 candidate list (see [C-1](#02-corrections-to-ssb-operational-contextmd)) |
| **CCTV Surveillance Setup with Automatic Face Recognition System with Auto Number Plate Recognition** | Procured by SSB. Nothing further stated: no vendor, no site count, no deployment, no interface | SSB | `[N3]` **primary** | **High** for procurement; **deployment UNKNOWN** |
| **Case-monitoring systems for post-handover police cases** | SSB *"is now in the process of developing systems and procedures for monitoring progress of investigation and trial in cases booked by local Police on their operations"* (as of the 2018–2021 window) | SSB | `[W7]` government report | **Medium** — a statement of intent; outcome unknown |
| **Rotational E-Transfer System** | An SSB personnel **transfer/posting** automation system built by a private vendor. PHP / Apache / Linux / MySQL. **Administrative, not operational** | SSB | `[W14]` vendor case study | **Medium** for existence; irrelevant to surveillance, recorded so it is not mistaken for a C2 system |
| **CLMS** (`clms.ssb.gov.in`) and **SSB Recruitment portal** (`recruitment.ssb.gov.in`, `ssbrectt.gov.in`) | Separate SSB web systems linked from the SSB site. Purpose not stated on the public site; naming suggests learning/course management and recruitment | SSB | `[W4]` | **Medium** for existence; **purpose UNKNOWN**; both appear administrative |
| **NIDMS — National IED Data Management System** | NSG, with Rashtriya Raksha University, to *"synergize & integrate IED related incidents … to collect all the IED incidents' data **in real time** from State Police & CAPFs"*, with *"'Artificial Intelligence & Machine Learning' … being incorporated as a part of futuristic application."* Total cost ₹10.11 crore | NSG / MHA | `[W3]` **primary** | **High.** Recorded because it is **the only MHA system found that ingests real-time incident data from CAPFs and names AI/ML** — but its scope is **IED incidents only**, and SSB's involvement would be only as one of the CAPFs that feed it |
| **"Integrated Command and Control Centre"** with *"upgraded Surveillance grid using AI based features, RADARS, Electro Optics Devices, Night Vision Devices, Motion Detectors"* | Named by MHA in a **national narcotics** answer covering international borders and coastal areas generally. **Not attributed to SSB or to the Indo-Nepal/Indo-Bhutan borders** | MHA (unattributed) | `[N4]` **primary** | **High** for the statement; **unattributable to SSB** |
| **CIBMS** | *"Integration of manpower, sensors, networks, intelligence and command control solutions"* — **India-Pakistan and India-Bangladesh borders only**; pilots 2 × 5 km Jammu, 61 km Dhubri | MHA / BSF | `[W3]` **primary** | **High — and explicitly not on SSB's borders** |
| **ILEC "Situation Room"** | **A 2021 BPRD proposal**, not a system in service. Would sit inside ICPs and build a *"near real-time situation of the borders"* from multi-agency data | Proposed: MHA | `[W7]` government report | **High** that it was proposed; **no evidence it exists** |
| **PMU — Project Monitoring Unit, Department of Border Management, MHA** | A real MHA unit at East Block-I, R.K. Puram, staffed via CPWD Border Fencing Zone. Its subject matter is **border infrastructure** (fencing, roads, buildings), not surveillance systems | MHA (Dept of Border Management) | `[W15]` **primary** (CPWD notification, 24.10.2025) | **High** for existence; **not a surveillance system** |
| **Modernisation Plan-IV** | CCS-approved Central Sector Scheme, total outlay **₹1,523 crore** to 31.03.2026; **SSB's share ₹122.21 crore**. AR 2024-25's list of major equipment for the plan is *"Multi Grenade Launcher, Under Barrel Grenade Launcher, Assault Rifle, Bomb Detection and Disposal Equipment, Mine Protected Vehicle …"* — **no video analytics, VMS, CCTV or command-and-control item** | MHA | `[W3]` **primary** | **High** |
| **CAPF modernisation, latest reported** | A Rajya Sabha reply of 04.08.2026 is reported to cover *"thermal imagers, passive night vision goggles, UAVs and drones, secure communication systems, **Hyper-Converged Infrastructure servers, networking equipment and digital command-and-control platforms**"* | MHA | `[W16]` news reporting a parliamentary reply | **Medium** — the primary PDF was not located in this pass; **this is the closest thing found to an MHA statement about CAPF command-and-control platforms and it must be verified** |

**UNKNOWN — blocking, and unchanged from the previous pass** — **What "existing
command and control systems" means for SSB.** The problem statement requires
integration with them. After this pass, **SIMS has been eliminated** as a
candidate (it is a national NDPS seizure database), and **nothing has replaced
it**. No source names an SSB C2 system, its vendor, protocol, data model, or
network reach.

---

## 6. Procurement evidence — what SSB is actually buying

This section exists because the brief asked specifically for CCTV, FRS, ANPR,
VMS, video-analytics, control-room and command-centre tenders associated with SSB.

**FACT** — SSB publishes a tender feed on its own website. This pass retrieved
the **complete feed as served: 280 tenders, dated 07.10.2025 to 11.08.2026**,
across FHQ and all six Frontiers (Guwahati 61, Tezpur 53, FHQ 44, Patna 44,
Siliguri 40, Lucknow 24, Ranikhet 14). `[W4]`

**FACT** — **Not one of those 280 tenders is for CCTV, cameras, NVR/DVR, video
management software, video analytics, face recognition, number-plate recognition,
a control room, or a command centre.** The full set of matches for the search
terms *cctv, camera, surveillance, video, analytic, control room, command, ANPR,
number plate, face, VMS, NVR, DVR, monitor, network, server* is: `[W4]`

| Date | Formation | Tender |
|---|---|---|
| 08.12.2025 | FHQ | *"Repair and renovation of **Communication Server Room** at FHQ, SSB, East Block-V, R.K. Puram, New Delhi"* |
| 31.10.2025 | FHQ | *"Victim Location Unit (With Breaching System) (18 Nos.)"* |
| 05.01.2026 | FHQ | Lift repair and AMC, SSB Campus Mahipalpur |
| 03.02.2026 | FHQ | Officers' mess toilet renovation, 25th Bn Ghitorni |
| 19.02.2026 | Ranikhet | Bitumen road repair, Transit Camp Kathgodam |

**FACT** — The feed is overwhelmingly **civil works at BOPs**: construction of
permanent buildings and barracks; women's barracks; toilet blocks; waterproofing;
border pillar construction; and, very heavily, *"**Construction of chain link
fencing i/c security gate, sentry post (01 No.) and morcha (04 Nos.)** at BOP
[name] of [n] Bn SSB [station]"* — a recurring standard package appearing dozens
of times across the Tezpur Frontier alone. `[W4]`

**INFERENCE** — That standard package is the **physical hardening of the BOP
compound itself** — a fence around the post, a gate, one sentry post and four
firing positions — **not** fencing of the international border. It is a
person-and-position security model. *Rests on: the tender titles' own wording
`[W4]` and MHA's statement that both SSB borders are open and unfenced `[W3]`.
Falsified by: a tender for linear fencing along the boundary on an SSB border.*

**FACT** — SSB's other visible recurring technical procurement is **off-grid
solar power at BOPs**, tendered by Executive Engineers at Frontier and Sector
HQs. Reported examples: `[W9]` *(trade press reproducing CPPP tender notices)*
- *"SITC of Off Grid Solar Power Station … of 6th Bn Hqrs SSB Ranighuli of SHQ SSB Bongaigaon under FTR Hqrs. SSB Guwahati"*, tender no. `N/FTRG/ENGG/764/1SKWp/SPP/BOPs/6th BN/VOL-/2025-26`, estimated **₹67,87,593**, completion 80 days
- *"Installation of Solar Power Plant at **07 Border Out Posts** of 70th Bn SSB Lakhimpur Kheri II (UP)"*
- *"SITC of Off Grid Solar Power Station each in **08 BOPs** of 31st Bn Gossaigaon"*
- *"Repairing and Up-gradation of **06 Nos** Off-grid Solar Power Plant at BOPs under 57th Bn SSB, Sitarganj"*, authority *"Executive Engineer, SHQ, SSB, Pilibhit"*

**FACT** — The only IT-adjacent SSB tenders surfaced by third-party aggregators
in the 2025 window are **cyber security audits** (infrastructure / security and
compliance audit) at ₹50,000–₹60,000, in Jharkhand and Uttar Pradesh. `[W17]`
*(aggregator listings)*

**FACT** — SSB's own site publishes a *"Three years Procurements Plan in r/o
SSB"*. The PDF served at the linked path is **not** that plan — it is a
concatenation of education-welfare MoUs (Rungta Education Foundation, DAV
University Jalandhar, CSR Educational Trust). The procurement plan itself was
**not retrievable** in this pass. `[W4][W6]`

**UNKNOWN** — Whether an SSB CCTV / FRS / ANPR / VMS / analytics / control-room
tender exists in the **CPPP (eprocure.gov.in) or GeM archives**. The SSB website
feed covers roughly ten months and is not an archive; CPPP's public search was
not queryable without a session in this pass; and the FRS/ANPR setup MHA
confirmed in Feb 2026 `[N3]` was **procured through some route that left no trace
in any feed searched here**.

**INFERENCE** — Two readings of the tender evidence are both live, and this
document does not choose between them:
1. SSB's video procurement happens **centrally at FHQ/MHA level** — possibly
   through the CAPF Modernisation Plan, GeM, or a nomination route — and
   therefore never appears in the Frontier-level engineering tender feed, which
   is dominated by CPWD-style civil works.
2. SSB's video estate is **small**, so few tenders exist to find.

*Rests on: the composition of `[W4]` and the confirmed-but-untraced procurement
in `[N3]`. Falsified by: locating the FRS/ANPR procurement document, which would
settle both the route and the scale.*

---

## 7. F. Evidence gaps

### 7.1 What was searched, and what it returned

Recorded so that the negative results are auditable rather than assumed.

| Source class | What was done | Result |
|---|---|---|
| **SSB Act, 2007** | Retrieved in full from the MHA-hosted PDF `[W1]` | **Closes SQ-26 (Act).** Contains no operational provisions — see §7.2 |
| **SSB Rules, 2009** | Retrieved in full, 110 pages `[W2]` | **Closes SQ-26 (Rules).** Yields the statutory rank list, charter and command chain |
| **MHA Annual Report 2024-25** | Retrieved in full `[W3]` | **Closes SQ-28.** Updated strength, formations, achievements; CIBMS confined to IPB/IBB |
| **Official SSB website** | Reachable; is a React SPA over a **public JSON API** at `ssb.gov.in/api/api`. Enumerated and queried: Frontiers, tenders (280), circulars (81), recruitment-rule cadres, forms, publications `[W4]` | **Closes SQ-27.** Yields Frontier names, the tender feed, and the cadre inventory. **Yields nothing operational** — no doctrine, no SOPs, no organisation chart below Frontier |
| **Parliamentary questions (MHA-hosted PDFs)** | Retrieved LS USQ 459 of 20.07.2021 in full `[W5]`; earlier pass retrieved LS USQ 488 and 634 of 03.02.2026 `[N3][N4]` | **Corrects the SIMS attribution.** No parliamentary answer describing an SSB monitoring or control-room arrangement was found |
| **BPRD / National Police Mission** | Retrieved the full project report *Integrated Border Management and National Security* `[W7]` | Yields the handover finding, the IG (Ops) SSB data gap, and the ILEC/Situation Room **proposal**. Contains no description of an existing control room |
| **Court records (Indian Kanoon)** | Four targeted searches — *"Sashastra Seema Bal"* combined with *CCTV*, *"seizure memo" BOP*, *"Company Commander"*, *wireless message*. Totals: 1, 0, 9, 1 results; the CCTV and wireless hits were read in full `[W10]` | **Negative.** The publicly indexed SSB case corpus is overwhelmingly **service and seniority litigation**. No judgment describing SSB border operational procedure was found. One incidental fact obtained: SSB deploys "platoons" under a "Commander" |
| **Tenders / RFPs / technical specifications** | SSB's own 280-tender feed enumerated exhaustively `[W4]`; six third-party aggregators searched `[W9][W17]` | **Negative for CCTV/VMS/analytics/control room.** Positive for BOP civil works and off-grid solar |
| **CAG** | Searched for a CAG audit of CAPF modernisation or border surveillance procurement | **Negative.** Results returned were **state** police modernisation audits, not CAPF or border-force audits |
| **Parliamentary Standing Committee on Home Affairs** | Searched for an SSB-specific or border-management report | **Negative for a retrievable SSB-specific report.** Only the previously known PRS summary *Working Conditions in Border Guarding Forces* `[N18]` |
| **SSB's own e-magazines** | Six recent Frontier e-magazines downloaded (*Rhino* — FTR Guwahati; *Barahsinga*; *Guldar*; *Dhanesh*; *Devbhoomi*; *Tiger Trail*), 4–34 MB each `[W4]` | **Blocked, not negative.** They are predominantly Hindi with non-extractable font encoding. **This is the most promising unexploited primary corpus found in this pass** — see SQ-W7 |
| **LPAI** | Searched for ICP Raxaul/Jogbani CCTV ownership and control-room arrangements | **Negative.** MHA confirms CCTV is among ICP facilities `[W3]`; **who operates it remains unknown** |

### 7.2 The structural gap: the statute is silent by design

**FACT** — The SSB Act, 2007 has eleven chapters: Preliminary; **Constitution of
the Force and Conditions of Service**; Offences; Punishments; Deductions from Pay
and Allowances; **Arrest and Proceedings Before Trial**; **Force Courts**;
Procedure of Force Courts; Confirmation and Revision of Proceedings; Execution of
Sentences, Pardons, Remissions; Miscellaneous. `[W1]`

**FACT** — Chapter VI, "Arrest and Proceedings Before Trial", concerns the arrest
of **members of the Force** for offences under the Act. It is not a source of
powers over civilians. `[W1]`

**FACT** — Neither the Act nor the Rules contains the words *camera, video,
photograph, surveillance, monitor, CCTV, sensor,* or *electronic record* in any
operational sense. `[W1][W2]`

**INFERENCE** — **The SSB's founding statute is a constitution-and-discipline
instrument, not an operational doctrine.** SSB's border-policing powers come from
notifications under other statutes (CrPC/BNSS, NDPS `[W5]`, Arms, Passport), and
its operational method lives in **internal orders issued under the DG's Rule 9(4)
authority, which are not public**. *Rests on: the chapter structure and word-level
absence in `[W1][W2]`. Falsified by: an SSB Standing Order, Border Management
Manual, or MHA operational instruction entering the public domain.*

**INFERENCE** — **This is why the workflow could not be found, and it means the
workflow is unlikely to be findable by desk research at all.** The documents that
would answer §3 and §4 are the class of document that does not get published.
*Rests on: the above, plus the exhaustive negative results in §7.1. Falsified by:
an RTI reply, a published SSB Standing Order, or a training-institution syllabus.*

### 7.3 Open questions carried forward and newly raised

Prior questions from [ssb-operational-context.md](ssb-operational-context.md)
§15 that **remain open after this pass**: SQ-1, SQ-2, SQ-3, SQ-4, SQ-6, SQ-7,
SQ-8, SQ-9, SQ-10, SQ-11, SQ-12, SQ-13, SQ-14, SQ-15, SQ-17, SQ-18, SQ-21,
SQ-22, SQ-23, SQ-24, SQ-25, SQ-29, SQ-30, SQ-31.

**Closed by this pass:** SQ-26 (Act and Rules retrieved), SQ-27 (SSB website
retrieved), SQ-28 (AR 2024-25 retrieved).

**Superseded:** SQ-5 (*"What is SIMS, technically?"*) — SIMS is an MHA/NCB
national NDPS seizure database `[W5]`, not an SSB system, so the question as
posed no longer applies. What replaces it is SQ-W1 below.

**Partly answered:** SQ-19 / SQ-20 (BOP and formation counts) — AR 2024-25 `[W3]`
re-confirms 539 + 195 BOPs and 6 / 18 / 73, making the primary figures stable
across three consecutive Annual Reports. The lower third-party counts remain
unreconciled.

**New questions raised by this pass:**

- **SQ-W1** — SSB's post-handover **case-monitoring system**: BPRD recorded in
  2021 that SSB *"is now in the process of developing systems and procedures"*
  for it `[W7]`. Was it built? What is it called? Does it hold anything but case
  outcomes?
- **SQ-W2** — Through **what procurement route** was the FRS/ANPR CCTV setup
  `[N3]` bought, given that it appears in no tender feed searched here?
- **SQ-W3** — What are **CLMS** (`clms.ssb.gov.in`) and the SSB recruitment
  portal, and does SSB run any other internal web system? `[W4]`
- **SQ-W4** — Does SSB have an **EDP / IT directorate** equivalent to BSF's
  (`edpdte@bsf.nic.in` `[W11]`), or does the **Communication cadre** own all
  technical systems?
- **SQ-W5** — What is the **CIOA cadre**? It appears in SSB's own cadre index
  `[W4]` with no documents attached and no expansion given anywhere found.
- **SQ-W6** — What became of the **ILEC / Situation Room** proposal `[W7]` after
  09.02.2021? Was any ILEC established at an India-Nepal ICP?
- **SQ-W7** — **Mine the SSB Frontier e-magazines.** *Rhino* (Guwahati),
  *Barahsinga*, *Guldar*, *Dhanesh*, *Devbhoomi*, *Tiger Trail*, *Dolphin*,
  *Koshi* — monthly, published by SSB itself, 110 issues indexed `[W4]`. They are
  the most likely public place for SSB to describe its own posts, equipment
  inductions and daily working. They require **OCR of Hindi Devanagari**.
- **SQ-W8** — Retrieve the **primary PDF of the Rajya Sabha reply of 04.08.2026**
  said to reference *"digital command-and-control platforms"* for CAPFs `[W16]`.
  If that phrase is in an MHA answer, it is the closest thing yet to a named C2
  direction.
- **SQ-W9** — Was anything agreed at the **14th India-Nepal JWG** `[W12]` beyond
  the CCTV sentence — specifically about who installs, who monitors, and whether
  any feed or data crosses the border?
- **SQ-W10** — Retrieve SSB's actual **"Three years Procurements Plan"**; the file
  published under that title is a different document `[W4][W6]`.
- **SQ-W11** — Is there a **sanctioned establishment table** for a BOP — how many
  personnel, what equipment, what ranks? Nothing found states it.

---

## 8. G. What can safely be used as product assumptions

These are the statements strong enough that later stages may build on them
**without further validation**, each with its evidence class. **Nothing in this
list is a product decision, a user model, or a workflow proposal.**

| # | Safe to assume | Evidence class |
|---|---|---|
| **G-1** | **Superintendence is with the Central Government; command with the DG.** The chain of command is **DG → ADG → IG → DIG → Commandant**, with responsibility defined by *"the area that may be assigned"* at every level above battalion | **Statutory** `[W1]` §5, `[W2]` r.9(2) |
| **G-2** | **The statutory rank ladder is fixed and complete** (Rule 8(1)): DG, ADG, IG, DIG, Commandant, 2-i-C, Dy Comdt, AC / Subedar Major, Inspector, SI, ASI / HC, Naik, L/Naik / Constable, Enrolled followers | **Statutory** `[W2]` r.8 |
| **G-3** | **Frontier = IG, Sector = DIG, Battalion = Commandant**, as consistently observed in SSB's own publications and reported officer designations, and consistent with Rule 9(2) | **Statutory + primary observation** `[W2][W4][W8]` |
| **G-4** | **An outpost is commanded by an officer of Deputy Commandant / Assistant Commandant rank, or by a subordinate officer not below Sub-Inspector.** This is a statutory floor, not a norm | **Statutory** `[W1]` §56(3)–(4) |
| **G-5** | **Frontier, Sector, Company, Platoon and BOP are administrative constructs, not statutory formations.** Only "battalion" and "unit" are constituted by the Central Government | **Statutory silence + Rule 9(4)** `[W1][W2]` |
| **G-6** | **The statutory task is Rule 9(1): safeguard the assigned borders *and promote a sense of security among the border population*; prevent trans-border crime, smuggling and illegal activity; prevent unauthorised entry and exit; carry out civic action.** Surveillance is not named as a task | **Statutory** `[W2]` r.9(1) |
| **G-7** | **Both SSB borders are open and unfenced, and MHA states the challenge as "misuse of the open border by terrorists and criminals"** — verbatim identical for India-Nepal and India-Bhutan across three consecutive Annual Reports (2022-23, 2023-24, 2024-25) | **Primary, repeated** `[N1][N2][W3]` |
| **G-8** | **No CIBMS-equivalent programme exists on the SSB borders.** CIBMS is defined and located on the India-Pakistan and India-Bangladesh borders; the India-Nepal and India-Bhutan paragraphs contain only roads and BOP counts | **Primary, repeated** `[N1][W3]` |
| **G-9** | **BOP counts are stable: 539 (Nepal) + 195 (Bhutan) = 734**, unchanged across AR 2022-23, 2023-24 and 2024-25 | **Primary, repeated** `[N1][N2][W3]` |
| **G-10** | **SSB has procured a CCTV setup with automatic face recognition and automatic number-plate recognition** — the deployment is unknown, but the procurement is a stated fact of record | **Primary** `[N3]` |
| **G-11** | **SSB apprehends and seizes; the local police investigate and prosecute.** Handover to the local police is the terminal step of an SSB case, and the receiving agency is documented as under-resourced for these cases | **Government report** `[W7]` |
| **G-12** | **SSB is NDPS-empowered**, named alongside BSF, Indian Coast Guard, RPF and NIA | **Primary** `[W5]` |
| **G-13** | **SIMS is MHA's national NDPS seizure-data portal, not an SSB system** — and therefore **not** a candidate for "existing command and control systems" | **Primary** `[W5]` |
| **G-14** | **Section 63 BSA, 2023 applies to SSB video exactly as to any other electronic record** — a certificate with a hash, signed by the device custodian and by an expert. SSB itself publishes the BNS/BNSS/BSA texts to the Force | **Statutory (force-agnostic)** `[S29]`, `[W4]` |
| **G-15** | **SSB's technical cadre is the Communication cadre, supported by a Wireless & Telecom Training Centre. There is no IT, cyber, video or electronics cadre** | **Primary** `[W3][W4]` |
| **G-16** | **BOP electrical supply is being addressed by off-grid solar, tendered per-battalion in lots of 6–8 BOPs** by Frontier and Sector Executive Engineers | **Primary-adjacent (CPPP notices via trade press)** `[W9]` |
| **G-17** | **SSB's current BOP construction programme hardens the post, not the border**: chain-link fencing, a security gate, one sentry post and four morchas per BOP, plus permanent buildings and barracks | **Primary (SSB's own tender feed)** `[W4]` |
| **G-18** | **42% of SSB BOPs lack road connectivity** (308 of 734) — carried forward, unchanged and uncontradicted by AR 2024-25 | **News, uncontradicted** `[N9]` |
| **G-19** | **SSB is deployed on internal-security and counter-insurgency duties beyond the border** — J&K, Assam, and LWE areas of Chhattisgarh, Jharkhand and Bihar — so not every battalion is a border battalion | **Primary** `[W3]` §7.51 |
| **G-20** | **India and Nepal have, as of 21 August 2026, agreed at government level to enhance border surveillance using CCTV and other modern technologies, and to strengthen real-time information sharing** | **News, multi-outlet, consistent** `[W12]` |

---

## 9. H. What must remain unknown

Stated as prohibitions on later stages. **Each of these must be carried into
`docs/02-product/` as an explicit open question, not silently resolved by
assumption.**

| # | Must remain UNKNOWN | Why it cannot be assumed |
|---|---|---|
| **H-1** | **Whether SSB monitors live video at all, and if so at what echelon.** | Two independent research passes, across primary statutes, three MHA Annual Reports, parliamentary answers, a BPRD project report, SSB's own website and publication corpus, court records and six tender aggregators, produced **no** description of an SSB control room, operations room, video wall, monitoring roster or operator establishment. The BSF/BOLD-QIT pattern is explicitly non-transferable ([ssb-operational-context.md](ssb-operational-context.md) §16 item 7) |
| **H-2** | **The detection → assessment → escalation → response sequence at a BOP or check post.** | Nothing describes it. The command chain (G-1) is a *disciplinary and administrative* chain established by Rule 9(2); **whether an operational alert travels the same path is not stated anywhere** |
| **H-3** | **What carries an alert, and to whom.** | The only report transport named in the statute is *"through the messenger"*, for a death, to a police station `[W2]`. Radio, phone and data links at a BOP are undocumented |
| **H-4** | **Whether a QRT construct exists in SSB.** | Not documented. The response element may be the patrol or naka already deployed |
| **H-5** | **The installed camera base — count, siting, make, resolution, codec, PTZ/fixed, thermal/visible, ONVIF conformance, recorder/VMS.** | No source states any of it. `[N3]` confirms procurement and nothing else |
| **H-6** | **What "existing command and control systems" means for SSB.** | The only prior candidate (SIMS) has been eliminated `[W5]` and nothing replaces it. Treating any named system as SSB's C2 without evidence would be inventing a requirement |
| **H-7** | **Whether a written SOP or Standing Order governs border-event handling, and what it says.** | Rule 9(4) places this in the DG's hands and such orders are not published. This is **structurally unlikely to be resolved by desk research** (§7.2) |
| **H-8** | **Whether any event that produces no seizure and no arrest is recorded anywhere.** | Every verified SSB reporting instrument is outcome-shaped or discipline-shaped |
| **H-9** | **The normal rank and establishment of a BOP in-charge and a check-post in-charge.** | The statute gives a floor (not below SI) and a ceiling (Dy Comdt / AC), not a norm `[W1]` §56(3)–(4) |
| **H-10** | **Who owns and monitors CCTV at ICP Raxaul and ICP Jogbani.** | MHA lists CCTV among ICP facilities and LPAI operates ICPs `[W3]`; SSB's relationship to those feeds is unstated |
| **H-11** | **The legal basis, authorisation level, retention rule and oversight for face recognition applied to Indian, Nepali and Bhutanese nationals exercising a treaty right of movement.** | Unresolved from the previous pass (SQ-8); nothing in `[W1][W2]` addresses it, and the SSB Act contains no data or privacy provision |
| **H-12** | **Bandwidth, power budget and connectivity at an SSB BOP.** | Off-grid solar tenders `[W9]` establish that power is being *addressed*, not what the resulting budget is. No data-link evidence was found at all |
| **H-13** | **What "suspicious activity" means on a border where crossing is lawful.** | Carried forward unresolved (SQ-7). MHA's own framing is *"misuse of the open border"* `[W3]`, which presupposes a lawful-use baseline nobody has defined |
| **H-14** | **Whether the Indo-Bhutan border is operationally the same problem as the Indo-Nepal border.** | Every source treats them together and MHA's challenge sentence is verbatim identical for both `[W3]` — which may reflect drafting convention rather than operational sameness. The Frontier structure hints otherwise: Tezpur and Siliguri Frontiers appear on the Bhutan side, Ranikhet / Lucknow / Patna on the Nepal side `[W4]` |

**A final constraint on later stages.** The correct status of the primary user is
that **the surveillance/CCTV operational workflow has not been sufficiently
validated from our sources** — not that it does not exist. Any user hierarchy or
workflow written into `docs/02-product/` before H-1 and H-2 are answered will be
**invented, not discovered**, and must be labelled as such at the point it is
written.

---

## 10. Sources

Reliability key: **P** = primary/official Indian government · **G** = government
research body · **A** = academic · **N** = news · **V** = vendor/trade ·
**C** = court record · **E** = encyclopedic/tertiary.

| ID | Source | Type | Retrieval | URL |
|---|---|---|---|---|
| W1 | **The Sashastra Seema Bal Act, 2007** (Act No. 53 of 2007), Gazette of India Extraordinary, 20.12.2007 — §2 definitions, §4 constitution, §5 control, §22/§23/§30 offences, §56 powers of commanding officers and of officers commanding a company/detachment/outpost | P | **Direct (full text)** | https://www.mha.gov.in/sites/default/files/2023-01/SSB-Act2007_0[1]_1[1]_0.pdf |
| W2 | **The Sashastra Seema Bal Rules, 2009** (made under s.155) — r.7 constitution, **r.8 ranks**, **r.9 task of the Force, command and control**, r.10 command, r.176 Courts of Inquiry | P | **Direct (full text, 110 pp.)** | https://www.mha.gov.in/sites/default/files/SSB-Rule2009_3.pdf |
| W3 | **MHA Annual Report 2024-25** — §3.20–3.24 CIBMS/IMB, §3.26–3.28 India-Nepal and India-Bhutan borders, §3.39 ICP list, §7.50–7.52 SSB profile/formations/strength/achievements, §7.60–7.61 Modernisation Plan-IV, NIDMS | P | **Direct (full text, 22.7 MB)** | https://www.mha.gov.in/sites/default/files/AREnglish_24032026.pdf |
| W4 | **Official SSB website and its public JSON API** (`ssb.gov.in`, API base `https://ssb.gov.in/api/api`) — Frontier list; full tender feed (280 records, 07.10.2025–11.08.2026); circulars (81); recruitment-rules cadre index; forms; publications index (110 issues); document paths incl. `assets/document/Laws/{BNS,BNSS,BSA}` | P | **Direct (API queried; documents downloaded)** | https://ssb.gov.in/ |
| W5 | **MHA, Lok Sabha Unstarred Question No. 459**, answered 20.07.2021 — *Drug Trafficking*; **defines SIMS** and records SSB's NDPS empowerment | P | **Direct (full text)** | https://www.mha.gov.in/MHA1/Par2017/pdfs/par2021-pdfs/LS-20072021/459.pdf |
| W6 | **SSB-signed Memoranda of Understanding** (Rungta Education Foundation; DAV University Jalandhar; CSR Educational Trust), published on the SSB site under the *"Three years Procurements Plan"* title — FHQ address, **IG (Admn)** as SSB Joint Manager | P | **Direct (scanned pages read)** | https://ssb.gov.in/assets/document/circulars/1.pdf |
| W7 | **Bureau of Police Research and Development, MHA / National Police Mission, Micro Mission 06** — *Integrated Border Management and National Security*, Project No. 05/MM:06, project leader Shri Santosh Mehra, IPS, ADG BPR&D, approved 09.02.2021. **Handover practice; IG (Ops) SSB case-data gap; ILEC and Situation Room proposal; ILEC equipment schedule** | G | **Direct (full text)** | https://bprd.nic.in/uploads/pdf/Integrated%20Border%20Management%20and%20National%20Security.pdf |
| W8 | Deccan Herald / PTI — *Indo-Nepal border under tight vigil ahead of PM Modi's Ayodhya visit*, 27.12.2023 — quotes **Deputy Inspector General, SSB, Gorakhpur, Akhileshvar Singh**; dog squads, one platoon of the women's wing, **metal detectors at Sonauli and Thuthibari outposts** | N | Direct (headline and attribution block; article body behind SPA) | https://www.deccanherald.com/india/uttar-pradesh/indo-nepal-border-under-tight-vigil-ahead-of-pm-modis-ayodhya-visit-2826402 |
| W9 | **EQ Mag Pro** — trade-press reproductions of SSB CPPP tender notices for off-grid solar power plants at BOPs (6th Bn Ranighuli / SHQ Bongaigaon / FTR Guwahati; 70th Bn Lakhimpur Kheri II; 31st Bn Gossaigaon; 57th Bn Sitarganj / EE SHQ Pilibhit) | V | Indirect (search-result extracts; the site returned HTTP 403 to direct fetch) | https://www.eqmagpro.com/tag/ssb-guwahati/ |
| W10 | **Indian Kanoon** — four targeted searches of the SSB corpus. *Nisha Priya Bhatia vs S.K Goel*, Delhi District Court, 06.03.2012 (incidental: *"Commander, Sh. S. Murup of the SSB Platoon which guards the R&AW training institute campus, Gurgaon"*); *Saurabh Dubey & Ors. vs Union of India*, Delhi High Court, 25.05.2015 (CAPF cadre seniority) | C | Direct | https://indiankanoon.org/ |
| W11 | **CPWD Border Fencing Zone circulation list** — BSF EDP Directorate contact (`edpdte@bsf.nic.in`), and DG addresses for ITBP, BRO and SSB | P | Direct (within `[W15]`) | — |
| W12 | **14th India-Nepal Joint Working Group on Border Management**, Dehradun, 20–21 August 2026 — CCTV surveillance agreement; delegations led by Ms. Pausumi Basu, JS (BM-I), MHA and Mr. Ananda Kafle, JS, MoHA Nepal; 15th meeting to be held in Nepal | N | Direct (multiple outlets, consistent wording) | https://therahnuma.com/nepal-and-india-agree-to-enhance-security-surveillance-at-sensitive-locations-along-border |
| W13 | Deccan Chronicle — *SSB Safeguards 2,450-km Open borders with Nepal, Bhutan: Bandi Sanjay* — MoS Home statement on SSB technology; 2025-26 outputs (661 trafficking victims rescued, 6,324 apprehended); 18 relief and rescue teams | N | Direct | https://www.deccanchronicle.com/nation/ssb-safeguards-2450-km-open-borders-with-nepal-bhutan-bandi-sanjay-1979854 |
| W14 | Raygain Technologies — case study, **SSB Rotational E-Transfer System** (PHP / Apache / Linux / MySQL) | V | Direct | https://raygain.com/case_studies/sashastra-seema-bal-ssb/ |
| W15 | **CPWD, Office of the Chief Engineer, Border Fencing Zone** — *Engagement of Retired Govt. Officer / Qualified Professionals as Chief Consultant on Contract Basis*, No. W-12011/268/CE/EE-I/2025-26/1452, dated 24.10.2025 — **Project Monitoring Unit, Department of Border Management, MHA**; circulated to JS (BM-I) MHA, DGs of BSF/ITBP/SSB/AR, Director (ICB) (BM-IV) | P | **Direct (scanned page read)** | https://ssb.gov.in/assets/document/Circulars/Circular_181125_144338.pdf |
| W16 | ETV Bharat — *New Weapons, Smarter Surveillance: CAPFs Gain Edge In Border, Internal Security Missions*, 04.08.2026 — reports a Rajya Sabha reply by MoS Home Nityanand Rai to MP Bhola Singh; SSB Modernisation Plan-IV outlay; *"Hyper-Converged Infrastructure servers, networking equipment and digital command-and-control platforms"* | N | Direct | https://www.etvbharat.com/en/bharat/new-weapons-smarter-surveillance-capfs-gain-stronger-edge-in-border-and-internal-security-missions-enn26080406342 |
| W17 | Tata nexarc / Tendersontime / TendersPlus / TenderDetail / BidAssist — third-party SSB tender aggregators. Used only to test for CCTV/VMS/analytics tenders; returned cyber-security audits, civil works and solar | V | Direct / partial (some returned HTTP 403) | https://www.tatanexarc.com/t/authority/sashastra-seema-bal-ssb-tenders/ |

**Carried forward** from [ssb-operational-context.md](ssb-operational-context.md)
§17 and cited here by its IDs: `[N1]`, `[N2]`, `[N3]`, `[N4]`, `[N6]`, `[N8]`,
`[N9]`, `[N18]`, `[N19]`, `[N23]`. **Carried forward** from
[domain-research.md](domain-research.md) §9: `[S29]`.

### 10.1 Sources sought and not obtained

Recorded so that a later pass does not repeat the attempt blindly.

- **India Code** (`indiacode.nic.in`) — HTTP 404 on the SSB Act handle and bitstream. **Not needed**: the MHA-hosted texts `[W1][W2]` were obtained instead.
- **SSB's *"Three years Procurements Plan"*** — the file published under that title is a set of education MoUs `[W6]`. The plan itself was not obtained.
- **The primary PDF of the Rajya Sabha reply of 04.08.2026** `[W16]` — not located.
- **A CAG audit of CAPF or border-force modernisation procurement** — none located.
- **A Parliamentary Standing Committee report specific to SSB** — none located beyond the PRS summary `[N18]`.
- **eprocure.gov.in (CPPP) archive search** — not queryable without a session in this pass.
- **SSB Frontier e-magazines** — downloaded but not readable (Hindi, non-extractable font encoding). See **SQ-W7**.

---

## Document status

**Complete for this pass — Stage 01, Domain Research, SSB operational workflow.**

**What this pass established:** the organisational hierarchy and the charter of
duties, now grounded in the **SSB Act, 2007 and the SSB Rules, 2009** rather than
in a foreign master's thesis; the **named Frontiers**; the **cadre inventory**;
the **exhaustive content of SSB's own public tender feed**; and a **correction to
the SIMS attribution** that removes the only candidate this project had for
"existing command and control systems".

**What this pass did not establish, after a documented and exhaustive search:**
the CCTV monitoring arrangement, the control-room arrangement, the incident and
alert workflow, and the response construct —
[§3](#3-c-verified-cctv--control-room-workflow),
[§4](#4-d-verified-incident--alert-workflow),
[§9](#9-h-what-must-remain-unknown).
[§7.2](#72-the-structural-gap-the-statute-is-silent-by-design) argues these are
**structurally unlikely to be resolved by desk research**, which is itself a
finding that later stages must plan around.

**No product, design, architecture or technology decisions are made or implied by
this document.** No IBVAP user hierarchy is proposed. No product workflow is
recommended.
