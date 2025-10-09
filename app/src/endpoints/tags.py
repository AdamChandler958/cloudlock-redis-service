from fastapi import APIRouter, Depends, HTTPException
from app.src.logger import setup_logger
from app.src.utils import get_redis_client
from typing import Annotated
from redis import Redis

from app.src.crud.tags import retrieve_tags
from app.src.models.MetadataKey import MetadataKey
import json

router = APIRouter(prefix="/tags", tags=["tags", "metadata"])
logger = setup_logger()


@router.get("/{metadata_key}")
def get_tags_for_item(
    metadata_key: MetadataKey, redis_client: Annotated[Redis, Depends(get_redis_client)]
):
    key = f"metadata:{metadata_key.bucket_name}:{metadata_key.file_name}"
    logger.info(f"Received request to retrieve tags for item {key}")

    try:
        tags = retrieve_tags(metadata_key=key, redis_client=redis_client)
        if tags is None:
            raise ValueError
    except ValueError:
        logger.error(f"No item with key {key} exists.")
        raise HTTPException(404, f"No item with key {key} exists.")

    tag_list = json.dumps(tags)
    logger.info(f"Retrieval of tags for item {key} was successful")
    return tag_list
