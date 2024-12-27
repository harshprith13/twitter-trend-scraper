from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from random import choice
import uuid
from datetime import datetime

# MongoDB Setup
client = MongoClient('mongodb://localhost:27017/')  # Connect to MongoDB
db = client['twitter_trends']  # Database name
collection = db['trending_topics']  # Collection name

# ProxyMesh Credentials (Replace with your credentials)
proxy_list = [
     "http://in.proxymesh.com:31280",
    "http://in.proxymesh.com:31280",
    "http://in.proxymesh.com:31280",
]

# Selenium Setup
chrome_options = Options()

# Function to set proxy
def set_proxy():
    proxy = choice(proxy_list)  # Randomly select a proxy
    chrome_options.add_argument(f'--proxy-server={proxy}')

# Set up ChromeDriver with Proxy
set_proxy()  # Set a proxy initially
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Function to log in to Twitter
def login_to_twitter(driver):
    try:
        print("Navigating to Twitter login page...")
        driver.get("https://twitter.com/login")
        WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.NAME, "text")))

        username = "harshprith13"  # Replace with your username
        password = "Waheguru@13"  # Replace with your password
        
        driver.find_element(By.NAME, "text").send_keys(username)
        driver.find_element(By.NAME, "text").send_keys(Keys.RETURN)
        time.sleep(2)
        
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "password")))
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
        print("Successfully logged in!")
    except Exception as e:
        print(f"Error during login: {e}")
        driver.quit()

# Function to scrape top 5 trending topics
# Function to scrape top 5 trending topics
# Function to scrape top 5 trending topics
def scrape_trending_topics(driver):
    try:
        print("Navigating to 'What’s Happening' page...")
        driver.get("https://twitter.com/explore/tabs/trending")
        time.sleep(5)
        
        # Wait for the trending topics to be visible (optional, to ensure content is loaded)
        WebDriverWait(driver, 80).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='trend']")))

        # Find the top 5 trending topics
        trends = driver.find_elements(By.XPATH, "//div[@data-testid='trend']")[:10]
        
        trending_topics = []

        # Loop through the trends and extract their names
        for trend in trends:
            try:
                # Use XPath to find the span containing the topic name (adjust for the specific class)
                topic_name = trend.find_element(By.XPATH, ".//span[@dir='ltr']").text
                trending_topics.append(topic_name)  # Append the topic name to the list
            except Exception as e:
                print(f"Error extracting topic name: {e}")

        print(f"Scraped topics: {trending_topics}")
        return trending_topics

    except Exception as e:
        print(f"Error while scraping trending topics: {e}")
        driver.quit()
        return []
# Function to store data in MongoDB
def store_in_mongodb(trending_topics, ip_address):
    try:
        print("Storing data in MongoDB...")
        
        # Generate a unique ID for the data
        unique_id = str(uuid.uuid4())
        
        # Ensure there are at least 5 topics, pad with empty strings if needed
        while len(trending_topics) < 5:
            trending_topics.append('')  # Add empty strings for missing topics

        # Prepare the data to be stored in MongoDB
        data = {
            "_id": unique_id,
            "trend1": trending_topics[0],
            "trend2": trending_topics[1],
            "trend3": trending_topics[2],
            "trend4": trending_topics[3],
            "trend5": trending_topics[4],
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "ip_address": ip_address
        }
        
        # Insert data into MongoDB collection
        collection.insert_one(data)
        print("Data stored in MongoDB successfully.")
        
    except Exception as e:
        print(f"Error while storing data in MongoDB: {e}")

# Main Script
def main():
    try:
        login_to_twitter(driver)  # Log in to Twitter
        time.sleep(5)
        
        trending_topics = scrape_trending_topics(driver)  # Scrape trending topics
        if trending_topics:
            ip_address = proxy_list[0].split("//")[1]  # Get the first proxy IP used
            store_in_mongodb(trending_topics, ip_address)
    except Exception as e:
        print(f"Error in main function: {e}")
    finally:
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    main()