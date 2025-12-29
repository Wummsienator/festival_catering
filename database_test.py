import pyodbc 

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

# cursor.execute("SELECT * FROM Tickets")
# for row in cursor:
#     print('row = %r' % (row,))


test = Database()
# print(test.getProductsForStand(1))
# print(test.getOrdersForTicket(1234567))
# print(test.getOrdersForStand(3))