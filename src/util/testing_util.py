from typing import List, Optional

from events.event_utils import simulate_mouse_click
from models.characters.character_base import Character
from models.characters.character_examples import CharacterData
from models.characters.character_impl import build_character
from models.characters.chassis import ChassisData
from models.characters.mods_base import ModData, SlotTypes
from models.characters.states import Attributes
from models.characters.subroutine_examples import direct_damage
from models.characters.subroutines_base import Subroutine
from models.combat.ai_impl import AIType
from models.scenes.combat_scene import CharacterInfo
from models.scenes.layouts import Layout


def click_on_char(char: Character, layout: Layout) -> None:
    info = _get_char_info(char, layout)
    rects = layout.get_rects(info)
    assert len(rects) == 1

    simulate_mouse_click(*rects[0].center)


def _get_char_info(char: Character, layout: Layout) -> CharacterInfo:
    info = [info for info in layout.all_objects()
            if isinstance(info, CharacterInfo)
            and info.character is char]
    assert len(info) == 1
    return info[0]


def selected_char(layout: Layout) -> Optional[Character]:
    infos = [info for info in layout.all_objects()
             if isinstance(info, CharacterInfo)
             and info.is_selected]
    assert len(infos) <= 1
    if infos:
        return infos[0].character
    return None


def _get_combatant(health: int, subroutine: Subroutine, name: str,
                   ai_type: AIType = AIType.No_AI) -> Character:
    mod_data = ModData(attribute_modifiers={Attributes.MAX_HEALTH: health},
                       subroutines_granted=(subroutine,),
                       valid_slots=(SlotTypes.ARMS,))
    chassis_data = ChassisData({SlotTypes.ARMS: 10})
    char_data = CharacterData(chassis_data, name, (mod_data,), '', ai_type)

    return build_character(data=char_data)


def create_combat_group(group_size: int, health: int = 10, damage: int = 2,
                        base_name: str = 'combatant',
                        subroutine: Subroutine = None) -> List[Character]:
    if subroutine is None:
        subroutine = direct_damage(damage)
    return [_get_combatant(health=health, subroutine=subroutine,
                           name=base_name + str(i))
            for i in range(group_size)]
