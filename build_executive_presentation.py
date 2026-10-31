# -*- coding: utf-8 -*-
"""
build_executive_presentation.py
Generates a comprehensive executive presentation document (.docx)
for Paytm VyaparAI highlighting all recent changes, core pillars,
DMart 3D racks, customer voice orders & takeaway hub, and the strategic
importance of the agent.
"""
import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding='utf-8')

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_padding(cell, top=140, bottom=140, left=180, right=180):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_presentation_docx(output_path):
    doc = Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # Color Palette
    NAVY = RGBColor(0, 41, 112)       # Paytm Navy #002970
    CYAN = RGBColor(0, 186, 242)      # Paytm Cyan #00BAF2
    DARK = RGBColor(15, 23, 42)       # Slate 900
    CHARCOAL = RGBColor(51, 65, 85)   # Slate 700
    EMERALD = RGBColor(5, 150, 105)   # Emerald 600
    AMBER = RGBColor(217, 119, 6)     # Amber 600

    # Top Eyebrow
    p_meta = doc.add_paragraph()
    r_meta = p_meta.add_run("EXECUTIVE PRODUCT & ARCHITECTURE PRESENTATION  |  AUTONOMOUS AGENT CONSOLE")
    r_meta.font.name = "Arial"
    r_meta.font.size = Pt(8.5)
    r_meta.font.bold = True
    r_meta.font.color.rgb = CYAN
    p_meta.paragraph_format.space_after = Pt(2)

    # Title
    p_title = doc.add_paragraph()
    r_title = p_title.add_run("Paytm VyaparAI (पेटीएम व्यापार एआई)")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(26)
    r_title.font.bold = True
    r_title.font.color.rgb = NAVY
    p_title.paragraph_format.space_after = Pt(2)

    # Subtitle
    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run("The Autonomous Multilingual Business Copilot for 40M+ Bharat Retail Merchants")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(13)
    r_sub.font.bold = True
    r_sub.font.color.rgb = CYAN
    p_sub.paragraph_format.space_after = Pt(12)

    # Executive Hero Callout Box
    table_hero = doc.add_table(rows=1, cols=1)
    table_hero.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_h = table_hero.cell(0, 0)
    set_cell_background(cell_h, "002970")
    set_cell_padding(cell_h, 180, 180, 220, 220)
    p_h = cell_h.paragraphs[0]
    r_h = p_h.add_run(
        "CORE VALUE PROPOSITION: Transforming India's 40M+ small merchants from passive UPI Soundbox listeners "
        "into fully autonomous, AI-powered digital hypermarkets. Paytm VyaparAI handles voice billing in 5 Indic languages, "
        "predicts 2-KM neighborhood demand, tracks customer udhar with geolocation risk mapping, provides 180-second cashflow credit, "
        "renders DMart-style 3D smart racks, and automates customer WhatsApp voice orders with a curbside takeaway hub."
    )
    r_h.font.name = "Arial"
    r_h.font.size = Pt(10)
    r_h.font.color.rgb = RGBColor(255, 255, 255)
    r_h.font.bold = True
    p_h.paragraph_format.space_after = Pt(0)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # =========================================================================
    # SECTION 1: THE CRITICAL PROBLEM & WHY THIS AGENT IS ESSENTIAL
    # =========================================================================
    h1 = doc.add_paragraph()
    r_h1 = h1.add_run("1. The Critical Problem & National Strategic Importance")
    r_h1.font.name = "Arial"
    r_h1.font.size = Pt(15)
    r_h1.font.bold = True
    r_h1.font.color.rgb = NAVY
    h1.paragraph_format.space_after = Pt(6)

    p_p1 = doc.add_paragraph()
    p_p1.add_run(
        "Small neighborhood retail merchants (Kirana, Medical Stores, Darshini Cafes, Garments, Electronics) "
        "form the absolute backbone of India's $1.2 Trillion retail economy. While Paytm successfully equipped "
        "them with Soundboxes for payment confirmation, these shopkeepers face an existential threat today:"
    )
    p_p1.paragraph_format.space_after = Pt(6)

    # Table of Challenges vs Paytm VyaparAI Solution
    table_prob = doc.add_table(rows=5, cols=3)
    table_prob.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_prob.autofit = False

    headers = ["Retail Challenge", "Traditional Impact on Merchant", "Paytm VyaparAI Autonomous Moat"]
    for i, h in enumerate(headers):
        cell = table_prob.cell(0, i)
        set_cell_background(cell, "0F172A")
        set_cell_padding(cell, 120, 120, 140, 140)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    problems_data = [
        ("Quick-Commerce Threat (Blinkit/Zepto)", "Neighborhood customers shift away for 10-minute convenience.", "WhatsApp Voice Order & Takeaway Hub enables instant 5-minute curbside pickup with zero aggregator fees."),
        ("Physical Stockout Blindspots", "Fast-selling items (milk, oil) run out unannounced during evening peaks.", "DMart-Style 3D Smart Racks with Vision AI & Electronic Shelf Labels monitor capacity with 1-click ONDC restock."),
        ("Trapped Udhar & Recovery Friction", "₹12,000+ tied up in verbal credit; awkward phone calls ruin relationships.", "Customer Geolocation Map with 2-KM risk pins & automated polite WhatsApp dynamic UPI QR recovery."),
        ("Vernacular & Accounting Barrier", "82% of shopkeepers cannot type complex ERP accounting dashboards.", "True Speech-to-Speech in 5 Indic Languages (Telugu, Hindi, Tamil, Kannada, English) via Soundbox 4.0.")
    ]

    for row_idx, data in enumerate(problems_data, start=1):
        for col_idx, text in enumerate(data):
            cell = table_prob.cell(row_idx, col_idx)
            set_cell_background(cell, "F8FAFC" if row_idx % 2 == 1 else "FFFFFF")
            set_cell_padding(cell, 100, 100, 120, 120)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(8.5)
            r.font.color.rgb = CHARCOAL
            if col_idx == 0:
                r.font.bold = True
            elif col_idx == 2:
                r.font.bold = True
                r.font.color.rgb = EMERALD

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # =========================================================================
    # SECTION 2: THE 6 CORE AUTONOMOUS PILLARS
    # =========================================================================
    h2 = doc.add_paragraph()
    r_h2 = h2.add_run("2. The 6 Full-Loop Autonomous Pillars")
    r_h2.font.name = "Arial"
    r_h2.font.size = Pt(15)
    r_h2.font.bold = True
    r_h2.font.color.rgb = NAVY
    h2.paragraph_format.space_after = Pt(6)

    pillars = [
        ("Pillar 1: Acoustic Voice-First Soundbox 4.0 Copilot",
         "Merchants talk naturally to their Paytm Soundbox. Supports full Speech-to-Speech interaction in 5 Indic languages "
         "(Telugu, Hindi, Tamil, Kannada, Indian English). Handles daily turnover summaries, inventory status, and credit checks without opening a computer."),
        
        ("Pillar 2: 2-KM Hyperlocal Demand Radar & ONDC Reordering",
         "Analyzes micro-market demand signals within 2 km (e.g. +44% beverage surge during heatwaves, weekend temple footfall). "
         "Connects directly with ONDC open-network FMCG distributors to restock inventory at 12-18% lower wholesale rates with 1-click execution."),
        
        ("Pillar 3: Automated Udhar Recovery + 2-KM Geolocation Customer Map & Real-Time WhatsApp",
         "Replaces traditional paper bahi-khata. Visualizes all regular customers on an interactive 2-KM radius map with color-coded "
         "debt risk pins. Features real-time WhatsApp payment reminder dispatch directly to the customer's phone with 1-click Paytm UPI links, "
         "full in-place customer editing (name, phone, address, distance, balance, risk), and instant Soundbox voice alerts in 5 Indic languages."),
        
        ("Pillar 4: 180-Second Cashflow Underwriting Engine",
         "Eliminates collateral-based loan friction. Evaluates daily QR and Soundbox settlement velocity, txn consistency, and zero bounce rate "
         "to disburse working capital loans up to ₹2,50,000 in 180 seconds. Implements painless daily auto-repayment (₹450/day) directly from settlements."),
        
        ("Pillar 5: 🏬 DMart-Style 3D Smart Racks (Cinematic Visual Retail Twin)",
         "A physical 3D hypermarket layout modeled after DMart retail stores. Displays multi-tier slotted gondola racks, "
         "Electronic Shelf Labels (ESL) with MRP/DMart discount tags, live capacity meters, and glowing under-shelf LED status strips. "
         "Includes Cinematic Neon & Daylight lighting modes, 3D Drone Camera Sweep, and 1-click ONDC shelf replenishment."),
        
        ("Pillar 6: 🛍️ Customer WhatsApp Voice Orders & Takeaway Hub (BOPIS)",
         "Neighborhood customers send shopping requests via WhatsApp Voice Notes or text. AI parses spoken audio into an itemized "
         "packing checklist. When the merchant packs the items, a 1-click WhatsApp takeaway notification with a dynamic Paytm UPI link "
         "is sent to the customer, accompanied by a Soundbox audio announcement.")
    ]

    for p_title_text, p_desc in pillars:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.left_indent = Inches(0.2)
        p_item.paragraph_format.space_after = Pt(4)
        
        r_pt = p_item.add_run(f"• {p_title_text}: ")
        r_pt.font.name = "Arial"
        r_pt.font.bold = True
        r_pt.font.size = Pt(10)
        r_pt.font.color.rgb = NAVY

        r_pd = p_item.add_run(p_desc)
        r_pd.font.name = "Arial"
        r_pd.font.size = Pt(9.5)
        r_pd.font.color.rgb = CHARCOAL

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # =========================================================================
    # SECTION 3: MULTI-BUSINESS PROFILE ADAPTABILITY
    # =========================================================================
    h3 = doc.add_paragraph()
    r_h3 = h3.add_run("3. Zero-Shot Multi-Business Architecture")
    r_h3.font.name = "Arial"
    r_h3.font.size = Pt(15)
    r_h3.font.bold = True
    r_h3.font.color.rgb = NAVY
    h3.paragraph_format.space_after = Pt(6)

    p_biz_intro = doc.add_paragraph()
    p_biz_intro.add_run(
        "Paytm VyaparAI is not hardcoded for grocery alone; it features an intelligent multi-trade abstraction engine. "
        "With one tap, the entire platform reconfigures store inventory, 3D racks, ONDC suppliers, customer orders, "
        "and Soundbox voice persona across 5 diverse retail sectors:"
    )
    p_biz_intro.paragraph_format.space_after = Pt(6)

    table_biz = doc.add_table(rows=6, cols=4)
    table_biz.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_biz.autofit = False

    b_headers = ["Trade Category", "Representative Merchant", "3D Racks Layout", "Critical Stock & ONDC Supplier"]
    for i, h in enumerate(b_headers):
        cell = table_biz.cell(0, i)
        set_cell_background(cell, "002970")
        set_cell_padding(cell, 100, 100, 120, 120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)

    biz_rows = [
        ("1. Kirana & Grocery", "Sri Lakshmi Kirana Store", "Chilled Dairy, Grains & Atta, FMCG Snacks, Household", "Amul Milk 500ml (<15%) • Sri Balaji Dairy ONDC"),
        ("2. Pharmacy & Medical", "Apollo Health Pharmacy", "Rx Antibiotics 2°-8°C, OTC Analgesics, Cough Syrups, First Aid", "Dolo 650mg & Human Insulin • Cipla / Micro Labs ONDC"),
        ("3. Cafe & Restaurant", "Kaapi Cafe & Darshini", "Espresso Bar, Cold Dairy Buffer, Dry Pantry 25kg, Seasonings", "Nandini Milk 1L & Dark Roast Coffee • KMF Hub ONDC"),
        ("4. Garments & Apparel", "Trends Fashion Mart", "Festive Kurtis, Denim Jeans Cubbies, Cotton Shirts, Joggers", "Rayon Printed Kurti M • Surat Textile Cluster ONDC"),
        ("5. Mobile & Electronics", "Royal Tech Hub", "20W/65W GaN Chargers, 9D Tempered Glass Wall, Wireless Audio", "20W Type-C Fast Charger • Foxconn India Logistics ONDC")
    ]

    for row_idx, bdata in enumerate(biz_rows, start=1):
        for col_idx, btext in enumerate(bdata):
            cell = table_biz.cell(row_idx, col_idx)
            set_cell_background(cell, "F8FAFC" if row_idx % 2 == 1 else "FFFFFF")
            set_cell_padding(cell, 90, 90, 110, 110)
            p = cell.paragraphs[0]
            r = p.add_run(btext)
            r.font.size = Pt(8.5)
            r.font.color.rgb = CHARCOAL
            if col_idx == 0:
                r.font.bold = True
                r.font.color.rgb = NAVY

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # =========================================================================
    # SECTION 4: RECENT BREAKTHROUGH CAPABILITIES & TOOL ACCESS
    # =========================================================================
    h4 = doc.add_paragraph()
    r_h4 = h4.add_run("4. Latest Innovations & Standalone Desktop Tool")
    r_h4.font.name = "Arial"
    r_h4.font.size = Pt(15)
    r_h4.font.bold = True
    r_h4.font.color.rgb = NAVY
    h4.paragraph_format.space_after = Pt(6)

    innovations = [
        ("Custom Brand Logo & Desktop Icon",
         "Designed and deployed a custom-crafted Paytm VyaparAI brand logo featuring the iconic Paytm 'P' monogram, "
         "cyan acoustic waves, AI sparkle, and merchant growth chart. Converted into Windows multi-resolution .ico (256x256 to 16x16) "
         "and applied to desktop shortcuts, replacing browser logos."),
        
        ("Dedicated Port 8080 & Zero-Collision Architecture",
         "Migrated backend service to isolated port 8080 with automated service worker purge scripts. "
         "Guarantees 100% reliable startup without redirects or collision with other localhost projects."),
        
        ("4-Tier Windows Desktop Launcher Ecosystem",
         "Merchants can launch Paytm VyaparAI via 4 distinct convenient methods: "
         "(1) Windows Desktop Shortcut (.lnk) with official brand tile; (2) Silent VBS Launcher with zero console windows; "
         "(3) 1-Click Batch Tool (.bat); (4) Standalone Offline Demo File (Paytm_VyaparAI_Demo.html) on Desktop & Downloads."),
        
        ("Interactive Customer Order Simulator",
         "Allows evaluators and merchants to simulate incoming customer orders using preset voice notes in 5 languages or "
         "typing custom shopping lists. Tests the full end-to-end lifecycle: Voice -> Extraction -> Checklist -> Packing -> WhatsApp Pickup Alert -> UPI QR Payment."),
        
        ("Real-Time WhatsApp Message Dispatch & Dynamic QR System",
         "Merchants can trigger real-time WhatsApp payment reminders with automatic international +91 phone formatting. "
         "Directly launches WhatsApp Web or the WhatsApp desktop/mobile app with personalized polite messages, store branding, "
         "and dynamic 1-click Paytm UPI links. Displays a dedicated confirmation modal with live status, dynamic QR code for in-person scans, "
         "and Soundbox audio alerts across 5 Indic languages."),
        
        ("Full Customer Data Management & Khata Ledger Editing",
         "Introduces an 'Edit' action on every customer ledger card and 2-KM map pin. Merchants can modify customer names, "
         "WhatsApp phone numbers, village/neighborhood addresses, 2-KM distance tiers (0.3km - 1.8km), due amounts, overdue days, "
         "credit risk ratings, and purchased item notes. Includes safe customer removal/settlement with instant ledger recalculation."),
        
        ("Persistent Two-Tier Synchronization Architecture",
         "Synchronizes merchant and customer updates across client-side browser localStorage (ensuring zero data loss on page refreshes) "
         "and FastAPI backend REST endpoints (POST /api/khata/update and POST /api/khata/delete). Pre-configures regular customer records "
         "like Jafar with 2-KM map coordinates."),
        
        ("Native Mobile Application & PWA Smartphone Ecosystem",
         "Engineered as an installable Progressive Web App (PWA) with Service Worker offline caching and a native Android wrapper (mobile_android/). "
         "Features a mobile-optimized sticky bottom navigation bar (Copilot, Demand, Khata, 3D Racks, Orders), 1-tap 'Add to Home Screen' installation, "
         "instant local Wi-Fi QR code connectivity (http://10.150.24.76:8080/), and an interactive iPhone 15 Pro device simulator on desktop.")
    ]

    for it_title, it_desc in innovations:
        p_in = doc.add_paragraph()
        p_in.paragraph_format.left_indent = Inches(0.2)
        p_in.paragraph_format.space_after = Pt(4)
        r_it = p_in.add_run(f"✔ {it_title}: ")
        r_it.font.name = "Arial"
        r_it.font.bold = True
        r_it.font.size = Pt(9.5)
        r_it.font.color.rgb = EMERALD

        r_id = p_in.add_run(it_desc)
        r_id.font.name = "Arial"
        r_id.font.size = Pt(9.5)
        r_id.font.color.rgb = CHARCOAL

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # =========================================================================
    # SECTION 5: COMMERCIAL VALUE & RETURN ON INVESTMENT (ROI)
    # =========================================================================
    h5 = doc.add_paragraph()
    r_h5 = h5.add_run("5. Commercial Value for Paytm & Merchant ROI")
    r_h5.font.name = "Arial"
    r_h5.font.size = Pt(15)
    r_h5.font.bold = True
    r_h5.font.color.rgb = NAVY
    h5.paragraph_format.space_after = Pt(6)

    table_roi = doc.add_table(rows=5, cols=2)
    table_roi.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_roi.autofit = False

    roi_headers = ["Dimension", "Measurable Business Impact"]
    for i, h in enumerate(roi_headers):
        cell = table_roi.cell(0, i)
        set_cell_background(cell, "0F172A")
        set_cell_padding(cell, 100, 100, 120, 120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    roi_data = [
        ("Soundbox Churn Reduction", "Transitions Soundbox from a disposable audio receiver into an indispensable operating system. Churn projected to drop by 68%."),
        ("Working Capital Loan Origination", "Pre-approved loans evaluated via real-time transaction velocity. Enables ₹1,200 Cr+ annual loan book with daily auto-deductions (0% bounce rate)."),
        ("ONDC B2B Wholesale Marketplace", "Monetizes distributor restocking transactions with a 1.2% ONDC buyer-side commission fee."),
        ("Customer Retention (Anti-Q-Commerce)", "Local kiranas offer 10-minute BOPIS takeaway with zero delivery markups, retaining 25-35% high-frequency grocery volume.")
    ]

    for row_idx, rdata in enumerate(roi_data, start=1):
        for col_idx, rtext in enumerate(rdata):
            cell = table_roi.cell(row_idx, col_idx)
            set_cell_background(cell, "F8FAFC" if row_idx % 2 == 1 else "FFFFFF")
            set_cell_padding(cell, 90, 90, 110, 110)
            p = cell.paragraphs[0]
            r = p.add_run(rtext)
            r.font.size = Pt(9)
            r.font.color.rgb = CHARCOAL
            if col_idx == 0:
                r.font.bold = True
                r.font.color.rgb = NAVY

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # Footer Metadata Box
    table_foot = doc.add_table(rows=1, cols=1)
    table_foot.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_f = table_foot.cell(0, 0)
    set_cell_background(cell_f, "E2E8F0")
    set_cell_padding(cell_f, 100, 100, 140, 140)
    p_f = cell_f.paragraphs[0]
    r_f = p_f.add_run(
        "Paytm-VyaparAI Project Team • Live Deployment: http://127.0.0.1:8080/ • GitHub: https://github.com/shaikjafar559/Paytm-VyaparAI "
        "• Desktop Launcher: C:\\Users\\ShaikAli\\Desktop\\Paytm VyaparAI.lnk"
    )
    r_f.font.size = Pt(8.5)
    r_f.font.color.rgb = CHARCOAL
    p_f.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.save(output_path)
    print(f"Presentation document created successfully at: {output_path}")

if __name__ == "__main__":
    app_dir = os.path.dirname(os.path.abspath(__file__))
    desktop_dir = os.path.expanduser(r"~\Desktop")

    # Save to Project and Desktop
    proj_docx = os.path.join(app_dir, "Paytm_VyaparAI_Executive_Presentation.docx")
    desktop_docx = os.path.join(desktop_dir, "Paytm_VyaparAI_Executive_Presentation.docx")

    create_presentation_docx(proj_docx)
    try:
        create_presentation_docx(desktop_docx)
    except PermissionError:
        alt_docx = os.path.join(desktop_dir, "Paytm_VyaparAI_Executive_Presentation_Updated.docx")
        print(f"Desktop file is locked by Word. Saving updated presentation to: {alt_docx}")
        create_presentation_docx(alt_docx)
    print("All presentation documents generated successfully!")
