from GUI.mainGUI import MainWindow
from PyQt5.QtWidgets import QApplication
import sys
import os
if __name__ == '__main__':
    # 取得當前檔案的絕對路徑
    current_path = os.path.abspath(__file__)
    # 取得當前檔案的目錄路徑
    current_directory = os.path.dirname(current_path)
    # 更改工作目錄為當前檔案的目錄
    os.chdir(current_directory)
    
    # if no loginSettings.ini, create a new one
    if os.path.exists("loginSettings.ini") == False:
        with open("loginSettings.ini", "w") as f:
            f.write("[loginInfo]\n")
            f.write("account=411006xxxx\n")
            f.write("password=xxxxxxxx\n")    

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
