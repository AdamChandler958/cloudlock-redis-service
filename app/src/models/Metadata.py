from pydantic import BaseModel


class Metadata(BaseModel):
    bucket_name: str
    file_size: int
    file_type: str
    tags: list[str] = None
