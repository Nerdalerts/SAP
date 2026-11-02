# PLM-to-ERP Integration Specification
## Automated EBOM-to-MBOM Handoff & Engineering Change Interface

**Document Identifier:** `INT-PLM-ERP-001`  
**Author:** Adarsh (Target Role: SAP Manufacturing / Production Planning / PLM Functional Consultant)  
**Process Area:** Cross-System Integration (PLM to SAP S/4HANA Manufacturing)  
**Reference Release:** SAP S/4HANA 2023 / Cloud Private Edition & SAP Integration Suite  
**Status:** Approved v1.0 | **Date:** 2 November 2026  
**Linked PRD Deliverable:** Must-Have P0 PLM-to-ERP Integration Mapping  

---

## 1. Architectural Overview & Integration Context

In discrete manufacturing, product development operates within Product Lifecycle Management (PLM) systems (e.g. Siemens Teamcenter, PTC Windchill, Dassault 3DEXPERIENCE), while operational procurement, inventory management, and shop floor execution reside in SAP S/4HANA. 

This specification establishes an automated, event-driven integration architecture via **SAP Integration Suite (Cloud Integration)** that:
1. Synchronizes CAD design items to SAP Product Master records (`MARA`).
2. Converts the Engineering Bill of Materials (EBOM) into an actionable Manufacturing Bill of Materials (MBOM).
3. Transmits Engineering Change Notices (ECNs) into SAP S/4HANA Change Masters (`AENR`).

```
+------------------------------------+
|             PLM System             |
| (Teamcenter / Windchill / Enovia)  |
+-----------------+------------------+
                  |
                  | HTTPS / JSON (Webhook on "Released for Production")
                  v
+------------------------------------+
|       SAP Integration Suite        |
|    (Cloud Integration on BTP)      |
|  * Value Mapping (UoM, Types)      |
|  * CAD Phantom Dissolution         |
|  * Consumable Recipe Injection     |
|  * Idempotency & Schema Validation |
+-----------------+------------------+
                  |
                  | OData v2/v4 REST / RFC
                  v
+------------------------------------+
|          SAP S/4HANA Core          |
|  * AIF Error Workbench (/AIF/ERR)  |
|  * Product Master (MM01 / MARA)    |
|  * Manufacturing BOM (CS01 / MAST) |
|  * Change Master (CC01 / AENR)     |
+------------------------------------+
```

---

## 2. Core Transformation Principles: EBOM vs. MBOM

| Dimension | Engineering BOM (EBOM in PLM) | Manufacturing BOM (MBOM in SAP S/4HANA) | Integration Pipeline Transformation Rule |
| :--- | :--- | :--- | :--- |
| **Purpose** | Functional product design & CAD geometry. | Shop floor assembly, costing, and procurement. | Realign functional assemblies into manufacturing sequences. |
| **Phantoms** | Contains CAD structural groupings (e.g. `VIRT-OPT-BRKT`). | Physical stations cannot stock virtual nodes. | **Phantom Dissolution:** Flatten virtual assembly nodes and attach child parts directly to parent. |
| **Consumables** | Absent (chemical adhesives, thermal paste, tape not modelled in 3D). | Critical (PUR adhesive `HL-ADH-501` required for waterproof seal). | **Recipe Injection:** Middleware queries plant consumable rulebook and injects 0.045 KG adhesive per headlamp. |
| **Packaging** | Excluded from CAD geometry. | Mandatory for finished goods storage & shipping. | **Packaging Rule:** Inject corrugated carton `HL-PKG-801` and protective film. |
| **Units of Measure** | Often non-ISO strings (`Inches`, `each`). | Strict ISO 3-character codes (`INH`, `ST`/`EA`). | **Value Mapping:** Convert engineering units to SAP ISO compliant codes. |

---

## 3. Interface Detailed Technical Specifications

### Interface 1: CAD Part Synchronization -> SAP Product Master
- **Trigger Event:** Design Engineer sets Part lifecycle status to "Released" in PLM.
- **Protocol:** REST HTTPS / TLS 1.3
- **Target SAP API:** `API_PRODUCT_SRV_0001` (`A_Product`)

