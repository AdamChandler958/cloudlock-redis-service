from redis import Redis
from app.src.logger import setup_logger
import json


logger = setup_logger()


def retrieve_tags(metadata_key: str, redis_client: Redis):
    logger.info(f"Retrieving tags for item: {metadata_key}")
    try:
        existing_tags = redis_client.hget(metadata_key, "tags")
    except Exception as e:
        logger.error(f"Tag retrieval failed with error: {e}")
        full_item = redis_client.hgetall(metadata_key)
        if not full_item:
            logger.error(f"Item with matching key: {metadata_key} does not exist")
            raise ValueError(f"No item found with key: {metadata_key}")

    logger.info(f"Tags retrieved for item: {metadata_key}")
    return existing_tags


def create_tag(metadata_key: str, new_tag_val: str, redis_client: Redis):
    logger.info(f"Creating new tag {new_tag_val} for item {metadata_key}")
    try:
        tags_retrieved = retrieve_tags(metadata_key, redis_client)
    except ValueError:
        logger.error("Exiting tag creation routine")
        return False

    existing_tags = [] if tags_retrieved is None else json.loads(tags_retrieved)

    if new_tag_val not in existing_tags:
        logger.info("Adding tag to file...")
        object_id = metadata_key.removeprefix("metadata:")
        tag_key = f"tag:{new_tag_val}"
        redis_client.sadd(tag_key, object_id)

        existing_tags.append(new_tag_val)
        updated_tags_json = json.dumps(existing_tags)

        redis_client.hset(metadata_key, "tags", updated_tags_json)
    else:
        logger.warning(
            f"Tag: {new_tag_val} is already attached to item: {metadata_key} \n skipping tag."
        )
        return True

    logger.info(f"Tag: {new_tag_val} successfully attached to item: {metadata_key}.")
    return True


def remove_tag(metadata_key: str, tag_value: str, redis_client: Redis):
    logger.info(f"Removing tag: {tag_value} from item {metadata_key}")

    try:
        tags_retrieved = retrieve_tags(metadata_key, redis_client)
    except ValueError:
        logger.error("Exiting tag deletion routine")
        return False

    existing_tags = [] if tags_retrieved is None else json.dumps(tags_retrieved)

    if tag_value not in existing_tags:
        logger.error(f"Tag: {tag_value} is not attached to item {metadata_key}")
        return True

    existing_tags.remove(tag_value)
    updated_tag_json = json.dumps(existing_tags)

    redis_client.srem(f"tag:{tag_value}", metadata_key.removeprefix("metadata:"))
    logger.info(f"Tag: {tag_value} removed from reverse lookup of item: {metadata_key}")

    redis_client.hset(metadata_key, "tags", updated_tag_json)
    logger.info(f"{tag_value} removed from item: {metadata_key} successfully.")
    return True
