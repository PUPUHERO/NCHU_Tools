"""自動登入NCHU portal"""
import json
import os
import configparser
from subprocess import CREATE_NO_WINDOW

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

"""載入套件"""
def main():
    # 自動安裝webdriver
    chrome_service = Service(ChromeDriverManager().install())
    # 避免建立cmd小黑框
    chrome_service.creation_flags = CREATE_NO_WINDOW

    URL = "https://idp.nchu.edu.tw"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"

    # 設定webdriver選項
    options = webdriver.ChromeOptions()
    options.add_argument('--user-agent=%s' % user_agent)
    options.add_argument("--start-maximized")

    # 維持瀏覽器開啟
    options.add_experimental_option("detach", True)

    # 建立webdriver
    browser = webdriver.Chrome(service=chrome_service, options=options)
    browser.implicitly_wait(10)
    browser.get(url=URL)

    """載入資料"""
    config = configparser.ConfigParser()
    config.read("loginSettings.ini")
    account = config["loginInfo"]["account"]
    password = config["loginInfo"]["password"]

    """輸入網頁"""
    account_input = browser.find_element(By.XPATH, "/html/body/div/div[2]/div/div[2]/div[1]/div/div/form/div/div[2]/div/input")
    password_input = browser.find_element(By.XPATH, "/html/body/div/div[2]/div/div[2]/div[1]/div/div/form/div/div[4]/div/input")
    CAPTCHA_input = browser.find_element(By.XPATH, "/html/body/div/div[2]/div/div[2]/div[1]/div/div/form/div/div[7]/div/input")

    account_input.send_keys(account)
    password_input.send_keys(password)

    def get_code(browser):
        CAPTCHA_code = browser.execute_script("""
            return code;
            """)
        code = CAPTCHA_code
        return code

    CAPTCHA_input.send_keys(get_code(browser))

    login_button = browser.find_element(By.XPATH, "/html/body/div/div[2]/div/div[2]/div[1]/div/div/form/div/div[8]/div[1]/button")
    login_button.click()
    
if __name__ == '__main__':
    # 取得當前檔案的絕對路徑
    current_path = os.path.abspath(__file__)
    # 取得當前檔案的目錄路徑
    current_directory = os.path.dirname(current_path)
    # 將工作目錄設定為父目錄(main.py所在的目錄)
    current_directory = os.path.dirname(current_directory)
    # 更改工作目錄為當前檔案的目錄
    os.chdir(current_directory)
    main()
