import pyodbc
import click
import os
from random import randint
from decimal import Decimal
import smtplib
import json

connection = pyodbc.connect('Driver={SQL Server}; Server=DESS\SQLEXPRESS; Database=PythonDB; Trusted_Connection=yes;')
cursor = connection.cursor()
user = None
smtp_server = "smtp.mail.ru"
port = 587
sender_email = ""
password = ""

def mail(receiver_email, code):
    try:
        smpt = smtplib.SMTP(smtp_server, port)
        smpt.starttls()
        smpt.login(sender_email, password=password)
        smpt.sendmail(sender_email, receiver_email, code)
    except Exception as e:
        print(e)
        exit()
    finally:
        smpt.quit() 
        codeConfirm = input("Введите код с почты: ")
        if(code != codeConfirm):
            print("Неправильно!\n")
            mail(receiver_email, code)


def selectUser(login):
    try:
        return cursor.execute(f"SELECT * FROM Users WHERE User_Login = '{login}'").fetchone()
    except Exception as e:
        print(e)

def toLogin():
    try:
        global user
        os.system('cls')
        print("[АВТОРИЗАЦИЯ]")
        login = input("Введите логин: ")
        password = input("Введите пароль: ")
        user = selectUser(login)
        if user is None:
            click.pause("Пользователь не найден\nНажмите любую кнопку для продолжения...")
            toLogin()
        else:
            if user[2] != password:
                click.pause("Неверный пароль\nНажмите любую кнопку для продолжения...")
                toLogin()
            else:
                cursor.execute(f"UPDATE [dbo].[Users] SET [User_Balance] = {user[4]}*2 WHERE [User_Login] = '{user[1]}'")
                user = selectUser(login)
                #mail(user[7], codeGen())
    except Exception as e:
        print(e)

def toRegister():
    try:
        os.system('cls')
        print("[РЕГИСТРАЦИЯ]")
        login = input("Введите логин: ")
        user = selectUser(login)
        if user is not None:
            click.pause("Пользователь с таким логином уже существует\nНажмите любую кнопку для продолжения...")
            toRegister()
        password = input("Введите пароль: ")
        password2 = input("Повторите пароль: ")
        if (password != password2):
            click.pause("Пароли не совпадают\nНажмите любую кнопку для продолжения...")
            toRegister()
        roleID = input("Выберите вашу роль (1 - Пользователь, 2 - Администратор): ")
        toEmail = input("Введите почту: ")
        mail(toEmail, codeGen())
        role = "Пользователь"
        match roleID:
            case "1":
                role = "Пользователь"
            case "2":
                role = "Администратор"
            case _:
                click.pause("1 или 2\nНажмите любую кнопку для продолжения...")
                toRegister()
        insert_query = f"INSERT INTO Users (User_Login, User_Password, User_Role, User_Mail) VALUES ('{login}', '{password}', '{role}', '{toEmail}')"
        cursor.execute(insert_query)
        connection.commit()
        click.pause("Вы успешно зарегистрировались, нажмите любую клавишу для перехода на авторизацию")
        toLogin()
    except Exception as e:
        print(e)

def selectIngredient():
    try:
        select_query = f"SELECT * FROM Ingredients"
        cursor.execute(select_query)
        ingrs = cursor.fetchall()
        x = 1
        for i in ingrs:
            print(f"{x} - {i[1]} - {i[2]}$ - {i[3]}шт - {i[4]}$(Закупочная цена)")
            x += 1
        ingrID = input("Введите номер ингредиента: ")
        ingr = ingrs[int(ingrID)-1]
        if ingr is None:
            click.pause("Такого ингредиента нет\nНажмите любую кнопку для продолжения...")
            selectIngredient()
        else: 
            return ingr
    except Exception as e:
        print(e)

