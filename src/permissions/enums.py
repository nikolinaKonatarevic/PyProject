from enum import StrEnum


class UserRole(StrEnum):
    OWNER = "owner"
    PARTICIPANT = "participant"
    NA = "n/a"


class RequestStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
