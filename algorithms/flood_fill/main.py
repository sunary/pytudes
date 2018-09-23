__author__ = 'sunary'


import Tkinter


CANVAS_SIZE = (600, 600)
TILE_SIZE = 30
BOARD_SIZE = (20, 20)
BOUND_INDEX = [(-1, 0), (0, -1), (0, 1), (1, 0)]
COLOR_CHARS = '0123456789abcdef'


class Board(object):

    def __init__(self, size=(20, 20), default_value=0):
        self.size = size
        self.tiles = [[default_value for _ in range(self.size[0])] for _ in range(self.size[1])]
        self.counter = 0

    def inside(self, x, y):
        return 0 <= x < self.size[0] and 0 <= y < self.size[1]

    def set_tiles(self, start, obstacles):
        self.counter = 1
        self.tiles[start[0]][start[1]] = self.counter

        for obs in obstacles:
            self.tiles[obs[0]][obs[1]] = -1

    def flood(self):
        for j in range(self.size[1]):
            for i in range(self.size[0]):
                if self.tiles[i][j] == self.counter:
                    for idx in BOUND_INDEX:
                        if self.inside(i + idx[0], j + idx[1]) and self.tiles[i + idx[0]][j + idx[1]] == 0:
                            self.tiles[i + idx[0]][j + idx[1]] = self.counter + 1

        self.counter += 1

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

                canvas.create_rectangle(TILE_SIZE * i + TILE_SIZE/10, TILE_SIZE * j + TILE_SIZE/10,
                                        TILE_SIZE * (i+1) - TILE_SIZE / 10, TILE_SIZE * (j+1) - TILE_SIZE / 10,
                                        outline=outline,
                                        fill=fill)


class FloodFill(object):

    master = Tkinter.Tk(className='Flood Fill')

    def __init__(self):
        self.board = Board(BOARD_SIZE)
        self.board.set_tiles((10, 10),
                             [(9, 10), (10, 9), (17, 17), (17, 18), (17, 19), (18, 17), (19, 17)])

        self.canvas = Tkinter.Canvas(self.master, width=CANVAS_SIZE[0], height=CANVAS_SIZE[1])
        self.canvas.pack()

        self.master.after(0, self.draw)
        self.master.mainloop()

    def draw(self):
        self.canvas.delete(Tkinter.ALL)

        self.update()
        self.master.after(500, self.draw)

    def update(self):
        self.board.flood()
        self.board.draw(self.canvas)


if __name__ == '__main__':
    ff = FloodFill()
