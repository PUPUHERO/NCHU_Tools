from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions
from subprocess import CREATE_NO_WINDOW
from webdriver_manager.chrome import ChromeDriverManager

import os
import sys
import time
import configparser

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    #使函數結束後該變數(瀏覽器)不要被關閉
    options.add_experimental_option("detach", True)
    chrome_service = Service(ChromeDriverManager().install())
    chrome_service.creationflags = CREATE_NO_WINDOW
    #if selenium >= 4.6.0
    chrome_service.creation_flags = CREATE_NO_WINDOW
    browser = webdriver.Chrome(service=chrome_service, options=options)

    # 創建明確等待，最長等待時間為10秒
    wait = WebDriverWait(browser, 10)

    browser.get("http://aleph.lib.nchu.edu.tw/")
    loginButton = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/table[1]/tbody/tr/td/table/tbody/tr/td[11]/div/a")))
    loginButton.click()
    usernameLineEdit = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/table[6]/tbody/tr/td[3]/form/table[1]/tbody/tr[1]/td/input[1]")))
    passwordLineEdit = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/table[6]/tbody/tr/td[3]/form/table[1]/tbody/tr[1]/td/input[2]")))

    """____載入資料____"""
    config = configparser.ConfigParser()
    config.read("loginSettings.ini")
    account = config["loginInfo"]["account"]
    password = config["loginInfo"]["password"]

    usernameLineEdit.send_keys(account)
    passwordLineEdit.send_keys(password)
    loginButton = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/table[6]/tbody/tr/td[3]/form/table[1]/tbody/tr[2]/td/input")))
    loginButton.click()

    myBookButton = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/table[5]/tbody/tr[1]/td[15]/a")))
    myBookButton.click()

    currentBorrowing = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/table[6]/tbody/tr/td[2]/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr[5]/td[4]/a")))
    currentBorrowing.click()
    
if __name__ == "__main__":
    # 取得當前檔案的絕對路徑
    current_path = os.path.abspath(__file__)
    # 取得當前檔案的目錄路徑
    current_directory = os.path.dirname(current_path)
    # 將工作目錄設定為父目錄(main.py所在的目錄)
    current_directory = os.path.dirname(current_directory)
    # 更改工作目錄為當前檔案的目錄
    os.chdir(current_directory)
    main()
    
