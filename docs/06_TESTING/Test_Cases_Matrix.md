# Comprehensive Test Cases Matrix
## SAP S/4HANA Manufacturing, PLM, and Quality Management

**Document Identifier:** `TC-MFG-MAT-001`  
**Author:** Adarsh (Target Role: SAP Manufacturing / Production Planning / PLM Functional Consultant)  
**Process Area:** End-to-End Manufacturing Execution (PP, QM, ECM, Integration)  
**Reference Release:** SAP S/4HANA 2023 / Cloud Private Edition  
**Status:** Approved v1.0 | **Date:** 2 November 2026  
**Linked PRD Deliverable:** Must-Have P0 Test Cases (25 Detailed Test Scripts)  

---

## 1. Test Execution Summary

| Test Category | Total Cases | Target Pass Rate | Linked Scenario IDs |
| :--- | :--- | :--- | :--- |
| **Master Data & Costing** | 5 | 100% | SC-01, SC-02 |
| **Planning & MRP Live** | 3 | 100% | SC-03 |
| **Shop Floor Execution (PP)** | 11 | 100% | SC-04 |
| **Quality Management (QM)** | 3 | 100% | SC-05 |
| **Engineering Change (ECM)** | 2 | 100% | SC-06 |
| **PLM Integration** | 1 | 100% | SC-07 |
| **Total** | **25** | **100%** | **SC-01 through SC-07** |

---

## 2. Detailed Test Scripts

---

### TC-MD-001: Material Master Creation & View Validation
- **Linked Story:** `US-MD-001` | **Linked FRD:** `FR-PP-001` | **Scenario:** SC-01
- **Objective:** Verify creation of finished material `HL-200X` with all required manufacturing, planning, costing, and work scheduling views.
- **Preconditions:** Plant `1010` and Storage Location `101A` active in Customizing.
- **Test Data:** Material `HL-200X`, Type `FERT`, Sector `M`, Base UoM `EA`, Plant `1010`, MRP Type `PD`, Valuation Class `7920`.
- **Execution Steps:**
  1. Open Fiori App *Manage Product Master Data* (`MM01`).
  2. Enter Material Number `HL-200X`, Industry Sector `M`, Material Type `FERT`.
  3. Select views: Basic Data 1/2, MRP 1, 2, 3, 4, Work Scheduling, QM, Accounting 1, Costing 1/2.
  4. Enter organizational levels: Plant `1010`, Storage Location `101A`.
  5. Populate mandatory fields: Net Weight = `1.45 KG`, Strategy `40`, Controller `P01`, Sched. Profile `PP0001`, Price Control `S`, Std Price `INR 4,850.00`.
  6. Click *Save*.
- **Expected Result:** Material `HL-200X` is created successfully. Confirmation message `Material HL-200X created` appears. Tables `MARA`, `MARC`, `MARD`, `MBEW` updated.
- **Status:** Passed | **Pass/Fail Criteria:** All views saved with zero field validation errors.

---

### TC-MD-002: Multi-Level BOM Creation & Recursion Prevention
- **Linked Story:** `US-MD-002` | **Linked FRD:** `FR-PP-006` | **Scenario:** SC-01
- **Objective:** Verify BOM creation with component scrap percentages, backflush flags, and recursion error handling.
- **Preconditions:** Components `HL-HOU-101`, `HL-LENS-201`, `HL-PCB-301`, `HL-ADH-501` active in Plant `1010`.
- **Test Data:** Parent `HL-200X`, Plant `1010`, Usage `1`, Base Qty `1 EA`.
- **Execution Steps:**
  1. Open transaction `CS01`. Enter Material `HL-200X`, Plant `1010`, Usage `1`.
  2. Add Item 0010: `HL-HOU-101`, Qty 1 EA, Item Cat `L`, Scrap `1.5%`.
  3. Add Item 0050: `HL-ADH-501`, Qty 0.045 KG, Item Cat `L`, Scrap `3.0%`.
  4. Negative Test: Add line item with Parent material `HL-200X`.
  5. Press *Enter*.
- **Expected Result:** System generates Error `29 018: Recursive BOM structure detected`. After removing invalid line, BOM saves with active Status `01`. Tables `MAST`, `STKO`, `STPO` populated.
- **Status:** Passed | **Pass/Fail Criteria:** Recursive entry blocked; valid BOM committed.

