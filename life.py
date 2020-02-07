from time import sleep
from collections import Counter
from itertools import chain


def main():
    def ascii_print(alive_coords, mx, mn):
        def draw(x, y):
            return 'X' if (x, y) in alive_coords else '-'

        # print world, line by line, localized to an extended bounding box
        for y in range(mn[1] - 1, mx[1] + 2):
            print(''.join([draw(x, y) for x in range(mn[0] - 1, mx[0] + 2)]))

    alive_coords = set(glider())  #box() #blinker()
    for step in range(200):
        alive_coords, mx, mn = sim_step(alive_coords)
        ascii_print(alive_coords, mx, mn)
        #sleep(0.125)
        print()
    print(alive_coords)


# functional approach which uses more memory, but preserves the previous data.
def sim_step(alive_coords: set) -> set:
    def all_neighbors(alive_coords):
        return chain.from_iterable([neighbors(x, y) for x, y in alive_coords])

    def neighbors(x, y):
        return [(x + x1, y + y1) for x1 in [-1, 0, 1] for y1 in [-1, 0, 1]
                if not (x1 == 0 and y1 == 0)]

    def life(coord, neighbors):
        return neighbors == 3 or (neighbors == 2 and coord in alive_coords)

    next_generation = set()
    # bounding box - max, min
    mx = mn = tuple()
    for coord, count in Counter(all_neighbors(alive_coords)).items():
        if life(coord, count):
            next_generation.add(coord)

            if len(mx) == 0:
                mx, mn = coord, coord
            else:
                mx = max(mx[0], coord[0]), max(mx[1], coord[1])
                mn = min(mn[0], coord[0]), min(mn[1], coord[1])

    return (next_generation, mx, mn)


def glider():
    return [(0, 1), (0, 2), (1, 0), (1, 1), (2, 2)]


def box():
    return [(0, 0), (0, 1), (1, 0), (1, 1)]


def blinker():
    return [(1, 1), (1, 2), (1, 0)]


def glider_chaos():
    return [(0, 1), (0, 2), (1, 0), (1, 1), (2, 2), (-5, -5), (-5, -6),
            (-5, -4)]


if __name__ == "__main__":
    main()
