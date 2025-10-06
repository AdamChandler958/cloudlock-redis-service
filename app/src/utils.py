import redis
from dotenv import load_dotenv
import os

load_dotenv()

REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_PORT = os.getenv("REDIS_PORT")


def get_redis_client():
    r = redis.Redis(host="redis", port=REDIS_PORT, db=0, password=REDIS_PASSWORD)
    return r
