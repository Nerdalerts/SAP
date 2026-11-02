# User Stories & Acceptance Criteria
## SAP S/4HANA Manufacturing, PLM, and Quality Management

**Document Identifier:** `US-MFG-ALL-001`  
**Author:** Adarsh (Target Role: SAP Manufacturing / Production Planning / PLM Functional Consultant)  
**Reference Release:** SAP S/4HANA 2023 / Cloud Private Edition  
**Status:** Approved v1.0 | **Date:** 2 November 2026  
**Linked PRD Deliverable:** Must-Have P0 User Stories (20 Full Agile Stories with Given/When/Then Criteria)  

---

## 1. Traceability Summary Matrix

| Story ID | Scenario | Functional Area | User Persona / Role | Linked FRD ID | Linked Test Case ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **US-MD-001** | SC-01 | Master Data | Master Data Specialist | FR-PP-001 | TC-MD-001 |
| **US-MD-002** | SC-01 | Master Data | BOM Engineer | FR-PP-006 | TC-MD-002 |
| **US-MD-003** | SC-01 | Costing | Plant Cost Accountant | FR-PP-008 | TC-MD-003 |
| **US-WC-001** | SC-02 | PP Master Data | Industrial Engineer | FR-PP-001 | TC-WC-001 |
| **US-WC-002** | SC-02 | PP Master Data | Process Engineer | FR-PP-007 | TC-WC-002 |
| **US-PLN-001**| SC-03 | Demand Planning | Demand Planner | FR-PP-001 | TC-PLN-001 |
| **US-PLN-002**| SC-03 | MRP Live | MRP Controller | FR-PP-002 | TC-PLN-002 |
| **US-PLN-003**| SC-03 | Planning / Shop Floor | Production Scheduler | FR-PP-001 | TC-PLN-003 |
| **US-PP-001** | SC-04 | Shop Floor Control | Production Supervisor | FR-PP-001 | TC-PP-001 |
| **US-PP-002** | SC-04 | Inventory Check | Production Scheduler | FR-PP-002 | TC-PP-002 |
| **US-PP-003** | SC-04 | Shop Floor Release | Production Supervisor | FR-PP-003 | TC-PP-003 |
| **US-PP-004** | SC-04 | Warehouse Logistics | Warehouse Material Handler | FR-PP-004, FR-PP-005 | TC-PP-004 |
| **US-PP-005** | SC-04 | Shop Floor Execution | Line Assembly Operator | FR-PP-006, FR-PP-007 | TC-PP-005 |
| **US-PP-006** | SC-04 | Shop Floor Execution | Line Assembly Operator | FR-PP-009, FR-PP-010 | TC-PP-006 |
| **US-PP-007** | SC-04 | Inventory Receipt | Production Supervisor | FR-PP-011 | TC-PP-007 |
| **US-PP-008** | SC-04 | Exception Handling | Production Supervisor | FR-PP-012 | TC-PP-008 |
| **US-QM-001** | SC-05 | Quality Inspection | Shop Floor Quality Inspector | FR-PP-013 | TC-QM-001 |
| **US-QM-002** | SC-05 | Defect Management | Quality Assurance Engineer | FR-PP-009, FR-PP-013 | TC-QM-002 |
| **US-ECM-001**| SC-06 | Change Management | Engineering Change Coordinator | FR-PP-014 | TC-ECM-001 |
| **US-INT-001**| SC-07 | PLM Integration | CAD / PLM Design Lead | FR-PP-001, FR-PP-014 | TC-INT-001 |

---

## 2. Detailed User Stories & Acceptance Criteria

