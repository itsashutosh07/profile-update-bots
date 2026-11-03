import os
import re
import sys
import time
import json
import subprocess
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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from gmail_otp_reader import get_otp_from_gmail

# Load credentials from .env file
load_dotenv()
email = os.environ.get("NAUKRI_EMAIL")
password = os.environ.get("NAUKRI_PASSWORD")
headline = os.environ.get("NAUKRI_HEADLINE", "").strip()

# Validate credentials
if not email or not password or not headline:
    print("[ERROR] Missing credentials!")
    print("Please create a .env file with:")
    print("NAUKRI_EMAIL=your_email@example.com")
    print("NAUKRI_PASSWORD=your_password")
    print("NAUKRI_HEADLINE=your_resume_headline")
    exit(1)

# Security: Basic email format validation
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

LOGIN_URL = "https://www.naukri.com/nlogin/login"
PROFILE_URL = "https://www.naukri.com/mnjuser/profile"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

OTP_INPUT_SELECTORS = [
    "input[type='text'][maxlength='1']",
    "input[type='tel'][maxlength='1']",
    "input[placeholder*='OTP' i]",
    "input[id*='otp' i]",
    "input[name*='otp' i]",
    "input[class*='otp' i]",
]


def build_chrome_user_agent():
    """Match User-Agent to installed Chrome to reduce headless fingerprint mismatch."""
    for binary in ("google-chrome", "google-chrome-stable", "chromium-browser", "chromium"):
        try:
            out = subprocess.check_output([binary, "--version"], text=True, stderr=subprocess.STDOUT).strip()
            match = re.search(r"(\d+\.\d+\.\d+\.\d+)", out)
            if match:
                version = match.group(1)
                ua = (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    f"(KHTML, like Gecko) Chrome/{version} Safari/537.36"
                )
                print(f"[INFO] Using Chrome User-Agent for version {version}")
                return ua
        except (FileNotFoundError, subprocess.SubprocessError, OSError):
            continue
    print("[INFO] Using default Chrome User-Agent")
    return DEFAULT_USER_AGENT


USER_AGENT = build_chrome_user_agent()

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


def fail_and_exit(status, message, details=None):
    """Write status, screenshot if possible, and exit with failure."""
    try:
        driver.save_screenshot(os.path.join(log_dir, f"{status.lower()}.png"))
    except Exception:
        pass
    write_status_summary(status=status, message=message, details=details or {})
    print(f"[ERROR] {status}: {message}")
    try:
        driver.quit()
    except Exception:
        pass
    sys.exit(1)


def is_otp_page():
    """True when Naukri OTP challenge UI is visible."""
    page = driver.page_source.lower()
    url = driver.current_url.lower()
    if "enter the otp" in page or "enter otp sent" in page:
        return True
    otp_boxes = driver.find_elements(By.CSS_SELECTOR, "input[type='tel'][maxlength='1'], input[type='text'][maxlength='1']")
    visible_otp = [el for el in otp_boxes if el.is_displayed()]
    return len(visible_otp) >= 4 and ("nlogin" in url or "login" in url)


def is_login_form_visible():
    """True when email/password login form is present."""
    try:
        username = driver.find_elements(By.ID, "usernameField")
        password = driver.find_elements(By.ID, "passwordField")
        return any(el.is_displayed() for el in username) and any(el.is_displayed() for el in password)
    except Exception:
        return False


def is_registration_shell():
    """Detect blank registration SPA that CI sometimes gets instead of login."""
    title = (driver.title or "").lower()
    page = driver.page_source.lower()
    if "register on naukri" in title:
        return True
    if "already registered" in page and "login here" in page and not is_login_form_visible():
        return True
    return False


