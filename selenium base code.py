from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import InvalidSessionIdException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.select import Select


# Necessary setup for selenium
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
    "profile.default_content_setting_values.notifications": 2,
    # Change default directory for downloads
    "download.default_directory": "C:\\Users\\johnc\\Desktop\\HPDOWNLOADS",
    "download.prompt_for_download": False,  # To auto download the file
    # just click it and it will download it to this path for pdf's at least.
    "download.directory_upgrade": True,
    # It will not show PDF directly in chrome
    "plugins.always_open_pdf_externally": True,
})
driver = webdriver.Chrome(
    "C:/Users/johnc/chromedriver.exe", options=options)
actions = ActionChains(driver)



def perform_actions():
    """ Perform and reset actions """
    actions.perform()
    actions.reset_actions()
    for device in actions.w3c_actions.devices:
        device.clear_actions()


def find(self):

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, self)))
    return driver.find_element(By.XPATH, self)


def load_page():
    url = driver.current_url
    driver.get(url)


def get_checked(xpath):  # don't put try statement on it because it wont go to correct one
    # sleep(.3) #1 second worked.. trying .3.  ITs needed
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    item = driver.find_element(By.XPATH, xpath)
    checked = item.get_attribute('checked')
    return checked  # returns true if checked


def press_enter():
    actions.send_keys(Keys.ENTER)
    perform_actions()


def find_allow_page_full_load(self):
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, self)))
    return driver.find_element(By.XPATH, self)


def find_elements(xpath):
    WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath)))
    return driver.find_elements(By.XPATH, xpath)


def find_wait(self, wait):
    WebDriverWait(driver, wait).until(
        EC.element_to_be_clickable((By.XPATH, self)))
    return driver.find_element(By.XPATH, self)


def find_stale_element(self):
    p("Looking for stale element:", self)
    ignored_exceptions = (NoSuchElementException,
                          StaleElementReferenceException,)
    your_element = WebDriverWait(driver, 30, ignored_exceptions=ignored_exceptions)\
        .until(EC.presence_of_element_located((By.XPATH, self)))
    return driver.find_element(By.XPATH, self)


def move_to_element(xpath):
    ActionChains(driver).move_to_element(xpath)
    perform_actions()



def click(self):
    try:
        element = find(self)
        actions.move_to_element(element)

        actions.click(element)
        perform_actions()
        # print("first click worked")

    except:
        # print('def click not found on xplicit wait part 1', self)
        try:
            # 2 worked  #1 usually works but maybe not if internet is slow.
            sleep(2)
            driver.find_element(By.XPATH, self).click()
            sleep(1)
            # print("Sleeping on click")
        except:
            # print('def click trying to find xpath after a sleep', self)
            try:
                driver.find_element(By.XPATH, self).click()

            except:
                try:
                    element = find(self)
                    ActionChains(driver).move_to_element(element).click()
                    perform_actions()
                    print("CLICKED IT WORK")

                except Exception as e:
                    p("Find and click did not work:", self)
                    p("EXCEPTION: ", e)


def typing(xpath_to_type_in, words_to_type):
    try:
        sleep(.2)  # was .5
        click(xpath_to_type_in)
        var = find(xpath_to_type_in)
        var.send_keys(words_to_type)
        sleep(.5)

    except:
        p('exception typing sleep 1')
        pass
        try:
            click(xpath_to_type_in)
            sleep(1)
            # var = driver.find_element_by_xpath(xpath_to_type_in)
            var = driver.find_element(By.XPATH, xpath_to_type_in)
            var.send_keys(words_to_type)
            sleep(1)
        except:
            p('exception typing sleep 2')
            pass
            try:
                # click(xpath_to_type_in)
                sleep(2)
                p('a')
                var = find(xpath_to_type_in)
                var.send_keys(words_to_type)
                sleep(2)
            except:
                seq = driver.find_elements_by_tag_name('iframe')
                p("NUmbe of iframes:", len(seq))
                p('exception typing sleep 3: probably didnt click link before it or iframe changed. might need to inspect and search iframe to input that xpath into switch_iframe_function')
                sys.exit()


def typing_backarrow(xpath_to_type_in, num_of_right_arrows, words_to_type):
    sleep(.2)  # was .5
    click(xpath_to_type_in)
    var = find(xpath_to_type_in)

    for i in range(num_of_right_arrows):
        sleep(.1)
        var.send_keys(Keys.ARROW_RIGHT)

    for i in range(num_of_right_arrows*2):
        sleep(.1)
        var.send_keys(Keys.BACKSPACE)

    var.send_keys(words_to_type)
    sleep(.1)


