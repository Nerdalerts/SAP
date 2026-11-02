# Functional Specification: Shop Floor Defect Pareto Analytics
## Custom Fiori Analytical App / CDS View for Quality Intelligence

**Document Identifier:** `FS-QM-REP-001`  
**Author:** Adarsh (Target Role: SAP Manufacturing / Production Planning / PLM Functional Consultant)  
**Process Area:** Quality Management (QM) & Operational Analytics  
**Reference Release:** SAP S/4HANA 2023 / Cloud Private Edition  
**Status:** Approved v1.0 | **Date:** 2 November 2026  
**Linked PRD Deliverable:** Nice-to-Have P1 Functional Design Specification (Reflecting Shop-Floor Defect Analysis)  

---

## 1. Business Context & Problem Statement

During high-volume automotive headlamp assembly, quality defects compound rapidly if systemic issues are not recognized and mitigated within the shift. In pre-SAP environments (such as typical tier-1 automotive manufacturing plants), defect tally marks are collected on paper clipboards and analyzed manually in Excel or Python days later.

This Functional Specification defines a standard **S/4HANA Fiori Analytical Application (Smart Business KPI / Analytical List Page)** based on Core Data Services (CDS) Views. It computes real-time 80/20 Pareto distributions of shop floor defects across work centers, defect categories, component batches, and shifts.

---

## 2. Business Objectives & Key Performance Indicators

- **Identify the Critical 20%:** Isolate root causes responsible for 80% of total assembly line scrap (e.g. photometric lux failures vs. adhesive bead voids).
- **Real-Time Drill-Down:** Enable Quality Engineers and Production Supervisors to drill from high-level plant defect trends down to specific production orders, operations, inspection lots, and resin batches.
- **Containment Speed:** Reduce containment decision time for defective batches from 48 hours to under 30 minutes.

---

## 3. Shop Floor Defect Catalog & Historical Distribution

Based on actual assembly line failure modes in automotive lighting:

| Defect Code | Defect Description | Category | Severity | Frequency (%) | Cumulative (%) | Primary Work Center |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `DEF-OPT-01` | Luminous Intensity Below Spec (< 28,000 cd) | Optical / Photometric | Critical | 34.2% | 34.2% | `WC-TST-05` (Darkroom) |
| `DEF-SEAL-02`| Sealant Bead Void / Continuous Gap | Mechanical Sealing | Critical | 26.5% | 60.7% | `WC-GLUE-03` (Robotic Dispenser) |
| `DEF-FOG-03` | Inner Polycarbonate Lens Fogging / Moisture | Environmental | Major | 18.7% | 79.4% | `WC-LEAK-06` (Leak Test) |
| `DEF-HAR-04` | Harness Terminal Pin Disengagement | Electrical | Major | 11.4% | 90.8% | `WC-ASSY-01` (Mechanical Cell) |
| `DEF-SCR-05` | Fastener Stripping / Over-Torque Boss Fracture| Assembly | Minor | 5.8% | 96.6% | `WC-OPT-02` (Optical Cell) |
| `DEF-VIS-06` | Cosmetic Blemish / Anti-Fog Coating Scratch | Visual Cosmetic | Minor | 3.4% | 100.0% | `WC-PKG-07` (Packaging) |

*Insight:* The top 3 defect codes (`DEF-OPT-01`, `DEF-SEAL-02`, and `DEF-FOG-03`) account for **79.4% (~80%)** of all shop floor rejections, confirming the 80/20 Pareto rule.

---

## 4. Technical Architecture: Core Data Services (CDS) View

The analytical application reads directly from standard S/4HANA Quality Notification and Defect tables (`QMFE`, `QMEL`, `QALS`, `AFKO`) via an optimized CDS view stack:

```
[UI5 / Fiori Elements Analytical List Page: C_DefectParetoAnalytics]
                               |
                               | OData v4 Analytical Query
                               v
           [CDS Analytical Query: C_DefectParetoQuery]
                               |
                               v
            [CDS Composite Cube: I_DefectAnalysisCube]
            (Joins QMFE, QMEL, QALS, AFKO, MARC, AFRU)
                               |
                               v
                 [SAP S/4HANA Database Tables]
```

