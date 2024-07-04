from pymongo import MongoClient
import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path, verbose=True)

mongo_connection_string = os.getenv("MONGO_CONNECTION_STRING")


class Connection(object):
    def __init__(self):
        self.MONGO_CONNECTION_STRING = mongo_connection_string
        # print(self.MONGO_CONNECTION_STRING)
        self.client = MongoClient(self.MONGO_CONNECTION_STRING)

    def get_mongodb_connection(self):
      
        db_connection = self.client.Ecommerce
        return db_connection


    def close_mongodb_connection(self):
        self.client.close()
        return
