from typing import List

from scenes.scenes_base import Scene
from views.artists.scene_artist_base import SceneArtist
from views.screen_factory import get_screen
from views.view_base import View


class SceneView(View):

    def __init__(self, scene: Scene, artists: List[SceneArtist]) -> None:
        self._scene = scene
        self._screen = get_screen()
        self._artists = artists

    def update(self) -> None:
        self._screen.clear()
        for artist in self._artists:
            artist.render(screen=self._screen, scene=self._scene)
        # VERY IMPORTANT TO CALL UPDATE ONCE
        self._screen.update()
