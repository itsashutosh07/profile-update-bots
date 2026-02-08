import os
import sys
import time
import json
import traceback
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

# Security: Basic email format validation
import re
if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
    print(f"[ERROR] Invalid email format: {email}")
    print("Please provide a valid email address")
    exit(1)

# Security: Validate password strength (minimum length)
if len(password) < 8:
    print("[WARNING] Password is very short. Consider using a stronger password.")
    print("[INFO] Continuing anyway...")

# Create timestamped folder for screenshots
timestamp = datetime.now().strftime("%d-%m-%y_%I-%M_%p")
log_dir = os.path.join("Logs Screenshot", timestamp)
os.makedirs(log_dir, exist_ok=True)
print(f"[INFO] Screenshots will be saved in: {log_dir}")

# Function to write status summary for dashboard
def write_status_summary(status, message, details=None):
    """
    Write a status summary file that can be read by the dashboard
    Status can be: SUCCESS, RATE_LIMITED, FAILURE, OTP_FAILED, LOGIN_FAILED
    """
    status_data = {
        "status": status,
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "details": details or {}
    }
    
    status_file = os.path.join(log_dir, "run_status.json")
    try:
        with open(status_file, 'w') as f:
            json.dump(status_data, f, indent=2)
        print(f"[STATUS] Written to {status_file}: {status}")
    except Exception as e:
        print(f"[WARN] Could not write status file: {e}")

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
        print(f"[DEBUG] Current URL after login: {driver.current_url}")
        print(f"[DEBUG] Page title after login: {driver.title}")
        
        # Check if page content contains OTP-related text
        page_source = driver.page_source.lower()
        
        # Check for rate limiting first
        rate_limit_keywords = [
            'max limit to generate otp',
            'reached max limit',
            'try after 24 hours',
            'too many otp requests',
            'otp limit exceeded'
        ]
        
        is_rate_limited = any(keyword in page_source for keyword in rate_limit_keywords)
        
        if is_rate_limited:
            print("[OTP] 🚫 RATE LIMITED!")
            print("[OTP] Naukri has blocked OTP generation due to too many requests.")
            print("[OTP] This is expected when testing frequently.")
            print("[OTP] The bot will try again on the next scheduled run (6 hours).")
            driver.save_screenshot(os.path.join(log_dir, "step_1_otp_rate_limited.png"))
            
            # Write status summary
            write_status_summary(
                status="RATE_LIMITED",
                message="Naukri rate limited OTP requests. Will retry in next scheduled run.",
                details={"retry_in": "6 hours", "expected": True}
            )
            
            # Exit gracefully - this is not a failure, just need to wait
            print("[INFO] Exiting gracefully - will retry on next schedule")
            driver.quit()
            print("[INFO] Browser closed.")
            sys.exit(0)  # Exit with success code since this is expected behavior
        
        has_otp_text = any(text in page_source for text in ['enter the otp', 'enter otp', 'otp sent', 'verification code', 'otp to login'])
        
        print(f"[DEBUG] OTP-related text in page: {has_otp_text}")
        
        # Look for OTP input fields - try multiple selectors
        otp_present = False
        otp_inputs = []
        
        # Common OTP field patterns - try them all
        otp_selectors = [
            "input[type='text'][maxlength='1']",  # Individual digit boxes
            "input[type='tel'][maxlength='1']",    # Tel input with maxlength 1
            "input[placeholder*='OTP' i]",         # OTP placeholder
            "input[id*='otp' i]",                  # OTP in ID
            "input[name*='otp' i]",                # OTP in name
            "input[class*='otp' i]",               # OTP in class
        ]
        
        for selector in otp_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements and len(elements) > 0:
                    # Filter out hidden elements
                    visible_elements = [el for el in elements if el.is_displayed()]
                    if visible_elements:
                        otp_inputs = visible_elements
                        otp_present = True
                        print(f"[OTP] Found {len(visible_elements)} visible OTP input fields using selector: {selector}")
                        break
            except Exception as e:
                print(f"[DEBUG] Error with selector {selector}: {str(e)}")
                continue
        
        # If we found OTP text but no inputs, wait a bit more for page to load
        if has_otp_text and not otp_present:
            print("[OTP] OTP text found but inputs not detected yet, waiting for page to load...")
            time.sleep(5)  # Increased wait time
            
            # Take a screenshot to see what's on the page
            driver.save_screenshot(os.path.join(log_dir, "step_1_otp_page_loading.png"))
            
            # Try again with extended timeout
            for selector in otp_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        visible_elements = [el for el in elements if el.is_displayed()]
                        if visible_elements:
                            otp_inputs = visible_elements
                            otp_present = True
                            print(f"[OTP] Found {len(visible_elements)} OTP fields on retry")
                            break
                except:
                    continue
            
            # If still not found, try waiting for the input to appear
            if not otp_present:
                print("[OTP] Still not found - trying explicit wait...")
                try:
                    wait = WebDriverWait(driver, 10)
                    otp_input = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'][maxlength='1'], input[type='tel'][maxlength='1']"))
                    )
                    otp_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text'][maxlength='1'], input[type='tel'][maxlength='1']")
                    otp_present = True
                    print(f"[OTP] Found {len(otp_inputs)} OTP fields via explicit wait")
                except Exception as wait_err:
                    print(f"[OTP] ❌ Explicit wait failed: {str(wait_err)}")
                    driver.save_screenshot(os.path.join(log_dir, "step_1_otp_inputs_not_found.png"))
        
        if otp_present or has_otp_text:
            print("[OTP] ⚠️  OTP verification required!")
            driver.save_screenshot(os.path.join(log_dir, "step_1_otp_prompt.png"))
            
            # Get OTP from Gmail
            print("[OTP] Fetching OTP from Gmail API...")
            otp_code = get_otp_from_gmail(sender_filter="naukri.com", max_wait_seconds=90)
            
            if not otp_code:
                raise Exception("Failed to retrieve OTP from Gmail - check Gmail API credentials")
            
            print(f"[OTP] ✓ Received OTP: {otp_code}")
            
            # Re-fetch OTP inputs in case page structure changed
            time.sleep(1)
            for selector in otp_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        visible_elements = [el for el in elements if el.is_displayed()]
                        if visible_elements:
                            otp_inputs = visible_elements
                            break
                except:
                    continue
            
            # Enter OTP
            if not otp_inputs:
                # If still no inputs found, try a more generic approach
                print("[OTP] Trying to find OTP inputs more generically...")
                all_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='tel']")
                visible_inputs = [inp for inp in all_inputs if inp.is_displayed() and inp.get_attribute('maxlength') == '1']
                if visible_inputs:
                    otp_inputs = visible_inputs
                    print(f"[OTP] Found {len(otp_inputs)} generic OTP fields")
            
            if len(otp_inputs) >= 6 and len(otp_code) == 6:
                # Multiple input boxes (one digit each) - Naukri's style
                print(f"[OTP] Entering OTP in {len(otp_inputs)} separate fields...")
                for i, digit in enumerate(otp_code):
                    if i < len(otp_inputs):
                        try:
                            # Click to focus
                            otp_inputs[i].click()
                            time.sleep(0.3)
                            # Clear and enter
                            otp_inputs[i].clear()
                            otp_inputs[i].send_keys(digit)
                            print(f"[OTP] Entered digit {i+1}")
                            time.sleep(0.5)
                        except Exception as e:
                            print(f"[OTP] Error entering digit {i+1}: {str(e)}")
            elif otp_inputs:
                # Single input box fallback
                print("[OTP] Entering OTP in single field...")
                otp_inputs[0].click()
                time.sleep(0.5)
                otp_inputs[0].clear()
                otp_inputs[0].send_keys(otp_code)
            else:
                print("[OTP] ⚠️  No OTP input fields found - trying direct page interaction")
                # Last resort - try to find any input and send keys
                time.sleep(2)
            
            print("[OTP] OTP entered, saving screenshot...")
            driver.save_screenshot(os.path.join(log_dir, "step_1_otp_entered.png"))
            
            # Click verify/submit button
            time.sleep(2)
            verify_button_found = False
            verify_selectors = [
                "//button[contains(translate(text(), 'VERIFY', 'verify'), 'verify')]",
                "//button[contains(translate(text(), 'SUBMIT', 'submit'), 'submit')]",
                "//button[contains(translate(text(), 'CONTINUE', 'continue'), 'continue')]",
                "//button[@type='submit']",
                "//input[@type='submit']",
            ]
            
            for selector in verify_selectors:
                try:
                    verify_btn = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    verify_btn.click()
                    print(f"[OTP] Verify button clicked using selector: {selector}")
                    verify_button_found = True
                    break
                except:
                    continue
            
            if not verify_button_found:
                print("[OTP] No verify button found - OTP might auto-submit")
                # Press Enter on last OTP input as fallback
                if otp_inputs:
                    try:
                        otp_inputs[-1].send_keys(Keys.RETURN)
                        print("[OTP] Pressed Enter on last OTP field")
                    except:
                        pass
            
            time.sleep(8)
            driver.save_screenshot(os.path.join(log_dir, "step_1_after_otp_verification.png"))
            print(f"[DEBUG] URL after OTP: {driver.current_url}")
            print(f"[DEBUG] Title after OTP: {driver.title}")
            
            # Check if we're actually logged in
            if "login" in driver.current_url.lower():
                print("[OTP] ⚠️  Still on login page after OTP - verification may have failed")
                driver.save_screenshot(os.path.join(log_dir, "step_1_otp_verification_failed.png"))
                
                # Double-check if we're really stuck or just redirecting
                time.sleep(3)
                if "login" in driver.current_url.lower():
                    # Check if there's an error message
                    page_text = driver.page_source.lower()
                    if any(err in page_text for err in ['invalid otp', 'incorrect otp', 'otp expired', 'otp is invalid']):
                        print("[OTP] ❌ OTP verification failed - invalid/expired OTP")
                        raise Exception("OTP verification failed - invalid/expired OTP")
                    else:
                        print("[OTP] ⚠️  Still on login page but no error - page might be loading slowly")
            else:
                print("[✓] OTP verification completed successfully")
        else:
            print("[OTP] ℹ️  No OTP fields detected")
            print(f"[DEBUG] Checked {len(otp_selectors)} different OTP selectors")
            print(f"[DEBUG] Has OTP text on page: {has_otp_text}")
            
            # Check if we might be logged in already
            page_source_check = driver.page_source.lower()
            if any(indicator in page_source_check for indicator in ['naukri360', 'my naukri', 'mynaukri']):
                print("[OTP] ✅ No OTP required - looks like you're already logged in (existing session)")
            elif "login" in driver.current_url.lower():
                print("[OTP] ⚠️  WARNING: Still on login page but no OTP detected!")
                print("[OTP] This might mean:")
                print("[OTP]   • Already logged in with existing session (local dev)")
                print("[OTP]   • OTP verification needed but wasn't detected (check screenshots)")
            else:
                print("[OTP] ✅ No OTP required - login successful")
    
    except Exception as otp_error:
        print(f"[OTP] ❌ OTP handling error: {str(otp_error)}")
        print(f"[OTP] Traceback: {traceback.format_exc()}")
        driver.save_screenshot(os.path.join(log_dir, "step_1_otp_error.png"))
        print("[OTP] Continuing anyway...")
    
    # Verify login was successful
    print("[🔍] Verifying login status...")
    time.sleep(3)
    current_url = driver.current_url
    print(f"[DEBUG] Final URL after login: {current_url}")
    
    # First, check if we're STILL on the login submission page (not redirected at all)
    is_stuck_on_login = "nlogin/login" in current_url.lower() and "URL=" in current_url
    
    if is_stuck_on_login:
        print("[⚠️] Still on login/OTP page - checking if actually logged in...")
        driver.save_screenshot(os.path.join(log_dir, "step_1_login_page_check.png"))
        
        # Look for login FORM elements - if present, we definitely failed
        try:
            login_button = driver.find_elements(By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'login')]")
            email_field = driver.find_elements(By.CSS_SELECTOR, "input[placeholder*='Email' i], input[placeholder*='email' i]")
            password_field = driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
            
            # If we can still see the login form, we're definitely not logged in
            if (login_button and email_field) or password_field:
                print("[ERROR] ❌ Login form still visible - login/OTP failed!")
                print(f"[DEBUG] Login button found: {len(login_button) > 0}")
                print(f"[DEBUG] Email field found: {len(email_field) > 0}")
                print(f"[DEBUG] Password field found: {len(password_field) > 0}")
                driver.save_screenshot(os.path.join(log_dir, "step_1_login_failed_form_visible.png"))
                raise Exception("Login failed - login form still visible. OTP handling may have failed.")
        except Exception as form_check_err:
            if "Login failed" in str(form_check_err):
                raise  # Re-raise our own exception
            print(f"[DEBUG] Form check error (will proceed): {form_check_err}")
    
    # Check for logged-in indicators
    page_source = driver.page_source.lower()
    logged_in_indicators = {
        'naukri360': 'naukri360' in page_source,
        'my_naukri': 'my naukri' in page_source or 'mynaukri' in page_source,
        'profile_link': '/mnjuser/profile' in page_source or '/mnjuser/homepage' in page_source,
    }
    
    is_logged_in = any(logged_in_indicators.values())
    positive_checks = sum(1 for v in logged_in_indicators.values() if v)
    
    print(f"[DEBUG] Login indicators: {logged_in_indicators}")
    print(f"[DEBUG] Positive indicators: {positive_checks}/3")
    
    if is_logged_in:
        print("[✓] Login verification passed - found logged-in indicators")
    elif not is_stuck_on_login:
        # URL changed but no clear indicators - probably okay
        print("[✓] Login verification: URL changed (assuming success)")
        is_logged_in = True
    else:
        print("[ERROR] ❌ Login verification failed - no logged-in indicators and still on login page")
        driver.save_screenshot(os.path.join(log_dir, "step_1_login_verification_failed.png"))
        raise Exception("Login verification failed - could not confirm successful login")
    
    print("[✓] Login verification completed")
    driver.save_screenshot(os.path.join(log_dir, "step_1_login_success.png"))

    # Step 2: Profile
    print("[→] Navigating to profile page...")
    driver.get("https://www.naukri.com/mnjuser/profile")
    time.sleep(8)
    
    # Verify we're on profile page
    if "profile" not in driver.current_url.lower():
        print(f"[WARN] ⚠️  Not on profile page. Current URL: {driver.current_url}")
        driver.save_screenshot(os.path.join(log_dir, "step_2_not_on_profile.png"))
    else:
        print("[✓] Successfully reached profile page")
    
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
    
    # Write success status
    write_status_summary(
        status="SUCCESS",
        message="Profile headline updated successfully",
        details={"profile_section": "Resume Headline", "automated": True}
    )
    print("[✅] Profile update completed successfully!")

except Exception as e:
    error_type = type(e).__name__
    error_msg = str(e)
    print(f"[ERROR] {error_type}: {error_msg}")
    print(f"[DEBUG] Current URL at error: {driver.current_url}")
    
    try:
        driver.save_screenshot(os.path.join(log_dir, "error_occurred.png"))
        print(f"[INFO] Error screenshot saved")
    except:
        print("[WARN] Could not save error screenshot")
    
    # Write failure status
    write_status_summary(
        status="FAILURE",
        message=f"Script failed: {error_type}",
        details={"error": error_msg, "error_type": error_type, "url": driver.current_url}
    )
    
    # Exit with error code
    sys.exit(1)

finally:
    driver.quit()
    print("[INFO] Browser closed.")