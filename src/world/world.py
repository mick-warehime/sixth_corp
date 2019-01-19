from world.location_base import Location
from world.locations import LoadingLocation

_location: Location = LoadingLocation()


def reset_location() -> None:
    global _location
    _location = LoadingLocation()


def get_location() -> Location:
    global _location
    return _location


def set_location(location: Location) -> None:
    global _location
    _location = location
