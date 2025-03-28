from pydantic import BaseModel


class DocumentBase(BaseModel):
    file_name: str
    file_path: str


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(DocumentBase):
    pass


class Document(DocumentBase):
    id: int
    project_id: int

    class Config:
        from_attributes = True


class PaginatedDocuments(BaseModel):
    documents: list[Document] | None
    count: int | None
    next: int | None
    prev: int | None
