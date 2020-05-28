
from PyQt5.QtWidgets import QDialog, QPlainTextEdit, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import *
from PyQt5.QtCore import QUrl, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication
import sys


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
 
class TMainWindow(QDialog):
    SigSendMessageToJS = pyqtSignal(str)
    def __init__(self, parent = None):
        super().__init__(parent)
        #---Qt widget and layout---
        self.text = QPlainTextEdit(self)
        self.text.setMidLineWidth(200)
        self.text.setReadOnly(True)
 
        self.line = QLineEdit(self)
 
        self.button1 = QPushButton('Send', self)
        self.button1.setToolTip('Send message by Interact object style')
 
        self.button2 = QPushButton('Send2', self)
        self.button2.setToolTip('Send message by runJavaScript style')
 
        self.pQtSendHLayout = QHBoxLayout()
        self.pQtSendHLayout.setSpacing(0)
        self.pQtSendHLayout.addWidget(self.line)
        self.pQtSendHLayout.addSpacing(5)
        self.pQtSendHLayout.addWidget(self.button1)
        self.pQtSendHLayout.addSpacing(5)
        self.pQtSendHLayout.addWidget(self.button2)
 
        self.pQtTotalVLayout = QVBoxLayout()
        self.pQtTotalVLayout.setSpacing(0)
        self.pQtTotalVLayout.addWidget(self.text)
        self.pQtTotalVLayout.setSpacing(5)
        self.pQtTotalVLayout.addLayout(self.pQtSendHLayout)
 
        self.pQtGroup = QGroupBox('Qt View', self)
        self.pQtGroup.setLayout(self.pQtTotalVLayout)
 
        #---Web widget and layout---
        self.browser = QWebEngineView(self)
        self.pWebChannel = QWebChannel(self.browser.page())
        self.pInteractObj = TInteractObj(self)
        self.pWebChannel.registerObject("interactObj", self.pInteractObj)
 
        self.browser.page().setWebChannel(self.pWebChannel)
 
        self.url = 'file:///F:/demo/now/static/html/JSTest.html'
        self.browser.page().load(QUrl(self.url))
        self.browser.show()
 
        self.pJSTotalVLayout = QVBoxLayout()
        self.pJSTotalVLayout.setSpacing(0)
        self.pJSTotalVLayout.addWidget(self.browser)
        self.pWebGroup = QGroupBox('Web View', self)
        self.pWebGroup.setLayout(self.pJSTotalVLayout)
 
        #---TMainWindow total layout---
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.addWidget(self.pQtGroup)
        self.mainLayout.setSpacing(5)
        self.mainLayout.addWidget(self.pWebGroup)
        self.setLayout(self.mainLayout)
        self.setMinimumSize(1130, 680)
 
        self.button1.clicked.connect(self.OnSendMessageByInteractObj)
        self.button2.clicked.connect(self.OnSendMessageByJavaScript)
        self.pInteractObj.SigReceivedMessFromJS.connect(self.OnReceiveMessageFromJS)
        self.SigSendMessageToJS.connect(self.pInteractObj.SigSendMessageToJS)
 
    def OnReceiveMessageFromJS(self, strParameter):
        print('OnReceiveMessageFromJS()')
        if not strParameter:
            return
        self.text.appendPlainText(strParameter)
 
    def OnSendMessageByInteractObj(self):
        strMessage = self.line.text()
        if not strMessage:
            return
        self.SigSendMessageToJS.emit(strMessage)
 
    def OnSendMessageByJavaScript(self):
        strMessage = self.line.text()
        if not strMessage:
            return
        strMessage = 'Received string from Qt:' + strMessage
        self.browser.page().runJavaScript("output(%s)" %strMessage)
        self.browser.page().runJavaScript("showAlert()")

if __name__ == '__main__':
    app = QApplication(sys.argv)
 
    dlg = TMainWindow()
    dlg.show()
 
    app.exec_()