set ansi_nulls on
go
set ansi_padding on
go
set quoted_identifier on 
go

use [master]
go

--drop database [pythonDB]
--go

CREATE DATABASE [pythonDB]
go

use [pythonDB]
go

CREATE TABLE Ingredients (
    ID_Ingredients INT PRIMARY KEY IDENTITY(1,1),
    Ingredient_Name NVARCHAR(max) NOT NULL,
    Ingredient_Price DECIMAL(10, 2) DEFAULT 25,
	ActualCount INT NOT NULL DEFAULT 0,
	Ingredient_BuyPrice  DECIMAL(10, 2) DEFAULT 15
);

CREATE TABLE Users (
    ID_User INT PRIMARY KEY IDENTITY(1,1),
    User_Login VARCHAR(50) NOT NULL,
    User_Password VARCHAR(50) NOT NULL,
    User_Role VARCHAR(20) CHECK (User_Role IN ('Пользователь', 'Администратор')) NOT NULL,
    User_Balance DECIMAL(18,2) DEFAULT 50000,
    User_Card VARCHAR(20) CHECK (User_Card IN ('Нет', 'Бронзовая', 'Серебряная', 'Золотая')) DEFAULT 'Нет',
	User_SumBuy DECIMAL(18,2) DEFAULT 0,
	User_Mail VARCHAR(max) NOT NULL,
	CONSTRAINT CK_User_Card CHECK ((User_Card = 'Нет' AND User_SumBuy = 0) OR (User_Card = 'Бронзовая' AND User_SumBuy = 5000) OR (User_Card = 'Серебряная' AND User_SumBuy = 15000) OR (User_Card = 'Золотая' AND User_SumBuy = 25000))
);

INSERT INTO [dbo].[Users]
([User_Login],[User_Password],[User_Role],[User_Balance], [User_Mail]) VALUES
('test', 'test123', 'Пользователь', 155000, 'lebedev.k4@yandex.ru'),
('user', 'user', 'Пользователь', 5555000, 'lebedev.k4@yandex.ru'),
('admin', 'admin', 'Администратор', 5555550, 'lebedev.k4@yandex.ru')
GO

-- Создание таблицы заказов блюд
CREATE TABLE Orders (
    ID_Order INT PRIMARY KEY IDENTITY(1,1),
    Order_ProductName VARCHAR(MAX) NOT NULL DEFAULT('Окрошка на квасе'),
    Order_Count INT NOT NULL,
    Order_Date DATETIME NOT NULL DEFAULT(GETDATE()),
	Order_Price DECIMAL(18,2) DEFAULT 0,
	Order_Sale int not null default 0,
	UserID int not null,
	FOREIGN KEY (UserID) REFERENCES Users(ID_User)
);

-- select * from Orders

-- Создание таблицы заказов ингредиентов
CREATE TABLE Ingredient_Orders(
    ID_IngredientOrders INT PRIMARY KEY IDENTITY(1,1),
    IngredientID INT NOT NULL,
	OrderID INT NOT NULL,
    Count INT NOT NULL,
    FOREIGN KEY (IngredientID) REFERENCES Ingredients(ID_Ingredients),
	FOREIGN KEY (OrderID) REFERENCES Orders(ID_Order)
);

INSERT INTO [dbo].[Ingredients]
([Ingredient_Name],[Ingredient_Price],[ActualCount],[Ingredient_BuyPrice]) VALUES 
('Квас хлебный', 30, 100000, 20),
('Картофель', 20, 100, 10),
('Огурцы', 15, 100, 10),
('Редис', 15, 100, 7),
('Лук зеленый', 25, 100, 15),
('Зелень петрушки', 25, 100, 10),
('Зелень укропа', 25, 100, 10),
('Горчица', 25, 100, 10),
('Перец черный молотый', 10, 50, 5),
('Соль', 10, 50, 5)
GO

SELECT * FROM Ingredients