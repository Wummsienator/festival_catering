import json

class Database:
    def __init__(self):
        self.data = None
        self.readData()
        return
    
    def readData(self):
        # Read from file and parse JSON
        with open("data.json", "r") as f:
            data = json.load(f)
        self.data = data

    def getData(self):
        return self.data

database = Database()
data = database.getData()

print(data)
