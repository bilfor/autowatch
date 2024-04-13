from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import time
import sys
import os
import requests
from bs4 import BeautifulSoup

def find_stream_url(page_url):
    # Send a GET request to the URL
    print(page_url)
    response = requests.get(page_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all anchor tags in the HTML
        links = soup.find_all('iframe')
        
        # Search for the desired link
        for link in links:
            url = link.get('src', '')
            if not 'https:' in url:
                url = 'https:' + url 
            return url
    else:
        print("Failed to retrieve the web page. Status code:", response.status_code)

def find_streams_in_urls(url_list):
    results = {}
    for url in url_list:
        stream_url = find_stream_url(url)
        results[url] = stream_url
    return results

# Path to the directory containing geckodriver
geckodriver_dir = '/home/billy/working/autowatch'

# Add geckodriver directory to the system PATH
os.environ['PATH'] += os.pathsep + geckodriver_dir

# URL of the webpage with the video
url = sys.argv[1]

stream_url = find_stream_url(url)

# Path to Firefox binary
firefox_binary_path = '/home/billy/Downloads/firefox/firefox'

# Path to Firefox profile with addons
firefox_profile_path = '/home/billy/.mozilla/firefox/firefox-profile/ev08el9k.default-release'

# Set Firefox options
firefox_options = FirefoxOptions()
firefox_options.binary_location = firefox_binary_path
firefox_options.profile = firefox_profile_path

# Set Firefox profile preferences
profile = FirefoxProfile(firefox_profile_path)
profile.set_preference("browser.startup.fullscreen", True)

# Create a Firefox WebDriver instance
driver = webdriver.Firefox(options=firefox_options)

# Open the webpage
driver.get(stream_url)

# Wait for the page to load
time.sleep(5)

# video_element = driver.find_element(By.ID, "video-player")
video_element = driver.find_element(By.ID, "volokit_player")

# Click on the video element
actions = ActionChains(driver)
actions.move_to_element(video_element).click().perform()

driver.execute_script("arguments[0].requestFullscreen();", video_element)
#driver.execute_script("document.documentElement.requestFullscreen();")

