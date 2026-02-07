import os
import time
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from gmail_otp_reader import get_otp_from_gmail

# Load credentials from .env file
load_dotenv()
email = os.environ.get("NAUKRI_EMAIL")
password = os.environ.get("NAUKRI_PASSWORD")

# Validate credentials
if not email or not password:
    print("[ERROR] Missing credentials!")
    print("Please create a .env file with:")
    print("NAUKRI_EMAIL=your_email@example.com")
    print("NAUKRI_PASSWORD=your_password")
    exit(1)

# Create timestamped folder for screenshots
timestamp = datetime.now().strftime("%d-%m-%y_%I-%M_%p")
log_dir = os.path.join("Logs Screenshot", timestamp)
os.makedirs(log_dir, exist_ok=True)
print(f"[INFO] Screenshots will be saved in: {log_dir}")

# Print ChromeDriver info only (skip broken chrome version detection on Windows)
print("ChromeDriver path (via webdriver-manager):")
print(ChromeDriverManager().install())

# Chrome options with anti-detection
options = Options()

# Check if headless mode is requested (via env variable or for server deployment)
headless = os.environ.get("HEADLESS", "false").lower() == "true"
if headless:
    options.add_argument("--headless=new")
    print("[INFO] Running in headless mode (no visible browser)")
else:
    print("[INFO] Running with visible browser")

# Anti-detection measures
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36")

# Additional anti-bot detection
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Logging
service = Service(ChromeDriverManager().install())
service.log_path = "chromedriver.log"
service.service_args = ["--verbose"]

# Driver
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 20)

# Remove webdriver property to avoid detection
driver.execute_cdp_cmd('Network.setUserAgentOverride', {
    "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36'
})
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

