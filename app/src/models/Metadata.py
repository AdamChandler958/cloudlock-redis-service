from pydantic import BaseModel
from typing import Optional


class Metadata(BaseModel):
    bucket_name: str
    file_size: int
    file_type: str
    tags: Optional[list[str]] = None
