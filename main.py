# Chellz Mini Project - IITM BUNKER
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import datetime
import logging

# set logger configuration
logging.basicConfig(filename='history.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s'
                    )

# constants
# use chrome browser
CHROME_PATH = '/home/chella/Desktop/Coding/Python Mini Modules/selenium/chromedriver/chromedriver'
MEET_URL = 'https://meet.google.com/'

# Specify start and start time to open and end the meet
# START_TIME = '13:00'
# END_TIME = '13:47'


def start_end_datetime(start_time, end_time):
    # return start and end time in datetime format
    current_datetime = datetime.datetime.today()
    current_date = current_datetime.strftime('%d-%B-%Y')
    start_datetime = current_date+'-'+start_time
    end_datetime = current_date+'-'+end_time
    start_dt = datetime.datetime.strptime(start_datetime, '%d-%B-%Y-%H:%M')
    end_dt = datetime.datetime.strptime(end_datetime, '%d-%B-%Y-%H:%M')
    return start_dt, end_dt

# data-strcture for the data of each class


class google_meet_class():
    def __init__(self, start_time, end_time, username, password, meet_link):
        self.start_time, self.end_time = start_end_datetime(
            start_time, end_time)
        self.call_type = 'meet'
        self.username = username
        self.password = password
        self.meet_link = meet_link


class webex_class():
    def __init__(self, start_time, end_time, username, email_id, meet_link):
        self.start_time, self.end_time = start_end_datetime(
            start_time, end_time)
        self.call_type = 'webex'
        self.username = username
        self.email_id = email_id
        self.meet_link = meet_link

# # use firefox browser
# FIREFOX_PATH = '/home/chella/Desktop/Coding/Python Mini Modules/selenium/firefoxdriver/geckodriver'
# browser = webdriver.Firefox(executable_path=FIREFOX_PATH)


def open_browser():
    # set notification pop up settings in chrome browser
    # allow camera and mic in pop ups
    opt = Options()
    opt.add_argument("--disable-infobars")
    # opt.add_argument("start-maximized")
    # opt.add_argument('--headless')
    opt.add_argument("--disable-extensions")
    opt.add_argument("--mute-audio")
    # Pass the argument 1 to allow and 2 to block
    opt.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.notifications": 2
    })
    browser = webdriver.Chrome(options=opt, executable_path=CHROME_PATH)
    return browser


def google_meet(browser, start_datetime, end_datetime, username, user_password, meet_link):

    # Google meet stuff
    browser.get(MEET_URL)

    # click on the sign in button
    try:
        sign_in = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.LINK_TEXT, "Sign in"))
        )
        sign_in.click()
    finally:
        logging.info('clicking sign in executing...')

    # enter signin emailid and move to next page
    try:
        mail_id = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.ID, "identifierId"))
        )
        mail_id.send_keys(username)
        mail_id.send_keys(Keys.RETURN)
    finally:
        logging.info('username filling executing...')

    time.sleep(5)
    # enter password and move to next page
    try:
        password = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.NAME, "password"))
        )
        password.send_keys(user_password)
        password.send_keys(Keys.RETURN)
    finally:
        logging.info('password filling executing...')

    # open tab
    # https://python-forum.io/Thread-Need-Help-Opening-A-New-Tab-in-Selenium
    browser.execute_script("window.open('');")

    # implicit wait
    time.sleep(10)

    # swith browser object to new window
    browser.switch_to.window(browser.window_handles[1])

    # open the google meet link in this new tab we created
    browser.get('https://' + meet_link)

    time.sleep(10)

    # mute my mic
    try:
        mic = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "DPvwYc.JnDFsc.dMzo5"))
        )
        mic.click()
    finally:
        logging.info('mute is executing...')

    # block the camera
    try:
        camera = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "GOH7Zb"))
        )
        camera.click()
    finally:
        logging.info('camera blocking is executing...')

    # join the meeting finally
    try:
        join = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "NPEfkd.RveJvd.snByac"))
        )
        join.click()
    finally:
        logging.info('join is executing...')

    # print confidence
    print('google meet class is successfully logged in')
    logging.info('google meet class is successfully logged in')

    # minimize browser
    browser.minimize_window()

    # wait till the class ends
    time_delta = end_datetime - datetime.datetime.now()
    time.sleep(time_delta.seconds)

    # maximize browser
    browser.maximize_window()
    time.sleep(5)

    # close the meet
    try:
        hang_up = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "s1GInc.zCbbgf"))
        )
        hang_up.click()
    finally:
        logging.info('hang up is executing...')

    # quit the browser
    browser.quit()


