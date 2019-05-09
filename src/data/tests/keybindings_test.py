import csv
import os
import tempfile
from os.path import dirname
from typing import Dict
from unittest import TestCase

from data.keybindings import Keybindings
from events.events_base import BasicEvents

# Ensure that working directory is sixth_corp
os.chdir(dirname(dirname(dirname(dirname(os.path.abspath(__file__))))))


class KeybindingsTest(TestCase):

    def default_binding(self) -> Dict[str, BasicEvents]:
        return {'y': BasicEvents.SETTINGS,
                'z': BasicEvents.SETTINGS}

    def load_bindings(self, bindings: Dict[str, BasicEvents]) -> None:
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
            self.keybindings.event_for_key('y'),
            BasicEvents.SETTINGS)

    def test_save_settings(self) -> None:
        self.load_bindings(self.default_binding())
        new_prefs_file = tempfile.NamedTemporaryFile(mode='w')
        self.keybindings.preference_file = new_prefs_file.name

        self.keybindings.save()

        # load from new file
        self.keybindings = Keybindings()
        self.keybindings.preference_file = new_prefs_file.name
        self.keybindings.load()
        self.assertEqual(self.keybindings.event_for_key('y'),
                         BasicEvents.SETTINGS)

    def test_update_settings(self) -> None:
        self.load_bindings(self.default_binding())
        self.keybindings.update_binding('y', BasicEvents.NONE)

        self.assertEqual(self.keybindings.event_for_key('y'), BasicEvents.NONE)

    def test_inverse_binding(self) -> None:
        bindings = self.default_binding()
        event = BasicEvents.SETTINGS
        self.load_bindings(bindings)
        actual = tuple(sorted((self.keybindings.keys_for_event(event))))
        expected = tuple(sorted(k for k, v in bindings.items() if v == event))
        assert actual == expected

    def test_inverse_binding_no_keys(self) -> None:
        bindings = self.default_binding()
        event = BasicEvents.DEBUG
        self.load_bindings(bindings)
        actual = tuple(sorted((self.keybindings.keys_for_event(event))))
        assert actual == ()
        expected = tuple(sorted(k for k, v in bindings.items() if v == event))
        assert actual == expected

    def test_update_settings_are_saved(self) -> None:
        self.load_bindings(self.default_binding())
        self.keybindings.update_binding('y', BasicEvents.NONE)

        # ensure key change persists through saving
        self.keybindings = Keybindings()
        self.keybindings.preference_file = self.preference_file.name
        self.keybindings.load()
        self.assertEqual(self.keybindings.event_for_key('y'), BasicEvents.NONE)
