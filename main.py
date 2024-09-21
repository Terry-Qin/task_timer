import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton, QDesktopWidget
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
import ctypes

class LockScreenApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateCountdown)
        self.remaining_time = 0
        self.resetState()

    def initUI(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #FFE5E5;
                font-family: 'Comic Sans MS', cursive;
                font-size: 16px;
            }
            QPushButton {
                background-color: #FF9999;
                color: #FFFFFF;
                padding: 10px;
                border: 2px solid #FF7777;
                border-radius: 15px;
                font-size: 18px;
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
            }
            QSpinBox {
                padding: 5px;
                border: 2px solid #FF9999;
                border-radius: 10px;
                background-color: #FFFFFF;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(20)

        title_label = QLabel("可爱的锁屏小助手")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Comic Sans MS", 24, QFont.Bold))
        layout.addWidget(title_label)

        # 创建输入区域
        input_layout = QHBoxLayout()
        self.minute_input = QSpinBox()
        self.minute_input.setRange(0, 1440)  # 0分钟到24小时
        self.minute_input.setFixedHeight(40)
        self.minute_input.setFixedWidth(100)
        self.minute_input.setValue(1)  # 默认1分钟
        
        self.second_input = QSpinBox()
        self.second_input.setRange(0, 59)  # 0到59秒
        self.second_input.setFixedHeight(40)
        self.second_input.setFixedWidth(100)
        self.second_input.setValue(0)  # 默认0秒

        input_layout.addWidget(QLabel("锁屏时间："))
        input_layout.addWidget(self.minute_input)
        input_layout.addWidget(QLabel("分"))
        input_layout.addWidget(self.second_input)
        input_layout.addWidget(QLabel("秒"))
        input_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(input_layout)

        # 创建开始按钮
        self.start_button = QPushButton("开始倒计时")
        self.start_button.clicked.connect(self.startCountdown)
        self.start_button.setFixedHeight(50)
        layout.addWidget(self.start_button)

        # 创建倒计时显示标签
        self.countdown_label = QLabel()
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setFont(QFont("Comic Sans MS", 36, QFont.Bold))
        layout.addWidget(self.countdown_label)

        self.setLayout(layout)
        self.setWindowTitle('可爱的锁屏小助手')
        self.setWindowIcon(QIcon('lock_icon.png'))  # 请确保你有一个可爱的锁屏图标
        self.resize(400, 300)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def resetState(self):
        self.remaining_time = 0
        self.start_button.setEnabled(True)
        self.start_button.setText("开始倒计时")
        self.countdown_label.setText("00:00:00")
        if hasattr(self, 'floating_countdown'):
            self.floating_countdown.close()

    def startCountdown(self):
        minutes = self.minute_input.value()
        seconds = self.second_input.value()
        self.remaining_time = minutes * 60 + seconds
        self.timer.start(1000)  # 每秒更新一次
        self.start_button.setEnabled(False)
        self.start_button.setText("倒计时进行中...")

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
            font-size: 48px;
            color: #FF5555;
            background-color: rgba(255, 229, 229, 200);
            border: 3px solid #FF9999;
            border-radius: 20px;
            padding: 10px;
        """)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.setGeometry(0, 0, 300, 100)
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
    sys.exit(app.exec_())