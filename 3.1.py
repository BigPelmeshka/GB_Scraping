from ScrapingJob import ScrapingJob
from pymongo import MongoClient
import json
from pprint import pprint

sj = ScrapingJob.sj('python','1')

mongodb_uri = 'localhost:27017'
db_name = 'vacancy'
collection_name = 'vacancy_db'

mongodb = MongoClient(mongodb_uri)
db = mongodb[db_name]
collection = db[collection_name]
records = sj.to_dict('records')

db.vacancy_db.insert_many(records)

db.vacancy_db.update_one({'name': 'Automation QA Engineer / Тестировщик (Python)'}, 
                                 {'$set': {'salary':'100 000'}})

[x for x in db.vacancy_db.find({'Наименование вакансии': 'Automation QA Engineer / Тестировщик (Python)'})]