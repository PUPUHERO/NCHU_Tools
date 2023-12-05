"""
此檔案用於將快捷按鈕放入工具列及桌面
PUPUHERO 2023/11/29
"""

"""
step1: 建立捷徑
====待完成====
step2: 將捷徑放入工具列
step3: 將捷徑放入桌面
"""

import os
import sys

# run pip install requirements.txt
import pip
pip.main(["install", "-r", "requirements.txt"])

import pythoncom
from win32com.client import Dispatch

file_tuple = (
    ("ilearning", "ilearning/SeleLogin.py", "shortcut/ilearningLogin.lnk"),
    ("NCHUPortal", "NCHUPortal/login.py", "shortcut/NUCHLogin.lnk")
)
current_path = os.path.dirname(__file__)

def check_shortcut_dir():
    if not os.path.exists("shortcut"):
        os.mkdir("shortcut")

def make_shortcut(target_path, shortcut_path):
    # 製造捷徑

    # 處理目標文件名稱和位置
    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(f"{os.path.join(current_path, shortcut_path)}")

    # 指定捷徑屬性
    shortcut.Targetpath = f"{sys.executable.split('python.exe')[0]}pythonw.exe"
    shortcut.Arguments = f"{os.path.join(current_path, target_path)}"
    shortcut.WorkingDirectory = current_path
    shortcut.WindowStyle = 7
    shortcut.save() 
    
if __name__ == "__main__":    
    import init
    check_shortcut_dir()
    make_shortcut(file_tuple[0][1], file_tuple[0][2])
    make_shortcut(file_tuple[1][1], file_tuple[1][2])



