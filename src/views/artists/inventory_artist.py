from typing import List, Sequence

from pygame.rect import Rect

from data.colors import BLUE, DARK_GRAY, GREEN, LIGHT_GRAY, RED, WHITE
from data.keybindings import Keybindings
from events.events_base import BasicEvents
from models.characters.mods_base import SlotTypes
from models.scenes.inventory_scene import (InventoryScene, SelectedModInfo,
                                           SlotHeaderInfo, SlotRowInfo)
from models.scenes.scenes_base import Scene
from views.artists.drawing_utils import rescale_horizontal, rescale_vertical
from views.artists.scene_artist_base import SceneArtist
from views.pygame_screen import Screen

_SLOT_FONT_SIZE, = rescale_horizontal(28)
_OVERLAY_FONT_SIZE, = rescale_horizontal(28)
_ERROR_FONT_SIZE, = rescale_horizontal(40)
_TEXT_COLOR = BLUE


def _render_slot_header(slot_data: SlotHeaderInfo, rect: Rect,
                        selected_mod_slots: List[SlotTypes],
                        screen: Screen) -> None:
    # Render the header for a given slot category, including storage capacity.
    # If the slot is a valid transfer slot, use a different border.

    screen.render_rect(rect, LIGHT_GRAY, 0)

    border = GREEN if slot_data.slot in selected_mod_slots else DARK_GRAY

    screen.render_rect(rect, border, 4)

    if slot_data.slot != SlotTypes.GROUND:
        text = '{} - {} / {}'.format(slot_data.slot.value, slot_data.num_filled,
                                     slot_data.capacity)
    else:
        text = slot_data.slot.value

    screen.render_text(text, _SLOT_FONT_SIZE, rect.x, rect.y, _TEXT_COLOR,
                       rect.w,
                       rect.h)


def _render_mod_slot(slot_data: SlotRowInfo, rect: Rect, screen: Screen) -> None:
    # Render a row representing a given equipped or stored mod.

    screen.render_rect(rect, LIGHT_GRAY, 0)
    border = RED if slot_data.is_selected else DARK_GRAY
    screen.render_rect(rect, border, 4)

    screen.render_text(slot_data.mod.description(), _SLOT_FONT_SIZE,
                       rect.x + 10,
                       rect.y, _TEXT_COLOR, h=rect.h)


def _render_selected_mod_info(info: SelectedModInfo, rect: Rect,
                              screen: Screen) -> None:
    # Render relevant information about a mod.
    screen.render_rect(rect, LIGHT_GRAY, 0)
    screen.render_rect(rect, RED, 4)

    spacing = 30

    # Mod header
    x = rect.x
    y = rect.y + 10

    mod = info.mod
    text_rect = screen.render_text(mod.description(), _SLOT_FONT_SIZE, x, y,
                                   _TEXT_COLOR, rect.w)
    y = text_rect.y + text_rect.h + spacing

    # Mod properties
    x = rect.x + 10
    valid_slots = [slot.value for slot in mod.valid_slots()]
    slots = 'Slots: ' + ', '.join(valid_slots)
    text_rect = screen.render_text(slots, _SLOT_FONT_SIZE, x, y, _TEXT_COLOR)
    y = text_rect.y + text_rect.h + spacing

    if mod.states_granted():
        states = [s.value for s in mod.states_granted()]
        subject = 'States granted: '

        text_rect = _render_mod_property(x, spacing, subject, states, text_rect,
                                         screen)

    if mod.attribute_modifiers():
        atts = ['{} : {}'.format(att.value, num)
                for att, num in mod.attribute_modifiers().items()]

        text_rect = _render_mod_property(x, spacing, 'Attribute modifiers:',
                                         atts, text_rect, screen)

    if mod.subroutines_granted():
        subs = [sub.description() for sub in mod.subroutines_granted()]
        _render_mod_property(x, spacing, 'Subroutines granted:', subs,
                             text_rect, screen)


def _render_mod_property(x: int, spacing: int, label: str, lines: Sequence[str],
                         text_rect: Rect, screen: Screen) -> Rect:
    y = text_rect.y + text_rect.h + spacing
    text_rect = screen.render_text(label, _SLOT_FONT_SIZE, x, y,
                                   _TEXT_COLOR)
    y = text_rect.y + text_rect.h
    text = '\n'.join(lines)
    text_rect = screen.render_text(text, _SLOT_FONT_SIZE, x + 40, y,
                                   _TEXT_COLOR)
    return text_rect


class InventoryArtist(SceneArtist):

    def render(self, screen: Screen, scene: Scene) -> None:
        assert isinstance(scene, InventoryScene)

        # Scene title, exit key, and error message
        inv_key = Keybindings().keys_for_event(BasicEvents.INVENTORY)[0]
        x, = rescale_horizontal(20)
        y_shift, = rescale_vertical(10)
        y = y_shift
        rect = screen.render_text('Inventory', _OVERLAY_FONT_SIZE, x, y, WHITE)
        y = rect.y + rect.h
        rect = screen.render_text('{} - Return'.format(inv_key),
                                  _OVERLAY_FONT_SIZE, x, y, WHITE)

        if scene.UI_error_message:
            x = rect.x + rect.w + 50
            h = y + rect.h - y_shift
            y = y_shift
            screen.render_text(scene.UI_error_message, _ERROR_FONT_SIZE, x, y,
                               RED, h=h)

        # Inventory slots, mods, and mod information
        layout = scene.layout
        scene_objects = layout.all_objects()

        if scene.selected_mod is not None:
            selected_mod_slots = scene.selected_mod.valid_slots()
            selected_mod_slots.append(SlotTypes.GROUND)  # ground always valid
        else:
            selected_mod_slots = []

        for obj in scene_objects:
            if obj is None:
                continue

            rects = layout.get_rects(obj)
            if isinstance(obj, SlotHeaderInfo):
                assert len(rects) == 1
                _render_slot_header(obj, rects[0], selected_mod_slots, screen)
            elif isinstance(obj, SlotRowInfo):
                assert len(rects) == 1
                _render_mod_slot(obj, rects[0], screen)
            elif isinstance(obj, SelectedModInfo):
                assert len(rects) == 1
                _render_selected_mod_info(obj, rects[0], screen)
