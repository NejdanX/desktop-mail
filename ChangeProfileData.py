from static.Forms.change_profile_data_form import Ui_ChangeProfileData
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from Constants import DB_FILE_NAME, SECRET_QUESTIONS
import sys
import sqlite3


class ChangeProfileData(QWidget, Ui_ChangeProfileData):
    def __init__(self, user_login):
        super(ChangeProfileData, self).__init__()
        self.setupUi(self)
        self.secret_question.addItems(SECRET_QUESTIONS)
        self.secret_question.setCurrentText('')
        self.user_login = user_login
        self.con = sqlite3.connect(DB_FILE_NAME)
        self.btn_save_change.clicked.connect(self.save_change)

    def save_change(self):
        cur = self.con.cursor()
        user_id = cur.execute(f'''SELECT User_id FROM User
                                 WHERE Login = "{self.user_login.lower()}"''').fetchone()[0]
        if self.input_full_name.text():
            cur.execute(f'''UPDATE User
                            SET Full_name = "{self.input_full_name.text()}"
                            WHERE User_id = "{user_id}"''')
        if self.secret_question.text() and self.secret_answer.text():
            cur.execute(f'''UPDATE User
                            SET Secret_question = "{self.secret_question.text()}", 
                                Answer = "{self.secret_answer.text()}"
                            WHERE User_id = "{user_id}"''')
        else:
            QMessageBox.information(self, 'Ошибка заполнения', 'Заполните поля секретного вопроса и ответа полностью',
                                    QMessageBox.Ok)
            return
        cur.execute(f'''UPDATE User
                        SET Date_of_birth = "{self.date_birthday.text()}"
                        WHERE User_id = "{user_id}"''')
        QMessageBox.information(self, 'Успешно', 'Данные успешно изменены', QMessageBox.Ok)
        self.con.commit()
        self.con.close()
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChangeProfileData('')
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())