from flask import Flask, render_template, request, jsonify, send_file, abort
from package.Models.Template import Template 
from NLP import predict
from package.MySQLDBConnector import SQLDBConnector
from package.MySQLStatementGenerator import MySQLStatementGenerator
from package.MongoDBConnector import MongoDBConnector
from package.MongoDBStatementGenerator import MongoDBStatementGenerator
from zipfile import ZipFile
import os
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getTemplateDetail', methods=['POST'])
def getTemplateDetail():
    data = request.files.get('file')
    template = Template()
    template.createTemplate(data.read())
    
    return jsonify(template.exportAsJson())

@app.route('/generateCode', methods=['POST'])
def generateCode():
    obj = request.get_json(force=True)
    template = Template()
    template.createTemplate(json.dumps(obj['data']))
    if (obj['connector'] == "mySQL"):
        connector = SQLDBConnector("[host]", "[port]", "[username]", "[password]", "[table name]", MySQLStatementGenerator())
    else:
        connector = MongoDBConnector("[connectionStr]", "[Table name]", MongoDBStatementGenerator())
    connector.generateCodeByTemplate(template)
    zipObj = ZipFile('templateZip/'+template.name+'.zip', 'w')
    zipObj.write('GenerateCode/api.js')
    zipObj.write('GenerateCode/db.js')
    zipObj.write('GenerateCode/server.js')
    zipObj.write('GenerateCode/readme.txt')
    zipObj.write('GenerateCode/install.bat')
    zipObj.write('GenerateCode/start.bat')
    zipObj.close()
    return '/templateZip/'+template.name+'.zip'

@app.route('/templateZip/<zipFile>')
def getZipFile(zipFile):
    try:
        return send_file('templateZip/'+zipFile, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route('/getNLPResult', methods=['POST'])
def getNLPResult():
    text = request.values.get("text")
    try:
        api = predict(text)
        return jsonify({"status":True, "data":api.exportAsJson()})
    except Exception:
        return jsonify({"status":False, "data":"No API found."})

if __name__ == '__main__':
    app.run(debug=False)


# testStr = "create an api to add a product containing title, description, product category"
# api = predict(testStr)
# print(
#     api.id,
#     api.name,
#     api.slug,
#     api.relatedEntity,
#     api.type,
#     api.attributes)
