from fastapi import APIRouter, Depends, HTTPException
from app.src.logger import setup_logger
from app.src.utils import get_redis_client
from typing import Annotated
from redis import Redis

from app.src.crud.tags import retrieve_tags, create_tag
import json

router = APIRouter(prefix="/tags", tags=["tags", "metadata"])
logger = setup_logger()


@router.get("/{file_name}")
async def get_tags_for_item(
    file_name: str,
    bucket_name: str,
    redis_client: Annotated[Redis, Depends(get_redis_client)],
):
    key = f"metadata:{bucket_name}:{file_name}"
    logger.info(f"Received request to retrieve tags for item {key}")

    try:
        tags = retrieve_tags(metadata_key=key, redis_client=redis_client)
        if tags is None:
            raise ValueError
    except ValueError:
        logger.error(f"No item with key {key} exists.")
        raise HTTPException(404, f"No item with key {key} exists.")

    tag_list = json.loads(tags)
    logger.info(f"Retrieval of tags for item {key} was successful")
    return tag_list


@router.post("/{metadata_key}")
def add_tag_to_existing_object(
    bucket_name: str,
    file_name: str,
    tag: str,
    redis_client: Annotated[Redis, Depends(get_redis_client)],
):
    metadata_key = f"metadata:{bucket_name}:{file_name}"
    logger.info(f"Received request to add tag {tag} to item {metadata_key}")

    if create_tag(
        metadata_key=metadata_key, new_tag_val=tag, redis_client=redis_client
    ):
        return {
            "message": f"Tag {tag} added to file {metadata_key} succesfully request complete"
        }
    else:
        raise HTTPException(404, f"File {metadata_key} does not exist")
