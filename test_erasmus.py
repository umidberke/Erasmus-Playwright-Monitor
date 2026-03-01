import requests
import PyPDF2
import io
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_telegram_alert(message):
    bot_token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("❌ API Error: Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID in .env file.")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"❌ Failed to send alert. Status: {response.status_code}")
    except Exception as e:
        print(f"❌ API Error: {e}")

# PYTEST RULE: The function must start with "test_"
# PYTEST FIXTURE: We pass "page" as an argument. Pytest handles the browser automatically.
def test_erasmus_destinations(page):
    print("\n[+] Initiating Pytest Automation Sequence...")
    
    url = "https://www.uniroma1.it/it/pagina/bando-erasmus-2026-2027-studio"
    page.goto(url)

    try:
        page.locator("text='Accetto'").click(timeout=3000)
    except:
        pass 

    faculty_locator = page.locator("a:has-text('Letters and Philosophy'), a:has-text('Lettere e Filosofia')").first
    
    # PYTEST ASSERTION 1: Fail the entire test immediately if the UI changes and the link disappears
    assert faculty_locator.count() > 0, "CRITICAL UI FAILURE: Faculty link not found on the page."

    pdf_url = faculty_locator.get_attribute("href")
    if pdf_url and pdf_url.startswith('/'):
        pdf_url = f"https://www.uniroma1.it{pdf_url}"
        
    print(f"[+] Downloading payload: {pdf_url}")
    response = requests.get(pdf_url)
    
    # PYTEST ASSERTION 2: Fail the test if the server rejects our download request
    assert response.status_code == 200, f"CRITICAL API FAILURE: PDF download rejected. Status: {response.status_code}"
    
    pdf_file = io.BytesIO(response.content)
    reader = PyPDF2.PdfReader(pdf_file)
    
    pdf_text = ""
    for page_num in range(len(reader.pages)):
        pdf_text += reader.pages[page_num].extract_text().lower()
    
    targets = ["polonia", "ungheria", "poland", "hungary"]
    found_targets = [country for country in targets if country in pdf_text]
    
    if found_targets:
        alert_msg = f"🚨 ERASMUS ALERT: Target destinations confirmed: {', '.join(found_targets).upper()}"
        print(alert_msg)
        send_telegram_alert(alert_msg) 
    else:
        print("[-] Target destinations NOT found in the current document.")
        
    # PYTEST ASSERTION 3: If we reach this point without crashing, the test passes.
    assert True