---

### TC-MD-003: Standard Cost Estimate Rollup & Price Release
- **Linked Story:** `US-MD-003` | **Linked FRD:** `FR-PP-008` | **Scenario:** SC-01
- **Objective:** Verify standard cost calculation across BOM components and routing operations and price marking/release.
- **Preconditions:** BOM and routing active for `HL-200X`; cost center activity prices released in `KP26`.
- **Test Data:** Material `HL-200X`, Plant `1010`, Costing Variant `PPC1`.
- **Execution Steps:**
  1. Open transaction `CK11N`. Enter Material `HL-200X`, Plant `1010`, Costing Variant `PPC1`.
  2. Click *Execute*. Inspect cost component split (Material Costs + Direct Labor + Machine Overhead).
  3. Verify total unit cost equals sum of BOM items and routing operation standard times. Click *Save*.
  4. Open transaction `CK24` (Price Marking & Release). Enter Costing Variant `PPC1`, Material `HL-200X`.
  5. Execute *Marking*, then execute *Release*.
- **Expected Result:** Cost estimate marked and released with status `FR` (Costing released without errors). Table `MBEW-STPRS` updated with released price.
- **Status:** Passed | **Pass/Fail Criteria:** Standard price updated in material master accounting view.

---

### TC-WC-001: Work Center Creation & Capacity Maintenance
- **Linked Story:** `US-WC-001` | **Linked FRD:** `FR-PP-001` | **Scenario:** SC-02
- **Objective:** Verify work center configuration with standard value key `SAP1`, 2-shift capacity, and cost center linkage.
- **Preconditions:** Cost Center `CC-PROD-102` active for Controlling Area `1000`.
- **Test Data:** Work Center `WC-GLUE-03`, Category `0001`, Plant `1010`.
- **Execution Steps:**
  1. Open transaction `CR01`. Enter Plant `1010`, Work Center `WC-GLUE-03`, Category `0001`.
  2. Basic Data tab: Standard Value Key = `SAP1`.
  3. Capacities tab: Category `002` (Machine). Enter Shift: 06:00 to 22:00, 2 shifts, Utilization = `95%`.
  4. Costing tab: Assign Cost Center `CC-PROD-102`, Activity Types `SET`, `MAC`, `LAB`.
  5. Click *Save*.
- **Expected Result:** Work Center `WC-GLUE-03` created. Capacity calculations yield 15.2 net daily productive hours. Tables `CRHD`, `KAKO`, `CRCO` updated.
- **Status:** Passed | **Pass/Fail Criteria:** Capacity and costing formulas link successfully without syntax warnings.

---

### TC-WC-002: Assembly Routing Creation & Component Allocation
- **Linked Story:** `US-WC-002` | **Linked FRD:** `FR-PP-007` | **Scenario:** SC-02
- **Objective:** Verify creation of 7-operation assembly routing and explicit component-to-operation allocation.
- **Preconditions:** Work Centers `WC-ASSY-01` to `WC-PKG-07` active; BOM active.
- **Test Data:** Material `HL-200X`, Plant `1010`, Base Qty `100 EA`.
- **Execution Steps:**
  1. Open transaction `CA01`. Enter Material `HL-200X`, Plant `1010`.
  2. Header: Usage `1`, Status `4` (Released), Base Qty `100 EA`.
  3. Maintain operations 0010 to 0070 with corresponding work centers, standard times, and control keys (`PP01` and `QM01`).
  4. Click *Component Allocation*. Allocate `HL-ADH-501` to Op `0030`, `HL-LENS-201` to Op `0020`, `HL-PKG-801` to Op `0070`.
  5. Click *Save*.
- **Expected Result:** Routing group `50001201` saved. Components locked to designated operations in table `PLAS`/`PLPO`.
- **Status:** Passed | **Pass/Fail Criteria:** Operations saved with valid standard value assignments.

---

