from  PyQt4 import QtCore ,QtGui
import cv2
import sys
import os
from socket import *
host = "0.0.0.0"
port = 4040
buf = 1024
addr = (host, port)
fName = 'img.jpg'
timeOut = 0.05
class videoThread(QtCore.QThread):
    changePixmap = QtCore.pyqtSignal(str)
    def __init__(self):
        super(videoThread,self).__init__()


    def run(self):
        print "thread started......"
        while True:
            s = socket(AF_INET, SOCK_DGRAM)
            s.bind(addr)

            data, address = s.recvfrom(buf)
            f = open(data, 'wb')

            data, address = s.recvfrom(buf)

            try:
                while (data):
                    f.write(data)
                    s.settimeout(timeOut)
                    data, address = s.recvfrom(buf)
            except timeout:
                f.close()
                s.close()
            image_path = os.path.join(os.getcwd(), fName)

            self.changePixmap.emit(image_path )



class Controller(QtGui.QWidget ):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        print "aaa"
        self.gridLayout = QtGui.QGridLayout()
        self.webBrowsser = QtGui.QLabel(self)
        self.webBrowsser.setScaledContents(True)
        self.gridLayout.addWidget(self.webBrowsser)
        self.video = videoThread()
        self.video.changePixmap.connect(self.setFrame)
        self.video.start()
        self.setLayout(self.gridLayout)
        self.show()

    def setFrame(self, image_path):
        convertToQtFormat = QtGui.QPixmap(image_path)
        frame = convertToQtFormat.scaled(640, 480, QtCore.Qt.KeepAspectRatio)

        self.webBrowsser.setPixmap(frame)


app_ = QtGui.QApplication( sys.argv)
temp = Controller()
app_.exec_()
