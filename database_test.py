import pyodbc 
import datetime
from decimal import *

class Database:
    def __init__(self):
        cnxn = pyodbc.connect("Driver={ODBC Driver 18 for SQL Server};"
                            r"Server=Control-Tower3\FESAPPSQLSERVER;"
                            "Database=FestivalCateringAPP;"
                            "Trusted_Connection=yes;"
                            "Encrypt=yes;"
                            "TrustServerCertificate=yes;")

        self._cursor = cnxn.cursor()

    def getProductsForStand(self, stand):
        products = []
        select = f"""
                    SELECT p.*, s2p.Quantity FROM Products AS p 
                    INNER JOIN Stand2Product AS s2p ON s2p.ProductID = p.ProductID 
                    WHERE s2p.StandID = {stand}
                 """
        for row in self._cursor.execute(select):
            products.append({"ID": row[0], "name": row[1], "price": row[2], "time": row[3], "quantity": row[4]})
        return products
    
    def getOrdersForTicket(self, ticket):
        orders = []
        select = f"""
                    SELECT o.*, s.StatusText FROM Orders AS o 
                    INNER JOIN Order2Ticket AS o2t ON o2t.OrderID = o.OrderID 
                    INNER JOIN Status AS s ON s.StatusID = o.StatusID 
                    WHERE o2t.TicketNR = {ticket}
                 """
        for row in self._cursor.execute(select):
            orders.append({"ID": row[0], "time": row[1], "timestamp": row[2], "price": row[3], "status": row[4], "status_desc": row[7], "special_request": row[5], "stand": row[6]})
        return orders
    
    def getOrdersForStand(self, stand):
        orders = []
        select = f"""
                    SELECT o.*, s.StatusText FROM Orders AS o 
                    INNER JOIN Status AS s ON s.StatusID = o.StatusID 
                    WHERE o.StandID = {stand}
                 """
        for row in self._cursor.execute(select):
            orders.append({"ID": row[0], "time": row[1], "timestamp": row[2], "price": row[3], "status": row[4], "status_desc": row[7], "special_request": row[5], "stand": row[6]})
        return orders
    
    def getPositionsForOrder(self, order):
        positions = []
        select = f"""
                    SELECT op.*, p.Name FROM OrderPositions AS op
                    INNER JOIN Products AS p ON p.ProductID = op.ProductID 
                    WHERE op.OrderID = {order}
                 """
        for row in self._cursor.execute(select):
            positions.append({"order": row[0], "position": row[1], "product": row[2], "name": row[4], "quantity": row[3]})
        return positions
    
    def get_special_requests_for_order(self, order):
        select = f"""
                    SELECT SpecialRequest FROM Orders
                    WHERE OrderID = {order}
                 """
        for row in self._cursor.execute(select):
            return row[0]
        
    def getProducts(self):
        products = []
        select = f"""
                    SELECT * FROM Products
                 """
        for row in self._cursor.execute(select):
            products.append({"ID": row[0], "name": row[1], "price": row[2], "time": row[3]})
        return products
    
    def checkVip(self, ticket):
        select = f"""
                 SELECT VIP FROM Tickets
                 WHERE TicketNR = {ticket}
                 """
        for row in self._cursor.execute(select):
            return row[0]
        
    def placeOrder(self, stand, ticket, position_list, special_requests):    #returns boolean if order could be placed
        #get new IDs
        new_order_id = ''
        new_order2ticket_id = ''
        select = """
                 SELECT Name, NextID FROM GlobalIDs
                 WHERE Name = 'Orders' OR Name = 'Order2Ticket'
                 """
        for row in self._cursor.execute(select):
            if row[0] == "Orders":
                new_order_id = row[1]
            elif row[0] == "Order2Ticket":
                new_order2ticket_id = row[1]

        self._cursor.execute(f"UPDATE GlobalIDs SET NextID = NextID + 1 WHERE Name = 'Orders'")
        self._cursor.execute(f"UPDATE GlobalIDs SET NextID = NextID + 1 WHERE Name = 'Order2Ticket'")

        #add new order
        time = 0
        price = 0
        products = []
        for p in position_list:
            products.append(f'{p["product"]}') 
        placeholders = ",".join("?" for _ in products)

        select = f"""
                 SELECT * FROM Products
                 WHERE Name IN ({placeholders})
                 """
        
        self._cursor.execute(select, products)
        r_rows = self._cursor.fetchall()

        #positions for new order
        for index, row in enumerate(r_rows):
            price += position_list[index]["quantity"] * row[2]
            time += position_list[index]["quantity"] * row[3]

            insert = f"""
                     INSERT INTO OrderPositions
                     VALUES ({new_order_id},{index + 1},{row[0]},{position_list[index]["quantity"]})
                     """
            self._cursor.execute(insert)

        #check if ticket has enough credits
        if self.getCreditForTicket(ticket) < price:
            return False

        #new order
        insert = """
                 INSERT INTO Orders
                 VALUES (?, ?, ?, ?, ?, ?, ?)
                 """
        
        params = (
            new_order_id,
            time,                     
            datetime.datetime.now(),     #because date object conversion doesn't work in string directly
            price,
            1,
            special_requests,
            stand
        )
        
        self._cursor.execute(insert, params)

        #order2ticket
        insert = f"""
                 INSERT INTO Order2Ticket
                 VALUES ({new_order2ticket_id},{new_order_id},{ticket})
                 """
        
        self._cursor.execute(insert)

        #update credit
        self._cursor.execute(f"UPDATE Tickets SET Credit = Credit - {price} WHERE TicketNR = {ticket}")
        
        self._cursor.commit()

        #success
        return True   

    def getCreditForTicket(self, ticket):
        select = f"""
                 SELECT Credit FROM Tickets
                 WHERE TicketNR = {ticket}
                 """
        
        for row in self._cursor.execute(select):
            return row[0]
        
    def checkLogin(self, ticket, password):
        select = f"""
                 SELECT * FROM Tickets
                 WHERE TicketNR = {ticket}
                 """
        
        #check if ticket exists
        for row in self._cursor.execute(select):
            #check password
            if row[1] == password:
                #check if ticket is connected to stand
                if row[4]:
                    return True, row[4]
                else:
                    return True, None
            else:
                False, None
        #ticket doesnt exist
        return False, None

test = Database()
# print(test.getProductsForStand(1))
# print(test.getOrdersForTicket(1234567))
# print(test.getOrdersForStand(3))
# print(test.getPositionsForOrder(1))
# print(test.get_special_requests_for_order(1))
# print(test.getProducts())
# print(test.checkVip(8910111))
# print(test.placeOrder(1, 1234567, [{"product": "Pizza Hawaii", "quantity": 3}, {"product": "Pizza Kebab", "quantity": 1}], '123456'))
# print(test.getCreditForTicket(1234567))
# print(test.checkLogin(1234567, "OneTwoThreeForSix"))
# print(test.checkLogin(1234567, "OneTwoThreeForFive"))
# print(test.checkLogin(11111111, "Admin"))