### US-MD-001: Material Master Definition for Automotive Headlamp Assembly
- **Role:** Master Data Specialist
- **User Story:** As a Master Data Specialist, I want to create and extend material master records for Finished Goods (`FERT`), Semi-Finished Assemblies (`HALB`), and Raw Materials (`ROH`) in Plant `1010` with MRP and Work Scheduling views so that downstream planning and production execution transactions can proceed without missing-view errors.
- **Acceptance Criteria:**
  - **AC-01 (Given/When/Then):**
    - *Given* a new engineering specification for headlamp `HL-200X`,
    - *When* the user creates the material via Fiori App `Manage Product Master Data` (`MM01`) with Material Type `FERT`, Industry Sector `M` (Mechanical Engineering), and Base UoM `EA`,
    - *Then* the system must require and successfully save Basic Data 1/2, MRP 1-4, Work Scheduling, QM, and Accounting/Costing views for Plant `1010`.
  - **AC-02 (Negative Path):**
    - *Given* an attempt to save `HL-200X` without maintaining the MRP Controller (`P01`) or Production Scheduling Profile (`PP0001`),
    - *When* the user clicks Save,
    - *Then* the system must halt commitment and display an explicit error prompting for mandatory work scheduling parameters.

---

### US-MD-002: Multi-Level Production BOM with Scrap and Backflush Flags
- **Role:** BOM Engineer
- **User Story:** As a BOM Engineer, I want to maintain a multi-level Bill of Materials for assembly `HL-200X` with Usage `1` (Production), line scrap percentages, and backflushing indicators so that component demand and automated consumption reflect physical shop floor realities.
- **Acceptance Criteria:**
  - **AC-01:**
    - *Given* material `HL-200X` in Plant `1010`,
    - *When* the user creates the BOM in `CS01` with Usage `1` and adds sub-components (`HL-HOU-101`, `HL-LENS-201`, `HL-PCB-301`, `HL-ADH-501`),
    - *Then* item category `L` (Stock item) must be assigned, consumable adhesive `HL-ADH-501` must have component scrap set to `3.0%`, and the Backflush indicator must default to `1` (Always backflush).
  - **AC-02 (Circular BOM Prevention):**
    - *Given* an open BOM in `CS02`,
    - *When* an engineer attempts to add parent material `HL-200X` as a component of sub-assembly `HL-HOU-101`,
    - *Then* the system must detect recursion, abort the transaction, and display Error `29 018: Recursive BOM structure detected`.

---

### US-MD-003: Standard Cost Roll-Up and Cost Estimate Release
- **Role:** Plant Cost Accountant
- **User Story:** As a Plant Cost Accountant, I want to execute cost roll-up calculations for `HL-200X` based on BOM components and routing standard values so that the standard valuation price is established prior to manufacturing release.
- **Acceptance Criteria:**
  - **AC-01:**
    - *Given* an active BOM and routing for `HL-200X`,
    - *When* the cost accountant executes Cost Estimate `CK11N` for Costing Variant `PPC1`,
    - *Then* the system must explode the BOM, multiply quantities by standard purchasing prices, multiply routing operation times by cost center activity rates (`SET`, `MAC`, `LAB`), and calculate a standard unit cost.
  - **AC-02:**
    - *Given* an approved cost calculation,
    - *When* the user executes Price Marking and Release in `CK24`,
    - *Then* table `MBEW-STPRS` must update with the new standard price and become effective for the current posting period.

---

### US-WC-001: Work Center Capacity and Cost Center Linkage
- **Role:** Industrial Engineer
- **User Story:** As an Industrial Engineer, I want to configure shop floor work centers (`WC-ASSY-01` to `WC-PKG-07`) with standard value key `SAP1`, shift capacities, and linked production cost centers so that lead-time scheduling and activity cost allocations function accurately.
- **Acceptance Criteria:**
  - **AC-01:**
    - *Given* a new assembly cell `WC-GLUE-03` in Plant `1010`,
    - *When* the user creates the work center in `CR01` with Category `0001` (Machine),
    - *Then* Standard Value Key `SAP1` must be assigned with parameters Setup, Machine, and Labor, Cost Center `CC-PROD-102` must be linked, and capacity category `002` (Machine) must be set to 2 shifts (16 hours gross / 14.4 hours net productive).

