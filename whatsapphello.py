import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ✅ Your WhatsApp number (with country code)
phone_number = "+97338314676"  # Replace with actual number
message = "Hello! This is an automated message from Python 😊"

# ✅ Use the existing Chrome session
chrome_profile_path = "C:\\Users\\eggy doge\\AppData\\Local\\Google\\Chrome\\User Data"

# ✅ Configure Chrome Options
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={chrome_profile_path}")  # Keeps session active
options.add_experimental_option("detach", True)  # Keeps browser open

# ✅ Correct way to initialize Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# ✅ Open WhatsApp Web
driver.get("https://web.whatsapp.com")
print("🔹 Checking WhatsApp login status...")

# ✅ Wait for the page to load
time.sleep(5)

# ✅ Check if WhatsApp Web is logged in
logged_in = False
while not logged_in:
    try:
        driver.find_element(By.XPATH, "//div[@id='side']")
        print("✅ WhatsApp is logged in! Proceeding...")
        logged_in = True
    except NoSuchElementException:
        print("⏳ Not logged in yet... Waiting for QR scan.")
        time.sleep(5)  # Keep checking every 5 seconds

# ✅ Open chat for the specific number
driver.get(f"https://web.whatsapp.com/send?phone={phone_number}&text={message}")

# ✅ Wait for the chat to load
time.sleep(10)

# ✅ Find message input box and ensure it sends
try:
    input_box = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
    input_box.click()
    
    # ✅ Use Actions API to simulate Enter keypress properly
    actions = ActionChains(driver)
    actions.move_to_element(input_box)
    actions.send_keys(Keys.ENTER)
    actions.perform()  # Executes the action

    print("✅ Message sent successfully!")
except NoSuchElementException:
    print("❌ Error: Could not find the message input box!")

# ✅ Close browser after a few seconds
time.sleep(5)
driver.quit()
