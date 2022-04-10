import spacy
from package.Models.API import API
from package.Models.Template import Template
from package.Models.Module import Module
from package.MySQLDBConnector import SQLDBConnector
from package.MySQLStatementGenerator import MySQLStatementGenerator

def predict(predictText):
    type_nlp = spacy.load("./trainning_output/type/model-last")
    type_doc = type_nlp(predictText)

    API_type = type_doc.ents[0].label_

    print(API_type)

    if (API_type == "select"):
        API_httpMethod = "get"
    else:
        API_httpMethod = "post"

    entity_nlp = spacy.load("./trainning_output/entity/model-last")
    entity_doc = entity_nlp(predictText)
    
    API_relatedEntity = entity_doc.ents[0].text
    
    #print(API_relatedEntity)

    API_slug = "/"+API_type+"/"+API_relatedEntity

    attribute_nlp = spacy.load("./trainning_output/attribute/model-last")
    attributes_doc = attribute_nlp(predictText)

    API_attributes = []
    for ent in attributes_doc.ents:
        #print(ent)
        API_attributes.append(ent.text.lower().replace(" ", "_"))

    api = API(
        API_type+"_"+API_relatedEntity,
        API_type+"_"+API_relatedEntity,
        API_slug,
        API_httpMethod,
        API_type,
        API_relatedEntity,
        API_attributes,
        [])

    return api



