import os
import sys

d = os.path.dirname(__file__)
__path = os.path.dirname(d)
sys.path.append(__path) # 添加自己指定的搜索路径

import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,QUrl
import PyQt5.QtWebEngineWidgets as WebEngine

from mypy2neo import search
from Ui_neo4j import Ui_Form


class neo4j(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.defaultPicture = os.path.abspath(r"..\..\static\pictures\1.gif")

        self.__setlayout()


    def __setlayout(self):
        layout = QtWidgets.QHBoxLayout()
        splitterV1 = QtWidgets.QSplitter(self)
        splitterV1.setOrientation(Qt.Vertical)

        self.scene = QtWidgets.QGraphicsScene()
        self.ui.PictureView.setScene(self.scene)
        wid = self.ui.PictureView.width()
        height = self.ui.PictureView.height()
        picture = QPixmap(self.defaultPicture)
        picture.scaled(wid,height)
        self.scene.addPixmap(picture)

        splitterV1.addWidget(self.ui.SqlToolBox)
        splitterV1.addWidget(self.ui.PictureView)

        self.url = 'file:///' +os.path.abspath\
        ('../../static/html/show.html').replace('\\','/')
        #self.url = 'file:///C:/Users/Administrator/Desktop/界面/test.html'

        self.browser = WebEngine.QWebEngineView()
        self.browser.load(QUrl(self.url))
        
        splitterV2 = QtWidgets.QSplitter(self)
        splitterV2.setOrientation(Qt.Vertical)
        splitterV2.addWidget(self.browser)
        splitterV2.addWidget(self.ui.table_sql)

        splitter = QtWidgets.QSplitter(self)
        splitter.setOrientation(Qt.Horizontal)
        splitter.addWidget(splitterV1)
        splitter.addWidget(splitterV2)

        layout.addWidget(splitter)
        self.setLayout(layout)
   
    def __createSearch(self, dic):

        i = 0
        for dictKey in dic.keys():
            newItem = QtWidgets.QTableWidgetItem(dic[dictKey])
            self.ui.table_sql.setItem(0,i,newItem)
            i += 1

        picture = QPixmap(self.neo.picture_path()[0]) if\
                    self.neo.picture_path()\
                    else QPixmap(self.defaultPicture)


        wid = self.ui.PictureView.width()
        height = self.ui.PictureView.height()
        picture.scaled(wid,height)
        self.scene.addPixmap(picture)


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
        

if __name__ == "__main__":
    import sys
    qapp = QtWidgets.QApplication(sys.argv)
    app = neo4j()
    app.show()
    sys.exit(qapp.exec_())