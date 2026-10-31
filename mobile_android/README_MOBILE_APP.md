# 📱 Paytm VyaparAI Mobile Application Guide
## Instant Access on Android, iOS & Paytm Smart POS

Paytm VyaparAI is engineered as an **Installable Progressive Web App (PWA)** and **Native Android Application Wrapper**, enabling 40M+ merchants to carry their AI business copilot on their smartphones with full touch navigation and voice capabilities.

---

### Option 1: Instant 1-Click Mobile Access via Wi-Fi (Zero Setup Required)

1. Make sure your smartphone and laptop are connected to the same Wi-Fi / Hotspot.
2. In your laptop browser, click the **`📱 Mobile App`** button in the top navigation bar.
3. A large QR Code appears pointing to:
   ```text
   http://10.150.24.76:8080/
   ```
4. **Scan the QR Code with your smartphone's camera** (or type `http://10.150.24.76:8080/` in Chrome/Safari).
5. The mobile app will open immediately with full touch navigation and sticky bottom bar.

---

### Option 2: Install as Native App on Your Phone (PWA "Add to Home Screen")

Once opened in your phone's browser:
* **Android (Google Chrome):**
  1. An **"Install Paytm VyaparAI"** banner will slide up from the bottom.
  2. Tap **"Install App"** (or tap the 3 vertical dots `⋮` at the top right → **"Install app"** / **"Add to Home screen"**).
  3. The official Paytm VyaparAI icon will appear on your phone's home screen.
  4. Tap the icon to launch the app in **standalone full-screen mode** with zero browser address bars!
* **iOS (Apple Safari on iPhone):**
  1. Tap the **Share button** (square with upward arrow `⎙`) at the bottom of Safari.
  2. Scroll down and tap **"Add to Home Screen"**.
  3. Tap **"Add"**. The app icon is now on your iPhone home screen!

---

### Option 3: Compile into Native Android `.apk`

The complete Android Studio project structure is provided in `mobile_android/`:
* `AndroidManifest.xml`: Configured with microphone permissions (for Soundbox), internet, and deep links.
* `MainActivity.java`: Fast hardware-accelerated WebView container with native WhatsApp and UPI intent handlers.
* `build.gradle`: Android SDK 34 ready.

To compile:
```bash
cd mobile_android
./gradlew assembleDebug
```
The generated APK will be at `mobile_android/app/build/outputs/apk/debug/app-debug.apk`.
