from datetime import datetime


class Document:
    def __init__(self, id: int, file_name: str, file_path: str, created_at: datetime, updated_at: datetime):
        self._id = id
        self._file_name = file_name
        self._file_path = file_path
        self._created_at = created_at
        self._updated_at = updated_at

    # Getters
    def get_document_id(self) -> int:
        return self._id

    def get_file_name(self) -> str:
        return self._file_name

    def get_file_path(self) -> str:
        return self._file_path

    def get_created_at(self) -> datetime:
        return self._created_at

    def get_updated_at(self) -> datetime:
        return self._updated_at

    # Setters
    def set_document_id(self, id: int):
        self._id = id

    def set_file_name(self, file_name: str):
        self._file_name = file_name

    def set_file_path(self, file_path: str):
        self._file_path = file_path

    def set_created_at(self, created_at: datetime):
        self._created_at = created_at

    def set_updated_at(self, updated_at: datetime):
        self._updated_at = updated_at
