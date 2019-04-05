from pygame.rect import Rect

from views.layouts import Layout


def test_vertical_layout_object_at():
    # AABBBB--CCCC

    layout = Layout([('A', 1), ['B', 2], (None, 1), ('C', 2)],
                    direction='vertical', dimensions=(12, 12))

    x = 6

    assert layout.object_at(x, 0) == 'A'
    assert layout.object_at(x, 3) == 'B'
    assert layout.object_at(x, 7) is None
    assert layout.object_at(x, 9) == 'C'


def test_horizontal_layout_rect_at():
    # AABBBB--CCCC

    layout = Layout([('A', 1), ['B', 2], (None, 1), ('C', 2)],
                    direction='horizontal', dimensions=(12, 12))

    y = 6

    assert layout.rect_at(0, y) == Rect(0, 0, 2, 12)
    assert layout.rect_at(3, y) == Rect(2, 0, 4, 12)
    assert layout.rect_at(7, y) == Rect(6, 0, 2, 12)
    assert layout.rect_at(9, y) == Rect(8, 0, 4, 12)


def test_nested_layouts():
    # ---------
    # ---------
    # ---------
    # ---ABC---
    # ---ABC---
    # ---ABC---
    # ---------
    # ---------
    # ---------

    inner_layout = Layout([('A', 1), ['B', 1], ('C', 1)],
                          direction='horizontal')
    hor_layout = Layout([(None, 1), (inner_layout, 1), (None, 1)],
                        direction='horizontal')
    outer_layout = Layout([(None, 1), (hor_layout, 1), (None, 1)],
                          dimensions=(9, 9))

    assert outer_layout.object_at(3, 3) == 'A'
    assert outer_layout.object_at(4, 3) == 'B'
    assert outer_layout.object_at(5, 5) == 'C'


def test_empty_layout_rect_is_container():
    empty = Layout((), dimensions=(3, 4))

    assert empty.rect_at(0, 0) == Rect(0, 0, 3, 4)


def test_get_rects_single_element():
    layout = Layout([('A', 1), ('B', 2), ('A', 1)], 'horizontal', (4, 4))
    actual = tuple(layout.get_rects('A'))
    expected = (Rect(0, 0, 1, 4), Rect(3, 0, 1, 4))
    assert actual == expected


def test_get_rects_all():
    inner_layout = Layout([('A', 1), ('B', 2), (None, 1)], 'horizontal')
    outer_layout = Layout([(inner_layout, 1),
                           ('D', 1),
                           (None, 2)],
                          'vertical', (20, 20))

    actual = tuple(outer_layout.get_rects(outer_layout))

    expected = (Rect(0, 0, 5, 5), Rect(0, 0, 20, 5),
                Rect(5, 0, 10, 5), Rect(15, 0, 5, 5), Rect(0, 5, 20, 5),
                Rect(0, 10, 20, 10))
    for rect in actual:
        assert rect in expected
    for rect in expected:
        assert rect in actual
