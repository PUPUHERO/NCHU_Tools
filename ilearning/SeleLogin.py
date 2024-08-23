import base64
import os
import configparser

try:
    from number_recognizer import NumberRecognizer
except ModuleNotFoundError:
    from .number_recognizer import NumberRecognizer

from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions

def loginAndFillCapt():
    #使函數結束後該變數(瀏覽器)不要被關閉
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_experimental_option("detach", True)
        #if selenium >= 4.6.0
        browser = webdriver.Chrome(options=options)

        browser.get("https://lms2020.nchu.edu.tw/")

        username = browser.find_element(by=By.NAME, value="account")
        password = browser.find_element(by=By.NAME, value="password")

        if(os.path.exists("loginSettings.ini")):
            config = configparser.ConfigParser()
            config.read("loginSettings.ini")
            ReadUser = config["loginInfo"]["account"]
            ReadPassword = config["loginInfo"]["password"]
        else:
            print("Need loginSettings.ini")
        
        username.send_keys(ReadUser)#輸入帳號
        password.send_keys(ReadPassword)#輸入密碼
        
        CAPT = getCAPT(browser)
        
        NR = NumberRecognizer()
        NR.setTarget(CAPT)
        numbers = NR.getNumbers()
        
        #填入驗證碼
        captcha = browser.find_element(by=By.NAME, value="captcha")   
        captcha.send_keys(numbers)
        #按下登入按鍵
        loginBut = browser.find_elements(by=By.CLASS_NAME, value='btn-text')[0]
        loginBut.click()
        
    except selenium.common.exceptions.NoSuchWindowException:
        pass
    except IndexError:
        pass
    except:
        raise
    
def getCAPT(browser):
    captchaBase64 = browser.execute_async_script("""
        var canvas = document.createElement('canvas');
        var context = canvas.getContext('2d');
        var img = document.querySelector('img.js-captcha');
        canvas.height = 28;
        canvas.width = 100;
        context.drawImage(img, 0, 0);
        
        callback = arguments[arguments.length - 1];
        callback(canvas.toDataURL());
        """)
    # 先將 data Url 前綴 (data:image/png;base64) 去除，再將 base64 資料轉為 bytes
    i = base64.b64decode(captchaBase64.split(',')[1])
    # 因為讀取的是檔案，但我們不想存檔案於本地端，
    # 所以在記憶體中創建一個內容為 i 的 bytes 檔案
    return i

"""Main"""
if __name__ == "__main__" :
    # 取得當前檔案的絕對路徑
    current_path = os.path.abspath(__file__)
    # 取得當前檔案的目錄路徑
    current_directory = os.path.dirname(current_path)
    # 將工作目錄設定為父目錄(main.py所在的目錄)
    current_directory = os.path.dirname(current_directory)
    # 更改工作目錄為當前檔案的目錄
    os.chdir(current_directory)
    
    loginAndFillCapt()