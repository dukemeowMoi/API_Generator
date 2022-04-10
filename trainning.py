import spacy
from spacy.tokens import DocBin

import csv
from pathlib import Path

def findTextInString(Str, text, e):
    sPos = Str.find(text)
    ePos = sPos + len(text)
    return sPos, ePos, e

def load_training_data(filename):
    output_dir = Path.cwd()
    data_loc = output_dir / filename

    TRAIN_DATA = []

    with data_loc.open("r", encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=";")
        for row in csvreader:
            if (len(row[1].split(",")) == 1):
                TRAIN_DATA.append((row[0], [(findTextInString(row[0], row[1], row[2]))]))
            else:
                keywords = row[1].split(",")
                spans = []
                for keyword in keywords:
                    spans.append(findTextInString(row[0], keyword, row[2]))
                TRAIN_DATA.append((row[0], spans))

    return TRAIN_DATA


nlp = spacy.load("en_core_web_lg")

ner=nlp.get_pipe("ner")

typePath = "./trainning_data/type/"
entityPath = "./trainning_data/entity/"
attributePath = "./trainning_data/attribute/"
path = typePath

TRAIN_DATA = load_training_data(path+"training.csv")
DEV_DATA = load_training_data(path+"dev.csv")

# the DocBin will store the example documents
db = DocBin()
for text, annotations in TRAIN_DATA:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations:
        span = doc.char_span(start, end, label=label)
        ents.append(span)
    doc.ents = ents
    db.add(doc)
db.to_disk(path+"/train.spacy")

db = DocBin()
for text, annotations in DEV_DATA:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations:
        span = doc.char_span(start, end, label=label)
        ents.append(span)
    doc.ents = ents
    db.add(doc)
db.to_disk(path+"/dev.spacy")
    