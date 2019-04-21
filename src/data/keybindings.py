import csv
import logging
from collections import defaultdict
from typing import Dict, List, Tuple

from data.constants import PREFERENCES_FILE
from events.events_base import BasicEvents, EventType


class Keybindings(object):
    """Stores all key bindings, mapping them to events."""
    preference_file = PREFERENCES_FILE
    binding_field = 'binding'
    key_field = 'key'
    _keys_loaded: bool = False
    _bindings: Dict[str, BasicEvents] = dict()
    _bindings_inverse: Dict[str, List[str]] = dict()

    def __init__(self) -> None:
        if not Keybindings._keys_loaded:
            self.load()
            Keybindings._keys_loaded = True

    def load(self) -> None:
        bindings: Dict[str, BasicEvents] = dict()
        bindings_inv: Dict[str, List[str]] = defaultdict(lambda: [])
        with open(self.preference_file) as bindings_file:
            reader = csv.DictReader(bindings_file)
            for row in reader:
                key = row[self.key_field]
                bound_event = row[self.binding_field]
                try:
                    bindings[key] = BasicEvents[bound_event]
                    bindings_inv[bound_event].append(key)
                except KeyError:
                    raise NotImplementedError(
                        'Binding <{}> does not exist. Add BasicEvents.'
                        '{}?'.format(bound_event, bound_event))

        Keybindings._bindings = bindings
        Keybindings._bindings_inverse = bindings_inv

        logging.debug('Loaded keybindings')
        logging.debug(str(self))

    def save(self) -> None:
        with open(self.preference_file, 'w') as bindings_file:
            writer = csv.DictWriter(
                bindings_file, fieldnames=[self.binding_field, self.key_field])
            writer.writeheader()
            for key, binding in self._bindings.items():
                writer.writerow(
                    {self.binding_field: binding, self.key_field: key})

    def update_binding(self, key: str, event: BasicEvents) -> None:
        previously_bound = [event_str for event_str in self._bindings_inverse
                            if self._bindings_inverse[event_str] == key]
        for event_str in previously_bound:
            self._bindings_inverse[event_str].remove(key)
        Keybindings._bindings[key] = event
        Keybindings._bindings_inverse[event.value].append(key)

        self.save()

        logging.debug('Updated keybindings')
        logging.debug(str(self))

    def event_for_key(self, key: str) -> EventType:
        return self._bindings.get(key, BasicEvents.NONE)

    def keys_for_event(self, event: BasicEvents) -> Tuple[str, ...]:
        return tuple(self._bindings_inverse[event.value])

    def __str__(self) -> str:
        keys = ["\nKEY BINDINGS", "--------------------"]
        for key, value in self._bindings.items():
            keys.append("{}: {}".format(key, value))
        keys.append("--------------------")
        return '\n'.join(keys)
