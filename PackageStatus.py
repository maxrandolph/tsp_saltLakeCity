import enum

class PackageStatus(enum.Enum):
    inaccessible = 1
    at_hub = 2
    in_transit = 3
    delivered = 4
