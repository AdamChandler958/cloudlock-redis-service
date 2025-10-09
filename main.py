from fastapi import FastAPI, Depends
from app.src.utils import get_redis_client
import uvicorn
from typing import Annotated
from redis import Redis
from app.src.logger import setup_logger
from app.src.endpoints import metadata, tags


app = FastAPI()

logger = setup_logger()

app.include_router(metadata.router)
app.include_router(tags.router)


@app.get("/")
def ready_status(client: Annotated[Redis, Depends(get_redis_client)]):
    logger.info("Starting redis-api-service...")
    try:
        client.echo("Redis is responding")
    except Exception as e:
        logger.critical(f"Redis is not responding with exception: {e}")
    logger.info("Redis is responding")
    return {"message": "Cloudlock redis service is running..."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3080, log_config=None)
