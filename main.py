'''
TODO:
生成图片列表中间保存问题
打开模型的速度尝试优化
参数调整完善
*打开日漫模型生成再进入黄种人的参数调整会崩溃(xxx层不存在)
一个一个保存太麻烦
'''
import sys
import personWindow
import backgroundWindow

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QTextEdit, QToolTip,
                             QPushButton, QFileDialog, QAction, QApplication, QDesktopWidget, QMessageBox)
from PyQt5.QtGui import QIcon, QColor, QPixmap, QFont
from PyQt5.Qt import QLineEdit


class mainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 窗口大小、居中显示、标题
        col = QColor(0, 0, 0)
        self.resize(1200, 800)
        self.center()
        self.setWindowTitle('MyWindow')
        # 禁止拉伸窗口大小
        self.setFixedSize(self.width(), self.height())

        # logo
        title = QLabel(self)
        title.resize(1200, 800)
        title.move(0, 0)
        title.setPixmap(QPixmap("src/bg.png"))

        # 帮助
        help_btn = QLabel("help?", self)
        help_btn.resize(80, 40)
        help_btn.move(1090, 30)
        help_btn.setStyleSheet('color:rgb(255, 255, 255);border-width: 0px;border-style: solid;'
                               'background-color: transparent;')
        help_btn.setCursor(Qt.PointingHandCursor)

        # 选择操作
            # 人像
        self.person = QPushButton(self)
        self.person.resize(230, 300)
        self.person.move(135, 368)
        self.person.setStyleSheet('border-radius:25px;background-color: rgb(236, 175, 193);')
        self.person.setCursor(Qt.PointingHandCursor)
        self.person.clicked.connect(self.toPerson)
        personLabel = QLabel(self)
        personLabel.setGeometry(170, 448, 70, 70)
        personLabel.setPixmap(QPixmap('src/person.png'))
        personLabel.setScaledContents(True)
        self.personText = QPushButton('人像生成', self)
        self.personText.setGeometry(165, 525, 120, 70)
        self.personText.setFont(QFont("黑体"))
        self.personText.setStyleSheet('color:rgb(255, 255, 255);font-size: 27px;background-color: transparent;')
        self.personText.setCursor(Qt.PointingHandCursor)
        self.personText.clicked.connect(self.toPerson)
            # 背景
        self.bkground = QPushButton(self)
        self.bkground.resize(230, 300)
        self.bkground.move(485, 368)
        self.bkground.setStyleSheet('border-radius:25px;background-color: rgb(176, 210, 234);')
        self.bkground.setCursor(Qt.PointingHandCursor)
        self.bkground.clicked.connect(self.toBkg)
        bkLabel = QLabel(self)
        bkLabel.setGeometry(520, 448, 70, 70)
        bkLabel.setPixmap(QPixmap('src/background.png'))
        bkLabel.setScaledContents(True)
        self.bkText = QPushButton('背景生成', self)
        self.bkText.setGeometry(515, 525, 120, 70)
        self.bkText.setFont(QFont("黑体"))
        self.bkText.setStyleSheet('color:rgb(255, 255, 255);font-size: 27px;background-color: transparent;')
        self.bkText.setCursor(Qt.PointingHandCursor)
        self.bkText.clicked.connect(self.toBkg)
            # 简笔画
        self.sim_picture = QPushButton(self)
        self.sim_picture.resize(230, 300)
        self.sim_picture.move(835, 368)
        self.sim_picture.setStyleSheet('border-radius:25px;background-color: rgb(190, 191, 229);')
        self.sim_picture.setCursor(Qt.PointingHandCursor)
        self.sim_picture.clicked.connect(self.toSim)
        simLabel = QLabel(self)
        simLabel.setGeometry(870, 448, 70, 70)
        simLabel.setPixmap(QPixmap('src/sim.png'))
        simLabel.setScaledContents(True)
        self.simText = QPushButton('简笔画填充', self)
        self.simText.setGeometry(865, 525, 150, 70)
        self.simText.setFont(QFont("黑体"))
        self.simText.setStyleSheet('color:rgb(255, 255, 255);font-size: 27px;background-color: transparent;')
        self.simText.setCursor(Qt.PointingHandCursor)
        self.simText.clicked.connect(self.toSim)

        self.show()

    def toPerson(self):
        self.newWindow = personWindow.personWindow()
        self.newWindow.show()
        self.close()

    def toBkg(self):
        self.newWindow = backgroundWindow.backgroundWindow()
        self.newWindow.show()
        self.close()

    def toSim(self):
        i = 0

    def center(self):
        temp_frame = self.frameGeometry()
        temp_CenterPoint = QDesktopWidget().availableGeometry().center()
        temp_frame.moveCenter(temp_CenterPoint)
        self.move(temp_frame.topLeft())


if __name__ == '__main__':
        # 创建应用程序和对象
        app = QApplication(sys.argv)
        ex = mainWindow()
        sys.exit(app.exec_())