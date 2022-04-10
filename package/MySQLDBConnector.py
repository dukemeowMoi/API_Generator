from package.DBConnector import DBConnector

import mysql.connector
from package.Models.Template import Template

from package.MySQLStatementGenerator import MySQLStatementGenerator

from shutil import copy

class SQLDBConnector(DBConnector):
    def __init__(self, serverHostName, serverPort, userName, password, database, statementGenerator):
        super().__init__("MySQL")
        self.serverHostName = serverHostName
        self.serverPort = serverPort
        self.userName = userName
        self.password = password
        self.database = database
        self.statementGenerator = statementGenerator

    def connect(self):
        self.mydb = mysql.connector.connect(
            host = self.serverHostName,
            user = self.userName,
            password = self.password,
            database = self.database
        )
        print(self.mydb)

    def insert(self, tableName, attributes):
        print("insert")

        fieldStr = ",".join(attributes["fields"])
        valueStr = ",".join(['%s'] * len(attributes["fields"]))

        mycursor = self.mydb.cursor()

        sql = "INSERT INTO %s (%s) VALUES (%s)" %(tableName, fieldStr, valueStr)
        val = attributes["values"]
        mycursor.execute(sql, val)

        self.mydb.commit()

        print("1 record inserted, ID:", mycursor.lastrowid)
        return mycursor.lastrowid
    
    def computeConstraints(self, connector, constraints):
        tempAry = []
        for cons in constraints:
            print(cons)
            if (cons == "OR" or cons == "AND"):
                tempAry.append(self.computeConstraints(cons, constraints[cons]))
            else:
                if len(cons) == 3:
                    cons["value"] = self.stringifyVariable(cons["value"])
                    tempAry.append(cons["field"]+cons["comparator"]+cons["value"])
                else:
                    tempAry.append(self.computeConstraints("", cons))
                    
        return " ("+(" "+connector+" ").join(tempAry)+") "

    def update(self, tableName, attributes):
        print("update")

        tmpAry = []
        for field in attributes["fields"]:
            tmpAry.append(field["field"] + " = " + self.stringifyVariable(field["value"]))
        setStr = ",".join(tmpAry)
        
        constraintStr = self.computeConstraints("", attributes["constraints"])

        mycursor = self.mydb.cursor()

        sql = "UPDATE %s SET %s WHERE %s" %(tableName, setStr, constraintStr)
        mycursor.execute(sql)

        self.mydb.commit()

        print(mycursor.rowcount, "record(s) affected")
        return mycursor.rowcount

    def select(self, tableName, attributes):
        print("select")
        fieldStr = ",".join(attributes["fields"])
        constraintStr = self.computeConstraints("", attributes["constraints"])
        print(constraintStr)
        mycursor = self.mydb.cursor()

        sql = "SELECT %s FROM %s WHERE %s" %(fieldStr, tableName, constraintStr)
        mycursor.execute(sql)

        result = mycursor.fetchall()

        return result
    
    def delete(self, tableName, attributes):
        print("delete")
        
        constraintStr = self.computeConstraints("", attributes["constraints"])

        mycursor = self.mydb.cursor()

        sql = "DELETE FROM %s WHERE %s" %(tableName, constraintStr)
        mycursor.execute(sql)

        self.mydb.commit()

        print(mycursor.rowcount, "record(s) affected")
        return mycursor.rowcount

    def generateCodeByTemplate(self, template):
        print("generate")

        # Read in the file
        with open('./templateCode/MySQL/db.js', 'r') as file :
            filedata = file.read()

            # Replace the target string
            filedata = filedata.replace('[hostname]', self.serverHostName)
            filedata = filedata.replace('[username]', self.userName)
            filedata = filedata.replace('[password]', self.password)
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

        
        

    def stringifyVariable(self, var):
        if (isinstance(var, str)):
            var = "'"+var+"'"
        else:
            var = str(var)
        return var

# Test Statement
# connector = SQLDBConnector("localhost", "3306", "ma", "789987", "fyp", MySQLStatementGenerator())
# with open('./Template/fyp_website_template.json', 'r') as file :
#     filedata = file.read()
#     template = Template()
#     template.createTemplate(filedata)
#     connector.generateCodeByTemplate(template)
# connector.connect()
# result = connector.insert("page", {"fields":["page_slug", "page_title", "page_content"], "values":["index", "Home", "Hello World"]})
# result = connector.update("page", {"fields": [{"field":"page_title", "value":"Home2"}, {"field":"page_content", "value":"Hello World2"}], "constraints": [{"field": "page_slug", "comparator": "=", "value": "index"}]})
# result = connector.select("page", {"fields": ["*"], "constraints": [{"field": "page_slug", "comparator": "=", "value": "index"}]})
# result = connector.delete("page", {"constraints": [{"field": "page_title", "comparator": "=", "value": "Home2"}]})
# print(result)