try:
    # Step 1: Login
    driver.get("https://www.naukri.com/mnjuser/login")
    time.sleep(8)
    driver.save_screenshot(os.path.join(log_dir, "step_1_login_page.png"))

    # Wait for and fill email field with explicit click
    print("[🔍] Locating email field...")
    print(f"[DEBUG] Current URL: {driver.current_url}")
    print(f"[DEBUG] Page title: {driver.title}")
    email_field = wait.until(EC.element_to_be_clickable((By.ID, "usernameField")))
    email_field.click()
    time.sleep(1)
    email_field.clear()
    email_field.send_keys(email)
    print("[✓] Email entered")
    
    # Fill password field
    password_field = wait.until(EC.element_to_be_clickable((By.ID, "passwordField")))
    password_field.click()
    time.sleep(1)
    password_field.clear()
    password_field.send_keys(password)
    print("[✓] Password entered")
    
    driver.save_screenshot(os.path.join(log_dir, "step_1_credentials_filled.png"))
    
    # Click login button
    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    login_btn.click()
    time.sleep(8)
    print("[✓] Login button clicked")
    driver.save_screenshot(os.path.join(log_dir, "step_1_after_login_click.png"))
    
    # Check if OTP is required
    try:
        print("[🔍] Checking for OTP prompt...")
        
        # Look for OTP input fields - try multiple selectors
        otp_present = False
        otp_inputs = []
        
        # Common OTP field patterns
        otp_selectors = [
            "input[type='text'][maxlength='1']",  # Individual digit boxes
            "input[placeholder*='OTP' i]",  # OTP placeholder
            "input[id*='otp' i]",  # OTP in ID
            "input[name*='otp' i]",  # OTP in name
        ]
        
        for selector in otp_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    otp_inputs = elements
                    otp_present = True
                    print(f"[OTP] Found {len(elements)} OTP input fields")
                    break
            except:
                continue
        
        if otp_present:
            print("[OTP] OTP verification required!")
            driver.save_screenshot(os.path.join(log_dir, "step_1_otp_prompt.png"))
            
            # Get OTP from Gmail
            print("[OTP] Fetching OTP from Gmail...")
            otp_code = get_otp_from_gmail(sender_filter="naukri.com", max_wait_seconds=90)
            
            if not otp_code:
                raise Exception("Failed to get OTP from Gmail")
            
            print(f"[OTP] Received OTP: {otp_code}")
            
            # Enter OTP
            if len(otp_inputs) >= len(otp_code):
                # Multiple input boxes (one digit each)
                print(f"[OTP] Entering OTP in {len(otp_inputs)} separate fields...")
                for i, digit in enumerate(otp_code):
                    if i < len(otp_inputs):
                        otp_inputs[i].clear()
                        otp_inputs[i].send_keys(digit)
                        time.sleep(0.5)
            else:
                # Single input box
                print("[OTP] Entering OTP in single field...")
                otp_inputs[0].clear()
                otp_inputs[0].send_keys(otp_code)
            
            print("[OTP] OTP entered")
            driver.save_screenshot(os.path.join(log_dir, "step_1_otp_entered.png"))
            
            # Click verify/submit button
            try:
                verify_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Verify') or contains(text(), 'Submit') or contains(text(), 'Continue')]"))
                )
                verify_btn.click()
                print("[OTP] Verify button clicked")
            except:
                # OTP might auto-submit
                print("[OTP] No verify button found (might auto-submit)")
            
            time.sleep(5)
            driver.save_screenshot(os.path.join(log_dir, "step_1_after_otp_verification.png"))
            print("[✓] OTP verification completed")
        else:
            print("[OTP] No OTP required - login successful")
    
    except Exception as otp_error:
        print(f"[OTP] OTP handling error: {str(otp_error)}")
        driver.save_screenshot(os.path.join(log_dir, "step_1_otp_error.png"))
        # Continue anyway - might not need OTP
    
    print("[✓] Logged in")
    driver.save_screenshot(os.path.join(log_dir, "step_1_login_success.png"))

    # Step 2: Profile
    driver.get("https://www.naukri.com/mnjuser/profile")
    print("[→] Navigated to profile page")
    time.sleep(5)
    driver.save_screenshot(os.path.join(log_dir, "step_2_profile_page.png"))
    time.sleep(3)

    # Step 3: Resume Headline
    print("[🔍] Locating Resume Headline section...")
    edit_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[text()='Resume headline']/following-sibling::span[contains(@class, 'edit')]")
    ))
    driver.save_screenshot(os.path.join(log_dir, "step_3_resume_headline_section_found.png"))
    edit_btn.click()
    print("[✏️] Clicked edit")
    time.sleep(2)
    driver.save_screenshot(os.path.join(log_dir, "step_3_edit_clicked.png"))

    # Step 4: Update text
    textarea = wait.until(EC.visibility_of_element_located((By.ID, "resumeHeadlineTxt")))
    textarea.click()
    time.sleep(1)
    textarea.clear()
    updated_text = (
        "Experienced Backend Software Engineer, Software Development, Backend Development, Microservices, Agile, Java, SpringBoot, Redis, Kafka, MySQL, Python,  Jenkins, Git, AWS, HTML, CSS, JS, Golang, Mongo, CI/CD, AI, MCP, RAG, Agentic AI, Databases, GenAI"
    )
    textarea.send_keys(updated_text)
    print("[✓] Text updated")
    driver.save_screenshot(os.path.join(log_dir, "step_4_text_updated.png"))

    # Step 5: Save
    time.sleep(2)
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Save']")))
    save_btn.click()
    time.sleep(3)
    print("[✓] Resume Headline updated")
    driver.save_screenshot(os.path.join(log_dir, "step_5_save_clicked.png"))

except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {str(e)}")
    print(f"[DEBUG] Current URL at error: {driver.current_url}")
    try:
        driver.save_screenshot(os.path.join(log_dir, "error_occurred.png"))
        print(f"[INFO] Error screenshot saved")
    except:
        print("[WARN] Could not save error screenshot")

finally:
    driver.quit()
    print("[INFO] Browser closed.")