def buyIngredient(ingr):
    try:
        os.system('cls')
        balance = user[4]
        print(f"[ЗАКУПКА ИНГРЕДИЕНТОВ (баланс: {balance})]")
        count = int(input("Введите количество ингредиентов для закупки: "))
        price = ingr[2]*count
        if balance < price:
            click.pause(f"Недостаточно средств, необходимо {price}, а в наличии только {balance}.\nНажмите любую кнопку для продолжения...")
            return
        user[4] -= price
        insert_query = f"UPDATE [dbo].[Ingredients] SET [ActualCount] = {ingr[3]}+{count} WHERE [Ingredient_Name] = '{ingr[1]}'"
        cursor.execute(insert_query)
        insert_query = f"UPDATE [dbo].[Users] SET [User_Balance] = {balance}-{price} WHERE [User_Login] = '{user[1]}'"
        cursor.execute(insert_query)
        connection.commit()
        click.pause(f"Ингредиент '{ingr[1]}' закуплен в количестве {count}шт.\nТеперь на складе {ingr[3]+count}шт.\nНажмите любую кнопку для продолжения...")
    except Exception as e:
        print(e)
    
def changeIngredient(ingr):
    try:
        os.system('cls')
        print("[ИЗМЕНЕНИЕ ИНГРЕДИЕНТОВ]")
        if(input("Изменить название?(Да/Нет)")=="Да"):
            ingr[1] = input("Введите новое название: ")
        if(input("Изменить цену?(Да/Нет)")=="Да"):
            ingr[2] = input("Введите новую цену: ")
        update_query = f"UPDATE [dbo].[Ingredients] SET [Ingredient_Name] = '{ingr[1]}', [Ingredient_Price] = {ingr[2]} WHERE [ID_Ingredients] = {ingr[0]}"
        cursor.execute(update_query)
        connection.commit()
        click.pause(f"Ингредиент '{ingr[1]}' изменен\nНажмите любую кнопку для продолжения...")
    except Exception as e:
        print(e)

def deleteIngredient(ingr):
    try:
        os.system('cls')
        print("[УДАЛЕНИЕ ИНГРЕДИЕНТОВ]")
        if(input("Вы уверены?(Да/Нет)")=="Да"):
            delete_query = f"DELETE FROM [dbo].[Ingredients] WHERE [ID_Ingredients] = {ingr[0]}"
            cursor.execute(delete_query)
            connection.commit()
            click.pause(f"Ингредиент '{ingr[1]}' удален\nНажмите любую кнопку для продолжения...")
        else:
            click.pause(f"Ингредиент '{ingr[1]}' не удален\nНажмите любую кнопку для продолжения...")
    except Exception as e:
        print(e)

def addIngredient():
    try:
        os.system('cls')
        print("[ДОБАВЛЕНИЕ ИНГРЕДИЕНТОВ]")
        name = input("Введите название ингредиента: ")
        price = input("Введите цену ингредиента: ")
        buyprice = input("Введите закупочную цену ингредиента: ")
        insert_query = f"INSERT INTO Ingredients (Ingredient_Name, Ingredient_Price, Ingredient_BuyPrice) VALUES ('{name}', {price}, {buyprice})"
        cursor.execute(insert_query)
        connection.commit()
        click.pause(f"Ингредиент '{name}' добавлен\nНажмите любую кнопку для продолжения...")
    except Exception as e:
        print(e)

def userHistory(userID):
    try:
        cursor.execute(f"SELECT * FROM Orders WHERE [USERID] = {userID}")
        orders = cursor.fetchall()
        print("История заказов:")
        if(len(orders)==0):
            print("Пусто")
        else:
            for i in orders:
                print(f"Заказ №{i[0]} \"{i[1]}\" на сумму {i[4]} [{i[3]}]")
                cursor.execute(f"SELECT * FROM [Ingredient_Orders] inner join [dbo].[Ingredients] on IngredientID = ID_Ingredients WHERE [ORDERID] = {i[0]} order by ID_IngredientOrders")
                ingr = cursor.fetchall()
                for j in ingr:
                    print(f"Доп. ингредиент: {j[6]} - {j[3]}шт./{j[8]}р.")
        click.pause(f"Нажмите любую кнопку для продолжения...")
    except Exception as e:
        print(e)

