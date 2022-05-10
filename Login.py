from static.Forms.login_form import Ui_LoginWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from Register import Registration
from RecoveryPassword import RecoveryPasswordDialog
from Constants import DB_FILE_NAME, RANDOM_GREETS
from random import choice
from Mail import Mail
import sys
import sqlite3


class Login(QMainWindow, Ui_LoginWindow):
    def __init__(self):
        self.con = sqlite3.connect(DB_FILE_NAME)
        super(Login, self).__init__()
        self.setupUi(self)
        self.label_random_greet.setText(choice(RANDOM_GREETS))
        self.label_random_greet.setWordWrap(True)
        self.initUi()

    def initUi(self):
        self.label_show_password.clicked.connect(self.set_echo_mode)
        self.btn_sign_in.clicked.connect(self.sign_in)
        self.label_password_recovery.clicked.connect(self.password_recovery)
        self.label_check_in.clicked.connect(self.check_in)

    def set_echo_mode(self):
        if self.input_password.echoMode() == QLineEdit.Password:  # Установка echoMode для пароля
            self.input_password.setEchoMode(QLineEdit.Normal)
        else:
            self.input_password.setEchoMode(QLineEdit.Password)

    def sign_in(self):
        """Авторизация пользователя и выдача соответствующих прав"""
        cur = self.con.cursor()
        is_correct_user = cur.execute('''
                                SELECT COUNT(Login) FROM User
                                    WHERE Login = ? AND Password = ?''',
                                      (self.input_login.text().lower(), self.input_password.text())).fetchall()
        if not is_correct_user[0][0]:
            self.statusBar().showMessage('Неверный логин или пароль')
        else:
            self.mail = Mail(self.input_login.text().capitalize(), self)
            self.mail.show()
            self.hide()

    def check_in(self):
        """Открывает форму на регистрацию"""
        self.register = Registration(self)
        self.register.show()

    def password_recovery(self):
        self.password_dialog = RecoveryPasswordDialog()
        if self.password_dialog.is_exit == 'ok':
            self.password_dialog.show()
        elif self.password_dialog.is_exit == 'Exit: unknown user':
            self.statusBar().showMessage('Такого пользователя нет в базе данных')
        elif self.password_dialog.is_exit == 'Exit: wrong answer':
            self.statusBar().showMessage('Неверный ответ на секретный вопрос')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())