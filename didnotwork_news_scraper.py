import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# Setup Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in background (no browser UI)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open BBC News
url = "https://www.bbc.com/news"
driver.get(url)

# Wait for JavaScript to load
time.sleep(5)

# Find all <script> tags
script_tags = driver.find_elements(By.TAG_NAME, "script")

# Extract JSON-LD structured data (used by BBC for news headlines)
bbc_json = None
for script in script_tags:
    if 'application/ld+json' in script.get_attribute("type"):
        bbc_json = script.get_attribute("innerText")
        break

# Close the browser
driver.quit()

# Process JSON Data
if bbc_json:
    try:
        data = json.loads(bbc_json)  # Parse JSON
        print("\n📰 BBC News Headlines (Extracted from JSON):")
        
        # Extract top 10 articles
        articles = data.get("itemListElement", [])[:10]
        for i, article in enumerate(articles, start=1):
            print(f"{i}. {article['name']}")
    
    except json.JSONDecodeError:
        print("❌ Failed to parse JSON data.")
else:
    print("❌ No JSON data found.")
