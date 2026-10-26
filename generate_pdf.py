import os
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

# Palette
NAVY = colors.HexColor("#002970")      # Paytm Primary Navy
DARK_NAVY = colors.HexColor("#0A192F") # High Tech Dark Navy
CYAN = colors.HexColor("#00BAF2")      # Paytm Cyan
LIGHT_BG = colors.HexColor("#F8FAFC")  # Crisp clean light slate
WHITE = colors.HexColor("#FFFFFF")
CHARCOAL = colors.HexColor("#1E293B")  # Slate 800
GRAY = colors.HexColor("#64748B")      # Slate 500
BORDER_COLOR = colors.HexColor("#CBD5E1")
ACCENT_GREEN = colors.HexColor("#059669")
ACCENT_RED = colors.HexColor("#E11D48")
ACCENT_GOLD = colors.HexColor("#D97706")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            self.saveState()
            self.setFillColor(DARK_NAVY)
            self.rect(0, 0, 11 * inch, 8.5 * inch, fill=True, stroke=False)
            self.setFillColor(CYAN)
            self.rect(0.6 * inch, 1.8 * inch, 0.12 * inch, 5.0 * inch, fill=True, stroke=False)
            self.restoreState()
        else:
            self.saveState()
            self.setFillColor(LIGHT_BG)
            self.rect(0, 0, 11 * inch, 8.5 * inch, fill=True, stroke=False)
            
            # Header line
            self.setStrokeColor(CYAN)
            self.setLineWidth(2)
            self.line(0.6 * inch, 7.85 * inch, 10.4 * inch, 7.85 * inch)
            
            # Footer line
            self.setStrokeColor(BORDER_COLOR)
            self.setLineWidth(0.75)
            self.line(0.6 * inch, 0.65 * inch, 10.4 * inch, 0.65 * inch)
            
            # Footer text
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(NAVY)
            self.drawString(0.6 * inch, 0.45 * inch, "Paytm VyaparAI  |  Multilingual AI Business Partner  |  English • Telugu • Hindi • Tamil • Kannada")
            
            self.setFont("Helvetica", 8)
            self.setFillColor(GRAY)
            page_text = f"Slide {self._pageNumber} of {page_count}"
            self.drawRightString(10.4 * inch, 0.45 * inch, page_text)
            self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=landscape(letter),
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.7 * inch
    )

    styles = getSampleStyleSheet()

    badge_style = ParagraphStyle(
        'Badge',
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=CYAN,
        spaceAfter=15
    )
    title_main_style = ParagraphStyle(
        'TitleMain',
        fontName='Helvetica-Bold',
        fontSize=38,
        leading=42,
        textColor=WHITE,
        spaceAfter=12
    )
    title_sub_style = ParagraphStyle(
        'TitleSub',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=CYAN,
        spaceAfter=25
    )
    title_desc_style = ParagraphStyle(
        'TitleDesc',
        fontName='Helvetica',
        fontSize=13,
        leading=19,
        textColor=colors.HexColor("#CBD5E1"),
        spaceAfter=30
    )
    title_footer_style = ParagraphStyle(
        'TitleFooter',
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=ACCENT_GOLD
    )

    section_cat_style = ParagraphStyle(
        'SectionCat',
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=CYAN,
        spaceAfter=3
    )
    section_title_style = ParagraphStyle(
        'SectionTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=NAVY,
        spaceAfter=15
    )
    card_title_style = ParagraphStyle(
        'CardTitle',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=NAVY,
        spaceAfter=4
    )
    card_stat_red = ParagraphStyle(
        'CardStatRed',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=ACCENT_RED,
        spaceAfter=6
    )
    card_stat_green = ParagraphStyle(
        'CardStatGreen',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=ACCENT_GREEN,
        spaceAfter=6
    )
    card_sub_cyan = ParagraphStyle(
        'CardSubCyan',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=CYAN,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'CardBody',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=CHARCOAL
    )
    bullet_style = ParagraphStyle(
        'BulletStyle',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=CHARCOAL,
        spaceAfter=6
    )

    story = []

    # SLIDE 1: TITLE SLIDE
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("MULTILINGUAL AI BUSINESS PARTNER  •  ENGLISH • TELUGU • HINDI • TAMIL • KANNADA", badge_style))
    story.append(Paragraph("Paytm VyaparAI", title_main_style))
    story.append(Paragraph("The Autonomous AI Business Partner for 40M+ Bharat Merchants", title_sub_style))
    story.append(Paragraph(
        "Transforming the Paytm Soundbox & POS into an intelligent, voice-first growth engine — "
        "supporting native voice in English, Telugu, Hindi, Tamil, and Kannada for inventory forecasting, smart udhar recovery, and instant credit.",
        title_desc_style
    ))
    story.append(Paragraph("⚡ Beyond Payments: Empowering India's Retail Backbone with Voice-Led Ambient AI", title_footer_style))
    story.append(PageBreak())

    # SLIDE 2: PROBLEM STATEMENT
    story.append(Spacer(1, 0.45 * inch))
    story.append(Paragraph("PROBLEM STATEMENT", section_cat_style))
    story.append(Paragraph("The Growth Blindspots: Why 40M+ Merchants Struggle Beyond Payments", section_title_style))

    p1 = [
        Paragraph("01  Dead Stock & Trapped Capital", card_title_style),
        Paragraph("25% - 30% Working Capital Blocked", card_stat_red),
        Paragraph("Merchants rely on manual intuition. Fast-moving SKUs stock out during peak evening rushes, while slow-moving items expire or tie up essential liquidity on dusty shelves.", body_style)
    ]
    p2 = [
        Paragraph("02  Sticky Udhar & Cashflow Leaks", card_title_style),
        Paragraph("₹1.5L - ₹3.0L Trapped per Store", card_stat_red),
        Paragraph("Manual red paper khatas cause delayed repayments and lost records. Shopkeepers feel uncomfortable aggressively following up with regular neighborhood customers.", body_style)
    ]
    p3 = [
        Paragraph("03  Zero Hyper-Local Market Intel", card_title_style),
        Paragraph("Losing 15% Share to Quick-Commerce", card_stat_red),
        Paragraph("Kiranas operate as isolated islands. They lack visibility into fast-shifting neighborhood product trends, unable to match quick-commerce agility and assortment.", body_style)
    ]
    p4 = [
        Paragraph("04  The Language & Screen Barrier", card_title_style),
        Paragraph("82% Reject English Software Apps", card_stat_red),
        Paragraph("Traditional SaaS tools mandate typing, barcodes, and English UI. Merchants in Andhra/Telangana, TN, Karnataka, and North India demand voice in Telugu, Tamil, Kannada, and Hindi.", body_style)
    ]

    prob_data = [[p1, p2, p3, p4]]
    prob_table = Table(prob_data, colWidths=[2.35 * inch] * 4, rowHeights=[4.7 * inch])
    prob_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (0,-1), 1, BORDER_COLOR),
        ('BOX', (1,0), (1,-1), 1, BORDER_COLOR),
        ('BOX', (2,0), (2,-1), 1, BORDER_COLOR),
        ('BOX', (3,0), (3,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(prob_table)
    story.append(PageBreak())

    # SLIDE 3: PROPOSED SOLUTION
    story.append(Spacer(1, 0.45 * inch))
    story.append(Paragraph("PROPOSED SOLUTION", section_cat_style))
    story.append(Paragraph("Paytm VyaparAI: 3 Autonomous Pillars of Merchant Growth", section_title_style))

    sol1 = [
        Paragraph("PILLAR 1", section_cat_style),
        Paragraph("Voice Copilot in 5 Indian Languages", card_title_style),
        Paragraph("English • Telugu • Hindi • Tamil • Kannada", card_sub_cyan),
        Spacer(1, 6),
        Paragraph("• <b>Hands-Free Counter Queries:</b> Speaks and answers oral questions naturally (e.g. Telugu: <i>'ఈరోజు కలెక్షన్ ఎంత?'</i>, Hindi: <i>'आज का मुनाफा बताओ'</i>).", bullet_style),
        Paragraph("• <b>WhatsApp AI Companion:</b> Sends daily morning audio briefings, low-stock warnings, and transcribes spoken voice notes into ledger balances.", bullet_style),
        Paragraph("• <b>Zero Typing Required:</b> Operates without barcodes or typing, perfectly tuned for busy store counters.", bullet_style),
    ]
    sol2 = [
        Paragraph("PILLAR 2", section_cat_style),
        Paragraph("Automated Udhar & Smart Cashflow Optimizer", card_title_style),
        Paragraph("Converting Trapped Credit into Liquid Capital", card_sub_cyan),
        Spacer(1, 6),
        Paragraph("• <b>Polite Multilingual Reminders:</b> Sends gentle WhatsApp voice notes & text in Telugu, Tamil, Kannada, Hindi, or English with 1-click dynamic UPI links.", bullet_style),
        Paragraph("• <b>Cashflow Deficit Radar:</b> Predicts cash crunches 5 days in advance before supplier bills and rent payments fall due.", bullet_style),
        Paragraph("• <b>1-Click Micro-Credit Underwriting:</b> Triggers pre-approved working capital loans (<3 mins) based on verified UPI settlement velocity.", bullet_style),
    ]
    sol3 = [
        Paragraph("PILLAR 3", section_cat_style),
        Paragraph("Hyper-Local Demand Forecaster & ONDC Restocking", card_title_style),
        Paragraph("Enterprise-Grade Intelligence for Neighborhood Kiranas", card_sub_cyan),
        Spacer(1, 6),
        Paragraph("• <b>2-Km Radius Trend Sensing:</b> Aggregates anonymized local Paytm transaction trends (e.g. <i>'Heatwave incoming: Cold drink sales up 44%'</i>).", bullet_style),
        Paragraph("• <b>Automated ONDC Replenishment:</b> Discovers wholesale distributor rates, prepares purchase orders, and initiates 1-tap reordering.", bullet_style),
        Paragraph("• <b>Festival Playbooks:</b> Curates festival inventory schedules and promotional WhatsApp posters automatically.", bullet_style),
    ]

    sol_data = [[sol1, sol2, sol3]]
    sol_table = Table(sol_data, colWidths=[3.15 * inch] * 3, rowHeights=[4.7 * inch])
    sol_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(sol_table)
    story.append(PageBreak())

    # SLIDE 4: TECHNOLOGY / TECH STACK
    story.append(Spacer(1, 0.45 * inch))
    story.append(Paragraph("TECHNOLOGY / TECH STACK USED", section_cat_style))
    story.append(Paragraph("Scalable, Low-Latency Architecture Built for Bharat", section_title_style))

    tech_rows = [
        [
            Paragraph("<b>Layer 1: Interaction & Soundbox Edge</b>", card_title_style),
            Paragraph("<b>Paytm Soundbox 3.0/4.0 Firmware, WhatsApp Cloud API, Android SDK:</b> Low-latency edge audio triggers, cellular IoT pinging, and WhatsApp webhook bridge for voice notes and interactive payment cards.", body_style)
        ],
        [
            Paragraph("<b>Layer 2: Indic Multilingual Engine</b>", card_title_style),
            Paragraph("<b>Bhashini ASR, IndicConformer, Coqui TTS (English, Telugu, Hindi, Tamil, Kannada):</b> High-accuracy speech recognition tuned for noisy street acoustics and mixed dialects; natural emotive voice synthesis across South & North India.", body_style)
        ],
        [
            Paragraph("<b>Layer 3: Agentic Reasoning & Guardrails</b>", card_title_style),
            Paragraph("<b>Fine-Tuned Indic LLMs (Llama 3 / Sarvam Indic / Gemma 2), LangGraph:</b> Autonomous multi-agent orchestration (Khata Agent, Demand Forecaster, Underwriting Agent) bound by deterministic financial validation guardrails.", body_style)
        ],
        [
            Paragraph("<b>Layer 4: Real-Time Data & Vector Memory</b>", card_title_style),
            Paragraph("<b>Apache Kafka, Flink, Milvus / Qdrant Vector DB, TimescaleDB:</b> Sub-second stream processing of merchant payment velocities; vector indexing of product SKUs, credit histories, and geo-neighborhood clusters.", body_style)
        ],
        [
            Paragraph("<b>Layer 5: B2B & Ecosystem Integrations</b>", card_title_style),
            Paragraph("<b>ONDC Open Commerce Protocol, Paytm Lending & Payments API, FMCG DMS:</b> Automated wholesale distributor discovery, dynamic purchase order creation, and instant UPI reconciliation.", body_style)
        ]
    ]

    tech_table = Table(tech_rows, colWidths=[2.8 * inch, 6.8 * inch], rowHeights=[0.88 * inch] * 5)
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.75, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 9),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(tech_table)
    story.append(PageBreak())

    # SLIDE 5: USP
    story.append(Spacer(1, 0.45 * inch))
    story.append(Paragraph("USP (UNIQUE SELLING PROPOSITION)", section_cat_style))
    story.append(Paragraph("Why Paytm Wins: Unrivaled Moats Over Standalone Software", section_title_style))

    u1 = [
        Paragraph("1. Hardware & Counter Presence Moat", card_title_style),
        Paragraph("Already on 10M+ Retail Counters", card_sub_cyan),
        Paragraph("Competitors must persuade merchants to download standalone apps and stare at screens. Paytm already commands the counter through Soundbox and POS. VyaparAI converts this installed base into an ambient AI console with zero friction.", body_style)
    ]
    u2 = [
        Paragraph("2. Proprietary Cashflow Underwriting", card_title_style),
        Paragraph("Verifiable, High-Velocity Financial Data", card_sub_cyan),
        Paragraph("Stand-alone khata apps rely on self-reported, prone-to-fraud manual entries. Paytm observes real, second-by-second UPI settlement velocities and customer repeat frequencies, unlocking flawless credit risk scoring.", body_style)
    ]
    u3 = [
        Paragraph("3. 5-Language Voice Architecture", card_title_style),
        Paragraph("English • Telugu • Hindi • Tamil • Kannada", card_sub_cyan),
        Paragraph("Engineered specifically for India's linguistic diversity. Merchants interact in colloquial dialect without typing or English barcodes. The AI translates spoken inputs into structured SKUs effortlessly.", body_style)
    ]
    u4 = [
        Paragraph("4. Closed-Loop ONDC & B2B Execution", card_title_style),
        Paragraph("From Insight to Execution in One Tap", card_sub_cyan),
        Paragraph("Generic analytics tools merely show charts. VyaparAI executes the entire retail loop: discovers supplier rates on ONDC, negotiates bulk orders, and settles invoices directly from Paytm merchant balances.", body_style)
    ]

    usp_data = [
        [u1, u2],
        [u3, u4]
    ]
    usp_table = Table(usp_data, colWidths=[4.75 * inch, 4.75 * inch], rowHeights=[2.3 * inch, 2.3 * inch])
    usp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(usp_table)
    story.append(PageBreak())

    # SLIDE 6: IMPACT & BENEFITS
    story.append(Spacer(1, 0.45 * inch))
    story.append(Paragraph("IMPACT & BENEFITS", section_cat_style))
    story.append(Paragraph("Dual Value Creation: Turbocharging Merchants & Paytm's Flywheel", section_title_style))

    imp_merchant = [
        Paragraph("FOR THE 40M+ BHARAT MERCHANTS", card_stat_green),
        Spacer(1, 6),
        Paragraph("• <b>+18% to +25% Monthly Revenue Growth:</b> Drastically eliminates stock-outs during peak hours and capitalizes on high-margin hyper-local demand trends.", bullet_style),
        Paragraph("• <b>4x Faster Udhar Recovery:</b> Empathetic, automated WhatsApp/Voice reminders in local languages recover trapped credit without embarrassing regular customers.", bullet_style),
        Paragraph("• <b>35% Drop in Working Capital Lock-in:</b> AI inventory intelligence prevents slow-moving stock accumulation and expiry waste.", bullet_style),
        Paragraph("• <b>Instant <3-Minute Credit Disbursals:</b> Seamless access to ₹25,000 to ₹5,00,000 micro-loans based strictly on payment track record.", bullet_style),
    ]

    imp_paytm = [
        Paragraph("FOR PAYTM'S BUSINESS FLYWHEEL", card_sub_cyan),
        Spacer(1, 6),
        Paragraph("• <b>+30% Lift in Soundbox Subscription ARPU:</b> Merchants happily pay an incremental tier for an active business partner rather than a passive speaker.", bullet_style),
        Paragraph("• <b>40% Reduction in Merchant Churn:</b> Deep integration into daily inventory, khata, and supplier workflows cements unbreakable ecosystem loyalty.", bullet_style),
        Paragraph("• <b>3x Merchant Lending Expansion:</b> Cashflow underwriting unlocks massive credit distribution fees with minimal credit default risk.", bullet_style),
        Paragraph("• <b>B2B & ONDC GMV Monetization:</b> Captures wholesale supplier flows and distributor bulk settlements beyond consumer retail checkouts.", bullet_style),
    ]

    imp_data = [[imp_merchant, imp_paytm]]
    imp_table = Table(imp_data, colWidths=[4.75 * inch, 4.75 * inch], rowHeights=[4.7 * inch])
    imp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(imp_table)
    story.append(PageBreak())

    # SLIDE 7: BUSINESS MODEL
    story.append(Spacer(1, 0.45 * inch))
    story.append(Paragraph("BUSINESS MODEL", section_cat_style))
    story.append(Paragraph("Four Diversified High-Margin Revenue Streams", section_title_style))

    b1 = [
        Paragraph("1. SaaS Subscription Tier", card_title_style),
        Paragraph("VyaparAI Pro Bundle", card_sub_cyan),
        Paragraph("₹99 - ₹199 / month", card_stat_green),
        Paragraph("Freemium baseline insights for all Soundbox users. Pro subscription unlocks automated WhatsApp recovery bots, multilingual voice, demand forecasting, and priority B2B pricing.", body_style)
    ]
    b2 = [
        Paragraph("2. Lending Origination Fees", card_title_style),
        Paragraph("Credit Distribution Spread", card_sub_cyan),
        Paragraph("1.5% - 2.5% per disbursal", card_stat_green),
        Paragraph("Paytm earns origination fees and risk-sharing spreads from lending partners for pre-underwritten working capital and invoice financing.", body_style)
    ]
    b3 = [
        Paragraph("3. ONDC B2B Wholesale Cut", card_title_style),
        Paragraph("Wholesale Marketplace Take-Rate", card_sub_cyan),
        Paragraph("0.5% - 1.5% of order GMV", card_stat_green),
        Paragraph("Commission on wholesale FMCG replenishment orders routed from merchants to regional distributors via the integrated ONDC protocol.", body_style)
    ]
    b4 = [
        Paragraph("4. Sponsored Brand Discovery", card_title_style),
        Paragraph("Hyper-Local Brand Campaigns", card_sub_cyan),
        Paragraph("Pay-per-trial / Placement", card_stat_green),
        Paragraph("FMCG enterprises (HUL, ITC, Nestlé) pay for targeted promotions, sample placements, and distributor tie-ins targeting high-performing store clusters.", body_style)
    ]

    biz_data = [[b1, b2, b3, b4]]
    biz_table = Table(biz_data, colWidths=[2.35 * inch] * 4, rowHeights=[4.7 * inch])
    biz_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (0,-1), 1, BORDER_COLOR),
        ('BOX', (1,0), (1,-1), 1, BORDER_COLOR),
        ('BOX', (2,0), (2,-1), 1, BORDER_COLOR),
        ('BOX', (3,0), (3,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(biz_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at {filename}")

if __name__ == "__main__":
    out_pdf = r"C:\Users\ShaikAli\.gemini\antigravity\scratch\paytm-merchant-growth-ai\Paytm_VyaparAI_Pitch_Deck.pdf"
    build_pdf(out_pdf)
