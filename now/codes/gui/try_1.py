import os
import sys

d = os.path.dirname(__file__)
__path = os.path.dirname(d)
sys.path.append(__path) # 添加自己指定的搜索路径

import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtGui import QPixmap, QGuiApplication
from PyQt5.QtCore import Qt, QUrl, QEvent,QObject,pyqtSignal,pyqtSlot
import PyQt5.QtWebEngineWidgets as WebEngine
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import *



from mypy2neo import search
from Ui_neo4j import Ui_Form
from myLib import myLib


class TInteractObj(QObject):
    SigReceivedMessFromJS = pyqtSignal(str)
    SigSendMessageToJS = pyqtSignal(str)
    def __init__(self, parent = None):
        super().__init__(parent)

    @pyqtSlot(str)
    def JSSendMessage(self, strParameter):
        print('JSSendMessage(%s) from Html' %strParameter)
        self.SigReceivedMessFromJS.emit(strParameter)
 
    @pyqtSlot(result=str)
    def fun(self):

        print('TInteractObj.fun()')
        return 'hello'


class neo4j(QtWidgets.QWidget):
    SigSendMessageToJS = pyqtSignal(str)
    def __init__(self, parent = None):

        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.resize(QGuiApplication.primaryScreen().availableSize() * 4 / 5);

        self.defaultPicture = os.path.dirname(os.path.dirname(d)) + \
        "\\static\\pictures\\1.gif"

        self.__setlayout()

        self.splitterV1.splitterMoved.connect(self.__pictureSizeChange)

        self.splitter.splitterMoved.connect(self.__pictureSizeChange)

        self.__draw(self.defaultPicture)


    def __setlayout(self):
        layout = QtWidgets.QHBoxLayout()
        self.splitterV1 = QtWidgets.QSplitter(self)
        self.splitterV1.setOrientation(Qt.Vertical)

        self.splitterV1.addWidget(self.ui.SqlToolBox)
        self.splitterV1.addWidget(self.ui.LabelWidget)
#        self.url = 'file:///' + os.path.dirname(os.path.dirname(d)) +\
 #       '/static/html/JSTest.html'

         #---Web widget and layout-------------------------
        self.browser = QWebEngineView(self)
        self.pWebChannel = QWebChannel(self.browser.page())
        self.pInteractObj = TInteractObj(self)
        self.pWebChannel.registerObject("interactObj", self.pInteractObj)
 
        self.browser.page().setWebChannel(self.pWebChannel)
 
        #self.url = 'file:///F:/demo/now/static/html/JSTest.html'
        self.url = 'file:///' + os.path.dirname(os.path.dirname(d)) +\
       '/static/html/show_1.html'
       	self.url = self.url.replace('\\','/')
        self.browser.page().load(QUrl(self.url))
        self.browser.show()
#------------------------------------------------------------------------------
       # self.url = 'file:///F:/demo/now`/static/html/JSTest.html'
        
        #self.url = self.url.replace('\\','/')
        #print("self.url = ",self.url)

        #self.browser = QWebEngineView()
        #self.browser.load(QUrl(self.url))
        
        self.splitterV2 = QtWidgets.QSplitter(self)
        self.splitterV2.setOrientation(Qt.Vertical)
        self.splitterV2.addWidget(self.browser)
        self.splitterV2.addWidget(self.ui.table_sql)

        self.splitter = QtWidgets.QSplitter(self)
        self.splitter.setOrientation(Qt.Horizontal) 
        self.splitter.addWidget(self.splitterV1)
        self.splitter.addWidget(self.splitterV2)
        layout.addWidget(self.splitter)
        self.setLayout(layout)

        #---------------------------------


        self.pInteractObj.SigReceivedMessFromJS.connect(self.OnReceiveMessageFromJS)
        self.SigSendMessageToJS.connect(self.pInteractObj.SigSendMessageToJS)
 
    def OnReceiveMessageFromJS(self, strParameter):
        print('OnReceiveMessageFromJS()')
        if not strParameter:
            return
        print("get str " + strParameter)


#-------------------------------------------------------------
   
    def __draw(self, picture_path):
        self.ui.Picture.clear()
        pic = QPixmap(picture_path)
        self.ui.Picture.setPixmap(pic)


    def __pictureSizeChange(self):
        self.ui.Picture.resize(self.ui.LabelWidget.size())

    def resizeEvent(self, event):   
        self.ui.Picture.resize(self.ui.LabelWidget.size())
        

    def __createSearch(self, dic):

        i = 0
        for dictKey in dic.keys():
            newItem = QtWidgets.QTableWidgetItem(dic[dictKey])
            self.ui.table_sql.setItem(0,i,newItem)
            i += 1
    def __pushJsonToJs(self,json):

            self.SigSendMessageToJS.emit(json)




    def on_btnConfirms_clicked(self): 
        search_name = self.ui.Check_lineEdit.text()

        self.neo = search.search_return(search_name)
        node_dict = self.neo.dict()
        print(node_dict)
        if node_dict:
            self.ui.table_sql.setColumnCount(len(node_dict))
            self.ui.table_sql.setRowCount(1)
            self.ui.table_sql.setHorizontalHeaderLabels(node_dict.keys())
            self.__createSearch(node_dict)
        picPath = self.neo.picture_path()[0] if\
        self.neo.picture_path()\
        else self.defaultPicture
        print('picpath = ',picPath)
        self.__draw(picPath)
        self.__pushJsonToJs(self.neo.json())




if __name__ == "__main__":
    import sys
    qapp = QtWidgets.QApplication(sys.argv)
    app = neo4j()
    app.show()
    sys.exit(qapp.exec_())