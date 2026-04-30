from enum import Enum as PyEnum

class DataStatus(str, PyEnum):
    pending  = "pending"
    approved = "approved"
    rejected = "rejected" 
    revision = "revision"

class UserRole(str, PyEnum):
    guest = "guest"
    owner = "owner"
    admin = "admin"