import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def create_pitch_docx(filename):
    doc = Document()

    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    NAVY = RGBColor(0, 41, 112)
    CYAN = RGBColor(0, 186, 242)
    CHARCOAL = RGBColor(30, 41, 59)
    GRAY = RGBColor(100, 116, 139)

    # Document Header
    p_track = doc.add_paragraph()
    r_track = p_track.add_run("MULTILINGUAL AI BUSINESS PARTNER  |  ENGLISH • TELUGU • HINDI • TAMIL • KANNADA")
    r_track.font.name = "Arial"
    r_track.font.size = Pt(10)
    r_track.font.bold = True
    r_track.font.color.rgb = CYAN
    p_track.paragraph_format.space_after = Pt(4)

    # Document Title
    p_title = doc.add_paragraph()
    r_title = p_title.add_run("Paytm VyaparAI")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(26)
    r_title.font.bold = True
    r_title.font.color.rgb = NAVY
    p_title.paragraph_format.space_after = Pt(2)

    # Subtitle
    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run("The Autonomous Multilingual AI Business Partner for 40M+ Bharat Merchants")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(14)
    r_sub.font.bold = True
    r_sub.font.color.rgb = CYAN
    p_sub.paragraph_format.space_after = Pt(12)

    # Summary Callout Box
    table_callout = doc.add_table(rows=1, cols=1)
    table_callout.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_c = table_callout.cell(0, 0)
    set_cell_background(cell_c, "F1F5F9")
    p_c = cell_c.paragraphs[0]
    r_c = p_c.add_run(
        "Executive Summary: Paytm VyaparAI transforms India's iconic Soundbox and POS terminal into an active business partner with native voice support in 5 Indian languages: English, Telugu (తెలుగు), Hindi (हिंदी), Tamil (தமிழ்), and Kannada (ಕನ್ನಡ). "
        "By merging Indic voice recognition with Paytm's real-time transaction velocity, VyaparAI automates inventory demand forecasting, "
        "recovers trapped udhar (credit), enables 1-tap ONDC wholesale restocking, and delivers pre-approved 3-minute working capital credit."
    )
    r_c.font.name = "Arial"
    r_c.font.size = Pt(10)
    r_c.font.color.rgb = CHARCOAL
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    def add_section_header(title):
        p = doc.add_paragraph()
        r = p.add_run(title)
        r.font.name = "Arial"
        r.font.size = Pt(15)
        r.font.bold = True
        r.font.color.rgb = NAVY
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)

    # 1. Problem Statement
    add_section_header("1. Problem Statement: The 4 Growth Blindspots Beyond Payments")
    problems = [
        ("Dead Stock & Trapped Working Capital: ", "25% to 30% of working capital is tied up in slow-moving or expired SKUs due to reliance on merchant intuition without data intelligence."),
        ("Sticky Udhar & Delayed Cash Recovery: ", "₹1.5 Lakh to ₹3.0 Lakh is locked in paper khata registers. Merchants hesitate to chase customers, creating liquidity crunches."),
        ("Zero Hyper-Local Market Visibility: ", "Small kiranas lose 15% wallet share to quick-commerce apps because they operate in isolation and miss neighborhood demand surges."),
        ("The Language & Typing Barrier: ", "82% of traditional merchants reject English software apps. Counter operations require native voice interaction in Telugu, Tamil, Kannada, Hindi, and English.")
    ]
    for p_title_text, p_body in problems:
        p_item = doc.add_paragraph(style='List Bullet')
        r_pt = p_item.add_run(p_title_text)
        r_pt.font.bold = True
        r_pt.font.color.rgb = NAVY
        r_pb = p_item.add_run(p_body)
        r_pb.font.color.rgb = CHARCOAL
        p_item.paragraph_format.space_after = Pt(4)

    # 2. Proposed Solution
    add_section_header("2. Proposed Solution: The 3 Autonomous Pillars of Paytm VyaparAI")
    pillars = [
        ("Pillar 1: Multilingual Voice Copilot (5 Languages)", "Merchants interact hands-free with the Soundbox and WhatsApp in English, Telugu, Hindi, Tamil, and Kannada. Daily verbal briefing: 'Aaj ka total munafa aur trending items batao' / 'ఈరోజు కలెక్షన్ ఎంత?'. Spoken voice notes automatically convert into structured ledger entries without typing."),
        ("Pillar 2: Smart Udhar Recovery & Cashflow Radar", "AI autonomously sends personalized, polite WhatsApp and voice reminder notes in the customer's native language with 1-click dynamic UPI links. A predictive radar alerts merchants 5 days before working capital deficits emerge."),
        ("Pillar 3: Hyper-Local Demand Forecaster & ONDC Restocking", "Analyzes 2-km radius transaction patterns (e.g. weather changes, local festivals) to predict inventory demand. Automatically discovers lowest distributor rates on ONDC and prepares 1-tap reorders.")
    ]
    for pil_title, pil_body in pillars:
        p_item = doc.add_paragraph(style='List Bullet')
        r_pt = p_item.add_run(pil_title + " — ")
        r_pt.font.bold = True
        r_pt.font.color.rgb = NAVY
        r_pb = p_item.add_run(pil_body)
        r_pb.font.color.rgb = CHARCOAL
        p_item.paragraph_format.space_after = Pt(5)

    # 3. Technology / Tech Stack
    add_section_header("3. Technology & Architecture")
    tech_table = doc.add_table(rows=6, cols=2)
    tech_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = [("Layer", 0), ("Technology & Components", 1)]
    for h_text, col_idx in headers:
        cell = tech_table.cell(0, col_idx)
        set_cell_background(cell, "002970")
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    layers_data = [
        ("1. Interaction & Hardware", "Paytm Soundbox 3.0/4.0 firmware hooks, WhatsApp Cloud API, Android SDK."),
        ("2. Indic Speech & 5-Language NLP", "Bhashini ASR, IndicConformer, Coqui TTS for English, Telugu, Hindi, Tamil, and Kannada."),
        ("3. AI Reasoning & Agents", "Fine-tuned Indic LLMs (Llama 3 / Sarvam Indic / Gemma 2), LangGraph multi-agent orchestration."),
        ("4. Real-Time Streaming & Memory", "Apache Kafka, Flink event processing, Milvus / Qdrant vector database, TimescaleDB."),
        ("5. B2B & Financial Integration", "ONDC Open Commerce protocol, Paytm Lending API, Payments Bank Settlement Gateway.")
    ]
    for row_idx, (layer_name, layer_desc) in enumerate(layers_data, start=1):
        c0 = tech_table.cell(row_idx, 0)
        c1 = tech_table.cell(row_idx, 1)
        if row_idx % 2 == 0:
            set_cell_background(c0, "F8FAFC")
            set_cell_background(c1, "F8FAFC")
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(layer_name)
        r0.font.bold = True
        r0.font.size = Pt(9.5)
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(layer_desc)
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = CHARCOAL

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 4. USP
    add_section_header("4. USP (Unique Selling Proposition): Why Paytm Wins")
    usps = [
        ("Acoustic & Hardware Moat: ", "Installed on 10M+ counters. Competitors require app downloads; Paytm upgrades existing hardware."),
        ("Proprietary Velocity Underwriting: ", "Competitors use self-reported khata. Paytm uses real, second-by-second transaction data."),
        ("5-Language Native Voice Experience: ", "English, Telugu, Hindi, Tamil, and Kannada voice control eliminates typing and language barriers across all of India."),
        ("Closed-Loop B2B Execution: ", "Completes the loop from demand prediction to ONDC supplier ordering and automatic UPI settlement.")
    ]
    for u_title, u_desc in usps:
        p_u = doc.add_paragraph(style='List Bullet')
        ru_t = p_u.add_run(u_title)
        ru_t.font.bold = True
        ru_t.font.color.rgb = NAVY
        ru_d = p_u.add_run(u_desc)
        ru_d.font.color.rgb = CHARCOAL

    # 5. Impact & Benefits
    add_section_header("5. Impact & Measurable Benefits")
    benefits = [
        ("Merchant Impact: ", "+18% to +25% monthly revenue, 4x faster udhar recovery, 35% reduction in dead working capital, and <3-minute credit disbursal."),
        ("Paytm Ecosystem Impact: ", "+30% Soundbox subscription ARPU, 40% reduction in merchant churn, 3x merchant lending loan growth, and new B2B wholesale GMV.")
    ]
    for b_title, b_desc in benefits:
        p_b = doc.add_paragraph(style='List Bullet')
        rb_t = p_b.add_run(b_title)
        rb_t.font.bold = True
        rb_t.font.color.rgb = NAVY
        rb_d = p_b.add_run(b_desc)
        rb_d.font.color.rgb = CHARCOAL

    # 6. Business Model
    add_section_header("6. Business Model & Monetization")
    bmodels = [
        ("SaaS Subscription ('VyaparAI Pro'): ", "₹99 - ₹199 / month add-on bundled with Soundbox for automated WhatsApp collection bots and predictive restocking."),
        ("Lending Commission & Spread: ", "1.5% - 2.5% fee on micro-working capital loans disbursed via AI underwriting."),
        ("B2B ONDC Marketplace Take-Rate: ", "0.5% - 1.5% GMV commission on wholesale replenishment orders routed to FMCG distributors."),
        ("Sponsored Brand Promotions: ", "FMCG brands (HUL, ITC) pay for targeted promotional campaigns and trial product placement.")
    ]
    for bm_title, bm_desc in bmodels:
        p_bm = doc.add_paragraph(style='List Bullet')
        rbm_t = p_bm.add_run(bm_title)
        rbm_t.font.bold = True
        rbm_t.font.color.rgb = NAVY
        rbm_d = p_bm.add_run(bm_desc)
        rbm_d.font.color.rgb = CHARCOAL

    doc.save(filename)
    print(f"DOCX successfully generated at {filename}")

if __name__ == "__main__":
    out_docx = r"C:\Users\ShaikAli\.gemini\antigravity\scratch\paytm-merchant-growth-ai\Paytm_VyaparAI_Pitch_Document.docx"
    create_pitch_docx(out_docx)
