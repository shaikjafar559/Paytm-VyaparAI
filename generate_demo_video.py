import os
import sys
import asyncio
import cv2
import shutil
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

DEMO_DIR = r"C:\Users\ShaikAli\.gemini\antigravity\scratch\paytm-merchant-growth-ai\demo_video_temp"
OUTPUT_MP4 = r"C:\Users\ShaikAli\Desktop\Paytm_VyaparAI_Demo_Video.mp4"
OUTPUT_WEBM = r"C:\Users\ShaikAli\Desktop\Paytm_VyaparAI_Demo_Video.webm"
WORKSPACE_MP4 = r"C:\Users\ShaikAli\.gemini\antigravity\scratch\paytm-merchant-growth-ai\Paytm_VyaparAI_Demo_Video.mp4"

# Clean previous temp files
if os.path.exists(DEMO_DIR):
    shutil.rmtree(DEMO_DIR, ignore_errors=True)
os.makedirs(DEMO_DIR, exist_ok=True)

CAPTION_SCRIPT = """
(function() {
    // 1. Mouse Follower
    const cursor = document.createElement('div');
    cursor.id = 'demo-cursor';
    cursor.style.cssText = `
        position: fixed;
        width: 22px;
        height: 22px;
        border-radius: 50%;
        background: rgba(0, 186, 242, 0.7);
        border: 2px solid #ffffff;
        pointer-events: none;
        z-index: 9999999;
        transform: translate(-50%, -50%);
        transition: width 0.15s, height 0.15s, background-color 0.15s;
        box-shadow: 0 0 16px rgba(0, 186, 242, 0.95);
        display: none;
    `;
    document.body.appendChild(cursor);

    window.addEventListener('mousemove', (e) => {
        cursor.style.display = 'block';
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    });
    window.addEventListener('mousedown', () => {
        cursor.style.width = '32px';
        cursor.style.height = '32px';
        cursor.style.background = 'rgba(255, 102, 0, 0.85)';
    });
    window.addEventListener('mouseup', () => {
        cursor.style.width = '22px';
        cursor.style.height = '22px';
        cursor.style.background = 'rgba(0, 186, 242, 0.7)';
    });

    // 2. Banner Caption Overlay
    const banner = document.createElement('div');
    banner.id = 'demo-banner-caption';
    banner.style.cssText = `
        position: fixed;
        bottom: 24px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0, 46, 110, 0.94);
        color: #ffffff;
        font-family: 'Inter', system-ui, sans-serif;
        font-size: 15px;
        font-weight: 700;
        padding: 10px 24px;
        border-radius: 9999px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.4);
        border: 2px solid #00baf2;
        z-index: 9999998;
        opacity: 0;
        transition: opacity 0.3s ease, transform 0.3s ease;
        pointer-events: none;
        display: flex;
        align-items: center;
        gap: 12px;
    `;
    document.body.appendChild(banner);

    window.setDemoCaption = function(text, badge = 'PAYTM VYAPAR AI') {
        banner.innerHTML = `<span style="background: #00baf2; color: #002e6e; padding: 3px 10px; border-radius: 6px; font-size: 11px; font-weight: 800; letter-spacing: 0.6px;">${badge}</span> <span>${text}</span>`;
        banner.style.opacity = '1';
        banner.style.transform = 'translateX(-50%) translateY(0)';
    };

    window.hideDemoCaption = function() {
        banner.style.opacity = '0';
        banner.style.transform = 'translateX(-50%) translateY(10px)';
    };
})();
"""

async def smooth_move_to(page, selector):
    try:
        elem = await page.query_selector(selector)
        if elem:
            box = await elem.bounding_box()
            if box:
                target_x = box['x'] + box['width'] / 2
                target_y = box['y'] + box['height'] / 2
                await page.mouse.move(target_x, target_y, steps=12)
                await page.wait_for_timeout(150)
    except Exception as e:
        pass

