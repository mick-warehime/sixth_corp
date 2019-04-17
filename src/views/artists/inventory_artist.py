from pygame.rect import Rect

from data.colors import WHITE, YELLOW, LIGHT_GRAY, DARK_GRAY, BLUE
from models.characters.mods_base import Mod
from models.scenes.inventory_scene import InventoryScene, SlotHeader
from models.scenes.scenes_base import Scene
from views.artists.scene_artist_base import SceneArtist
from views.pygame_screen import Screen

_FONT_SIZE = 40


def _render_slot_header(slot_data: SlotHeader, rect: Rect,
                        screen: Screen) -> None:
    screen.render_rect(rect, LIGHT_GRAY, 0)
    screen.render_rect(rect, DARK_GRAY, 2)

    text = '{} - {} / {}'.format(slot_data.slot.value, slot_data.num_filled,
                                 slot_data.capacity)

    screen.render_text(text, _FONT_SIZE, rect.x + 10, rect.center[1] - 10, BLUE)


def _render_mod_slot(mod: Mod, rect: Rect, screen: Screen) -> None:
    pass


class InventoryArtist(SceneArtist):

    def render(self, screen: Screen, scene: Scene) -> None:
        assert isinstance(scene, InventoryScene)

        # Scene title and exit key
        screen.render_texts(list(scene.options),
                            font_size=35, x=20, y=10, color=WHITE, spacing=30)

        layout = scene.layout
        all_rects = layout.get_rects(layout)
        scene_objects = {layout.object_at(*rect.center) for rect in all_rects}

        for obj in scene_objects:
            if obj is None:
                continue

            rects = layout.get_rects(obj)
            if isinstance(obj, SlotHeader):
                assert len(rects) == 1
                _render_slot_header(obj, rects[0], screen)
            elif isinstance(obj, Mod):
                assert len(rects) == 1
                _render_mod_slot(obj, rects[0], screen)
