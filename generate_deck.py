import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    NAVY = RGBColor(0, 41, 112)
    DARK_BG = RGBColor(10, 25, 47)
    CYAN = RGBColor(0, 186, 242)
    LIGHT_BG = RGBColor(245, 248, 252)
    WHITE = RGBColor(255, 255, 255)
    CHARCOAL = RGBColor(30, 41, 59)
    GRAY_TEXT = RGBColor(100, 116, 139)
    CARD_BG = RGBColor(255, 255, 255)
    CARD_BORDER = RGBColor(226, 232, 240)
    GREEN = RGBColor(16, 185, 129)
    GOLD = RGBColor(245, 158, 11)

    def add_header(slide, title_text, category_text, dark=False):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(10), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = CYAN

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.5), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(26)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE if dark else NAVY

    # SLIDE 1: TITLE SLIDE
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = DARK_BG
    bg1.line.color.rgb = DARK_BG

    accent_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(0.15), Inches(4.2))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = CYAN
    accent_bar.line.color.rgb = CYAN

    badge = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.5), Inches(5.8), Inches(0.45))
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(15, 45, 82)
    badge.line.color.rgb = CYAN
    tf_b = badge.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "ENGLISH • TELUGU • HINDI • TAMIL • KANNADA"
    p_b.alignment = PP_ALIGN.CENTER
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = CYAN

    title_box = slide1.shapes.add_textbox(Inches(1.2), Inches(2.1), Inches(11), Inches(1.8))
    tf = title_box.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "Paytm VyaparAI"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    p2 = tf.add_paragraph()
    p2.text = "The Autonomous Multilingual AI Business Partner for 40M+ Merchants"
    p2.font.size = Pt(22)
    p2.font.color.rgb = CYAN
    p2.space_before = Pt(10)

    desc_box = slide1.shapes.add_textbox(Inches(1.2), Inches(4.0), Inches(10.5), Inches(1.5))
    tf_d = desc_box.text_frame
    tf_d.word_wrap = True
    desc_p = tf_d.paragraphs[0]
    desc_p.text = "Transforming the Paytm Soundbox & POS into an intelligent, voice-first business partner — speaking English, Telugu, Hindi, Tamil, and Kannada to automate inventory forecasting, smart udhar recovery, and instant credit underwriting."
    desc_p.font.size = Pt(15)
    desc_p.font.color.rgb = RGBColor(203, 213, 225)

    footer_box = slide1.shapes.add_textbox(Inches(1.2), Inches(5.8), Inches(10), Inches(0.8))
    tf_f = footer_box.text_frame
    pf = tf_f.paragraphs[0]
    pf.text = "Beyond Payments: Empowering India's Retail Backbone with Voice-Led Ambient AI"
    pf.font.size = Pt(13)
    pf.font.bold = True
    pf.font.color.rgb = GOLD

    # SLIDE 2: PROBLEM STATEMENT
    slide2 = prs.slides.add_slide(blank_layout)
    bg2 = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg2.fill.solid()
    bg2.fill.fore_color.rgb = LIGHT_BG
    bg2.line.color.rgb = LIGHT_BG

    add_header(slide2, "The Growth Blindspots: Why 40M+ Merchants Struggle Beyond Payments", "Problem Statement")

    problems = [
        {
            "num": "01",
            "title": "Dead Stock & Inventory Traps",
            "stat": "25-30% Working Capital Tied Up",
            "desc": "Merchants rely on gut feel for restocking. Fast-moving goods stock out during peak hours, while slow inventory collects dust with zero warning."
        },
        {
            "num": "02",
            "title": "Sticky Udhar & Cash Flow Leaks",
            "stat": "₹1.5L - ₹3L Trapped per Store",
            "desc": "Manual paper khatas lead to awkward debt recovery, lost ledgers, and delayed repayments, crippling everyday cash cycles."
        },
        {
            "num": "03",
            "title": "Zero Hyper-Local Market Intel",
            "stat": "Losing 15% Share to Quick-Commerce",
            "desc": "Kiranas operate in silos without knowing what's trending 500m away, failing to match consumer demand shifts and promotions."
        },
        {
            "num": "04",
            "title": "Language & Typing Barrier",
            "stat": "82% Merchants Dislike English Apps",
            "desc": "Existing software mandates typing and English UI. Merchants in South & North India want hands-free voice in Telugu, Tamil, Kannada, Hindi, and English."
        }
    ]

    card_w = Inches(2.7)
    card_h = Inches(4.8)
    card_y = Inches(1.8)
    spacing = Inches(0.3)
    start_x = Inches(0.8)

    for i, p in enumerate(problems):
        cx = start_x + i * (card_w + spacing)
        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, card_y, card_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.5)

        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = Inches(0.2)
        tf_c.margin_right = Inches(0.2)
        tf_c.margin_top = Inches(0.25)

        pn = tf_c.paragraphs[0]
        pn.text = p["num"]
        pn.font.size = Pt(20)
        pn.font.bold = True
        pn.font.color.rgb = CYAN

        pt = tf_c.add_paragraph()
        pt.text = p["title"]
        pt.font.size = Pt(15)
        pt.font.bold = True
        pt.font.color.rgb = NAVY
        pt.space_before = Pt(8)

        ps = tf_c.add_paragraph()
        ps.text = p["stat"]
        ps.font.size = Pt(12)
        ps.font.bold = True
        ps.font.color.rgb = RGBColor(225, 29, 72)
        ps.space_before = Pt(8)

        pd = tf_c.add_paragraph()
        pd.text = p["desc"]
        pd.font.size = Pt(11)
        pd.font.color.rgb = GRAY_TEXT
        pd.space_before = Pt(12)

    # SLIDE 3: PROPOSED SOLUTION
    slide3 = prs.slides.add_slide(blank_layout)
    bg3 = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg3.fill.solid()
    bg3.fill.fore_color.rgb = LIGHT_BG
    bg3.line.color.rgb = LIGHT_BG

    add_header(slide3, "Paytm VyaparAI: 3 Autonomous Pillars of Merchant Growth", "Proposed Solution")

    pillars = [
        {
            "pillar": "PILLAR 1",
            "title": "Voice Copilot in 5 Indian Languages",
            "tagline": "English • Telugu • Hindi • Tamil • Kannada",
            "points": [
                "Ambient Soundbox Interaction: Speaks and answers counter questions naturally in Telugu, Tamil, Kannada, Hindi, and English.",
                "WhatsApp AI Agent: Sends morning insights, audio summaries, low-stock alerts, and receives voice notes for instant ledger updates.",
                "Zero Data Entry: Transcribes voice notes into structured entries without barcode scanning or manual catalog typing."
            ]
        },
        {
            "pillar": "PILLAR 2",
            "title": "Automated Udhar & Smart Cashflow Optimizer",
            "tagline": "Turn Trapped Credit into Instant Liquidity",
            "points": [
                "Polite Multilingual Reminders: AI sends personalized, gentle payment reminders in local languages with dynamic 1-click UPI links.",
                "Cashflow Trajectory Predictor: Anticipates working capital deficits 5 days before rent/distributor payouts due.",
                "1-Click Micro-Credit Underwriting: Triggers real-time loan pre-approvals via Paytm Lending based on payment velocity."
            ]
        },
        {
            "pillar": "PILLAR 3",
            "title": "Hyper-Local Demand Forecaster & ONDC Restocking",
            "tagline": "Big-Box Retail Intelligence for Kirana Stores",
            "points": [
                "Neighborhood Trend Sensing: Aggregates pin-code level Paytm transaction trends (e.g., 'Heatwave incoming: Increase juice orders by 44%').",
                "Automated Distributor Order Routing: Compares distributor prices on ONDC and drafts WhatsApp bulk reorder slips with single-tap approval.",
                "Festival & Seasonality Playbooks: Proactively generates curated stocking lists and consumer promo posters."
            ]
        }
    ]

    pw = Inches(3.7)
    ph = Inches(4.9)
    py = Inches(1.75)
    p_spacing = Inches(0.3)
    p_start_x = Inches(0.8)

    for i, p in enumerate(pillars):
        px = p_start_x + i * (pw + p_spacing)
        card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, py, pw, ph)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.5)

        tf_p = card.text_frame
        tf_p.word_wrap = True
        tf_p.margin_left = Inches(0.25)
        tf_p.margin_right = Inches(0.25)
        tf_p.margin_top = Inches(0.25)

        p_tag = tf_p.paragraphs[0]
        p_tag.text = p["pillar"]
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = CYAN

        p_t = tf_p.add_paragraph()
        p_t.text = p["title"]
        p_t.font.size = Pt(15)
        p_t.font.bold = True
        p_t.font.color.rgb = NAVY
        p_t.space_before = Pt(4)

        p_sub = tf_p.add_paragraph()
        p_sub.text = p["tagline"]
        p_sub.font.size = Pt(11)
        p_sub.font.bold = True
        p_sub.font.color.rgb = GOLD
        p_sub.space_before = Pt(4)

        for pt_item in p["points"]:
            p_b = tf_p.add_paragraph()
            p_b.text = "• " + pt_item
            p_b.font.size = Pt(10.5)
            p_b.font.color.rgb = CHARCOAL
            p_b.space_before = Pt(8)

    # SLIDE 4: TECH STACK
    slide4 = prs.slides.add_slide(blank_layout)
    bg4 = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg4.fill.solid()
    bg4.fill.fore_color.rgb = LIGHT_BG
    bg4.line.color.rgb = LIGHT_BG

    add_header(slide4, "Scalable, Low-Latency Architecture Built for Bharat", "Technology / Tech Stack Used")

    tech_layers = [
        {
            "layer": "LAYER 1: INTERACTION & SOUNDBOX EDGE",
            "tech": "Paytm Soundbox 3.0 / 4.0 Firmware, WhatsApp Cloud API, Android SDK",
            "desc": "Ultra-lightweight edge triggers on Soundbox with cellular IoT connectivity; seamless WhatsApp webhook bridge for audio and rich cards."
        },
        {
            "layer": "LAYER 2: 5-LANGUAGE SPEECH & NLP ENGINE",
            "tech": "Bhashini ASR, IndicConformer, Coqui TTS (English, Telugu, Hindi, Tamil, Kannada)",
            "desc": "High-accuracy transcription of colloquial dialects across South and North India; expressive voice generation with emotional politeness tuning."
        },
        {
            "layer": "LAYER 3: AGENTIC REASONING & ORCHESTRATION",
            "tech": "Fine-Tuned Indic LLMs (Llama 3 / Sarvam Indic / Gemma 2), LangGraph Multi-Agent",
            "desc": "Specialized autonomous subagents: Khata Reconciliation Agent, Inventory & Demand Forecaster, and Credit Underwriting Agent running in deterministic guardrails."
        },
        {
            "layer": "LAYER 4: REAL-TIME DATA & VECTOR MEMORY",
            "tech": "Apache Kafka, Flink, Milvus / Qdrant Vector DB, PostgreSQL, TimescaleDB",
            "desc": "Sub-second event streaming of merchant transaction logs; vector indexing of merchant SKU names, customer credit histories, and geo-neighborhood clusters."
        },
        {
            "layer": "LAYER 5: B2B & ECOSYSTEM INTEGRATIONS",
            "tech": "ONDC Open Protocol, Paytm Payments Gateway & Lending APIs, FMCG DMS",
            "desc": "Seamless routing of purchase orders to regional distributors and automatic reconciliation with UPI settlement flows."
        }
    ]

    tw = Inches(11.733)
    th = Inches(0.9)
    ty_start = Inches(1.75)
    t_spacing = Inches(0.12)

    for i, t in enumerate(tech_layers):
        curr_y = ty_start + i * (th + t_spacing)
        card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), curr_y, tw, th)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.5)

        tf_t = card.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = Inches(0.3)
        tf_t.margin_right = Inches(0.3)
        tf_t.margin_top = Inches(0.12)

        p_l = tf_t.paragraphs[0]
        p_l.text = t["layer"]
        p_l.font.size = Pt(11)
        p_l.font.bold = True
        p_l.font.color.rgb = CYAN

        p_tc = tf_t.add_paragraph()
        p_tc.text = t["tech"] + "  |  " + t["desc"]
        p_tc.font.size = Pt(11)
        p_tc.font.color.rgb = CHARCOAL
        p_tc.space_before = Pt(3)

    # SLIDE 5: USP
    slide5 = prs.slides.add_slide(blank_layout)
    bg5 = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg5.fill.solid()
    bg5.fill.fore_color.rgb = LIGHT_BG
    bg5.line.color.rgb = LIGHT_BG

    add_header(slide5, "Why Paytm Wins: Unrivaled Moats Over Standalone Software", "USP (Unique Selling Proposition)")

    usps = [
        {
            "title": "Hardware & Acoustic Moat",
            "subtitle": "Already on 10M+ Counters",
            "desc": "Competitors require app downloads and screen time. Paytm already owns the physical counter space via Soundbox and POS. VyaparAI turns this sunk hardware cost into an intelligent conversational console."
        },
        {
            "title": "Proprietary Velocity Underwriting",
            "subtitle": "Real-time Cash Flow Insights",
            "desc": "Stand-alone Khata apps rely on manual self-reported entries. Paytm possesses verifiable, second-by-second transaction volumes and customer repeat frequencies, unlocking unmatched credit risk assessment."
        },
        {
            "title": "5 Indian Languages Voice Native",
            "subtitle": "English • Telugu • Hindi • Tamil • Kannada",
            "desc": "Zero language or literacy barriers. Merchants converse naturally in their mother tongue without typing or scanning barcodes. Spoken product names automatically map to catalog items."
        },
        {
            "title": "Closed-Loop ONDC & B2B Settlement",
            "subtitle": "From Advice to Execution",
            "desc": "Other solutions only provide analytics. VyaparAI completes the transaction loop: discovers supplier discounts on ONDC, negotiates order, and settles invoices directly from Paytm merchant balance."
        }
    ]

    uw = Inches(5.7)
    uh = Inches(2.25)
    ux_coords = [Inches(0.8), Inches(6.8), Inches(0.8), Inches(6.8)]
    uy_coords = [Inches(1.8), Inches(1.8), Inches(4.35), Inches(4.35)]

    for i, u in enumerate(usps):
        card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, ux_coords[i], uy_coords[i], uw, uh)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.5)

        tf_u = card.text_frame
        tf_u.word_wrap = True
        tf_u.margin_left = Inches(0.3)
        tf_u.margin_right = Inches(0.3)
        tf_u.margin_top = Inches(0.2)

        pu_title = tf_u.paragraphs[0]
        pu_title.text = u["title"]
        pu_title.font.size = Pt(16)
        pu_title.font.bold = True
        pu_title.font.color.rgb = NAVY

        pu_sub = tf_u.add_paragraph()
        pu_sub.text = u["subtitle"]
        pu_sub.font.size = Pt(11)
        pu_sub.font.bold = True
        pu_sub.font.color.rgb = CYAN
        pu_sub.space_before = Pt(2)

        pu_desc = tf_u.add_paragraph()
        pu_desc.text = u["desc"]
        pu_desc.font.size = Pt(11.5)
        pu_desc.font.color.rgb = CHARCOAL
        pu_desc.space_before = Pt(6)

    # SLIDE 6: IMPACT & BENEFITS
    slide6 = prs.slides.add_slide(blank_layout)
    bg6 = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg6.fill.solid()
    bg6.fill.fore_color.rgb = LIGHT_BG
    bg6.line.color.rgb = LIGHT_BG

    add_header(slide6, "Dual Value Creation: Turbocharging Merchants & Paytm's Flywheel", "Impact & Benefits")

    col1 = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.9))
    col1.fill.solid()
    col1.fill.fore_color.rgb = CARD_BG
    col1.line.color.rgb = CARD_BORDER
    col1.line.width = Pt(1.5)

    tf_c1 = col1.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_left = Inches(0.3)
    tf_c1.margin_right = Inches(0.3)
    tf_c1.margin_top = Inches(0.25)

    p_c1_h = tf_c1.paragraphs[0]
    p_c1_h.text = "FOR THE 40M+ MERCHANTS"
    p_c1_h.font.size = Pt(16)
    p_c1_h.font.bold = True
    p_c1_h.font.color.rgb = GREEN

    m_benefits = [
        ("+18% to +25% Monthly Revenue", "Eliminating stock-outs of high-velocity items and capitalizing on seasonal neighborhood demand trends."),
        ("4x Faster Udhar Recovery", "Polite, persistent WhatsApp/Voice follow-ups in local languages reduce bad debts and recover cash cycle within 7 days."),
        ("35% Reduction in Working Capital Lock-in", "Optimized stock levels eliminate expired items and dead inventory holding costs."),
        ("Zero-Bureaucracy Credit Access", "Access to ₹25,000 to ₹5,00,000 working capital loans in under 180 seconds directly via transaction track record.")
    ]
    for b_title, b_sub in m_benefits:
        p_bt = tf_c1.add_paragraph()
        p_bt.text = "• " + b_title
        p_bt.font.size = Pt(13)
        p_bt.font.bold = True
        p_bt.font.color.rgb = NAVY
        p_bt.space_before = Pt(10)

        p_bs = tf_c1.add_paragraph()
        p_bs.text = "   " + b_sub
        p_bs.font.size = Pt(11)
        p_bs.font.color.rgb = CHARCOAL

    col2 = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9))
    col2.fill.solid()
    col2.fill.fore_color.rgb = CARD_BG
    col2.line.color.rgb = CARD_BORDER
    col2.line.width = Pt(1.5)

    tf_c2 = col2.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_left = Inches(0.3)
    tf_c2.margin_right = Inches(0.3)
    tf_c2.margin_top = Inches(0.25)

    p_c2_h = tf_c2.paragraphs[0]
    p_c2_h.text = "FOR PAYTM'S BUSINESS FLYWHEEL"
    p_c2_h.font.size = Pt(16)
    p_c2_h.font.bold = True
    p_c2_h.font.color.rgb = CYAN

    p_benefits = [
        ("Soundbox Subscription ARPU Lift (+30%)", "Merchants gladly pay an additional premium for an active business partner rather than a passive speaker."),
        ("40% Churn Reduction", "Deep integration into daily inventory, khata, and supplier workflows makes switching away from Paytm unthinkable."),
        ("3x Scale in Merchant Lending Disbursals", "Superior underwriting data leads to lower NPAs and unlocks massive credit distribution commissions with NBFC partners."),
        ("B2B Payments & ONDC GMV Monetization", "Captures supplier payments and distributor wholesale transactions, expanding GMV beyond retail checkouts.")
    ]
    for b_title, b_sub in p_benefits:
        p_bt = tf_c2.add_paragraph()
        p_bt.text = "• " + b_title
        p_bt.font.size = Pt(13)
        p_bt.font.bold = True
        p_bt.font.color.rgb = NAVY
        p_bt.space_before = Pt(10)

        p_bs = tf_c2.add_paragraph()
        p_bs.text = "   " + b_sub
        p_bs.font.size = Pt(11)
        p_bs.font.color.rgb = CHARCOAL

    # SLIDE 7: BUSINESS MODEL
    slide7 = prs.slides.add_slide(blank_layout)
    bg7 = slide7.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg7.fill.solid()
    bg7.fill.fore_color.rgb = LIGHT_BG
    bg7.line.color.rgb = LIGHT_BG

    add_header(slide7, "Four Diversified High-Margin Revenue Streams", "Business Model")

    biz_models = [
        {
            "stream": "1. SaaS Subscription Tier",
            "model": "Freemium & Soundbox Bundle",
            "pricing": "₹99 - ₹199 / month",
            "desc": "Base insights free for all Soundbox users. 'VyaparAI Pro' unlocks automated WhatsApp payment collection bots, 5-language voice, and priority B2B pricing."
        },
        {
            "stream": "2. Loan Origination & Servicing",
            "model": "Credit Distribution Fee",
            "pricing": "1.5% - 2.5% per disbursal",
            "desc": "Earn origination fees and risk-sharing spread from partner NBFCs and banks for pre-underwritten working capital and supplier invoice financing."
        },
        {
            "stream": "3. B2B & ONDC Marketplace Take-Rate",
            "model": "Distributor Commission",
            "pricing": "0.5% - 1.5% of order GMV",
            "desc": "Paytm takes a cut from FMCG brands and distributors for automating bulk restocking orders routed directly via the VyaparAI engine."
        },
        {
            "stream": "4. FMCG Sponsored Brand Discovery",
            "model": "Hyper-Local Brand Campaigns",
            "pricing": "Pay-per-promotion / Sponsored Sample",
            "desc": "Brands (HUL, ITC, Nestlé) pay to run targeted merchant trade promotions and new product sample distributions based on neighborhood demand data."
        }
    ]

    bw = Inches(2.7)
    bh = Inches(4.8)
    by = Inches(1.8)
    b_spacing = Inches(0.3)
    b_start_x = Inches(0.8)

    for i, b in enumerate(biz_models):
        bx = b_start_x + i * (bw + b_spacing)
        card = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, bw, bh)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.5)

        tf_b = card.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = Inches(0.2)
        tf_b.margin_right = Inches(0.2)
        tf_b.margin_top = Inches(0.25)

        pb_s = tf_b.paragraphs[0]
        pb_s.text = b["stream"]
        pb_s.font.size = Pt(14)
        pb_s.font.bold = True
        pb_s.font.color.rgb = NAVY

        pb_m = tf_b.add_paragraph()
        pb_m.text = b["model"]
        pb_m.font.size = Pt(11)
        pb_m.font.bold = True
        pb_m.font.color.rgb = CYAN
        pb_m.space_before = Pt(6)

        pb_p = tf_b.add_paragraph()
        pb_p.text = b["pricing"]
        pb_p.font.size = Pt(13)
        pb_p.font.bold = True
        pb_p.font.color.rgb = GREEN
        pb_p.space_before = Pt(8)

        pb_d = tf_b.add_paragraph()
        pb_d.text = b["desc"]
        pb_d.font.size = Pt(11)
        pb_d.font.color.rgb = CHARCOAL
        pb_d.space_before = Pt(10)

    prs.save(output_path)
    print(f"Presentation successfully created at {output_path}")

if __name__ == "__main__":
    out_dir = r"C:\Users\ShaikAli\.gemini\antigravity\scratch\paytm-merchant-growth-ai"
    out_file = os.path.join(out_dir, "Paytm_VyaparAI_Pitch_Deck.pptx")
    create_deck(out_file)
