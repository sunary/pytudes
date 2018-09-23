__author__ = 'sunary'


import Tkinter


CANVAS_SIZE = (400, 600)
BOARD_SIZE = (20, 30)
TILE_SIZE = 20

INF = 9999
FULL_BOUND_INDEX = [(-1, -1), (-1, 1), (1, -1), (1, 1),
                    (0, 1), (1, 0), (0, -1), (-1, 0)]
BOUND_INDEX = [(0, 1), (1, 0), (0, -1), (-1, 0)]
# NAME_INDEX = ['RIGHT', 'DOWN', 'LEFT', 'UP']


class Board(object):

    def __init__(self, size, cursor, value):
        self.size = size
        self.cursor = cursor
        self.previous_move_id = None
        self.value = value

    def is_empty(self, board, tile):
        tile_value = board[tile[0]][tile[1]]
        return tile_value >= 0 and tile_value != self.value

    def is_home(self, board, tile):
        tile_value = board[tile[0]][tile[1]]
        return tile_value == self.value

    def cursor_value(self, board, tile):
        tile_value = board[tile[0]][tile[1]]
        return tile_value == self.value + 1

    def repeat_move_id(self, id1, id2):
        if isinstance(id1, int) and isinstance(id2, int):
            return (id1 + 4) % 4 == (id2 + 4) % 4

        return False

    def previous_cursor(self):
        if self.previous_move_id is None:
            return None

        return self.cursor[0] - BOUND_INDEX[self.previous_move_id][0], \
            self.cursor[1] - BOUND_INDEX[self.previous_move_id][1]

    def length_shortest_path(self, board, source, obstacles, dests=None, dests_value=None):
        if board is None:
            board = [[0 for _ in range(self.size[1])] for _ in range(self.size[0])]

        tiles = [[0 for _ in range(self.size[1])] for _ in range(self.size[0])]
        for obs in obstacles:
            if obs:
                tiles[obs[0]][obs[1]] = -1

        queue_tiles = list()
        queue_tiles.append(self.cursor)

        tiles[source[0]][source[1]] = 1
        while queue_tiles:
            current = queue_tiles.pop(0)

            for i, idx in enumerate(BOUND_INDEX):
                if tiles[current[0]][current[1]] == 0 and self.repeat_move_id(i-2, self.previous_move_id):
                    continue

                if not self.inside(current[0] + idx[0], current[1] + idx[1]):
                    continue

                next_tile = (current[0] + idx[0], current[1] + idx[1])
                if dests is not None and next_tile in dests:
                    return tiles[current[0]][current[1]] + 1
                elif dests_value is not None and board[next_tile[0]][next_tile[1]] == dests_value:
                    return tiles[current[0]][current[1]] + 1

                if tiles[next_tile[0]][next_tile[1]] == 0 and board[next_tile[0]][next_tile[1]] >= 0:
                    queue_tiles.append(next_tile)
                    tiles[next_tile[0]][next_tile[1]] = tiles[current[0]][current[1]] + 1

        return INF

    def nearest_empty(self, board, other_cursors):
        empty_tiles = []

        for j in range(self.size[1]):
            for i in range(self.size[0]):
                if self.empty_near_home(board, (i, j)):
                    empty_tiles.append([i, j, self.length_shortest_path(None, self.cursor, [self.previous_cursor()], dests=[(i, j)])])
                    # empty_tiles.append([i, j, abs(self.cursor[0] - i) + abs(self.cursor[1] - j)])

        nearest_cursor = [INF, INF]
        for cursor in other_cursors:
            if abs(self.cursor[0] - cursor[0]) + abs(self.cursor[1] - cursor[1]) < \
                    abs(self.cursor[0] - nearest_cursor[0]) + abs(self.cursor[1] - nearest_cursor[1]):
                nearest_cursor = cursor

        empty_tiles = sorted(empty_tiles,
                             key=lambda x: [x[2], -(abs(x[0] - nearest_cursor[0]) + abs(x[1] - nearest_cursor[1]))])

        return empty_tiles[0][0], empty_tiles[0][1]

    def empty_near_home(self, board, tile):
        if self.is_empty(board, tile):
            for idx in BOUND_INDEX:
                if self.inside(tile[0] + idx[0], tile[1] + idx[1]) and \
                        self.is_home(board, (tile[0] + idx[0], tile[1] + idx[1])):
                    return True
        return False
    
    def next_empty(self, board, size):
        max_lower_than_size = 0
        memory_id = None
        for i, idx in enumerate(BOUND_INDEX):
            length = self.length_shortest_path(board, (self.cursor[0] + idx[0], self.cursor[1] + idx[1]),
                                               [self.cursor], dests_value=self.value)
            if max_lower_than_size < length <= size:
                max_lower_than_size = length
                memory_id = i

        return memory_id

    def distance_from_home(self, board, other_cursors):
        unstable_tiles = []

        for idx in BOUND_INDEX:
            if board[self.cursor[0] + idx[0]][self.cursor[1] + idx[1]] >= 0:
                unstable_tiles.append((self.cursor[0] + idx[0], self.cursor[1] + idx[1]))

        for j in range(self.size[1]):
            for i in range(self.size[0]):
                if self.cursor_value(board, (i, j)):
                    unstable_tiles.append((i, j))

        min_distance = self.size[0]
        for i, cursor in enumerate(other_cursors):
            enemy_cursor_value = (i + 2) * 2
            if enemy_cursor_value == self.value + 1:
                enemy_cursor_value = 2

            distance = self.length_shortest_path(board, cursor, [self.previous_cursor()], dests_value=self.value)
            if distance < min_distance:
                min_distance = distance

            for j2 in range(self.size[1]):
                for i2 in range(self.size[0]):
                    if board[i2][j2] == enemy_cursor_value - 1:
                        for i3, j3 in unstable_tiles:
                            distance = abs(self.cursor[0] - i2) + abs(self.cursor[1] - j2) + abs(i2 - i3) + abs(j2 - j3)
                            if distance < min_distance:
                                min_distance = distance

        return min_distance

    def back_to_home(self, board):
        home_tiles = []
        for j in range(self.size[1]):
            for i in range(self.size[0]):
                if self.is_home(board, (i, j)):
                    home_tiles.append([i, j, abs(i - self.cursor[0]) + abs(j - self.cursor[1])])

        if len(home_tiles) > 13:
            home_tiles = sorted(home_tiles, key=lambda x: x[2])[:13]

        for i in range(len(home_tiles)):
            home_tiles[i][2] = self.length_shortest_path(board, self.cursor,
                                                         [self.previous_cursor()], dests_value=self.value)

        home_tiles = sorted(home_tiles, key=lambda x: x[2])
        for i, j, _ in home_tiles:
            next_move_id = self.move_to(board, (i, j))
            if next_move_id:
                return next_move_id

    def move_to(self, board, dest):
        min_step = INF
        next_move_id = -1
        for i, idx in enumerate(BOUND_INDEX):
            if self.inside(self.cursor[0] + idx[0], self.cursor[1] + idx[1]) and \
                    (self.is_empty(board, (self.cursor[0] + idx[0], self.cursor[1] + idx[1])) or
                        self.is_home(board, (self.cursor[0] + idx[0], self.cursor[1] + idx[1]))) and \
                    (self.is_home(board, self.cursor) or self.repeat_move_id(i - 2, self.previous_move_id)):
                distance = self.length_shortest_path(board, self.cursor, [self.previous_cursor()], dests=[dest])
                if distance < min_step:
                    min_step = distance
                    next_move_id = i

        return next_move_id

    def inside(self, x, y):
        return 0 <= x < self.size[0] and 0 <= y < self.size[1]