def ensure_login_page(max_attempts=3):
    """
    Open the real Naukri login form.
    CI sometimes lands on a blank registration shell at /mnjuser/login;
    recover by clicking 'Login here' or navigating to /nlogin/login.
    """
    for attempt in range(1, max_attempts + 1):
        print(f"[→] Opening login page (attempt {attempt}/{max_attempts})...")
        driver.get(LOGIN_URL)
        time.sleep(5)
        print(f"[DEBUG] URL: {driver.current_url}")
        print(f"[DEBUG] Title: {driver.title}")
        driver.save_screenshot(os.path.join(log_dir, f"step_1_login_attempt_{attempt}.png"))

        if is_login_form_visible():
            print("[✓] Login form is visible")
            return

        if is_registration_shell():
            print("[WARN] Registration shell detected instead of login form")
            driver.save_screenshot(os.path.join(log_dir, "step_1_registration_shell.png"))
            # Prefer clicking the header "Login here" link when present
            clicked = False
            for xpath in [
                "//a[contains(translate(., 'LOGINHERE', 'loginhere'), 'login here')]",
                "//a[contains(@href, 'nlogin') or contains(@href, 'Login')]",
                "//*[contains(text(), 'Already Registered')]/a",
            ]:
                try:
                    link = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    link.click()
                    clicked = True
                    print(f"[✓] Clicked login link via: {xpath}")
                    time.sleep(5)
                    break
                except Exception:
                    continue
            if not clicked:
                print("[→] Login link not clickable; forcing /nlogin/login")
                driver.get(LOGIN_URL)
                time.sleep(5)

            if is_login_form_visible():
                print("[✓] Login form visible after recovery")
                return

        # Soft wait for SPA to finish rendering login fields
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "usernameField")))
            print("[✓] Login form appeared after wait")
            return
        except Exception:
            print("[WARN] usernameField still not visible")

    driver.save_screenshot(os.path.join(log_dir, "step_1_login_form_missing.png"))
    fail_and_exit(
        "LOGIN_FAILED",
        "Could not load Naukri login form (got registration/blank page)",
        {"url": driver.current_url, "title": driver.title},
    )


def find_clickable(selectors, timeout=15, description="element"):
    """Try multiple (By, value) selectors until one is clickable."""
    last_err = None
    per_try = max(3, timeout // max(len(selectors), 1))
    for by, value in selectors:
        try:
            el = WebDriverWait(driver, per_try).until(EC.element_to_be_clickable((by, value)))
            print(f"[✓] Found {description} via {by}={value}")
            return el
        except Exception as e:
            last_err = e
            continue
    raise TimeoutException(f"Could not find clickable {description}. Last error: {last_err}")


def collect_visible_otp_inputs():
    """Return visible OTP digit inputs, sorted left-to-right when possible."""
    for selector in OTP_INPUT_SELECTORS:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            visible = [el for el in elements if el.is_displayed()]
            if visible:
                try:
                    visible.sort(key=lambda el: (el.location.get("y", 0), el.location.get("x", 0)))
                except Exception:
                    pass
                return visible
        except Exception:
            continue

    all_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='tel']")
    visible_inputs = [
        inp for inp in all_inputs if inp.is_displayed() and inp.get_attribute("maxlength") == "1"
    ]
    if visible_inputs:
        try:
            visible_inputs.sort(key=lambda el: (el.location.get("y", 0), el.location.get("x", 0)))
        except Exception:
            pass
    return visible_inputs


def set_otp_digit(element, digit):
    """Set one OTP digit and notify React-controlled inputs."""
    driver.execute_script(
        """
        const el = arguments[0];
        const val = arguments[1];
        el.focus();
        el.value = val;
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
        """,
        element,
        digit,
    )


def enter_otp_code(otp_inputs, otp_code):
    """Type OTP into Naukri single- or multi-box fields (one digit per box)."""
    if len(otp_inputs) >= 6 and len(otp_code) == 6:
        print(f"[OTP] Entering OTP in {len(otp_inputs)} separate fields...")
        for i, digit in enumerate(otp_code):
            if i >= len(otp_inputs):
                break
            try:
                otp_inputs[i].click()
                time.sleep(0.15)
                set_otp_digit(otp_inputs[i], digit)
                otp_inputs[i].send_keys(digit)
                print(f"[OTP] Entered digit {i + 1}")
                time.sleep(0.25)
            except Exception as e:
                print(f"[OTP] Error entering digit {i + 1}: {e}")
                set_otp_digit(otp_inputs[i], digit)
    elif otp_inputs:
        print("[OTP] Entering OTP in single field...")
        otp_inputs[0].click()
        time.sleep(0.3)
        otp_inputs[0].clear()
        otp_inputs[0].send_keys(otp_code)
    else:
        raise Exception("No OTP input fields found to enter code")


