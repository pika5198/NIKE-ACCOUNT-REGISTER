import time
import zipfile
import os
from selenium import webdriver
import pandas as pd
import re
from selenium.webdriver.support.ui import Select
import requests
from bs4 import BeautifulSoup



def set_proxy(proxy_ip):
    IP = proxy_ip
    test = re.search(r'(.*):(.*):(.*):(.*)', IP, re.M | re.I)
    PROXY_HOST = test.group(1)  # rotating proxy or host
    PROXY_PORT = test.group(2)  # port
    PROXY_USER = test.group(3)  # username
    PROXY_PASS = test.group(4)  # password

    # chrome_path = 'chromedriver.exe'
    plugin_path = "proxy_auth_plugin.zip"

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    with zipfile.ZipFile(plugin_path, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
    return plugin_path


def get_chromedriver(plugin_path,use_proxy=True, user_agent=None):
    # path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        # chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument('--incognito')
        chrome_options.add_extension(plugin_path)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver



def registered_acc(Emailadreess , pwd , BillingFirst , BillingLast , birthday):
    driver.maximize_window()
    driver.get("https://www.nike.com/")
    time.sleep(2)
    driver.get("https://www.nike.com/us/login")
    # driver.get("https://www.nike.com/register")
    time.sleep(3)
    register_button = driver.find_element_by_xpath('//div[@class = "nike-unite-component action-link loginJoinLink current-member-signin"]/a')
    register_button.click()
    # continue_button = driver.find_element_by_xpath("//input[@value='JOIN US']")
    # driver.execute_script("submitLink('javascript:void(0)')")
    now_url = driver.current_url
    time.sleep(2)
    if now_url == "https://www.nike.com/us/login" or "https://www.nike.com/login":
        emailAddress_input = driver.find_element_by_name("emailAddress")
        password_input = driver.find_element_by_name("password")
        firstName_input = driver.find_element_by_name("firstName")
        lastName_input = driver.find_element_by_name("lastName")
        dateOfBirth_input = driver.find_element_by_name("dateOfBirth")
        time.sleep(2)
        emailAddress_input.send_keys(Emailadreess)
        time.sleep(2)
        password_input.send_keys(pwd)
        time.sleep(2)
        try:
            if driver.find_element_by_xpath('//div[@class = "nike-unite-component action-link duplicateEmailSignIn"]'):
                time.sleep(1)
                driver.find_element_by_xpath('//div[@class = "nike-unite-component action-link duplicateEmailSignIn"]/a').click()
                emailAddress_input = driver.find_element_by_name("emailAddress")
                password_input = driver.find_element_by_name("password")
                time.sleep(1)
                # for i in Emailadreess:
                #     time.sleep(0.3)
                #     emailAddress_input.send_keys(i)
                for b in pwd:
                    time.sleep(0.05)
                    password_input.send_keys(b)
                signin_button = driver.find_element_by_xpath(
                    "//input[@value='SIGN IN']")
                time.sleep(2)
                signin_button.click()
                time.sleep(4)
                now_url = driver.current_url
                time.sleep(1)
                if now_url == 'https://www.nike.com/':
                    print(f"looks like {Emailadreess} is already a Member,trying to login...")
                    print("login successful.....")
                    return "step1 Successful.." 
                else:
                    print('login failed...')
                    driver.quit()
                    return 'login failed'
        except:
            pass
        firstName_input.send_keys(BillingFirst)
        time.sleep(2)
        lastName_input.send_keys(BillingLast)
        time.sleep(2)
        dateOfBirth_input.send_keys(birthday)
        time.sleep(2)
        gender_button = driver.find_element_by_xpath(
            '//ul[@data-componentname="gender"]/li')
        gender_button.click()
        time.sleep(2)
        continue_button = driver.find_element_by_xpath(
            "//input[@value='JOIN US']")
        time.sleep(3)
        continue_button.click()
        time.sleep(10)
        now_url = driver.current_url
        time.sleep(2)
        if now_url == 'https://www.nike.com/':
            print("register successful.....")
            return "step1 Successful.." 
        else:
            driver.quit()
            print('register failed...')
            return 'register failed'
    else:
        time.sleep(2)
        driver.quit()
        return "login_proxy_error"

def confirm_phonenumber(phone,country):
    driver.get("https://www.nike.com/member/settings")
    time.sleep(3)
    confirm_url = driver.current_url
    if confirm_url == "https://www.nike.com/member/settings":
        print("submiting phone number...")
        try:
            confirm_phonenumber_if = driver.find_element_by_xpath("//span[@class='fs-block']")
            if confirm_phonenumber_if:
                driver.quit()
                print("account has already added phone number...")
                return 'resister successful!'
        except:
            pass
        time.sleep(1)
        add_button = driver.find_element_by_xpath(
            "//button[@aria-label='Add Mobile Number']")
        time.sleep(1)
        add_button.click()
        time.sleep(1)
        driver.find_element_by_xpath(f"//select[@class='country']").click()
        time.sleep(1)
        driver.find_element_by_xpath(f"//option[@value='{country}']").click()
        time.sleep(1)
        phoneNumber_input = driver.find_element_by_xpath(
            "//input[@data-componentname='phoneNumber']")
        time.sleep(0.5)
        for a in phone:
            time.sleep(0.05)
            phoneNumber_input.send_keys(a)
        time.sleep(1)
        send_button = driver.find_element_by_xpath(
            "//input[@class='sendCodeButton']")
        time.sleep(1)
        send_button.click()
        time.sleep(1)
        return "send msg"
        # driver.close()
    else:
        time.sleep(2)
        driver.close()
        print("confirm failed")
        return "confirm failed" 

def get_msg_code(api):
    print("getting sms code..")
    ss = requests.session()
    time.sleep(2)
    for i in range(0,11):
        msg_code_text = ss.get(api)
        soup = BeautifulSoup(msg_code_text.content, 'lxml')
        msg_text = str(soup.text)
        time.sleep(1)
        matchObj = re.match( r'.*(\d{6}).*', msg_text, re.M|re.I)
        print(msg_text)
        if matchObj:
            print(matchObj.group(1))
            msg_code = str(matchObj.group(1))
            return msg_code
        elif i != 10:
            print(f"retrying getting message - {i+1}...")
            time.sleep(3)
        elif i == 10:
            driver.quit()
            print('not found message..')
            return "no message"
        

def fill_code(msg_code_status_code):
    enter_code_input = driver.find_element_by_xpath(
            "//input[@placeholder='Enter Code']")
    checkbox = driver.find_element_by_xpath(
            "//input[@name='progressMobile']")
    continue_button = driver.find_element_by_xpath(
            "//input[@value='CONTINUE']")
    time.sleep(3)
    for a in msg_code_status_code:
            time.sleep(0.1)
            enter_code_input.send_keys(a)
    time.sleep(3)
    checkbox.click()
    time.sleep(1)
    continue_button.click()
    time.sleep(2)

def double_check(phone):
    time.sleep(2)
    try:
        now_phone_number = driver.find_element_by_xpath(
                "//div[@class='ncss-col-sm-6 va-sm-m']/span/span")
        print(now_phone_number.text)
        if phone in now_phone_number.text:
            time.sleep(1)
            driver.quit()
            print('resister successful!!')
            return 'resister successful!'
        else:
            driver.quit()
            print('resister failed!!')
            return 'resister failed!'
    except:
        driver.quit()
        print('resister failed!!!')
        return 'resister failed !!'


if __name__ == '__main__':
    # item_code = input("product code : ")
    # product_link = f"https://alleyoop.shop/form1.php?item_code={item_code}"
    profile = "profiles.csv"
    df = pd.read_csv(profile, delimiter=',', skiprows=0, header=0,dtype=str)
    country = input("what is phone country(ex:CA US): ").upper()
    print(df.head())
    for i in range(0, len(df)):
        try:
            print(f"\n+starting task-{i+1}")
            # ProfileName = str(df["ProfileName"][i])
            Emailadreess = str(df["Emailadreess"][i])
            print(Emailadreess)
            pwd = str(df["pwd"][i])
            BillingFirst = str(df["BillingFirst"][i])
            BillingLast = str(df["BillingLast"][i])
            birthday = str(df["birthday"][i])
            proxy_ip = str(df["proxy"][i])
            api = str(df["api"][i])
            phone = str(df["phone"][i])
            status = str(df["status"][i])
            if status == "register successful":
                print(f"{Emailadreess} is already a Member,skiping....")
                continue
            print(status)
            plugin_path = set_proxy(proxy_ip)
            driver = get_chromedriver(plugin_path,use_proxy=True)
            status_code1 = registered_acc(Emailadreess , pwd , BillingFirst , BillingLast , birthday)
            if status_code1 == "step1 Successful..":
                print("account register successful")
                time.sleep(2)
                print("starting confirm phonenumber..")
                status_code2 = confirm_phonenumber(phone,country)
                time.sleep(1)
                if status_code2 == "send msg":
                    time.sleep(1)
                    msg_code_status_code = get_msg_code(api)
                    time.sleep(1)
                    if msg_code_status_code == "no message":
                        df['status'][i] = 'no message'
                    else:
                        print("successfully got code...")
                        time.sleep(1)
                        fill_code(msg_code_status_code)
                        time.sleep(3)
                        double_check_code = double_check(phone)
                        time.sleep(1)
                        if double_check_code == 'resister successful!':
                            df['status'][i] = 'register successful'
                        else:
                            df['status'][i] = 'fill number failed'
                elif status_code2 == 'resister successful!':
                    df['status'][i] = 'register successful'
                else:
                    df['status'][i] = 'confirm failed'
            elif status_code1 == "login_proxy_error":
                print("login_proxy_error")
                df['status'][i] = 'login_proxy_error'
                time.sleep(1)
            elif status_code1 == 'login failed':
                print('login failed')
                df['status'][i] = 'login failed'
                time.sleep(1)
            elif status_code1 == "register failed":
                print("register failed")
                df['status'][i] = 'register failed'
                time.sleep(1)
            df.to_csv("profiles.csv",index=None)
        except :
            driver.quit()
            df['status'][i] = 'error'
            print('error')
            time.sleep(2)
            