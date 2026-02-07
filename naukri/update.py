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

# Chrome options
options = Options()

# Check if headless mode is requested (via env variable or for server deployment)
headless = os.environ.get("HEADLESS", "false").lower() == "true"
if headless:
    options.add_argument("--headless=new")
    print("[INFO] Running in headless mode (no visible browser)")
else:
    print("[INFO] Running with visible browser")

options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")

# Logging
service = Service(ChromeDriverManager().install())
service.log_path = "chromedriver.log"
service.service_args = ["--verbose"]

# Driver
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 20)

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
    time.sleep(5)
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