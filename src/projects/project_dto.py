from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    name: str = Field(max_length=40)
    description: str


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    name: str
    description: str


class Project(ProjectBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
