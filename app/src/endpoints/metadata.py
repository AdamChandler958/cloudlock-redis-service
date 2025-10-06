from fastapi import APIRouter, Depends, HTTPException
from app.src.logger import setup_logger
from app.src.utils import get_redis_client
from typing import Annotated
from redis import Redis
from app.src.models.Metadata import Metadata
from app.src.crud.metadata import add_file_metadata


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