def webex_meet(browser, start_datetime, end_datetime, username, email_id, meet_link):

    # Webex stuff
    browser.get(meet_link)

    # click join-meeting button, ID: smartJoinButton
    try:
        join_meeting_btn = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.ID, "smartJoinButton"))
        )
        join_meeting_btn.click()
    finally:
        logging.info('clicking join meeting button is executing...')

    # wait for 5 seconds for next page to load
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
        logging.info('username and email id filling is executing...')

    # click next button, ID: guest_next-btn
    try:
        next_btn = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.ID, "guest_next-btn"))
        )
        next_btn.click()
    finally:
        logging.info('clicking next button is executing...')

    # wait for 5 seconds for next page to load
    time.sleep(5)

    # got it button
    try:
        got_it_button = "/html/body/div[4]/div[2]/div/div/div/div/div[1]/button"
        WebDriverWait(browser, 15).until(EC.presence_of_element_located((
            By.XPATH, got_it_button)))
        browser.find_element_by_xpath(
            got_it_button).click()
    except:
        logging.info('There is no got-it banner appearing...')
    else:
        logging.info('Got it banner appeared and successfully removed')

    # when we move on to the next task, We need to come out of the iframe and go to the main frame back
    browser.switch_to.default_content()

    # implicit wait
    time.sleep(5)

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
        logging.info('clicking mute and off camera button is executing...')

    # click join meeting button, ID: interstitial_join_btn
    try:
        join_btn = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.ID, "interstitial_join_btn"))
        )
        join_btn.click()
    finally:
        logging.info('clicking final join button is executing...')

    # print confidence
    print('webex class is successfully logged in')
    logging.info('webex class is successfully logged in')

    # minimize browser
    browser.minimize_window()

    # wait till the class ends
    time_delta = end_datetime - datetime.datetime.now()
    time.sleep(time_delta.seconds)

    # maximize browser
    browser.maximize_window()
    time.sleep(5)

    # quit the browser
    browser.quit()


# Main Part
n = int(input('Total number of classes today = '))
classes = []
for slot in range(n):
    print('Answer the following questions for class'+' '+str(slot+1))
    class_mode = int(
        input('press 1 for google-meet, press 2 for webex-meet = '))
    if class_mode == 1:
        start_time = input(
            'Give start time of this class in 24hr format, eg., 13:00. UR INPUT = ')
        end_time = input(
            'Give end time of this class in 24hr format, eg., 13:50. UR INPUT = ')
        username = input('Provide your smail id = ')
        password = input('Provide your smail id password = ')
        meet_link = input('Provide the full google meet link = ')
        classes.append(google_meet_class(
            start_time, end_time, username, password, meet_link))
    elif class_mode == 2:
        start_time = input(
            'Give start time of this class in 24hr format, eg., 13:00. UR INPUT = ')
        end_time = input(
            'Give end time of this class in 24hr format, eg., 13:50. UR INPUT = ')
        username = input(
            'Provide your name and rollnumber - format("Ram ME17B000") = ')
        email_id = input('Provide your smail id = ')
        meet_link = input('Provide the full webex meet link = ')
        classes.append(webex_class(start_time, end_time,
                                   username, email_id, meet_link))
    else:
        print('Wrong Class Mode')
        print('do it again')

for i in range(len(classes)):
    # find the time deltas for all classes
    time_deltas = []
    current_datetime = datetime.datetime.now()
    for slot in classes:
        time_deltas.append(slot.start_time - current_datetime)
    # sleep till first class starts
    first_class_index = time_deltas.index(min(time_deltas))
    print('We will now wait for ' +
          str(time_deltas[first_class_index].seconds)+'seconds for the next class')
    logging.info('We will now wait for ' +
                 str(time_deltas[first_class_index].seconds)+'seconds for the next class')
    # with 10 second buffer
    time.sleep(time_deltas[first_class_index].seconds + 10)
    # execute the web automation part
    class_now = classes[first_class_index]
    while True:
        current_datetime = datetime.datetime.now()
        if (current_datetime >= class_now.start_time) and ((current_datetime-class_now.start_time).seconds <= 420):
            try:
                browser = open_browser()
                # minimize the browser
                # https://stackoverflow.com/questions/52504503/how-to-execute-tests-with-selenium-webdriver-while-browser-is-minimized?noredirect=1&lq=1
                # browser.minimize_window()
            except Exception as e:
                logging.error('Error with browser opening: '+str(e))
                logging.warning('browser opening failed - trying again...')
                print('browser opening failed - trying again...')
            else:
                logging.info('open browser code is successfully executed')
                try:
                    if class_now.call_type == 'meet':
                        google_meet(browser, class_now.start_time, class_now.end_time,
                                    class_now.username, class_now.password, class_now.meet_link)
                    elif class_now.call_type == 'webex':
                        webex_meet(browser, class_now.start_time, class_now.end_time,
                                   class_now.username, class_now.email_id, class_now.meet_link)
                except Exception as e:
                    logging.error('Error with browser navigations: '+str(e))
                    browser.quit()
                    print('online class is unable to open - trying again...')
                    logging.warning(
                        'online class is unable to open - trying again...')
                else:
                    print('class '+str(i+1)+' with slot ' +
                          str(class_now.start_time.strftime('%H:%M')) + ' is successfully bunked')
                    logging.info('class '+str(i+1)+' with slot ' +
                                 str(class_now.start_time.strftime('%H:%M')) + ' is successfully bunked')
                    break
        elif (current_datetime-class_now.start_time).seconds > 420:
            break
