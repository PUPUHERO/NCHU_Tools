from GUI.mainGUI import MainWindow
from auth.init import check_loginSettings
from PyQt5.QtWidgets import QApplication
import sys
import os
import argparse

from ilearning.SeleLogin import loginAndFillCapt as ilearning_main
from NCHUPortal.login import main as NCHUPortal_main
from Library.login import main as Library_main

if __name__ == '__main__':
    # 定義命令列參數
    parser = argparse.ArgumentParser(description='0 for ilearning, 1 for NCHUPortal, 2 for NCHU library')
    parser.add_argument('--service', type=str, help='0 for ilearning, 1 for NCHUPortal, 2 for NCHU library')
    
    # 解析參數
    args = parser.parse_args()
    
    # 使用解析後的參數
    if args.service is None:
        # 無參數時進入GUI介面
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
    elif args.service == '0':
        ilearning_main()
    elif args.service == '1':
        NCHUPortal_main()
    elif args.service == '2':
        Library_main()
    else:
        print('Invalid argument')
        sys.exit(1)   
    
