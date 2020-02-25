import sys
import bedroom_bkgDetailWindow
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QWidget, QLabel, QTextEdit, QToolTip,
                             QPushButton, QFileDialog, QAction, QApplication, QDesktopWidget, QMessageBox, QCheckBox,
                             QDialog)
from PyQt5.QtGui import QIcon, QColor, QPixmap, QFont, QMovie
from PyQt5.Qt import QLineEdit
import main
import generate_background
import time

class backgroundWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.waitWin = waitWindow()

        self.initUI()

    def initUI(self):
        # 窗口大小、居中显示、标题
        self.resize(1200, 800)
        self.center()
        self.setWindowTitle('人像生成')
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 禁止拉伸窗口大小
        self.setFixedSize(self.width(), self.height())

        # logo
        title = QLabel(self)
        title.resize(1200, 800)
        title.move(0, 0)
        title.setPixmap(QPixmap("src/background-bg.png"))

        # 标签,点击标签不同类型的脸生成
        self.Judge = 0 #用于判断是哪个标签，初始值为0
        bedroom = QPushButton("卧室", self)
        bedroom.resize(117, 28)
        bedroom.move(248, 248)
        bedroom.setFont(QFont("黑体"))
        bedroom.setStyleSheet('color:rgb(255, 255, 255);border-radius:25px;font-size: 20px;background-color: rgb(217, 217, 217);')
        bedroom.clicked.connect(self.bedroomGenerate)
        bedroom.setCursor(Qt.PointingHandCursor)  # 设置鼠标移动到上面的形状

        forest = QPushButton("森林", self)
        forest.resize(93, 28)
        forest.move(448, 195)
        forest.setFont(QFont("黑体"))
        forest.setStyleSheet('color:rgb(255, 255, 255);border-radius:25px;font-size: 20px;background-color: rgb(217, 217, 217);')
        forest.clicked.connect(self.forestGenerate)
        forest.setCursor(Qt.PointingHandCursor)

        sky = QPushButton("天空", self)
        sky.resize(103, 28)
        sky.move(537, 268)
        sky.setFont(QFont("黑体"))
        sky.setStyleSheet('color:rgb(255, 255, 255);border-radius:25px;font-size: 20px;background-color: rgb(217, 217, 217);')
        sky.clicked.connect(self.skyGenerate)
        sky.setCursor(Qt.PointingHandCursor)

        aurora = QPushButton("极光", self)
        aurora.resize(109, 28)
        aurora.move(731, 226)
        aurora.setFont(QFont("黑体"))
        aurora.setStyleSheet('color:rgb(255, 255, 255);border-radius:25px;font-size: 20px;background-color: rgb(217, 217, 217);')
        aurora.clicked.connect(self.auroraGenerate)
        aurora.setCursor(Qt.PointingHandCursor)

        # 放置生成的五张图片
        self.pic0 = QLabel(self)
        self.pic0.resize(200, 200)
        self.pic0.move(33, 350)
        self.pic0.setPixmap(QPixmap("src/background-pic-bg.png"))
        self.pic0.setScaledContents(True)

        self.pic1 = QLabel(self)
        self.pic1.resize(200, 200)
        self.pic1.move(266, 350)
        self.pic1.setPixmap(QPixmap("src/background-pic-bg.png"))
        self.pic1.setScaledContents(True)

        self.pic2 = QLabel(self)
        self.pic2.resize(200, 200)
        self.pic2.move(499, 350)
        self.pic2.setPixmap(QPixmap("src/background-pic-bg.png"))
        self.pic2.setScaledContents(True)

        self.pic3 = QLabel(self)
        self.pic3.resize(200, 200)
        self.pic3.move(732, 350)
        self.pic3.setPixmap(QPixmap("src/background-pic-bg.png"))
        self.pic3.setScaledContents(True)

        self.pic4 = QLabel(self)
        self.pic4.resize(200, 200)
        self.pic4.move(965, 350)
        self.pic4.setPixmap(QPixmap("src/background-pic-bg.png"))
        self.pic4.setScaledContents(True)

        # 放置复选框，在进行进一步参数调整时需要对复选框选中数量进行判断
        self.PicArray = [False, False, False, False, False]
        self.sum = int(0)  # 复选框选中的总数
        print(sum)
        self.IsSelectPic0 = QCheckBox(' ', self)
        self.IsSelectPic0.resize(25, 25)
        self.IsSelectPic0.move(217, 530)
        self.IsSelectPic0.stateChanged.connect(self.SelectPicture)
        self.IsSelectPic0.setCursor(Qt.PointingHandCursor)

        self.IsSelectPic1 = QCheckBox(' ', self)
        self.IsSelectPic1.resize(25, 25)
        self.IsSelectPic1.move(450, 530)
        self.IsSelectPic1.stateChanged.connect(self.SelectPicture)
        self.IsSelectPic1.setCursor(Qt.PointingHandCursor)

        self.IsSelectPic2 = QCheckBox(' ', self)
        self.IsSelectPic2.resize(25, 25)
        self.IsSelectPic2.move(683, 530)
        self.IsSelectPic2.stateChanged.connect(self.SelectPicture)
        self.IsSelectPic2.setCursor(Qt.PointingHandCursor)

        self.IsSelectPic3 = QCheckBox(' ', self)
        self.IsSelectPic3.resize(25, 25)
        self.IsSelectPic3.move(916, 530)
        self.IsSelectPic3.stateChanged.connect(self.SelectPicture)
        self.IsSelectPic3.setCursor(Qt.PointingHandCursor)

        self.IsSelectPic4 = QCheckBox(' ', self)
        self.IsSelectPic4.resize(25, 25)
        self.IsSelectPic4.move(1149, 530)
        self.IsSelectPic4.stateChanged.connect(self.SelectPicture)
        self.IsSelectPic4.setCursor(Qt.PointingHandCursor)

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
        self.next = QPushButton("参数细化", self)
        self.next.resize(100, 50)
        self.next.move(550, 620)
        self.next.setFont(QFont("黑体"))
        self.next.setStyleSheet('color:rgb(255, 255, 255);font-size: 25px;background-color: transparent;')
        self.next.setCursor(Qt.PointingHandCursor)
            # 跳转到参数细化
        self.next.clicked.connect(self.Next)

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
        refresh.resize(60, 20)
        refresh.move(1100, 320)
        refresh.setFont(QFont("黑体"))
        refresh.setStyleSheet('color:rgb(150, 150, 150);font-size: 15px;background-color: transparent;')
        refresh.setCursor(Qt.PointingHandCursor)
            # 保存图片
        refresh.clicked.connect(self.refresh)

    #刷新的响应事件
    def refresh(self):
         #这里加生成图片的代码
         generate_background.generate_bg(0, bedroom_Gs, 0, 0)
         self.setPic()
        
        
    def backMain(self):
        self.newWindow = main.mainWindow()
        self.newWindow.show()
        self.close()

    def bedroomGenerate(self):
        self.Judge = 1 #flag,标记选择标签为卧室
        self.waitWin.show()
        self.wait()

    def operate(self):
        # 此处生成的代码
        #点击卧室选择模型
        global bedroom_Gs
        bedroom_Gs = generate_background.bg_select(0)
        #此处生成五张图片，type=0,latent置为0,返回5个latents数组
        #global latents_array
        #latents_array = generate_background.generate_bg(0, Gs, 0)
        generate_background.generate_bg(0, bedroom_Gs, 0, 0)
        self.timer.stop()
        self.waitWin.close()
        self.setPic()

    def wait(self):
        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.operate)  # 计时结束调用operate()方法
        self.timer.start(3000)  # 设置计时间隔并启动

    def forestGenerate(self):
        self.Judge = 2 #flag,标记选择标签为森林
        self.waitWin.show()
        self.wait()

    def skyGenerate(self):
        self.Judge = 3 #flag,标记选择标签为天空
        self.waitWin.show()
        self.wait()

    def auroraGenerate(self):
        self.Judge = 4 #flag,标记选择标签为极光
        self.waitWin.show()
        self.wait()

    def setPic(self):
        self.pic0.setPixmap(QPixmap("result_picture//0.png"))  # 修改显示的五张图片
        self.pic1.setPixmap(QPixmap("result_picture//1.png"))
        self.pic2.setPixmap(QPixmap("result_picture//2.png"))
        self.pic3.setPixmap(QPixmap("result_picture//3.png"))
        self.pic4.setPixmap(QPixmap("result_picture//4.png"))

    #进行参数细化
    def Next(self):
        if self.sum == 0:
             # 没有选中图片
             QMessageBox.about(self, "提示", "选中图片不能为空")
        if self.sum == 1:
            # 打开新窗口进行参数细化,并将选择的图片放入文件夹保存
            for i in range(0, 5):
                if self.PicArray[i] == True:
                    if i == 0:
                        self.image = QtGui.QPixmap("result_picture\\0.png").scaled(256, 256)
                        self.image.save("chosen_picture\\0.png")
                    if i == 1:
                        self.image = QtGui.QPixmap("result_picture\\1.png").scaled(256, 256)
                        self.image.save("chosen_picture\\1.png")
                    if i == 2:
                        self.image = QtGui.QPixmap("result_picture\\2.png").scaled(256, 256)
                        self.image.save("chosen_picture\\2.png")
                    if i == 3:
                        self.image = QtGui.QPixmap("result_picture\\3.png").scaled(256, 256)
                        self.image.save("chosen_picture\\3.png")
                    if i == 4:
                        self.image = QtGui.QPixmap("result_picture\\4.png").scaled(256, 256)
                        self.image.save("chosen_picture\\4.png")

            #此处没有填充完所有参数细化的界面
            if self.Judge == 1:
                self.newWindow = bedroom_bkgDetailWindow.bkgDetailWindow()
            #卧室的参数细化，还有其他的后续增加

            #史瑜君注意！！！如果点了非卧室其他的标签，由于上面没有初始化，下面的show函数会出错退出程序，所以要参数细化时就点卧室这个便签
            self.newWindow.show()
            self.close()
        if self.sum > 1:
            QMessageBox.about(self, "提示", "不能同时对多张图片进行操作")

    def save(self):
        QMessageBox.about(self, "提示", "确认保存所选人物素材？")
        for i in range(0, 5):
            if self.PicArray[i] == True:
                filename = QFileDialog.getSaveFileName(self, "选择图片保存位置", "", "*.png;;*.jpg;;*bmp;;All Files(*)")
                if i == 0:
                    self.image = QtGui.QPixmap("result_picture\\0.png").scaled(256, 256)
                    self.image.save(filename[0])
                if i == 1:
                    self.image = QtGui.QPixmap("result_picture\\1.png").scaled(256, 256)
                    self.image.save(filename[0])
                if i == 2:
                    self.image = QtGui.QPixmap("result_picture\\2.png").scaled(256, 256)
                    self.image.save(filename[0])
                if i == 3:
                    self.image = QtGui.QPixmap("result_picture\\3.png").scaled(256, 256)
                    self.image.save(filename[0])
                if i == 4:
                    self.image = QtGui.QPixmap("result_picture\\4.png").scaled(256, 256)
                    self.image.save(filename[0])


    # 每次选择一个图片，选择总数加一，取消选择则减一,将选择了哪些图片记录下来
    def SelectPicture(self, state):
        if state == Qt.Checked:
            self.sum = self.sum + 1;
        else:
            self.sum = self.sum - 1;
        if self.IsSelectPic0.isChecked():
            self.PicArray[0] = True
        else:
            self.PicArray[0] = False
        if self.IsSelectPic1.isChecked():
            self.PicArray[1] = True
        else:
            self.PicArray[1] = False
        if self.IsSelectPic2.isChecked():
            self.PicArray[2] = True
        else:
            self.PicArray[2] = False
        if self.IsSelectPic3.isChecked():
            self.PicArray[3] = True
        else:
            self.PicArray[3] = False
        if self.IsSelectPic4.isChecked():
            self.PicArray[4] = True
        else:
            self.PicArray[4] = False

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
        self.gif = QMovie('src/bkg-wait.gif')
        self.initUI()

    def initUI(self):
        self.resize(900, 675)
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
