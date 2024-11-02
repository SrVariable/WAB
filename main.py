from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from time import strftime, localtime, strptime, sleep
import sys
import os

TARGET_URL = "https://lapalabradeldia.com"
TIMESTAMP_FORMAT = "%Y-%m-%d_%H-%M-%S"
LOGGING = False

def extract_timestamp(filename):
    timestamp = filename.replace("backup_","").replace(".txt","")
    return strptime(timestamp, TIMESTAMP_FORMAT)

def load_backup(backup_dir):
    if not os.path.lexists(backup_dir):
        if LOGGING:
            print(f"The directory '{backup_dir}' doesn't exist, creating it...")
        os.mkdir(backup_dir)
        return TARGET_URL

    files = os.listdir(backup_dir)
    files = [f for f in files if os.path.isfile(os.path.join(backup_dir, f))]
    if len(files) == 0:
        if LOGGING:
            print("Couldn't find any backup, going to main page...")
        return TARGET_URL
    backup = max(files, key=extract_timestamp)
    with open(backup_dir + "/" +  backup, "r") as f:
        return f.read()

def create_backup(backup_dir, backup_url):
    if not os.path.lexists(backup_dir):
        if LOGGING:
            print(f"The directory '{backup_dir}' doesn't exist, creating it...")
        os.mkdir(backup_dir)

    # File format: backup_YY-mm-dd_HH-MM-SS.txt
    filename = backup_dir + "/backup_" + strftime(TIMESTAMP_FORMAT, localtime()) + ".txt"
    if LOGGING:
        print(f"Creating the backup in '{filename}'")
    with open(filename, "w") as f:
        f.write(backup_url)

def get_backup_url(driver):
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for button in buttons:
        if button.get_attribute("aria-label") == "Boton Ajustes":
            button.click()
            break
    # 3 tabs, enter, tab, enter get backup link
    for i in range(3):
        ActionChains(driver).send_keys(Keys.TAB).perform()
    ActionChains(driver).send_keys(Keys.ENTER).perform()
    ActionChains(driver).send_keys(Keys.TAB).perform()
    ActionChains(driver).send_keys(Keys.ENTER).perform()
    # Sleep a little to assure that the url is correct
    sleep(2)
    return driver.current_url

def config_driver():
    # It is supposed to work on Ubuntu 24.04, but have to test on other Linux distros
    # because it has to have different paths, or maybe setting the options are not
    # even required
    options = webdriver.FirefoxOptions()
    options.browser_location = "/usr/bin/firefox"
    service = webdriver.firefox.service.Service(executable_path="/snap/bin/geckodriver")
    driver = webdriver.Firefox(service=service, options=options)
    return driver

def reject_cookies(driver):
    if LOGGING:
        print("Rejecting cookies...")

    # Find and click manage options button
    elements = driver.find_elements(By.TAG_NAME, "p")
    for e in elements:
        if e.text == "Manage options":
            e.click()
            break

    # Find and click every input checked
    dialog_contents = driver.find_elements(By.CLASS_NAME, "fc-dialog-content")
    for dialog_content in dialog_contents:
        fc_headers = dialog_content.find_elements(By.CLASS_NAME, "fc-header")
        for fc_header in fc_headers:
            if fc_header.text == "Manage your data":
                checks = dialog_content.find_elements(By.TAG_NAME, "input")
                for check in checks:
                    if check.is_selected():
                        check_parent = check.find_element(By.XPATH, "./..")
                        check_parent.click()
    vendor_button = driver.find_element(By.CLASS_NAME, "fc-navigation-button")
    vendor_button.click()
    for dialog_content in dialog_contents:
        fc_headers = dialog_content.find_elements(By.CLASS_NAME, "fc-header")
        for fc_header in fc_headers:
            if fc_header.text == "Confirm our vendors":
                checks = dialog_content.find_elements(By.TAG_NAME, "input")
                for check in checks:
                    if check.is_selected():
                        check_parent = check.find_element(By.XPATH, "./..")
                        check_parent.click()

    # Click confirm choices
    button_labels = driver.find_elements(By.CLASS_NAME, "fc-button-label")
    for button_label in button_labels:
        if button_label.text == "Confirm choices":
            button_label.click()

    if LOGGING:
        print("Cookies rejected!")

def start_guessing():
    if LOGGING:
        print("""
        How to play:
        - "quit" "-q"        Quits the game
        - "delete" "-d"      Deletes the word
        Anything else will be typed
        """)
    while True:
        if LOGGING:
            guessing = input("Guess the word: ")
        else:
            guessing = input()
        if guessing == "quit":
            break
        if guessing == "delete":
            for i in range(6):
                ActionChains(driver).send_keys(Keys.BACK_SPACE).perform()
            continue
        ActionChains(driver).send_keys(guessing).send_keys(Keys.ENTER).perform()

if __name__ == "__main__":
    # TODO: Add options like:
    #
    # --load=<url>          to manually load the backup url
    # --save-backup=no      to disable auto backup
    # --backup-dir=<path>   to set another backup directory

    program_path = os.path.dirname(os.path.realpath(__file__))
    backup_dir = program_path + "/backup"

    try:
        driver = config_driver()
    except:
        if LOGGING:
            print("Couldn't find the browser")
        sys.exit(1)

    driver.get(TARGET_URL)
    # Sleep a little to assure that the page has loaded
    sleep(2)
    try:
        reject_cookies(driver)
    except:
        if LOGGING:
            print("Something wrong happened while rejecting cookies")
        driver.quit()
        sys.exit(1)

    # Load backup by default
    if True:
        option = "y"
    else:
        option = input("Do you want to load the latest backup? (y/n): ")

    option = option.lower()
    if option[0] == "y":
        url = load_backup(backup_dir)
        driver.get(url)
        if LOGGING:
            print(f"Stats imported! Going back to {TARGET_URL}")

    driver.get(TARGET_URL)
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    #start_guessing()
    sleep(120)

    # Save backup by default
    if True:
        option = "y"
    else:
        option = input("Do you want to backup? (y/n): ")

    option = option.lower()
    if option[0] == "y":
        create_backup(backup_dir, get_backup_url(driver))

    print("- " + strftime("%Y-%m-%d %H:%M:%S", localtime()) + ": " + driver.current_url)
    if LOGGING:
        print("See you!")
    driver.quit()
