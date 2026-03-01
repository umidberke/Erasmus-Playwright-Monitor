# Erasmus-Playwright-Monitor

An automated, headless UI testing and document parsing pipeline built with Python and Playwright. 

This tool was engineered to autonomously monitor the Sapienza University portal for Erasmus 2026-2027 updates, bypassing UI blockers, extracting dynamic PDF targets, and parsing binary data in-memory to trigger secure mobile API alerts.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Browser Automation:** Playwright (Chromium, Headless)
* **Data Extraction:** Requests, PyPDF2 (In-memory binary parsing via `io.BytesIO`)
* **API Integration:** Telegram Bot API (Push Notifications)
* **Security:** `python-dotenv` for local environment variable isolation

## ⚙️ Architecture & Data Flow
1. **DOM Traversal & UI Bypass:** Launches a headless Chromium instance, navigates to the target university portal, and handles asynchronous cookie consent barriers.
2. **Dynamic Locators:** Utilizes strict Playwright locators to target specific faculty links (Letters and Philosophy) handling both English and raw Italian DOM structures.
3. **In-Memory Parsing:** Intercepts the target PDF URL, downloads the payload via `requests`, and parses the text directly in-memory using `PyPDF2` without writing to the local disk.
4. **Keyword Scanning:** Scans the extracted text stream for target designations (Poland, Hungary).
5. **API Push Notification:** If targets are confirmed, constructs an HTTP POST payload and pushes a secure alert to a registered Telegram mobile client.

## 🚀 Local Setup
1. Clone the repository: `git clone https://github.com/umidberke/Erasmus-Playwright-Monitor.git`
2. Install dependencies: `python -m pip install playwright requests PyPDF2 python-dotenv`
3. Install Playwright browsers: `playwright install`
4. Create a `.env` file in the root directory with your Telegram API credentials:
   ```env
   TELEGRAM_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here