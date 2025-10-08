from fastapi import APIRouter, Depends, HTTPException
from app.src.logger import setup_logger
from app.src.utils import get_redis_client
from typing import Annotated
from redis import Redis
from app.src.models.Metadata import Metadata
from app.src.crud.metadata import add_file_metadata, read_metadata
import json


router = APIRouter(prefix="/metadata", tags=["metadata"])
logger = setup_logger()


@router.post("/{file_name}")
def add_metadata_to_single_file(
    file_name: str,
    metadata: Metadata,
    redis_client: Annotated[Redis, Depends(get_redis_client)],
):
    logger.info(f"Received request to add metadata to file {file_name}")
    if add_file_metadata(
        file_name=file_name, metadata=metadata, redis_client=redis_client
    ):
        return {"message": f"Metadata added to file {file_name}"}
    else:
        logger.warning("An error occured while processing this request")
        raise HTTPException(422, "An error occured while processing this request")


@router.get("/{file_name}")
async def read_file_metadata(
    file_name: str,
    bucket_name: str,
    redis_client: Annotated[Redis, Depends(get_redis_client)],
):
    logger.info(
        f"Received request to fetch metadata for file {file_name} in bucket {bucket_name}"
    )

    metadata_response = read_metadata(file_name, bucket_name, redis_client)

    tags_value = metadata_response.get("tags")
    if isinstance(tags_value, str):
        metadata_response["tags"] = json.loads(tags_value)

    logger.info(f"{metadata_response=}")

    metadata = Metadata(**metadata_response)
    logger.info("Request for metadata processed")
    return metadata
