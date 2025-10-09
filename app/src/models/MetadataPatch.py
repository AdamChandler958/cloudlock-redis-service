from pydantic import BaseModel
from typing import Optional


class MetadataPatch(BaseModel):
    bucket_name: Optional[str] = ""
    object_name: Optional[str] = ""
    file_type: Optional[str] = ""
    file_size: Optional[int] = 0
    tags: Optional[list[str]] = None