def enter_otp_via_paste(otp_inputs, otp_code):
    """Paste full OTP into the first box (works on many React OTP widgets)."""
    if not otp_inputs or len(otp_code) != 6:
        enter_otp_code(otp_inputs, otp_code)
        return
    print("[OTP] Entering OTP via paste into first field...")
    clear_otp_inputs(otp_inputs)
    first = otp_inputs[0]
    first.click()
    time.sleep(0.3)
    ActionChains(driver).click(first).send_keys(otp_code).perform()
    time.sleep(0.5)


def otp_fields_contain_code(otp_inputs, otp_code):
    """Best-effort check that OTP boxes hold the expected digits."""
    if len(otp_inputs) < 6 or len(otp_code) != 6:
        return False
    try:
        values = []
        for el in otp_inputs[:6]:
            val = (el.get_attribute("value") or "").strip()
            if not val and driver.execute_script("return arguments[0].value;", el):
                val = str(driver.execute_script("return arguments[0].value;", el)).strip()
            values.append(val)
        combined = "".join(values)
        if combined == otp_code:
            return True
        return all(values[i] == otp_code[i] for i in range(6) if values[i])
    except Exception:
        return False


def clear_otp_inputs(otp_inputs):
    for el in otp_inputs:
        try:
            set_otp_digit(el, "")
            el.clear()
        except Exception:
            pass


def click_otp_verify_button():
    """Click the OTP card Verify button (avoid header/login submit)."""
    verify_selectors = [
        "//*[contains(translate(., 'ENTER THE OTP', 'enter the otp'), 'enter the otp')]"
        "//button[contains(translate(normalize-space(.), 'VERIFY', 'verify'), 'verify')]",
        "//button[contains(translate(normalize-space(.), 'VERIFY', 'verify'), 'verify') "
        "and not(ancestor::*[contains(@class, 'header')])]",
        "//button[contains(translate(normalize-space(.), 'SUBMIT', 'submit'), 'submit')]",
        "//button[contains(translate(normalize-space(.), 'CONTINUE', 'continue'), 'continue')]",
    ]

    for selector in verify_selectors:
        try:
            verify_btn = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, selector))
            )
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();",
                verify_btn,
            )
            print(f"[OTP] Verify button clicked using selector: {selector}")
            return True
        except Exception:
            continue

    if otp_inputs := collect_visible_otp_inputs():
        try:
            otp_inputs[-1].send_keys(Keys.RETURN)
            print("[OTP] Pressed Enter on last OTP field")
            return True
        except Exception:
            pass
    return False


def otp_page_error_snippet(page_text):
    """Return a short visible error string from the OTP page if present."""
    markers = [
        "oops! something went wrong",
        "invalid otp",
        "incorrect otp",
        "otp expired",
        "otp is invalid",
        "please try again",
        "max limit to generate otp",
    ]
    for marker in markers:
        if marker in page_text:
            return marker
    return ""


def is_invalid_otp_error(page_text):
    return any(
        err in page_text
        for err in ("invalid otp", "incorrect otp", "otp expired", "otp is invalid")
    )


def is_transient_otp_error(page_text):
    return any(
        err in page_text
        for err in (
            "something went wrong",
            "please try again",
            "try again after",
        )
    )


def wait_until_logged_in_after_otp(timeout_seconds=45):
    """Wait for navigation away from OTP/login challenge."""
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        url = driver.current_url.lower()
        if not is_otp_page():
            if "nlogin/login" not in url and not is_login_form_visible():
                return True
            if "mnjuser" in url and "login" not in url and "nlogin" not in url:
                return True
        time.sleep(1)
    return False


