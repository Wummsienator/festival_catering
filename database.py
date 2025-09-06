import json
import datetime

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
            o2t_obj = data["Order2Ticket"][o2t]
            if o2t_obj["ticket"] == ticket:
                order = data["Orders"][o2t_obj["order"]]
                #append order number
                order["order"] = o2t_obj["order"]
                #append stand number
                for o2s in data["Order2Stand"]:
                    o2s_obj  = data["Order2Stand"][o2s]
                    if o2s_obj ["order"] == o2t_obj["order"]:
                        order["stand"] = o2s_obj ["stand"]
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
            o2s_obj  = data["Order2Stand"][o2s]
            if o2s_obj ["stand"] == stand:
                order = data["Orders"][o2s_obj ["order"]]
                #append order number
                order["order"] = o2s_obj ["order"]
                #append stand number
                order["stand"] = stand      
                #get status description
                for s in data["Status"]:
                    if s == order["status"]:
                        order["status_desc"] = data["Status"][s]
        orders.append(order)
        return orders
    
    def placeOrder(self, stand, ticket, position_list, price, special_requests):
        data = self.readData()
        time = 0
        price = 0
        positions = {}

        #add positions
        counter = 1
        for p in position_list:
            prod = data["Products"][p["product"]]
            price += p["quantity"] * prod["price"]
            time += p["quantity"] * prod["time"]
            positions[str(counter)] = p

            #update quantity for stand
            for sp in data["Stands"][stand]["products"]:
                if sp["product"] == p["product"]:
                    sp["quantity"] = sp["quantity"] - p["quantity"]

            counter += 1
            
        #get timestamp
        x = datetime.datetime.now()
        timestamp = str(x.day) + "." + str(x.month) + "." + str(x.year) + " - " + str(x.hour) + ":" + str(x.minute)

        #add order
        data["Orders"][data["GlobalIDs"]["Orders"]] = {"time": time, "timestamp": timestamp, "price": price, "status": "1", "specialRequests": special_requests, "positions": positions}

        #add order2stand
        data["Order2Stand"][data["GlobalIDs"]["Order2Stand"]] = {"order": str(data["GlobalIDs"]["Orders"]), "stand": stand}

        #add order2ticket
        data["Order2Ticket"][data["GlobalIDs"]["Order2Ticket"]] = {"order": str(data["GlobalIDs"]["Orders"]), "ticket": ticket}

        #update ids
        data["GlobalIDs"]["Orders"] = data["GlobalIDs"]["Orders"] + 1
        data["GlobalIDs"]["Order2Stand"] = data["GlobalIDs"]["Order2Stand"] + 1
        data["GlobalIDs"]["Order2Ticket"] = data["GlobalIDs"]["Order2Ticket"] + 1

        #update credit for ticket
        data["Tickets"][ticket]["credit"] = data["Tickets"][ticket]["credit"] - price

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

    def getProductsForStand(self, stand):
        data = self.readData()
        products = []

        #find stand
        for s in data["Stands"]:
            if s == stand:
                stProd = data["Stands"][s]["products"]
                #get product informations
                for stP in stProd:
                    for p in data["Products"]:
                        if stP["product"] == p:
                            productData = data["Products"][p]
                            #append product id
                            productData["product"] = p
                            #append quantity
                            productData["quantity"] = stP["quantity"]
                            
                            products.append(productData)
        return products
    
    def addCreditForTicket(self, ticket, amount):
        data = self.readData()
        for t in data["Tickets"]:
            if t == ticket:
                data["Tickets"][t]["credit"] = data["Tickets"][t]["credit"] + amount

        self.writeData(data)

    def connectOrderToTicket(self, order, ticket):
        if self.checkOrder2TicketExists(order, ticket):
            return

        data = self.readData()
        for t in data["Tickets"]:
            if t == ticket:
                #add order2ticket
                data["Order2Ticket"][data["GlobalIDs"]["Order2Ticket"]] = {"order": order, "ticket": ticket}
                #update id
                data["GlobalIDs"]["Order2Ticket"] = data["GlobalIDs"]["Order2Ticket"] + 1
                self.writeData(data)

    def checkOrder2TicketExists(self, order, ticket):
        data = self.readData()
        for o2t in data["Order2Ticket"]:
            if data["Order2Ticket"][o2t]["order"] == order and data["Order2Ticket"][o2t]["ticket"] == ticket:
                return True
        return False

    def checkLogin(self, ticket, password):
        data = self.readData()
        for t in data["Tickets"]:
            if t == ticket:
                if data["Tickets"][t]["password"] == password:
                    return True
                else:
                    return False 



