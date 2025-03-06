from enum import Enum


class UserRole(Enum):
    OWNER = "owner"
    PARTICIPANT = "participant"
    NA = "n/a"


class RequestStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