---

### US-WC-002: Assembly Routing and Component Allocation
- **Role:** Process Engineer
- **User Story:** As a Process Engineer, I want to create an assembly routing with operation sequences 0010 to 0070 and allocate specific BOM components to matching operations so that shop floor operators only see parts relevant to their station.
- **Acceptance Criteria:**
  - **AC-01:**
    - *Given* routing group `50001201` for material `HL-200X`,
    - *When* the user maintains operations in `CA02` and executes Component Allocation,
    - *Then* PUR adhesive `HL-ADH-501` must be assigned strictly to Operation `0030`, Projector lens `HL-LENS-201` to Operation `0020`, and shipping carton `HL-PKG-801` to Operation `0070`.

---

### US-PLN-001: Planned Independent Requirements (PIR) Maintenance
- **Role:** Demand Planner
- **User Story:** As a Demand Planner, I want to maintain monthly and weekly forecast quantities for `HL-200X` in S/4HANA under Planning Strategy `40` so that procurement and production schedules anticipate OEM customer orders.
- **Acceptance Criteria:**
  - **AC-01:**
    - *Given* monthly OEM forecast schedules,
    - *When* the planner inputs demand via Fiori App `Maintain PIRs` (`MD61`) for Plant `1010` with Version `00` (Active),
    - *Then* requirements type `VSF` must be recorded in table `PBED`, and incoming sales orders must dynamically consume the forecast without duplicating gross demand.

---

### US-PLN-002: In-Memory MRP Live Execution and Shortage Detection
- **Role:** MRP Controller
- **User Story:** As an MRP Controller, I want to execute MRP Live (`MD01N`) directly in SAP HANA so that component shortages and rescheduling dates are calculated across the entire BOM in real time.
- **Acceptance Criteria:**
  - **AC-01:**
    - *Given* active PIR demand for 500 units of `HL-200X`,
    - *When* the controller triggers MRP Live in `MD01N`,
    - *Then* the system must generate Planned Orders for assemblies and Purchase Requisitions for raw materials within 30 seconds, flagging materials with negative stock coverage in Fiori App `Monitor Material Coverage` (`MD04`).

---

### US-PLN-003: Planned Order Conversion to Production Order
- **Role:** Production Scheduler
- **User Story:** As a Production Scheduler, I want to convert planned orders into firm production orders so that assembly can be scheduled on specific shop floor lines.
- **Acceptance Criteria:**
  - **AC-01:**
    - *Given* a planned order in `MD04` with satisfied component coverage,
    - *When* the scheduler executes conversion via Fiori App `Manage Planned Orders` (`CO40`),
    - *Then* the system must generate a production order of type `PP01`, copy the active BOM and routing, assign reservation numbers, and update order status to `CRTD`.

---

### US-PP-001: Discrete Production Order Creation and Scheduling
- **Role:** Production Supervisor
- **User Story:** As a Production Supervisor, I want to create a production order for 100 units of `HL-200X` and execute lead-time scheduling so that start and end dates for each shop floor operation are established.
- **Acceptance Criteria:**
  - **AC-01:**
    - *Given* material `HL-200X` in Plant `1010`,
    - *When* the supervisor creates order type `PP01` via `CO01` for lot size 100 EA,
    - *Then* operations `0010` to `0070` must be scheduled across the factory calendar, calculating earliest/latest start dates and reservation items in table `RESB`.

---

### US-PP-002: Dynamic Component ATP Availability Check
- **Role:** Production Scheduler
- **User Story:** As a Production Scheduler, I want the system to verify that all required raw materials and sub-assemblies are in stock before authorizing production so that the assembly line is not starved midway through a shift.
- **Acceptance Criteria:**
  - **AC-01 (Full Availability):**
    - *Given* sufficient unrestricted stock in storage locations `101B` and `101C`,
    - *When* an availability check is executed in `CO02`,
    - *Then* the order status must update to `MACM` (Material committed).
  - **AC-02 (Missing Parts Block):**
    - *Given* zero stock of Bi-LED module `HL-PCB-301`,
    - *When* the ATP check runs,
    - *Then* the order must be assigned status `MSPT` (Missing Part), and an alert must populate the Missing Parts List.

