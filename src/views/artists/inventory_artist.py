from typing import List

from pygame.rect import Rect

from data.colors import WHITE, LIGHT_GRAY, DARK_GRAY, BLUE, RED, GREEN
from models.characters.mods_base import SlotTypes
from models.scenes.inventory_scene import InventoryScene, SlotHeader, SlotData, \
    ModInformation
from models.scenes.scenes_base import Scene
from views.artists.scene_artist_base import SceneArtist
from views.pygame_screen import Screen

_FONT_SIZE = 40
_TEXT_COLOR = BLUE


def _render_slot_header(slot_data: SlotHeader, rect: Rect,
                        selected_mod_slots: List[SlotTypes],
                        screen: Screen) -> None:
    screen.render_rect(rect, LIGHT_GRAY, 0)

    border = GREEN if slot_data.slot in selected_mod_slots else DARK_GRAY

    screen.render_rect(rect, border, 4)

    text = '{} - {} / {}'.format(slot_data.slot.value, slot_data.num_filled,
                                 slot_data.capacity)

    screen.render_text(text, _FONT_SIZE, rect.x, rect.y, _TEXT_COLOR, rect.w,
                       rect.h)


def _render_mod_slot(slot_data: SlotData, rect: Rect, screen: Screen) -> None:
    screen.render_rect(rect, LIGHT_GRAY, 0)
    border = RED if slot_data.is_selected else DARK_GRAY
    screen.render_rect(rect, border, 4)

    screen.render_text(slot_data.mod.description(), _FONT_SIZE, rect.x + 10,
                       rect.y, _TEXT_COLOR, h=rect.h)


def _render_selected_mod_info(info: ModInformation, rect: Rect,
                              screen: Screen) -> None:
    screen.render_rect(rect, LIGHT_GRAY, 0)
    screen.render_rect(rect, RED, 4)

    spacing = 30

    # Mod header
    x = rect.x
    y = rect.y + 10

    mod = info.mod
    text_rect = screen.render_text(mod.description(), _FONT_SIZE, x, y,
                                   _TEXT_COLOR, rect.w)
    y = text_rect.y + text_rect.h + spacing

    # Mod properties
    x = rect.x + 10
    valid_slots = [slot.value for slot in mod.valid_slots()]
    slots = 'Slots: ' + ', '.join(valid_slots)
    text_rect = screen.render_text(slots, _FONT_SIZE, x, y, _TEXT_COLOR)
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


def _render_mod_property(x, spacing, label, lines, text_rect, screen):
    y = text_rect.y + text_rect.h + spacing
    text_rect = screen.render_text(label, _FONT_SIZE, x, y,
                                   _TEXT_COLOR)
    y = text_rect.y + text_rect.h
    text = '\n'.join(lines)
    text_rect = screen.render_text(text, _FONT_SIZE, x + 40, y, _TEXT_COLOR)
    return text_rect


class InventoryArtist(SceneArtist):

    def render(self, screen: Screen, scene: Scene) -> None:
        assert isinstance(scene, InventoryScene)

        # Scene title and exit key
        screen.render_texts(list(scene.options),
                            font_size=35, x=20, y=10, color=WHITE, spacing=30)

        # All other boxes with text
        layout = scene.layout
        all_rects = layout.get_rects(layout)
        scene_objects = {layout.object_at(*rect.center) for rect in all_rects}

        if scene.selected_mod is not None:
            selected_mod_slots = scene.selected_mod.valid_slots()
        else:
            selected_mod_slots = []

        for obj in scene_objects:
            if obj is None:
                continue

            rects = layout.get_rects(obj)
            if isinstance(obj, SlotHeader):
                assert len(rects) == 1
                _render_slot_header(obj, rects[0], selected_mod_slots, screen)
            elif isinstance(obj, SlotData):
                assert len(rects) == 1
                _render_mod_slot(obj, rects[0], screen)
            elif isinstance(obj, ModInformation):
                assert len(rects) == 1
                _render_selected_mod_info(obj, rects[0], screen)
