import sys
import os
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, QToolTip, QPushButton, QFileDialog, QAction, QApplication, QDesktopWidget, QMessageBox, QCheckBox
from PyQt5.Qt import QLineEdit
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QHBoxLayout, QSpinBox, QSlider, QLabel, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QImage
from PyQt5.QtCore import Qt
import play_with_dlatent
import personWindow

class QSlider(QSlider):
    def wheelEvent(self, *args, **kwargs): # real signature unknown
        pass

class DetailWindow(QWidget):
    def __init__(self, father, title, Gs, model_res, dir_list, dir_weight, img, latent):
        super().__init__()

        play_with_dlatent.init(Gs, latent, model_res)

        self.father = father

        self.model_res = model_res

        #窗口标题
        self.title = title

        self.init_pic = img
        self.result_pic = img

        #调整向量名称列表
        self.dir_list = dir_list

        #向量权重
        self.dir_weight = dir_weight
        
        self.path = "chosen_picture"

        # 参数值
        self.value = [0] * 6

        self.initUI()

    def initUI(self):
        # 窗口大小、居中显示、标题
        self.resize(1200, 800)
        self.center()
        self.setWindowTitle(self.title)
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
        self.inpic.setPixmap(QPixmap(self.init_pic))
        self.inpic.setScaledContents(True)
        # 删除
        for maindir, subdir, file_name_list in os.walk(self.path):
            for filename in file_name_list:
                if (filename.endswith(".png")):
                    os.remove(maindir + "\\" + filename)

        # 输出窗口
        self.outpic = QLabel(self)
        self.outpic.resize(256, 256)
        self.outpic.move(644, 200)
        self.outpic.setPixmap(QPixmap(self.result_pic))
        self.outpic.setScaledContents(True)
        # 保存图片
        save = QPushButton('↓', self)
        save.setGeometry(860, 416, 40, 40)
        save.setStyleSheet('color:rgb(237, 237, 237);border-radius: 20px;'
                           'border-color: rgb(0, 0, 0);background-color: rgb(236, 175, 193);font-size: 25px;')
        save.setCursor(Qt.PointingHandCursor)
        save.clicked.connect(self.savePic)

        #以下用于方便循环时赋值
        label_name_table = {
            'age': '年龄',
            'angle_horizontal': '水平角度',
            'angle_vertical': '垂直角度',
            'beauty': '美容',
            'emotion_angry': '愤怒',
            'emotion_disgust': '厌恶',
            'emotion_easy': '放松',
            'emotion_fear': '恐惧',
            'emotion_happy': '开心',
            'emotion_sad': '难过',
            'emotion_surprise': '惊喜',
            'exposure': '曝光',
            'eyes_open': '眼睛开闭',
            'face_shape': '惊喜',
            'glasses': '眼镜',
            'gender': '性别',
            'height': '高度',
            'width': '宽度',
            'race_yellow': '黄种人',
            'race_black': '黑种人',
            'race_white': '白种人',
            'smile': '笑容'
        }

        slider_change_callbacks = [
            self.onValueChange0,
            self.onValueChange1,
            self.onValueChange2,
            self.onValueChange3,
            self.onValueChange4,
            self.onValueChange5
        ]

        slider_release_callbacks = [
            self.onRelease0,
            self.onRelease1,
            self.onRelease2,
            self.onRelease3,
            self.onRelease4,
            self.onRelease5
        ]

        #放置调整控件
        self.label = [0] * 6
        self.value_label = [0] * 6
        self.slider = [0] * 6
        for i in range(6):
            #参数名
            self.label[i] = QLabel(label_name_table[self.dir_list[i]], self)
            self.label[i].setGeometry(270 + 345*(i&1), 480 + 80*(int(i/2)), 120, 20)
            self.label[i].setFont(QFont("黑体"))
            self.label[i].setStyleSheet(
                'color:rgb(78, 39, 23);border-width: 0px;background-color: transparent;font-size: 15px;')
            #参数值
            self.value_label[i] = QLabel('0', self)
            self.value_label[i].setGeometry(415 + 345*(i&1), 480 + 80*(int(i/2)), 30, 20)
            self.value_label[i].setFont(QFont("黑体"))
            self.value_label[i].setStyleSheet('color:rgb(78, 39, 23);border-width: 0px;background-color: transparent;font-size: 15px;')
            #拖动条
            self.slider[i] = QSlider(Qt.Horizontal, self)
            self.slider[i].setGeometry(295 + 345*(i&1), 510 + 80*(int(i/2)), 250, 20)
            self.slider[i].setFocusPolicy(Qt.NoFocus)
            self.slider[i].valueChanged[int].connect(slider_change_callbacks[i])
            self.slider[i].sliderReleased.connect(slider_release_callbacks[i])
            # self.slider[i].sliderReleased.connect(lambda:self.onRelease(i))
            self.slider[i].setMinimum(-100)  # 参数最小值
            self.slider[i].setMaximum(100)  # 参数最大值
            self.slider[i].setSingleStep(5)  # 步长,没有加回调
            self.slider[i].setStyleSheet('color:rgb(236, 175, 193);background-color: transparent;')
            #调整方向提示
            neg_label = QLabel('-', self)
            neg_label.setGeometry(270 + 345*(i&1), 510 + 80*(int(i/2)), 20, 20)
            neg_label.setAlignment(Qt.AlignCenter)
            neg_label.setFont(QFont("黑体"))
            neg_label.setStyleSheet(
                'color:rgb(78, 39, 23);border-width: 1px;border-style: solid;border-color: rgb(236, 175, 193);'
                'border-radius: 10px;background-color: transparent;font-size: 15px;')
            pos_label = QLabel('+', self)
            pos_label.setGeometry(550 + 345*(i&1), 510 + 80*(int(i/2)), 20, 20)
            pos_label.setAlignment(Qt.AlignCenter)
            pos_label.setFont(QFont("黑体"))
            pos_label.setStyleSheet(
                'color:rgb(78, 39, 23);border-width: 1px;border-style: solid;border-color: rgb(236, 175, 193);'
                'border-radius: 10px;background-color: transparent;font-size: 15px;')

        # 返回按钮
        back = QPushButton(self)
        back.setGeometry(1059, 627, 141, 173)
        back.clicked.connect(self.backPerson)  # 保存结果图
        back.setStyleSheet("QPushButton{border-image: url(src/balloon.png)}"
                            "QPushButton:hover{border-image: url(src/start.png)}")
        back.setCursor(Qt.PointingHandCursor)

        self.show()

    #生成新图像，传入向量名与调整
    def refresh_pic(self, dir_name, step):
        im = play_with_dlatent.select_directions('./latent_directions/' + dir_name + '.npy', step)
        self.result_pic = QImage(im.tobytes('raw', 'RGB'), im.size[0], im.size[1], QImage.Format_RGB888)
        self.outpic.setPixmap(QPixmap(self.result_pic))
        self.outpic.setScaledContents(True)

    def onRelease(self, index):
        print('index = ' + str(index))
        current = self.slider[index].value()
        step = (current - self.value[index]) * self.dir_weight[index]
        self.value[index] = current
        self.refresh_pic(self.dir_list[index], step)

    def onRelease0(self):
        current = self.slider[0].value()
        step = (current - self.value[0]) * self.dir_weight[0]
        self.value[0] = current
        self.refresh_pic(self.dir_list[0], step)

    def onRelease1(self):
        current = self.slider[1].value()
        step = (current - self.value[1]) * self.dir_weight[1]
        self.value[1] = current
        self.refresh_pic(self.dir_list[1], step)

    def onRelease2(self):
        current = self.slider[2].value()
        step = (current - self.value[2]) * self.dir_weight[2]
        self.value[2] = current
        self.refresh_pic(self.dir_list[2], step)

    def onRelease3(self):
        current = self.slider[3].value()
        step = (current - self.value[3]) * self.dir_weight[3]
        self.value[3] = current
        self.refresh_pic(self.dir_list[3], step)

    def onRelease4(self):
        current = self.slider[4].value()
        step = (current - self.value[4]) * self.dir_weight[4]
        self.value[4] = current
        self.refresh_pic(self.dir_list[4], step)

    def onRelease5(self):
        current = self.slider[5].value()
        step = (current - self.value[5]) * self.dir_weight[5]
        self.value[5] = current
        self.refresh_pic(self.dir_list[5], step)

    def backPerson(self):
        self.father.setEnabled(True)
        self.close()

    def onValueChange0(self, value):
        self.value_label[0].setNum(value)

    def onValueChange1(self, value):
        self.value_label[1].setNum(value)

    def onValueChange2(self, value):
        self.value_label[2].setNum(value)

    def onValueChange3(self, value):
        self.value_label[3].setNum(value)

    def onValueChange4(self, value):
        self.value_label[4].setNum(value)

    def onValueChange5(self, value):
        self.value_label[5].setNum(value)

    def savePic(self):
        # 保存到 保存图片/result.png
        self.result_pic.save("result_picture\\result.png")
        QMessageBox.about(self, "提示", "图像保存成功！")

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
    ex = ModelDetailWindow()
    sys.exit(app.exec_())