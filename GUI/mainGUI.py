import os
import sys
import configparser
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QToolBar, QAction
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QLineEdit, QDialog

try:
    from GUI.shortcutTools import shortcutAction
except ModuleNotFoundError:
    from shortcutTools import shortcutAction
    
def getPath(filename):
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
    path = os.path.join(bundle_dir, filename)
    return path

class MainWidget(QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = configparser.ConfigParser()
        self.make_loginSettings()
        self.hint_label = QLabel()
        self.programs = kwargs["parent"].programs
        self.initUI()
          
    def make_loginSettings(self):
        try:
            self.config.read("loginSettings.ini")
            self.config['loginInfo']['account']
            self.config['loginInfo']['password']
        except KeyError:
            self.config['loginInfo'] = {'account': '', 'password': ''}
            with open("loginSettings.ini", 'w') as configFile:
                self.config.write(configFile)
        
    def hint_label_update(self):
        self.config.read("loginSettings.ini")
        self.hint_label.setAlignment(Qt.AlignCenter)
        self.hint_label.setText('初次使用請先點選左上角設定帳號密碼\n目前帳號為:{}'.format(self.config['loginInfo']['account']))
        

    def initUI(self):
        # 創建垂直布局
        vertical_main_layout = QVBoxLayout()

        # 創建水平布局
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setSpacing(50)
        
        # 建立提示文字
        self.hint_label_update()
        # 將垂直布局和水平布局添加到主布局中
        vertical_main_layout.addWidget(self.hint_label)

        # 創建圖片和按鈕的函式
        def create_image_and_button(_, image_path, process_path, button_text):
            # 創建圖片
            label = QLabel()
            pixmap = QPixmap(image_path).scaled(300, 300, aspectRatioMode=Qt.KeepAspectRatio)
            label.setPixmap(pixmap)
            label.mousePressEvent = lambda event: self.execute_process(process_path)
            vertical_layout = QVBoxLayout()
            vertical_layout.setAlignment(Qt.AlignCenter)
            vertical_layout.addWidget(label)
            # 創建按鈕
            button = QPushButton(button_text)
            button.setMinimumHeight(50)
            vertical_layout.addWidget(button)
            button.clicked.connect(lambda: self.execute_process(process_path))
            return vertical_layout
        
        # 創建圖片和按鈕並添加到水平布局中
        for program in self.programs:
            vertical_layout = create_image_and_button(program[0], getPath(program[1]), getPath(program[2]), program[3])
            horizontal_layout.addLayout(vertical_layout)
            
        # 將水平布局添加到主垂直布局中
        vertical_main_layout.addLayout(horizontal_layout)

        # 設置布局為窗口的主佈局
        self.setLayout(vertical_main_layout)
        
    def execute_process(self, program_path):
        # 創建 QProcess
        process = QProcess()
        
        # 使用 QProcess 啟動外部進程
        process.start('python', [program_path])
        
        # 等待進程結束後再銷毀 QProcess 物件
        process.waitForFinished()
        process.deleteLater()
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 設定檔案標題及相對路徑
        self.programs = [
            ("興大入口", "GUI\\icons\\nchu.jpg", 'NCHUPortal\\login.py', '快速登入'),
            ("iLearning", "GUI\\icons\\ilearning.png", 'ilearning\\SeleLogin.py', '快速登入'),
            ("圖書館", "GUI\\icons\\library.jpg", 'library\\login.py', '自動續借')
        ]
        # 設置窗口的標題和大小
        self.setWindowTitle('興大實用系統')
        self.setGeometry(300, 300, 1200, 300)
        
        self.widget = MainWidget(parent = self)
        self.setCentralWidget(self.widget)
        
        window = self
        
        # 創建 QMenuBar
        menubar = QMenuBar()

        # 添加選單到選單欄
        setting_menu = menubar.addMenu('設定')

        # 添加動作到選單
        open_action = QAction('帳號密碼', window)
        open_action.triggered.connect(self.openPasswordWindow)
        setting_menu.addAction(open_action)

        # 添加捷徑選單到選單欄
        shortcut_menu = menubar.addMenu('捷徑')
        
        # 添加捷徑動作到選單
        for program in self.programs:
            shortcut_menu.addAction(shortcutAction(program_path=program[2], text="在桌面建立{}捷徑".format(program[0]), parent=window))        
        
        # 設置選單欄為 QMainWindow 的選單欄
        window.setMenuBar(menubar)
    
    def openPasswordWindow(self):
        password_window = PasswordWindow(self)
        password_window.exec_()
        self.widget.hint_label_update()

class PasswordWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent = parent)
        
        # 關閉對話框的「?」按鈕
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        # 也可以使用下面這行程式碼
        # self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        # 設定對話框的標題和大小
        self.setWindowTitle('設定帳號密碼')
        self.resize(300, 300)
        
        if parent is not None:
            # 計算在 QMainWindow 上的相對位置
            parent_pos = self.parent().pos()
            relative_x = parent_pos.x() + 50
            relative_y = parent_pos.y() + 50

            # 設定對話框的位置
            self.move(relative_x, relative_y)
        
        self.student_id_line_edit = QLineEdit()
        self.student_id_line_edit.setPlaceholderText("學號")
        self.password_line_edit = QLineEdit()
        self.password_line_edit.setEchoMode(QLineEdit.Password)
        self.password_line_edit.setPlaceholderText("密碼")
        
        ok_button = QPushButton("確定")
        ok_button.clicked.connect(self.ok)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.cancel)
        
        layout = QVBoxLayout()
        layout.addWidget(self.student_id_line_edit)
        layout.addWidget(self.password_line_edit)
        layout.addWidget(ok_button)
        layout.addWidget(cancel_button)
        
        self.setLayout(layout)
        
    def ok(self):
        config = configparser.ConfigParser()
        config.read("loginSettings.ini")
        config.set("loginInfo", "account", self.student_id_line_edit.text() or "None")
        config.set("loginInfo", "password", self.password_line_edit.text())
        config.write(open("loginSettings.ini", "w"))        
        self.close()
        
    def cancel(self):
        self.close()
                

if __name__ == '__main__':
    # 取得當前檔案的絕對路徑
    current_path = os.path.abspath(__file__)
    # 取得當前檔案的目錄路徑
    current_directory = os.path.dirname(current_path)
    # 將工作目錄設定為父目錄(main.py所在的目錄)
    current_directory = os.path.dirname(current_directory)
    # 更改工作目錄為當前檔案的目錄
    os.chdir(current_directory)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
