__author__ = 'sunary'


import Tkinter
import math
import random


CANVAS_SIZE = (700, 500)
MOVE_SIZE = 0.5

BOIDS_SIZE = (10, 10)

SEPARATION_STRENGTH = 0.5
SEPARATION_DISTANCE = 40.0
COHESION_STRENGTH = 0.1
COHESION_DISTANCE = 30.0
ALIGNMENT_STRENGTH = 0.5
ALIGNMENT_DISTANCE = 40.0


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
        separation_force = self.separation(boids, SEPARATION_STRENGTH, SEPARATION_DISTANCE)
        cohesion_force = self.cohesion(boids, COHESION_STRENGTH, COHESION_DISTANCE)
        alignment_force = self.alignment(boids, ALIGNMENT_STRENGTH, ALIGNMENT_DISTANCE)

        move = [math.cos(self.angle) * MOVE_SIZE, -math.sin(self.angle) * MOVE_SIZE]
        move = [move[0] + separation_force[0], move[1] + separation_force[1]]
        move = [move[0] + cohesion_force[0], move[1] + cohesion_force[1]]
        move = [move[0] + alignment_force[0], move[1] + alignment_force[1]]

        self.angle = math.atan2(move[1], move[0])
        self.loc = [self.loc[0] + move[0], self.loc[1] + move[1]]

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

    def separation(self, boids, strength, distance):
        separation_force = [0, 0]
        for b in boids:
            if self.distance(b) < distance:
                offset = (self.loc[0] - b.loc[0], self.loc[1] - b.loc[1])
                separation_force[0] += offset[0] / distance
                separation_force[1] += offset[1] / distance

        return separation_force[0] * strength, separation_force[1] * strength

    def cohesion(self, boids, strength, distance):
        average_position = [0, 0]
        counter = 0
        for b in boids:
            if self.distance(b) < distance:
                average_position[0] += b.loc[0]
                average_position[1] += b.loc[1]
                counter += 1

        if counter:
            average_position = (average_position[0]/counter, average_position[1]/counter)

        cohesion_force = [average_position[0] - self.loc[0], average_position[1] - self.loc[1]]

        return cohesion_force[0] * strength/distance, cohesion_force[1] * strength/distance

    def alignment(self, boids, strength, distance):
        average_angle = 0
        counter = 0
        for b in boids:
            if self.distance(b) < distance:
                average_angle += b.angle
                counter += 1

        if counter:
            average_angle /= counter

        return [math.cos(average_angle) * MOVE_SIZE * strength, -math.sin(average_angle) * MOVE_SIZE * strength]

    def distance(self, boid):
        return math.sqrt((self.loc[0] - boid.loc[0])**2 + (self.loc[1] - boid.loc[1])**2)


class Flocking(object):

    master = Tkinter.Tk(className='Flocking')

    def __init__(self):
        self.boids = [Boid() for _ in range(BOIDS_SIZE[0] * BOIDS_SIZE[1])]

        for i in range(1, BOIDS_SIZE[0] + 1):
            for j in range(1, BOIDS_SIZE[1] + 1):
                self.boids[(i-1) * BOIDS_SIZE[0] + (j-1)].set(
                    loc=[i * 50, j * 50], angle=random.uniform(-math.pi, math.pi))

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
