from typing import List
from pydantic import BaseModel, Field
from beanie import PydanticObjectId


class Entity(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias='_id')

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PydanticObjectId: str}
        orm_mode = True

    def __hash__(self):
        return hash(self.id)


class PagingModel:
    def __init__(self, limit: int = 1000, skip: int = 0) -> None:
        self.limit = limit
        self.skip = skip


class LoggedInUser(BaseModel):
    token: str
    scopes: List[str]
    roles: List[str]