def click_resend_otp_link():
    """Request a fresh OTP when Naukri shows resend."""
    for xpath in [
        "//*[contains(translate(., 'RESEND', 'resend'), 'resend')]",
        "//a[contains(translate(., 'RESEND', 'resend'), 'resend')]",
        "//button[contains(translate(., 'RESEND', 'resend'), 'resend')]",
    ]:
        try:
            el = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            driver.execute_script("arguments[0].click();", el)
            print("[OTP] Clicked resend OTP")
            time.sleep(3)
            return True
        except Exception:
            continue
    print("[OTP] Resend OTP control not found")
    return False


def submit_otp_for_verification(otp_code, entry_mode, screenshot_suffix):
    """Enter OTP, click verify, return (logged_in, page_error_snippet)."""
    otp_inputs = collect_visible_otp_inputs()
    if not otp_inputs:
        time.sleep(2)
        otp_inputs = collect_visible_otp_inputs()
    if not otp_inputs:
        raise Exception("OTP inputs disappeared before entry")

    if entry_mode == "paste":
        enter_otp_via_paste(otp_inputs, otp_code)
    else:
        enter_otp_code(otp_inputs, otp_code)

    otp_inputs = collect_visible_otp_inputs()
    if otp_inputs and not otp_fields_contain_code(otp_inputs, otp_code):
        print("[OTP] Fields missing digits after entry — retrying digit mode")
        clear_otp_inputs(otp_inputs)
        enter_otp_code(otp_inputs, otp_code)

    driver.save_screenshot(os.path.join(log_dir, f"step_1_otp_entered_{screenshot_suffix}.png"))
    if screenshot_suffix == "paste" or screenshot_suffix == "digits_1":
        driver.save_screenshot(os.path.join(log_dir, "step_1_otp_entered.png"))

    time.sleep(2)
    if not click_otp_verify_button():
        print("[OTP] No verify button found - OTP might auto-submit")

    if wait_until_logged_in_after_otp(timeout_seconds=45):
        driver.save_screenshot(os.path.join(log_dir, "step_1_after_otp_verification.png"))
        return True, ""

    page_text = driver.page_source.lower()
    return False, otp_page_error_snippet(page_text)


def run_otp_verification_flow(login_submit_epoch):
    """
    Fetch Gmail OTP once for this login, then retry verify with alternate entry
    methods. Naukri resend often does not create a new Gmail message.
    """
    driver.save_screenshot(os.path.join(log_dir, "step_1_otp_prompt.png"))
    min_received_after = login_submit_epoch - 30

    print("[OTP] Fetching OTP from Gmail API...")
    session_otp = get_otp_from_gmail(
        sender_filter="naukri.com",
        max_wait_seconds=90,
        min_received_after=min_received_after,
    )
    if not session_otp:
        raise Exception(
            "Failed to retrieve OTP from Gmail for this login attempt "
            "(check Gmail API credentials or inbox delivery)"
        )

    otp_code = session_otp["otp"]
    print(
        f"[OTP] ✓ Session OTP: {otp_code} "
        f"(Gmail id {session_otp['message_id'][:10]}…, subject: {session_otp['subject']!r})"
    )

    entry_modes = ["paste", "digits", "digits"]
    last_page_error = ""

    for idx, mode in enumerate(entry_modes, start=1):
        print(f"[OTP] Verify pass {idx}/{len(entry_modes)} (entry={mode})")
        if idx > 1:
            otp_inputs = collect_visible_otp_inputs()
            if otp_inputs:
                clear_otp_inputs(otp_inputs)
            time.sleep(2)

        try:
            logged_in, page_error = submit_otp_for_verification(
                otp_code, mode, f"{mode}_{idx}"
            )
        except Exception as entry_err:
            print(f"[OTP] Entry error on pass {idx}: {entry_err}")
            continue

        if logged_in:
            print("[✓] OTP verification completed successfully")
            return True

        last_page_error = page_error
        print(f"[DEBUG] URL after OTP: {driver.current_url}")
        if page_error:
            print(f"[OTP] Page error: {page_error}")

        page_text = driver.page_source.lower()
        driver.save_screenshot(os.path.join(log_dir, f"step_1_after_otp_pass_{idx}.png"))

        if is_invalid_otp_error(page_text):
            raise Exception(f"OTP verification failed - invalid/expired OTP ({page_error})")

        if is_transient_otp_error(page_text):
            print("[OTP] Transient Naukri error — will retry with alternate OTP entry")
            time.sleep(3)
            continue

        break

    driver.save_screenshot(os.path.join(log_dir, "step_1_otp_verification_failed.png"))
    detail = last_page_error or "still on login/OTP page after submit"
    raise Exception(f"OTP verification failed - {detail}")


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
options.add_argument(f"--user-agent={USER_AGENT}")
options.add_argument("--lang=en-US,en")

