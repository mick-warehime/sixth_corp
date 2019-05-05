from enum import Enum
from itertools import accumulate
from typing import Any, List, Sequence, Set, Tuple

from pygame.rect import Rect


class _LayoutDirections(Enum):
    VERTICAL = 'vertical'
    HORIZONTAL = 'horizontal'


class Layout(object):
    """Determines Rect positions for ingame elements.

    Layouts are used to organize the positions of rects on the screen, with an
    interface to pull out the objects associated with any point.
    """

    def __init__(self, elements: Sequence[Tuple[Any, int]] = (),
                 direction: str = 'vertical',
                 dimensions: Tuple[int, int] = None) -> None:
        """Initialize a Layout.

        Args:
            elements: The ingame objects composing the Layout, paired with their
                weights. E.g., [(obj_A, 2), (obj_B, 1), (obj_C, 4)] corresponds
                to assigning a rect to obj_A that is twice as big as that of
                obj_B and half as big as that of obj_C. Rects are ordered in the
                layout from top (left) to bottom (right).  "None" elements are
                treated as gaps between other elements. elements which are
                themselves Layout objects are treated differently from others in
                that all API calls to this Layout are passed through these
                elements. A Layout may only appear as a single element.
            direction: 'vertical' or 'horizontal' layout direction.
            dimensions: (optional) Set a fixed absolute dimension for the
                layout container. This should only be passed to the top-level
                Layout and should match the desired screen (w,h) size.
        """
        self._elements = tuple(x[0] for x in elements)
        self._cumulative_weights = tuple(
            accumulate((float(x[1]) for x in elements), lambda a, b: a + b))
        if self._cumulative_weights:
            self._total_weight = self._cumulative_weights[-1]
        else:
            self._total_weight = 0.0

        try:
            self._direction = _LayoutDirections(direction)
        except ValueError:
            raise ValueError('Input direction must be one of {}'.format(
                [k.value for k in _LayoutDirections]))

        self._container: Rect = None
        if dimensions is not None:
            self._set_container(Rect(0, 0, *dimensions))

    def object_at(self, x: int, y: int) -> Any:
        """Returns the object at the specified point.

        If no object is at the specified point, i.e. if it corresponds to a
        gap between objects, this function returns None.

        Args:
            x: horizontal direction from the left.
            y: vertical direction from the top.
        """
        assert self._container is not None
        if not self._container.collidepoint(x, y):  # point is outside layout.
            return None

        if not self._elements:
            return None

        element = self._elements[self._element_index_at(x, y)]
        if isinstance(element, Layout):
            return element.object_at(x, y)
        return element

    def rect_at(self, x: int, y: int) -> Rect:
        """Returns the Rect associated with the specified point.

        A new Rect object is generated at each call.

        Args:
            x: horizontal direction from the left.
            y: vertical direction from the top.
        """
        assert self._container is not None
        if not self._container.collidepoint(x, y):  # point is outside layout.
            raise ValueError('Point is outside layout bounds.')

        if not self._elements:
            return self._container.copy()

        index = self._element_index_at(x, y)
        element = self._elements[index]
        if isinstance(element, Layout):
            return element.rect_at(x, y)

        return self._rect_for_index(index)

    def get_rects(self, element: Any) -> List[Rect]:
        """Get the Rects of an element in the Layout.

        If the element is included more than once, then all of its associated
        Rects are returned. If the element is not in the layout, then an empty
        list is returned.

        If the element is this Layout instance, then all Rects are returned.

        If the element is None, then all 'gap' rects are returned.

        Args:
            element: Component of the layout whose rect we would like.
        """

        assert self._container is not None

        # All rects case
        rects = []
        if element is self:
            for index, candidate in enumerate(self._elements):
                if isinstance(candidate, Layout):
                    rects.extend(candidate.get_rects(candidate))
                    rects.append(candidate._container)
                else:
                    rects.append(self._rect_for_index(index))
            return rects

        # Single element case
        for index, candidate in enumerate(self._elements):
            if element == candidate:
                rects.append(self._rect_for_index(index))
            elif isinstance(candidate, Layout):
                rects.extend(candidate.get_rects(element))

        return rects

    def all_objects(self) -> List[Any]:
        """All objects stored in the layout.

        This includes the objects within child Layouts, but not the Layout
        objects themselves.
        """
        out = []
        for elem in self._elements:
            if elem is None:
                continue
            elif isinstance(elem, Layout):
                out.extend(elem.all_objects())
            else:
                out.append(elem)
        return out

    def _rect_for_index(self, index: int) -> Rect:
        assert 0 <= index < len(self._elements)
        # The rect is shifted to match the container position and scaled
        # to match its weight and the layout orientation.
        weight = self._cumulative_weights[index]
        prev_weight = 0 if index == 0 else self._cumulative_weights[index - 1]
        container = self._container
        x = container.x
        y = container.y
        w = container.width
        h = container.height
        if self._direction == _LayoutDirections.HORIZONTAL:
            x += (prev_weight / self._total_weight) * container.width
            w = (weight - prev_weight) * container.width / self._total_weight
        else:
            y += (prev_weight / self._total_weight) * container.height
            h = (weight - prev_weight) * container.height / self._total_weight
        return Rect(x, y, w, h)

    def _element_index_at(self, x: int, y: int) -> int:
        # Find the index of the rect corresponding to the input point. We only
        # consider one direction (x or y). The cumulative weights represent the
        # right (or bottom) edges of each rect.
        assert self._container is not None
        if self._direction == _LayoutDirections.HORIZONTAL:
            pos_weight = float(x - self._container.x) / self._container.width
        else:
            pos_weight = float(y - self._container.y) / self._container.height
        pos_weight *= self._total_weight

        if pos_weight < self._cumulative_weights[0]:
            return 0
        # largest index of all weights less than pos_weight
        index = 0
        for index, _ in enumerate(w for w in self._cumulative_weights
                                  if w <= pos_weight):
            pass
        return index + 1

    def _set_container(self, container: Rect) -> None:
        """Specify Layout container and containers for all child Layouts."""
        assert self._container is None, 'containers only specified once.'
        self._container = container

        layout_children: Set[Layout] = set()
        for index, child in enumerate(self._elements):
            if isinstance(child, Layout):
                if child in layout_children:
                    raise ValueError('Layout may only exist as one element.')
                child._set_container(self._rect_for_index(index))
                layout_children.add(child)
