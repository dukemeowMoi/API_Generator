class DBConnector:
    def __init__(self, type):
        self.type = type

    def connect(self):
        print("connect")

    def insert(self, attributes):
        print("insert")

    def update(self, attributes):
        print("update")

    def select(self, attributes):
        print("select")
    
    def delete(self, attributes):
        print("delete")

    def generateAPI(self, api):
        print("generate")

    def stringifyVariable(self, var):
        print("stringify")