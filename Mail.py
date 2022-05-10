from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QLineEdit
from PyQt5.QtWidgets import QMenu, QAction, QHeaderView, QMessageBox, QInputDialog
from ClickableLabel import ClickableLabel
from static.Forms.mail_form import Ui_MailForm
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt
from copy import deepcopy
from datetime import datetime as dt
from FrameLayout import FrameLayout
from RecoveryPassword import RecoveryPasswordDialog
from ChangeProfileData import ChangeProfileData
from Constants import DB_FILE_NAME
import MessageRead
import MessageWrite
import sys
import sqlite3


class Mail(QWidget, Ui_MailForm):
    def __init__(self, user_login, login_form=''):
        super(Mail, self).__init__()
        self.setupUi(self)
        self.con = sqlite3.connect(DB_FILE_NAME)
        self.dict_mail_info = {'user_id': [], 'id_message': [], 'title': [], 'date': [],
                               'sender': [], 'receiver': [], 'text': [], 'is_read': [], 'is_deleted': []}
        self.login_form = login_form
        self.is_read = '01'
        self.is_your_send = '01'
        self.only_delete = '0'
        self.active_label = {self.lbl_all: False, self.lbl_received: False, self.lbl_unread: False,
                             self.lbl_read: False, self.lbl_sent: False, self.lbl_trash: False}
        self.user_login = user_login
        self.initUI()
        self.gridLayout.addWidget(self.frame, 1, 0)

    def initUI(self):
        self.messages_table.cellActivated.connect(self.open_message)
        self.messages_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.messages_table.customContextMenuRequested.connect(self.context)
        self.search.editingFinished.connect(self.set_initial_text)
        self.search.textEdited.connect(self.search_messages)
        self.setting_date.clicked.connect(self.get_date)
        self.btn_write_message.clicked.connect(self.write_message)
        self.lbl_all.clicked.connect(self.label_acts)
        self.lbl_received.clicked.connect(self.label_acts)
        self.lbl_read.clicked.connect(self.label_acts)
        self.lbl_sent.clicked.connect(self.label_acts)
        self.lbl_unread.clicked.connect(self.label_acts)
        self.lbl_trash.clicked.connect(self.label_acts)
        self.frame = FrameLayout(title=self.user_login.capitalize())
        self.frame.setStyleSheet(f'''background-color: rgb(0, 120, 240);
                                    font: 18pt;
                                    font-family: {self.lbl_all.fontInfo().family()}''')
        self.change_data = ClickableLabel('Изменить данные профиля')
        self.change_password = ClickableLabel('Сменить пароль')
        self.sign_out = ClickableLabel('Выйти из аккаунта')
        self.change_data.clicked.connect(self.change_profile_data)
        self.change_password.clicked.connect(self.password_recovery)
        self.sign_out.clicked.connect(self.return_login_form)
        self.frame.addWidget(self.change_data)
        self.frame.addWidget(self.change_password)
        self.frame.addWidget(self.sign_out)
        self.frame.setGeometry(0, 0, 200, 200)
        self.label_acts()
        self.setting_table()
        self.get_db_data()

    def context(self, point):
        """Контекстное меню"""
        menu = QMenu()
        if self.messages_table.itemAt(point):
            self.mark_read = self.dict_mail_info['is_read'][self.dict_mail_info['id_message'].index(
                int(self.messages_table.item(self.messages_table.currentRow(), 0).text()))]
            read_message = 'Пометить как непрочитанное' if self.mark_read else 'Пометить как прочитанное'
            self.mark_read = 0 if self.mark_read else 1
            open_message = QAction('Открыть сообщение', menu)
            mark_as_read = QAction(read_message, menu)
            recovery_message = QAction('Восстановить сообщение', menu)
            if self.active_label[list(self.active_label.keys())[-1]]:
                delete_message = QAction('Удалить сообщение', menu)
                delete_message.triggered.connect(self.delete_message)
                recovery_message.setEnabled(True)
            else:
                delete_message = QAction('Убрать сообщение в корзину', menu)
                delete_message.triggered.connect(self.delete_with_recovery)
                recovery_message.setEnabled(False)
            open_message.triggered.connect(self.open_message)
            mark_as_read.triggered.connect(self.mark_as_read)
            recovery_message.triggered.connect(self.delete_with_recovery)
            menu.addActions([open_message, mark_as_read, delete_message, recovery_message])
        menu.exec(self.messages_table.mapToGlobal(point))
        self.get_db_data()

    def delete_with_recovery(self):
        """Помечает данные для удаления/восстановления в БД и помещает их в корзину с возможностью восстановления"""
        if self.sender().text() == 'Восстановить сообщение':
            is_deleted = 0
        else:
            is_deleted = 1
        cur = self.con.cursor()
        id_message = self.messages_table.item(self.messages_table.currentRow(), 0).text()
        cur.execute('''UPDATE Mail
                        SET Is_deleted = ?
                        WHERE Mail_id = ?''', (is_deleted, id_message))
        self.con.commit()
        self.get_db_data()

    def delete_message(self):
        """Безвозвратно удаляет сообщение из БД, если сообщение находится в корзине"""
        id_message = self.messages_table.item(self.messages_table.currentRow(), 0).text()
        self.con.cursor().execute('''DELETE from Mail
                                     WHERE Mail_id = ?''', (id_message,))
        self.con.commit()
        self.get_db_data()

    def label_acts(self):
        """Активирует фильтр при клике на Label"""
        self.is_read = '01'
        self.is_your_send = '01'
        self.only_delete = '0'
        self.active_label = {key: False for key in self.active_label}
        if self.sender() and self.sender().text() != 'Вход':
            self.active_label[self.sender()] = True
        else:
            self.active_label[self.lbl_all] = True
        for key in self.active_label.keys():
            if self.active_label[key]:
                key.setStyleSheet('color: rgb(214, 202, 229); border: 2px solid orange')
            else:
                key.setStyleSheet('color: rgb(214, 202, 229); border: 0px solid black')
        if self.sender() == self.lbl_all:
            self.get_db_data()
        elif self.sender() == self.lbl_read:
            self.is_read = '1'
            self.search_messages()
        elif self.sender() == self.lbl_unread:
            self.is_read = '0'
            self.search_messages()
        elif self.sender() == self.lbl_sent:
            self.is_your_send = '1'
            self.search_messages()
        elif self.sender() == self.lbl_received:
            self.is_your_send = '0'
            self.search_messages()
        elif self.sender() == self.lbl_trash:
            self.only_delete = '1'
            self.search_messages()

    def get_date(self):
        """Получает дату по клику на QCalendarWidget"""
        self.get_db_data(self.setting_date.selectedDate().getDate())

    def search_messages(self):
        """Ищет сообщение в QTableWidget"""
        self.dict_info_copy = {'user_id': [], 'id_message': [], 'title': [], 'date': [],
                               'sender': [], 'receiver': [], 'text': [], 'is_read': [], 'is_deleted': []}
        for i in range(len(self.dict_mail_info['id_message'])):
            items = []
            for key in self.dict_mail_info.keys():
                if str(self.dict_mail_info['is_read'][i]) in self.is_read:
                    items.append(self.dict_mail_info[key][i])
                else:
                    break
            if any([True for item in items[2:-2] if self.search.text() in item]) or \
                    (self.search.text() == 'Поиск по письмам' and items):
                if items[4] != items[5]:
                    if items[4] == self.user_login and '1' not in self.is_your_send:
                        continue
                    elif items[5] == self.user_login and '0' not in self.is_your_send:
                        continue
                if str(items[-1]) != self.only_delete:
                    continue
                for index, key in enumerate(self.dict_mail_info.keys()):
                    self.dict_info_copy[key].append(items[index])
        self.print_table(self.dict_info_copy)

    def set_initial_text(self):
        if not self.search.text() or self.search.text() == 'Поиск по письмам':
            self.search.setText('Поиск по письмам')

    def setting_table(self):
        self.messages_table.setColumnCount(6)
        self.messages_table.setHorizontalHeaderLabels(list(self.dict_mail_info.keys())[1:-2])
        self.messages_table.resizeColumnToContents(0)
        self.messages_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.messages_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.messages_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def color_row(self, row, is_read, color):
        """Красит строку, в зависимости от того, прочитано сообщение или нет"""
        font = QFont()
        font.setBold(is_read)
        for i in range(self.messages_table.columnCount()):
            self.messages_table.item(row, i).setFont(font)
            self.messages_table.item(row, i).setBackground(color)

    def print_table(self, data):
        self.messages_table.setRowCount(0)
        for i in range(len(data['title'])):
            self.messages_table.setRowCount(self.messages_table.rowCount() + 1)
            for j, key in enumerate(list(data.keys())[1:-2]):
                item = data[key][i]
                if key == 'date':
                    item = dt.fromisoformat(item)
                    if (dt.today().date() - item.date()).days == 0:
                        item = 'Today'
                    elif (dt.today().date() - item.date()).days == 1:
                        item = 'Yesterday'
                    else:
                        item = item.strftime('%d %B %Y')
                self.messages_table.setItem(i, j, QTableWidgetItem(str(item).replace('\\n', '\n')))
            if data['is_read'][i]:
                self.color_row(i, 0, QColor(255, 255, 255))
            else:
                self.color_row(i, 1, QColor(230, 230, 230))

    def get_db_data(self, date=''):
        """Получает данные из базы данных и подготавливает их к выводу"""
        self.dict_mail_info = {'user_id': [], 'id_message': [], 'title': [], 'date': [],
                               'sender': [], 'receiver': [], 'text': [], 'is_read': [], 'is_deleted': []}
        cur = self.con.cursor()
        date = '-'.join([str(i).rjust(2, '0') for i in date]) if date else '%'
        mails_info = cur.execute(f'''SELECT * from Mail
                                        WHERE Date LIKE '{date}%' AND User_id = (
                                    SELECT User_id from User
                                        WHERE Login = '{self.user_login.lower()}')''').fetchall()
        mails_info = sorted(mails_info, key=lambda x: x[3], reverse=True)  # Сортируем письма по дате
        for mail in mails_info:
            for index, key in enumerate(self.dict_mail_info):
                self.dict_mail_info[key].append(mail[index])
        self.dict_info_copy = deepcopy(self.dict_mail_info)
        self.search_messages()

    def open_message(self):
        """Открывает сообщение в отдельном окне"""
        data_about_selected_message = []
        id_message_index = self.dict_info_copy['id_message'].index(
            int(self.messages_table.item(self.messages_table.currentRow(), 0).text()))
        for key in list(self.dict_info_copy.keys())[1:-2]:
            data_about_selected_message.append(self.dict_info_copy[key][id_message_index])
        self.mark_read = 1
        self.mark_as_read()
        self.message = MessageRead.Message(data_about_selected_message)
        self.message.setWindowModality(Qt.ApplicationModal)
        self.message.show()
        self.get_db_data()

    def mark_as_read(self):
        id_message = self.messages_table.item(self.messages_table.currentRow(), 0).text()
        cur = self.con.cursor()
        cur.execute('''UPDATE Mail
                        SET Is_read = ?
                        WHERE Mail_id = ?''', (self.mark_read, id_message))
        self.con.commit()

    def write_message(self):
        """Открывает отдельно окно для отправки письма"""
        self.message = MessageWrite.Message(self, self.user_login)
        self.message.setWindowModality(Qt.ApplicationModal)
        self.message.show()

    def change_profile_data(self):
        self.change = ChangeProfileData(self.user_login)
        self.change.setWindowModality(Qt.ApplicationModal)
        self.change.show()

    def password_recovery(self):
        """Восстановление или изменение пароля"""
        answer = QMessageBox.question(self, '', 'Вы помните свой текущий пароль?', QMessageBox.Yes, QMessageBox.No)
        if answer == QMessageBox.Yes:
            cur = self.con.cursor()
            font = QFont()
            font.setPointSize(12)
            self.input_old_password = QInputDialog(self)
            self.input_old_password.setFont(font)
            self.input_old_password.setFixedSize(400, 300)
            self.input_old_password.setWindowTitle('Change password')
            self.input_old_password.setLabelText('Введите ваш старый пароль')
            self.input_old_password.setTextEchoMode(QLineEdit.Password)
            ok = self.input_old_password.exec()
            check_password = cur.execute('''
                                    SELECT COUNT(Login) FROM User
                                        WHERE Password = ?''', (self.input_old_password.textValue(),)).fetchall()
            if not check_password[0][0] and ok:
                QMessageBox.information(self, 'Ошибка пароль', 'Вы ввели неверный пароль',
                                        QMessageBox.Ok)
                return
            self.password_dialog = RecoveryPasswordDialog(user=self.user_login, without_question=True)
        else:
            self.password_dialog = RecoveryPasswordDialog()
            if self.password_dialog.is_exit == 'ok':
                self.password_dialog.show()
            elif self.password_dialog.is_exit == 'Exit: unknown user':
                QMessageBox.information(self, 'Ошибка пользователя', 'Такого пользователя нет в базе данных',
                                        QMessageBox.Ok)
            elif self.password_dialog.is_exit == 'Exit: wrong answer':
                QMessageBox.information(self, 'Ошибка ответа', 'Неверный ответ на секретный вопрос',
                                        QMessageBox.Ok)

    def return_login_form(self):
        if self.login_form:
            self.login_form.show()
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Mail('God')
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
