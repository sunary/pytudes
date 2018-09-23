__author__ = 'sunary'


import Tkinter
import math
import random


CANVAS_SIZE = (700, 500)

BOIDS_SIZE = (10, 10)
MOVE_SIZE = 1.1
COHESION_SIZE = 50
SEPARATION_SIZE = 15


class Boid(object):

    def __init__(self):
        self.loc = None
        self.angle = None
        self.triangle = [[0, 0] for _ in range(3)]

    def set(self, loc, angle):
        self.loc = loc
        self.angle = angle

        self.update_triangle()

    def draw(self, canvas):
        canvas.create_polygon(self.triangle[0][0], self.triangle[0][1],
                              self.triangle[1][0], self.triangle[1][1],
                              self.triangle[2][0], self.triangle[2][1], fill='red')

    def update(self, boids):
        neighbour_bolds = self.check_around(boids)
        new_move_size = MOVE_SIZE + 1.0/(len(neighbour_bolds) + 2)

        if len(neighbour_bolds):
            self.angle = 0.5*self.angle + 0.5*self.alignment_angle(neighbour_bolds)

        self.loc = [self.loc[0] + new_move_size * math.cos(self.angle),
                    self.loc[1] - new_move_size * math.sin(self.angle)]

        if len(neighbour_bolds):
            cohesion_angle = self.cohesion_angle(neighbour_bolds)
            self.separation_avoid(neighbour_bolds, move_size=MOVE_SIZE/2, temp_angle=cohesion_angle)

        self.update_triangle()

    def update_triangle(self):
        self.loc[0] = CANVAS_SIZE[0] + self.loc[0] if self.loc[0] < 0 else self.loc[0]
        self.loc[1] = CANVAS_SIZE[1] + self.loc[1] if self.loc[1] < 0 else self.loc[1]

        self.loc[0] = self.loc[0] - CANVAS_SIZE[0] if self.loc[0] > CANVAS_SIZE[0] else self.loc[0]
        self.loc[1] = self.loc[1] - CANVAS_SIZE[1] if self.loc[1] > CANVAS_SIZE[1] else self.loc[1]

        self.triangle[0] = [self.loc[0] + 10 * math.cos(self.angle), self.loc[1] - 10 * math.sin(self.angle)]
        self.triangle[1] = [self.loc[0] + 8 * math.cos(self.angle + math.pi * 5/6),
                            self.loc[1] - 8 * math.sin(self.angle + math.pi * 5/6)]
        self.triangle[2] = [self.loc[0] + 8 * math.cos(self.angle + math.pi * 7/6),
                            self.loc[1] - 8 * math.sin(self.angle + math.pi * 7/6)]

    def check_around(self, boids, r=COHESION_SIZE):
        neighbour_bolds = []
        for b in boids:
            if (self.loc[0] - b.loc[0])**2 + (self.loc[1] - b.loc[1])**2 < r**2:
                neighbour_bolds.append(b)

        return neighbour_bolds

    def alignment_angle(self, neighbour_boids):
        return sum([b.angle for b in neighbour_boids])/len(neighbour_boids)

    def cohesion_angle(self, neighbour_boids):
        middle = [sum([b.loc[0] for b in neighbour_boids])/len(neighbour_boids),
                  sum([b.loc[1] for b in neighbour_boids])/len(neighbour_boids)]

        return math.atan2(middle[1] - self.loc[1], middle[0] - self.loc[0])

    def separation_avoid(self, neighbour_boids, move_size=MOVE_SIZE, temp_angle=None):
        move_size_cos = math.cos(temp_angle) * move_size
        move_size_sin = math.sin(temp_angle) * move_size

        for i in range(7, 1, -1):
            has_collision = False
            for b in neighbour_boids:
                b_distance = (self.loc[0] + move_size_cos*i/8 - b.loc[0])**2 + (self.loc[1] - move_size_sin*i/8 - b.loc[1])**2
                if b_distance < SEPARATION_SIZE**2:
                    has_collision = True
                    break

            if not has_collision:
                self.loc = [self.loc[0] + move_size_cos*i/8, self.loc[1] - move_size_sin*i/8]
                return


class Flocking(object):

    master = Tkinter.Tk(className='Flocking')

    def __init__(self):
        self.boids = [Boid() for _ in range(BOIDS_SIZE[0] * BOIDS_SIZE[1])]

        for i in range(1, BOIDS_SIZE[0] + 1):
            for j in range(1, BOIDS_SIZE[1] + 1):
                self.boids[(i-1) * BOIDS_SIZE[0] + (j-1)].set(loc=[i * 50, j * 50], angle=math.pi * random.randrange(-10, 10)/10)

        self.canvas = Tkinter.Canvas(self.master, width=CANVAS_SIZE[0], height=CANVAS_SIZE[1])
        self.canvas.pack()

        self.master.after(0, self.draw)
        self.master.mainloop()

    def draw(self):
        self.canvas.delete(Tkinter.ALL)

        for i in range(len(self.boids)):
            self.boids[i].draw(self.canvas)

        self.update()
        self.master.after(20, self.draw)

    def update(self):
        temp_boids = self.boids[:]
        for i in range(len(self.boids)):
            self.boids[i].update(temp_boids[:i] + temp_boids[i+1:])


if __name__ == '__main__':
    flocking = Flocking()
