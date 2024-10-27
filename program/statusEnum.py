from enum import Enum

# enumeration for 3 status types
class Status(Enum):
    inRoute = "in route"
    atHub = "at the hub"
    delivered = "delivered"
