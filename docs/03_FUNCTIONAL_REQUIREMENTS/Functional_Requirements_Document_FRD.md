# Functional Requirements Document (FRD)
## Production Order Execution and Confirmation in SAP S/4HANA

**Document Identifier:** `FRD-MFG-PP-001`  
**Author:** Adarsh (Target Role: SAP Manufacturing / Production Planning / PLM Functional Consultant)  
**Process Area:** SAP S/4HANA Production Planning & Shop Floor Execution (PP-SFC)  
**Reference Release:** SAP S/4HANA 2023 / Cloud Private Edition  
**Status:** Approved v1.0 | **Date:** 2 November 2026  
**Linked PRD Deliverable:** Must-Have P0 Functional Requirements Document (FRD)  

---

## 1. Document Overview & Scope

This Functional Requirements Document (FRD) specifies the system configuration, functional logic, data validations, and operational behavior for **Production Order Execution and Confirmation** within SAP S/4HANA. 

The scope covers the full execution lifecycle of discrete assembly orders for the **Bi-LED Headlamp Assembly (`HL-200X`)** in Plant `1010`, including:
- Production order creation, scheduling, and dynamic component availability checking.
- Order release governance and line-side material staging.
- Manual goods issues (Movement `261`) and automated backflushing of consumables.
- Milestone operation confirmations, actual labor/machine activity recording, and scrap tracking.
- Automatic Goods Receipt (Movement `101`) upon final assembly completion.
- Integrated touchpoints with **Quality Management (QM)** for in-process inspection lots and **Engineering Change Management (ECM)** for WIP revision cutovers.

---

## 2. Functional Requirements Matrix

