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
        # print('-------dbname  connection mongo--------------',dbname)
        #client = MongoClient(self.MONGO_CONNECTION_STRING)
        db_connection = self.client.founder_suite
        return db_connection


    # def get_celery_client(self):
    #     celery = self.client["celery_workers"]
    #     return celery

    def close_mongodb_connection(self):
        self.client.close()
        return



def mongo_connection_check():
    mongo_conn_obj = Connection()
    db_conn = mongo_conn_obj.get_mongodb_connection()
    data=db_conn.users
    startup=db_conn.startup
    temp_form_db=db_conn.temp_form_db
    verify_link=db_conn.verify_link
    startup_info=startup.find()
    temp_form_db_info=temp_form_db.find()
    verify_link_info=verify_link.find()
    user= data.find()
    print("Mongo Connection success",str(db_conn))
    mongo_conn_obj.close_mongodb_connection()