| PLM Source Field | S/4HANA Target Field | Target Table | Type (Len) | Transformation / Derivation Logic |
| :--- | :--- | :--- | :--- | :--- |
| `item_id` | `Product` | `MARA-MATNR` | CHAR(40) | Remove whitespace; ensure uppercase. |
| `item_name` | `ProductDescription` | `MAKT-MAKTX` | CHAR(40) | Truncate at 40 characters; language = `EN`. |
| `part_type` | `ProductType` | `MARA-MTART` | CHAR(4) | Lookup mapping table: `Assembly`->`HALB`, `Component`->`ROH`. |
| `uom` | `BaseUnit` | `MARA-MEINS` | UNIT(3) | Value map: `EA`->`EA`, `KG`->`KG`, `MM`->`MMT`. |
| `weight_g` | `NetWeight` | `MARA-NTGEW` | QUAN(13,3) | `weight_g / 1000` (converts grams to kilograms). |
| `cad_drawing_no` | `DocumentNumber` | `MARA-ZEINR` | CHAR(22) | Direct copy of CAD drawing reference number. |

---

### Interface 2: EBOM Release -> S/4HANA Manufacturing BOM
- **Trigger Event:** PLM Assembly Release workflow sign-off.
- **Protocol:** OData v2 POST / PATCH
- **Target SAP API:** `API_BILL_OF_MATERIAL_SRV_0002` (`A_BillOfMaterial`)

| PLM EBOM Node | S/4HANA Target Field | Target Table | Type (Len) | Transformation / Derivation Logic |
| :--- | :--- | :--- | :--- | :--- |
| `header.item_id` | `BillOfMaterialMaterial` | `MAST-MATNR` | CHAR(40) | Target parent assembly material number. |
| `header.plant` | `Plant` | `MAST-WERKS` | CHAR(4) | Plant code mapping: `PLM_MFG_01` -> `1010`. |
| `header.usage` | `BillOfMaterialVariantUsage`| `MAST-STLAN` | CHAR(1) | Constant `1` (Production BOM). |
| `item.find_no` | `BillOfMaterialItemNumber` | `STPO-POSNR` | CHAR(4) | Formatted as 4-digit zero-padded sequence (`0010`, `0020`, ...). |
| `item.part_no` | `BillOfMaterialComponent` | `STPO-IDNRK` | CHAR(40) | Target child material number. |
| `item.qty` | `BillOfMaterialItemQuantity`| `STPO-MENGE` | QUAN(13,3) | Direct decimal quantity. |
| `item.uom` | `BillOfMaterialItemUnit` | `STPO-MEINS` | UNIT(3) | Value mapped ISO UoM. |
| `item.item_type`| `BillOfMaterialItemCategory`| `STPO-POSTP` | CHAR(1) | Default `L` (Stock item). |
| `item.scrap_pct`| `ComponentScrapInPercent` | `STPO-KAUSF` | DEC(5,2) | Pass engineering scrap factor (e.g. 1.5%). |

---

### Interface 3: Engineering Change Notice (ECN) -> SAP Change Master (ECM)
- **Trigger Event:** Change Control Board (CCB) approval of ECN in PLM.
- **Target SAP API:** `API_ENGINEERING_CHANGE_MASTER_SRV` (`A_EngineeringChangeMaster`)

| PLM ECN Field | S/4HANA Target Field | Target Table | Type (Len) | Transformation / Derivation Logic |
| :--- | :--- | :--- | :--- | :--- |
| `ecn_number` | `ChangeNumber` | `AENR-AENNR` | CHAR(12) | Formatted as `ECM-YYYY-NNN`. |
| `ecn_title` | `ChangeDescription` | `AENR-AETXT` | CHAR(40) | Truncate at 40 characters. |
| `effective_date`| `ValidFromDate` | `AENR-DATUV` | DATS(8) | ISO 8601 string `YYYY-MM-DD` converted to SAP `YYYYMMDD`. |
| `change_reason` | `ReasonForChange` | `AENR-AENAM` | CHAR(40) | Change category classification code. |
| `object_flags` | `ObjectTypesActive` | `AENR-AEOI` | CHAR(1) | Set flags for Material (`X`), BOM (`X`), Routing (`X`). |

---

