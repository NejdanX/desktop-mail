# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'write_message_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_write_message_form(object):
    def setupUi(self, write_message_form):
        write_message_form.setObjectName("write_message_form")
        write_message_form.resize(759, 559)
        write_message_form.setStyleSheet("QWidget#write_message_form {background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:1 rgba(0, 0, 128, 255));;}\n"
"QWidget#write_message_form {border: 1px solid orange;}")
        self.gridLayout = QtWidgets.QGridLayout(write_message_form)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(write_message_form)
        self.label.setStyleSheet("font: 14pt \"MS Serif\";\n"
"color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.input_receiver = QtWidgets.QLineEdit(write_message_form)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.input_receiver.setFont(font)
        self.input_receiver.setObjectName("input_receiver")
        self.gridLayout.addWidget(self.input_receiver, 1, 1, 1, 1)
        self.lbl_error = QtWidgets.QLabel(write_message_form)
        self.lbl_error.setStyleSheet("color: rgb(255, 0, 0);\n"
"font: 14pt \"MS Serif\";")
        self.lbl_error.setText("")
        self.lbl_error.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_error.setObjectName("lbl_error")
        self.gridLayout.addWidget(self.lbl_error, 5, 0, 1, 2)
        self.input_title = QtWidgets.QLineEdit(write_message_form)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.input_title.setFont(font)
        self.input_title.setObjectName("input_title")
        self.gridLayout.addWidget(self.input_title, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(write_message_form)
        self.label_2.setStyleSheet("font: 14pt \"MS Serif\";\n"
"color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.write_message = QtWidgets.QTextBrowser(write_message_form)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        self.write_message.setFont(font)
        self.write_message.setReadOnly(False)
        self.write_message.setObjectName("write_message")
        self.gridLayout.addWidget(self.write_message, 2, 0, 1, 2)
        self.btn_send_message = QtWidgets.QPushButton(write_message_form)
        self.btn_send_message.setStyleSheet("font: 14pt \"MS Serif\";\n"
"background-color: rgb(0, 170, 0);")
        self.btn_send_message.setObjectName("btn_send_message")
        self.gridLayout.addWidget(self.btn_send_message, 4, 0, 1, 2)

        self.retranslateUi(write_message_form)
        QtCore.QMetaObject.connectSlotsByName(write_message_form)

    def retranslateUi(self, write_message_form):
        _translate = QtCore.QCoreApplication.translate
        write_message_form.setWindowTitle(_translate("write_message_form", "Form"))
        self.label.setText(_translate("write_message_form", "Тема"))
        self.label_2.setText(_translate("write_message_form", "Получатель"))
        self.write_message.setHtml(_translate("write_message_form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Tahoma\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p></body></html>"))
        self.btn_send_message.setText(_translate("write_message_form", "Отправить письмо"))
