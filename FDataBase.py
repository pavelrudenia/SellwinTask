import datetime
import psycopg2.extras


class FDataBase:
    def __init__(self, db):
        self.__db = db
        # self.__cur = db.cursor()
        self.__cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def UpdateStatus(self):
        try:
            self.__cur.execute("call UpdateStatus()")
            #res = self.__cur.fetchone()
            # if not res:
            #     print("Ошибка обновления")
            #     return False
            # return res
        except Exception as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

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

    def getProduct(self):
        try:
            self.__cur.execute(
                f"SELECT * FROM Products  ")
            res = self.__cur.fetchall()
            # res = [dict(row) for row in res]

            if not res:
                print("Продукты не найдены")
                return False

            return res
        except Exception as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def getProductPrice(self, name):
        try:
            self.__cur.execute(
                f"SELECT discounted_price FROM Products where product_name = '{name}' ")
            res = self.__cur.fetchone()

            if not res:
                print("Продукт не найден")
                return False

            return res
        except Exception as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def getCardDiscount(self, card_number,series):
        try:
            self.__cur.execute(
                f"SELECT current_discount FROM cards where card_number = '{card_number}' and card_series = '{series}' ")
            res = self.__cur.fetchone()

            if not res:
                print("Карта не найдена")
                return False

            return res
        except Exception as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def addСard(self, card_series, card_number, card_status, current_discount,
                data_card_end, author):
        try:

            self.__cur.execute(
                f"SELECT COUNT(*) AS \"'count'\" from Cards where card_number = '{card_number}' and card_series Like '{card_series}'")
            res = self.__cur.fetchone()
            if res["'count'"] > 0:

                return False
            else:
                data_card_create = datetime.datetime.now()
                data_card_last_use = "Не использовалась"
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
            self.__cur.execute(
                f"SELECT COUNT(*) as \"'count'\" FROM users WHERE name LIKE '{name}'")
            res = self.__cur.fetchone()
            if res["'count'"] > 0:
                print("Пользователь с таким  именем уже существует")
                return False

            self.__cur.execute(
                f"INSERT INTO users(name,email,psw) VALUES( '{name}', '{email}', '{hpsw}')")
            self.__db.commit()
        except Exception as e:
            print("Ошибка добавления пользователя в БД " + str(e))
            return False

        return True

    def CreateOrder(self, count, name_prod, price, current_discount, discount,
                    card_number,card_series):
        try:
            self.__cur.execute(
                f"SELECT total_sum FROM cards where card_number = '{card_number}' and card_series Like '{card_series}';")
            total_sum_last = self.__cur.fetchone()
            total_sum = float(discount) + float(total_sum_last['total_sum'])
            data = datetime.datetime.now()
            self.__cur.execute(
                f"INSERT INTO Orders(date,product,count,amount,discount_amount,discount,card_number) VALUES('{data}', '{name_prod}', '{count}', '{price}', '{current_discount}', '{discount}', '{card_number}')")

            self.__cur.execute(
                f" UPDATE cards SET data_card_last_use = '{data}' where card_number = '{card_number}';")
            self.__cur.execute(
                f" UPDATE cards SET total_sum = '{total_sum}' where card_number = '{card_number}';")
            self.__db.commit()
        except Exception as e:
            print("Ошибка добавления пользователя в БД " + str(e))
            return False

        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(
                f"SELECT * FROM users WHERE id = '{user_id}' LIMIT 1")
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
            self.__cur.execute(
                f"SELECT * FROM users WHERE name = '{name}' LIMIT 1")
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
            self.__cur.execute(
                f"SELECT * FROM Cards WHERE owner = '{name}' and card_status LIKE 'Активная' ")
            res = self.__cur.fetchall()

            if not res:
                print("Карты не найдены")
                return False

            return res
        except Exception as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def getCardsByName_unactive(self, name):
        try:
            self.__cur.execute(
                f"SELECT * FROM Cards WHERE owner = '{name}' and card_status LIKE 'Неактивная'")
            res = self.__cur.fetchall()

            if not res:
                print("Карты не найдены")
                return False

            return res
        except Exception as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def getCardsByName_overdue(self, name):
        try:
            self.__cur.execute(
                f"SELECT * FROM Cards WHERE owner = '{name}' and card_status LIKE 'Просроченная'")
            res = self.__cur.fetchall()

            if not res:
                print("Карты не найдены")
                return False

            return res
        except Exception as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def getCardsByName_delete(self, name):
        try:
            self.__cur.execute(
                f"SELECT * FROM Cards WHERE owner = '{name}' and card_status LIKE 'В корзине'")
            res = self.__cur.fetchall()

            if not res:
                print("Карты в корзине не найдены")
                return False

            return res
        except Exception as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def getCard(self, alias,series):
        try:

            self.__cur.execute(
                f"SELECT * FROM Cards WHERE card_number = '{alias}' and card_series = '{series}'")
            res = self.__cur.fetchone()

            if res:
                return res
        except Exception as e:
            print("Ошибка получения карты из БД " + str(e))
        return (False, False)

    def getOrders(self, card_number):
        try:

            self.__cur.execute(
                f"SELECT * FROM Orders WHERE card_number = '{card_number}' ")
            res = self.__cur.fetchall()

            if res:
                return res
        except Exception as e:
            print("Ошибка получения карты из БД " + str(e))
        return (False, False)

    def getOrdersDate(self, card_number, start, end):
        try:

            self.__cur.execute(
                f"SELECT * FROM Orders WHERE card_number = '{card_number}'and date between '{start}' and '{end}' ")
            res = self.__cur.fetchall()

            if res:
                return res
        except Exception as e:
            print("Ошибка получения карты из БД " + str(e))
        return (False, False)

    def CardDeactivate(self, series, number):
        try:
            self.__cur.execute(
                f"SELECT * FROM Cards WHERE card_number = '{number}' and card_series = '{series}'  LIMIT 1")
            res = self.__cur.fetchone()

            if res:
                self.__cur.execute(
                    f"UPDATE Cards SET card_status = 'Неактивная' WHERE card_number = '{number}' and card_series = '{series}';")
                self.__db.commit()
                return res
        except Exception as e:
            print("Ошибка при изменении статуса " + str(e))
        return (False, False)

    def CardАctivate(self, series, number):
        try:
            self.__cur.execute(
                f"SELECT * FROM Cards WHERE card_number = '{number}' and card_series = '{series}'  LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                self.__cur.execute(
                    f"UPDATE Cards SET card_status = 'Активная' WHERE card_number = '{number}' and card_series = '{series}';")
                self.__db.commit()
                return res
        except Exception as e:
            print("Ошибка при изменении статуса " + str(e))
        return (False, False)

    def ToBasket(self, series, number):
        try:

            self.__cur.execute(
                f"SELECT * FROM Cards WHERE card_number = '{number}' and card_series = '{series}'  LIMIT 1")
            res = self.__cur.fetchone()

            if res:
                self.__cur.execute(
                    f"UPDATE Cards SET card_status = 'В корзине' WHERE card_number = '{number}' and card_series = '{series}';")
                self.__db.commit()
                return res
        except Exception as e:
            print("Ошибка при изменении статуса " + str(e))
        return (False, False)

    def DeleteCard(self, series, number):
        try:
            self.__cur.execute(
                f"SELECT * FROM Cards WHERE card_number = '{number}' and card_series = '{series}'  LIMIT 1")
            res = self.__cur.fetchone()

            if res:
                self.__cur.execute(
                    f"Delete From Cards WHERE card_number = '{number}' and card_series = '{series}';")
                self.__db.commit()
                return res
        except Exception as e:
            print("Ошибка при изменении статуса " + str(e))
        return (False, False)

    def searchCard(self, number, series, status, dis, end_card):
        try:

            self.__cur.execute(
                f"SELECT * FROM Cards WHERE card_number = '{number}'"
                f"and card_series = '{series}' and "
                f"data_card_end = '{end_card}' and card_status = '{status}' "
                f"and current_discount = '{dis}'")

            res = self.__cur.fetchone()
            print(res)
            if res:
                return res
        except Exception as e:
            print("Ошибка получения карты из БД " + str(e))
        return (False, False)
