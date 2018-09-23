__author__ = 'sunary'


import Tkinter


CANVAS_SIZE = (600, 600)
TILE_SIZE = 30
BOARD_SIZE = (20, 20)
BOUND_INDEX = [(0, 1), (0, -1), (1, 0), (-1, 0)]
COLOR_CHARS = '0123456789abcdef'


class Board(object):

    def __init__(self, size=(20, 20), default_value=0, dest=None):
        self.size = size
        self.tiles = [[default_value for _ in range(self.size[0])] for _ in range(self.size[1])]
        self.dest = dest

        self.counter = 1
        self.obstacles = []
        self.previous_move_id = None

    def inside(self, x, y):
        return 0 <= x < self.size[0] and 0 <= y < self.size[1]

    def find_max_path(self, source):
        self.tiles[source[0]][source[1]] = self.counter
        self.obstacles.append(source)
        self.counter += 1

        order = []
        _bound_index = BOUND_INDEX
        if self.previous_move_id:
            _bound_index = BOUND_INDEX[self.previous_move_id:] + BOUND_INDEX[:self.previous_move_id]
        for idx in _bound_index:
            if self.inside(source[0] + idx[0], source[1] + idx[1]) and \
                    self.has_path((source[0] + idx[0], source[1] + idx[1]), self.obstacles, self.dest):
                order.append([BOUND_INDEX.index(idx), idx, 0])

        if order:
            for i in range(len(order)):
                if order[i][0] == self.previous_move_id:
                    order[i][2] += 1

                if self.next_bridge(source, order[i][0]):
                    order[i][2] += 2

                if source[0] == self.dest[0] and order[i][1][0] == 0:
                    if source[1] < self.dest[1] and order[i][1][1] > 0:
                        order[i][2] -= 2
                    elif source[1] > self.dest[1] and order[i][1][1] < 0:
                        order[i][2] -= 2
                elif source[1] == self.dest[1] and order[i][1][1] == 0:
                    if source[0] < self.dest[0] and order[i][1][1] > 0:
                        order[i][2] -= 2
                    elif source[0] > self.dest[0] and order[i][1][1] < 0:
                        order[i][2] -= 2

            order = sorted(order, key=lambda x: -x[2])
            self.previous_move_id = order[0][0]
            return self.previous_move_id

    def has_path(self, source, obstacles, dest):
        tiles = [[0 for _ in range(self.size[0])] for _ in range(self.size[1])]

        tiles[source[0]][source[1]] = 1
        for t in obstacles:
            tiles[t[0]][t[1]] = -1

        for j in range(self.size[1]):
            for i in range(self.size[0]):
                if tiles[i][j] == 1:
                    marked = []
                    marked.append((i, j))
                    while marked:
                        i2, j2 = marked.pop(0)
                        for idx in BOUND_INDEX:
                            if self.inside(i2 + idx[0], j2 + idx[1]) and tiles[i2 + idx[0]][j2 + idx[1]] == 0:
                                if (i2 + idx[0], j2 + idx[1]) == dest:
                                    return True
                                marked.append((i2 + idx[0], j2 + idx[1]))
                                tiles[i2 + idx[0]][j2 + idx[1]] = tiles[i2][j2] + 1
        return False

    def next_bridge(self, cursor, move_id):
        next_cursor = (cursor[0] + BOUND_INDEX[move_id][0], cursor[1] + BOUND_INDEX[move_id][1])
        empty_neighbor = []
        for idx in BOUND_INDEX:
            if self.inside(next_cursor[0] + idx[0], next_cursor[1] + idx[1]) and \
                    self.tiles[next_cursor[0] + idx[0]][next_cursor[1] + idx[1]] == 0:
                empty_neighbor.append((next_cursor[0] + idx[0], next_cursor[1] + idx[1]))

        if len(empty_neighbor) >= 2:
            for i in range(len(empty_neighbor)-1):
                for j in range(i+1, len(empty_neighbor)):
                    if not self.has_path(empty_neighbor[i], self.obstacles + [next_cursor, self.dest], empty_neighbor[j]):
                        # TODO count empty block
                        return True
        return False

    def draw(self, canvas):
        for j in range(self.size[1]):
            for i in range(self.size[0]):
                outline = None
                fill = None
                if self.tiles[i][j] < 0:
                    fill = 'grey'
                elif self.tiles[i][j] == 0:
                    outline = 'black'
                else:
                    idx_color1 = (16 - self.tiles[i][j]) % 16
                    idx_color2 = (self.tiles[i][j] - 1) % 16
                    fill = '#{}{}0'.format(COLOR_CHARS[idx_color1], COLOR_CHARS[idx_color2])

                if (i, j) == self.dest:
                    fill = '#000'

                canvas.create_rectangle(TILE_SIZE * i + TILE_SIZE/10, TILE_SIZE * j + TILE_SIZE/10,
                                        TILE_SIZE * (i+1) - TILE_SIZE / 10, TILE_SIZE * (j+1) - TILE_SIZE / 10,
                                        outline=outline,
                                        fill=fill)


class MaxPath(object):
    master = Tkinter.Tk(className='Max path')

    def __init__(self):
        self.board = Board(BOARD_SIZE, dest=(18, 11))
        self.source = [1, 2]

        self.canvas = Tkinter.Canvas(self.master, width=CANVAS_SIZE[0], height=CANVAS_SIZE[1])
        self.canvas.pack()

        self.master.after(0, self.draw)
        self.master.mainloop()

    def draw(self):
        self.canvas.delete(Tkinter.ALL)

        self.update()
        self.master.after(100, self.draw)

    def update(self):
        move_id = self.board.find_max_path(self.source)
        if move_id is not None:
            self.source = [self.source[0] + BOUND_INDEX[move_id][0], self.source[1] + BOUND_INDEX[move_id][1]]
        self.board.draw(self.canvas)


if __name__ == '__main__':
    max_path = MaxPath()
