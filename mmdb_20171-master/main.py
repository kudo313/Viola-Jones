import sys
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot, QRect, Qt
from numpy import size

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
on = True


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        destopSize = QDesktopWidget().screenGeometry()
        w, h = destopSize.width(), destopSize.height()
        self.setGeometry(w / 2 - 300, h / 2 - 250, 700, 500)
        self.setWindowTitle("Face Detection")

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabImage = QWidget()
        self.tabVideo = QWidget()
        self.tabWebcam = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tabImage, "Image")

        # Create TAB IMAGE
        # Create textbox to get path of image
        self.imagePathI = QLineEdit(self.tabImage)
        self.imagePathI.setGeometry(QRect(20, 30, 450, 30))

        # Create load Button to load image
        self.loadButtonI = QPushButton("Load", self.tabImage)
        self.loadButtonI.setGeometry(QRect(500, 30, 100, 30))
        self.loadButtonI.clicked.connect(self.loadImage)

        # Create box to show image
        self.imageView = QGraphicsView(self.tabImage)
        self.imageView.setGeometry(QRect(20, 80, 450, 360))

        # Create form to get parametes
        self.scaleLabelI = QLabel("Scale Factor:", self.tabImage)
        self.scaleLabelI.setGeometry(QRect(500, 130, 100, 30))
        self.sl = QSlider(Qt.Horizontal, self.tabImage)
        self.sl.setGeometry(QRect(500, 100, 150, 30))
        self.sl.setMinimum(100)
        self.sl.setMaximum(300)
        self.sl.setValue(100)
        self.sl.setTickPosition(QSlider.TicksBelow)
        self.sl.setTickInterval(5)
        self.sl.valueChanged.connect(self.valuechange1)

        self.l1 = QLabel("0", self.tabImage)
        self.l1.setGeometry(QRect(590, 130, 150, 30))

        self.MinNeighborLabelI = QLabel("Min Neighbor:", self.tabImage)
        self.MinNeighborLabelI.setGeometry(QRect(500, 200, 100, 30))
        self.minNeighborSpinBoxI =  QSlider(Qt.Horizontal, self.tabImage)
        self.minNeighborSpinBoxI.setGeometry(QRect(500, 180, 150, 30))
        self.minNeighborSpinBoxI.setMinimum(0)
        self.minNeighborSpinBoxI.setMaximum(50)
        self.minNeighborSpinBoxI.setValue(0)
        self.minNeighborSpinBoxI.setTickPosition(QSlider.TicksBelow)
        self.minNeighborSpinBoxI.setTickInterval(10)
        self.minNeighborSpinBoxI.valueChanged.connect(self.valuechange2)

        self.l2 = QLabel("0", self.tabImage)
        self.l2.setGeometry(QRect(590, 200, 150, 30))

        if self.imageView.width() > self.imageView.height():
            sizz = self.imageView.height()
        else:
            sizz = self.imageView.width() 
        self.minSizeSlide = QSlider(Qt.Horizontal, self.tabImage)
        self.minSizeSlide.setGeometry(QRect(500, 250, 150, 30))
        self.minSizeSlide.setMinimum(0)
        self.minSizeSlide.setMaximum(sizz)
        self.minSizeSlide.setValue(20)
        self.minSizeSlide.setTickPosition(QSlider.TicksBelow)
        self.minSizeSlide.setTickInterval(20)
        self.minSizeLabel = QLabel("Min Size: ", self.tabImage)
        self.minSizeLabel.setGeometry(QRect(500, 280, 100, 30))
        self.minSizeSlide.valueChanged.connect(self.valuechange3)

        self.l3 = QLabel("0", self.tabImage)
        self.l3.setGeometry(QRect(590, 280, 150, 30))

        self.maxSizeSlide = QSlider(Qt.Horizontal, self.tabImage)
        self.maxSizeSlide.setGeometry(QRect(500, 330, 150, 30))
        self.maxSizeSlide.setMinimum(0)
        self.maxSizeSlide.setMaximum(sizz)
        self.maxSizeSlide.setValue(20)
        self.maxSizeSlide.setTickPosition(QSlider.TicksBelow)
        self.maxSizeSlide.setTickInterval(100)
        self.maxSizeLabbel = QLabel("Max Size: ", self.tabImage)
        self.maxSizeLabbel.setGeometry(QRect(500, 360, 100, 30))
        self.maxSizeSlide.valueChanged.connect(self.valuechange4)

        self.l4 = QLabel("0", self.tabImage)
        self.l4.setGeometry(QRect(590, 360, 150, 30))


        # Create button to Detect
        self.detectButtonI = QPushButton("Detect", self.tabImage)
        self.detectButtonI.setGeometry(QRect(550, 400, 100, 30))
        self.detectButtonI.clicked.connect(self.detectOfImage)

        # self.grayButton = QPushButton("GrayImg", self.tabImage)
        # self.grayButton.setGeometry(QRect(550, 430, 100, 30))
        # self.grayButton.clicked.connect(self.showImgGray)

        # END IMAGE TAB

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        

    @pyqtSlot()
    def loadImage(self):
        dialog = QFileDialog()
        folder_path, _ = dialog.getOpenFileName(options=QFileDialog.Options())
        self.imagePathI.setText(folder_path)
        image_reader = QImageReader(self.imagePathI.text())
        print(folder_path)
        if image_reader.canRead() is True:
            widget_height = self.imageView.height()
            widget_width = self.imageView.width()
            image = image_reader.read().scaled(widget_width, widget_height, Qt.KeepAspectRatio)
            item = QGraphicsPixmapItem(QPixmap.fromImage(image))
            scene = QGraphicsScene()
            scene.addItem(item)
            self.imageView.setScene(scene)
        else:
            scene = QGraphicsScene()
            self.imageView.setScene(scene)

    def showImgGray(self):
        path = self.imagePathI.text()
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imshow('img', gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def valuechange1(self):
        size = self.sl.value()
        self.l1.setText(str(size/100))

    def valuechange2(self):
        size = self.minNeighborSpinBoxI.value()
        self.l2.setText(str(size))

    def valuechange3(self):
        size = self.minSizeSlide.value()
        self.l3.setText(str(size))

    def valuechange4(self):
        size = self.maxSizeSlide.value()
        self.l4.setText(str(size))

    def detectOfImage(self):
        path = self.imagePathI.text()
        s = self.sl.value()/100
        m = self.minNeighborSpinBoxI.value()
        minSize = (self.minSizeSlide.value(), self.minSizeSlide.value())
        maxSize = (self.maxSizeSlide.value(), self.maxSizeSlide.value())
        img = cv2.imread(path)
        width = int(img.shape[1])
        height = int(img.shape[0])
        # per_width = width/500
        # per_height = height/500
        # if per_width > per_height:
        #     dim = (int(width/per_width), int(height/per_width))
        # else:
        #     dim = (int(width/per_height), int(height/per_height))

        # img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, s, m, minSize= minSize, maxSize= maxSize)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imwrite('result.png', img)
        winname = "Test"
        destopSize = QDesktopWidget().screenGeometry()
        w, h = destopSize.width(), destopSize.height()
        cv2.namedWindow(winname)
        x = int(w/2 - width/2)
        y = int(h/2 - height/2)
        cv2.moveWindow(winname, x, y)  # Move it to (40,30)
        cv2.imshow(winname, img)
        # cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # self.detect_face(path,"a",s,m)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
