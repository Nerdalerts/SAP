"""
SAP Manufacturing Coverage Project - Artifact Generation Script
Generates:
1. data/SAP_Manufacturing_Coverage_Data_Mapping_and_Testing.xlsx
2. docs/SAP_Manufacturing_Coverage_Executive_Summary.pdf
"""

import os
import csv
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

BASE_DIR = r"C:\Users\PC\Desktop\SAP"
DATA_DIR = os.path.join(BASE_DIR, "data")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

def generate_excel():
    excel_path = os.path.join(DATA_DIR, "SAP_Manufacturing_Coverage_Data_Mapping_and_Testing.xlsx")
    print(f"Generating Excel workbook: {excel_path}...")
    
    # Read CSV data
    dict_csv = os.path.join(DOCS_DIR, "05_DATA_MAPPING", "data_dictionary.csv")
    tc_csv = os.path.join(DATA_DIR, "test_cases.csv")
    
    df_dict = pd.read_csv(dict_csv)
    df_tc = pd.read_csv(tc_csv)
    
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)
    
    # Define styles
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    title_font = Font(name="Calibri", size=14, bold=True, color="1B365D")
    sub_font = Font(name="Calibri", size=10, italic=True, color="555555")
    data_font = Font(name="Calibri", size=10)
    bold_font = Font(name="Calibri", size=10, bold=True)
    
    header_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    alt_fill = PatternFill(start_color="F7F9FC", end_color="F7F9FC", fill_type="solid")
    accent_fill = PatternFill(start_color="E8F1F5", end_color="E8F1F5", fill_type="solid")
    pass_fill = PatternFill(start_color="D4EDDA", end_color="D4EDDA", fill_type="solid")
    pass_font = Font(name="Calibri", size=10, bold=True, color="155724")
    
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    
    # -----------------------------------------------------------------
    # Sheet 1: Project Overview
    # -----------------------------------------------------------------
    ws_ov = wb.create_sheet(title="Project_Overview")
    ws_ov.views.sheetView[0].showGridLines = True
    
    ws_ov["A1"] = "SAP Manufacturing Coverage Project: Data Mapping & Verification Workbook"
    ws_ov["A1"].font = title_font
    ws_ov["A2"] = "Reference Release: SAP S/4HANA 2023 | Discrete Automotive Assembly (HL-200X)"
    ws_ov["A2"].font = sub_font
    
    overview_data = [
        ["Metric / Deliverable", "Value", "Notes / Target"],
        ["Candidate / Author", "Adarsh", "Target Role: SAP Manufacturing / PP / PLM Consultant"],
        ["Reference Manufacturing Case", "Bi-LED Automotive Headlamp Assembly (HL-200X)", "Synthetic discrete assembly; 0% confidential data"],
        ["Target S/4HANA Plant", "1010", "Storage Locs: 101A (FG), 101B (HALB), 101C (ROH), 101Q (QM)"],
        ["Mapped Scenarios (P0)", "7 of 7 Complete (100%)", "SC-01 through SC-07 with As-Is, To-Be & Exception Paths"],
        ["Business Scenario Document (BSD)", "1 Integrated BSD Complete", "Covers Scenarios 3, 4, and 6 in an unbroken thread"],
        ["Functional Requirements Document (FRD)", "1 Full FRD (15 Requirements)", "FR-PP-001 to FR-PP-015 with field logic & validations"],
        ["Agile User Stories (P0)", "20 Stories with Given/When/Then", "100% mapped to test cases and functional requirements"],
        ["System Test Cases (P0)", "25 Detailed Test Cases", "100% Passed / Simulated with comprehensive validation"],
        ["Data Mapping Fields (P0)", "57 Master Data Fields Mapped", "Material Master, BOM, Work Center, and Routing"],
        ["End-to-End Traceability (P0)", "100% Bi-Directional Traceability", "Scenario -> Story -> FRD -> Test Case -> SAP Object"],
        ["P1 Deliverables Included", "Defect Pareto FS + Client Workshop", "Reflecting Uno Minda shop floor defect diagnostics"]
    ]
    
    for r_idx, row in enumerate(overview_data, start=4):
        for c_idx, val in enumerate(row, start=1):
            cell = ws_ov.cell(row=r_idx, column=c_idx, value=val)
            if r_idx == 4:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cell.font = bold_font if c_idx == 1 else data_font
                cell.border = thin_border
                if r_idx % 2 == 1 and c_idx != 1:
                    cell.fill = alt_fill
                    
    # Auto-fit columns
    for col in ws_ov.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws_ov.column_dimensions[col_letter].width = max(max_len + 3, 14)

    # -----------------------------------------------------------------
    # Helper to style standard data table
    # -----------------------------------------------------------------
    def add_table_sheet(title, df_subset, title_text):
        ws = wb.create_sheet(title=title)
        ws.views.sheetView[0].showGridLines = True
        
        ws["A1"] = title_text
        ws["A1"].font = title_font
        ws["A2"] = "SAP S/4HANA Master Data Architecture | Plant 1010"
        ws["A2"].font = sub_font
        
        headers = list(df_subset.columns)
        for c_idx, h in enumerate(headers, start=1):
            cell = ws.cell(row=4, column=c_idx, value=h)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            
        for r_idx, row in enumerate(df_subset.itertuples(index=False), start=5):
            for c_idx, val in enumerate(row, start=1):
                cell = ws.cell(row=r_idx, column=c_idx, value=val)
                cell.font = data_font
                cell.border = thin_border
                if r_idx % 2 == 1:
                    cell.fill = alt_fill
                if str(val) == "Passed":
                    cell.fill = pass_fill
                    cell.font = pass_font
                    cell.alignment = Alignment(horizontal="center")
                    
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 45)

    # Add master data sheets
    add_table_sheet("Material_Master", df_dict[df_dict["Object_Type"] == "Material"], "Material Master Field Mapping (MARA, MARC, MARD, MBEW)")
    add_table_sheet("BOM_Mapping", df_dict[df_dict["Object_Type"] == "BOM"], "Production Bill of Materials Mapping (MAST, STKO, STPO)")
    add_table_sheet("Work_Center_Mapping", df_dict[df_dict["Object_Type"] == "WorkCenter"], "Shop Floor Work Center Mapping (CRHD, CRTX, KAKO, CRCO)")
    add_table_sheet("Routing_Mapping", df_dict[df_dict["Object_Type"] == "Routing"], "Assembly Routing & Operation Mapping (MAPL, PLKO, PLPO, AFVV)")
    add_table_sheet("Test_Cases", df_tc, "Comprehensive System Integration Test Execution Matrix (25 Scripts)")
    
    # Save Excel
    wb.save(excel_path)
    print("Excel generated successfully!")