def switch_to_new_window():
    p(driver.current_window_handle)
    p(driver.window_handles)

    try:
        # sleep(4)  # 2 worked but not all the time. #trying to remove this first sleep
        second_window = driver.window_handles[1]
        sleep(3)  # worked at 4
        driver.switch_to.window(second_window)
        sleep(3)  # works better slower, added this extra wait

    except:
        # p(driver.current_window_handle)
        # p('unable to switch to window after attempt 1')
        try:
            sleep(2)
            second_window = driver.window_handles[1]
            sleep(2)
            driver.switch_to.window(second_window)
            # sleep(4)
            p(driver.current_window_handle)
            p(driver.window_handles)
        except:

            pass
            try:
                # sleep(5)
                second_window = driver.window_handles[1]
                sleep(5)  # workd at 10
                driver.switch_to.window(second_window)
                sleep(5)

            except Exception as e:
                p("Switching to new 8687 window")
                p("EXCEPTION: ", e)
                p("Played sound")
                winsound.PlaySound("SystemExit", winsound.SND_ALIAS)


def switch_to_old_window():
    try:
        # sleep(2)
        window_before = driver.window_handles[0]
        sleep(2)
        driver.switch_to.window(window_before)
        sleep(2)
    except:
        print("step22")
        pass
        try:
            sleep(4)
            window_before = driver.window_handles[0]
            sleep(4)
            driver.switch_to.window(window_before)
            sleep(4)
        except:
            p("Step33")
            pass
            try:
                # sleep(8)
                window_before = driver.window_handles[0]
                sleep(5)  # worked at 8
                driver.switch_to.windoww(window_before)
                sleep(5)
            except Exception as e:
                p("Switching to old98 window")
                p("EXCEPTION: ", e)
                p("Played sound")
                winsound.PlaySound("SystemExit", winsound.SND_ALIAS)


def back(times):
    for i in range(times):
        driver.execute_script("window.history.go(-1)")
        sleep(.2)


def get_value(xpath):  # will come back 1 for one selection or another number for another one
    WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.XPATH, xpath)))
    item = driver.find_element(By.XPATH, xpath)
    return item.get_attribute('value')


def switch_iframe(xpath_to_iframe):
    seq = driver.find_elements_by_tag_name('iframe')
    p("NUmbe of iframes:", len(seq))
    iframe_xp = xpath_to_iframe
    iframe = find(iframe_xp)
    driver.switch_to.frame(iframe)
    p("USe this to close iframe and go back to original: driver.switch_to.default_content()")
    # then you have to close it


def get_all_values(xpath, printname):
    # print("loading sleep")
    # print(printname)
    data_dict = {}

    try:
        WebDriverWait(driver, .01).until(
            EC.visibility_of_element_located((By.XPATH, xpath)))
        item = driver.find_element(By.XPATH, xpath)
    except:
        data_dict[printname] = 'None'
        # print("DID NOT FIND: ", printname)
        return data_dict

    keyname = printname

    outer_html = item.get_attribute('outerHTML')
    # print(outer_html)

    if 'type="radio"' in outer_html:
        data = item.get_attribute('checked')

        # print("CHECKED1")
        # print(data)
        if data == None:
            data = 'None'

        data_dict[keyname] = data
        return data_dict

    if 'class="DrpItems10"' in outer_html:

        if 'select' in outer_html:

            try:
                select = Select(driver.find_element(
                    By.XPATH, xpath))  # does find work?
                selected_option = select.first_selected_option
                data = selected_option.text
                # print("FOUND SELECTED1", data)
                if data == None:
                    data = 'None'

                data_dict[keyname] = data
                # print("select returned dict and drpt")
                return data_dict
            except:
                print("passed dropdown")

    if 'select' in outer_html:
        # try:

        select = Select(driver.find_element(
            By.XPATH, xpath))  # does find work?
        selected_option = select.first_selected_option
        data = selected_option.text
        if data == None:
            data = 'None'
        # print("FOUND SELECTED1", data)
        data_dict[keyname] = data
        return data_dict
        # except:
        #     pass
        # print("passed dropdown22")

    data = item.get_attribute('value')
    # print("FOUND VALUE value")
    # print(data)

    if data == 'on':
        data = item.get_attribute('checked')

        # print("CHECKED2")
        print(data)
        if data == None:
            data = 'None'
        data_dict[keyname] = data
        return data_dict

    if data == '':
        pass
        # print("passing empty str")

    else:
        # print("TRYING TO APPEND IT...", keyname)
        data_dict[keyname] = data
        return data_dict

    data = item.get_attribute('checked')

    # print("CHECKEDc")
    print(data)

    data = item.text
    if data == None:
        data = 'None'

    data_dict[keyname] = data

    # print(" DONE  DONE DONE DONE DONE DONE ")
    # print("DATA_DICT: ", data_dict)

    return data_dict


def get_selected(xpath, print_name):
    try:
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, xpath)))
        select = Select(driver.find_element(
            By.XPATH, xpath))  # does find work?
        selected_option = select.first_selected_option
        selected = selected_option.text
        # print(print_name, "SELECTED ITEM:", selected)
        return selected
    except:
        try:
            stale_finder = find_stale_element(xpath)
            selected_option = stale_finder.first_selected_option
            selected = selected_option.text
        except:
            print("Trying to get value exception since get_selected failed")
            value = get_value(xpath)
            return value
