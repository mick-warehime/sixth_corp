from typing import List, NamedTuple, Tuple, Union

from data.constants import SCREEN_SIZE, BackgroundImages
from events.events_base import (EventListener, EventType,
                                InventorySelectionEvent,
                                InventoryTransferEvent)
from models.characters.chassis import Chassis
from models.characters.mods_base import Mod, SlotTypes
from models.characters.player import get_player
from models.scenes.scenes_base import Resolution, Scene
from views.layouts import Layout


class SlotHeader(NamedTuple):
    """Data represented in the header row of an inventory slot."""
    slot: SlotTypes
    capacity: int
    mods: Tuple[Mod, ...]

    @property
    def num_filled(self) -> int:
        return len(self.mods)


class SlotData(NamedTuple):
    """Data represented by single row of an inventory slot."""
    mod: Mod
    is_selected: bool


class ModInformation(NamedTuple):
    mod: Mod


class InventoryScene(Scene, EventListener):

    def __init__(self) -> None:
        super().__init__()
        self._background_image = BackgroundImages.INVENTORY.path
        self._player = get_player()
        self._layout: Layout = None
        self._selected_mod: Mod = None
        self._update_layout()

    def notify(self, event: EventType) -> None:
        if isinstance(event, InventorySelectionEvent):
            if self._selected_mod is event.mod:
                self._selected_mod = None
            else:
                self._selected_mod = event.mod
            self._update_layout()
        if isinstance(event, InventoryTransferEvent):
            if self._selected_mod is None:
                return
            if event.new_slot not in self._selected_mod.valid_slots():
                return
            # Carry out valid transfer of slot
            self._player.chassis.transfer_mod(self._selected_mod,
                                              event.new_slot)

    @property
    def inventory_available(self) -> bool:
        return True

    @property
    def layout(self) -> Layout:
        return self._layout

    @property
    def selected_mod(self) -> Mod:
        return self._selected_mod

    @property
    def background_image(self) -> str:
        return self._background_image

    # TODO(mick) - move settings, combat, decision scene -> model classes
    def is_resolved(self) -> bool:
        return False

    def get_resolution(self) -> Resolution:
        return None

    def _update_layout(self) -> None:
        chassis = self._player.chassis

        # Left half of screen, composed of chassis slots

        capacities = chassis.slot_capacities

        fillable_slots = [slot for slot in SlotTypes
                          if capacities.get(slot, 0) > 0
                          and slot != SlotTypes.STORAGE]

        rows_per_column = 15

        # Left half of left column
        num_rows = 0
        slot_elems_0 = []
        for slot in fillable_slots[:3]:
            data = _slot_header(slot, chassis)
            num_rows += _DEFAULT_ROWS_PER_SLOT + 1
            slot_elems_0.extend(
                [(self._slot_layout(data), _DEFAULT_ROWS_PER_SLOT), (None, 1)])
        assert slot_elems_0
        # Don't need final gap
        slot_elems_0.pop()
        num_rows -= 1

        # Padding on bottom of column for consistent row number
        if num_rows < rows_per_column:
            slot_elems_0.append((None, rows_per_column - num_rows))

        chassis_col_0 = Layout(slot_elems_0)

        # Right half of left column has extra space for the storage slot
        num_rows = 0
        slot_elems_1 = []
        for slot in fillable_slots[3:]:
            data = _slot_header(slot, chassis)
            num_rows += _DEFAULT_ROWS_PER_SLOT + 1
            slot_elems_1.extend(
                [(self._slot_layout(data), _DEFAULT_ROWS_PER_SLOT), (None, 1)])
        storage_data = _slot_header(SlotTypes.STORAGE, chassis)
        storage_rows = storage_data.num_filled + 1
        slot_elems_1.append((self._slot_layout(storage_data, storage_rows),
                             storage_rows))
        num_rows += storage_rows

        if num_rows < rows_per_column:
            slot_elems_1.append((None, rows_per_column - num_rows))
        chassis_col_1 = Layout(slot_elems_1)

        left_half = Layout([(None, 1), (chassis_col_0, 10), (None, 1),
                            (chassis_col_1, 10), (None, 1)], 'horizontal')

        # Right half of screen, containing mod information (if present) and
        # loot slots (if present)

        # selected mod information

        if self._selected_mod is not None:
            info = ModInformation(self._selected_mod)
            mod_info_layout = Layout([(None, 1), (info, 3), (None, 1)],
                                     'horizontal')
            mod_info_layout = Layout([(None, 1), (mod_info_layout, 5),
                                      (None, 1)])
        else:
            mod_info_layout = Layout()  # nothing to display

        loot_layout = Layout()  # Keep blank for now

        right_half = Layout([(mod_info_layout, 1), (loot_layout, 1)])

        # combined halves
        layout = Layout([(left_half, 1), (right_half, 1)], 'horizontal')

        # Gap at top for information display.
        self._layout = Layout([(None, 1), (layout, 14)], dimensions=SCREEN_SIZE)

    def _slot_layout(self, slot_data: SlotHeader,
                     num_rows: int = None) -> Layout:
        """Vertical layout storing a single slot's data."""

        # First row is just basic slot information
        elements: List[Tuple[Union[SlotHeader, SlotData], int]] = []
        elements.append((slot_data, 1))
        for mod in slot_data.mods:
            elements.append((SlotData(mod, mod is self._selected_mod), 1))

        # Add padding to ensure consistent row sizes
        num_rows = _DEFAULT_ROWS_PER_SLOT if num_rows is None else num_rows

        if len(elements) < num_rows:
            elements.append((None, num_rows - len(elements)))

        return Layout(elements)


_DEFAULT_ROWS_PER_SLOT = 4


def _slot_header(slot: SlotTypes, chassis: Chassis) -> SlotHeader:
    return SlotHeader(slot, chassis.slot_capacities[slot],
                      chassis.mods_in_slot(slot))
