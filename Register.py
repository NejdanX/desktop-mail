from static.Forms.register_form import Ui_RegisterForm
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtCore import Qt
from Constants import DB_FILE_NAME, SECRET_QUESTIONS
import Password
import sys
import sqlite3
from re import search


def transliterate(name):
    """Транслит русских символов для логина"""
    dictionary = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
              'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
              'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
              'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
              'ю': 'u', 'я': 'ya', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'YO',
              'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
              'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H',
              'Ц': 'C', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SCH', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'E',
              'Ю': 'U', 'Я': 'YA'}
    result = ''
    for symbol in name:
        if symbol in dictionary:
            result += dictionary[symbol]
        else:
            result += symbol
    return result


class Registration(QWidget, Ui_RegisterForm):
    def __init__(self, *args):
        self.con = sqlite3.connect(DB_FILE_NAME)
        super(Registration, self).__init__()
        self.setupUi(self)
        self.secret_question.addItems(SECRET_QUESTIONS)
        self.secret_question.setCurrentText('')
        self.btn_register.clicked.connect(self.add_user)
        self.input_full_name.editingFinished.connect(self.generate_login)
        self.date_birthday.editingFinished.connect(self.generate_login)

    def add_user(self):
        """Добавляет пользователя в БД"""
        cur = self.con.cursor()
        if self.input_password.text() != self.input_repeat_password.text():
            self.message_label.setText('Ошибка: введенные пароли не совпадают')
            return
        fn, dt, lg = self.input_full_name.text(), self.date_birthday.text(), self.input_email.currentText()
        psw, ques, ans = self.input_password.text(), self.secret_question.currentText(), self.secret_answer.text()
        correctness = self.check_correctness(fn, dt, lg, psw, ques, ans)
        if correctness == 'ok':
            cur.execute(f'''INSERT INTO User(Full_name, Date_of_birth, Login, Password, Secret_question, Answer)  
                            VALUES {(fn, dt, lg.lower(), psw, ques, ans)}''')
            self.con.commit()
            self.con.close()
            QMessageBox.information(self, 'Успешно', 'Регистрация прошла успешно', QMessageBox.Ok)
            self.close()
        else:
            self.message_label.setText(correctness)

    def generate_login(self):
        """Предлагает варианты логина пользователю"""
        self.input_email.clear()
        fn = self.input_full_name.text()
        date = self.date_birthday.text()
        variants = set()
        if search(r'[А-Яа-я]', fn):
            fn = transliterate(fn)
        end = '@python.com'
        if fn and date and len(fn) >= 3:
            variants.add(fn[0][0] + fn[1][0] + fn[2][0] + end)
            variants.add(fn.replace(' ', '') + end)
            variants.add(fn[0] + fn[1][0] + fn[2][0] + end)
            variants.add(fn[1][0] + fn[0] + end)
            if len(fn.split()) >= 3:
                fn = fn.split()
                variants.add(fn[1][0] + fn[0] + end)
                variants.add(fn[0] + end)
                variants.add(fn[0] + date[-4:] + end)
                variants.add(fn[0] + date[-2:] + end)
                variants.add(''.join(fn) + end)
        self.input_email.addItems(variants)

    def check_correctness(self, *args):
        """Проверяет наличие данного пользователя в БД и корректность введенных данных"""
        cur = self.con.cursor()
        for elem in args:
            if not elem:
                return 'Ошибка: не все поля заполнены'
        if Password.check_password(args[3]) != 'ok':
            return Password.check_password(args[3])
        user_already_in = cur.execute('''
                                SELECT COUNT(Login) FROM User
                                    WHERE Login = ?''',
                                      (args[2].lower(),)).fetchall()
        if user_already_in[0][0]:
            return 'Ошибка: пользователь с таким логином есть в базе данных'
        return 'ok'

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


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Registration()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
