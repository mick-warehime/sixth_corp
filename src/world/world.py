from world.location_base import Location
from world.locations import CityLocation


class World(object):
    def __init__(self) -> None:
        self.location: Location = CityLocation()


_world = None


def get_world() -> World:
    global _world
    if _world is None:
        reset_world()
    return _world


def reset_world() -> None:
    global _world
    _world = World()


def get_location() -> Location:
    return get_world().location


def set_location(location: Location) -> None:
    global _world
    _world.location = location