# Additional anti-bot detection
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
})

# Logging
service = Service(ChromeDriverManager().install())
service.log_path = "chromedriver.log"
service.service_args = ["--verbose"]

# Driver
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 20)

# Remove webdriver property to avoid detection
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": USER_AGENT})
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

try:
    # Step 1: Login — use /nlogin/login (mnjuser/login often serves a blank registration shell in CI)
    ensure_login_page()
    driver.save_screenshot(os.path.join(log_dir, "step_1_login_page.png"))

    # Wait for and fill email field with explicit click
    print("[🔍] Locating email field...")
    print(f"[DEBUG] Current URL: {driver.current_url}")
    print(f"[DEBUG] Page title: {driver.title}")
    email_field = find_clickable([
        (By.ID, "usernameField"),
        (By.CSS_SELECTOR, "input[placeholder*='Email']"),
        (By.XPATH, "//input[@type='text' and contains(@placeholder, 'Email')]"),
    ], description="email field")
    email_field.click()
    time.sleep(1)
    email_field.clear()
    email_field.send_keys(email)
    print("[✓] Email entered")
    
    # Fill password field
    password_field = find_clickable([
        (By.ID, "passwordField"),
        (By.CSS_SELECTOR, "input[type='password']"),
        (By.XPATH, "//input[@type='password']"),
    ], description="password field")
    password_field.click()
    time.sleep(1)
    password_field.clear()
    password_field.send_keys(password)
    print("[✓] Password entered")
    
    driver.save_screenshot(os.path.join(log_dir, "step_1_credentials_filled.png"))
    
    # Click login button (prefer the form Login button, not header Login link)
    login_btn = find_clickable([
        (By.XPATH, "//button[@type='submit' and contains(., 'Login')]"),
        (By.XPATH, "//button[@type='submit']"),
        (By.XPATH, "//button[normalize-space()='Login']"),
    ], description="login button")
    login_submit_epoch = time.time()
    login_btn.click()
    time.sleep(8)
    print("[✓] Login button clicked")
    driver.save_screenshot(os.path.join(log_dir, "step_1_after_login_click.png"))
    
    # Check if OTP is required
    try:
        print("[🔍] Checking for OTP prompt...")
        print(f"[DEBUG] Current URL after login: {driver.current_url}")
        print(f"[DEBUG] Page title after login: {driver.title}")
        
        page_source = driver.page_source.lower()
        
        rate_limit_keywords = [
            'max limit to generate otp',
            'reached max limit',
            'try after 24 hours',
            'too many otp requests',
            'otp limit exceeded'
        ]
        
        if any(keyword in page_source for keyword in rate_limit_keywords):
            print("[OTP] 🚫 RATE LIMITED!")
            driver.save_screenshot(os.path.join(log_dir, "step_1_otp_rate_limited.png"))
            write_status_summary(
                status="RATE_LIMITED",
                message="Naukri rate limited OTP requests. Will retry in next scheduled run.",
                details={"retry_in": "6 hours", "expected": True}
            )
            print("[INFO] Exiting gracefully - will retry on next schedule")
            driver.quit()
            print("[INFO] Browser closed.")
            sys.exit(0)
        
        has_otp_text = any(
            text in page_source
            for text in [
                'enter the otp',
                'enter otp',
                'otp sent',
                'verification code',
                'otp to login',
            ]
        )
        print(f"[DEBUG] OTP-related text in page: {has_otp_text}")
        
        otp_inputs = collect_visible_otp_inputs()
        otp_present = len(otp_inputs) >= 4
        
        if has_otp_text and not otp_present:
            print("[OTP] OTP text found but inputs not detected yet, waiting for page to load...")
            time.sleep(5)
            driver.save_screenshot(os.path.join(log_dir, "step_1_otp_page_loading.png"))
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "input[type='text'][maxlength='1'], input[type='tel'][maxlength='1']")
                    )
                )
            except Exception as wait_err:
                print(f"[OTP] Explicit wait for OTP fields: {wait_err}")
            otp_inputs = collect_visible_otp_inputs()
            otp_present = len(otp_inputs) >= 4
        
        if otp_present or has_otp_text:
            print("[OTP] ⚠️  OTP verification required!")
            if otp_inputs:
                print(f"[OTP] Found {len(otp_inputs)} visible OTP input fields")
            run_otp_verification_flow(login_submit_epoch)
        else:
            print("[OTP] ℹ️  No OTP fields detected")
            url_l = driver.current_url.lower()
            if "mnjuser" in url_l and "login" not in url_l and "nlogin" not in url_l:
                print("[OTP] ✅ No OTP required - already on authenticated mnjuser page")
            elif "login" in url_l or "nlogin" in url_l:
                raise Exception("Still on login page after password submit and no OTP UI detected")
            else:
                print("[OTP] ✅ No OTP required - login successful")
    
    except Exception as otp_error:
        print(f"[OTP] ❌ OTP handling error: {str(otp_error)}")
        print(f"[OTP] Traceback: {traceback.format_exc()}")
        driver.save_screenshot(os.path.join(log_dir, "step_1_otp_error.png"))
        page_text = driver.page_source.lower()
        fail_and_exit(
            "OTP_FAILED",
            str(otp_error),
            {
                "url": driver.current_url,
                "title": driver.title,
                "page_error": otp_page_error_snippet(page_text),
            },
        )
    
    # Verify login was successful — require real post-login URL, not page-source heuristics
    print("[🔍] Verifying login status...")
    time.sleep(3)
    current_url = driver.current_url.lower()
    print(f"[DEBUG] Final URL after login: {current_url}")
    driver.save_screenshot(os.path.join(log_dir, "step_1_login_page_check.png"))

    if is_otp_page():
        fail_and_exit(
            "OTP_FAILED",
            "Still on OTP page after login flow",
            {"url": driver.current_url},
        )

    if is_login_form_visible() or "nlogin/login" in current_url or "/login" in current_url.split("?")[0]:
        # Allow only authenticated mnjuser paths
        if not ("mnjuser" in current_url and "login" not in current_url and "nlogin" not in current_url):
            fail_and_exit(
                "LOGIN_FAILED",
                "Login verification failed - still on login page",
                {"url": driver.current_url, "title": driver.title},
            )

    authenticated = (
        ("mnjuser" in current_url and "nlogin" not in current_url and "login" not in current_url)
        or "homepage" in current_url
        or "/mnjuser/profile" in current_url
    )
    if not authenticated:
        fail_and_exit(
            "LOGIN_FAILED",
            "Login verification failed - not on an authenticated Naukri page",
            {"url": driver.current_url, "title": driver.title},
        )

    print("[✓] Login verification passed")
    driver.save_screenshot(os.path.join(log_dir, "step_1_login_success.png"))

    # Step 2: Profile
    print("[→] Navigating to profile page...")
    driver.get(PROFILE_URL)
    time.sleep(8)
    
    # Verify we're on profile page (and not bounced back to login)
    profile_url = driver.current_url.lower()
    if "nlogin" in profile_url or "/login" in profile_url.split("?")[0]:
        fail_and_exit(
            "LOGIN_FAILED",
            "Profile page redirected to login - session not established",
            {"url": driver.current_url},
        )
    if "profile" not in profile_url:
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
    textarea.send_keys(headline)
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