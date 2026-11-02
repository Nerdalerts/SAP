# Master Data Mapping Specification
## SAP S/4HANA Manufacturing Master Data Field Mappings

**Document Identifier:** `MAP-MFG-MD-001`  
**Author:** Adarsh (Target Role: SAP Manufacturing / Production Planning / PLM Functional Consultant)  
**Process Area:** Master Data Management (Material, BOM, Work Center, Routing)  
**Reference Release:** SAP S/4HANA 2023 / Cloud Private Edition  
**Status:** Approved v1.0 | **Date:** 2 November 2026  
**Linked PRD Deliverable:** Must-Have P0 Data-Mapping Sheet  

---

## 1. Document Overview

This document specifies the end-to-end data mapping rules for migrating legacy engineering and plant manufacturing data into SAP S/4HANA standard master data objects. It governs data structures for:
1. **Material Master** (`MARA`, `MAKT`, `MARC`, `MARD`, `MBEW`)
2. **Bill of Materials (BOM)** (`MAST`, `STKO`, `STPO`)
3. **Work Center** (`CRHD`, `CRTX`, `KAKO`, `CRCO`)
4. **Routing** (`MAPL`, `PLKO`, `PLAS`, `PLPO`)

---

## 2. Material Master Data Mapping

Governs the creation and extension of Finished Products (`HL-200X`), Semi-Finished Assemblies (`HL-HOU-101`, `HL-LENS-201`, `HL-PCB-301`), and Raw Materials (`HL-ADH-501`, `HL-SCR-701`).

| # | Source Field Name | Source Description | Target SAP Table | Target SAP Field | SAP Field Description | Data Type (Len) | Transformation / Derivation Rule | Mand. / Opt. | Business Validation Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **M01** | `Legacy_Part_No` | Legacy Item Code | `MARA` | `MATNR` | Material Number | CHAR(18/40) | Remove whitespace; uppercase; format as `HL-XXX-NNN`. | Mand. | Must not exist in `MARA`; max 40 chars. |
| **M02** | `Item_Class` | Engineering Group | `MARA` | `MTART` | Material Type | CHAR(4) | Map `Finished`->`FERT`, `Assembly`->`HALB`, `Raw`->`ROH`, `Pack`->`VERP`. | Mand. | Must exist in `T134`. |
| **M03** | `Industry_Type` | Sector | `MARA` | `MBRSH` | Industry Sector | CHAR(1) | Default to `M` (Mechanical Engineering). | Mand. | Must exist in `T137`. |
| **M04** | `Part_Description`| Engineering Title | `MAKT` | `MAKTX` | Material Description | CHAR(40) | Direct copy; truncate at 40 chars; language = `EN`. | Mand. | Non-blank; no special non-printable chars. |
| **M05** | `UOM` | Unit of Measurement | `MARA` | `MEINS` | Base Unit of Measure | UNIT(3) | Map `EA`->`ST` (or `EA`), `KG`->`KG`, `M`->`M`. | Mand. | Must exist in `T006` with ISO compliance. |
| **M06** | `Net_Weight_g` | Mass in grams | `MARA` | `NTGEW` | Net Weight | QUAN(13,3) | Convert grams to kilograms (`Value / 1000`). | Opt. | Must be >= 0. |
| **M07** | `Plant_Code` | Manufacturing Plant| `MARC` | `WERKS` | Plant | CHAR(4) | Map legacy plant `PL01` to S/4HANA Plant `1010`. | Mand. | Must exist in `T001W`. |
| **M08** | `Default_Loc` | Storage Location | `MARD` | `LGORT` | Storage Location | CHAR(4) | Map `FG`->`101A`, `SUB`->`101B`, `RAW`->`101C`, `PKG`->`101D`. | Mand. | Must exist in `T001L` under Plant `1010`. |
| **M09** | `MRP_Method` | Planning Code | `MARC` | `DISMM` | MRP Type | CHAR(2) | If FERT/HALB/ROH set `PD`; if bulk hardware set `ND` or `VB`. | Mand. | Must exist in `T438A`. |
| **M10** | `Planner_ID` | Line Controller | `MARC` | `DISPO` | MRP Controller | CHAR(3) | Map automotive line to `P01`. | Mand. | Must exist in `T024D` for Plant `1010`. |
| **M11** | `Lot_Size_Type` | Sizing Policy | `MARC` | `DISLS` | Lot Sizing Procedure | CHAR(2) | Set `EX` (Exact Lot-for-Lot) for discrete assemblies. | Mand. | Must exist in `T439A`. |
| **M12** | `Make_Buy_Code` | Procurement Source | `MARC` | `BESKZ` | Procurement Type | CHAR(1) | Map `Make`->`E` (In-house), `Buy`->`F` (External). | Mand. | Must be `E`, `F`, or `X`. |
| **M13** | `Prod_Sched_Prof`| Scheduling Flags | `MARC` | `SFGRP` | Production Sched. Profile | CHAR(6) | Set `PP0001` (Release checks + auto-GR). | Mand. for FERT/HALB | Must exist in `TCO43`. |
| **M14** | `Backflush_Flag` | Line Consumption | `MARC` | `RGEKZ` | Backflush Indicator | CHAR(1) | Set `1` (Always) for consumables/screws; blank for serialized. | Opt. | Must be `1`, `2`, or blank. |
| **M15** | `Valuation_Class`| Ledger Group | `MBEW` | `BKLAS` | Valuation Class | CHAR(4) | Map FERT->`7920`, HALB->`7900`, ROH->`3000`, VERP->`3050`. | Mand. | Must exist in `T025`. |
| **M16** | `Price_Control` | Costing Type | `MBEW` | `VPRSV` | Price Control Indicator | CHAR(1) | Set `S` (Standard Price) for FERT/HALB; `V` (Moving Avg) for ROH. | Mand. | Must be `S` or `V`. |
| **M17** | `Standard_Cost` | Standard Valuation | `MBEW` | `STPRS` | Standard Price | CURR(11,2)| Set initial inventory price in INR. | Mand. if `VPRSV`='S' | Must be > 0.00. |

