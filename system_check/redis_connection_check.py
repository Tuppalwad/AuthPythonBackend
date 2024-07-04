import redis
import os
from dotenv import load_dotenv

load_dotenv()
REDIS_URL= os.environ.get("REDIS_URL_STRING","BAD_GETWAY_KAY")


def redis_connection_check():
    r = redis.from_url(REDIS_URL) # short timeout for the test
    r.ping()
    print('connected to redis "{}"'.format(REDIS_URL))
    r.close()