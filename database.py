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

    def get_products_for_stand(self, stand):
        products = []
        select = f"""
                    SELECT p.*, s2p.Quantity FROM Products AS p 
                    INNER JOIN Stand2Product AS s2p ON s2p.ProductID = p.ProductID 
                    WHERE s2p.StandID = {stand}
                 """
        for row in self._cursor.execute(select):
            products.append({"ID": row[0], "name": row[1], "price": round(row[2], 2), "time": row[3], "quantity": row[4]})
        return products
    
    def get_orders_for_ticket(self, ticket):
        orders = []
        select = f"""
                    SELECT o.*, s.StatusText FROM Orders AS o 
                    INNER JOIN Order2Ticket AS o2t ON o2t.OrderID = o.OrderID 
                    INNER JOIN Status AS s ON s.StatusID = o.StatusID 
                    WHERE o2t.TicketNR = {ticket}
                 """
        for row in self._cursor.execute(select):
            orders.append({"ID": row[0], "time": row[1], "timestamp": row[2], "price": round(row[3], 2), "status": row[4], "status_desc": row[7], "special_request": row[5], "stand": row[6]})
        return orders
    
    def get_orders_for_stand(self, stand):
        orders = []
        select = f"""
                    SELECT o.*, s.StatusText FROM Orders AS o 
                    INNER JOIN Status AS s ON s.StatusID = o.StatusID 
                    WHERE o.StandID = {stand}
                 """
        for row in self._cursor.execute(select):
            orders.append({"ID": row[0], "time": row[1], "timestamp": row[2], "price": round(row[3], 2), "status": row[4], "status_desc": row[7], "special_request": row[5], "stand": row[6]})
        return orders
    
    def get_positions_for_order(self, order):
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
        
        return self._cursor.execute(select).fetchone()[0]

        
    def get_products(self):
        products = []
        select = f"""
                    SELECT * FROM Products
                 """
        for row in self._cursor.execute(select):
            products.append({"ID": row[0], "name": row[1], "price": round(row[2], 2), "time": row[3]})
        return products
    
    def check_vip(self, ticket):
        select = f"""
                 SELECT VIP FROM Tickets
                 WHERE TicketNR = {ticket}
                 """
        for row in self._cursor.execute(select):
            return row[0]
        
    def place_order(self, stand, ticket, position_list, price, special_requests):    #returns boolean if order could be placed
        #check if ticket has enough credits
        if self.get_credit_for_ticket(ticket) < price:
            return False

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
        # price = 0
        products = []
        for p in position_list:
            products.append(p["productID"]) 
        placeholders = ",".join("?" for _ in products)

        select = f"""
                 SELECT * FROM Products
                 WHERE ProductID IN ({placeholders})
                 """
        
        self._cursor.execute(select, products)
        r_rows = self._cursor.fetchall()

        #positions for new order
        for index, row in enumerate(r_rows):
            # price += position_list[index]["quantity"] * row[2]
            time += position_list[index]["quantity"] * row[3]

            insert = f"""
                     INSERT INTO OrderPositions
                     VALUES ({new_order_id},{index + 1},{row[0]},{position_list[index]["quantity"]})
                     """
            self._cursor.execute(insert)

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

    def get_credit_for_ticket(self, ticket):
        select = f"""
                 SELECT Credit FROM Tickets
                 WHERE TicketNR = {ticket}
                 """
        
        row = self._cursor.execute(select).fetchone()
        return round(row[0],2)
        
    def check_login(self, ticket, password):
        select = f"""
                 SELECT * FROM Tickets
                 WHERE TicketNR = {ticket}
                 """
        
        #check if ticket exists
        row = self._cursor.execute(select).fetchone()
        if row:
            #check password
            if row[1] == password:
                #check if ticket is connected to stand
                if row[4]:
                    return True, row[4]
                else:
                    return True, None
            else:
                return False, None
        else:
            #ticket doesnt exist
            return False, None
    
    def connect_order_to_ticket(self, order, ticket):
        if self._check_order2ticket_exists(order, ticket):
            return
        
        #get new id
        new_order2ticket_id = ''
        select = """
                 SELECT NextID FROM GlobalIDs
                 WHERE Name = 'Order2Ticket'
                 """
        
        new_order2ticket_id = self._cursor.execute(select).fetchone()[0]

        self._cursor.execute(f"UPDATE GlobalIDs SET NextID = NextID + 1 WHERE Name = 'Order2Ticket'")

        #link ticket to order
        insert = f"""
                 INSERT INTO Order2Ticket
                 VALUES ({new_order2ticket_id},{order},{ticket})
                 """
        
        self._cursor.execute(insert)
        self._cursor.commit()
    
    def _check_order2ticket_exists(self, order, ticket):
        select = f"""
                 SELECT ID FROM Order2Ticket
                 WHERE OrderID = {order} AND TicketNR = {ticket}
                 """
        
        if self._cursor.execute(select).fetchone():
            return True
        else:
            return False

    def add_product_for_stand(self, stand, product, quantity):
        select = f"""
                 SELECT * FROM Stand2Product
                 WHERE StandID = {stand} AND ProductID = {product}
                 """
        
        #check if product already exists on stand
        if self._cursor.execute(select).fetchone():
            self._cursor.execute(f"UPDATE Stand2Product SET Quantity = Quantity + {quantity} WHERE StandID = {stand} AND ProductID = {product}")
            self._cursor.commit()
            return
        
        #add new product on stand
        insert = f"""
                 INSERT INTO Stand2Product
                 VALUES ({stand},{product},{quantity})
                 """
        
        self._cursor.execute(insert)
        self._cursor.commit()

    def change_status_for_order(self, order):
        select = f"""
                 SELECT StatusID FROM Orders
                 WHERE OrderID = {order}
                 """

        row = self._cursor.execute(select).fetchone()

        #check if order exists and is not in final status
        if row and row[0] < 4:
            #update status
            self._cursor.execute(f"UPDATE Orders SET StatusID = StatusID + 1 WHERE OrderID = {order}")
            self._cursor.commit()

    def search_stand(self, standStr):
        stands = []
        select = f"""
                 SELECT * FROM Stands
                 WHERE Name LIKE '%{standStr}%'
                 """
        
        for row in self._cursor.execute(select):
            stands.append({"ID": row[0], "name": row[1]})
        return stands