---

## 3. Bill of Materials (BOM) Data Mapping

Governs the creation of Production BOMs via `CS01`/`CS02` (Tables `MAST`, `STKO`, `STPO`).

| # | Source Field Name | Source Description | Target SAP Table | Target SAP Field | SAP Field Description | Data Type (Len) | Transformation / Derivation Rule | Mand. / Opt. | Business Validation Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **B01** | `Parent_Part_No` | Assembly Material | `MAST` | `MATNR` | Parent Material Number | CHAR(18/40) | Map to target S/4HANA material number. | Mand. | Parent material must exist in `MARC` Plant `1010`. |
| **B02** | `Plant_Code` | Production Plant | `MAST` | `WERKS` | Plant | CHAR(4) | Constant `1010`. | Mand. | Must match Plant `1010`. |
| **B03** | `BOM_Usage` | BOM Purpose | `MAST` | `STLAN` | BOM Usage | CHAR(1) | Constant `1` (Production BOM). | Mand. | Must exist in `T416`. |
| **B04** | `BOM_Base_Qty` | Reference Yield | `STKO` | `BMENG` | Base Quantity | QUAN(13,3) | Set `1.000` for `EA`. | Mand. | Must be > 0. |
| **B05** | `BOM_Base_UOM` | Reference Unit | `STKO` | `BMEIN` | Base Unit of Measure | UNIT(3) | Inherit from Parent Material Base UoM (`EA`). | Mand. | Must match `MARA-MEINS`. |
| **B06** | `BOM_Status` | Lifecycle State | `STKO` | `STLST` | BOM Status | NUMC(2) | Set `01` (Active for MRP & Production). | Mand. | Must exist in `T415S`. |
| **B07** | `Valid_From_Date`| Effective Date | `STKO` | `DATUV` | Valid-From Date | DATS(8) | Default to migration date `2026-01-01` or ECM date. | Mand. | Valid YYYYMMDD format. |
| **B08** | `Line_Item_No` | Sequence Number | `STPO` | `POSNR` | BOM Item Number | CHAR(4) | Auto-increment by 10 (`0010`, `0020`, `0030`, ...). | Mand. | Unique per BOM header. |
| **B09** | `Item_Category` | Procurement Class | `STPO` | `POSTP` | Item Category | CHAR(1) | Set `L` (Stock item) for physical components; `T` for text. | Mand. | Must exist in `T418`. |
| **B10** | `Child_Part_No` | Component Material | `STPO` | `IDNRK` | Component Material | CHAR(18/40) | Map to child SAP Material Number. | Mand. | Must exist in `MARC` Plant `1010`. |
| **B11** | `Component_Qty` | Quantity per Parent| `STPO` | `MENGE` | Component Quantity | QUAN(13,3) | Direct decimal quantity (e.g. `1.000`, `0.045`, `6.000`). | Mand. | Must be > 0. |
| **B12** | `Component_UOM` | Unit of Issue | `STPO` | `MEINS` | Component Unit | UNIT(3) | Match Child Material Base UoM. | Mand. | Must match child `MARA-MEINS`. |
| **B13** | `Scrap_Percentage`| Expected Line Loss | `STPO` | `KAUSF` | Component Scrap % | DEC(5,2) | Map e.g. `3.00%` for adhesive, `1.50%` for housing. | Opt. | Must be between 0.00% and 99.99%. |
| **B14** | `Issue_Location` | Line-Side Loc | `STPO` | `LGORT` | Issue Storage Location | CHAR(4) | Map `101B` (Sub-assembly), `101C` (Raw), `101D` (Pack). | Opt. | Must exist in `T001L`. |

