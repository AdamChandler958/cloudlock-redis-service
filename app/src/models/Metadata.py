from pydantic import BaseModel
from typing import Optional


class Metadata(BaseModel):
    bucket_name: str
    object_name: str
    file_type: str
    file_size: int
    tags: Optional[list[str]] = None
