import os
import sys

d = os.path.dirname(__file__)
__path = os.path.dirname(d)
sys.path.append(__path) # 添加自己指定的搜索路径

import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtGui import QPixmap, QGuiApplication
from PyQt5.QtCore import Qt, QUrl, QEvent,QObject,pyqtSignal,pyqtSlot
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import *




from mypy2neo import search
from gui.Ui_neo4j import Ui_Form
from myLib import myLib



class channel_showNode(QObject):
    fromJS = pyqtSignal(str)
    toJS = pyqtSignal(str)
    def __init__(self, parent = None):
        super().__init__(parent)

    @pyqtSlot(str)
    def JSSendMessage(self, strParameter):
        print('showNode(%s) from Html' %strParameter)
        self.fromJS.emit(strParameter)

class channel_expandNode(QObject):
    fromJS = pyqtSignal(str)
    toJS = pyqtSignal(str)
    def __init__(self, parent = None):
        super().__init__(parent)

    @pyqtSlot(str)
    def JSSendMessage(self, strParameter):
        print('showNode(%s) from Html' %strParameter)
        self.fromJS.emit(strParameter)


class neo4j(QtWidgets.QWidget):
    ToJS_showNode = pyqtSignal(str)
    ToJS_expandNode = pyqtSignal(str)
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
        #------js和qt通信--------------------------



        self.channel_expandNode = channel_expandNode(self)
        self.pWebChannel.registerObject('channel_expandNode',self.channel_expandNode)

        self.channel_showNode = channel_showNode(self)
        self.pWebChannel.registerObject("channel_showNode",self.channel_showNode) 

        self.browser.page().setWebChannel(self.pWebChannel)
 
        #self.url = 'file:///F:/demo/now/static/html/JSTest.html'
        self.url = 'file:///' + os.path.dirname(os.path.dirname(d)) +\
       '/static/html/show.html'
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


        self.channel_showNode.fromJS.connect(self.returnShowNode)
        self.ToJS_showNode.connect(self.channel_showNode.toJS)
        self.channel_expandNode.fromJS.connect(self.returnExpandNode)
        self.ToJS_expandNode.connect(self.channel_expandNode.toJS)

    def returnShowNode(self,strParameter):
        if not strParameter:
            return
        a = search.search_return(strParameter)
        self.ToJS_showNode.emit(a.singleNode_json())

    def returnExpandNode(self,strParameter):
        if not strParameter:
            return
        a = search.search_return(strParameter)
        print("expandNode")
        print(a.json())
        self.__createSearch(a.dict())

        self.__draw(a.picture_path())
        self.ToJS_expandNode.emit(a.json())
        



#-------------------------------------------------------------
   
    def __draw(self, picture_path):
        if not picture_path:
            picture_path = self.defaultPicture
        else:
            picture_path = picture_path[0]
        self.ui.Picture.clear()
        pic = QPixmap(picture_path)
        self.ui.Picture.setPixmap(pic)


    def __pictureSizeChange(self):
        self.ui.Picture.resize(self.ui.LabelWidget.size())

    def resizeEvent(self, event):   
        self.ui.Picture.resize(self.ui.LabelWidget.size())
        

    def __createSearch(self, dic):
        self.ui.table_sql.setColumnCount(len(dic))
        self.ui.table_sql.setRowCount(1)
        self.ui.table_sql.setHorizontalHeaderLabels(dic.keys())

        i = 0
        for dictKey in dic.keys():
            newItem = QtWidgets.QTableWidgetItem(dic[dictKey])
            self.ui.table_sql.setItem(0,i,newItem)
            i += 1





    def on_btnConfirms_clicked(self): 
        search_name = self.ui.Check_lineEdit.text()

        self.neo = search.search_return(search_name)
        node_dict = self.neo.dict()
        print(node_dict)
        if node_dict:
            self.__createSearch(node_dict)
            self.__draw(self.neo.picture_path())
            self.ToJS_showNode.emit(self.neo.singleNode_json())




if __name__ == "__main__":
    import sys
    qapp = QtWidgets.QApplication(sys.argv)
    app = neo4j()
    app.show()
    sys.exit(qapp.exec_())