---

## 4. Work Center Data Mapping

Governs shop floor assembly cells and inspection stations (`CR01`/`CR02`, Tables `CRHD`, `CRTX`, `KAKO`, `CRCO`).

| # | Source Field Name | Source Description | Target SAP Table | Target SAP Field | SAP Field Description | Data Type (Len) | Transformation / Derivation Rule | Mand. / Opt. | Business Validation Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **W01** | `Work_Cell_ID` | Legacy Station Code | `CRHD` | `ARBPL` | Work Center Name | CHAR(8) | Format as `WC-XXXX-NN` (e.g. `WC-ASSY-01`). | Mand. | Must be unique within Plant `1010`. |
| **W02** | `Plant_Code` | Plant | `CRHD` | `WERKS` | Plant | CHAR(4) | Constant `1010`. | Mand. | Must exist in `T001W`. |
| **W03** | `Work_Center_Cat`| Station Category | `CRHD` | `VERWE` | Work Center Category | CHAR(4) | Set `0001` (Machine / Assembly Line). | Mand. | Must exist in `TC21`. |
| **W04** | `Cell_Name` | Station Description | `CRTX` | `KTEXT` | Work Center Description | CHAR(40) | Descriptive station name; max 40 chars. | Mand. | Non-blank. |
| **W05** | `Std_Value_Key` | Parameter Template | `CRHD` | `VGWTS` | Standard Value Key | CHAR(4) | Set `SAP1` (Setup, Machine, Labor). | Mand. | Must exist in `TC25`. |
| **W06** | `Cap_Category` | Capacity Type | `KAKO` | `KAPAR` | Capacity Category | CHAR(3) | Set `001` (Machine) or `002` (Labor). | Mand. | Must exist in `TC27`. |
| **W07** | `Shift_Hours_Day`| Operating Hours | `KAKO` | `BEGZT` / `ENDZT`| Operating Shift Time | TIME(6) | Set 2 shifts: 06:00 to 22:00 (16 hrs gross). | Mand. | End Time > Start Time. |
| **W08** | `Capacity_Factor`| Net Utilization % | `KAKO` | `NUTZZ` | Rate of Capacity Util. | NUMC(3) | Map 90% -> `90`, 95% -> `95`. | Mand. | Value between 50 and 100. |
| **W09** | `Cost_Center` | Controlling Cost Ctr| `CRCO` | `KOSTL` | Cost Center | CHAR(10) | Map `CC-PROD-101`, `CC-PROD-102`, `CC-QUAL-201`. | Mand. | Must exist in `CSKS` for Controlling Area `1000`. |
| **W10** | `Setup_Act_Type` | Activity Code Setup | `CRCO` | `LSTAR1` | Setup Activity Type | CHAR(6) | Set `SET` (Setup Hours). | Mand. | Must exist in `CSLA`. |
| **W11** | `Mach_Act_Type` | Activity Code Mach | `CRCO` | `LSTAR2` | Machine Activity Type | CHAR(6) | Set `MAC` (Machine Hours). | Mand. | Must exist in `CSLA`. |
| **W12** | `Lab_Act_Type` | Activity Code Labor | `CRCO` | `LSTAR3` | Labor Activity Type | CHAR(6) | Set `LAB` (Labor Hours). | Mand. | Must exist in `CSLA`. |