### TC-PLN-001: Planned Independent Requirements Maintenance
- **Linked Story:** `US-PLN-001` | **Linked FRD:** `FR-PP-001` | **Scenario:** SC-03
- **Objective:** Verify forecast demand entry under Planning Strategy `40` (Planning with final assembly).
- **Preconditions:** Material master `HL-200X` MRP 3 Strategy Group set to `40`.
- **Test Data:** Material `HL-200X`, Plant `1010`, Version `00`, Monthly Buckets: Month 1 = 500 EA, Month 2 = 600 EA.
- **Execution Steps:**
  1. Open Fiori App *Maintain PIRs* (`MD61`).
  2. Enter Material `HL-200X`, Plant `1010`, Planning Version `00`.
  3. Enter monthly forecast quantities: 500 EA and 600 EA.
  4. Click *Save*.
- **Expected Result:** PIRs committed in table `PBED` with requirement type `VSF`. Displayed in Stock/Requirements list (`MD04`).
- **Status:** Passed | **Pass/Fail Criteria:** Forecast quantities visible in MRP demand horizon.

---

### TC-PLN-002: In-Memory MRP Live Execution & Shortage Detection
- **Linked Story:** `US-PLN-002` | **Linked FRD:** `FR-PP-002` | **Scenario:** SC-03
- **Objective:** Verify MRP Live execution on HANA and generation of multi-level planned orders and purchase requisitions.
- **Preconditions:** Active PIRs for `HL-200X`; zero initial stock on hand.
- **Test Data:** Plant `1010`, Regenerative Planning (`NEUPL`), In-Memory Engine.
- **Execution Steps:**
  1. Open transaction `MD01N` (Schedule MRP Runs). Enter Plant `1010`, Material `HL-200X`.
  2. Select *BOM Explosion: Yes*, *Lead Time Scheduling: Yes*.
  3. Click *Execute*.
  4. Open transaction `MD04` (Stock/Requirements List).
- **Expected Result:** MRP Live completes execution in < 15 seconds. Planned orders generated for `HL-200X` (order type `LA`); purchase requisitions generated for `HL-ADH-501` and fasteners.
- **Status:** Passed | **Pass/Fail Criteria:** In-memory calculation completes without classic MRP fallback.

---

### TC-PLN-003: Planned Order Conversion to Production Order
- **Linked Story:** `US-PLN-003` | **Linked FRD:** `FR-PP-001` | **Scenario:** SC-03
- **Objective:** Verify conversion of planned order to firm production order type `PP01`.
- **Preconditions:** Planned order exists in table `PLAF`.
- **Test Data:** Planned Order Number `0000104820`, Lot Size `100 EA`.
- **Execution Steps:**
  1. Open transaction `MD04` or Fiori App *Manage Planned Orders* (`CO40`).
  2. Select planned order for `HL-200X` and click *Convert to Production Order*.
  3. Verify Order Type `PP01`, Production Plant `1010`.
  4. Click *Save*.
- **Expected Result:** Production Order number generated (e.g. `1000845`). Status set to `CRTD`. Planned order deleted from `PLAF`.
- **Status:** Passed | **Pass/Fail Criteria:** Production order created with matching BOM and routing copied.

---

### TC-PP-001: Production Order Creation & Lead-Time Scheduling
- **Linked Story:** `US-PP-001` | **Linked FRD:** `FR-PP-001` | **Scenario:** SC-04
- **Objective:** Verify manual creation and automated routing lead-time scheduling for 100 units of `HL-200X`.
- **Preconditions:** Material `HL-200X` active in Plant `1010`.
- **Test Data:** Order Type `PP01`, Material `HL-200X`, Quantity `100 EA`, Scheduling Type `Forward`.
- **Execution Steps:**
  1. Open transaction `CO01`. Enter Material `HL-200X`, Plant `1010`, Order Type `PP01`.
  2. Total Quantity = 100 EA. Start Date = Current Date.
  3. Press *Enter* to trigger lead-time scheduling.
  4. Inspect operation tab: verify operation start and finish times across `WC-ASSY-01` to `WC-PKG-07`.
  5. Click *Save*.
- **Expected Result:** Order created with system status `CRTD`. Reservations generated for all 8 BOM components in table `RESB`.
- **Status:** Passed | **Pass/Fail Criteria:** Scheduling calculates realistic finish timestamps using factory calendar.

---

