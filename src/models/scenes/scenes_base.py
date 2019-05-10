"""Basic interfaces for scenes, effects, and resolutions."""
import abc
import random
from bisect import bisect_left
from itertools import accumulate
from typing import Callable, Sequence, Tuple


class Scene(metaclass=abc.ABCMeta):
    """Basic representation of a game scene."""

    @abc.abstractmethod
    def is_resolved(self) -> bool:
        """Whether the scene is resolved."""

    @abc.abstractmethod
    def get_resolution(self) -> 'Resolution':
        """The resolution to the scene (if is_resolved is True)."""

    @property
    @abc.abstractmethod
    def background_image(self) -> str:
        """The path to the background image."""


EffectType = Callable[[], None]


class Resolution(object):
    """Determines the next scene."""

    def next_scene(self) -> Scene:
        raise NotImplementedError

    @property
    def effects(self) -> Sequence[EffectType]:
        """These are implemented when the resolution occurs."""
        raise NotImplementedError


class BasicResolution(Resolution):

    def __init__(self, scene_fun: Callable[[], Scene],
                 effect_seq: Tuple[EffectType, ...] = ()) -> None:
        self._scene_fun = scene_fun
        self._effect_seq = effect_seq

    def next_scene(self) -> Scene:
        return self._scene_fun()

    @property
    def effects(self) -> Sequence[EffectType]:
        return self._effect_seq


class ProbabilisticResolution(Resolution):
    """A Resolution that probabilistically selects from other resolutions.

    Each possible resolution is given a positive weight. Its relative
    probability is its weight divided by the sum of all weights.

    At initialization, a resolution is randomly selected as above and its
    corresponding scene/effects are returned. All invocations of next_scene
    and effects then return the same values.
    """

    def __init__(self,
                 resolutions_weights: Sequence[Tuple[Resolution, int]]) -> None:
        assert resolutions_weights, 'At least one resolution must be specified.'
        assert all(rw[1] >= 0 for rw in resolutions_weights), (
            'weights must be positive, got {}'.format(resolutions_weights))

        # Sample resolutions according to weight.
        cum_weights = list(accumulate((rw[1] for rw in resolutions_weights),
                                      lambda a, b: a + b))
        num = random.randint(0, cum_weights[-1]-1) + 1
        index = bisect_left(cum_weights, num)

        assert index < len(resolutions_weights), (num, index)
        self._sampled_res: Resolution = resolutions_weights[index][0]

    def next_scene(self) -> Scene:
        return self._sampled_res.next_scene()

    @property
    def effects(self) -> Sequence[EffectType]:
        return self._sampled_res.effects


SceneConstructor = Callable[[], Scene]
