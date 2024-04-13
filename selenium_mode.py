from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys

# Path to Firefox GeckoDriver
geckodriver_path = './geckodriver'

# URL of the webpage with the video
url = sys.argv[1]

# Create a Firefox WebDriver instance
driver = webdriver.Firefox(executable_path=geckodriver_path)

# Open the webpage
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Find the video element using its class name
iframe = driver.find_element_by_tag_name('iframe')

# Switch to the iframe
driver.switch_to.frame(iframe)

clappr_player = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'player-container')))

# Execute JavaScript to fullscreen the iframe content
driver.execute_script('document.documentElement.requestFullscreen()')
