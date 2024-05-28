from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QPushButton, QWidget, QLabel
import lib as stelle
import sys, os, ctypes, shutil


__author__ = "Narr <Narr@cinamon.io>"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class MyApp(QMainWindow):
    def __init__(self):
            if is_admin():
                super().__init__()
                self.initUI()
        # 관리자 권한으로 실행 중일 때 수행할 작업
                pass
            else:
            # 현재 프로그램 인스턴스를 관리자 권한으로 다시 실행
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


    def initUI(self):
        self.setWindowTitle('Melange on Windows')
        self.move(300, 300)
        self.resize(400, 960)
        
        self.engine_root :str = stelle.get_engine_root('5.3')
        label_001 = QLabel('Engine Root : ' + self.engine_root, self)
        btn_001 = QPushButton("Open Engine Folder", self)
        ###
        
        btn_002 = QPushButton("Sync UECustomShader", self)
        btn_003 = QPushButton("버튼3", self)
        btn_004 = QPushButton("버튼4", self)

        # Connect the clicked signal of the buttons to the on_click slot
        btn_001.clicked.connect(lambda: stelle.openFolder(self.engine_root))
        
        btn_002.clicked.connect(self.sync_UECustomShader_repo)
        
        
        btn_003.clicked.connect(self.on_click)
        btn_004.clicked.connect(self.on_click)

        # Create a layout
        layout = QHBoxLayout()
        # Add the buttons to the layout
        layout.addWidget(label_001)
        layout.addWidget(btn_001)
        layout.addWidget(btn_002)
        layout.addWidget(btn_003)
        layout.addWidget(btn_004)

        # Create a QWidget and set it as the central widget of the QMainWindow
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.show()

    def on_click(self):
        print('Button clicked!')
        
    def sync_UECustomShader_repo(self):
        shutil.rmtree(self.engine_root + 'Shaders')
        stelle.execute_console_command('git clone https://gitlab.cinamon.me/cinev/customshader.git Shaders', '')
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())