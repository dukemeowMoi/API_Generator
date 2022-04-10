import json

from .API import API
from .Module import Module

class Template:
    def createTemplate(self, content):
        data = json.loads(content)
        self.name = data["name"]
        self.id = data["id"]
        
        moduleList = []
        for module in data['modules']:
            apiList = []
            for api in module["APIs"]:
                apiObj = API(
                    api["name"],
                    api["id"],
                    api["slug"],
                    api["httpMethod"],
                    api["type"],
                    api["relatedEntity"],
                    api["attributes"] if 'attributes' in api else [],
                    api["constraints"] if 'constraints' in api else [])
                apiList.append(apiObj)
            moduleObj = Module(module["name"], module["id"], apiList)
            moduleList.append(moduleObj)

        self.modules = moduleList


    def exportAsJson(self):
         return {
            "name":self.name,
            "id":self.id,
            "modules": [module.exportAsJson() for module in self.modules]
         }