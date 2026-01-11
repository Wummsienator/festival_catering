import pyodbc 
import datetime

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
        
    def placeOrder(self, stand, ticket, position_list, price, special_requests):
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

        # self._cursor.execute(f"UPDATE GlobalIDs SET NextID = {new_order_id + 1} WHERE Name = 'Orders'")
        # self._cursor.execute(f"UPDATE GlobalIDs SET NextID = {new_order2ticket_id + 1} WHERE Name = 'Order2Ticket'")
        # self._cursor.commit()

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

        for index, row in enumerate(r_rows):
            price += position_list[index]["quantity"] * row[2]
            time += position_list[index]["quantity"] * row[3]

            insert = f"""
                     INSERT INTO OrderPositions
                     VALUES ({new_order_id},{index + 1},{row[0]},{position_list[index]["quantity"]})
                     """
            self._cursor.execute(insert)

        
        # self._cursor.commit()

# cursor.execute("SELECT * FROM Tickets")
# for row in cursor:
#     print('row = %r' % (row,))


test = Database()
# print(test.getProductsForStand(1))
# print(test.getOrdersForTicket(1234567))
# print(test.getOrdersForStand(3))
# print(test.getPositionsForOrder(1))
# print(test.get_special_requests_for_order(1))
# print(test.getProducts())
# print(test.checkVip(8910111))
test.placeOrder(1, 121212122121, [{"product": "Pizza Hawaii", "quantity": 3}, {"product": "Pizza Kebab", "quantity": 1}], 5, '123456')