---

### US-PP-003: Production Order Release and Shop Traveler Generation
- **Role:** Production Supervisor
- **User Story:** As a Production Supervisor, I want to release the production order and print barcoded shop travelers so that line operators have authorization to draw materials and start assembly.
- **Acceptance Criteria:**
  - **AC-01:**
    - *Given* a production order in status `CRTD` with component availability confirmed,
    - *When* the supervisor clicks Release (`REL`) in `CO02`,
    - *Then* the system status must change to `REL`, reservations must become active for warehouse picking, and shop floor traveler cards with 2D DataMatrix barcodes must be dispatched to the line printer.

---

### US-PP-004: Staging and Serialized Goods Issue for High-Value Modules
- **Role:** Warehouse Material Handler
- **User Story:** As a Warehouse Material Handler, I want to stage components to line-side bins and record goods issue for serialized Bi-LED modules (`HL-PCB-301`) so that inventory balances and unit serial genealogy are accurately maintained.
- **Acceptance Criteria:**
  - **AC-01:**
    - *Given* released production order `1000845`,
    - *When* the handler performs Goods Issue (`MIGO` Movement Type `261`) for material `HL-PCB-301`,
    - *Then* the system must mandate entry of 100 unique valid serial numbers, debit storage location `101B`, and update production order actual costs.

---

### US-PP-005: Milestone Operation Confirmation and Automated Backflushing
- **Role:** Line Assembly Operator
- **User Story:** As a Line Assembly Operator, I want to confirm milestone Operation `0050` (Photometric Test) so that preceding assembly operations (`0010` to `0040`) are confirmed automatically and standard consumables are backflushed.
- **Acceptance Criteria:**
  - **AC-01:**
    - *Given* a released production order,
    - *When* the operator confirms Operation `0050` in Fiori App `Confirm Production Operation` (`CO11N`) with Yield = 98 EA and Scrap = 2 EA,
    - *Then* operations `0010`, `0020`, `0030`, and `0040` must update to confirmed status, and PUR adhesive `HL-ADH-501` (4.545 KG) and fasteners `HL-SCR-701` (606 EA) must be backflushed automatically (Movement `261`).

---

### US-PP-006: Scrap Recording with Mandatory Defect Reason Code
- **Role:** Line Assembly Operator
- **User Story:** As a Line Assembly Operator, I want the system to enforce reason code entry whenever scrap is confirmed so that quality engineering can conduct defect Pareto analysis.
- **Acceptance Criteria:**
  - **AC-01 (Valid Scrap Entry):**
    - *Given* 2 units damaged during optical alignment,
    - *When* the operator enters Scrap = 2 EA and Reason Code `0103` (Photometric Cutoff Failure) in `CO11N`,
    - *Then* the confirmation must post successfully and record reason code `0103` in table `AFRU`.
  - **AC-02 (Missing Reason Code Error):**
    - *Given* Scrap = 2 EA entered with an empty Reason Code field,
    - *When* the operator clicks Save,
    - *Then* the system must block submission with Error `RU 054: Enter a reason for variance`.

---

### US-PP-007: Final Milestone Confirmation and Automatic Finished Goods Receipt
- **Role:** Production Supervisor
- **User Story:** As a Production Supervisor, I want the confirmation of final packaging Operation `0070` to post automatic Goods Receipt (Movement `101`) into finished goods inventory so that finished headlamps are immediately available for customer dispatch.
- **Acceptance Criteria:**
  - **AC-01:**
    - *Given* successful completion of Operation `0070`,
    - *When* the supervisor posts final confirmation in `CO11N` for 98 EA yield,
    - *Then* S/4HANA must generate a Movement Type `101` material document depositing 98 EA of `HL-200X` into storage location `101A`, advance order status to `DLV`, and credit the production order.

