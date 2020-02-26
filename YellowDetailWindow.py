import sys
import os
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, QToolTip, QPushButton, QFileDialog, QAction, QApplication, QDesktopWidget, QMessageBox, QCheckBox
from PyQt5.Qt import QLineEdit
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QHBoxLayout, QSpinBox, QSlider, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt5.QtCore import Qt
import personWindow
import play_with_dlatent
import personWindow

class QSlider(QSlider):
    def wheelEvent(self, *args, **kwargs):  # real signature unknown
        pass

class YellowDetailWindow(QWidget):
    def __init__(self):
        print("enter")
        super().__init__()

        global Gs
        Gs = personWindow.yellow_Gs

        self.path = "chosen_picture"
        self.pic = os.listdir(self.path)
        pic_name = self.pic[0]
        global pic_num
        pic_num = os.path.splitext(pic_name)[0]
        # 删除chosen_picture
        # os.remove(self.path)

        # 参数值
        self.value1 = 0
        self.value2 = 0
        self.value3 = 0
        self.value4 = 0
        self.value5 = 0
        self.value6 = 0

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
        title.setPixmap(QPixmap("src/detail-bg.png"))

        # 输入窗口

        self.inpic = QLabel(self)
        self.inpic.resize(256, 256)
        self.inpic.move(300, 200)


        self.path = "chosen_picture"
        self.pic = os.listdir(self.path)
        str = "chosen_picture/" + self.pic[0]
        self.inpic.setPixmap(QPixmap(str))
        #删除
        for maindir, subdir, file_name_list in os.walk(self.path):
            for filename in file_name_list:
                if (filename.endswith(".png")):
                    os.remove(maindir + "\\" + filename)



        self.inpic.setScaledContents(True)
        # 输出窗口
        self.outpic = QLabel(self)
        self.outpic.resize(256, 256)
        self.outpic.move(644, 200)
        self.outpic.setPixmap(QPixmap("src/detail-pic-bg.png"))
        self.outpic.setScaledContents(True)
        # 保存图片
        save = QPushButton('↓', self)
        save.setGeometry(860, 416, 40, 40)
        save.setStyleSheet('color:rgb(237, 237, 237);border-radius: 20px;'
                           'border-color: rgb(0, 0, 0);background-color: rgb(236, 175, 193);font-size: 25px;')
        save.setCursor(Qt.PointingHandCursor)
        save.clicked.connect(self.savePic)

        # 参数名
        # 颜值 高/低
        self.name1 = QLabel('颜值', self)
        self.name1.setGeometry(270, 480, 40, 20)
        self.name1.setFont(QFont("黑体"))
        self.name1.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 0px;background-color: transparent;font-size: 15px;')
        # 水平调整角度 左/右
        self.name2 = QLabel('水平调整角度', self)
        self.name2.setGeometry(270, 560, 100, 20)
        self.name2.setFont(QFont("黑体"))
        self.name2.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 0px;background-color: transparent;font-size: 15px;')
        # 性别 女/男
        self.name3 = QLabel('性别', self)
        self.name3.setGeometry(270, 640, 40, 20)
        self.name3.setFont(QFont("黑体"))
        self.name3.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 0px;background-color: transparent;font-size: 15px;')
        # 白种人 原/白
        self.name4 = QLabel('白种人', self)
        self.name4.setGeometry(615, 480, 60, 20)
        self.name4.setFont(QFont("黑体"))
        self.name4.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 0px;background-color: transparent;font-size: 15px;')
        # 黑种人 原/黑
        self.name5 = QLabel('黑种人', self)
        self.name5.setGeometry(615, 560, 60, 20)
        self.name5.setFont(QFont("黑体"))
        self.name5.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 0px;background-color: transparent;font-size: 15px;')
        # 表情 笑/严
        self.name6 = QLabel('表情', self)
        self.name6.setGeometry(615, 640, 40, 20)
        self.name6.setFont(QFont("黑体"))
        self.name6.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 0px;background-color: transparent;font-size: 15px;')

        # 参数值
        # 颜值
        self.Val1 = QLabel('0', self)
        self.Val1.setGeometry(315, 480, 30, 20)
        self.Val1.setFont(QFont("黑体"))
        self.Val1.setStyleSheet('color:rgb(78, 39, 23);border-width: 0px;background-color: transparent;font-size: 15px;')
        # 水平调整角度
        self.Val2 = QLabel('0', self)
        self.Val2.setGeometry(378, 560, 30, 20)
        self.Val2.setFont(QFont("黑体"))
        self.Val2.setStyleSheet('color:rgb(78, 39, 23);border-width: 0px;background-color: transparent;font-size: 15px;')
        # 性别
        self.Val3 = QLabel('0', self)
        self.Val3.setGeometry(315, 640, 30, 20)
        self.Val3.setFont(QFont("黑体"))
        self.Val3.setStyleSheet('color:rgb(78, 39, 23);border-width: 0px;background-color: transparent;font-size: 15px;')
        # 白种人
        self.Val4 = QLabel('0', self)
        self.Val4.setGeometry(675, 480, 30, 20)
        self.Val4.setFont(QFont("黑体"))
        self.Val4.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 0px;background-color: transparent;font-size: 15px;')
        # 黑种人
        self.Val5 = QLabel('0', self)
        self.Val5.setGeometry(675, 560, 30, 20)
        self.Val5.setFont(QFont("黑体"))
        self.Val5.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 0px;background-color: transparent;font-size: 15px;')
        # 表情
        self.Val6 = QLabel('0', self)
        self.Val6.setGeometry(660, 640, 30, 20)
        self.Val6.setFont(QFont("黑体"))
        self.Val6.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 0px;background-color: transparent;font-size: 15px;')

        # 参数滑动条
        # 颜值
        self.splider1 = QSlider(Qt.Horizontal, self)
        self.splider1.setGeometry(295, 510, 250, 20)
        self.splider1.setFocusPolicy(Qt.NoFocus)
        self.splider1.valueChanged[int].connect(self.changedVal1)
        #实时调整
        self.splider1.sliderReleased.connect(self.released1)

        self.splider1.setMinimum(-100)  # 参数最小值
        self.splider1.setMaximum(100)  # 参数最大值
        self.splider1.setSingleStep(10)  # 步长
        self.splider1.setStyleSheet('color:rgb(236, 175, 193);background-color: transparent;')
        left1 = QLabel('低', self)
        left1.setGeometry(270, 510, 20, 20)
        left1.setAlignment(Qt.AlignCenter)
        left1.setFont(QFont("黑体"))
        left1.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 1px;border-style: solid;border-color: rgb(236, 175, 193);'
            'border-radius: 10px;background-color: transparent;font-size: 15px;')
        right1 = QLabel('高', self)
        right1.setGeometry(550, 510, 20, 20)
        right1.setAlignment(Qt.AlignCenter)
        right1.setFont(QFont("黑体"))
        right1.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 1px;border-style: solid;border-color: rgb(236, 175, 193);'
            'border-radius: 10px;background-color: transparent;font-size: 15px;')
        # 水平调整角度
        self.splider2 = QSlider(Qt.Horizontal, self)
        self.splider2.setGeometry(295, 590, 250, 20)
        self.splider2.setFocusPolicy(Qt.NoFocus)
        self.splider2.valueChanged[int].connect(self.changedVal2)
        # 实时调整
        self.splider2.sliderReleased.connect(self.released2)

        self.splider2.setMinimum(-100)  # 参数最小值
        self.splider2.setMaximum(100)  # 参数最大值
        self.splider2.setSingleStep(10)  # 步长
        self.splider2.setStyleSheet('color:rgb(236, 175, 193);background-color: transparent;')
        left2 = QLabel('左', self)
        left2.setGeometry(270, 590, 20, 20)
        left2.setAlignment(Qt.AlignCenter)
        left2.setFont(QFont("黑体"))
        left2.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 1px;border-style: solid;border-color: rgb(236, 175, 193);'
            'border-radius: 10px;background-color: transparent;font-size: 15px;')
        right2 = QLabel('右', self)
        right2.setGeometry(550, 590, 20, 20)
        right2.setAlignment(Qt.AlignCenter)
        right2.setFont(QFont("黑体"))
        right2.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 1px;border-style: solid;border-color: rgb(236, 175, 193);'
            'border-radius: 10px;background-color: transparent;font-size: 15px;')
        # 性别
        self.splider3 = QSlider(Qt.Horizontal, self)
        self.splider3.setGeometry(295, 670, 250, 20)
        self.splider3.setFocusPolicy(Qt.NoFocus)
        self.splider3.valueChanged[int].connect(self.changedVal3)
        # 实时调整
        self.splider3.sliderReleased.connect(self.released3)

        self.splider3.setMinimum(-100)  # 参数最小值
        self.splider3.setMaximum(100)  # 参数最大值
        self.splider3.setSingleStep(10)  # 步长
        self.splider3.setStyleSheet('color:rgb(236, 175, 193);background-color: transparent;')
        left3 = QLabel('女', self)
        left3.setGeometry(270, 670, 20, 20)
        left3.setAlignment(Qt.AlignCenter)
        left3.setFont(QFont("黑体"))
        left3.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 1px;border-style: solid;border-color: rgb(236, 175, 193);'
            'border-radius: 10px;background-color: transparent;font-size: 15px;')
        right3 = QLabel('男', self)
        right3.setGeometry(550, 670, 20, 20)
        right3.setAlignment(Qt.AlignCenter)
        right3.setFont(QFont("黑体"))
        right3.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 1px;border-style: solid;border-color: rgb(236, 175, 193);'
            'border-radius: 10px;background-color: transparent;font-size: 15px;')
        # 白种人
        self.splider4 = QSlider(Qt.Horizontal, self)
        self.splider4.setGeometry(640, 510, 250, 20)
        self.splider4.setFocusPolicy(Qt.NoFocus)
        self.splider4.valueChanged[int].connect(self.changedVal4)
        # 实时调整
        self.splider4.sliderReleased.connect(self.released4)

        self.splider4.setMinimum(0)  # 参数最小值
        self.splider4.setMaximum(100)  # 参数最大值
        self.splider4.setSingleStep(10)  # 步长
        self.splider4.setStyleSheet('color:rgb(236, 175, 193);background-color: transparent;')
        left4 = QLabel('原', self)
        left4.setGeometry(615, 510, 20, 20)
        left4.setAlignment(Qt.AlignCenter)
        left4.setFont(QFont("黑体"))
        left4.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 1px;border-style: solid;border-color: rgb(236, 175, 193);'
            'border-radius: 10px;background-color: transparent;font-size: 15px;')
        right4 = QLabel('白', self)
        right4.setGeometry(895, 510, 20, 20)
        right4.setAlignment(Qt.AlignCenter)
        right4.setFont(QFont("黑体"))
        right4.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 1px;border-style: solid;border-color: rgb(236, 175, 193);'
            'border-radius: 10px;background-color: transparent;font-size: 15px;')
        # 黑种人
        self.splider5 = QSlider(Qt.Horizontal, self)
        self.splider5.setGeometry(640, 590, 250, 20)
        self.splider5.setFocusPolicy(Qt.NoFocus)
        self.splider5.valueChanged[int].connect(self.changedVal5)
        # 实时调整
        self.splider5.sliderReleased.connect(self.released5)

        self.splider5.setMinimum(0)  # 参数最小值
        self.splider5.setMaximum(100)  # 参数最大值
        self.splider5.setSingleStep(10)  # 步长
        self.splider5.setStyleSheet('color:rgb(236, 175, 193);background-color: transparent;')
        left5 = QLabel('原', self)
        left5.setGeometry(615, 590, 20, 20)
        left5.setAlignment(Qt.AlignCenter)
        left5.setFont(QFont("黑体"))
        left5.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 1px;border-style: solid;border-color: rgb(236, 175, 193);'
            'border-radius: 10px;background-color: transparent;font-size: 15px;')
        right5 = QLabel('黑', self)
        right5.setGeometry(895, 590, 20, 20)
        right5.setAlignment(Qt.AlignCenter)
        right5.setFont(QFont("黑体"))
        right5.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 1px;border-style: solid;border-color: rgb(236, 175, 193);'
            'border-radius: 10px;background-color: transparent;font-size: 15px;')
        # 表情
        self.splider6 = QSlider(Qt.Horizontal, self)
        self.splider6.setGeometry(640, 670, 250, 20)
        self.splider6.setFocusPolicy(Qt.NoFocus)
        self.splider6.valueChanged[int].connect(self.changedVal6)
        # 实时调整
        self.splider6.sliderReleased.connect(self.released6)

        self.splider6.setMinimum(-100)  # 参数最小值
        self.splider6.setMaximum(100)  # 参数最大值
        self.splider6.setSingleStep(10)  # 步长
        self.splider6.setStyleSheet('color:rgb(236, 175, 193);background-color: transparent;')
        left6 = QLabel('笑', self)
        left6.setGeometry(615, 670, 20, 20)
        left6.setAlignment(Qt.AlignCenter)
        left6.setFont(QFont("黑体"))
        left6.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 1px;border-style: solid;border-color: rgb(236, 175, 193);'
            'border-radius: 10px;background-color: transparent;font-size: 15px;')
        right6 = QLabel('严', self)
        right6.setGeometry(895, 670, 20, 20)
        right6.setAlignment(Qt.AlignCenter)
        right6.setFont(QFont("黑体"))
        right6.setStyleSheet(
            'color:rgb(78, 39, 23);border-width: 1px;border-style: solid;border-color: rgb(236, 175, 193);'
            'border-radius: 10px;background-color: transparent;font-size: 15px;')

        # 返回首页

        back = QPushButton(self)
        back.setGeometry(1059, 627, 141, 173)
        back.clicked.connect(self.backPerson)  # 保存结果图
        back.setStyleSheet("QPushButton{border-image: url(src/balloon.png)}"
                            "QPushButton:hover{border-image: url(src/start.png)}")
        back.setCursor(Qt.PointingHandCursor)
        self.show()

    #颜值
    def released1(self):
        step = self.value1 * 0.02 * -1
        dir_flag = 1
        play_with_dlatent.select_directions(Gs, step, pic_num, dir_flag)
        self.outpic.setPixmap(QPixmap('result_picture/result.png'))
        self.outpic.setScaledContents(True)

    #水平角度
    def released2(self):
        step = self.value2 * 0.02
        print("step:", step)
        dir_flag = 2
        play_with_dlatent.select_directions(Gs, step, pic_num, dir_flag)
        self.outpic.setPixmap(QPixmap('result_picture/result.png'))
        self.outpic.setScaledContents(True)

    #性别
    def released3(self):
        step = self.value3 * 0.05
        dir_flag = 3
        play_with_dlatent.select_directions(Gs, step, pic_num, dir_flag)
        self.outpic.setPixmap(QPixmap('result_picture/result.png'))
        self.outpic.setScaledContents(True)

    #白种人
    def released4(self):
        step = self.value4 * 0.07
        dir_flag = 4
        play_with_dlatent.select_directions(Gs, step, pic_num, dir_flag)
        self.outpic.setPixmap(QPixmap('result_picture/result.png'))
        self.outpic.setScaledContents(True)

    #黑种人
    def released5(self):
        step = self.value5 * 0.03
        dir_flag = 5
        play_with_dlatent.select_directions(Gs, step, pic_num, dir_flag)
        self.outpic.setPixmap(QPixmap('result_picture/result.png'))
        self.outpic.setScaledContents(True)

    #表情
    def released6(self):
        step = self.value6 * 0.04
        dir_flag = 6
        play_with_dlatent.select_directions(Gs, step, pic_num, dir_flag)
        self.outpic.setPixmap(QPixmap('result_picture/result.png'))
        self.outpic.setScaledContents(True)

    def backPerson(self):
        self.newWindow = personWindow.personWindow()
        self.newWindow.show()
        self.close()

    def changedVal1(self, value):
        self.value1 = value
        self.Val1.setNum(self.value1)

    def changedVal2(self, value):
        self.value2 = value
        self.Val2.setNum(self.value2)

    def changedVal3(self, value):
        self.value3 = value
        self.Val3.setNum(self.value3)

    def changedVal4(self, value):
        self.value4 = value
        self.Val4.setNum(self.value4)

    def changedVal5(self, value):
        self.value5 = value
        self.Val5.setNum(self.value5)

    def changedVal6(self, value):
        self.value6 = value
        self.Val6.setNum(self.value6)

    def savePic(self):
        # 保存到 保存图片/result.png
        self.image = QtGui.QPixmap("result_picture\\result.png").scaled(256, 256)
        self.image.save("保存图片\\result.png")
        self.outpic.setPixmap(QPixmap('result_picture/result.png'))


    # 窗口在屏幕中心显示
    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    # 创建应用程序和对象
    app = QApplication(sys.argv)
    ex = YellowDetailWindow()
    sys.exit(app.exec_())