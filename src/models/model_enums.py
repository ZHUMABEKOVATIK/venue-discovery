from enum import Enum as PyEnum

class DataStatus(str, PyEnum):
    new  = "NEW"
    approved = "APPROVED"
    rejected = "REJECTED"
    revision = "REVISION"

class UserRole(str, PyEnum):
    guest = "guest"
    owner = "owner"
    admin = "admin"