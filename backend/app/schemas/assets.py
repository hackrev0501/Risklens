from typing import List, Optional
from pydantic import BaseModel


class TagBase(BaseModel):
    name: str
    description: Optional[str] = None


class TagRead(TagBase):
    id: int

    class Config:
        from_attributes = True


class AssetBase(BaseModel):
    identifier: str
    type: str = "host"
    name: Optional[str] = None
    business_criticality: int = 1
    tags: List[str] = []


class AssetRead(BaseModel):
    id: int
    identifier: str
    type: str
    name: Optional[str]
    business_criticality: int
    tags: List[TagRead] = []

    class Config:
        from_attributes = True