### TC-PP-002: Dynamic Component ATP Availability Check
- **Linked Story:** `US-PP-002` | **Linked FRD:** `FR-PP-002` | **Scenario:** SC-04
- **Objective:** Verify dynamic ATP check against unrestricted stock in storage locations `101B` and `101C`.
- **Preconditions:** Staged stock present for all 8 components in storage locations `101B`/`101C`.
- **Test Data:** Production Order `1000845`.
- **Execution Steps:**
  1. Open transaction `CO02`. Enter Order Number `1000845`.
  2. Click *Check Availability* icon (or menu *Order -> Functions -> Availability -> Check Material*).
  3. Verify ATP confirmation log.
- **Expected Result:** System issues message `All required components are available`. System status updates to `MACM` (Material committed).
- **Status:** Passed | **Pass/Fail Criteria:** Status `MACM` visible in table `JEST`.

---

### TC-PP-003: Order Release Block on Missing Parts
- **Linked Story:** `US-PP-003` | **Linked FRD:** `FR-PP-003` | **Scenario:** SC-04
- **Objective:** Verify hard release blocking when critical component has zero inventory.
- **Preconditions:** Set stock of Bi-LED module `HL-PCB-301` to 0 EA in Plant `1010`. Customizing `OPJK` configured to "Release Block on Missing Parts".
- **Test Data:** Production Order `1000846`.
- **Execution Steps:**
  1. Open transaction `CO02`. Enter Order `1000846`.
  2. Click *Release Order* icon (`REL`).
  3. Inspect system reaction.
- **Expected Result:** System generates Warning/Error dialog: `Order release rejected: Missing parts detected for material HL-PCB-301`. Order remains in status `CRTD` with user status `MSPT`. Release blocked.
- **Status:** Passed | **Pass/Fail Criteria:** Order cannot transition to `REL` while critical part deficit exists.

---

### TC-PP-004: Material Staging & Serialized Goods Issue
- **Linked Story:** `US-PP-004` | **Linked FRD:** `FR-PP-004`, `FR-PP-005` | **Scenario:** SC-04
- **Objective:** Verify manual goods issue of serialized component `HL-PCB-301` to released production order.
- **Preconditions:** Order `1000845` in status `REL`; 100 units of `HL-PCB-301` available in `101B` with serial numbers.
- **Test Data:** Material `HL-PCB-301`, Qty `100 EA`, Movement Type `261`, Order `1000845`.
- **Execution Steps:**
  1. Open transaction `MIGO`. Select *Goods Issue -> Order*.
  2. Enter Order `1000845`, Material `HL-PCB-301`, Storage Location `101B`.
  3. Click *Serial Numbers* tab. Select 100 valid serial numbers.
  4. Click *Check*, then click *Post*.
- **Expected Result:** Material document posted. Stock deducted from `101B`. Actual costs debited to order. Reservation updated to `Final Issue`.
- **Status:** Passed | **Pass/Fail Criteria:** Table `MSEG` created with movement 261; serial numbers linked in table `OBJK`.

---

### TC-PP-005: Milestone Operation Confirmation Op 0050
- **Linked Story:** `US-PP-005` | **Linked FRD:** `FR-PP-007` | **Scenario:** SC-04
- **Objective:** Verify milestone confirmation of Operation `0050` automatically confirms preceding operations 0010 to 0040.
- **Preconditions:** Production Order `1000845` released (`REL`).
- **Test Data:** Order `1000845`, Operation `0050`, Yield `98 EA`, Scrap `2 EA`.
- **Execution Steps:**
  1. Open transaction `CO11N`. Enter Order `1000845`, Operation `0050`.
  2. Enter Yield = 98 EA, Scrap = 2 EA, Reason = `0103`.
  3. Enter actual machine time = 58 min, labor time = 59 min.
  4. Click *Save*.
  5. Inspect Operation tab in `CO02`.
- **Expected Result:** Confirmation posted in table `AFRU`. Operations 0010, 0020, 0030, and 0040 show status `CNF`. Order status updates to `PCNF`.
- **Status:** Passed | **Pass/Fail Criteria:** Preceding operations confirmed proportionally without manual operator entry.

---

### TC-PP-006: Automated Backflush of Assembly Consumables
- **Linked Story:** `US-PP-005` | **Linked FRD:** `FR-PP-006` | **Scenario:** SC-04
- **Objective:** Verify automated Movement Type `261` backflushing of PUR adhesive and fasteners during milestone confirmation.
- **Preconditions:** BOM items for `HL-ADH-501` and `HL-SCR-701` flagged with Backflush Indicator `1`.
- **Test Data:** Operation `0050` confirmation for 98 EA yield.
- **Execution Steps:**
  1. Confirm Operation `0050` as executed in `TC-PP-005`.
  2. Open transaction `CO03` (Display Order) -> *Goto -> Documented Goods Movements*.
  3. Inspect material documents.
