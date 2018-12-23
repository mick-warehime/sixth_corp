from events import Event
from typing import Dict
import csv
import logging
from constants import PREFERENCES_FILE


class Keybindings(object):
    preference_file = PREFERENCES_FILE
    binding_field = 'binding'
    key_field = 'key'

    def __init__(self) -> None:
        self.bindings: Dict[str, Event] = dict()

    def load(self) -> None:
        bindings: Dict[str, Event] = dict()
        with open(self.preference_file) as bindings_file:
            reader = csv.DictReader(bindings_file)
            for row in reader:
                key = row[self.key_field]
                binding = row[self.binding_field]
                bindings[key] = Event[binding]

        self.bindings = bindings

        logging.debug('Loaded keybindings')
        logging.debug(str(self))

    def save(self) -> None:
        with open(self.preference_file, 'w') as bindings_file:
            writer = csv.DictWriter(
                bindings_file, fieldnames=[self.binding_field, self.key_field])
            writer.writeheader()
            for key, binding in self.bindings.items():
                writer.writerow(
                    {self.binding_field: binding, self.key_field: key})

    def update_binding(self, key: str, event: Event) -> None:
        self.bindings[key] = event

        self.save()

        logging.debug('Updated keybindings')
        logging.debug(str(self))

    def get_binding(self, key: str) -> Event:
        return self.bindings.get(key, Event.NONE)

    def __str__(self) -> str:
        keys = ["\nKEY BINDINGS", "--------------------"]
        for key, value in self.bindings.items():
            keys.append("{}: {}".format(key, value))
        keys.append("--------------------")
        return '\n'.join(keys)

    @classmethod
    def event_for_binding(self, binding: Event) -> Event:
        if binding == Event.SETTINGS:
            return Event.SETTINGS
        return Event.NONE
