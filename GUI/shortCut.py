import os
import winshell
from win32com.client import Dispatch

def create_python_shortcut_onDesktop(script_path, arguments=""):
    shell = Dispatch("WScript.Shell")
    # 獲得桌面路徑
    desktop_path = winshell.desktop()
    # 創建捷徑的完整路徑 = 桌面路徑 + 檔案目錄名稱 + ".lnk"
    shortcut_path = desktop_path + "\\" + script_path.rsplit("\\", 1)[-2].split("\\")[-1] + ".lnk"
    
    # 處理要執行的 python 檔案的路徑
    script_path = os.path.abspath(script_path) # 呼叫前兩層目錄的路徑和python檔案的路徑組合
    
    # 創建捷徑
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = "python" # 指定捷徑的目標為 python
    shortcut.WindowStyle = 7 # 指定捷徑的視窗風格為headless
    shortcut.Arguments = f'"{script_path}" {arguments}' # 指定捷徑的參數
    shortcut.WorkingDirectory = script_path.rsplit("\\", 1)[0] # 指定捷徑的工作目錄
    shortcut.save()