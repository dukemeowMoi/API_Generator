# API_Generator
 
This application aims to provide efficient and convenient way for developers to generate API coding in NodeJS format.

## Install

```bash
$ pip install mysql.connector
$ pip install pymongo
$ pip install dnspython
$ pip install flask
$ pip install spacy
$ pip install flask
$ python -m spacy download en_core_web_lg
```
## Start Program

```bash
$ py main.py
```

## Train models
Step 1: Prepare the training dataset and development dataset according to csv files provided in ./trainning_data folder

Step 2: Choose which model you target to train by modifying the path variable in ./trainning.py

Step 3: Compute the ./trainning.py file to generate .spacy file

```bash
$ py trainning.py
```

Step 4: Train the model by using trainning command provided by Spacy framework<br>

Trainning modal for predicting API Related Entity: <br>
```bash
py -m spacy train .\config.cfg --output .\trainning_output\type --paths.train .\trainning_data\entity\train.spacy --paths.dev .\trainning_data\entity\dev.spacy
```

Trainning modal for predicting API Type: <br>
```bash
py -m spacy train .\config.cfg --output .\trainning_output\type --paths.train .\trainning_data\type\train.spacy --paths.dev .\trainning_data\type\dev.spacy
```

Trainning modal for predicting API Related Attributes: <br>
```bash
py -m spacy train .\config.cfg --output .\trainning_output\type --paths.train .\trainning_data\attribute\train.spacy --paths.dev .\trainning_data\attribute\dev.spacy
```
