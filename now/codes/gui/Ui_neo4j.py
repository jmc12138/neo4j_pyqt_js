# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\codes\project\code\gui\neo4j.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(707, 461)
        self.SqlToolBox = QtWidgets.QToolBox(Form)
        self.SqlToolBox.setGeometry(QtCore.QRect(10, 20, 241, 191))
        self.SqlToolBox.setObjectName("SqlToolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 241, 101))
        self.page.setObjectName("page")
        self.gridLayout = QtWidgets.QGridLayout(self.page)
        self.gridLayout.setObjectName("gridLayout")
        self.btnConfirms = QtWidgets.QPushButton(self.page)
        self.btnConfirms.setObjectName("btnConfirms")
        self.gridLayout.addWidget(self.btnConfirms, 1, 0, 1, 1)
        self.Check_lineEdit = QtWidgets.QLineEdit(self.page)
        self.Check_lineEdit.setObjectName("Check_lineEdit")
        self.gridLayout.addWidget(self.Check_lineEdit, 0, 0, 1, 1)
        self.SqlToolBox.addItem(self.page, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 241, 101))
        self.page_2.setObjectName("page_2")
        self.SqlToolBox.addItem(self.page_2, "")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 241, 101))
        self.page_3.setObjectName("page_3")
        self.SqlToolBox.addItem(self.page_3, "")
        self.table_sql = QtWidgets.QTableWidget(Form)
        self.table_sql.setGeometry(QtCore.QRect(350, 240, 256, 192))
        self.table_sql.setObjectName("table_sql")
        self.table_sql.setColumnCount(0)
        self.table_sql.setRowCount(0)
        self.LabelWidget = QtWidgets.QWidget(Form)
        self.LabelWidget.setGeometry(QtCore.QRect(10, 230, 271, 181))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LabelWidget.sizePolicy().hasHeightForWidth())
        self.LabelWidget.setSizePolicy(sizePolicy)
        self.LabelWidget.setObjectName("LabelWidget")
        self.Picture = QtWidgets.QLabel(self.LabelWidget)
        self.Picture.setGeometry(QtCore.QRect(0, 0, 72, 15))
        self.Picture.setText("")
        self.Picture.setScaledContents(True)
        self.Picture.setObjectName("Picture")

        self.retranslateUi(Form)
        self.SqlToolBox.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btnConfirms.setText(_translate("Form", "确认"))
        self.SqlToolBox.setItemText(self.SqlToolBox.indexOf(self.page), _translate("Form", "查找"))
        self.SqlToolBox.setItemText(self.SqlToolBox.indexOf(self.page_2), _translate("Form", "新建"))
        self.SqlToolBox.setItemText(self.SqlToolBox.indexOf(self.page_3), _translate("Form", "删除"))
