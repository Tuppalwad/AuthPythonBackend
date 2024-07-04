import os
from dotenv import load_dotenv
from Mongo_Connection.connection import Connection

dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path, verbose=True)

# or os.environ.get("MONGO_CONNECTION_STRING")
mongo_connection_string = os.getenv("MONGO_CONNECTION_STRING")
secret_key = os.getenv("SECRET_KEY")
MJ_APIKEY_PUBLIC=os.getenv("MJ_APIKEY_PUBLIC")
MJ_APIKEY_PRIVATE=os.getenv("MJ_APIKEY_PRIVATE")
BACKEND_URL=os.getenv("BACKEND_URL")
APP_URL=os.getenv("APP_URL")
FROM_EMAIL_ID=os.getenv("FROM_EMAIL_ID")

S3_BUCKET =os.getenv("S3_BUCKET")
S3_KEY =os.getenv("S3_KEY")
S3_SECRET =os.getenv("S3_SECRET")
FLASK_PORT =os.getenv("FLASK_PORT")
FLASK_DEBUG =os.getenv("FLASK_DEBUG")  # this value will be of type STRING

mongo_conn_obj = Connection()
