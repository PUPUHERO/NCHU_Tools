from GUI.mainGUI import MainWindow
from auth.init import check_loginSettings
from PyQt5.QtWidgets import QApplication
import sys
import os
if __name__ == '__main__':
    check_loginSettings()
    # 取得當前檔案的絕對路徑
    current_path = os.path.abspath(__file__)
    # 取得當前檔案的目錄路徑
    current_directory = os.path.dirname(current_path)
    # 更改工作目錄為當前檔案的目錄
    os.chdir(current_directory)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
