from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog
from static.Forms.password_dialog_form import Ui_RecoveryPassword
from PyQt5.QtCore import Qt
from Constants import DB_FILE_NAME
import Password
import sqlite3
import sys


class RecoveryPasswordDialog(QWidget, Ui_RecoveryPassword):
    def __init__(self, user='', without_question=False):
        super(RecoveryPasswordDialog, self).__init__()
        self.is_exit = 'ok'
        self.user = user
        self.con = sqlite3.connect(DB_FILE_NAME)
        if not without_question:
            self.is_exit = self.secret_question()
        self.setupUi(self)
        self.btn_enter.clicked.connect(self.check_password)

    def secret_question(self):
        """Восстановить пароль через секретный вопрос"""
        cur = self.con.cursor()
        input_user = QInputDialog(self)
        input_user.setFixedSize(400, 300)
        input_user.setWindowTitle('Recovery password')
        input_user.setLabelText('Введите ваш логин')
        input_user.exec_()
        self.user = input_user.textValue()
        user_question = cur.execute('''
                                SELECT COUNT(Login), Secret_question, Answer FROM User
                                    WHERE Login = ?''', (self.user.lower(),)).fetchall()
        if not user_question[0][0]:
            return 'Exit: unknown user'
        input_answer = QInputDialog(self)
        input_answer.setFixedSize(400, 300)
        input_answer.setWindowTitle('Recovery password')
        input_answer.setLabelText(user_question[0][1])
        ok_answer = input_answer.exec_()
        answer = input_answer.textValue()
        if ok_answer and answer == user_question[0][2]:
            return 'ok'
        else:
            return 'Exit: wrong answer'

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F1:  # Установка echoMode для пароля
            if self.input_password.echoMode() == self.input_password.Password:
                self.input_password.setEchoMode(self.input_password.Normal)
                self.input_repeat_password.setEchoMode(self.input_repeat_password.Normal)
            else:
                self.input_password.setEchoMode(self.input_password.Password)
                self.input_repeat_password.setEchoMode(self.input_repeat_password.Password)
        if event.key() == Qt.Key_F2:  # Случайно сгенерированный пароль
            password = Password.generate_password(12)
            self.input_password.setText(password)
            self.input_repeat_password.setText(password)

    def check_password(self):
        cur = self.con.cursor()
        if self.input_password.text() != self.input_repeat_password.text():
            self.message_label.setText('Ошибка: введенные пароли не совпадают')
            return
        if Password.check_password(self.input_password.text()) != 'ok':
            self.message_label.setText(Password.check_password(self.input_password.text()))
            return
        cur.execute('''UPDATE User
                       SET password = ?
                           WHERE Login = ?''', (self.input_password.text(), self.user.lower()))
        self.con.commit()
        self.con.close()
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RecoveryPasswordDialog()
    if ex.is_exit == 'ok':
        ex.show()
        sys.excepthook = except_hook
        sys.exit(app.exec())
