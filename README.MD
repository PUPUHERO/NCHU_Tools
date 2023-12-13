# NCHU Tools 興大實用工具

## 介紹

這是一個為了方便興大學生使用而開發的工具，目前有以下功能：
- 自動填寫ilearning驗證碼
- 自動填寫興大入口網站驗證碼
- ~~圖書館自動登入~~(已棄用)

## 前置作業

### (前置)環境設定

必須先安裝python3，並且安裝以下套件：[requirements.txt](requirements.txt)

    pip3 install -r requirements.txt

### (前置)帳密設定

需先在當前project目錄下建立loginSettings.ini並設定帳密，格式如下：

    [loginInfo]
    account = 411006xxxx
    password = xxxxxxxxxx

## 使用方法

### 快捷操作

執行`setup_helper.py`，會安裝requirements.txt中所有套件並且在shortcut資料夾中建立捷徑，可將其釘選到工作列，方便使用。

### GUI介面

執行`main.py`，會出現GUI介面，可在上面選擇要執行的功能。

## 待研發功能

- [ ] 自動登入圖書館
- [ ] 自動釘選到工作列
- [ ] 將辨識方式改為CNN
