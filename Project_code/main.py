import profile
import sys
import os
from PySide6 import QtWidgets
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import login_screen_new
import createacc
import profile
from pyrebase import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import requests
import drug_shop
import shop_page_win
import basket_page_win
import numpy as np
from datetime import datetime
import history
# bird
from cgitb import text
from pyexpat import model
from re import S, search
from tkinter.tix import Tree
from xml.etree.ElementTree import tostring
import drug_shop

#nat
from operator import index
from tkinter import dialog
import shop_page_win


cred = credentials.Certificate(
    'Project_code\dbsetting.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://terbal-dab76-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

ref = db.reference('Users/')

# for authentication
firebaseConfig={"apiKey": "AIzaSyCeHgEbtofLKr48WGrCoXc3sFtm8Uze76k", 
  "authDomain": "terbal-dab76.firebaseapp.com",
  "projectId": "terbal-dab76",
  "storageBucket": "terbal-dab76.appspot.com",
  "messagingSenderId": "808320521956",
  "appId": "1:808320521956:web:55ec33eba3785fa0833ef1",
  "databaseURL" : "", #add this because not using the real time database
  "measurementId": "G-2NR6J7NTL2"}


firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()


class Login(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)

        self.ui = login_screen_new.Ui_Dialog()  # load the login ui
        self.ui.setupUi(self)
        self.setWindowTitle("Terbal")

        self.ui.loginbutton.clicked.connect(self.loginfunction)
        self.ui.password.setEchoMode(
            QtWidgets.QLineEdit.Password)  # make password into dots
        self.ui.signupbutton.clicked.connect(self.gotocreate)
        self.ui.invalid_login.setVisible(False)

    def loginfunction(self):
        email = self.ui.email.text()
        password = self.ui.password.text()
        try:
            auth.sign_in_with_email_and_password(email, password)
            home = SelectShop()
            login = Login()
            widget.removeWidget(login)
            widget.addWidget(home)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(e, exc_type, fname, exc_tb.tb_lineno)
            self.ui.invalid_login.setVisible(True)

    def gotocreate(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class CreateAcc(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)

        self.ui = createacc.Ui_Dialog()  # load create acc ui
        self.ui.setupUi(self)
        self.setWindowTitle("Terbal")

        self.ui.createaccbutton.clicked.connect(self.createaccfunction)
        self.ui.password.setEchoMode(
            QtWidgets.QLineEdit.Password)  # hide password
        self.ui.confirmpass.setEchoMode(
            QtWidgets.QLineEdit.Password)  # hide confirm password
        # when register email failed will show up
        self.ui.invalid.setVisible(False)

    def createaccfunction(self):
        email = self.ui.email.text()
        if self.ui.password.text() == self.ui.confirmpass.text():
            password = self.ui.password.text()
            try:
                auth.create_user_with_email_and_password(email, password)
                user = auth.sign_in_with_email_and_password(email, password)
                ref.child(user['localId']).set(
                    {'Email': email, 'Password': password, 'Picture': '', 'Name': '', 'Address': '',
                     'Mobile': '', 'Basket': '', 'Order': ''})
                login = Login()
                createacc = CreateAcc()
                widget.removeWidget(createacc)
                widget.addWidget(login)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                self.ui.invalid.setVisible(True)


class SelectShop(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)

        self.ui = drug_shop.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Terbal")

        self.ui.SearchBar.returnPressed.connect(self.Search)

        self.ui.pushButton.clicked.connect(lambda: self.choosen(1))
        self.ui.pushButton_2.clicked.connect(lambda: self.choosen(2))
        self.ui.pushButton_3.clicked.connect(lambda: self.choosen(3))
        self.ui.pushButton_4.clicked.connect(lambda: self.choosen(4))
        self.ui.pushButton_5.clicked.connect(lambda: self.choosen(5))
        self.ui.pushButton_6.clicked.connect(lambda: self.choosen(6))

        self.ui.profile_icon.clicked.connect(self.profile)
        self.ui.home_icon.clicked.connect(self.order)

        uid = auth.current_user['localId']
        try:
            basket_number = db.reference(
                f'Users/{uid}/Basket Number').get()
        except:
            db.reference(
                f'Users/{uid}').update({'Basket Number': basket_number[0]})

        self.shop_name = [self.ui.shop_name_r1.text(), self.ui.shop_name_r1_2.text(), self.ui.shop_name_r1_3.text(
        ), self.ui.shop_name_r1_4.text(), self.ui.shop_name_r1_5.text(), self.ui.shop_name_r1_6.text()]

    def choosen(self, shop_num):
        shop_number[0] = shop_num
        try:
            shop = ShopPage()
            home = SelectShop()
            widget.removeWidget(home)
            widget.addWidget(shop)
            widget.setCurrentIndex(widget.currentIndex() + 1)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(e, exc_type, fname, exc_tb.tb_lineno)

    def profile(self):
        try:
            home = SelectShop()
            profile = Profile()
            widget.removeWidget(home)
            widget.addWidget(profile)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def order(self):
        home = SelectShop()
        order = Order_History()
        widget.removeWidget(home)
        widget.addWidget(order)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Search(self):
        shop_name = [self.ui.shop_name_r1.text(), self.ui.shop_name_r1_2.text(), self.ui.shop_name_r1_3.text(),
                     self.ui.shop_name_r1_4.text(), self.ui.shop_name_r1_5.text(), self.ui.shop_name_r1_6.text()]
        widgets = []
        search_text = self.ui.SearchBar.text()
        i = 0

        for i in shop_name:
            widgets.append(i)

        self.ui.shop_r1.setVisible(False)
        self.ui.shop_r2.setVisible(False)
        self.ui.shop_r3.setVisible(False)
        self.ui.shop_r4.setVisible(False)
        self.ui.shop_r5.setVisible(False)
        self.ui.shop_r6.setVisible(False)
        search_result = [
            string for string in widgets if search_text.lower() in string.lower()]
        for i in search_result:
            if i in widgets[0]:
                self.ui.shop_r1.setVisible(True)
            if i == widgets[1]:
                self.ui.shop_r2.setVisible(True)
            if i == widgets[2]:
                self.ui.shop_r3.setVisible(True)
            if i == widgets[3]:
                self.ui.shop_r4.setVisible(True)
            if i == widgets[4]:
                self.ui.shop_r5.setVisible(True)
            if i == widgets[5]:
                self.ui.shop_r6.setVisible(True)




class Profile(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)

        self.ui = profile.Ui_Dialog()  # load create acc ui
        self.ui.setupUi(self)
        self.setWindowTitle("Terbal")

        self.ui.browsepic.clicked.connect(self.imageProf)
        self.ui.save.clicked.connect(self.saveProf)
        self.ui.logout.clicked.connect(self.logoutProf)
        self.ui.home.clicked.connect(self.gotoHome)

        self.uid = auth.current_user['localId']
        self.user = db.reference(f'Users/{self.uid}').get()
        try:
            url = self.user['Picture']
            image = QImage()
            image.loadFromData(requests.get(url).content)
            pixmap = QPixmap(image)
            self.ui.profilepic.setPixmap(pixmap.scaled(161, 151))
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            pass
        self.ui.email.setText(self.user['Email'])
        self.ui.name.setText(self.user['Name'])
        self.ui.address.setText(self.user['Address'])
        self.ui.mobile.setText(self.user['Mobile'])

    def imageProf(self):
        path = "D:\\Uni\\SE_Y2\\semester_2\\SE Principle\\Project\\profile images"
        selected_filter = "Images (*.png *.jpg *.jpeg *.gif)"
        self.image_file = QFileDialog.getOpenFileName(
            self, 'Open file', path, selected_filter)
        label = self.ui.profilepic
        pixmap = QPixmap(self.image_file[0])
        label.setPixmap(pixmap.scaled(161, 151))

    def gotoHome(self):
        profile = Profile()
        home = SelectShop()
        widget.removeWidget(profile)
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def saveProf(self):
        db.reference(f'Users/{self.uid}').update(
            {'Name': self.ui.name.text(), 'Address': self.ui.address.text(), 'Mobile': self.ui.mobile.text()})
        try:
            storage = firebase.storage()
            profile_pic = f"{self.image_file[0]}"
            storage.child(f'Image/{self.uid}').put(profile_pic)
            profile_pic_url = storage.child(
                f'Image/{self.uid}').get_url(auth.current_user['idToken'])
            db.reference(
                f'Users/{self.uid}').update({'Picture': profile_pic_url})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            pass

    def logoutProf(self):
        profile = Profile()
        login = Login()
        widget.removeWidget(profile)
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Order_History(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)

        self.ui = history.Ui_Dialog()
        self.ui.setupUi(self)

        self.uid = auth.current_user['localId']

        self.ui.tableWidget.setRowCount(20)
        self.ui.tableWidget.setColumnCount(3)

        self.ui.tableWidget.setCurrentCell(0, 0)

        self.ui.orderBackButton.clicked.connect(self.gotoHome)
        self.pullOrder()
        self.setData()

    def pullOrder(self):
        self.order_db = db.reference(f'Users/{self.uid}/Order').get()
        dates = list(self.order_db)

        shop = list(np.array(list(list(list(self.order_db.values())[
            i].keys()) for i in range(len(dates)))).flatten())

        item_temp = np.array(list(list(list(self.order_db.values())[
                             i].values()) for i in range(len(dates))))
        item_temp1 = list(list(item_temp[i][0].values())
                          for i in range(len(item_temp)))
        item = list(sum(item_temp1[i]) for i in range(len(item_temp1)))

        data_temp = list([dates, shop, item])
        self.data = {f'col{i+1}': data_temp[i] for i in range(len(data_temp))}
        # print('self.data: ', self.data)

    def setData(self):
        for n, key in enumerate(sorted(self.data.keys())):
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem()
                newitem.setData(Qt.DisplayRole, item)
                newitem.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(m, n, newitem)

    def gotoHome(self):
        order = Order_History()
        home = SelectShop()
        widget.removeWidget(order)
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex() + 1)




class ShopPage(QDialog):
    def __init__(self):

        QDialog.__init__(self, None)
        self.ui = shop_page_win.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Terbal Shop Page")
        self.uid = auth.current_user['localId']

        # Basket button
        self.item_txt = "Item"
        self.shop_db = db.reference(f'Shop/R{shop_number[0]}').get()
        self.ui.shop_name.setText(self.shop_db['Name'])
        self.ui.shop_km.setText(self.shop_db['Distance'])
        self.ui.shop_mins.setText(self.shop_db['Time'])
        self.ui.shop_delivery_fee.setText(f"{str(self.shop_db['Fee'])}฿")
        self.ui.toolButton.clicked.connect(self.gotoHome)
        self.ui.basketButton.clicked.connect(self.gotoBasket)

        # middle layout
        layout_middle = QVBoxLayout()

        # items name and price
        self.item_name = ["อ้วยอันโอสถ \nยาแคปซูลฟ้าทะลายโจรสกัด",
                          "ยันฮี ยาฟาร์แท็บ ฟ้าทะลายโจร", "Ya Dom Poi-Sian", "Propoliz mouth spray"]
        self.item_price = [120, 80, 20, 90]

        self.amount_of_item = len(self.item_name)
        shop_name = self.shop_db['Name']
        self.temp_quantity = db.reference(
            f'Users/{self.uid}/Basket/{shop_name}').get()
        try:
            self.item_quantity = list(self.temp_quantity.values())
        except:
            self.item_quantity = []
        for i in range(self.amount_of_item - len(self.item_quantity)):
            self.item_quantity.append(0)

        self.basket_quantity_temp = db.reference(
            f'Users/{self.uid}/Basket').get()
        if len(list(self.basket_quantity_temp)) != 0:
            self.basket_quantity = list(
                list(self.basket_quantity_temp.values())[0].values())
            self.item_num = sum(self.basket_quantity)
            self.net_price = np.dot(self.item_price, self.basket_quantity)
        else:
            self.basket_quantity = self.item_quantity
            self.item_num = sum(self.basket_quantity)
            self.net_price = np.dot(self.item_price, self.basket_quantity)

        self.ui.basketButton.setText("  Basket • " + str(self.item_num) + " " + self.item_txt +
                                     "                              " + "฿" + str(self.net_price))
        self.orderButton = []
        self.item_quantity_label = []
        item_name_label = []
        item_price_label = []
        min_layout = []

        # declare each item (in this case, I use .append because I use list)
        for i in range(self.amount_of_item):
            self.orderButton.append(QPushButton("order", self))
            self.item_quantity_label.append(QLabel())  # quantity
            item_name_label.append(QLabel())  # name
            item_price_label.append(QLabel())  # price
            min_layout.append(QHBoxLayout())  # line by line

        for i in range(self.amount_of_item):

            item_name_label[i].setText(self.item_name[i])
            item_price_label[i].setText(str(self.item_price[i]) + "฿")
            self.item_quantity_label[i].setText(
                "x" + str(self.item_quantity[i]))


            # change ui for button in shop_page_win
            self.orderButton[i].setStyleSheet(u"QPushButton{\n"
                " background-color: white;\n"
                " border: 2px solid black;\n"
                " border-radius: 5px;\n"
                "}\n"
                "\n"
                "QPushButton:hover{\n"
                " color: #15133C;\n"
                " border: 2px solid rgb(111,218,156);\n"
                "}\n"
                "\n"
                "QPushButton:pressed{\n"
                " color: #EFEAD8;\n"
                " background: #6D8B74;\n"
                " border: 2px solid #D0C9C0;\n"
                "}")

            # self.orderButton should be here(the middle), but not in for loop. I write it at almost last line
            min_layout[i].addWidget(item_name_label[i])
            min_layout[i].addWidget(item_price_label[i])
            min_layout[i].addWidget(self.item_quantity_label[i])
            min_layout[i].addWidget(self.orderButton[i])
            layout_middle.addLayout(min_layout[i])

        # order button (MUST!! not in for loop), you can design whatever other code is
        self.orderButton[0].clicked.connect(lambda: self.gotoSelectItem(0))
        self.orderButton[1].clicked.connect(lambda: self.gotoSelectItem(1))
        self.orderButton[2].clicked.connect(lambda: self.gotoSelectItem(2))
        self.orderButton[3].clicked.connect(lambda: self.gotoSelectItem(3))

        # print("Program running!!")
        self.displayInShop = False
        # scrollAreaWidgetContents is in scrollArea (they are created together)
        self.ui.scrollAreaWidgetContents.setLayout(layout_middle)

    def displayInShopPage(self, i, text):
        if text == "add":
            self.item_quantity[i] += 1
            self.item_num += 1  # for all items at basket button
            self.net_price += self.item_price[i]
        elif text == "minus":
            if self.item_quantity[i] >= 1:
                self.item_quantity[i] -= 1
                self.item_num -= 1  # for all items at basket button
                self.net_price -= self.item_price[i]

        # print("Quantity: ", self.item_quantity[i], ", i: ", i)
        self.item_quantity_label[i].setText("x" + str(self.item_quantity[i]))

        if(self.item_num > 0):
            self.item_txt = "Items"

        self.ui.basketButton.setText("  Basket • " + str(self.item_num) + " " + self.item_txt +
                                     "                              " + "฿" + str(self.net_price))

    def gotoHome(self):
        try:
            # clear basket when go to home
            # db.reference(f'Users/{self.uid}/Basket').delete()
            # db.reference(f'Users/{self.uid}').update({'Basket': ''})
            shop = ShopPage()
            home = SelectShop()
            widget.removeWidget(shop)
            widget.addWidget(home)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        except Exception as e:
            print(e)

    def gotoSelectItem(self, index):  # go to another screen **

        self.popup = []
        self.s_item_name = []
        self.noteToShop = []
        self.noteLineEdit = []
        layout_control = []
        plus_button = []
        minus_button = []
        self.addToBasketButton = []
        self.item_amount_label = []
        self.item_amount = []
        layout_big = []
        self.item_pic = []

        shop_name = self.shop_db['Name']

        ref = f'Users/{self.uid}/Basket/{shop_name}'
        if db.reference(ref).get() is None:
            db.reference(f'Users/{self.uid}/Basket').update({self.shop_db['Name']: {
                f'Item {i}': 0 for i in range(len(self.item_name))}})

        self.temp_shop_order = list(
            db.reference(f'Users/{self.uid}/Basket').get())

        for i in range(len(self.temp_shop_order)):
            if self.temp_shop_order[i] != shop_name:
                db.reference(
                    f'Users/{self.uid}/Basket/{self.temp_shop_order[i]}').delete()
                self.basket_quantity_temp = db.reference(
                    f'Users/{self.uid}/Basket').get()
                self.basket_quantity = list(
                    list(self.basket_quantity_temp.values())[0].values())
                self.item_num = sum(self.basket_quantity)
                self.net_price = np.dot(self.item_price, self.basket_quantity)
                self.ui.basketButton.setText("  Basket • " + str(self.item_num) + " " + self.item_txt +
                                             "                              " + "฿" + str(self.net_price))
        db.reference(
            f'Users/{self.uid}').update({'Basket Number': shop_number[0]})

        pic_name = ["pic/Fa_talaijord.jpeg",
                    "pic/poi_sian.jpeg",
                    "pic/propoliz.jpeg",
                    "pic/yan_hee.jpeg"]

        for i in range(self.amount_of_item):
            diag = QDialog(self)
            diag.setFixedSize(375, 600)
            diag.setWindowTitle("Select amount of items")

            self.popup.append(diag)
            layout_big.append(QVBoxLayout())
            self.s_item_name.append(QLabel(self))
            self.noteToShop.append(QLabel(self))
            self.noteLineEdit.append(QLineEdit(self))
            layout_control.append(QHBoxLayout())
            plus_button.append(QPushButton("+", self))
            minus_button.append(QPushButton("-", self))
            self.item_pic.append(QLabel(self))

            # ori 0, can use index or i are the same o/p
            self.item_amount.append(self.item_quantity[index])

            self.item_amount_label.append(QLabel(self))
            self.addBasketButton = QPushButton(self)
            self.addToBasketButton.append(self.addBasketButton)

        for i in range(self.amount_of_item):
            # # customize button
            # plus_button[i].setGeometry(QRect(210, 550, 51, 51))
            # minus_button[i].setGeometry(QRect(100, 550, 51, 51))
            fontB = QFont()
            fontB.setPointSize(28)
            plus_button[i].setFont(fontB)
            minus_button[i].setFont(fontB)
            # self.item_pic[i].setGeometry(QRect(20, 20, 331, 171)) # 331 171
            self.item_pic[i].setPixmap(QPixmap(pic_name[i]))
            self.item_pic[i].setAlignment(Qt.AlignCenter)
            layout_big[i].addWidget(self.item_pic[i])

            self.s_item_name[i].setText(
                self.item_name[i] + "  \n" + str(self.item_price[i]) + "฿")  # item name
            font1 = QFont()
            font1.setPointSize(24)
            self.s_item_name[i].setFont(font1)
            layout_big[i].addWidget(self.s_item_name[i])

            self.noteToShop[i].setText("Note to shop")
            font2 = QFont()
            font2.setPointSize(18)
            self.noteToShop[i].setFont(font2)
            layout_big[i].addWidget(self.noteToShop[i])

            self.noteLineEdit[i].setPlaceholderText("Add your request")
            self.noteLineEdit[i].setFont(font2)
            layout_big[i].addWidget(self.noteLineEdit[i])

            font3 = QFont()
            font3.setPointSize(26)
            self.item_amount_label[i].setFont(font3)
            self.item_amount_label[i].setAlignment(Qt.AlignCenter)
            self.item_amount_label[i].setText(str(self.item_amount[i]))
            layout_control[i].addWidget(minus_button[i])
            layout_control[i].addWidget(self.item_amount_label[i])
            layout_control[i].addWidget(plus_button[i])
            layout_big[i].addLayout(layout_control[i])

            # may be cutomize addToBasketButton
            font4 = QFont()
            font4.setPointSize(24)
            self.addToBasketButton[i].setLayoutDirection(Qt.LeftToRight)
            self.addToBasketButton[i].setStyleSheet(u"text-align: left;")
            self.addToBasketButton[i].setFont(font4)
            self.addToBasketButton[i].setText(
                "Add to Basket                                 ฿" + str(self.item_price[i]))

            layout_big[i].addWidget(self.addToBasketButton[i])

            self.popup[i].setLayout(layout_big[i])

        self.addToBasketButton[0].clicked.connect(
            lambda: self.addToBasketdb(0))
        self.addToBasketButton[1].clicked.connect(
            lambda: self.addToBasketdb(1))
        self.addToBasketButton[2].clicked.connect(
            lambda: self.addToBasketdb(2))
        self.addToBasketButton[3].clicked.connect(
            lambda: self.addToBasketdb(3))

        plus_button[0].clicked.connect(lambda: self.addAmount(0))
        plus_button[1].clicked.connect(lambda: self.addAmount(1))
        plus_button[2].clicked.connect(lambda: self.addAmount(2))
        plus_button[3].clicked.connect(lambda: self.addAmount(3))

        minus_button[0].clicked.connect(lambda: self.minusAmount(0))
        minus_button[1].clicked.connect(lambda: self.minusAmount(1))
        minus_button[2].clicked.connect(lambda: self.minusAmount(2))
        minus_button[3].clicked.connect(lambda: self.minusAmount(3))

        self.addToBasketButton[0].clicked.connect(self.popup[0].close)
        self.addToBasketButton[1].clicked.connect(self.popup[1].close)
        self.addToBasketButton[2].clicked.connect(self.popup[2].close)
        self.addToBasketButton[3].clicked.connect(self.popup[3].close)

        self.popup[index].show()

    def addToBasketdb(self, type):
        # print({self.item_name[type]: self.item_quantity[type]})
        shop_name = self.shop_db['Name']
        db.reference(f'Users/{self.uid}/Basket/{shop_name}').update(
            {f'Item {type}': self.item_quantity[type]})

    def gotoBasket(self):
        basket_quantity_temp = db.reference(
            f'Users/{self.uid}/Basket').get()
        basket_quantity = list(
            list(basket_quantity_temp.values())[0].values())
        net_price = np.dot(self.item_price, basket_quantity)
        basket = Basket(self.item_name, self.item_price,
                        basket_quantity, net_price)
        widget.addWidget(basket)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def addAmount(self, i):
        self.item_amount[i] += 1
        if self.item_amount[i] > 0:
            self.orderButton[i].setText("change")

        self.displayInPopUp(i)
        self.displayInShopPage(i, "add")

    def minusAmount(self, i):
        self.item_amount[i] -= 1
        if self.item_amount[i] == 0:
            self.orderButton[i].setText("order")
        elif self.item_amount[i] < 0:
            self.item_amount[i] = 0

        self.displayInPopUp(i)
        self.displayInShopPage(i, "minus")

    def displayInPopUp(self, i):
        self.item_amount_label[i].setText(str(self.item_amount[i]))
        self.addToBasketButton[i].setText(
            "Add to Basket                    ฿" + str(self.item_price[i] * self.item_amount[i]))
        # print("Amount: ", self.item_amount[i], ", i: ", i)


class Basket(QDialog):
    def __init__(self, item_name, item_price, item_quantity, all_food_price):
        QDialog.__init__(self, None)
        self.ui = basket_page_win.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Basket Page")
        self.uid = auth.current_user['localId']

        # set value
        self.item_quantity = item_quantity  # list
        self.item_name = item_name  # list
        self.item_price = item_price  # list
        self.all_food_price = all_food_price

        # access shop db
        basket_number_temp = db.reference(
            f'Users/{self.uid}/Basket Number').get()
        self.basket_db = db.reference(f'Shop/R{basket_number_temp}').get()

        # access user db
        self.user = db.reference(f'Users/{self.uid}').get()
        self.temp_shop_name = db.reference(
            f'Users/{self.uid}/Basket').get().keys()

        # button
        self.ui.basket_shop_name.setText(self.basket_db['Name'])
        self.ui.basket_shop_km.setText(self.basket_db['Distance'])
        self.ui.basket_shop_mins.setText(self.basket_db['Time'])
        self.ui.addressLineEdit.setText(self.user['Address'])

        # print("Name: ", self.item_name)
        # print("Price: ", self.item_price)
        # print("Quantity: ", self.item_quantity)
        # print("All food price: ", self.all_food_price)

        layout_middle = QVBoxLayout()
        self.amount_of_item = len(self.item_name)

        item_quantity_label = []
        item_name_label = []
        item_price_label = []
        min_layout = []

        for i in range(self.amount_of_item):
            item_quantity_label.append(QLabel())  # quantity
            item_name_label.append(QLabel())  # name
            item_price_label.append(QLabel())  # price
            min_layout.append(QHBoxLayout())  # line by line

        for i in range(self.amount_of_item):
            item_quantity_label[i].setText("x" + str(self.item_quantity[i]))
            item_name_label[i].setText(self.item_name[i])
            item_price_label[i].setText(
                str(self.item_price[i] * self.item_quantity[i]) + "฿")

            min_layout[i].addWidget(item_quantity_label[i])
            min_layout[i].addWidget(item_name_label[i])
            min_layout[i].addWidget(item_price_label[i])
            layout_middle.addLayout(min_layout[i])

        self.ui.basketScrollAreaWidgetContents.setLayout(layout_middle)
        self.ui.placeOrderButton.clicked.connect(self.confirmOrder)
        self.ui.basketBackButton.clicked.connect(self.gotoShop)

        # set the value in UI window
        self.deliveryFee = self.basket_db['Fee']
        self.ui.all_food_price_label.setText("฿" + str(self.all_food_price))
        self.ui.delivery_fee_label.setText("฿" + str(self.deliveryFee))

        self.total_price = float(self.all_food_price) + float(self.deliveryFee)
        self.ui.total_price_label.setText("฿" + str(self.total_price))

    def confirmOrder(self):
        order_hist = {}
        basket_db_name = self.basket_db['Name']

        # Order history
        for i in range(len(self.item_quantity)):
            order_hist.update({f'Item {i}': self.item_quantity[i]})

        # Limit the number of orders to 10
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        order_dir = f'Users/{self.uid}/Order'
        try:
            if len(list(db.reference(order_dir).get().keys())) >= 10:
                oldest_date = min(list(db.reference(order_dir).get().keys()))
                db.reference(f'{order_dir}/{oldest_date}').delete()
        except:
            pass


        # Delete the order from the basket
        try:
            home = SelectShop()
            basket_quantity_temp = db.reference(
                f'Users/{self.uid}/Basket').get()
            basket_quantity = list(
                list(basket_quantity_temp.values())[0].values())
            net_price = np.dot(self.item_price, basket_quantity)
            basket = Basket(self.item_name, self.item_price,
                            basket_quantity, net_price)
            db.reference(
                f'{order_dir}/{current_time}/{basket_db_name}').update(order_hist)
            db.reference(f'Users/{self.uid}').update({'Basket': ''})
            db.reference(f'Users/{self.uid}').update({'Basket Number': '0'})
            widget.removeWidget(basket)
            widget.addWidget(home)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(e, exc_type, fname, exc_tb.tb_lineno)
            pass

        print("Order Confirm:")
        print("Item name: ", self.item_name)
        print("Item price: ", self.item_price)
        print("Item quantity: ", self.item_quantity)
        print("Payment method: ", self.ui.paymentMethodComboBox.currentText())

    def gotoShop(self):
        try:
            shop = ShopPage()
            basket = Basket(self.item_name, self.item_price,
                            self.item_quantity, self.all_food_price)
            widget.removeWidget(basket)
            widget.addWidget(shop)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    shop_number = [0]

    window = Login()
    window.show()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(window)
    widget.setFixedSize(375, 730)
    widget.show()

    app.exec()