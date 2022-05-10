from PyQt5.QtWidgets import QApplication, QWidget
from static.Forms.read_message_form import Ui_message_information_form
from datetime import timedelta, datetime as dt
import sys


class Message(QWidget, Ui_message_information_form):
    def __init__(self, message_data):
        super(Message, self).__init__()
        self.message_data = message_data
        self.setupUi(self)
        self.setWindowTitle(self.message_data[1])
        self.print_message()

    def print_message(self):
        """Выводит информацию и текст письма"""
        HTML = "<font size = {} ><b>{}</b></font>".format(
            4, 'ТЕМА: ' + self.message_data[1].upper() + '<br><br>')
        date = self.message_data[2]
        if date == 'Today':
            date = dt.today()
        elif date == 'Yesterday':
            date = dt.today() - timedelta(days=1)
        date = dt.fromisoformat(date).strftime('%d %B %Y %H:%M')
        HTML += 'Дата: ' + "<font size = {} >{}</font>".format(
            3, date + '<br>')
        HTML += 'Отправитель: ' + "<font color = 'blue', size = {} ><u>{}</u></font>".format(
            3, self.message_data[3] + '<br>')
        HTML += 'Получатель: ' + "<font color = 'blue', size = {} ><u>{}</u></font>".format(
            3, self.message_data[4] + '<br><br>')
        HTML += self.message_data[5].replace('\\n', '<br>')
        self.message.setHtml(HTML)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Message(['1', 'Письмо', '1970-01-01 00:00:00', 'Sample', 'Sample', 'Text'])
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())