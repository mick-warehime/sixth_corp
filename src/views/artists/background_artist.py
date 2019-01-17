from scenes.scenes_base import Scene
from views.artists.scene_artist_base import SceneArtist
from views.screen_base import Screen
from world.world import get_location


class BackgroundArtist(SceneArtist):

    def render(self, screen: Screen, scene: Scene) -> None:
        background_image = get_location().background_image_path
        screen.render_image(background_image, 0, 0, 0, 0)
