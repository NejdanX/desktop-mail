from PyQt5.QtWidgets import QWidget
from static.Forms.write_message_form import Ui_write_message_form
from datetime import datetime as dt
from Constants import DB_FILE_NAME
import sqlite3
import sys


class Message(QWidget, Ui_write_message_form):
    def __init__(self, mail, sender_login):
        super(Message, self).__init__()
        self.setupUi(self)
        self.mail = mail
        self.sender_login = sender_login.lower()
        self.con = sqlite3.connect(DB_FILE_NAME)
        self.btn_send_message.clicked.connect(self.add_message_in_db)

    def add_message_in_db(self):
        """Добавляет новое письмо в БД"""
        cursor = self.con.cursor()
        is_real_user = cursor.execute('''SELECT User_id, Login FROM User
                                      WHERE Login = ?''', (self.input_receiver.text().lower(),)).fetchall()
        if is_real_user:
            title = self.input_title.text() if self.input_title.text() else '<Без темы>'
            sender_id = cursor.execute('''SELECT User_id FROM User 
                                          WHERE Login = ?''', (self.sender_login,)).fetchone()[0]
            parameters_sender = (sender_id, title, str(dt.today()), self.sender_login.capitalize(),
                          is_real_user[0][1].capitalize(), self.write_message.toPlainText(), 1)
            parameters_receiver = (is_real_user[0][0], title, str(dt.today()), self.sender_login.capitalize(),
                          is_real_user[0][1].capitalize(), self.write_message.toPlainText(), 0)
            cursor.execute(f'''INSERT INTO Mail(User_id, Title, Date, Sender_login, Receiver_login, Text, Is_read)
                               VALUES {parameters_sender}''')
            cursor.execute(f'''INSERT INTO Mail(User_id, Title, Date, Sender_login, Receiver_login, Text, Is_read)
                                           VALUES {parameters_receiver}''')
            self.con.commit()
            self.con.close()
            self.close()
        else:
            self.lbl_error.setText('Пользователя с таким логином не существует')

    def closeEvent(self, event):
        self.mail.get_db_data()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
