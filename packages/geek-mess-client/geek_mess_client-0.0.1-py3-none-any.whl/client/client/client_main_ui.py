# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_main_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ClientMainWindow(object):
    def setupUi(self, ClientMainWindow):
        ClientMainWindow.setObjectName("ClientMainWindow")
        ClientMainWindow.resize(714, 563)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ClientMainWindow.sizePolicy().hasHeightForWidth())
        ClientMainWindow.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        ClientMainWindow.setPalette(palette)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("balloon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ClientMainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(ClientMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 691, 501))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.labelContactsList = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelContactsList.setFont(font)
        self.labelContactsList.setObjectName("labelContactsList")
        self.gridLayout.addWidget(self.labelContactsList, 0, 0, 1, 2)
        self.labelHistoryMessages = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelHistoryMessages.setFont(font)
        self.labelHistoryMessages.setObjectName("labelHistoryMessages")
        self.gridLayout.addWidget(self.labelHistoryMessages, 0, 4, 1, 2)
        self.listViewContacts = QtWidgets.QListView(self.layoutWidget)
        self.listViewContacts.setObjectName("listViewContacts")
        self.gridLayout.addWidget(self.listViewContacts, 1, 0, 4, 3)
        spacerItem = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 3, 1, 1)
        self.listViewMessages = QtWidgets.QListView(self.layoutWidget)
        self.listViewMessages.setObjectName("listViewMessages")
        self.gridLayout.addWidget(self.listViewMessages, 1, 4, 1, 3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 17, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 5, 1, 1)
        self.labelNewMessage = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelNewMessage.setFont(font)
        self.labelNewMessage.setObjectName("labelNewMessage")
        self.gridLayout.addWidget(self.labelNewMessage, 3, 4, 1, 3)
        spacerItem2 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 4, 3, 1, 1)
        self.textEditMessage = QtWidgets.QTextEdit(self.layoutWidget)
        self.textEditMessage.setObjectName("textEditMessage")
        self.gridLayout.addWidget(self.textEditMessage, 4, 4, 1, 3)
        self.pushButtonAddContact = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButtonAddContact.setFont(font)
        self.pushButtonAddContact.setObjectName("pushButtonAddContact")
        self.gridLayout.addWidget(self.pushButtonAddContact, 5, 0, 1, 1)
        self.pushButtonDelContact = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButtonDelContact.setFont(font)
        self.pushButtonDelContact.setObjectName("pushButtonDelContact")
        self.gridLayout.addWidget(self.pushButtonDelContact, 5, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(128, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 5, 2, 1, 3)
        self.pushButtonClearMessage = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButtonClearMessage.setFont(font)
        self.pushButtonClearMessage.setObjectName("pushButtonClearMessage")
        self.gridLayout.addWidget(self.pushButtonClearMessage, 5, 5, 1, 1)
        self.pushButtonSendMessage = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButtonSendMessage.setFont(font)
        self.pushButtonSendMessage.setObjectName("pushButtonSendMessage")
        self.gridLayout.addWidget(self.pushButtonSendMessage, 5, 6, 1, 1)
        ClientMainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(ClientMainWindow)
        self.statusbar.setObjectName("statusbar")
        ClientMainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(ClientMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 714, 21))
        self.menubar.setObjectName("menubar")
        self.file = QtWidgets.QMenu(self.menubar)
        self.file.setObjectName("file")
        self.contacts = QtWidgets.QMenu(self.menubar)
        self.contacts.setObjectName("contacts")
        ClientMainWindow.setMenuBar(self.menubar)
        self.actionAddContact = QtWidgets.QAction(ClientMainWindow)
        self.actionAddContact.setObjectName("actionAddContact")
        self.actionDelContact = QtWidgets.QAction(ClientMainWindow)
        self.actionDelContact.setObjectName("actionDelContact")
        self.actionExit = QtWidgets.QAction(ClientMainWindow)
        self.actionExit.setObjectName("actionExit")
        self.file.addAction(self.actionExit)
        self.contacts.addAction(self.actionAddContact)
        self.contacts.addAction(self.actionDelContact)
        self.menubar.addAction(self.file.menuAction())
        self.menubar.addAction(self.contacts.menuAction())

        self.retranslateUi(ClientMainWindow)
        QtCore.QMetaObject.connectSlotsByName(ClientMainWindow)

    def retranslateUi(self, ClientMainWindow):
        _translate = QtCore.QCoreApplication.translate
        ClientMainWindow.setWindowTitle(_translate("ClientMainWindow", "Программа чат"))
        self.labelContactsList.setText(_translate("ClientMainWindow", "Список контактов:"))
        self.labelHistoryMessages.setText(_translate("ClientMainWindow", "История сообщений:"))
        self.labelNewMessage.setText(_translate("ClientMainWindow", "Введите новое сообщение:"))
        self.pushButtonAddContact.setText(_translate("ClientMainWindow", "Добавить контакт"))
        self.pushButtonDelContact.setText(_translate("ClientMainWindow", "Удалить контакт"))
        self.pushButtonClearMessage.setText(_translate("ClientMainWindow", "Очистить поле"))
        self.pushButtonSendMessage.setText(_translate("ClientMainWindow", "Отправить сообщение"))
        self.file.setTitle(_translate("ClientMainWindow", "Файл"))
        self.contacts.setTitle(_translate("ClientMainWindow", "Контакты"))
        self.actionAddContact.setText(_translate("ClientMainWindow", "Добавить контакт"))
        self.actionDelContact.setText(_translate("ClientMainWindow", "Удалить контакт"))
        self.actionExit.setText(_translate("ClientMainWindow", "Выход"))
