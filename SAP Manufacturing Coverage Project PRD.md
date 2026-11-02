# SAP Manufacturing Coverage Project: PRD

**Author:** Adarsh | **Status:** Draft v1 | **Date:** 2 November 2026 | **Type:** Self-initiated portfolio project

## 1. Problem statement

The target role (SAP Manufacturing / Production Planning / PLM consultant) asks for business-process mapping, Business Scenario Documents, Functional Requirements Documents (FRDs), user stories, design and data-mapping documents, test plans, and working knowledge of SAP PP and PLM. The current resume has strong shop-floor analysis (Uno Minda) and process-mapping work (Technip), but **no SAP exposure and no requirements-documentation artifact**. A screener cannot verify that the candidate can do the core job, so the application reads as a data-analytics profile applying to functional consulting.

This project produces a small, verifiable body of work that closes that gap honestly.

## 2. Project thesis

**"From shop floor to SAP":** take a generalized discrete-manufacturing process (an assembly line with BOMs, routings, quality checks and engineering changes, informed by the Uno Minda internship but using **no confidential or employer-specific data**) and translate it into SAP PP / QM / PLM process scenarios with consultant-grade documentation.

The project is documentation-led. It does **not** claim implementation, configuration or certification experience. Hands-on SAP steps are included only if a trial or training system is actually available (see Open Questions).

## 3. Goals

1. **Process coverage:** map 7 manufacturing scenarios from as-is to to-be SAP process flows (table in section 6).
2. **Requirements artifacts:** deliver 1 Business Scenario Document, 1 FRD, and at least 15 user stories with Given/When/Then acceptance criteria.
3. **Data and integration mapping:** deliver 1 data-mapping sheet (source fields to SAP master data for material, BOM, routing, work center) and 1 PLM-to-ERP integration mapping.
4. **Test documentation:** deliver 1 test plan with at least 20 test cases tied back to the user stories.
5. **Verified learning:** complete at least one free SAP learning path (openSAP or SAP Learning) on PP or PLM, and cite it accurately.
6. **Packaging:** publish everything as one GitHub repo plus a single PDF summary, ready to link from the resume.

## 4. Non-goals

- **Not a client implementation.** Nothing here may be described as client work or SAP project experience.
- **No custom development.** ABAP or extensions are out; the role is functional, not technical.
- **No confidential data.** Uno Minda specifics (volumes, part numbers, internal figures) stay out; use generalized or synthetic examples.
- **No full ERP scope.** Finance, HR and sales modules are out; only PP, QM, PLM and their touchpoints.
- **No certification claims.** Learning paths are listed as completed courses, not credentials, unless a real certificate is issued.

## 5. Audience and user stories

**Primary audience:** the recruiter or hiring manager screening for evidence of SAP-relevant skills. **Secondary:** the interviewer who will probe scenarios.

**Project-level stories**

- As a recruiter, I want a one-page summary and a linked repo so that I can verify the candidate can write requirements without reading everything.
- As an interviewer, I want clear as-is/to-be flows so that I can ask scenario questions and see the candidate's reasoning.
- As the candidate, I want every artifact to be traceable (scenario to story to test case) so that I can explain it end to end in an interview.

**Sample process-level stories (the content being written)**

- As a production planner, I want planned production driven by demand and BOM data so that I know which components to procure and when.
- As a shop-floor supervisor, I want to confirm completed operations against a production order so that actual progress and scrap are recorded.
- As a quality engineer, I want defects captured against an inspection lot so that recurring issues (for example lens fogging, weld defects) can be analysed.
- As a design engineer, I want an engineering change to flow to the production BOM so that the shop floor builds the current revision.
- As a plant IT lead, I want master-data mapping rules documented so that data migration errors are caught before go-live.

Each story gets acceptance criteria, for example: *Given* a released production order, *when* the supervisor confirms an operation with a scrap quantity, *then* the order status and actual quantities update and the scrap is visible for quality analysis.

## 6. Scope: SAP coverage map

