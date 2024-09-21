import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton, QDesktopWidget, QMainWindow
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
import ctypes

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 0, 0)
        
        layout.addStretch()
        
        button_style = """
            QPushButton {
                background-color: #FF9999;
                color: #FFFFFF;
                border: none;
                font-size: 18px;
                padding: 5px;
                width: 30px;
                height: 30px;
            }
            QPushButton:hover {
                background-color: #FF7777;
            }
        """
        
        # 添加最小化按钮
        minimize_button = QPushButton("—")
        minimize_button.setStyleSheet(button_style)
        minimize_button.clicked.connect(self.parent.showMinimized)
        layout.addWidget(minimize_button)
        
        # 保留原有的关闭按钮
        close_button = QPushButton("×")
        close_button.setStyleSheet(button_style.replace("#FF7777", "#FF5555"))
        close_button.clicked.connect(self.parent.close)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
        self.setFixedHeight(30)
        self.setStyleSheet("background-color: #FFE5E5; border-top-left-radius: 10px; border-top-right-radius: 10px;")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.moving = True
            self.parent.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.parent.moving:
            self.parent.move(event.globalPos() - self.parent.offset)

    def mouseReleaseEvent(self, event):
        self.parent.moving = False

class LockScreenApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.moving = False
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        main_widget = QWidget()
        main_widget.setStyleSheet("""
            QWidget {
                background-color: #FFE5E5;
                font-family: 'Comic Sans MS', cursive;
                font-size: 18px;
                border-radius: 10px;
            }
            QPushButton {
                background-color: #FF9999;
                color: #FFFFFF;
                padding: 10px;
                border: 2px solid #FF7777;
                border-radius: 15px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF7777;
            }
            QPushButton:disabled {
                background-color: #FFCCCC;
                border: 2px solid #FFAAAA;
            }
            QLabel {
                color: #FF5555;
                font-weight: bold;
            }
            QSpinBox {
                padding: 5px;
                border: 2px solid #FF9999;
                border-radius: 10px;
                background-color: #FFFFFF;
                font-weight: bold;
                font-size: 18px;
            }
        """)

        layout = QVBoxLayout(main_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(10, 0, 10, 10)  # 调整上边距为0

        title_bar = CustomTitleBar(self)
        layout.addWidget(title_bar)

        # 创建一个新的标题容器
        title_container = QWidget()
        title_container.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FF9999, stop:1 #FFCCCC);
            border-radius: 20px;
            margin: 10px 0;
            padding: 10px;
        """)
        title_layout = QVBoxLayout(title_container)

        title_label = QLabel("可爱的锁屏小助手")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Comic Sans MS", 64, QFont.Bold))  # 调整字体大小
        title_label.setStyleSheet("""
            color: #FF3333;
            text-shadow: 3px 3px 6px #FFFFFF;
        """)
        title_layout.addWidget(title_label)

        subtitle_label = QLabel("让锁屏变得更有趣！")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setFont(QFont("Arial", 24, QFont.StyleItalic))  # 使用不同的字体和样式
        subtitle_label.setStyleSheet("color: #FF5555;")
        title_layout.addWidget(subtitle_label)

        layout.addWidget(title_container)

        # 创建输入区域
        input_layout = QHBoxLayout()
        self.minute_input = QSpinBox()
        self.minute_input.setRange(0, 1440)
        self.minute_input.setFixedHeight(45)
        self.minute_input.setFixedWidth(110)
        self.minute_input.setValue(1)
        
        self.second_input = QSpinBox()
        self.second_input.setRange(0, 59)
        self.second_input.setFixedHeight(45)
        self.second_input.setFixedWidth(110)
        self.second_input.setValue(0)

        input_layout.addWidget(QLabel("锁屏时间："))
        input_layout.addWidget(self.minute_input)
        input_layout.addWidget(QLabel("分"))
        input_layout.addWidget(self.second_input)
        input_layout.addWidget(QLabel("秒"))
        input_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(input_layout)

        # 创建按钮布局
        button_layout = QHBoxLayout()

        self.start_button = QPushButton("开始倒计时")
        self.start_button.clicked.connect(self.startCountdown)
        self.start_button.setFixedHeight(55)
        button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("停止计时")
        self.stop_button.clicked.connect(self.stopCountdown)
        self.stop_button.setFixedHeight(55)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)

        self.reset_button = QPushButton("重置")
        self.reset_button.clicked.connect(self.resetState)
        self.reset_button.setFixedHeight(55)
        button_layout.addWidget(self.reset_button)

        layout.addLayout(button_layout)

        self.countdown_label = QLabel()
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setFont(QFont("Comic Sans MS", 42, QFont.Bold))
        self.countdown_label.setStyleSheet("color: #FF3333; text-shadow: 2px 2px 4px #FFAAAA;")
        layout.addWidget(self.countdown_label)

        self.setCentralWidget(main_widget)
        self.setWindowTitle('可爱的锁屏助手')
        self.setWindowIcon(QIcon('lock_icon.png'))
        self.resize(500, 450)  # 调整窗口大小以适应更的标题
        self.center()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateCountdown)
        self.remaining_time = 0
        self.resetState()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def resetState(self):
        self.remaining_time = 0
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.start_button.setText("开始倒计时")
        self.countdown_label.setText("00:00:00")
        self.minute_input.setEnabled(True)
        self.second_input.setEnabled(True)
        if hasattr(self, 'floating_countdown'):
            self.floating_countdown.close()

    def startCountdown(self):
        minutes = self.minute_input.value()
        seconds = self.second_input.value()
        self.remaining_time = minutes * 60 + seconds
        self.timer.start(1000)  # 每秒更新一次
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.start_button.setText("倒计时进行中...")
        self.minute_input.setEnabled(False)
        self.second_input.setEnabled(False)

    def stopCountdown(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.start_button.setText("继续倒计时")
        if hasattr(self, 'floating_countdown'):
            self.floating_countdown.close()

    def updateCountdown(self):
        self.remaining_time -= 1
        hours, remainder = divmod(self.remaining_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.countdown_label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

        if self.remaining_time <= 0:
            self.timer.stop()
            if hasattr(self, 'floating_countdown'):
                self.floating_countdown.close()
            self.lockScreen()
            self.resetState()
        elif self.remaining_time <= 10:
            self.showFullScreenCountdown()
            self.floating_countdown.setTime(self.remaining_time)

    def showFullScreenCountdown(self):
        if not hasattr(self, 'floating_countdown'):
            self.floating_countdown = FloatingCountdown()
        self.floating_countdown.setTime(self.remaining_time)
        self.floating_countdown.show()

    def lockScreen(self):
        ctypes.windll.user32.LockWorkStation()

    def closeEvent(self, event):
        self.resetState()
        super().closeEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moving = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.moving:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.moving = False

class FloatingCountdown(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            font-family: 'Comic Sans MS', cursive;
            font-size: 54px;
            color: #FF5555;
            background-color: rgba(255, 229, 229, 200);
            border: 3px solid #FF9999;
            border-radius: 20px;
            padding: 15px;
        """)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.setGeometry(0, 0, 350, 120)
        self.moveToTopCenter()

    def moveToTopCenter(self):
        screen = QDesktopWidget().screenNumber(QDesktopWidget().cursor().pos())
        screen_geometry = QDesktopWidget().screenGeometry(screen)
        size = self.geometry()
        self.move(screen_geometry.left() + (screen_geometry.width() - size.width()) // 2,
                  screen_geometry.top() + 50)  # 50是距离顶部的距离，可以根据需要调整

    def setTime(self, time):
        self.label.setText(f"还剩 {time} 秒就要锁屏啦！")
        self.adjustSize()  # 根据文本内容调整窗口大小
        self.moveToTopCenter()  # 重新定位窗口

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LockScreenApp()
    ex.show()
    sys.exit(app.exec_())