from pymongo import MongoClient
mongo_conn = MongoClient('localhost', 2717)
mongo_cli = mongo_conn['bet_control']
