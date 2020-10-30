import numpy as np
import math
from queue import PriorityQueue
import os.path as path
from sys import argv


class Cave:
    def __init__(self, pos_x, pos_y, index):
        self.posX = pos_x
        self.posY = pos_y
        self.index = index
        self.g_score = float("inf")
        self.f_score = float("inf")
        self.connections = []

    def get_pos(self):
        return self.posX, self.posY

    def get_name(self):
        return self.index + 1

    def get_index(self):
        return self.index

    def get_connections(self):
        return self.connections

    def __eq__(self, other):
        return self.get_pos() == other.get_pos()

    def __lt__(self, other):
        return self.f_score < other.f_score

    def __gt__(self, other):
        return self.f_score > other.f_score

    def __hash__(self):
        return id(self)


def get_distance(cv1, cv2):
    x1, y1 = cv1
    x2, y2 = cv2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def cave_data(raw_caves):
    caves_coord = raw_caves[1: raw_caves[0] * 2 + 1]
    cave_cords = np.array([caves_coord[i:i + 2] for i in range(0, len(caves_coord), 2)])
    caves = {}
    index = 0
    for cv in cave_cords:
        caves[index] = Cave(cv[0], cv[1], index)
        index += 1
    cav_conn_rows = raw_caves[raw_caves[0] * 2 + 1:]
    connection_matrix = np.array(
        [cav_conn_rows[i:i + raw_caves[0]] for i in range(0, len(cav_conn_rows), raw_caves[0])])
    for ind, rows in enumerate(connection_matrix):
        for idx, val in enumerate(rows):
            if val == 1:
                caves[idx].connections.append(caves[ind])
    return caves


def pathfinder(start, end):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    start.g_score = 0
    start.f_score = 0

    start.f_score = get_distance(start.get_pos(), end.get_pos())
    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[1]  # type: Cave
        open_set_hash.remove(current)

        if current == end:
            return reconstruct_path(came_from, end)
        for con_cave in current.get_connections():  # type: Cave
            temp_g_score = current.g_score + get_distance(con_cave.get_pos(), current.get_pos())

            if temp_g_score < con_cave.g_score:
                came_from[con_cave] = current
                con_cave.g_score = temp_g_score
                con_cave.f_score = temp_g_score
                if con_cave not in open_set_hash:
                    open_set.put((con_cave.f_score, con_cave))
                    open_set_hash.add(con_cave)

    return None, None


def reconstruct_path(came_from, current):
    paths = [current.get_name()]
    dist = 0

    while current in came_from:  # type: Cave
        dist += get_distance(current.get_pos(), came_from[current].get_pos())
        current = came_from[current]
        paths.append(current.get_name())

    return list(reversed(paths)), round(dist, 2)


def main():
    if len(argv) < 2:
        exit(0)
    else:
        cav_file_name = argv[1].strip()
        with open(f'{cav_file_name}.cav') as f:
            raw_cave_data = list(map(int, f.readline().split(',')))
            caves = cave_data(raw_cave_data)
            route, distance = pathfinder(caves.get(0), caves.get(len(caves.keys()) - 1))

        with open(f'{cav_file_name}.csn', 'w+') as f1:
            if route:
                f1.write(' '.join(map(str, route)))
            else:
                f1.write('0')


if __name__ == '__main__':
    main()
