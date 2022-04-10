from package.DBConnector import DBConnector
from pymongo import MongoClient
import pymongo

from shutil import copy
from package.Models.Template import Template
from package.MongoDBStatementGenerator import MongoDBStatementGenerator

class MongoDBConnector(DBConnector):
    def __init__(self, connectionStr, database, statementGenerator):
        super().__init__("Mongo")
        self.connectionStr = connectionStr
        self.database = database
        self.statementGenerator = statementGenerator

    def connect(self):
        self.client = MongoClient(self.connectionStr)
        self.db = self.client[self.database]

    def insert(self, tableName, attributes):
        print("insert")

        tmpObj = {}
        for idx, attribute in enumerate(attributes['fields']):
            tmpObj[attribute] = attributes['values'][idx]

        self.db[tableName].insert_one(tmpObj)

    def computeComparator(self, var):
        return {
        '=': "$eq",
        '>=': "$gte",
        '>': "$gt",
        '<=': "$lte",
        '<': "$lt",
        '!=': "$ne",
        }.get(var,'$eq')
    
    def computeConnector(self, var):
        return {
        'AND': "$and",
        'OR': "$or",
        }.get(var,'$and')

    def computeConstraints(self, connector, constraints):
        tempAry = []
        for cons in constraints:
            if (cons == "OR" or cons == "AND"):
                tempAry.append(self.computeConstraints(cons, constraints[cons]))
            else:
                if len(cons) == 3:
                    tempAry.append({cons["field"]: {self.computeComparator(cons["comparator"]):cons["value"]}})
                else:
                    tempAry.append(self.computeConstraints("", cons))
                    
        return {self.computeConnector(connector):tempAry}

    def update(self, tableName, attributes):
        print("update")

        tmpObj = {}
        for attribute in attributes['fields']:
            tmpObj[attribute['field']] = attribute['value']

        filterAry = self.computeConstraints("",attributes['constraints'])
        print(filterAry)

        result = self.db[tableName].update_one(filterAry, {"$set": tmpObj})

        return result.modified_count
    

    def select(self, tableName, attributes):
        print("select")

        fieldAry = {}
        for field in attributes['fields']:
            fieldAry[field] = 1

        filterAry = self.computeConstraints("",attributes['constraints'])
        print(filterAry)
        print(fieldAry)
        result = self.db[tableName].find(filterAry, fieldAry)
        return result
       
    
    def delete(self, tableName, attributes):
        print("delete")

        filterAry = self.computeConstraints("",attributes['constraints'])
        print(filterAry)

        result = self.db[tableName].delete_one(filterAry)

        return result.deleted_count

    def generateCodeByTemplate(self, template):
        print("generate")

        # Read in the file
        with open('./templateCode/MongoDB/db.js', 'r') as file :
            filedata = file.read()

            # Replace the target string
            filedata = filedata.replace('[connectionStr]', self.connectionStr)
            filedata = filedata.replace('[database]', self.database)

            # Write the file out again
            with open('./GenerateCode/db.js', 'w') as file:
                file.write(filedata)

        copy('./templateCode/server.js', './GenerateCode/server.js')

        with open('./templateCode/api.js', 'r') as file :
            apifiledata = file.read()

            apiStrs = ""

            for module in template.modules:
                for api in module.apiList:
                    if api.type == "insert":
                        apiStrs += self.statementGenerator.generateInsertStatementCode(api)
                    else:
                        if api.type == "update":
                            apiStrs += self.statementGenerator.generateUpdateStatementCode(api)
                        else:
                            if api.type == "select":
                                apiStrs += self.statementGenerator.generateSelectStatementCode(api)
                            else:
                                if api.type == "delete":
                                    apiStrs += self.statementGenerator.generateDeleteStatementCode(api)
            
            apifiledata = apifiledata.replace('[api_code]', apiStrs)
        
            # Write the file out again
            with open('./GenerateCode/api.js', 'w') as file:
                file.write(apifiledata)
# Test Statement
# connector = MongoDBConnector("mongodb+srv://ma:789987@fyp.cf4gh.mongodb.net/?retryWrites=true&w=majority", "fyp", MongoDBStatementGenerator())
# with open('./Template/fyp_website_template.json', 'r') as file :
#     filedata = file.read()
#     template = Template()
#     template.createTemplate(filedata)
#     connector.generateCodeByTemplate(template)
# connector.connect()
# result = connector.insert("page", {"fields":["page_slug", "page_title", "page_content"], "values":["index", "Home", "Hello World"]})
# result = connector.update("page", {"fields": [{"field":"page_title", "value":"Home"}, {"field":"page_content", "value":"Hello World2"}], "constraints": {"AND":[{
# 	"field":"page_title",
# 	"comparator": "=",
# 	"value": "Home2"
# },{
# 	"OR": [{
# 	"field":"page_slug",
# 	"comparator": "=",
# 	"value": "index"},
# 	{
# 	"field":"page_slug",
# 	"comparator": "=",
# 	"value": "home"}]
# }]}})
# result = connector.update("page", {"fields": [{"field":"page_title", "value":"Home"}, {"field":"page_content", "value":"Hello World"}], "constraints": [{"field": "page_slug", "comparator": "=", "value": "index"}]})
# result = connector.select("page", {"fields": ["page_slug", "page_title"], "constraints": [{"field": "page_slug", "comparator": "=", "value": "index"}]})
# result = connector.delete("page", {"constraints": [{"field": "page_title", "comparator": "=", "value": "Home"}]})
# print(result)