- **Expected Result:** System automatically posts Movement Type `261` for PUR adhesive `HL-ADH-501` (4.545 KG deducted from `101C`) and fasteners `HL-SCR-701` (606 EA deducted from `101C`).
- **Status:** Passed | **Pass/Fail Criteria:** Goods movement documents exist in table `MSEG` referencing confirmation document.

---

### TC-PP-007: Scrap Recording with Mandatory Reason Code Enforcement
- **Linked Story:** `US-PP-006` | **Linked FRD:** `FR-PP-009` | **Scenario:** SC-04
- **Objective:** Verify that entering scrap without a valid reason code is blocked by system validation.
- **Preconditions:** Order `1000845` active.
- **Test Data:** Operation `0030`, Scrap = 3 EA, Reason Code = Blank.
- **Execution Steps:**
  1. Open transaction `CO11N`. Enter Order `1000845`, Operation `0030`.
  2. Enter Yield = 95 EA, Scrap = 3 EA. Leave Reason for Variance blank.
  3. Click *Save*.
- **Expected Result:** System rejects transaction with Error `RU 054: Enter a reason for variance`. Confirmation is not saved.
- **Status:** Passed | **Pass/Fail Criteria:** Save blocked until a valid reason code (e.g. `0102`) is entered.

---

### TC-PP-008: Scrap Tolerance Threshold (> 3%) Supervisor Lockout
- **Linked Story:** `US-PP-006` | **Linked FRD:** `FR-PP-010` | **Scenario:** SC-04
- **Objective:** Verify that scrap exceeding 3.0% requires supervisor authorization object `C_AFKO_AWA`.
- **Preconditions:** Operator user role without supervisor authorization logged in.
- **Test Data:** Operation `0040`, Yield = 90 EA, Scrap = 10 EA (10.0% scrap).
- **Execution Steps:**
  1. In `CO11N`, enter Scrap = 10 EA, Reason = `0102` (Adhesive Void).
  2. Attempt to save as standard operator.
  3. Switch to supervisor user with authorization `C_AFKO_AWA` and attempt save.
- **Expected Result:** Operator save blocked with Authorization Error. Supervisor save prompts QM warning, generates Defect Notification `F2`, and commits transaction.
- **Status:** Passed | **Pass/Fail Criteria:** Hard authorization gatekeeper prevents unapproved excessive scrap.

---

### TC-PP-009: Final Milestone Confirmation Op 0070
- **Linked Story:** `US-PP-007` | **Linked FRD:** `FR-PP-007` | **Scenario:** SC-04
- **Objective:** Verify confirmation of final packaging Operation `0070` and auto-confirmation of preceding leak test Op 0060.
- **Preconditions:** Milestone Op 0050 confirmed.
- **Test Data:** Order `1000845`, Operation `0070`, Yield = 98 EA.
- **Execution Steps:**
  1. Open transaction `CO11N`. Enter Order `1000845`, Operation `0070`.
  2. Enter Yield = 98 EA. Check *Final Confirmation* flag.
  3. Click *Save*.
- **Expected Result:** Operation `0060` and `0070` confirmed. Status advances to `CNF`.
- **Status:** Passed | **Pass/Fail Criteria:** All operations across routing show status `CNF`.

---

### TC-PP-010: Automated Finished Goods Receipt Movement 101
- **Linked Story:** `US-PP-007` | **Linked FRD:** `FR-PP-011` | **Scenario:** SC-04
- **Objective:** Verify automated posting of Movement Type `101` into Storage Location `101A` upon final confirmation.
- **Preconditions:** Control key for Op `0070` configured with Automatic Goods Receipt (`AUTGR`).
- **Test Data:** Order `1000845`, Final Confirmation posted.
- **Execution Steps:**
  1. Inspect documented goods movements in `CO03` or open `MMBE` for material `HL-200X`.
  2. Check Storage Location `101A`.
