import logging
from typing import List, Sequence

from models.abilities_base import Ability
from models.character_base import Character
from world.world import get_location
from views.pygame_view import PygameView
from models.states import Attribute

_COMBAT_BACKGROUND = 'src/images/background_combat.png'


class CombatSceneView(PygameView):

    def __init__(self) -> None:
        super(CombatSceneView, self).__init__(
            get_location().background_image_path)
        self.texts: List[str] = None
        self._targetting_enabled = False
        self._target_descriptions = []

    def render(self) -> None:
        super().render()
        self.render_text(self.texts)

    def _scene_description(self, player: Character,
                           enemy: Character) -> List[str]:
        texts = [
            'You are fighting a dreaded {}.'.format(enemy.__class__.__name__),
            'Your health: {}'.format(player.get_attribute(Attribute.HEALTH)),
            'Enemy health: {}'.format(enemy.get_attribute(Attribute.HEALTH)),
            ''
        ]
        return texts

    def _combat_options(self,
                        allowed_abilities: Sequence[Ability]) -> List[str]:
        return ['{} - {}'.format(i + 1, a.description())
                for i, a in enumerate(allowed_abilities)]

    def update(self, player: Character, enemy: Character,
               allowed_abilities: Sequence[Ability]) -> None:
        header = self._scene_description(player, enemy)
        options = self._combat_options(allowed_abilities)
        self.texts = header + options
        if self._targetting_enabled:
            self.texts.extend(['', 'Targets:'] + self._target_descriptions)

        self.render()

    @property
    def targetting_enabled(self) -> bool:
        return self._targetting_enabled

    def enable_targetting(self, targets: Sequence[Character]) -> None:
        assert not self._targetting_enabled
        logging.debug('Targetting enabled')
        self._targetting_enabled = True
        self._target_descriptions = [
            '{} - {}'.format(i + 1, t.__class__.__name__)
            for i, t in enumerate(targets)]

    def disable_targetting(self) -> None:
        assert self._targetting_enabled
        logging.debug('Targetting disabled')
        self._targetting_enabled = False
