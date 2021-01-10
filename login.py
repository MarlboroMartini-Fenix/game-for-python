from PyQt5.Qt import *

from welcome import MainCookie
from signup import Dialog
import sqlite3


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(496, 265)
        self.u_name_label = QLabel(Dialog)
        self.u_name_label.setGeometry(QRect(150, 110, 71, 20))
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.u_name_label.setFont(font)
        self.u_name_label.setAlignment(Qt.AlignCenter)
        self.u_name_label.setObjectName("u_name_label")
        self.pass_label = QLabel(Dialog)
        self.pass_label.setGeometry(QRect(150, 150, 71, 21))
        font = QFont()
        font.setPointSize(10)
        self.pass_label.setFont(font)
        self.pass_label.setAlignment(Qt.AlignCenter)
        self.pass_label.setObjectName("pass_label")
        self.uname_lineEdit = QLineEdit(Dialog)
        self.uname_lineEdit.setGeometry(QRect(230, 110, 113, 20))
        self.uname_lineEdit.setObjectName("uname_lineEdit")
        self.pass_lineEdit = QLineEdit(Dialog)
        self.pass_lineEdit.setGeometry(QRect(230, 150, 113, 20))
        self.pass_lineEdit.setObjectName("pass_lineEdit")
        self.login_btn = QPushButton(Dialog)
        self.login_btn.setGeometry(QRect(230, 200, 51, 23))
        self.login_btn.setObjectName("login_btn")
        self.signup_btn = QPushButton(Dialog)
        self.signup_btn.setGeometry(QRect(290, 200, 51, 23))
        self.signup_btn.setObjectName("signup_btn")
        self.label = QLabel(Dialog)
        self.label.setGeometry(QRect(190, 10, 211, 51))
        font = QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Login Form"))
        self.u_name_label.setText(_translate("Dialog", "USERNAME "))
        self.pass_label.setText(_translate("Dialog", "PASSWORD"))
        self.login_btn.setText(_translate("Dialog", "Login"))
        self.signup_btn.setText(_translate("Dialog", "Sign Up"))
        self.label.setText(_translate("Dialog", "Login Form"))


class LoginDatabase():
    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def is_table(self, table_name):
        query = "SELECT name from sqlite_master WHERE type='table' AND name='{}';".format(table_name)
        cursor = self.conn.execute(query)
        result = cursor.fetchone()
        if result == None:
            return False
        else:
            return True


class MainDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        self.setupUi(self)

        self.loginDatabase = LoginDatabase('login.db')
        if self.loginDatabase.is_table('USERS'):
            pass
        else:
            self.loginDatabase.conn.execute("CREATE TABLE USERS(USERNAME TEXT NOT NULL, EMAIL TEXT, PASSWORD TEXT)")
            self.loginDatabase.conn.execute("INSERT INTO USERS VALUES(?, ?, ?)",
                                           ('admin', 'admin@gmail.com', 'admin')
            )
            self.loginDatabase.conn.commit()

        self.login_btn.clicked.connect(self.loginCheck)
        self.signup_btn.clicked.connect(self.signUpCheck)

    def showMessageBox(self, title, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

    def welcomeWindowShow(self, username):
        self.welcomeWindow = MainWindow(username)
        self.welcomeWindow.show()

    def signUpShow(self):
        self.signUpWindow = Dialog(self)
        self.signUpWindow.show()

    def loginCheck(self):
        username = self.uname_lineEdit.text()
        password = self.pass_lineEdit.text()
        if (not username) or (not password):
            msg = QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля.')
            return

        result = self.loginDatabase.conn.execute("SELECT * FROM USERS WHERE USERNAME = ? AND PASSWORD = ?",
                                                 (username, password))
        if len(result.fetchall()):
            self.welcomeWindowShow(username)
            self.hide()
            self.loginDatabase.conn.close()
        else:
            self.showMessageBox('Внимание!', 'Неправильное имя пользователя или пароль.')

    def signUpCheck(self):
        self.signUpShow()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = MainDialog()
    w.show()
    sys.exit(app.exec_())