| Req ID | Requirement Title | Category | Priority | Linked User Story | S/4HANA Fiori App / GUI Code | Key Table(s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FR-PP-001** | Production Order Creation & Scheduling | Execution | Must-Have | `US-PP-001`, `US-PP-004` | `Manage Production Orders` / `CO01` | `AFKO`, `AFPO` |
| **FR-PP-002** | Dynamic Component ATP Check | Inventory | Must-Have | `US-PP-002` | `Change Production Order` / `CO02` | `RESB`, `MARD` |
| **FR-PP-003** | Order Release Governance & Blocking | Control | Must-Have | `US-PP-003` | `Release Production Order` / `CO02` | `JEST`, `JCDS` |
| **FR-PP-004** | Line-Side Material Staging | Logistics | Must-Have | `US-PP-005` | `Post Goods Movement` / `MIGO` | `MSEG`, `MKPF` |
| **FR-PP-005** | High-Value Component Serialized Issue | Traceability | Must-Have | `US-PP-006` | `Post Goods Movement` / `MIGO` | `MSEG`, `OBJK`, `EQUI` |
| **FR-PP-006** | Consumable Automated Backflushing | Logistics | Must-Have | `US-PP-007` | `Confirm Operation` / `CO11N` | `AFRU`, `MSEG` |
| **FR-PP-007** | Milestone Operation Confirmation | Execution | Must-Have | `US-PP-008` | `Confirm Operation` / `CO11N` | `AFRU`, `AFVV` |
| **FR-PP-008** | Actual Activity & Labor Cost Capture | Costing | Must-Have | `US-PP-009` | `Confirm Operation` / `CO11N` | `AFRU`, `COSS` |
| **FR-PP-009** | Shop Floor Scrap Reason Mandatory Entry | Quality | Must-Have | `US-PP-010` | `Confirm Operation` / `CO11N` | `AFRU`, `T007A` |
| **FR-PP-010** | Scrap Tolerance & Supervisor Lockout | Control | Should-Have | `US-PP-011` | `Confirm Operation` / `CO11N` | `AFRU`, Custom BAdI |
| **FR-PP-011** | Automatic Finished Goods Receipt (101) | Inventory | Must-Have | `US-PP-012` | `Confirm Operation` / `CO11N` | `MSEG`, `MKPF` |
| **FR-PP-012** | Failed Goods Movements Workbench (COGI)| Exception | Must-Have | `US-PP-013` | `Postprocessing Failed Goods` / `COGI`| `AFFW` |
| **FR-PP-013** | In-Process QM Lot Synchronization | Quality | Must-Have | `US-QM-001`, `US-QM-002` | `Record Results` / `QE51N` | `QALS`, `QAMV` |
| **FR-PP-014** | In-Flight ECM Cutover & Master Data Re-Read| PLM / ECM | Must-Have | `US-ECM-001`, `US-ECM-002`| `Change Production Order` / `CO02` | `AFKO`, `RESB`, `AENR`|
| **FR-PP-015** | Order Technical Completion (TECO) | Financial | Must-Have | `US-PP-014`, `US-PP-015` | `Change Production Order` / `CO02` | `AFKO`, `JEST` |

---

## 3. Detailed Functional Specifications

### FR-PP-001: Production Order Creation & Lead-Time Scheduling
- **Description:** The system shall create discrete production orders of order type `PP01` for material `HL-200X` in Plant `1010` either via manual entry in Fiori App `Manage Production Orders` (`CO01`) or via automated conversion of planned orders (`CO40`).
- **Functional Logic:**
  - Order type `PP01` automatically copies the active Production BOM (Usage `1`) and routing group `50001201`.
  - Lead-time scheduling determines planned start and finish dates using routing standard values (setup, machine, labor) and work center factory calendar (Plant `1010`).
  - System generates reservations (`RESB`) for all 8 BOM items.
- **Validation Rules:**
  - Planned order conversion must verify that the material is not flagged with a plant deletion indicator (`MARC-LVORM`).
  - Scheduling type must default to `1` (Forward) or `2` (Backward) based on production scheduling profile `PP0001`.

### FR-PP-002: Dynamic Available-to-Promise (ATP) Check
- **Description:** The system shall execute a dynamic component availability check against current unrestricted stock and scheduled receipts before an order can be released to the floor.
- **Functional Logic:**
  - Checking rule `PP` (Production Order) verifies stock in storage locations `101B` and `101C`.
  - Checks consider safety stock thresholds and open reservations for earlier scheduled production orders.
- **System Action:**
  - If any component is unavailable, the order status is updated with system status `MSPT` (Missing Part) and user status `HOLD_MAT`.
  - Missing parts list is compiled and viewable in `CO02` -> *Goto -> Missing Parts*.

### FR-PP-003: Order Release Governance & Hard Blocking
- **Description:** The system shall strictly control transition from status `CRTD` (Created) to `REL` (Released).
- **Functional Logic:**
  - In Customizing (`OPJK`), the check control is configured to **Block Release** if critical components (such as LED module `HL-PCB-301` or Projector lens `HL-LENS-201`) have missing parts.
  - Release triggers the activation of component reservations, enabling warehouse transfer orders.
  - Generates shop floor traveler documents containing 2D DataMatrix barcodes encoding Order ID, Material Number, and Operation sequence.

### FR-PP-004: Line-Side Material Staging
- **Description:** Components required for assembly operations must be staged from central warehouse storage locations to line-side picking bins (`101B` for sub-assemblies, `101C` for fasteners/chemicals).
- **Functional Logic:**
  - Planners execute staging using Transfer Postings (`MIGO` Movement Type `311` - Transfer within Plant).
  - Material reservations reflect line-side storage locations configured in BOM item master data.

### FR-PP-005: High-Value Component Serialized Goods Issue
- **Description:** Bi-LED driver module `HL-PCB-301` must be issued to the production order with individual serial number verification.
- **Functional Logic:**
  - Movement Type `261` (Goods Issue for Order) is executed via `MIGO`.
  - The system enforces entry of serial numbers corresponding to table `EQUI`. Unregistered or duplicate serial numbers are rejected with Error `IO 201`.
  - Updates table `MSEG` with material document and links serial records in `OBJK`.

### FR-PP-006: Consumable Automated Backflushing
- **Description:** Low-value, high-velocity components (fasteners `HL-SCR-701`, EPDM gaskets `HL-GSK-601`, PUR adhesive `HL-ADH-501`, shipping cartons `HL-PKG-801`) shall be backflushed automatically upon operation confirmation.
- **Functional Logic:**
  - Backflush Indicator is set to `1` (Always backflush) in BOM items (`STPO-RGEKZ`).
  - When Operation `0050` or `0070` is confirmed in `CO11N`, S/4HANA automatically generates Movement Type `261` postings for associated components.
  - Quantities consumed = `Confirmed Yield * BOM Base Component Qty * (1 + Component Scrap % / 100)`.

### FR-PP-007: Milestone Operation Confirmation Architecture
- **Description:** The assembly routing contains 7 operations. Operation `0050` (In-Process Photometric Darkroom Test) and Operation `0070` (Packaging) are configured as **Milestones** using Control Key `PP01` / `QM01`.
- **Functional Logic:**
  - Confirming milestone Operation `0050` automatically confirms all preceding non-milestone operations (`0010`, `0020`, `0030`, `0040`) proportionally.
  - Operators are prevented from skipping Operation `0050` to confirm Operation `0070`.
  - System status transitions to `PCNF` (Partially Confirmed) or `CNF` (Confirmed).

```
[Op 0010: Prep] ----+
[Op 0020: Optics] --+---> [Op 0050: Photometric Test] (MILESTONE 1)
[Op 0030: Glue] ----+          * Auto-confirms Op 0010-0040
[Op 0040: Cure] ----+          * Triggers auto-backflush of sub-assemblies

[Op 0060: Leak Test] ---> [Op 0070: Final Pack] (MILESTONE 2)
                               * Auto-confirms Op 0060
                               * Triggers auto-backflush of packaging
                               * Triggers automated 101 Goods Receipt
```

### FR-PP-008: Actual Activity & Labor Cost Capture
- **Description:** Operation confirmation shall capture actual machine and labor hours worked, recording direct costs against production cost centers.
- **Functional Logic:**
  - Confirmation screen `CO11N` prompts for:
    - Setup Time (Minutes)
    - Machine Time (Minutes)
    - Labor Time (Minutes)
  - Cost calculation: `Actual Hours * Standard Activity Price (KP26)`.
  - Actual costs posted to Cost Center `CC-PROD-101` / `CC-PROD-102` and debited to the production order cost collector (`COSS`/`COSP`).

### FR-PP-009: Shop Floor Scrap Reason Mandatory Entry
- **Description:** Any scrap recorded during operation confirmation must require a valid reason code.
- **Functional Logic:**
  - If field `AFRU-LMNGA` (Scrap Quantity) > `0`, field `AFRU-GRUND` (Reason for Variance/Scrap) becomes mandatory.
  - Reason codes correspond to shop floor defect categories:
    - `0101`: Lens Scratch / Coating Blemish
    - `0102`: Adhesive Bead Gap / Seal Void
    - `0103`: Photometric Cutoff / Lux Failure
    - `0104`: Harness Terminal Pin Disengagement
    - `0105`: Fastener Stripping / Over-Torque Boss Failure
  - Submitting scrap without a reason code generates Error `RU 054: Enter a reason for variance`.

### FR-PP-010: Scrap Tolerance Threshold & Quality Supervisor Lockout
- **Description:** If scrap entered on an operation exceeds 3.0% of the operation batch quantity, the confirmation shall trigger an administrative quality lockout.
- **Functional Logic:**
  - Enforced via confirmation enhancement (BAdI `WORKORDER_CONFIRM`).
  - If `Scrap Qty / (Yield Qty + Scrap Qty) > 0.03`:
    - System issues a high-priority warning dialog.
    - System automatically generates an S/4HANA QM Defect Notification (Type `F2`).
    - Save action requires authorization object `C_AFKO_AWA` (Plant Production Supervisor authorization).
    - If the user lacks authorization, confirmation save is blocked.

### FR-PP-011: Automatic Finished Goods Receipt (Movement 101)
- **Description:** Upon final confirmation of Operation `0070`, the system shall automatically post Goods Receipt into Finished Goods inventory.
- **Functional Logic:**
  - Control key for Operation `0070` is configured with **Automatic Goods Receipt** flag (`T430-AUTGR`).
  - System executes Movement Type `101` (Goods Receipt for Production Order).
  - Material is deposited into Storage Location `101A` (Finished Goods).
  - Production order status advances to `DLV` (Delivered).
  - Material valuation: Stock account debited, Production Order credit offset posted (`BSX` / `GBB-AUF`).

### FR-PP-012: Failed Goods Movements Reprocessing Workbench (COGI)
- **Description:** In the event of inventory discrepancies during backflushing (e.g. temporary stock shortfall of PUR adhesive `HL-ADH-501`), the operation confirmation must succeed while logging the failed movement in the postprocessing error queue (`COGI`).
- **Functional Logic:**
  - System logs failed line items in table `AFFW`.
  - Supervisor accesses transaction `COGI` (or Fiori App *Postprocessing of Goods Movements*).
  - Displays explicit error message (e.g. `M7 021: Deficit of SL Unrestricted-use 0.450 KG`).
  - Once warehouse clerk posts replenishing stock transfer (`MIGO` Mov `311`), supervisor selects record and clicks **Post** to clear the error.

### FR-PP-013: In-Process QM Lot Synchronization
- **Description:** Orders containing operations with control key `QM01` (Op `0050` and Op `0060`) shall link dynamically to QM inspection lots.
- **Functional Logic:**
  - S/4HANA generates an In-Process Inspection Lot (Origin `03`) upon order release.
  - Inspection characteristics (lux measurement, pressure drop) must be recorded in Fiori App `Record Results` (`QE51N`).
  - If results are rejected, the lot status prevents order closure until a formal Usage Decision (`QA11`) is posted.

### FR-PP-014: In-Flight ECM Cutover & Master Data Re-Read
- **Description:** When an engineering change (`ECM-2026-088`) is released with an immediate effectivity date, production orders currently in status `CRTD` or `REL` (with zero confirmations) must support automated BOM re-reading.
- **Functional Logic:**
  - Supervisor selects *Functions -> Read Master Data* in `CO02`.
  - S/4HANA evaluates the Valid-From date against the order scheduled start date.
  - Cancels old reservations for discontinued item `HL-SCR-701` and creates active reservations for replacement item `HL-SCR-702`.
  - Updates order header with the new Revision Level `B`.

### FR-PP-015: Order Technical Completion (TECO) & Variance Settlement
- **Description:** When assembly operations and goods receipts are concluded, the order must be set to Technical Completion (`TECO`).
- **Functional Logic:**
  - Sets system status `TECO` (`JEST`).
  - Deletes open component reservations (`RESB`) and releases remaining work center capacity allocations (`KBED`).
  - Locks order against further operational postings (confirmation or goods issue).
  - Allows financial variance calculation (`KKS2`) and order cost settlement (`KO88`).

---

## 4. Status Progression Lifecycle & System Status Matrix

```
  +---------+
  |  CRTD   |  Created: BOM/Routing copied, reservations inactive.
  +----+----+
       |  Availability Check (ATP Pass)
       v
  +----+----+
  |   REL   |  Released: Reservations active, traveler printed, staging allowed.
  +----+----+
       |  Milestone Confirmation (Op 0050)
       v
  +----+----+
  |  PCNF   |  Partially Confirmed: Auto-backflushed Op 0010-0040.
  +----+----+
       |  Final Confirmation (Op 0070)
       v
  +----+----+
  |CNF / DLV|  Confirmed & Delivered: Auto GR 101 into Loc 101A.
  +----+----+
       |  Technical Completion (CO02)
       v
  +----+----+
  |  TECO   |  Technically Completed: Open reservations cleared, ready for costing.
  +----+----+
       |  Financial Variance Settlement (KO88)
       v
  +----+----+
  |  CLSD   |  Closed: Balance = 0, archived.
  +---------+
```

---

## 5. Security & Authorization Matrix

| Business Role | SAP Auth Object | Allowed Activities / T-Codes | Restriction / Scope |
| :--- | :--- | :--- | :--- |
| **Production Supervisor** | `C_AFKO_ATY`, `C_AFKO_AWA` | `CO01`, `CO02`, `CO05N`, `COGI` | Plant `1010`, Order Type `PP01`. Full release & supervisor scrap override. |
| **Line Assembly Operator** | `C_AFRU_APO`, `C_AFRU_AWK` | `CO11N`, `Fiori Confirm Operation` | Plant `1010`, Work Centers `WC-ASSY-01` to `WC-PKG-07`. Confirmation only. |
| **Warehouse Handler** | `M_MATE_STA`, `M_MSEG_BWA` | `MIGO` (Mov 261, 311, 262) | Plant `1010`, Storage Locations `101B`, `101C`, `101D`. |
| **Quality Inspector** | `Q_INSP_LOT`, `Q_CHAR_RES` | `QA32`, `QE51N`, `F2929`, `QA11` | Plant `1010`, Insp Type `03`, `04`. Result recording & UD. |
