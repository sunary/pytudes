__author__ = 'sunary'


import random
import Tkinter


CANVAS_SIZE = (600, 600)
TILE_SIZE = 30
BOARD_SIZE = (20, 20)
BOUND_INDEX = [(-1, 0), (0, -1), (0, 1), (1, 0)]
COLOR_CHARS = '0123456789abcdef'


class Snake(object):

    def __init__(self):
        self.tiles = []

    def reset(self):
        self.tiles = [(8, 9), (9, 9), (10, 9), (11, 9)]

    def move_to(self, position):
        self.tiles = [position] + self.tiles[:-1]

    def eat(self, position):
        self.tiles = [position] + self.tiles

    def draw(self, canvas):
        for i, t in enumerate(self.tiles):
            idx_color1 = (16 - i) % 16
            idx_color2 = (i - 1) % 15
            idx_color3 = 0
            fill = '#{}{}{}'.format(COLOR_CHARS[idx_color1], COLOR_CHARS[idx_color2], COLOR_CHARS[idx_color3])
            if i == 0:
                fill = 'blue'
            canvas.create_rectangle(TILE_SIZE * t[0] + TILE_SIZE / 10, TILE_SIZE * t[1] + TILE_SIZE / 10,
                                    TILE_SIZE * (t[0] + 1) - TILE_SIZE / 10, TILE_SIZE * (t[1] + 1) - TILE_SIZE / 10,
                                    fill=fill)


class Board(object):

    def __init__(self, size=(20, 20)):
        self.size = size
        self.food = None
        self.snake = Snake()
        self.snake.reset()
        self.random_food()

    def draw(self, canvas):
        for j in range(self.size[1]):
            for i in range(self.size[0]):
                canvas.create_rectangle(TILE_SIZE * i + TILE_SIZE / 10, TILE_SIZE * j + TILE_SIZE / 10,
                                        TILE_SIZE * (i + 1) - TILE_SIZE / 10, TILE_SIZE * (j + 1) - TILE_SIZE / 10,
                                        outline='black')

        if self.food:
            canvas.create_rectangle(TILE_SIZE * self.food[0] + TILE_SIZE / 10, TILE_SIZE * self.food[1] + TILE_SIZE / 10,
                                    TILE_SIZE * (self.food[0] + 1) - TILE_SIZE / 10, TILE_SIZE * (self.food[1] + 1) - TILE_SIZE / 10,
                                    fill='gray')
        self.snake.draw(canvas)

    def random_food(self):
        tiles = [[True for _ in range(self.size[0])] for _ in range(self.size[1])]
        for t in self.snake.tiles:
            tiles[t[0]][t[1]] = False

        empty_tiles = []
        for j in range(self.size[1]):
            for i in range(self.size[0]):
                if tiles[i][j]:
                    empty_tiles.append((i, j))

        if empty_tiles:
            self.food = random.choice(empty_tiles)

    def move(self):
        next_position = self.next_move()
        if next_position:
            if next_position == self.food:
                self.snake.eat(next_position)
                self.random_food()
            else:
                self.snake.move_to(next_position)

    def next_move(self):
        move_to_food = self.find_shortest_path(self.snake.tiles[0], self.snake.tiles[1:], self.food)
        move_to_tail = self.find_longest_path(self.snake.tiles[0], self.snake.tiles[1:-1], self.snake.tiles[-1])
        if self.find_shortest_path(self.food, self.snake.tiles[:-1], self.snake.tiles[-1]):
            return move_to_food or move_to_tail
        else:
            return move_to_tail or move_to_food

    def find_shortest_path(self, source, obstacles, dest):
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
                                marked.append((i2 + idx[0], j2 + idx[1]))
                                tiles[i2 + idx[0]][j2 + idx[1]] = tiles[i2][j2] + 1

        if tiles[dest[0]][dest[1]] > 0:
            back = (dest[0], dest[1])
            while tiles[back[0]][back[1]] != 2:
                random.shuffle(BOUND_INDEX)
                for idx in BOUND_INDEX:
                    if self.inside(back[0] + idx[0], back[1] + idx[1]) and \
                            tiles[back[0] + idx[0]][back[1] + idx[1]] == tiles[back[0]][back[1]] - 1:
                        back = (back[0] + idx[0], back[1] + idx[1])
                        break
            return back
        else:
            return None

    def find_longest_path(self, source, obstacles, dest):
        # TODO implement algorithm/max_path
        return self.find_shortest_path(source, obstacles, dest)

    def inside(self, x, y):
        return 0 <= x < self.size[0] and 0 <= y < self.size[1]


class SnakeGame(object):
    master = Tkinter.Tk(className='Snake')

    def __init__(self):
        self.board = Board(BOARD_SIZE)

        self.canvas = Tkinter.Canvas(self.master, width=CANVAS_SIZE[0], height=CANVAS_SIZE[1])
        self.canvas.pack()

        self.master.after(0, self.draw)
        self.master.mainloop()

    def draw(self):
        self.canvas.delete(Tkinter.ALL)

        self.update()
        self.master.after(20, self.draw)

    def update(self):
        self.board.move()
        self.board.draw(self.canvas)


if __name__ == '__main__':
    snake = SnakeGame()
