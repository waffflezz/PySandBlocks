from src.settings import border_x, border_y
from src.particles import Sand
from typing import Optional
from src.screen import Display


def line_check(display):
    x = border_x[0] + 1
    for y in range(border_y[1] - 2, border_y[0], -1):
        current_sand: Optional[Sand] = display.get_pixel(x, y)
        next_sand: Optional[Sand] = display.get_pixel(x, y + 1)
        if current_sand is None and next_sand is None:
            return

        if current_sand is None and next_sand:
            sand = wave_algorithm(x, y + 1, display)
            if sand:
                return sand
            return

        if current_sand and next_sand is None:
            sand = wave_algorithm(x, y, display)
            if sand:
                return sand
            return

        if current_sand.color != next_sand.color:
            sand = wave_algorithm(x, y + 1, display)
            if sand:
                return sand


def wave_algorithm(start_x, start_y, display: Display):
    height = len(display.display)
    width = len(display.display[0])
    visited = [[False] * height for _ in range(width)]
    sand_group = []

    stack = [(start_x, start_y)]
    visited[start_x][start_y] = True

    touch_left = False
    touch_right = False
    while stack:
        x, y = stack.pop()

        if x == border_x[0] + 1:
            touch_left = True
        elif x == border_x[1] - 1:
            touch_right = True

        sand_group.append((x, y))

        neighbors = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y),
                     (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1),
                     (x + 1, y + 1)]
        for nx, ny in neighbors:
            if 0 <= nx < width and 0 <= ny < height:
                if not visited[nx][ny] and display.display[nx][
                    ny] is not None and display.display[nx][ny].color == \
                        display.display[x][y].color:
                    stack.append((nx, ny))
                    visited[nx][ny] = True

    if touch_left and touch_right:
        return sand_group
    else:
        return []
