from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import datetime

# constants
# use chrome browser
CHROME_PATH = '/home/Desktop/Coding/Python Mini Modules/selenium/chromedriver/chromedriver'
MEET_URL = 'https://meet.google.com/'

username = 'Rohit'
email_id = 'me17b179@smail.iitm.ac.in'
meet_link = 'https://meet66.webex.com/meet/pr1587341261'


# set notification pop up settings in chrome browser
# allow camera and mic in pop ups
opt = Options()
opt.add_argument("--disable-infobars")
# opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.notifications": 2
})
browser = webdriver.Chrome(options=opt, executable_path=CHROME_PATH)


# Webex stuff
# Google meet stuff
browser.get(meet_link)

# click join-meeting button, ID: smartJoinButton
try:
    join_meeting_btn = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located(
            (By.ID, "smartJoinButton"))
    )
    join_meeting_btn.click()
finally:
    print('clicking join meeting button is executed...')

# wait for 3 seconds for next page to load
time.sleep(5)

# fill in username and smail id, CLASS: style-input-2nuAk undefined
# Here is the tricky part, webex clever guys tried to hide every html important elements into some shit called iframe tags
# we need to first navigate to the iframe and then search for the element
# browser.switch_to.frame(
#     "pbui_iframe")
WebDriverWait(browser, 10).until(
    EC.frame_to_be_available_and_switch_to_it((
        By.ID, "pbui_iframe")))
try:
    form_inputs = WebDriverWait(browser, 20).until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, "style-input-2nuAk.undefined"))
    )
    form_inputs[0].send_keys(username)
    form_inputs[1].send_keys(email_id)
finally:
    print('username and email id filling executed...')

# click next button, ID: guest_next-btn
try:
    next_btn = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located(
            (By.ID, "guest_next-btn"))
    )
    next_btn.click()
finally:
    print('clicking next button is executed...')

# wait for 3 seconds for next page to load
time.sleep(3)

# when we move on to the next task, We need to come out of the iframe and go to the main frame back
browser.switch_to.default_content()

# Again webex clever guys tried to hide inportant html elements in this page inside iframe
# so we need to navigate to the appropriate iframe again
# browser.switch_to.frame(
#     "pbui_iframe")
WebDriverWait(browser, 10).until(
    EC.frame_to_be_available_and_switch_to_it((
        By.ID, "pbui_iframe")))

# Mute and off the camera
try:
    mic_cam_btns = WebDriverWait(browser, 20).until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, "style-text-vqI8d"))
    )
    mic_cam_btns[0].click()
    mic_cam_btns[1].click()
finally:
    print('clicking mute and off camera is executed...')

# click join meeting button, ID: interstitial_join_btn
try:
    join_btn = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located(
            (By.ID, "interstitial_join_btn"))
    )
    join_btn.click()
finally:
    print('Click final join button is executed...')


# # quit the browser
# browser.quit()