- **Expected Result:** S/4HANA automatically generates Movement Type `101` material document for 98 EA. Unrestricted stock in `101A` increases by 98 EA. Order status set to `DLV`.
- **Status:** Passed | **Pass/Fail Criteria:** Order status reflects `DLV`; finished stock available in `101A`.

---

### TC-PP-011: Postprocessing Failed Goods Movements in COGI
- **Linked Story:** `US-PP-008` | **Linked FRD:** `FR-PP-012` | **Scenario:** SC-04
- **Objective:** Verify logging of backflush inventory shortfall in COGI and successful reprocessing after stock replenishment.
- **Preconditions:** Temporary stock deficit created for adhesive `HL-ADH-501`.
- **Test Data:** Failed backflush entry in table `AFFW`.
- **Execution Steps:**
  1. Post operation confirmation in `CO11N`. System confirms operation but logs backflush deficit warning.
  2. Open transaction `COGI`. Verify failed movement line item with error `M7 021`.
  3. Post replenishing transfer posting (`MIGO` Mov `311`) transferring 5 KG of adhesive into `101C`.
  4. In `COGI`, select the error record and click *Post*.
- **Expected Result:** System successfully posts Movement Type `261`. The error record is removed from `COGI`/`AFFW`. Order costs debited.
- **Status:** Passed | **Pass/Fail Criteria:** Failed movement cleared from queue with zero remaining errors.

---

### TC-PP-012: Production Order Technical Completion (TECO)
- **Linked Story:** `US-PP-001` | **Linked FRD:** `FR-PP-015` | **Scenario:** SC-04
- **Objective:** Verify setting Technical Completion (`TECO`), cancellation of open reservations, and release of capacities.
- **Preconditions:** Order `1000845` fully confirmed and delivered (`CNF DLV`).
- **Test Data:** Order `1000845`.
- **Execution Steps:**
  1. Open transaction `CO02`. Enter Order `1000845`.
  2. Select menu *Order -> Functions -> Restrict Processing -> Technically Complete*.
  3. Click *Save*.
  4. Inspect open reservations in table `RESB`.
- **Expected Result:** System status updates to `TECO`. All open component reservations flagged for deletion (`RESB-KNTTP`). Capacity load removed from work centers.
- **Status:** Passed | **Pass/Fail Criteria:** Status `TECO` active; order locked against further goods movements.

---

### TC-QM-001: In-Process QM Lot 03 Generation & Results Recording
- **Linked Story:** `US-QM-001` | **Linked FRD:** `FR-PP-013` | **Scenario:** SC-05
- **Objective:** Verify generation of In-Process Inspection Lot (Origin `03`) and recording of quantitative photometric readings.
- **Preconditions:** Routing Operation `0050` assigned Control Key `QM01`; Inspection Type `03` active in material master QM view.
- **Test Data:** Lot Origin `03`, Measured Lux = `34,500 cd` (Spec: 28,000 - 45,000 cd).
- **Execution Steps:**
  1. Release production order. S/4HANA automatically creates Inspection Lot Origin `03`.
  2. Open transaction `QE51N` (Record Results). Enter Inspection Lot number.
  3. Select Characteristic `MIC-OPT-01` (Luminous Intensity). Enter actual value `34500`.
  4. Press *Enter* to evaluate.
  5. Click *Save*.
- **Expected Result:** System assigns valuation status "Accepted" (green flag). Tables `QALS` and `QASR` updated.
- **Status:** Passed | **Pass/Fail Criteria:** Measured value recorded; lot valuation compliant with engineering tolerance.

---

### TC-QM-002: Defect Recording & Quality Notification Creation
- **Linked Story:** `US-QM-002` | **Linked FRD:** `FR-PP-009`, `FR-PP-013` | **Scenario:** SC-05
- **Objective:** Verify recording defect code `DEF-SEAL-02` (Adhesive Void) and automated creation of Quality Notification Type `F2`.
- **Preconditions:** Active inspection lot for Operation `0060` (Pressure Decay Leak Test).
- **Test Data:** Leak rate measured = `0.85 sccm` (Tolerance: <= 0.50 sccm), Defect Code `DEF-SEAL-02`, Defect Qty `3 EA`.
- **Execution Steps:**
  1. In `QE51N`, record measured leak rate `0.85`. Characteristic evaluated as "Rejected" (red flag).
  2. Click *Record Defects* (or open Fiori App *Record Defects* `F2929`).
  3. Select Defect Code `DEF-SEAL-02` (Seal Void), Defect Quantity = 3 EA.
  4. Click *Save*.