## 4. Sample JSON Integration Payload

### Outbound Payload from PLM to SAP Integration Suite (EBOM Handoff)

```json
{
  "event_type": "EBOM_PRODUCTION_RELEASE",
  "source_system": "TEAMCENTER_PLM",
  "timestamp": "2026-11-02T14:30:00Z",
  "ecn_reference": "ECM-2026-088",
  "effective_date": "2026-12-01",
  "parent_material": {
    "item_id": "HL-200X",
    "revision": "B",
    "description": "Bi-LED Automotive Headlamp Assembly (RH)",
    "plant_code": "1010",
    "base_uom": "EA",
    "base_qty": 1.0
  },
  "ebom_items": [
    {
      "sequence": 10,
      "item_id": "HL-HOU-101",
      "revision": "A",
      "description": "Composite Headlamp Housing Sub-Assembly",
      "quantity": 1.0,
      "uom": "EA",
      "is_phantom": false
    },
    {
      "sequence": 20,
      "item_id": "HL-LENS-201",
      "revision": "A",
      "description": "Projector Optical Lens Module",
      "quantity": 1.0,
      "uom": "EA",
      "is_phantom": false
    },
    {
      "sequence": 30,
      "item_id": "HL-PCB-301",
      "revision": "B",
      "description": "Bi-LED Driver & Heat Sink Module",
      "quantity": 1.0,
      "uom": "EA",
      "is_phantom": false
    },
    {
      "sequence": 40,
      "item_id": "HL-HAR-401",
      "revision": "A",
      "description": "Waterproof 6-Pin Sealed Wiring Harness",
      "quantity": 1.0,
      "uom": "EA",
      "is_phantom": false
    },
    {
      "sequence": 50,
      "item_id": "HL-SCR-702",
      "revision": "A",
      "description": "Torx T20 Fastener M4x18 Zinc Plated",
      "quantity": 6.0,
      "uom": "EA",
      "is_phantom": false
    }
  ],
  "manufacturing_injections": {
    "inject_consumables": true,
    "consumable_items": [
      {
        "sequence": 60,
        "item_id": "HL-ADH-501",
        "description": "Automotive 2K PUR Structural Adhesive",
        "quantity": 0.045,
        "uom": "KG",
        "scrap_pct": 3.0
      },
      {
        "sequence": 70,
        "item_id": "HL-PKG-801",
        "description": "Static-Shield Corrugated Shipping Carton",
        "quantity": 1.0,
        "uom": "EA",
        "scrap_pct": 0.0
      }
    ]
  }
}
```

---

## 5. Error Handling, Exception Queues & Reconciliation

### Error Classification & Automated Resolution

| Error Code | Error Condition | System Action | Resolution Procedure |
| :--- | :--- | :--- | :--- |
| **INT-ERR-001** | Missing Material Master in SAP | S/4HANA returns HTTP `422 Unprocessable Entity`. Payload pushed to AIF dead-letter queue. | Trigger automated alert to Master Data Steward. Extend material to Plant `1010` and reprocess in `/AIF/ERR`. |
| **INT-ERR-002** | Invalid / Unmapped Unit of Measure | Payload rejected at Integration Suite schema validation. | Update Value Mapping table in Cloud Integration (e.g. `INCHES` -> `INH`) and restart message. |
| **INT-ERR-003** | Inactive or Closed Change Master | S/4HANA rejects BOM update referencing locked Change Number `AENR`. | Reactivate Change Master in `CC02` or update payload with valid Change Number. |
| **INT-ERR-004** | Network Timeout / Connection Drop | Middleware executes 3 exponential retries (1m, 5m, 15m). | If retries fail, message transitions to Dead Letter Queue (DLQ) with alert to on-call integration team. |

### Monitoring & Governance
1. **SAP Application Interface Framework (AIF):** Integration specialists utilize transaction `/AIF/ERR` (Fiori App *Message Monitoring*) to inspect failed payloads, view field-level syntax errors, and re-trigger commit actions with zero data loss.
2. **Reconciliation Audit Report:** A nightly batch job runs transaction `CS15` (Where-Used) and compares active SAP MBOM structures against PLM released EBOM hashes, publishing an automated daily discrepancy dashboard.
