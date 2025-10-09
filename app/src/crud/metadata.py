import json
from app.src.models.Metadata import Metadata
from app.src.logger import setup_logger
from redis import Redis

logger = setup_logger()


def add_file_metadata(file_name: str, metadata: Metadata, redis_client: Redis):
    logger.info("Adding metadata...")
    metadata_key = f"metadata:{metadata.bucket_name}:{file_name}"

    if metadata.tags is not None:
        tags_json = json.dumps(metadata.tags)
    else:
        tags_json = None

    try:
        redis_client.hset(
            metadata_key,
            mapping={
                "bucket_name": metadata.bucket_name,
                "object_name": file_name,
                "file_type": metadata.file_type,
                "file_size": metadata.file_size,
                "tags": tags_json if tags_json is not None else "",
            },
        )
    except Exception as e:
        logger.error(f"An error occured while adding metadata: {e}.")
        return False

    if metadata.tags is not None:
        logger.info("Adding tags to file...")

        object_id = f"{metadata.bucket_name}:{file_name}"
        try:
            for tag in metadata.tags:
                tag_key = f"tag:{tag}"
                redis_client.sadd(tag_key, object_id)
        except Exception as e:
            logger.error(f"An error occured while adding tags to file: {e}")
            return False

    logger.info("Metadata added successfully.")
    return True


def read_metadata(file_name: str, bucket_name: str, redis_client: Redis):
    logger.info("Reading metadata...")

    try:
        metadata_response = redis_client.hgetall(
            name=f"metadata:{bucket_name}:{file_name}"
        )
    except Exception as e:
        logger.error(f"Unable to fetch metadata due to error: {e}")

    logger.info("Metadata retrieval successful.")
    return metadata_response


def update_metadata(
    file_name: str,
    bucket_name: str,
    redis_client: Redis,
    file_type: str = None,
    file_size: int = None,
    tags: list[str] = None,
):
    logger.info("Updating metadata...")

    metadata_response = read_metadata(
        file_name=file_name, bucket_name=bucket_name, redis_client=redis_client
    )

    update_dict = {
        "bucket_name": bucket_name,
        "object_name": file_name,
        "file_type": file_type
        if file_type is not None
        else metadata_response.get("file_type"),
        "file_size": file_size
        if file_size is not None
        else metadata_response.get("file_size"),
        "tags": tags if tags is not None else metadata_response.get("tags"),
    }

    metadata_response.update(update_dict)

    try:
        redis_client.hset(f"metadata:{bucket_name}:{file_name}", metadata_response)
    except Exception as e:
        logger.error(f"Metadata failed to update with error: {e}")
        return False

    logger.info("Metadata successfully updated...")
    return True
