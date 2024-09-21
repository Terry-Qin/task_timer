import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton, QDesktopWidget
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QFont, QPalette, QColor
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
                background-color: #f0f0f0;
                font-size: 16px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QLabel {
                color: #333333;
            }
            QSpinBox {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(20)

        title_label = QLabel("Windows自动锁屏")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(title_label)

        # 创建输入区域
        input_layout = QHBoxLayout()
        self.time_input = QSpinBox()
        self.time_input.setRange(1, 1440)  # 1��钟到24小时
        self.time_input.setFixedHeight(40)
        self.time_input.setFixedWidth(100)
        input_layout.addWidget(QLabel("锁屏时间（分钟）:"))
        input_layout.addWidget(self.time_input)
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
        self.countdown_label.setFont(QFont("Arial", 36, QFont.Bold))
        layout.addWidget(self.countdown_label)

        self.setLayout(layout)
        self.setWindowTitle('Windows自动锁屏')
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
        self.countdown_label.setText("00:00")
        if hasattr(self, 'floating_countdown'):
            self.floating_countdown.close()

    def startCountdown(self):
        minutes = self.time_input.value()
        self.remaining_time = minutes * 60
        self.timer.start(1000)  # 每秒更新一次
        self.start_button.setEnabled(False)
        self.start_button.setText("倒计时进行中...")

    def updateCountdown(self):
        self.remaining_time -= 1
        minutes, seconds = divmod(self.remaining_time, 60)
        self.countdown_label.setText(f"{minutes:02d}:{seconds:02d}")

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
            font-size: 48px;
            color: red;
            background-color: rgba(0, 0, 0, 150);
            border-radius: 10px;
            padding: 10px;
        """)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.setGeometry(0, 0, 200, 100)
        self.move(QDesktopWidget().availableGeometry().topRight() - QPoint(220, -20))

    def setTime(self, time):
        self.label.setText(f"锁屏倒计时: {time}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LockScreenApp()
    sys.exit(app.exec_())