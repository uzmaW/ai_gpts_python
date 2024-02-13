from sqlmodel import Field, SQLModel
from uuid import UUID,uuid4



class LocationBase(SQLModel):
    name: str
    location: str


class Location(LocationBase, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        description="Unique identifier (UUID) for the record",
    )


class LocationCreate(LocationBase):
    pass