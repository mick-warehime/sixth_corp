from typing import Callable, Union

from pygame.rect import Rect

from models.scenes.decision_scene import DecisionInfo, DecisionScene
from models.scenes.scenes_base import Scene
from views.artists.drawing_utils import rescale_horizontal
from views.artists.scene_artist_base import SceneArtist
from views.pygame_screen import Screen

_TextFun = Callable[[], str]
_TextOrFun = Union[str, _TextFun]

_PROMPT_FONT_SIZE = rescale_horizontal(50)[0]
_CHOICE_FONT_SIZE = rescale_horizontal(40)[0]


def _render_text_data(data: DecisionInfo, rect: Rect, screen: Screen) -> None:
    # Use data options to specify arguments to screen.render_text.

    if data.is_prompt:
        args = [data.text, _PROMPT_FONT_SIZE]
    else:
        args = ['{}: {}'.format(data.key, data.text), _CHOICE_FONT_SIZE]
    args.extend([rect, data.color, data.centered])

    screen.render_text_in_rect(*args)  # type: ignore


class DecisionArtist(SceneArtist):
    """Render the components of the decision scene."""

    def render(self, screen: Screen, scene: Scene) -> None:
        assert isinstance(scene, DecisionScene)

        datas = [obj for obj in scene.layout.all_objects()
                 if isinstance(obj, DecisionInfo)]

        for data in datas:
            rects = scene.layout.get_rects(data)
            assert len(rects) == 1
            _render_text_data(data, rects[0], screen)
