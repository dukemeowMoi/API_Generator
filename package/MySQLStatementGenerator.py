from package.StatementGenerator import StatementGenerator

class MySQLStatementGenerator(StatementGenerator):

    def generateInsertStatementCode(self, api):
        sql = "INSERT INTO %s set ?" %(api.relatedEntity)
        body = self.getCommonHeader(api)
        body += "let query = '%s';\n" %(sql)
        body += self.checkAndFilterAttributes(api)
        body += "sql.query(query,atts,(err,result)=>{if(err){console.log('error:',err);res.status(500).send(err);return;}res.send(result);});\n"
        body += self.getCommonFooter()
        return body

    def generateUpdateStatementCode(self, api):
        sql = "Update %s SET ? where [cons]" %(api.relatedEntity)
        body = self.getCommonHeader(api)
        body += "let query = '%s';\n" %(sql)
        body += self.checkAndFilterAttributes(api)
        body += self.checkAndFilterConstraints(api)
        body += "sql.query(query,[atts, Object.values(cons)],(err,result)=>{if(err){console.log('error:',err);res.status(500).send(err);return;}res.send(result);});\n"
        body += self.getCommonFooter()
        return body

    def generateSelectStatementCode(self, api):
        attributes = ",".join(api.attributes)
        sql = "SELECT %s FROM %s where [cons]" %(attributes, api.relatedEntity)
        body = self.getCommonHeader(api)
        body += "let query = '%s';\n" %(sql)
        body += self.checkAndFilterConstraints(api)
        body += "sql.query(query,Object.values(cons),(err,result)=>{if(err){console.log('error:',err);res.status(500).send(err);return;}res.send(result);});\n"
        body += self.getCommonFooter()
        return body
    
    def generateDeleteStatementCode(self, api):
        sql = "DELETE FROM %s where [cons]" %(api.relatedEntity)
        body = self.getCommonHeader(api)
        body += "let query = '%s';\n" %(sql)
        body += self.checkAndFilterConstraints(api)
        body += "sql.query(query,Object.values(cons),(err,result)=>{if(err){console.log('error:',err);res.status(500).send(err);return;}res.send(result);});\n"
        body += self.getCommonFooter()
        return body

    def checkAndFilterAttributes(self, api):
        body = "var attributes = [%s];\n" %(",".join("'"+c+"'" for c in api.attributes))
        body += "if (!attributes.every(a => Object.keys(parameters).includes(a)) || attributes.length == 0){\n"
        body += "console.log('error: ', 'Attributes not match');"
        body += "res.status(500).send('Attributes not match');"
        body += "return;"
        body += "}\n"
        body += "var atts = Object.fromEntries(Object.entries(parameters).filter(([k]) => attributes.includes(k)));\n"
        return body

    def checkAndFilterConstraints(self, api):
        body = "var constraints = [%s];\n" %(",".join("'"+c+"'" for c in api.constraints))
        body += "if (!constraints.every(a => Object.keys(parameters).includes(a))){\n"
        body += "console.log('error: ', 'Constraints not match');"
        body += "res.status(500).send('Constraints not match');"
        body += "return;"
        body += "}\n"
        body += "var cons = Object.fromEntries(Object.entries(parameters).filter(([k]) => constraints.includes(k)));\n"
        body += "if (Object.keys(cons).length == 0) cons[1] = 1;"
        body += "var keys = Object.keys(cons).map(k => k + '= ?');\n"
        body += "query = query.replace('[cons]', keys.join(' AND '));\n"
        return body

    def getCommonHeader(self, api):
        header = ""
        if api.httpMethod == "get":
            header += "router.get('[slug]', (req, res) => {\n".replace('[slug]', api.slug)
            header += "var parameters = req.query;\n"
        else:
            header += "router.post('[slug]', (req, res) => {\n".replace('[slug]', api.slug)
            header += "var parameters = req.body;\n"
        
        return header


    def getCommonFooter(self):
        footer = "});\n"
        return footer