---

### US-PP-008: Reprocessing Failed Goods Movements in COGI
- **Role:** Production Supervisor
- **User Story:** As a Production Supervisor, I want to review and reprocess failed backflush movements in transaction `COGI` so that inventory imbalances caused by temporary bin stockouts are corrected without disrupting shop floor confirmations.
- **Acceptance Criteria:**
  - **AC-01:**
    - *Given* a failed goods issue record in table `AFFW` due to missing adhesive stock,
    - *When* the warehouse posts replenishing transfer movement `311` and the supervisor clicks Post in `COGI`,
    - *Then* the error record must be cleared, inventory deducted, and production order costs debited.

---

### US-QM-001: In-Process Quality Inspection Characteristic Recording
- **Role:** Shop Floor Quality Inspector
- **User Story:** As a Shop Floor Quality Inspector, I want to record quantitative photometric lux and hermetic pressure decay test readings against In-Process Inspection Lots (Origin `03`) so that quality compliance is digitally verified before packaging.
- **Acceptance Criteria:**
  - **AC-01:**
    - *Given* an active inspection lot linked to Operation `0050`,
    - *When* the inspector inputs measured lux value `34,500 cd` (specification: 28,000 - 45,000 cd) in `QE51N`,
    - *Then* the system must assign characteristic valuation "Accepted" and display a green indicator.

---

### US-QM-002: Defect Recording and Usage Decision Disposition
- **Role:** Quality Assurance Engineer
- **User Story:** As a Quality Assurance Engineer, I want to record defect codes (`DEF-SEAL-02`) and execute Usage Decisions (`QA11`) so that rejected assemblies are quarantined in Blocked Stock or routed to rework.
- **Acceptance Criteria:**
  - **AC-01:**
    - *Given* 5 headlamps failing leak testing at Operation `0060`,
    - *When* the QA engineer records defect code `DEF-SEAL-02` and posts Usage Decision code `R` (Rejected) in `QA11`,
    - *Then* the system must transfer 5 EA to Blocked Stock `101Q` via Movement Type `350` and generate an internal Quality Notification (Type `F2`).

---

### US-ECM-001: Engineering Change Master and BOM Validity Cutover
- **Role:** Engineering Change Coordinator
- **User Story:** As an Engineering Change Coordinator, I want to create an Engineering Change Master (`CC01`) with Valid-From Date `2026-12-01` and update the `HL-200X` BOM so that replacement fastener `HL-SCR-702` is automatically scheduled for orders starting on or after the cutover date.
- **Acceptance Criteria:**
  - **AC-01:**
    - *Given* Change Master `ECM-2026-088` with Valid-From `2026-12-01`,
    - *When* the BOM is modified in `CS02` referencing the Change Number,
    - *Then* `HL-SCR-701` must show Valid-To `2026-11-30`, `HL-SCR-702` must show Valid-From `2026-12-01`, and Revision Level `B` must be assigned in `CC11`.

---

### US-INT-001: PLM EBOM-to-MBOM Automated Synchronization
- **Role:** CAD / PLM Design Lead
- **User Story:** As a CAD / PLM Design Lead, I want design releases in PLM to trigger automated creation and updating of S/4HANA Manufacturing BOMs via SAP Integration Suite so that engineering handoffs do not require manual spreadsheet transcription.
- **Acceptance Criteria:**
  - **AC-01:**
    - *Given* an approved CAD assembly in PLM,
    - *When* the design engineer marks status "Released for Production",
    - *Then* the middleware must map EBOM attributes, dissolve CAD phantom sub-assemblies, inject manufacturing consumable `HL-ADH-501`, post the MBOM via OData API `API_BILL_OF_MATERIAL_SRV_0002`, and receive an HTTP `201 Created` response.
