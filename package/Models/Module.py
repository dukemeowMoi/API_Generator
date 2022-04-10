class Module:
      def __init__(self, name, id, apiList):
        self.name = name
        self.id = id
        self.apiList = apiList

      def exportAsJson(self):
         return {
            "name":self.name,
            "id":self.id,
            "APIs": [api.exportAsJson() for api in self.apiList]
         }