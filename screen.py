import pygame as py
import pygame.gfxdraw
import sys, random, math

py.init()

alpha = 0

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

ConnectionRange = 160

ScreenSize = (1200, 600)

clock = py.time.Clock()
screen = py.display.set_mode(ScreenSize)


class Dot():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speedX = random.randint(-10, 10) * 0.1
        self.speedY = random.randint(-10, 10) * 0.1
        self.radius = random.randint(1, 5)

    def update(self):
        self.x += self.speedX
        self.y += self.speedY

    def isOutofScreen(self):
        if self.x < 0 or self.x > ScreenSize[0] or self.y < 0 or self.y > ScreenSize[1]:
            return True
        else:
            return False

    def isInRange(self, other):
        dist = math.hypot((self.x - other.x), (self.y - other.y))
        if dist < ConnectionRange:
            return True
        else:
            return False

    def getDistance(self, other):
        dist = math.hypot((self.x - other.x), (self.y - other.y))
        return dist

    def eatOther(self, other):
        self.radius += 0.01
        other.radius -= 0.01


dots = list()

while True:
    for key in py.event.get():
        if key.type == py.QUIT:
            py.quit()
            sys.exit()
    screen.fill(BLACK)

    clock.tick(60)

    while len(dots) < 100:
        dots.append(Dot(random.randint(0, ScreenSize[0]), random.randint(0, ScreenSize[1])))

    # update every dot in the list
    for dot in dots:
        dot.update()
        if dot.isOutofScreen():
            dots.remove(dot)





    # move away the dots in the range of the mouse
    mousePos = py.math.Vector2()
    mousePos.x, mousePos.y = py.mouse.get_pos()
    for dot in dots:
        if dot.isInRange(mousePos):
            angle = math.atan2(dot.y - mousePos[1], dot.x - mousePos[0])
            offset = ConnectionRange - dot.getDistance(mousePos)
            dot.x += offset * math.cos(angle)
            dot.y += offset * math.sin(angle)

    # drawing the connections between them if in the range
    for dot in dots:
        for other in dots:
            if dot.isInRange(other) and dot is not other:
                alpha = 255 - (dot.getDistance(other) / ConnectionRange * 255)
                pygame.gfxdraw.line(screen, int(dot.x), int(dot.y), int(other.x), int(other.y), (255, 0, 0, alpha))
                # pygame.draw.aaline(screen, (255, 0, 0, alpha), (int(dot.x), int(dot.y)), (int(other.x), int(other.y)))

    # drawing the dots on the screen
    for dot in dots:
        py.gfxdraw.aacircle(screen, int(dot.x), int(dot.y), int(dot.radius), BLUE)
        py.gfxdraw.filled_circle(screen, int(dot.x), int(dot.y), int(dot.radius), BLUE)
    py.display.update()