async def record():
    print("[1/3] Launching Playwright browser & starting video capture...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            record_video_dir=DEMO_DIR,
            record_video_size={"width": 1280, "height": 720},
            viewport={"width": 1280, "height": 720}
        )
        page = await context.new_page()

        print("Navigating to local Paytm VyaparAI terminal (http://127.0.0.1:8080/)...")
        await page.goto("http://127.0.0.1:8080/", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        # Inject Caption and Cursor script
        await page.evaluate(CAPTION_SCRIPT)
        await page.mouse.move(640, 360)
        await page.wait_for_timeout(500)

        # SCENE 1: Welcome & Overview
        print("Recording Scene 1: Overview & Soundbox Connection...")
        await page.evaluate("setDemoCaption('Next-Gen AI Retail OS for 40M+ Bharat Kirana Merchants', 'OVERVIEW')")
        await page.mouse.move(300, 120, steps=15)
        await page.wait_for_timeout(2000)

        # SCENE 2: Standee Modal & Verified QR
        print("Recording Scene 2: Verified Merchant Standee QR...")
        await page.evaluate("setDemoCaption('Official Verified QR Standee (Shaik Japhar - 8310508118@ptyes)', 'STANDee QR')")
        await smooth_move_to(page, "#merchant-qr-btn")
        await page.click("#merchant-qr-btn")
        await page.wait_for_timeout(2500)

        # Close standee modal
        await page.evaluate("closeMerchantQrModal()")
        await page.wait_for_timeout(600)

        # SCENE 3: Soundbox 4.0 Indic Audio Engine
        print("Recording Scene 3: Soundbox Voice Chime...")
        await page.evaluate("setDemoCaption('Soundbox 4.0 Indic Multilingual Audio Engine (Hindi, Telugu, Tamil, English)', 'VOICE CHIME')")
        sound_btns = await page.query_selector_all("#tab-voice button, .soundbox-btn, button:has-text('Hindi'), button:has-text('Telugu')")
        for b in sound_btns[:2]:
            try:
                box = await b.bounding_box()
                if box:
                    await page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2, steps=10)
                    await b.click()
                    await page.wait_for_timeout(1200)
            except Exception:
                pass

        # SCENE 4: Smart Khata & Customer Records
        print("Recording Scene 4: Smart Khata Ledger...")
        await page.evaluate("setDemoCaption('Tab 2: Smart Khata Ledger with Customer Phone Numbers & Balance Sync', 'SMART KHATA')")
        await smooth_move_to(page, "#tab-udhar")
        await page.click("#tab-udhar")
        await page.wait_for_timeout(2000)

        # SCENE 5: Multi-Channel Customer Dispatch (WhatsApp & Telecom SMS)
        print("Recording Scene 5: Multi-Channel Customer Dispatch...")
        await page.evaluate("setDemoCaption('Multi-Channel Dispatch: Real-Time WhatsApp & Telecom SMS Gateway', 'DISPATCH')")
        sms_btn = await page.query_selector("button:has-text('Normal SMS')")
        if sms_btn:
            box = await sms_btn.bounding_box()
            if box:
                await page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2, steps=12)
                await sms_btn.click()
                await page.wait_for_timeout(1500)

                # Send via telecom gateway
                gateway_btn = await page.query_selector("button:has-text('Direct Telecom SMS Gateway Dispatch')")
                if gateway_btn:
                    gbox = await gateway_btn.bounding_box()
                    if gbox:
                        await page.mouse.move(gbox['x'] + gbox['width']/2, gbox['y'] + gbox['height']/2, steps=10)
                        await gateway_btn.click()
                        await page.wait_for_timeout(1800)

                # Switch to WhatsApp Tab
                wa_tab = await page.query_selector("#tab-channel-wa")
                if wa_tab:
                    await wa_tab.click()
                    await page.wait_for_timeout(1500)

                # Close dispatch modal explicitly using JS function
                await page.evaluate("closeWhatsAppDispatchModal()")
                await page.wait_for_timeout(800)

        # SCENE 6: Payment Tracker Tab & Real-Time Receipt Modal
        print("Recording Scene 6: Payment Tracker & Instant Payment Modal...")
        await page.evaluate("setDemoCaption('Tab 7: Live Payment Tracker & Passbook with KPI Analytics', 'PASSBOOK')")
        await smooth_move_to(page, "#tab-tracker")
        await page.click("#tab-tracker")
        await page.wait_for_timeout(1800)

        # Simulate Payment
        await page.evaluate("setDemoCaption('Simulating Real-Time Customer UPI Payment Ingestion', 'LIVE PAYMENT')")
        name_input = await page.query_selector("#sim-pay-name")
        amt_input = await page.query_selector("#sim-pay-amt")
        if name_input and amt_input:
            await name_input.fill("Shaik Jafar")
            await amt_input.fill("1250")
            pay_btn = await page.query_selector("button:has-text('Receive Payment')")
            if pay_btn:
                await smooth_move_to(page, "button:has-text('Receive Payment')")
                await pay_btn.click()
                await page.wait_for_timeout(2500)

                # View Receipt Modal
                await page.evaluate("setDemoCaption('Instant Payment Received Modal with RRN, Checkmark & Print Receipt', 'RECEIPT ENGINE')")
                await page.wait_for_timeout(2500)

                # Close Receipt Modal explicitly
                await page.evaluate("closePaymentReceivedModal()")
                await page.wait_for_timeout(800)

        # Scroll passbook feed
        await page.evaluate("setDemoCaption('Automated Passbook Ledger with Replay Voice Chimes & CSV Export', 'PASSBOOK')")
        await page.evaluate("window.scrollBy({ top: 300, behavior: 'smooth' })")
        await page.wait_for_timeout(1500)
        await page.evaluate("window.scrollBy({ top: -300, behavior: 'smooth' })")
        await page.wait_for_timeout(1000)

        # SCENE 7: ONDC Wholesale Restock
        print("Recording Scene 7: ONDC Wholesale Restock...")
        await page.evaluate("setDemoCaption('Tab 4: Autonomous ONDC Wholesale Restocking Engine', 'ONDC SUPPLY')")
        await smooth_move_to(page, "#tab-demand")
        await page.click("#tab-demand")
        await page.wait_for_timeout(2000)

        # SCENE 8: Instant Working Capital Credit
        print("Recording Scene 8: Instant Credit...")
        await page.evaluate("setDemoCaption('Tab 5: Cash-Flow Velocity Underwriting (₹5,00,000 Pre-Approved Credit)', 'FINTECH')")
        await smooth_move_to(page, "#tab-credit")
        await page.click("#tab-credit")
        await page.wait_for_timeout(2000)

        # SCENE 9: Mobile Phone Simulator
        print("Recording Scene 9: Mobile Phone Simulator...")
        await page.evaluate("setDemoCaption('Cross-Platform Mobile PWA & Offline Store Simulator', 'MOBILE APP')")
        try:
            await page.evaluate("openMobileSimulator()")
            await page.wait_for_timeout(2800)
            await page.evaluate("closeMobileSimulator()")
            await page.wait_for_timeout(800)
        except Exception:
            pass

        # SCENE 10: Conclusion
        print("Recording Scene 10: Conclusion...")
        await page.evaluate("setDemoCaption('Paytm VyaparAI: Transforming 40M+ Bharat Merchants into Smart Retailers', 'COMPLETE')")
        await smooth_move_to(page, "#tab-voice")
        await page.click("#tab-voice")
        await page.wait_for_timeout(2500)

        # Get recorded video path before closing
        video_path = await page.video.path()
        print(f"Recorded raw WebM video to: {video_path}")

        await context.close()
        await browser.close()
        return video_path

def convert_to_mp4(webm_path):
    print(f"[2/3] Processing WebM: {webm_path}")
    shutil.copyfile(webm_path, OUTPUT_WEBM)
    print(f"Saved pristine WebM video to Desktop: {OUTPUT_WEBM}")

    print(f"[3/3] Converting frames to MP4: {OUTPUT_MP4}...")
    cap = cv2.VideoCapture(webm_path)
    if not cap.isOpened():
        print("Notice: OpenCV could not read raw stream directly, WebM is already available.")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(OUTPUT_MP4, fourcc, fps, (width, height))
    out_ws = cv2.VideoWriter(WORKSPACE_MP4, fourcc, fps, (width, height))

    frames = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        out_ws.write(frame)
        frames += 1

    cap.release()
    out.release()
    out_ws.release()
    print(f"Successfully rendered MP4 ({frames} frames @ {fps} FPS): {OUTPUT_MP4}")

if __name__ == '__main__':
    raw_video = asyncio.run(record())
    if raw_video and os.path.exists(raw_video):
        convert_to_mp4(raw_video)
        print("ALL OPERATIONS COMPLETED! Video ready on Desktop!")