---

## 5. Assembly Routing Data Mapping

Governs production operations 0010 to 0070 (`CA01`/`CA02`, Tables `MAPL`, `PLKO`, `PLAS`, `PLPO`, `AFVV`).

| # | Source Field Name | Source Description | Target SAP Table | Target SAP Field | SAP Field Description | Data Type (Len) | Transformation / Derivation Rule | Mand. / Opt. | Business Validation Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **R01** | `Finished_Part_No`| Assembly Material | `MAPL` | `MATNR` | Material Number | CHAR(18/40) | Map to target finished material `HL-200X`. | Mand. | Must exist in `MARC` Plant `1010`. |
| **R02** | `Plant_Code` | Manufacturing Plant| `MAPL` | `WERKS` | Plant | CHAR(4) | Constant `1010`. | Mand. | Must exist in `T001W`. |
| **R03** | `Routing_Group` | Group Identifier | `PLKO` | `PLNNR` | Task List Group | CHAR(8) | Auto-numbered (e.g. `50001201`). | Mand. | Unique task list group in `PLKO`. |
| **R04** | `Group_Counter` | Variant Counter | `PLKO` | `PLNAL` | Group Counter | CHAR(2) | Constant `01`. | Mand. | Format `01`, `02`. |
| **R05** | `Routing_Usage` | Application Purpose| `PLKO` | `VERWE` | Task List Usage | CHAR(3) | Set `1` (Production). | Mand. | Must exist in `T411`. |
| **R06** | `Routing_Status` | Release State | `PLKO` | `STATU` | Status | CHAR(3) | Set `4` (Released for General Use). | Mand. | Must exist in `T412`. |
| **R07** | `Base_Batch_Qty` | Reference Quantity | `PLKO` | `BMSCH` | Base Quantity | QUAN(13,3) | Set `100.000` (Standard lot size 100 EA). | Mand. | Must be > 0. |
| **R08** | `Op_Seq_No` | Operation Sequence | `PLPO` | `VORNR` | Operation Number | CHAR(4) | `0010`, `0020`, `0030`, `0040`, `0050`, `0060`, `0070`. | Mand. | 4-digit zero-padded sequence. |
| **R09** | `Station_ID` | Assigned Work Center| `PLPO` | `ARBID` | Work Center ID | NUMC(8) | Lookup internal ID for `WC-ASSY-01` to `WC-PKG-07`. | Mand. | Must resolve in `CRHD`. |
| **R10** | `Control_Code` | Execution Control | `PLPO` | `STEUS` | Control Key | CHAR(4) | Set `PP01` for standard; `QM01` for Op 0050/0060. | Mand. | Must exist in `T430`. |
| **R11** | `Op_Description` | Process Step Name | `PLPO` | `LTXA1` | Operation Short Text | CHAR(40) | Descriptive operation title (max 40 chars). | Mand. | Non-blank. |
| **R12** | `Setup_Time_Min` | Setup Duration | `AFVV` | `VGW01` | Standard Value 1 (Setup)| QUAN(9,3) | Setup time in minutes per base quantity. | Mand. | Must be >= 0. |
| **R13** | `Machine_Time_Min`| Machine Run Time | `AFVV` | `VGW02` | Standard Value 2 (Mach) | QUAN(9,3) | Machine cycle time in minutes per base quantity. | Mand. | Must be >= 0. |
| **R14** | `Labor_Time_Min` | Labor Touch Time | `AFVV` | `VGW03` | Standard Value 3 (Labor)| QUAN(9,3) | Direct labor minutes per base quantity. | Mand. | Must be >= 0. |
