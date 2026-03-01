from playwright.sync_api import sync_playwright
import requests
import PyPDF2
import io
import os
from dotenv import load_dotenv

# Load the hidden environment variables immediately
load_dotenv()

def send_telegram_alert(message):
    # Securely fetch credentials from the .env file
    bot_token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    # Failsafe: Check if credentials actually loaded
    if not bot_token or not chat_id:
        print("❌ API Error: Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID in .env file.")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("📲 Telegram alert sent successfully.")
        else:
            print(f"❌ Failed to send alert. Status: {response.status_code}")
    except Exception as e:
        print(f"❌ API Error: {e}")

def run_erasmus_spy():
    with sync_playwright() as p:
        print("Starting Playwright Spy...")
        
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = "https://www.uniroma1.it/it/pagina/bando-erasmus-2026-2027-studio"
        print(f"Navigating to: {url}")
        page.goto(url)

        try:
            page.locator("text='Accetto'").click(timeout=3000)
            print("Cookie banner cleared.")
        except:
            pass 

        print("Hunting for the Letters and Philosophy PDF...")
        faculty_locator = page.locator("a:has-text('Letters and Philosophy'), a:has-text('Lettere e Filosofia')").first

        if faculty_locator.count() > 0:
            pdf_url = faculty_locator.get_attribute("href")
            
            if pdf_url and pdf_url.startswith('/'):
                pdf_url = f"https://www.uniroma1.it{pdf_url}"
                
            print(f"TARGET ACQUIRED: {pdf_url}")
            
            print("Downloading and scanning document...")
            response = requests.get(pdf_url)
            
            pdf_file = io.BytesIO(response.content)
            reader = PyPDF2.PdfReader(pdf_file)
            
            pdf_text = ""
            for page_num in range(len(reader.pages)):
                pdf_text += reader.pages[page_num].extract_text().lower()
            
            targets = ["polonia", "ungheria", "poland", "hungary"]
            found_targets = [country for country in targets if country in pdf_text]
            
            print("-" * 40)
            # This block is now correctly indented INSIDE the faculty locator block
            if found_targets:
                alert_msg = f"🚨 ERASMUS ALERT: Target destinations confirmed in the latest PDF: {', '.join(found_targets).upper()}"
                print(alert_msg)
                send_telegram_alert(alert_msg) 
            else:
                print("Status: Target destinations NOT found in the current document.")
            print("-" * 40)
            
        else: # This now correctly matches the 'if faculty_locator' check
            print("ALERT: Could not find the faculty link.")

        browser.close()

if __name__ == "__main__":
    run_erasmus_spy()