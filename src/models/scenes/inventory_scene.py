import logging
from typing import Any, Callable, Iterable, List, NamedTuple, Optional, Tuple

from data.constants import SCREEN_SIZE, BackgroundImages
from events.events_base import (BasicEvents, EventListener, EventType,
                                InventorySelectionEvent,
                                InventoryTransferEvent)
from models.characters.chassis import Chassis
from models.characters.mods_base import Mod, SlotTypes
from models.characters.player import get_player
from models.scenes.layouts import Layout
from models.scenes.scenes_base import BasicResolution, Resolution, Scene


class SlotHeaderInfo(NamedTuple):
    """Data represented in the header row of an inventory slot."""
    slot: SlotTypes
    capacity: int
    mods: Tuple[Mod, ...]

    @property
    def num_filled(self) -> int:
        return len(self.mods)


class SlotRowInfo(NamedTuple):
    """Data represented by single row of an inventory slot."""
    mod: Mod
    is_selected: bool


class SelectedModInfo(NamedTuple):
    """Data representing information about the selected Mod."""
    mod: Mod


class InventoryScene(Scene, EventListener):

    def __init__(self, prev_scene_loader: Callable[[], Scene],
                 loot_mods: Callable[[], Iterable[Mod]] = None) -> None:
        """

        Args:
            prev_scene_loader: Zero-argument function that returns the previous
                scene.
            loot_mods: Zero-argument function that returns the mods on the
                ground.
        """
        super().__init__()
        self._background_image = BackgroundImages.INVENTORY.path
        self._player = get_player()
        self._selected_mod: Optional[Mod] = None
        if loot_mods is not None:
            self._mods_on_ground = list(loot_mods())
        else:
            self._mods_on_ground = []
        self._update_layout()
        self._resolution = BasicResolution(prev_scene_loader)
        self._is_resolved = False
        self._UI_error_message: str = ''

    def notify(self, event: EventType) -> None:
        if isinstance(event, InventorySelectionEvent):
            if self._selected_mod is event.mod:
                self._selected_mod = None
            else:
                self._selected_mod = event.mod
            self._update_layout()
        if isinstance(event, InventoryTransferEvent):
            # Check that transfer is valid
            if self._selected_mod is None:
                return
            new_slot = event.new_slot
            valid_slots = self._selected_mod.valid_slots() + [SlotTypes.GROUND]
            if new_slot not in valid_slots:
                self._UI_error_message = 'Invalid slot'
                return
            chassis = self._player.chassis
            if self._selected_mod in chassis.mods_in_slot(new_slot):
                return  # Mod already in the specified slot.
            if chassis.slot_full(new_slot) and new_slot != SlotTypes.GROUND:
                self._UI_error_message = 'Slot full'
                return

            # Carry out valid transfer, accounting for GROUND slot which is not
            # actually a chassis slot.
            if new_slot == SlotTypes.GROUND:
                chassis.remove_mod(self._selected_mod)
                self._mods_on_ground.append(self._selected_mod)
                logging.debug('Moving {} to ground.'.format(self._selected_mod))
            else:
                if self._selected_mod in self._mods_on_ground:
                    self._mods_on_ground.remove(self._selected_mod)
                chassis.transfer_mod(self._selected_mod, new_slot)
        if event == BasicEvents.INVENTORY:
            self._is_resolved = True

    @property
    def layout(self) -> Layout:
        return self._layout

    @property
    def selected_mod(self) -> Optional[Mod]:
        return self._selected_mod

    @property
    def UI_error_message(self) -> str:
        return self._UI_error_message

    @property
    def background_image(self) -> str:
        return self._background_image

    def is_resolved(self) -> bool:
        return self._is_resolved

    def get_resolution(self) -> Resolution:
        assert self.is_resolved()
        res = self._resolution
        del self._resolution
        return res

    def _update_layout(self) -> None:

        # The layout associates scene data with different rects on the screen.
        # These rects are used to process mouse clicks and to determine how to
        # draw the scene. For example, a given mod stored in one of the slot
        # categories is associated with the rect where it will show up on the
        # screen.
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
            info = SelectedModInfo(self._selected_mod)
            mod_info_layout = Layout([(None, 1), (info, 3), (None, 1)],
                                     'horizontal')
            mod_info_layout = Layout([(None, 1), (mod_info_layout, 5),
                                      (None, 1)])
        else:
            mod_info_layout = Layout()  # nothing to display

        # Ground inventory
        header = SlotHeaderInfo(SlotTypes.GROUND, 0,
                                tuple(self._mods_on_ground))

        loot_layout = self._slot_layout(header, num_rows=6)
        loot_layout = Layout([(None, 1), (loot_layout, 3), (None, 1)],
                             'horizontal')
        loot_layout = Layout([(None, 1), (loot_layout, 6), (None, 1)])

        right_half = Layout([(mod_info_layout, 7), (loot_layout, 8)])

        # combined halves
        layout = Layout([(left_half, 1), (right_half, 1)], 'horizontal')

        # Gap at top for information display.
        self._layout = Layout([(None, 1), (layout, 14)], dimensions=SCREEN_SIZE)

    def _slot_layout(self, slot_data: SlotHeaderInfo,
                     num_rows: int = None) -> Layout:
        """Vertical layout storing a single slot's data."""

        # First row is just basic slot information
        elems: List[Tuple[Any, int]] = [(slot_data, 1)]
        for mod in slot_data.mods:
            elems.append((SlotRowInfo(mod, mod is self._selected_mod), 1))

        # Add padding to ensure consistent row sizes
        num_rows = _DEFAULT_ROWS_PER_SLOT if num_rows is None else num_rows

        if len(elems) < num_rows:
            elems.append((None, num_rows - len(elems)))

        return Layout(elems)


_DEFAULT_ROWS_PER_SLOT = 4


def _slot_header(slot: SlotTypes, chassis: Chassis) -> SlotHeaderInfo:
    return SlotHeaderInfo(slot, chassis.slot_capacities[slot],
                          chassis.mods_in_slot(slot))
