import datetime

import re
import psycopg2.extras
from flask_login import current_user

from flask import url_for


class FDataBase:
    def __init__(self, db):
        self.__db = db
        #self.__cur = db.cursor()
        self.__cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def addProduct(self, product_name, price, discounted_price):
        try:

            self.__cur.execute(
                f"SELECT COUNT(*) AS \"'count'\" from Products where product_name LIKE'{product_name}'")
            res = self.__cur.fetchone()
            if res["'count'"] > 0:
                print("Продукт с таким именем уже существует")
                return False

            self.__cur.execute(
                f"INSERT INTO Products(product_name, price, discounted_price) VALUES('{product_name}','{price}','{discounted_price}')")
            self.__db.commit()
        except Exception as e:
            print("Ошибка добавления продукта в БД " + str(e))
            return False
        return True

    def addСard(self, card_series, card_number, card_status,current_discount,data_card_end,author):
        try:

            # self.__cur.execute(
            #     f"SELECT COUNT(*) AS \"'count'\" from Cards where card_number LIKE'{card_number}'")
            # res = self.__cur.fetchone()
            # if res["'count'"] > 0:
            #     print("Карта с таким номером уже существует")
            #     return False
            data_card_create =datetime.datetime.now()
            data_card_last_use = "a"
            total_sum = 0
            self.__cur.execute(
                f"INSERT INTO Cards(owner,card_series, card_number, card_status,current_discount, data_card_create,data_card_end, data_card_last_use,total_sum) VALUES('{author}','{card_series}','{card_number}','{card_status}','{current_discount}','{data_card_create}','{data_card_end}','{data_card_last_use}','{total_sum}')")
            self.__db.commit()
        except Exception as e:
            print("Ошибка добавления продукта в БД " + str(e))
            return False

        return True

    def addUser(self, name, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT(*) as \"'count'\" FROM users WHERE name LIKE '{name}'")
            res = self.__cur.fetchone()
            print(res)
            if res["'count'"] > 0:
                print("Пользователь с таким  именем уже существует")
                return False

            self.__cur.execute(f"INSERT INTO users(name,email,psw) VALUES( '{name}', '{email}', '{hpsw}')")
            self.__db.commit()
        except Exception as e:
            print("Ошибка добавления пользователя в БД " + str(e))
            return False

        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = '{user_id}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except Exception as e:
            print("Ошибка получения данных из БД " + str(e))

        return False


    def getUserByName(self, name):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE name = '{name}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except Exception as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def getCardsByName(self, name):
        try:
            self.__cur.execute(f"SELECT * FROM Cards WHERE owner = '{name}'")
            res = self.__cur.fetchall()
            print(res)
            if not res:
                print("Карты не найдены")
                return False

            return res
        except Exception as e:
            print("Ошибка получения данных из БД " + str(e))

        return False


    def getCard(self, alias):
        try:
            print(alias)
            self.__cur.execute(f"SELECT * FROM Cards WHERE card_number = '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            print(res)
            if res:
                return res
        except Exception as e:
            print("Ошибка получения карты из БД " + str(e))
        return (False, False)