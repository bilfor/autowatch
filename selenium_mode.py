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

# Path to the directory containing geckodriver
geckodriver_dir = '.'

# Add geckodriver directory to the system PATH
os.environ['PATH'] += os.pathsep + geckodriver_dir

# URL of the webpage with the video
url = sys.argv[1]

# Path to Firefox binary
firefox_binary_path = '/usr/bin/firefox'

# Path to Firefox profile with addons
firefox_profile_path = '/home/will/.mozilla/firefox/ev08el9k.default-release'

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
driver.get(url)

# Wait for the page to load
time.sleep(5)

video_element = driver.find_element(By.ID, "video-player")

# Click on the video element
actions = ActionChains(driver)
actions.move_to_element(video_element).click().perform()

driver.execute_script("arguments[0].requestFullscreen();", video_element)
#driver.execute_script("document.documentElement.requestFullscreen();")