- **Expected Result:** System generates Quality Notification Type `F2` (Internal Problem Notification). Defect record saved in table `QMFE`/`QMEL`.
- **Status:** Passed | **Pass/Fail Criteria:** Defect notification created with link to inspection lot and production order.

---

### TC-QM-003: Usage Decision Rejection & Stock Transfer to Blocked Stock
- **Linked Story:** `US-QM-002` | **Linked FRD:** `FR-PP-013` | **Scenario:** SC-05
- **Objective:** Verify Usage Decision rejection (Code `R`) and automated transfer of defective units to Blocked Stock `101Q` via Movement `350`.
- **Preconditions:** Inspection lot contains rejected characteristics.
- **Test Data:** Inspection Lot with 5 defective units, UD Code `R` (Reject).
- **Execution Steps:**
  1. Open transaction `QA11` (Record Usage Decision). Enter Inspection Lot number.
  2. Enter UD Code = `R` (Rejected).
  3. In *Inspection Lot Stock* tab, enter 5 EA under *To Blocked Stock*. Storage Location = `101Q`.
  4. Click *Save*.
- **Expected Result:** Usage Decision committed. S/4HANA automatically posts Movement Type `350`, moving 5 EA to Blocked Stock `101Q`. Finished stock release prevented.
- **Status:** Passed | **Pass/Fail Criteria:** Units quarantined in `101Q`; table `MSEG` created with movement 350.

---

### TC-ECM-001: Engineering Change Master & BOM Validity Cutover
- **Linked Story:** `US-ECM-001` | **Linked FRD:** `FR-PP-014` | **Scenario:** SC-06
- **Objective:** Verify ECM creation, BOM versioning with Valid-From date, and Revision Level assignment.
- **Preconditions:** Replacement component `HL-SCR-702` created in Plant `1010`.
- **Test Data:** Change Number `ECM-2026-088`, Valid-From `2026-12-01`, Revision Level `B`.
- **Execution Steps:**
  1. Open transaction `CC01`. Create Change Master `ECM-2026-088`, Valid-From `2026-12-01`. Activate object types: Material, BOM, Routing.
  2. Open transaction `CS02`. Enter Material `HL-200X`, Plant `1010`, Change Number `ECM-2026-088`.
  3. Set Valid-To for `HL-SCR-701` to `2026-11-30`. Add replacement `HL-SCR-702` with Valid-From `2026-12-01`. Click *Save*.
  4. Open transaction `CC11`. Assign Revision Level `B` to `HL-200X` linked to `ECM-2026-088`.
- **Expected Result:** BOM shows date-effective split in table `STPO`. Material master displays Revision Level `B`.
- **Status:** Passed | **Pass/Fail Criteria:** Validity dates segmented correctly without data overwrites.

---

### TC-INT-001: PLM EBOM-to-MBOM Automated Interface & AIF Exception
- **Linked Story:** `US-INT-001` | **Linked FRD:** `FR-PP-001`, `FR-PP-014` | **Scenario:** SC-07
- **Objective:** Verify inbound OData API payload processing, automated consumable injection, and AIF dead-letter queue error handling.
- **Preconditions:** SAP Integration Suite OData communication channel configured.
- **Test Data:** Outbound JSON payload with parent `HL-200X`, 5 CAD child items, and test invalid UoM `INCHES`.
- **Execution Steps:**
  1. Trigger mock webhook payload containing invalid UoM `INCHES`.
  2. Inspect response: HTTP `422 Unprocessable Entity`.
  3. Open S/4HANA transaction `/AIF/ERR` (Message Monitoring). Verify trapped message in error queue.
  4. Correct value mapping in middleware (`INCHES` -> `INH`) and click *Restart Message* in AIF.
  5. Inspect BOM in `CS03`.
- **Expected Result:** Message reprocessed successfully (HTTP `201 Created`). S/4HANA MBOM updated with child components and injected PUR adhesive `HL-ADH-501`.
- **Status:** Passed | **Pass/Fail Criteria:** Payload ingested, consumables injected, and error cleared from AIF queue.
