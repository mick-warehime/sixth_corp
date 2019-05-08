from typing import Optional

from events.event_utils import simulate_mouse_click
from models.characters.character_base import Character
from models.scenes.combat_scene import CharacterInfo
from models.scenes.layouts import Layout


def click_on_char(char: Character, layout: Layout):
    info = _get_char_info(char, layout)
    rects = layout.get_rects(info)
    assert len(rects) == 1

    simulate_mouse_click(*rects[0].center)


def _get_char_info(char: Character, layout: Layout) -> CharacterInfo:
    info = [info for info in layout.all_objects()
            if isinstance(info, CharacterInfo)
            and info.character is char]
    assert len(info) == 1
    info = info[0]
    return info


def selected_char(layout: Layout) -> Optional[Character]:
    infos = [info for info in layout.all_objects()
             if isinstance(info, CharacterInfo)
             and info.is_selected]
    assert len(infos) <= 1
    if infos:
        return infos[0].character
    return None