def adminInterface():
    match(input("Выберите функцию!  (1 - Выбор ингредиента, 2 - Добавление ингредиента, 3 - История, 4 - Выход): ")):
        case "1":
            select = selectIngredient()
            match(input(f"Действие с ингредиентом '{select[1]}'  (1 - Закупка, 2 - Изменение, 3 - Удаление): ")):
                case "1":
                    buyIngredient(select)
                case "2":
                    changeIngredient(select)
                case "3":
                    deleteIngredient(select)
                case _:
                    click.pause("1 или 2\nНажмите любую кнопку для продолжения...")              
        case "2":
            addIngredient()
        case "3":
            users = cursor.execute("SELECT * FROM Users")
            for i in users:
                print(f"{i[0]} - {i[1]}")
            id = input("Введите номер пользователя, историю которого хотите посмотреть:")
            os.system('cls')
            userHistory(id)
            return
        case "4":
            exit()
        case _:
            click.pause("1 или 2 или 3\nНажмите любую кнопку для продолжения...")
            adminInterface()

def calculateStorage(ingrs, count):
    for i in ingrs:
        if i[3] < count:
            return False
    return True

def calculatePrice(ingrs):
    price = 0
    for i in ingrs:
        price += float(i[2])
    return price

def calculateAction(count):
    if count >= 3:
        return count // 3
    else:
        return 0
    
def codeGen():
    return str(randint(100000,999999))

def requestAdd():
    return input("Вы хотите добавить дополнительные ингредиенты в заказ? (Да/Нет): ")== "Да"

def countSale():
    sale = 0
    if(randint(1, 6)==5):
        print("В ВАШЕМ ЗАКАЗЕ БЫЛ НАЙДЕН ТАРАКАН, МЫ ПРЕДОСТАВИМ ВАМ СКИДКУ В 30%!")
        sale += 30
    match(user[5]):
        case "Бронзовая":
            sale += 5
        case "Серебряная":
            sale += 10
        case "Золотая":
            sale += 20
    return sale

