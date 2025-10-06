from fastapi import FastAPI, Depends
from app.src.utils import get_redis_client
import uvicorn
from typing import Annotated
from redis import Redis

app = FastAPI()


@app.get("/")
def ready_status(client: Annotated[Redis, Depends(get_redis_client)]):
    client.echo("Redis is responding")
    return {"message": "Cloudlock redis service is running..."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3080, log_config=None)
