# Client Workshop Agenda & End-User Training Outline
## SAP S/4HANA Manufacturing Implementation & Change Enablement

**Document Identifier:** `WS-MFG-TRN-001`  
**Author:** Adarsh (Target Role: SAP Manufacturing / Production Planning / PLM Functional Consultant)  
**Client Context:** Automotive Tier-1 Lighting Manufacturing Plant (Plant `1010`)  
**Reference Release:** SAP S/4HANA 2023 / Cloud Private Edition  
**Status:** Approved v1.0 | **Date:** 2 November 2026  
**Linked PRD Deliverable:** Nice-to-Have P1 Workshop Agenda and Training Outline  

---

## 1. Executive Summary & Workshop Objectives

Transitioning from legacy shop floor paper travelers and spreadsheet forecasting to an integrated SAP S/4HANA Manufacturing solution requires structured alignment between functional consultants, plant leadership, industrial engineers, and shop floor supervisors. 

This document defines a **3-Day Consultant-Led Business Process Alignment Workshop** and a targeted **Role-Based End-User Training Curriculum**.

---

## 2. 3-Day Client Workshop Agenda: "From Shop Floor to S/4HANA"

### Day 1: Master Data Foundation & Engineering Handoff
**Target Audience:** Industrial Engineers, BOM Specialists, PLM Design Leads, Plant Controller.

| Time Window | Session Topic | Key Deliverables & Discussion Topics | Lead Facilitator |
| :--- | :--- | :--- | :--- |
| **09:00 - 10:30** | Executive Vision & Enterprise Structure | Plant `1010` organization, storage locations (`101A` to `101Q`), valuation classes. | Lead Consultant |
| **10:45 - 12:30** | Material Master & Multi-Level BOM Deep Dive | Material Types (`FERT`, `HALB`, `ROH`), Component scrap %, line backflushing. | Master Data Consultant |
| **13:30 - 15:00** | Shop Floor Work Centers & Routings | Standard value keys (`SAP1`), capacity shift calendars (16 hrs/day), activity rates (`KP26`). | PP Consultant |
| **15:15 - 17:00** | PLM-to-ERP Integration Blueprint | EBOM to MBOM realignment, CAD phantom dissolution, consumable recipe injection. | Integration Specialist |

### Day 2: Demand Planning, MRP Live & Order Scheduling
**Target Audience:** Demand Planners, MRP Controllers, Production Schedulers, Procurement Buyers.

| Time Window | Session Topic | Key Deliverables & Discussion Topics | Lead Facilitator |
| :--- | :--- | :--- | :--- |
| **09:00 - 10:30** | Demand Management & Forecasting | Strategy `40` (Planning with final assembly), PIR entry (`MD61`), sales order consumption. | Planning Consultant |
| **10:45 - 12:30** | In-Memory MRP Live (`MD01N`) Simulation | MRP run mechanics on HANA, stock/requirements list (`MD04`), reschedule messages. | PP Consultant |
| **13:30 - 15:00** | Capacity Leveling & Order Conversion | Finite capacity scheduling, bottleneck analysis at adhesive cell (`WC-GLUE-03`), `CO40`. | PP Consultant |
| **15:15 - 17:00** | Component ATP Check & Order Release Gates | Availability check control (`OPJK`), missing parts management, hard release blocks. | PP Consultant |

### Day 3: Shop Floor Execution, Quality Milestones & ECM Cutover
**Target Audience:** Production Supervisors, Line Operators, Quality Managers, Change Coordinators.

| Time Window | Session Topic | Key Deliverables & Discussion Topics | Lead Facilitator |
| :--- | :--- | :--- | :--- |
| **09:00 - 10:30** | Production Order Lifecycle & Staging | Order release (`REL`), shop traveler barcode printing, serialized goods issue (`261`). | PP Consultant |
| **10:45 - 12:30** | Milestone Confirmations & Scrap Tracking | Op `0050`/`0070` milestones (`CO11N`), scrap reason codes, supervisor lockout (>3%). | PP/QM Consultant |
| **13:30 - 15:00** | In-Process QM Inspection & Usage Decision | Lot Origin `03`, result recording (`QE51N`), defect notifications (`F2929`), rework orders. | QM Consultant |
| **15:15 - 17:00** | Engineering Change Cutover & Open Issues | Change Master (`CC01`), Valid-From dates, WIP order cutovers, sign-off on open issues log. | PLM/PP Consultant |

---

## 3. Role-Based End-User Training Curriculum

The end-user training program delivers tailored, hands-on micro-learning modules for each operational role prior to system cutover:

```
+---------------------------------------------------------------------------------+
|                       Plant 1010 Training Tracks                                |
+---------------------------------------------------------------------------------+
| Track A: Production Planner         | Track B: Shop Floor Supervisor            |
| * PIR Maintenance (MD61)            | * Manage Production Orders (CO01/CO02)    |
| * MRP Live Execution (MD01N)        | * Missing Parts Evaluation (CO02 / ATP)   |
| * Material Coverage Analysis (MD04) | * Failed Goods Reprocessing (COGI)        |
| * Planned Order Conversion (CO40)   | * Order Technical Completion (TECO)       |
+-------------------------------------+-------------------------------------------+
| Track C: Line Assembly Operator     | Track D: Quality Assurance Inspector      |
| * Scanning Traveler Barcodes        | * Managing Inspection Lots (QA32)         |
| * Confirming Operations (CO11N)     | * Characteristic Result Recording (QE51N) |
| * Recording Yield & Actual Hours    | * Defect Recording (F2929 / QM01)         |
| * Mandatory Scrap Reason Selection  | * Usage Decision & Blocked Stock (QA11)   |
+---------------------------------------------------------------------------------+
```

### Training Success Metrics
1. **Certification Score:** Minimum 85% passing score on hands-on system scenario simulations.
2. **First-Day Operational Independence:** Supervisors execute order creation, release, and confirmations with zero escalation calls to the IT hypercare desk.
