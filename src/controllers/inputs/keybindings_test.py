import csv
import tempfile
from typing import Dict
from unittest import TestCase

from controllers.inputs.keybindings import Keybindings
from events.events_base import Event


class KeybindingsTest(TestCase):

    def default_binding(self) -> Dict[str, Event]:
        return {'y': Event.SETTINGS}

    def load_bindings(self, bindings: Dict[str, Event]) -> None:
        self.preference_file = tempfile.NamedTemporaryFile(mode='w')
        self.keybindings = Keybindings()
        self.keybindings.preference_file = self.preference_file.name

        BINDING = 'binding'
        KEY = 'key'
        with open(self.preference_file.name, 'w') as fake_csv:
            writer = csv.DictWriter(fake_csv, fieldnames=[BINDING, KEY])
            writer.writeheader()
            for key, binding in bindings.items():
                writer.writerow({BINDING: binding, KEY: key})

        self.keybindings.load()

    def test_load_settings(self) -> None:
        self.load_bindings(self.default_binding())

        self.assertEqual(
            self.keybindings.get_binding('y'),
            Event.SETTINGS)

    def test_save_settings(self) -> None:
        self.load_bindings(self.default_binding())
        new_prefs_file = tempfile.NamedTemporaryFile(mode='w')
        self.keybindings.preference_file = new_prefs_file.name

        self.keybindings.save()

        # load from new file
        self.keybindings = Keybindings()
        self.keybindings.preference_file = new_prefs_file.name
        self.keybindings.load()
        self.assertEqual(self.keybindings.get_binding('y'), Event.SETTINGS)

    def test_update_settings(self) -> None:
        self.load_bindings(self.default_binding())
        self.keybindings.update_binding('y', Event.NONE)

        self.assertEqual(self.keybindings.get_binding('y'), Event.NONE)

    def test_update_settings_are_saved(self) -> None:
        self.load_bindings(self.default_binding())
        self.keybindings.update_binding('y', Event.NONE)

        # ensure key change persists through saving
        self.keybindings = Keybindings()
        self.keybindings.preference_file = self.preference_file.name
        self.keybindings.load()
        self.assertEqual(self.keybindings.get_binding('y'), Event.NONE)