# -----------------------------------------------------------------
# Numbered Canvas for PDF
# -----------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "SAP S/4HANA Manufacturing Coverage Project | Portfolio Executive Summary")
            self.drawRightString(558, 750, "Candidate: Adarsh")
            self.setStrokeColor(colors.HexColor("#CCCCCC"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)
            
        # Footer
        self.setStrokeColor(colors.HexColor("#CCCCCC"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        
        self.drawString(54, 32, "Confidentiality: 100% Synthetic Manufacturing Data | Reference: SAP S/4HANA 2023")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_text)
        self.restoreState()

def generate_pdf():
    pdf_path = os.path.join(DOCS_DIR, "SAP_Manufacturing_Coverage_Executive_Summary.pdf")
    print(f"Generating PDF executive summary: {pdf_path}...")
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1B365D'),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#4A5568'),
        spaceAfter=12
    )
    
    h1_style = ParagraphStyle(
        'H1Style',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1B365D'),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'H2Style',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#2C3E50'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor('#2D3748'),
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )
    
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#2D3748')
    )
    
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.white
    )
    
    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1B365D')
    )

    story = []
    
    # Document Header
    story.append(Paragraph("SAP S/4HANA Manufacturing Coverage Project", title_style))
    story.append(Paragraph("Executive Briefing & Portfolio Artifact Summary | Candidate: Adarsh", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1B365D"), spaceAfter=10))
    
    # Metadata Box
    meta_data = [
        [
            Paragraph("<b>Target Role:</b> SAP PP / QM / PLM Functional Consultant", table_cell),
            Paragraph("<b>Date:</b> November 2026", table_cell),
            Paragraph("<b>Status:</b> Baseline Release v1.0", table_cell)
        ],
        [
            Paragraph("<b>Architecture:</b> SAP S/4HANA 2023 / Cloud Private Edition", table_cell),
            Paragraph("<b>Product Scope:</b> Bi-LED Automotive Headlamp (HL-200X)", table_cell),
            Paragraph("<b>Deliverables:</b> 100% P0 & P1 Complete", table_cell)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[180, 160, 164])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0F4F8')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))
    
    # 1. Project Background & Rationale
    story.append(Paragraph("1. Project Background & Rationale", h1_style))
    story.append(Paragraph(
        "Screeners and hiring managers evaluating candidates for SAP Manufacturing (PP / QM / PLM) functional consulting roles look for verifiable evidence of requirements elicitation, Business Scenario Documents (BSDs), Functional Requirements Documents (FRDs), Agile user stories, data migration mapping, and structured testing governance. "
        "While my industrial background includes intensive shop floor diagnostics at <b>Uno Minda</b> (automotive lighting assembly) and process mapping at <b>Technip Energies</b>, this self-initiated portfolio project directly closes the documentation gap by translating that physical engineering knowledge into <b>consultant-grade SAP S/4HANA artifacts</b>.",
        body_style
    ))
    story.append(Paragraph(
        "<i>Ethics & Confidentiality Notice:</i> All models, part numbers, routings, and defect metrics in this repository are synthetic and generalized. No confidential or employer-specific data is used.",
        callout_style
    ))
    story.append(Spacer(1, 6))
    
    # 2. Manufacturing Case Study
    story.append(Paragraph("2. Discrete Manufacturing Reference Model: Bi-LED Headlamp (HL-200X)", h1_style))
    story.append(Paragraph(
        "The project models an automotive discrete assembly line in Plant <b>1010</b> producing the Bi-LED Headlamp Assembly (<code>HL-200X</code>). The assembly routing encompasses 7 synchronized operations across dedicated work centers:",
        body_style
    ))
    
    mfg_steps = [
        "<b>Op 0010 (WC-ASSY-01):</b> Housing prep, grommet insertion, and wiring harness routing.",
        "<b>Op 0020 (WC-OPT-02):</b> Precision optical projector lens alignment and LED driver mounting.",
        "<b>Op 0030 (WC-GLUE-03):</b> Automated robotic dispensing of 2K polyurethane structural adhesive (HL-ADH-501).",
        "<b>Op 0040 (WC-CURE-04):</b> Polycarbonate outer lens ultrasonic mating and thermal tunnel curing.",
        "<b>Op 0050 (WC-TST-05):</b> Milestone in-process photometric lux cutoff and luminous intensity inspection (Min 28,000 cd).",
        "<b>Op 0060 (WC-LEAK-06):</b> Helium sniffing and differential pressure decay moisture ingress leak test (Max 0.5 sccm).",
        "<b>Op 0070 (WC-PKG-07):</b> Final milestone packaging, protective film application, and 2D barcode serialization."
    ]
    for step in mfg_steps:
        story.append(Paragraph(f"• {step}", bullet_style))
    story.append(Spacer(1, 8))
    
    # 3. Portfolio Deliverables Matrix
    story.append(Paragraph("3. Summary of Portfolio Deliverables (P0 & P1)", h1_style))
    
    deliv_data = [
        [Paragraph("Deliverable Area", table_header), Paragraph("Artifact Name & Scope", table_header), Paragraph("Key Functional Details", table_header), Paragraph("Status", table_header)],
        [
            Paragraph("<b>Scenario Flows</b>", table_cell),
            Paragraph("7 Scenario Documents<br/>(SC-01 to SC-07)", table_cell),
            Paragraph("As-Is vs To-Be Mermaid flows, actors, inputs/outputs, and <b>explicit exception paths</b> for every flow.", table_cell),
            Paragraph("<b>100% Complete</b>", table_cell)
        ],
        [
            Paragraph("<b>Business Scenario Document (BSD)</b>", table_cell),
            Paragraph("BSD-MFG-PP-PLM-001", table_cell),
            Paragraph("End-to-end blueprint integrating Scenarios 3, 4, and 6 (Demand Planning -> Order Execution -> ECM Cutover).", table_cell),
            Paragraph("<b>100% Complete</b>", table_cell)
        ],
        [
            Paragraph("<b>Functional Requirements (FRD)</b>", table_cell),
            Paragraph("FRD-MFG-PP-001<br/>(15 Requirements)", table_cell),
            Paragraph("Order release gates, ATP checks, milestone confirmations, scrap reason codes, and automatic Goods Receipt 101.", table_cell),
            Paragraph("<b>100% Complete</b>", table_cell)
        ],
        [
            Paragraph("<b>User Stories & Acceptance</b>", table_cell),
            Paragraph("20 Agile User Stories", table_cell),
            Paragraph("Standard Agile format with strict <i>Given/When/Then</i> criteria and negative/exception testing paths.", table_cell),
            Paragraph("<b>100% Complete</b>", table_cell)
        ],
        [
            Paragraph("<b>Data Mapping & Integration</b>", table_cell),
            Paragraph("57 Field Mappings +<br/>PLM-to-ERP Spec", table_cell),
            Paragraph("Field-level rules for Material, BOM, Work Center, Routing, and PLM EBOM-to-MBOM interface via SAP Integration Suite.", table_cell),
            Paragraph("<b>100% Complete</b>", table_cell)
        ],
        [
            Paragraph("<b>Testing & Verification</b>", table_cell),
            Paragraph("Test Plan + 25 Test Scripts (TC-MD-001 to TC-INT-001)", table_cell),
            Paragraph("SIT/UAT governance, preconditions, step-by-step transactions, and 100% pass verification.", table_cell),
            Paragraph("<b>100% Complete</b>", table_cell)
        ],
        [
            Paragraph("<b>Design Document (P1)</b>", table_cell),
            Paragraph("FS-QM-REP-001 (Defect Pareto Analytics)", table_cell),
            Paragraph("Fiori Analytical List Page / CDS view calculating real-time 80/20 scrap Pareto (reflecting Uno Minda shop floor work).", table_cell),
            Paragraph("<b>100% Complete</b>", table_cell)
        ],
        [
            Paragraph("<b>Workshop Agenda (P1)</b>", table_cell),
            Paragraph("WS-MFG-TRN-001", table_cell),
            Paragraph("3-day client blueprinting workshop agenda and role-based end-user training curriculum.", table_cell),
            Paragraph("<b>100% Complete</b>", table_cell)
        ],
        [
            Paragraph("<b>End-to-End Traceability</b>", table_cell),
            Paragraph("RTM-MFG-ALL-001", table_cell),
            Paragraph("100% bi-directional mapping from Scenario -> BSD -> Story -> FRD -> Test Case -> SAP Table.", table_cell),
            Paragraph("<b>100% Complete</b>", table_cell)
        ]
    ]
    deliv_table = Table(deliv_data, colWidths=[95, 115, 234, 60])
    deliv_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1B365D')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(deliv_table)
    story.append(Spacer(1, 10))
    
    # 4. Key S/4HANA Architectural Highlights
    story.append(Paragraph("4. Key S/4HANA Architectural & Functional Highlights", h1_style))
    
    highlights = [
        "<b>In-Memory MRP Live (MD01N):</b> Replaced traditional batch runs with HANA in-memory calculations, providing dynamic shortage detection and planned order scheduling in seconds.",
        "<b>Milestone Operation Confirmation & Backflushing:</b> Confirming milestone Op 0050 automatically triggers proportional confirmations for preceding operations (0010-0040) and auto-backflushes standard consumables (Movement 261).",
        "<b>Shop Floor Scrap Lockout & Reason Codes:</b> Enforces mandatory 4-digit scrap reason codes in CO11N. Scrap exceeding 3.0% triggers an automated QM notification (F2) and requires supervisor authorization object C_AFKO_AWA.",
        "<b>Engineering Change Cutover Governance:</b> Governs BOM revision level changes via Change Master CC01 with Valid-From dates, establishing clear cutover rules for active WIP production orders.",
        "<b>PLM-to-ERP Integration:</b> Transforms PLM EBOM into S/4HANA MBOM via SAP Integration Suite, dissolving CAD phantoms, injecting plant consumables, and routing exceptions to SAP AIF (/AIF/ERR)."
    ]
    for h in highlights:
        story.append(Paragraph(f"• {h}", bullet_style))
    story.append(Spacer(1, 8))
    
    # 5. Verified SAP Learning & Methodology
    story.append(Paragraph("5. Verified SAP Learning & Methodology Alignment", h1_style))
    story.append(Paragraph(
        "To ensure terminology, transactions, and business objects reflect authentic S/4HANA best practices, the deliverables align with official SAP curricula:",
        body_style
    ))
    story.append(Paragraph("• <b>SAP Learning Journey:</b> <i>Discovering SAP S/4HANA Manufacturing</i> (Master data, order lifecycles, and shop floor control).", bullet_style))
    story.append(Paragraph("• <b>SAP Learning Journey:</b> <i>Production Planning in SAP S/4HANA (S4200)</i> (MRP Live mechanics, Planning Strategy 40, lot sizes).", bullet_style))
    story.append(Paragraph("• <b>openSAP Course:</b> <i>Key Functional Capabilities in SAP S/4HANA</i> (Architecture, Fiori user experience, and integration).", bullet_style))
    story.append(Spacer(1, 8))
    
    # 6. Resume Integration & Interview Talking Points
    story.append(Paragraph("6. Resume Integration & Interview Talking Points", h1_style))
    story.append(Paragraph(
        "<b>Resume Bullets:</b><br/>"
        "• <i>Self-Initiated Project: SAP S/4HANA Manufacturing & PLM Coverage:</i> Authored consultant-grade documentation for discrete automotive assembly: 1 Business Scenario Document (BSD), 1 Functional Requirements Document (FRD), and 20 Agile user stories with Given/When/Then criteria.<br/>"
        "• Formulated master data mapping sheets for Material Master, BOM, Routing, and Work Centers, and defined an automated PLM-to-ERP integration specification.<br/>"
        "• Built a formal Quality Assurance Test Plan with 25 test cases, achieving 100% bi-directional traceability across requirements and S/4HANA objects.<br/>"
        "• Designed a Functional Specification for a Fiori Defect Pareto Analytics CDS view reflecting industrial shop floor failure diagnostics.",
        body_style
    ))
    story.append(Paragraph(
        "<b>One-Line Interview Statement:</b><br/>"
        "<i>\"I bring hands-on automotive shop floor diagnostic experience from Uno Minda and process engineering discipline from Technip Energies, combined with a verifiable, independently produced body of SAP S/4HANA functional consulting artifacts spanning PP, QM, and PLM.\"</i>",
        callout_style
    ))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF generated successfully!")

if __name__ == "__main__":
    generate_excel()
    generate_pdf()
