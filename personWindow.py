import sys
import DetailWindow
from PyQt5 import QtGui, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QWidget, QLabel, QTextEdit, QToolTip,
                             QPushButton, QFileDialog, QAction, QApplication, QDesktopWidget, QMessageBox, QCheckBox,
                             QDialog)
from PyQt5.QtGui import QIcon, QColor, QPixmap, QFont, QMovie, QImage
from PyQt5.Qt import QLineEdit
import generate_face
import dnnlib.tflib as tflib
import multiprocessing
import time
import main

#标记点击的标签，便于刷新操作
flag = -1
pic_num = 0
yellow_Gs = None
model_Gs = None
cartoon_Gs = None
ancient_Gs = None

class personWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.waitWin = waitWindow()

        self.initUI()

    def initUI(self):
        # 窗口大小、居中显示、标题
        self.resize(1200, 800)
        self.center()
        self.setWindowTitle('Sim-Create: 人像生成')
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 禁止拉伸窗口大小
        self.setFixedSize(self.width(), self.height())

        self.flag = 0  # 标志人脸生成代码是否完成，完成置1

        # logo
        title = QLabel(self)
        title.resize(1200, 800)
        title.move(0, 0)
        title.setPixmap(QPixmap("src/person-bg.png"))

        #标签,点击标签不同类型的脸生成

        yellow = QPushButton("黄种人脸", self)
        yellow.resize(117, 28)
        yellow.move(248, 248)
        yellow.setFont(QFont("黑体"))
        yellow.setStyleSheet('color:rgb(255, 255, 255);border-radius:25px;font-size: 20px;background-color: rgb(204, 204, 204);')
        yellow.clicked.connect(self.yellowGenerate)
        yellow.setCursor(Qt.PointingHandCursor)  # 设置鼠标移动到上面的形状

        supermodel = QPushButton("超模人脸", self)
        supermodel.resize(93, 28)
        supermodel.move(448, 195)
        supermodel.setFont(QFont("黑体"))
        supermodel.setStyleSheet('color:rgb(255, 255, 255);border-radius:25px;font-size: 20px;background-color: rgb(204, 204, 204);')
        supermodel.clicked.connect(self.supermodelGenerate)
        supermodel.setCursor(Qt.PointingHandCursor)

        cartoon = QPushButton("日漫人脸", self)
        cartoon.resize(103, 28)
        cartoon.move(537, 268)
        cartoon.setFont(QFont("黑体"))
        cartoon.setStyleSheet('color:rgb(255, 255, 255);border-radius:25px;font-size: 20px;background-color: rgb(204, 204, 204);')
        cartoon.clicked.connect(self.cartoonGenerate)
        cartoon.setCursor(Qt.PointingHandCursor)

        ancient = QPushButton("古风人脸", self)
        ancient.resize(109, 28)
        ancient.move(731, 226)
        ancient.setFont(QFont("黑体"))
        ancient.setStyleSheet('color:rgb(255, 255, 255);border-radius:25px;font-size: 20px;background-color: rgb(204, 204, 204);')
        ancient.clicked.connect(self.ancientGenerate)
        ancient.setCursor(Qt.PointingHandCursor)

        # 放置生成的五张图片
        self.pic = [0] * 5
        for i in range(5):
            self.pic[i] = QLabel(self)
            self.pic[i].resize(200, 200)
            self.pic[i].move(33 + 233 * i, 350)
            self.pic[i].setPixmap(QPixmap("src/person-pic-bg.png"))
            self.pic[i].setScaledContents(True)

        # 放置复选框，在进行进一步参数调整时需要对复选框选中数量进行判断
        self.PicArray = [False, False, False, False, False]
        self.sum = int(0)  # 复选框选中的总数
        print(sum)

        self.IsSelectPic = [0] * 5
        for i in range(5):
            self.IsSelectPic[i] = QCheckBox(' ', self)
            self.IsSelectPic[i].resize(50, 50)
            self.IsSelectPic[i].move(217 + 233 * i, 530)
            self.IsSelectPic[i].stateChanged.connect(self.SelectPicture)
            self.IsSelectPic[i].setCursor(Qt.PointingHandCursor)

        # 返回首页
        self.back = QPushButton("返回首页", self)
        self.back.resize(100, 50)
        self.back.move(380, 620)
        self.back.setFont(QFont("黑体"))
        self.back.setStyleSheet('color:rgb(255, 255, 255);font-size: 20px;background-color: transparent;')
        self.back.setCursor(Qt.PointingHandCursor)
        # 跳转到首页
        self.back.clicked.connect(self.backMain)

        # 参数细化
        self.toDetailButton = QPushButton("参数细化", self)
        self.toDetailButton.resize(100, 50)
        self.toDetailButton.move(550, 620)
        self.toDetailButton.setFont(QFont("黑体"))
        self.toDetailButton.setStyleSheet('color:rgb(255, 255, 255);font-size: 25px;background-color: transparent;')
        self.toDetailButton.setCursor(Qt.PointingHandCursor)
        # 跳转到参数细化
        self.toDetailButton.clicked.connect(self.toDetail)

        # 保存图片
        save = QPushButton("保存图片", self)
        save.resize(100, 50)
        save.move(720, 620)
        save.setFont(QFont("黑体"))
        save.setStyleSheet('color:rgb(255, 255, 255);font-size: 20px;background-color: transparent;')
        save.setCursor(Qt.PointingHandCursor)
        # 保存图片
        save.clicked.connect(self.save)

        refresh = QPushButton("刷新", self)
        refresh.resize(80, 30)
        refresh.move(1100, 320)
        refresh.setFont(QFont("黑体"))
        refresh.setStyleSheet('color:rgb(150, 150, 150);font-size: 30px;background-color: transparent;')
        refresh.setCursor(Qt.PointingHandCursor)
            # 保存图片
        refresh.clicked.connect(self.refresh)


    # 刷新的响应事件
    def refresh(self):
        global flag
        if flag == -1:
            return
        global yellow_Gs, model_Gs, cartoon_Gs, ancient_Gs
        # 这里加生成图片的代码
        models = [yellow_Gs, model_Gs, cartoon_Gs, ancient_Gs]
        g_model = models[flag]
        pics, latents = generate_face.generate(g_model)
        self.set_pic(pics)
        self.set_latents(latents)

    def yellowGenerate(self):
        # 调用生成模型
        global flag
        global yellow_Gs
        if (flag != 0):
            flag = 0
            yellow_Gs = generate_face.face_select(0)
        pics, latents = generate_face.generate(yellow_Gs)
        self.set_pic(pics)
        self.set_latents(latents)

    def supermodelGenerate(self):
        #self.wait()
        #调用生成模型
        global flag
        global model_Gs
        if (flag != 1):
            flag = 1
            model_Gs = generate_face.face_select(1)
        pics, latents = generate_face.generate(model_Gs)
        self.set_pic(pics)
        self.set_latents(latents)

    def cartoonGenerate(self):
        #self.wait()
        #调用生成模型
        global flag
        global cartoon_Gs
        if (flag != 2):
            flag = 2
            cartoon_Gs = generate_face.face_select(2)
        pics, latents = generate_face.generate(cartoon_Gs)
        self.set_pic(pics)
        self.set_latents(latents)

    def ancientGenerate(self):
        #self.wait()
        #调用生成模型
        global flag
        global ancient_Gs
        if (flag != 3):
            flag = 3
            ancient_Gs = generate_face.face_select(3)
        pics, latents = generate_face.generate(ancient_Gs)
        self.set_pic(pics)
        self.set_latents(latents)

    '''def wait(self):
        self.waitWin.show()
        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.operate)  # 计时结束调用operate()方法
        self.timer.start(1000)  # 设置计时间隔并启动

    def operate(self):
        # 每隔1000ms检测flag值是否为1
        # 若为1，关闭定时器，关闭加载动画，开始加载图片
        self.timer.stop()
        self.waitWin.close()
        self.set_pic()
    '''

    def set_latents(self, latents):
        self.latents = latents[:]

    def set_pic(self, pics):
        self.imgs = []
        for i in range(5):
            img = QImage(pics[i].tobytes('raw', 'RGB'), pics[i].size[0], pics[i].size[1], QImage.Format_RGB888)
            self.imgs.append(img)
            self.pic[i].setPixmap(QPixmap(img))  # 修改显示的五张图片

    #进入参数调整界面
    def toDetail(self):
        global flag
        global pic_num
        if flag == -1:
            QMessageBox.about(self, "提示", "您还没有生成图像")
            return
        if self.sum == 0:
             #没有选中图片
             QMessageBox.about(self, "提示", "选中图片不能为空")
        if self.sum == 1:
            #打开新窗口进行参数细化,并将选择的图片放入文件夹保存
            for i in range(5):
                if self.PicArray[i] == True:
                    pic_num = i
                    self.imgs[i].save("chosen_picture\\" + str(i) + ".png")
                    break
            if flag == 0: #黄种人
                self.newWindow = DetailWindow.DetailWindow(
                    self,
                    'Sim-Create: 调整界面',
                    yellow_Gs,
                    1024,
                    ['age', 'gender', 'angle_vertical', 'angle_horizontal', 'eyes_open', 'width'],
                    [-0.05, 0.05, 0.05, 0.05, 0.05, -0.05],
                    self.imgs[pic_num],
                    self.latents[i]
                )
            elif flag == 1: #超模
                self.newWindow = DetailWindow.DetailWindow(
                    self,
                    'Sim-Create: 调整界面',
                    model_Gs,
                    1024,
                    ['angle_vertical', 'angle_horizontal', 'gender', 'race_yellow', 'race_black', 'emotion_happy'],
                    [0.05, 0.05, 0.05, 0.05, 0.05, 0.05],
                    self.imgs[pic_num],
                    self.latents[i]
                )
            elif flag == 2: #动漫，向量待修改
                self.newWindow = DetailWindow.DetailWindow(
                    self,
                    'Sim-Create: 调整界面',
                    cartoon_Gs,
                    512,
                    ['angle_vertical', 'angle_horizontal', 'eyes_open', 'glasses', 'emotion_happy', 'emotion_fear'],
                    [-0.05, 0.05, 0.05, 0.05, 0.05, -0.05],
                    self.imgs[pic_num],
                    self.latents[i]
                )
            elif flag == 3: #古风测试
                self.newWindow = DetailWindow.DetailWindow(
                    self,
                    'Sim-Create: 调整界面',
                    ancient_Gs,
                    512,
                    ['angle_vertical', 'angle_horizontal', 'eyes_open', 'glasses', 'emotion_happy', 'emotion_fear'],
                    [-0.05, 0.05, 0.05, 0.05, 0.05, -0.05],
                    self.imgs[pic_num],
                    self.latents[i]
                )
            else:
                QMessageBox.about(self, "提示", "抱歉，该模型暂时不支持参数调整")
                return
            self.setDisabled(True)
            self.newWindow.show()
            # self.close()

        if self.sum > 1:
            QMessageBox.about(self, "提示", "不能同时对多张图片进行操作")

    def save(self):
        # 这里应该使用批量保存，而不是一个一个保存
        QMessageBox.about(self, "提示", "确认保存所选人物素材？")
        for i in range(0, 4):
            if self.PicArray[i] == True:
                filename = QFileDialog.getSaveFileName(self, "选择第" + str(i+1) + "张图片保存位置", "", "*.png;;*.jpg;;*bmp;;All Files(*)")
                self.image = QtGui.QPixmap("result_picture\\" + str(i) + ".png").scaled(256, 256)
                self.image.save(filename[0])

    #每次选择一个图片，选择总数加一，取消选择则减一,将选择了哪些图片记录下来
    def SelectPicture(self, state):

        if state == Qt.Checked:
            self.sum = self.sum + 1;
        else:
            self.sum = self.sum - 1;

        for i in range(5):
            self.PicArray[i] = self.IsSelectPic[i].isChecked()

    def backMain(self):
        self.newWindow = main.mainWindow()
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

class waitWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.waitGif = QLabel(self)
        self.gif = QMovie('src/wait.gif')
        self.initUI()

    def initUI(self):
        self.resize(650, 387)
        self.center()
        self.setWindowTitle('图片生成中，请等待……')

        self.waitGif.setMovie(self.gif)
        self.waitGif.setScaledContents(True)
        self.gif.start()
        self.setWindowFlags(Qt.FramelessWindowHint)

    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())
