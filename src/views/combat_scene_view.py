import logging
from typing import List, Sequence

from characters.abilities_base import Ability
from characters.character_base import Character
from characters.states import Attribute
from views.pygame_view import PygameView
from world.world import get_location

_COMBAT_BACKGROUND = 'src/images/background_combat.png'
_PLAYER_IMAGE = 'src/images/walle.png'
_ENEMY_IMAGE = 'src/images/drone.png'


class CombatSceneView(PygameView):

    def __init__(self) -> None:
        super(CombatSceneView, self).__init__(
            get_location().background_image_path)
        self.texts: List[str] = None
        self._targetting_enabled = False
        self._target_descriptions: List[str] = []

    def render(self) -> None:
        super().render()
        self.render_text(self.texts)
        self.render_image(_PLAYER_IMAGE, 200, 700, (150, 150))
        self.render_image(_ENEMY_IMAGE, 800, 800, (200, 150))

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

    def targets_shown(self) -> bool:
        return self._targetting_enabled

    def show_targets(self, targets: Sequence[Character]) -> None:
        assert not self._targetting_enabled
        logging.debug('Targetting enabled')
        self._targetting_enabled = True
        self._target_descriptions = [
            '{} - {}'.format(i + 1, t.description())
            for i, t in enumerate(targets)]

    def hide_targets(self) -> None:
        assert self._targetting_enabled
        logging.debug('Targetting disabled')
        self._targetting_enabled = False
