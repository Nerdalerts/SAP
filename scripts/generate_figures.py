"""
Script to generate high-resolution, executive-grade engineering figures for:
1. docs/images/fig1_defect_pareto_analysis.png
2. docs/images/fig2_assembly_station_cycle_times.png
3. docs/images/fig3_s4hana_order_lifecycle.png
4. docs/images/fig4_plm_ebom_to_mbom_pipeline.png
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

# Set global matplotlib parameters for clean corporate publication styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#CBD5E0'
plt.rcParams['axes.linewidth'] = 0.8

IMG_DIR = r"C:\Users\PC\Desktop\SAP\docs\images"
os.makedirs(IMG_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# Figure 1: Shop-Floor Defect Pareto Analysis (80/20 Rule)
# -----------------------------------------------------------------------------
def make_fig1():
    fig, ax1 = plt.subplots(figsize=(10, 5.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax1.set_facecolor('#FAFAFA')

    defects = [
        "Photometric Below Spec\n(< 28k cd) [OPT-01]",
        "Adhesive Seal Void\nBead Gap [SEAL-02]",
        "Inner Lens Fogging /\nMoisture [FOG-03]",
        "Harness Terminal\nPin Fault [HAR-04]",
        "Fastener Stripping /\nBoss Crack [SCR-05]",
        "Cosmetic Coating\nBlemish [VIS-06]"
    ]
    freq = [34.2, 26.5, 18.7, 11.4, 5.8, 3.4]
    cum_freq = np.cumsum(freq)
    x = np.arange(len(defects))

    # Bar chart
    bars = ax1.bar(x, freq, color='#1A365D', width=0.55, edgecolor='#0F233E', linewidth=1, zorder=3, label="Defect Frequency (%)")
    
    # Dual axis for cumulative line
    ax2 = ax1.twinx()
    line = ax2.plot(x, cum_freq, color='#DD6B20', marker='o', linewidth=2.5, markersize=7, zorder=4, label="Cumulative (%)")

    # 80% Pareto Reference Line
    ax2.axhline(80, color='#E53E3E', linestyle='--', linewidth=1.5, alpha=0.85, zorder=2)
    ax2.text(4.2, 81.5, '80% Pareto Threshold', color='#C53030', fontweight='bold', fontsize=9.5)

    # Shaded vital few zone
    ax1.axvspan(-0.4, 2.4, color='#EBF8FF', alpha=0.6, zorder=1)
    ax1.text(1.0, 31, 'Top 3 Defect Categories = 79.4% of Total Line Scrap\n(Vital Few: Optics, PUR Sealing, Moisture Hermetics)', 
             ha='center', fontsize=9, fontweight='bold', color='#2B6CB0',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFFFFF', edgecolor='#BEE3F8', alpha=0.9))

    # Add data labels
    for bar in bars:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., h + 0.8, f'{h:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1A365D')

    for i, c in enumerate(cum_freq):
        ax2.text(i, c + 2.2, f'{c:.1f}%', ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#C05621')

    ax1.set_ylabel('Defect Frequency per 1,000 Units (%)', fontsize=10.5, fontweight='bold', color='#1A365D')
    ax2.set_ylabel('Cumulative Percentage (%)', fontsize=10.5, fontweight='bold', color='#C05621')
    ax1.set_xticks(x)
    ax1.set_xticklabels(defects, fontsize=8.5, rotation=0, ha='center', fontweight='medium')
    ax1.set_ylim(0, 42)
    ax2.set_ylim(0, 110)

    ax1.grid(axis='y', linestyle=':', alpha=0.4, color='#A0AEC0', zorder=0)
    ax1.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)

    plt.title('Figure 1: Automotive Headlamp Assembly Shop-Floor Defect Pareto Analysis (Uno Minda Field Diagnostics)', 
              fontsize=11.5, fontweight='bold', pad=18, color='#0F2A4A', ha='center')

    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fig1_defect_pareto_analysis.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print("Fig 1 generated:", out_path)

# -----------------------------------------------------------------------------
# Figure 2: Assembly Routing Cycle Times & Standard Values
# -----------------------------------------------------------------------------
def make_fig2():
    fig, ax = plt.subplots(figsize=(10.5, 5.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFA')

    work_centers = [
        "WC-ASSY-01\nHousing Prep",
        "WC-OPT-02\nOptics Align",
        "WC-GLUE-03\nRobotic PUR",
        "WC-CURE-04\nCure Tunnel",
        "WC-TST-05\n[M1] Photom.",
        "WC-LEAK-06\nLeak Chamber",
        "WC-PKG-07\n[M2] Final Pack"
    ]
    
    setup_time = [15.0, 20.0, 25.0, 10.0, 15.0, 10.0, 10.0]
    machine_time = [0.0, 30.0, 45.0, 90.0, 60.0, 40.0, 0.0]
    labor_time = [120.0, 150.0, 15.0, 30.0, 60.0, 20.0, 50.0]
    
    x = np.arange(len(work_centers))
    width = 0.24

    b1 = ax.bar(x - width, setup_time, width, label='Setup Time (VGW01)', color='#718096', edgecolor='#4A5568')
    b2 = ax.bar(x, machine_time, width, label='Machine Time (VGW02)', color='#2B6CB0', edgecolor='#1A365D')
    b3 = ax.bar(x + width, labor_time, width, label='Labor Time (VGW03)', color='#319795', edgecolor='#234E52')

    # Highlight milestones
    ax.text(4, 130, '[Milestone 1: Op 0050]\nAuto-confirms Op 10-40\nAuto-backflushes PUR/Gaskets', 
            ha='center', fontsize=8, fontweight='bold', color='#2C5282',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#EBF8FF', edgecolor='#90CDF4'))

    ax.text(6, 75, '[Milestone 2: Op 0070]\nAuto-GR Mov 101 to 101A\nStatus: CNF DLV', 
            ha='center', fontsize=8, fontweight='bold', color='#22543D',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#F0FFF4', edgecolor='#9AE6B4'))

    # Line Bottleneck Annotation
    ax.annotate('Curing Capacity Bottleneck\n(90 min Machine Cycle)', xy=(3, 90), xytext=(2.6, 125),
                arrowprops=dict(arrowstyle="->", color="#C53030", lw=1.5),
                fontsize=8, fontweight='bold', color='#C53030',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF5F5', edgecolor='#FEB2B2'))

    ax.set_ylabel('Standard Minutes per 100 Headlamp Assemblies', fontsize=10, fontweight='bold', color='#1A365D')
    ax.set_xticks(x)
    ax.set_xticklabels(work_centers, fontsize=8.5, fontweight='medium')
    ax.set_ylim(0, 175)
    ax.grid(axis='y', linestyle=':', alpha=0.4, color='#A0AEC0')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E0', fontsize=9, loc='upper left')

    plt.title('Figure 2: Assembly Routing Standard Values & Work Center Operation Times (Base Qty: 100 EA)', 
              fontsize=11.5, fontweight='bold', pad=18, color='#0F2A4A', ha='center')

    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fig2_assembly_station_cycle_times.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print("Fig 2 generated:", out_path)

# -----------------------------------------------------------------------------
# Figure 3: SAP S/4HANA Order Lifecycle & Milestone Execution Architecture
# -----------------------------------------------------------------------------
def make_fig3():
    fig, ax = plt.subplots(figsize=(11, 4.8), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.axis('off')

    # Draw lifecycle cards
    stages = [
        {"code": "CRTD", "title": "Order Created", "sub": "CO01 / CO40\nBOM & Routing copied\nReservations (RESB)", "col": "#E2E8F0", "text_col": "#2D3748"},
        {"code": "REL", "title": "Order Released", "sub": "CO02 Availability Check\nStatus MACM (ATP Pass)\nBarcoded Travelers printed", "col": "#BEE3F8", "text_col": "#2B6CB0"},
        {"code": "PCNF", "title": "Milestone Confirmed", "sub": "CO11N Op 0050 (Darkroom)\nAuto-confirms Op 0010-0040\nBackflush Mov 261 PUR", "col": "#FEFCBF", "text_col": "#B7791F"},
        {"code": "CNF / DLV", "title": "Final Pack & GR", "sub": "CO11N Op 0070 (Pack)\nAuto Movement 101 to 101A\nStock Unrestricted", "col": "#C6F6D5", "text_col": "#22543D"},
        {"code": "TECO", "title": "Tech Completed", "sub": "CO02 Functions TECO\nClear open reservations\nReady for Variance (KO88)", "col": "#E9D8FD", "text_col": "#6B46C1"}
    ]

    card_width = 1.7
    card_height = 2.4
    y_pos = 1.2

    for i, s in enumerate(stages):
        x_pos = 0.5 + i * 2.1
        
        # Draw box
        rect = patches.FancyBboxPatch((x_pos, y_pos), card_width, card_height,
                                      boxstyle="round,pad=0.1,rounding_size=0.15",
                                      facecolor=s["col"], edgecolor="#A0AEC0", linewidth=1.2, zorder=2)
        ax.add_patch(rect)
        
        # Header box
        hdr = patches.FancyBboxPatch((x_pos, y_pos + card_height - 0.65), card_width, 0.65,
                                     boxstyle="round,pad=0.08,rounding_size=0.12",
                                     facecolor="#1A365D", edgecolor="#1A365D", zorder=3)
        ax.add_patch(hdr)

        # Header Text
        ax.text(x_pos + card_width/2, y_pos + card_height - 0.35, s["code"],
                ha='center', va='center', color='#FFFFFF', fontweight='bold', fontsize=11, zorder=4)

        # Title
        ax.text(x_pos + card_width/2, y_pos + card_height - 0.95, s["title"],
                ha='center', va='center', color=s["text_col"], fontweight='bold', fontsize=9.5, zorder=4)

        # Body Text
        ax.text(x_pos + card_width/2, y_pos + 0.6, s["sub"],
                ha='center', va='center', color='#2D3748', fontsize=7.8, zorder=4, linespacing=1.3)

        # Arrow to next
        if i < len(stages) - 1:
            ax.annotate('', xy=(x_pos + card_width + 0.35, y_pos + card_height/2),
                        xytext=(x_pos + card_width + 0.05, y_pos + card_height/2),
                        arrowprops=dict(arrowstyle="->", color="#4A5568", lw=2.2))

    # Add Quality & Exception Overlays
    rect_qm = patches.FancyBboxPatch((4.7, 0.1), 3.8, 0.8,
                                     boxstyle="round,pad=0.1,rounding_size=0.1",
                                     facecolor="#FFF5F5", edgecolor="#FEB2B2", linewidth=1.0)
    ax.add_patch(rect_qm)
    ax.text(6.6, 0.5, "Integrated QM & Scrap Guardrails:\n• In-Process Lot Origin 03 (QE51N) • Mandatory 4-digit Scrap Reasons\n• Scrap > 3% triggers Supervisor Lockout (C_AFKO_AWA) & QM Defect F2",
            ha='center', va='center', color='#9B2C2C', fontsize=7.5, fontweight='bold')

    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.2)
    plt.title('Figure 3: SAP S/4HANA Discrete Production Order Lifecycle, Status Gates & Shop-Floor Trigger Points', 
              fontsize=11.5, fontweight='bold', pad=14, color='#0F2A4A', ha='center')

    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fig3_s4hana_order_lifecycle.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print("Fig 3 generated:", out_path)

# -----------------------------------------------------------------------------
# Figure 4: PLM EBOM-to-MBOM Integration Pipeline
# -----------------------------------------------------------------------------
def make_fig4():
    fig, ax = plt.subplots(figsize=(11, 4.8), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.axis('off')

    # Box 1: PLM EBOM
    b1 = patches.FancyBboxPatch((0.4, 0.8), 2.9, 3.2, boxstyle="round,pad=0.1", facecolor='#F7FAFC', edgecolor='#CBD5E0', lw=1.2)
    ax.add_patch(b1)
    ax.text(1.85, 3.7, "PLM System (Teamcenter/Windchill)\nEngineering BOM (EBOM)", ha='center', va='center', fontweight='bold', fontsize=9, color='#1A365D')
    ebom_items = "• 3D CAD Geometry & Assemblies\n• Structural Groupings\n• Virtual CAD Phantoms\n  (e.g., VIRT-OPT-BRKT)\n• Engineering Revisions (Rev A -> B)\n• Non-ISO Units (Inches, Each)\n• No Packaging / Consumables"
    ax.text(1.85, 2.1, ebom_items, ha='center', va='center', fontsize=7.8, color='#4A5568', linespacing=1.3)

    # Box 2: Middleware
    b2 = patches.FancyBboxPatch((4.0, 0.8), 3.0, 3.2, boxstyle="round,pad=0.1", facecolor='#EBF8FF', edgecolor='#90CDF4', lw=1.2)
    ax.add_patch(b2)
    ax.text(5.5, 3.7, "SAP Integration Suite (Cloud Int.)\nTransformation Rules Engine", ha='center', va='center', fontweight='bold', fontsize=9, color='#2B6CB0')
    mid_items = "1. Dissolve CAD Phantoms:\n   Flatten virtual nodes to parent\n2. Consumable Recipe Injection:\n   Inject 0.045 KG PUR (HL-ADH-501)\n3. Packaging Injection:\n   Add carton HL-PKG-801\n4. ISO Value Mapping (UoM/Types)\n5. Error Queue: SAP AIF (/AIF/ERR)"
    ax.text(5.5, 2.1, mid_items, ha='center', va='center', fontsize=7.8, color='#2C5282', linespacing=1.3)

    # Box 3: S/4HANA MBOM
    b3 = patches.FancyBboxPatch((7.7, 0.8), 2.9, 3.2, boxstyle="round,pad=0.1", facecolor='#F0FFF4', edgecolor='#9AE6B4', lw=1.2)
    ax.add_patch(b3)
    ax.text(9.15, 3.7, "SAP S/4HANA Core\nManufacturing BOM (MBOM)", ha='center', va='center', fontweight='bold', fontsize=9, color='#22543D')
    mbom_items = "• Plant 1010, BOM Usage 1\n• Item Category L (Stock Items)\n• Component Scrap % (3% PUR)\n• Line Storage Locs (101B, 101C)\n• Backflush Flags (RGEKZ = 1)\n• Component Allocation to Ops\n• Standard Cost Released (CK24)"
    ax.text(9.15, 2.1, mbom_items, ha='center', va='center', fontsize=7.8, color='#276749', linespacing=1.3)

    # Arrows
    ax.annotate('', xy=(3.9, 2.4), xytext=(3.4, 2.4), arrowprops=dict(arrowstyle="->", color="#2B6CB0", lw=2.2))
    ax.text(3.65, 2.65, "JSON / REST\nWebhook", ha='center', fontsize=7, fontweight='bold', color='#2B6CB0')

    ax.annotate('', xy=(7.6, 2.4), xytext=(7.1, 2.4), arrowprops=dict(arrowstyle="->", color="#22543D", lw=2.2))
    ax.text(7.35, 2.65, "OData v2/v4\nAPI_BOM", ha='center', fontsize=7, fontweight='bold', color='#22543D')

    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.4)
    plt.title('Figure 4: Automated Engineering-to-Manufacturing Handoff Pipeline (PLM EBOM -> SAP S/4HANA MBOM)', 
              fontsize=11.5, fontweight='bold', pad=14, color='#0F2A4A', ha='center')

    plt.tight_layout()
    out_path = os.path.join(IMG_DIR, "fig4_plm_ebom_to_mbom_pipeline.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print("Fig 4 generated:", out_path)

if __name__ == "__main__":
    make_fig1()
    make_fig2()
    make_fig3()
    make_fig4()
    print("All 4 figures generated successfully!")
