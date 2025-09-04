import json

class Database:
    def __init__(self):
        return
    
    def readData(self):
        # Read from file and parse JSON
        with open("data.json", "r") as f:
            data = json.load(f)
        return data
    
    def writeData(self, data):
        json_str = json.dumps(data, indent=4)
        with open("data.json", "w") as f:
            f.write(json_str)
    
    def getproductsForStand(self, stand):
        products = []
        data = self.readData()
        for p in data["Stands"][stand]["products"]:
            products.append(data["Products"][p])
        return products
    
    def adjustTimers(self):
        data = self.readData()
        #adjust timers
        for o in data["Orders"]:
            if data["Orders"][o]["time"] > 0:
                data["Orders"][o]["time"] = data["Orders"][o]["time"] - 1
        self.writeData(data)

    def getOrdersForTicket(self, ticket):
        orders = []
        data = self.readData()
        for o2t in data["Order2Ticket"]:
            #get relation object
            o2tObj = data["Order2Ticket"][o2t]
            if o2tObj["ticket"] == ticket:
                order = data["Orders"][o2tObj["order"]]
                #append order number
                order["order"] = o2tObj["order"]
                #append stand number
                for o2s in data["Order2Stand"]:
                    o2sObj = data["Order2Stand"][o2s]
                    if o2sObj["order"] == o2tObj["order"]:
                        order["stand"] = o2sObj["stand"]
                #get status description
                for s in data["Status"]:
                    if s == order["status"]:
                        order["status_desc"] = data["Status"][s]
                orders.append(order)
        return orders
    
    def getOrdersForStand(self, stand):
        orders = []
        data = self.readData()
        for o2s in data["Order2Stand"]:
            #get relation object
            o2sObj = data["Order2Stand"][o2s]
            if o2sObj["stand"] == stand:
                order = data["Orders"][o2sObj["order"]]
                #append order number
                order["order"] = o2sObj["order"]
                #append stand number
                order["stand"] = stand      
                #get status description
                for s in data["Status"]:
                    if s == order["status"]:
                        order["status_desc"] = data["Status"][s]
        orders.append(order)
        return orders
    
    def placeOrder(self, stand, ticket, positionList):
        data = self.readData()
        time = 0
        price = 0
        positions = {}

        #add positions
        counter = 1
        for p in positionList:
            prod = data["Products"][p["product"]]
            price += p["quantity"] * prod["price"]
            time += p["quantity"] * prod["time"]
            positions[str(counter)] = p

            #update quantity for stand
            for sp in data["Stands"][stand]["products"]:
                if sp["product"] == p["product"]:
                    sp["quantity"] = sp["quantity"] - p["quantity"]

            counter += 1
            

        #add order
        data["Orders"][data["GlobalIDs"]["Orders"]] = {"time": time, "price": price, "status": "1", "positions": positions}

        #add order2stand
        data["Order2Stand"][data["GlobalIDs"]["Order2Stand"]] = {"order": str(data["GlobalIDs"]["Orders"]), "stand": stand}

        #add order2ticket
        data["Order2Ticket"][data["GlobalIDs"]["Order2Ticket"]] = {"order": str(data["GlobalIDs"]["Orders"]), "ticket": ticket}

        #update ids
        data["GlobalIDs"]["Orders"] = data["GlobalIDs"]["Orders"] + 1
        data["GlobalIDs"]["Order2Stand"] = data["GlobalIDs"]["Order2Stand"] + 1
        data["GlobalIDs"]["Order2Ticket"] = data["GlobalIDs"]["Order2Ticket"] + 1

        self.writeData(data)

    def getCreditForTicket(self, ticket):
        return self.readData()["Tickets"][ticket]["credit"]
    
    def searchStand(self, standStr):
        data = self.readData()
        rData = []
        for stand in data["Stands"]:
            if stand.startswith(standStr):
                standData = data["Stands"][stand]
                #append stand number
                standData["stand"] = stand
                rData.append(standData)
        return rData
        
    def checkLogin(self, ticket, password):
        data = self.readData()
        for t in data["Tickets"]:
            if t == ticket:
                if data["Tickets"][t]["password"] == password:
                    return True
                else:
                    return False 

database = Database()

# print(database.getproductsForStand("1"))
# print(database.getproductsForStand("3"))

# print(database.getOrdersForTicket("1234567"))
# print(database.getOrdersForTicket("8910111"))

#print(database.getOrdersForStand("1"))

#database.adjustTimers()

#database.placeOrder("2", "8910111", [{"product": "3", "quantity": 1}])


