from pydantic import BaseModel


class MetadataKey(BaseModel):
    bucket_name: str
    file_name: str
