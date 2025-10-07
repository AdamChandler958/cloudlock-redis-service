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
                "filetype": metadata.file_type,
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
