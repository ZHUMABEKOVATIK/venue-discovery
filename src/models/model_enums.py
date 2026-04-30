from enum import Enum as PyEnum

class DataStatus(str, PyEnum):
    pending  = "pending"
    approved = "approved"
    rejected = "rejected" 
    revision = "revision"

class UserRole(PyEnum, str):
    guest = "guest"
    owner = "owner"
    admin = "admin"