| # | Scenario (generalized) | SAP area | Deliverable |
| --- | --- | --- | --- |
| 1 | Product and BOM definition | Master data / PLM | Process flow, data mapping |
| 2 | Routings and work centers | PP master data | Process flow, data mapping |
| 3 | Demand to production plan | PP (planning / MRP) | BSD, user stories |
| 4 | Production order execution and confirmation | PP / shop floor | FRD, user stories, test cases |
| 5 | Quality inspection and defect handling | QM | User stories, test cases |
| 6 | Engineering change to production | PLM change management | BSD, FRD section |
| 7 | PLM-to-ERP data transfer | Integration | Integration mapping sheet |

*Note:* module and transaction names differ between SAP ECC and S/4HANA. Pick one release as the reference (S/4HANA is the sensible default), and verify terminology against official SAP documentation before publishing.

## 7. Requirements

### Must-have (P0)

- **Scenario flows (7):** as-is and to-be diagrams, each with actors, inputs, outputs and exceptions. *Done when* every flow has at least one exception path.
- **Business Scenario Document:** one BSD covering scenarios 3, 4 and 6. *Done when* it states scope, assumptions, process steps and open issues.
- **FRD:** one FRD for production order execution and confirmation. *Done when* each requirement has an ID, priority and linked user story.
- **User stories:** at least 15, in standard format, each with Given/When/Then criteria.
- **Data-mapping sheet:** material, BOM, routing and work center fields, with source, target, transformation rule and validation rule.
- **Test plan:** at least 20 cases, each linked to a story, with preconditions, steps and expected results.
- **Accuracy pass:** every SAP term checked against official documentation; nothing fabricated.

### Nice-to-have (P1)

- A short design-document example for one custom report (for example a defect Pareto report), reflecting the Pareto analysis already done in Python.
- A one-page client-style workshop agenda and end-user training outline.
- Hands-on screenshots from a trial/training system, **only if real**.

### Future considerations (P2)

- Extend to SAP Digital Manufacturing / MES scenarios.
- Add a process-industry or repetitive-manufacturing variant.
- Add a supply-chain integration scenario (procurement to production) linking to the Technip experience.

## 8. Success metrics

**Leading (within 4 weeks)**

- All P0 deliverables complete and linked from one repo (target: 100%).
- Traceability: every user story maps to at least one test case, and every scenario to at least one story.
- One learning path completed and cited.

**Lagging (1 to 3 months)**

- Ability to walk through any scenario in an interview without notes.
- Interview shortlists or recruiter responses for SAP, ERP and functional roles after the resume update. Treat this as a signal, not a guarantee.

## 9. Resume integration

Only after completion, add a single entry such as: *Self-initiated project: SAP PP/QM/PLM process mapping and requirements documentation (BSD, FRD, user stories, test plan).* Bullets must describe what was actually produced, with real counts, and the entry must be labelled self-initiated. Keep a one-line honest statement ready for interviews: new to SAP, strong in shop-floor process analysis, and has documented the SAP processes independently.

## 10. Timeline (4 weeks)

- **Week 1 (2 to 8 Nov):** start the SAP learning path, fix the reference release, scope scenarios, decide system-access question.
- **Week 2:** as-is and to-be flows for scenarios 1 to 7; draft data-mapping sheet.
- **Week 3:** BSD, FRD, user stories and acceptance criteria.
- **Week 4:** test plan, accuracy pass, package repo and PDF, update resume.

If the application deadline is earlier, cut P1 items first, then reduce user stories to 10, but never drop the accuracy pass.

## 11. Open questions

- **Blocking:** Is any SAP trial or training system accessible, or is this strictly documentation-based? (Decide by end of Week 1.)
- **Blocking:** What is the application deadline for the target role?
- **Non-blocking:** Should the case be based on generalized headlamp assembly, or a public case study, to avoid any confidentiality concern?
- **Non-blocking:** Does the target employer emphasize particular modules (PP, PLM, MES) that should get more weight in the FRD?
- **Non-blocking:** Publish publicly on GitHub, or share privately by link with applications?
