from package.StatementGenerator import StatementGenerator

class MongoDBStatementGenerator(StatementGenerator):

    def generateInsertStatementCode(self, api):
        body = self.getCommonHeader(api)
        body += self.checkAndFilterAttributes(api)
        body += "conn.collection('%s').insertOne(atts, function(err, result) {\n" %(api.relatedEntity)
        body += "if (err) {res.status(500).send('Error inserting %s');}\n" %(api.relatedEntity)
        body += "else {res.status(204).send()}\n"
        body += "});\n"
        body += self.getCommonFooter()
        return body

    def generateUpdateStatementCode(self, api):
        body = self.getCommonHeader(api)
        body += self.checkAndFilterAttributes(api)
        body += self.checkAndFilterConstraints(api)
        body += "conn.collection('%s').updateMany(cons, {$set: atts},function(err, result) {\n" %(api.relatedEntity)
        body += "if (err) {res.status(500).send('Error deleting %s');}\n" %(api.relatedEntity)
        body += "else {res.status(204).send()}\n"
        body += "});\n"
        body += self.getCommonFooter()
        return body

    def generateSelectStatementCode(self, api):
        body = self.getCommonHeader(api)
        body += self.checkAndFilterConstraints(api)
        body += "atts = {%s};\n" %(",".join("'"+a+"' : 1" for a in api.attributes))
        body += "conn.collection('%s').find(cons).project(atts).toArray(function(err, result) {\n" %(api.relatedEntity)
        body += "if (err) {res.status(500).send('Error finding %s');}\n" %(api.relatedEntity)
        body += "else {res.json(result);}\n"
        body += "});\n"
        body += self.getCommonFooter()
        return body
    
    def generateDeleteStatementCode(self, api):
        body = self.getCommonHeader(api)
        body += self.checkAndFilterConstraints(api)
        body += "conn.collection('%s').deleteMany(cons, function(err, result) {\n" %(api.relatedEntity)
        body += "if (err) {res.status(500).send('Error deleting %s');}\n" %(api.relatedEntity)
        body += "else {res.status(204).send()}\n"
        body += "});\n"
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
        body += "if (Object.keys(cons).includes('_id')) cons['_id'] = new sql.mongoDB.ObjectId(cons['_id']);\n"
        return body

    def getCommonHeader(self, api):
        header = ""
        if api.httpMethod == "get":
            header += "router.get('[slug]', (req, res) => {\n".replace('[slug]', api.slug)
            header += "var parameters = req.query;\n"
        else:
            header += "router.post('[slug]', (req, res) => {\n".replace('[slug]', api.slug)
            header += "var parameters = req.body;\n"
        header += "sql.getConnection().then(conn => {\n"
        return header


    def getCommonFooter(self):
        footer = "}, err => res.status(500).send('Error connecting DB'));\n"
        footer += "});\n"
        return footer