### CDS Cube Definition (ABAP CDS Pseudocode)

```sql
@AbapCatalog.sqlViewName: 'ZV_DEF_PARETO'
@AbapCatalog.compiler.compareFilter: true
@AccessControl.authorizationCheck: #CHECK
@EndUserText.label: 'Defect Pareto Analytics Cube'
@Analytics.dataCategory: #CUBE

define view ZI_DefectParetoCube
  as select from qmfe as DefectItem
  inner join qmel as Notification on DefectItem.qmnum = Notification.qmnum
  inner join qals as InspLot      on Notification.prueflos = InspLot.prueflos
  left outer join afko as ProdOrder on InspLot.aufnr = ProdOrder.aufnr
{
  key DefectItem.qmnum          as QualityNotification,
  key DefectItem.fenum          as DefectItemNumber,
      
      // Dimensions
      Notification.werk         as Plant,
      Notification.matnr        as MaterialNumber,
      Notification.aufnr        as ProductionOrder,
      DefectItem.fecod          as DefectCode,
      DefectItem.fegrp          as DefectCodeGroup,
      DefectItem.erdat          as DefectCreatedDate,
      InspLot.vornr             as OperationNumber,
      InspLot.arbpl             as WorkCenter,
      
      // Measures
      @DefaultAggregation: #SUM
      DefectItem.anzfehler      as DefectCount,
      
      @DefaultAggregation: #SUM
      cast(DefectItem.anzfehler * 48.50 as abap.curr(13,2)) as EstimatedScrapCostINR
}
```

---

## 5. UI / UX Design: Fiori Analytical List Page Layout

```
+-----------------------------------------------------------------------------------------+
| S/4HANA Fiori: Shop Floor Defect Pareto Analytics - Plant 1010                          |
+-----------------------------------------------------------------------------------------+
| Filter Bar: Plant [ 1010 ] | Material [ HL-200X ] | Date Range [ Last 30 Days ]         |
+-----------------------------------------------------------------------------------------+
| Visual Filters:                                                                         |
| [By Work Center (Bar)]        [By Defect Category (Donut)]    [By Shift (Bar)]          |
| WC-TST-05: 34%                Photometric: 34%                Shift 1 (Day): 42%        |
| WC-GLUE-03: 27%               Sealing: 27%                    Shift 2 (Evening): 58%    |
+-----------------------------------------------------------------------------------------+
| Interactive Pareto Chart (Defect Frequency vs. Cumulative %):                           |
| 100% |                                              *--*                                |
|  80% |                              *-------------*                                     |
|  60% |                *-----------*                                                     |
|  40% |  |===|        /                                                                  |
|  20% |  |   |  |===|                                                                    |
|   0% +--+---+--+---+--+---+--+---+--+---+--+---+----------------------------------------+
|        OPT-01 SEAL-02 FOG-03 HAR-04 SCR-05 VIS-06                                       |
+-----------------------------------------------------------------------------------------+
| Tabular Item Detail (Drill-down to Production Order, Batch, & Inspector):                |
| Order No | Oper | Work Center | Defect Code | Reason Description        | Scrap Qty |   |
| 1000845  | 0050 | WC-TST-05   | DEF-OPT-01  | Cutoff Line Blur          | 2 EA      |   |
| 1000848  | 0030 | WC-GLUE-03  | DEF-SEAL-02 | Adhesive Void Bead Gap    | 3 EA      |   |
+-----------------------------------------------------------------------------------------+
```

---

## 6. Functional Business Rules & Alerting Thresholds

1. **Shift Anomaly Alert:** If a single work center (e.g. `WC-GLUE-03`) accumulates more than 5 instances of `DEF-SEAL-02` within a single shift, the system issues an automated warning notification to the Maintenance Supervisor to inspect nozzle pressure.
2. **Batch Quarantine Trigger:** If the defect frequency for `DEF-OPT-01` spikes above 5% across multiple orders, the system automatically marks the associated LED driver batch (`HL-PCB-301`) with inspection status `Restricted` in batch master table `MCH1`.
