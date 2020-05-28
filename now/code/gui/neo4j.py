import os
import sys

d = os.path.dirname(__file__)
__path = os.path.dirname(d)
sys.path.append(__path) # 添加自己指定的搜索路径

import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtGui import QPixmap, QGuiApplication
from PyQt5.QtCore import Qt, QUrl, QEvent
import PyQt5.QtWebEngineWidgets as WebEngine

from mypy2neo import search
from Ui_neo4j import Ui_Form


class neo4j(QtWidgets.QWidget):
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
        self.url = 'file:///' + os.path.dirname(os.path.dirname(d)) +\
        '/static/html/show_1.html'
        self.url = self.url.replace('\\','/')
        print("self.url = ",self.url)

        self.browser = WebEngine.QWebEngineView()
        self.browser.load(QUrl(self.url))
        
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




if __name__ == "__main__":
    import sys
    qapp = QtWidgets.QApplication(sys.argv)
    app = neo4j()
    app.show()
    sys.exit(qapp.exec_())