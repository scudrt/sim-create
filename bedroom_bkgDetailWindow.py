import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, QToolTip, QPushButton, QFileDialog, QAction, QApplication, QDesktopWidget, QMessageBox, QCheckBox
from PyQt5.Qt import QLineEdit
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QHBoxLayout, QSpinBox, QSlider, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QImage
from PyQt5.QtCore import Qt
import backgroundWindow
import os
import re
import generate_background


class QSlider(QSlider):
    def wheelEvent(self, *args, **kwargs): # real signature unknown
        pass

class bkgDetailWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 参数值
        self.value = 0

        self.initUI()

    def initUI(self):
        # 窗口大小、居中显示、标题
        self.resize(1200, 800)
        self.center()
        self.setWindowTitle('黄种人脸-参数细化')
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 禁止拉伸窗口大小
        self.setFixedSize(self.width(), self.height())

        # logo
        title = QLabel(self)
        title.resize(1200, 800)
        title.move(0, 0)
        title.setPixmap(QPixmap("src/background-detail-bg.png"))

        # 输入窗口

        self.inpic = QLabel(self)
        self.inpic.resize(256, 256)
        self.inpic.move(300, 200)
        self.path = "chosen_picture"
        self.pic = os.listdir(self.path)
        str = "chosen_picture/" + self.pic[0]
        self.inpic.setPixmap(QPixmap(str))


        self.inpic.setScaledContents(True)
        # 输出窗口
        self.outpic = QLabel(self)
        self.outpic.resize(256, 256)
        self.outpic.move(644, 200)
        self.outpic.setPixmap(QPixmap("src/background-pic-bg.png"))
        self.outpic.setScaledContents(True)
        # 保存图片
        save = QPushButton('↓', self)
        save.setGeometry(860, 416, 40, 40)
        save.setStyleSheet('color:rgb(237, 237, 237);border-radius: 20px;'
                           'border-color: rgb(0, 0, 0);background-color: rgb(176, 210, 234);font-size: 25px;')
        save.setCursor(Qt.PointingHandCursor)
        save.clicked.connect(self.savePic)

        # 参数名
        # 细节 原/白
        self.name = QLabel('丰富细节', self)
        self.name.setGeometry(340, 520, 70, 20)
        self.name.setFont(QFont("黑体"))
        self.name.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 0px;background-color: transparent;font-size: 15px;')
      # 参数值
        # 细节
        self.Val = QLabel('0', self)
        self.Val.setGeometry(420, 520, 20, 20)
        self.Val.setFont(QFont("黑体"))
        self.Val.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 0px;background-color: transparent;font-size: 15px;')

        # 参数滑动条
        # 细节
        self.splider = QSlider(Qt.Horizontal, self)
        self.splider.setGeometry(415, 550, 450, 20)
        self.splider.setFocusPolicy(Qt.NoFocus)
        self.splider.valueChanged[int].connect(self.changedVal)
        #实时改变
        self.splider.sliderReleased.connect(self.released1)
        self.splider.setMinimum(0)  # 参数最小值
        self.splider.setMaximum(100)  # 参数最大值
        self.splider.setSingleStep(10)  # 步长
        self.splider.setStyleSheet('color:rgb(236, 175, 193);background-color: transparent;')
        left = QLabel('0', self)
        left.setGeometry(380, 550, 20, 20)
        left.setAlignment(Qt.AlignCenter)
        left.setFont(QFont("黑体"))
        left.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 1px;border-style: solid;border-color: rgb(236, 175, 193);'
            'border-radius: 10px;background-color: transparent;font-size: 15px;')
        right = QLabel('100', self)
        right.setGeometry(880, 550, 20, 20)
        right.setAlignment(Qt.AlignCenter)
        right.setFont(QFont("黑体"))
        right.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 1px;border-style: solid;border-color: rgb(236, 175, 193);'
            'border-radius: 10px;background-color: transparent;font-size: 10px;')
        # 返回首页
        back = QPushButton(self)
        back.setGeometry(1059, 627, 141, 173)
        back.clicked.connect(self.Back)  # 保存结果图
        back.setStyleSheet("QPushButton{border-image: url(src/rocket.png)}"
                            "QPushButton:hover{border-image: url(src/rocket-start.png)}")
        back.setCursor(Qt.PointingHandCursor)

        self.show()

    def released1(self):
        #参数细化生成代码
        self.path = "chosen_picture"
        self.pic = os.listdir(self.path)
        pic_name = self.pic[0]
        pic_num = os.path.splitext(pic_name)[0]
        slider = self.splider.value()
        #print(slider)
        im = generate_background.generate_bg(1, backgroundWindow.bedroom_Gs, pic_num, slider)
        qimage = QImage(im.tobytes('raw', 'RGB'), im.size[0], im.size[1], QImage.Format_RGB888)
        # 将result.png显示在outpic
        self.outpic.setPixmap(QPixmap(qimage))
        self.outpic.setScaledContents(True)



    def changedVal(self, value):
        self.value = value
        self.Val.setNum(self.value)


    def savePic(self):
        # 保存到 保存图片/result.png
        self.image = QtGui.QPixmap("result_picture\\result.png").scaled(256, 256)
        self.image.save("保存图片\\result.png")
        self.outpic.setPixmap(QPixmap('result_picture/result.png'))

    def Back(self):
        # 根据参数生成结果，保存为result_picture/result.png
        # 此处为生成代码
        self.path = "chosen_picture"
        self.pic = os.listdir(self.path)
        str = "chosen_picture/" + self.pic[0]
        # 删除
        for maindir, subdir, file_name_list in os.walk(self.path):
            for filename in file_name_list:
                if (filename.endswith(".png")):
                    os.remove(maindir + "\\" + filename)

        self.newWindow = backgroundWindow.backgroundWindow()
        self.newWindow.show()
        self.close()


    # 窗口在屏幕中心显示
    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())