def productBuy():
    global user
    print(f"Приветствую {user[1]} на окне составления заказа!\nДействует акция за каждые 3 купленные окрошки на квасе - вы получаете окрошку на квасе в подарок!")
    ingrs = cursor.execute("SELECT * FROM Ingredients").fetchall()
    basePrice = 50
    orderCount = int(input(f"Сколько окрошек на квасе вы хотите купить? ({basePrice}$/шт)   : "))
    orderCountTemp = orderCount + orderCount // 3
    for o in ingrs:
        o[3]  -= orderCountTemp
        if o[3] < 0:
            print("Извините, но на складе нет такого количества ингредиентов!\n ")
            click.pause("Нажмите любую кнопку для продолжения...")
            return
        
    orderPrice = basePrice * orderCount
    product = []
    for i in range(orderCountTemp):
        print(f"СБОРКА ОКРОШКИ №{i+1}")
        ingrAddList = {"ingr":[], "count":[], "price":0}
        while requestAdd():
            num = 1
            for i in ingrs:
                print(f"{num} - {i[1]} - {i[2]}$")
                num+=1
            ingrID = int(input("Введите номер ингредиента, который вы хотите добавить: "))-1
            addcount = int(input("Введите количество ингредиента, который вы хотите добавить: "))
            if ingrs[ingrID][3] < addcount:
                print("Извините, но на складе нет такого количества ингредиентов!\n ")
                click.pause("Нажмите любую кнопку для продолжения...")
                return
            else:
                ingrs[ingrID][3]  -= addcount
            orderPrice += float(ingrs[ingrID][2]) * addcount
            ingrAddList["price"] += float(ingrs[ingrID][2]) * addcount
            ingrAddList["ingr"].append(ingrs[ingrID][0])
            ingrAddList["count"].append(addcount)
            print(f"Вы добавили \"{ingrs[ingrID][1]}\" в заказ №{num}! ({addcount} шт)")
        product.append(ingrAddList)
    sale = countSale()
    orderPrice -= orderPrice * (sale/100)
    print(f"Стоимость заказа составит {orderPrice} (Скидка {sale}%)")
    if input("Вы уверены, что хотите совершить покупку? (Да/Нет): ") != "Да":
        return
    if user[4] < orderPrice:
        print("Извините, но у вас недостаточно средств!\n ")
        click.pause("Нажмите любую кнопку для продолжения...")
        return
    
    for i in ingrs:
        cursor.execute(f"UPDATE Ingredients SET ActualCount = {i[3]} WHERE ID_Ingredients = {i[0]}")

    sumBuy = float(cursor.execute(f"SELECT User_SumBuy FROM Users WHERE ID_User = {user[0]}").fetchall()[0][0])
    sumBuy += orderPrice
    cursor.execute(f"UPDATE Users SET User_Balance = {user[4]} - {orderPrice}, User_SumBuy = {sumBuy} WHERE ID_User = {user[0]}")
    if sumBuy > 0 and sumBuy < 5000:
        cursor.execute(f"UPDATE Users SET User_Card = \'Нет\' WHERE ID_User = {user[0]}")
    elif sumBuy >= 5000 and sumBuy < 15000:
        cursor.execute(f"UPDATE Users SET User_Card = \'Бронзовая\' WHERE ID_User = {user[0]}")
    elif sumBuy >= 15000 and sumBuy < 25000:
        cursor.execute(f"UPDATE Users SET User_Card = \'Серебряная\' WHERE ID_User = {user[0]}")
    elif sumBuy >= 25000:
        cursor.execute(f"UPDATE Users SET User_Card = \'Золотая\' WHERE ID_User = {user[0]}")
    for i in product:
        d = i["price"]
        cursor.execute(f"INSERT INTO Orders (UserID, Order_Price, Order_Count, Order_Sale) VALUES ({user[0]}, {orderPrice}, {d}, {sale})")
        count = len(i["ingr"])
        if(count > 0):
            orderID = cursor.execute("SELECT MAX(ID_Order) FROM Orders").fetchone()[0]
            for j in range(count):
                ingID = i["ingr"][j]
                ingCount = i["count"][j]
                cursor.execute(f"insert into Ingredient_Orders (OrderID, IngredientID, Count) values ({orderID}, {ingID}, {ingCount})")
    user[4] -= Decimal(orderPrice)
    user = cursor.execute(f"select * from Users where ID_User = {user[0]}").fetchall()[0]
    connection.commit()

def userInterface():
    match(input("Выберите функцию!  (1 - Составить заказ, 2 - История, 3 - Выход): ")):
        case "1":
            productBuy()
            return
        case "2":
            userHistory(user[0])
            return
        case "3":
            exit()
        case _:
            click.pause("1 или 2 или 3\nНажмите любую кнопку для продолжения...")
            userInterface()

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, 'MailPassword.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
        sender_email = data['Mail']
        password = data['Password']
    os.system('cls')
    match(input("ДОБРО ПОЖАЛОВАТЬ!\nВыберите функцию(1 - Авторизация, 2 - Регистрация, 3 - Выход): ")):
        case "1":
            toLogin()
        case "2":
            toRegister()
        case _:
            exit()
    while 1:
        os.system('cls')
        print(f"Добро пожаловать {user[1]}! Вход выполнен под ролью \"{user[3]}\" ({user[4]}$)")
        match(user[3]):
            case "Администратор":
                adminInterface()
            case "Пользователь":
                userInterface()
    click.pause("Нажмите любую клавишу для выхода...")