class Robo(object):

    def __init__(self, cursor, value):
        self.value = value
        self.board = Board(BOARD_SIZE, cursor, value)

    def move_by_boundary(self, board, size):
        next_empty = self.board.next_empty(board, size)
        return self.board.move_to(board, next_empty)

    def next_move(self, board, other_cursors):
        if self.board.is_home(board, self.board.cursor):
            nearest_empty = self.board.nearest_empty(board, other_cursors)
            print nearest_empty
            self.board.previous_move_id = self.board.move_to(board, nearest_empty)
        else:
            size = self.board.distance_from_home(board, other_cursors)
            self.board.previous_move_id = self.move_by_boundary(board, size)

        return self.board.previous_move_id


class Referee(object):

    def __init__(self, size=(20, 30)):
        self.size = size
        self.board = [[0 for _ in range(self.size[1])] for _ in range(self.size[0])]

        self.robo1 = Robo((10, 1), 1)
        self.robo2 = Robo((10, 28), 3)

        robo1_init_values = [(9, 0), (9, 1), (9, 2), (10, 0), (10, 1), (10, 2), (11, 0), (11, 1), (11, 2)]
        for i, j in robo1_init_values:
            self.board[i][j] = self.robo1.value

        robo2_init_values = [(9, 27), (9, 28), (9, 29), (10, 27), (10, 28), (10, 29), (11, 27), (11, 28), (11, 29)]
        for i, j in robo2_init_values:
            self.board[i][j] = self.robo2.value

    def update(self):
        robo1_next_step_id = self.robo1.next_move(self.board, [self.robo2.board.cursor])
        robo2_next_step_id = self.robo2.next_move(self.board, [self.robo1.board.cursor])

        self.board = self.fill_surround(self.board, self.robo1.board.cursor, robo1_next_step_id, self.robo1.board.value)
        self.board = self.fill_surround(self.board, self.robo2.board.cursor, robo2_next_step_id, self.robo2.board.value)

        self.robo1.board.cursor = (self.robo1.board.cursor[0] + BOUND_INDEX[robo1_next_step_id][0],
                                   self.robo1.board.cursor[1] + BOUND_INDEX[robo1_next_step_id][1])
        self.robo2.board.cursor = (self.robo2.board.cursor[0] + BOUND_INDEX[robo2_next_step_id][0],
                                   self.robo2.board.cursor[1] + BOUND_INDEX[robo2_next_step_id][1])

    def fill_surround(self, board, cursor, next_step_id, fill_value):
        if board[cursor[0] + BOUND_INDEX[next_step_id][0]][cursor[1] + BOUND_INDEX[next_step_id][1]] == fill_value:
            return board
        else:
            counter_connected = 0
            x = cursor[0] + BOUND_INDEX[next_step_id][0]
            y = cursor[1] + BOUND_INDEX[next_step_id][1]
            board[x][y] = fill_value

            for idx in BOUND_INDEX:
                if self.robo1.board.inside(x + idx[0], y + idx[1]) and board[x + idx[0]][y + idx[1]] == fill_value:
                    counter_connected += 1

            if counter_connected < 2:
                return board

            tiles = [[0 for _ in range(self.size[1])] for _ in range(self.size[0])]
            for j in range(self.size[1]):
                for i in range(self.size[0]):
                    if board[i][j] == fill_value:
                        tiles[i][j] = fill_value

            def no_checked_surround(b, c, f_value):
                for idx2 in FULL_BOUND_INDEX:
                    if self.robo1.board.inside(c[0] + idx2[0], c[1] + idx2[1]) and \
                            b[c[0] + idx2[0]][c[1] + idx2[1]] < 0 and \
                            b[c[0] + idx2[0]][c[1] + idx2[1]] != f_value:
                        return False
                return True

            # TODO: wrong fill surround
            flood_counter = 1
            flood_tiles = []
            for idx in FULL_BOUND_INDEX:
                if self.robo1.board.inside(x + idx[0], y + idx[1]) and \
                        tiles[x + idx[0]][y + idx[1]] == 0 and \
                        no_checked_surround(tiles, (x + idx[0], y + idx[1]), flood_counter):
                    tiles[x + idx[0]][y + idx[1]] = -flood_counter
                    flood_tiles.append((x + idx[0], y + idx[1]))
                    flood_counter += 1

            flood_map = {x: True for x in range(-1, -flood_counter, -1)}
            while flood_tiles:
                tile = flood_counter.pop(0)
                for idx in FULL_BOUND_INDEX:
                    if self.robo1.board.inside(tile[0] + idx[0], tile[1] + idx[1]):
                        if tiles[tile[0] + idx[0]][tile[1] + idx[1]] == 0:
                            tiles[tile[0] + idx[0]][tile[1] + idx[1]] = tiles[tile[0]][tile[1]]
                            flood_tiles.append((tile[0] + idx[0], tile[1] + idx[1]))
                    else:
                        flood_map[tiles[tile[0]][tile[1]]] = False

            for k, v in flood_map.items():
                if v:
                    for j in range(self.size[1]):
                        for i in range(self.size[0]):
                            if tiles[i][j] == k:
                                board[i][j] = fill_value

            return board

    def draw(self, canvas):
        for j in range(self.size[1]):
            for i in range(self.size[0]):
                fill = None
                if self.board[i][j] == self.robo1.value:
                    fill = '#00f'
                elif self.board[i][j] == self.robo2.value:
                    fill = '#0ff'

                if (i, j) == self.robo1.board.cursor:
                    fill = '#0af'
                elif (i, j) == self.robo2.board.cursor:
                    fill = '#aff'

                if fill is not None:
                    canvas.create_rectangle(TILE_SIZE * i + TILE_SIZE / 10, TILE_SIZE * j + TILE_SIZE / 10,
                                            TILE_SIZE * (i + 1) - TILE_SIZE / 10, TILE_SIZE * (j + 1) - TILE_SIZE / 10,
                                            fill=fill)


class Splix(object):
    master = Tkinter.Tk(className='Splix')

    def __init__(self):
        self.referee = Referee()

        self.canvas = Tkinter.Canvas(self.master, width=CANVAS_SIZE[0], height=CANVAS_SIZE[1])
        self.canvas.pack()

        self.master.after(0, self.draw)
        self.master.mainloop()

    def draw(self):
        self.canvas.delete(Tkinter.ALL)

        self.update()
        self.master.after(500, self.draw)

    def update(self):
        self.referee.update()
        self.referee.draw(self.canvas)


if __name__ == '__main__':
    splix = Splix()
