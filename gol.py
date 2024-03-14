import pygame
import time
from random import randrange


class gol():
    """docstring for ClassName"""

    def __init__(self):

        self.start_time = time.time()

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        self.width = 6
        self.height = 6
        self.margin = 1

        self.sizex = 255
        self.sizey = 75

        self.frame = 1
        self.play = 1

        self.grid = [[0 for x in range(self.sizex)] for y in range(self.sizey)]

        for x in range(int(self.sizex * self.sizey / 3)):
            self.grid[randrange(self.sizey)][randrange(self.sizex)] = 1

        pygame.init()
        self.myfont = pygame.font.SysFont("Courier New", 14)

        size = [100 + (self.height + self.margin) * self.sizex + self.margin,
                (self.height + self.margin) * self.sizey + self.margin]
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Game of Life")
        self.done = False
        self.clock = pygame.time.Clock()
        self.time = 0
        self.main()

    # Main loop
    def main(self):
        while not self.done:

            self.screen.fill(self.BLACK)
            pygame.draw.rect(self.screen, self.WHITE,[2, 2, 96, (self.height + self.margin) * self.sizey + self.margin - 4])
            if self.play == 0:
                pygame.draw.polygon(self.screen, self.GREEN, ((40, (self.height + self.margin) * self.sizey - 60), (40, (self.height + self.margin) * self.sizey - 40), (60, (self.height + self.margin) * self.sizey - 50)))
            else:
                pygame.draw.rect(self.screen, self.RED, [
                                 40, ((self.height + self.margin) * self.sizey - 58), 6, 15])
                pygame.draw.rect(self.screen, self.RED, [
                                 50, ((self.height + self.margin) * self.sizey - 58), 6, 15])

            fps = self.myfont.render(
                "FPS:" + str(self.frame / (time.time() - self.start_time)), 1, self.BLACK)
            self.screen.blit(
                fps, (10, (self.height + self.margin) * self.sizey - 35))
            frames = self.myfont.render(
                "Frame:" + str(self.frame), 1, self.BLACK)

            # Reset after x amount of frames
            if self.frame > 500:
                self.frame = 0
                for x in range(int(self.sizex * self.sizey / 3)):
                    self.grid[randrange(self.sizey)][randrange(self.sizex)] = 1

            self.screen.blit(
                frames, (10, (self.height + self.margin) * self.sizey - 20))
            for row in range(self.sizey):
                for column in range(self.sizex):
                    color = self.WHITE
                    if self.grid[row][column] == 1:
                        color = self.RED
                    pygame.draw.rect(
                        self.screen, color, [(self.margin + self.width) * column + self.margin + 100,
                                             (self.margin + self.height) * row + self.margin, self.width, self.height])
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pos[0] > 100 and self.play == 0:
                        x, y = ((pos[0] - 100) // (self.width + self.margin)
                                ), (pos[1] // (self.height + self.margin))
                        self.grid[y][x] = 1
                    elif pos[0] > 38 and pos[1] > (self.height + self.margin) * self.sizey - 62 and pos[0] < 62 and pos[1] < (self.height + self.margin) * self.sizey - 40:
                        self.play = not self.play

            dt = self.clock.tick()
            self.time += dt
            if self.time > 1 and self.play == 1:
                self.frame += 1
                self.grid = self.rules()
                self.time = 0
            # if self.frame==100:
            #   self.done=True
        pygame.quit()

    # Check neighbours in grid
    def neighbours(self, y, x):
        z = 0
        ad = [[-1, -1], [0, -1], [1, -1], [-1, 0],
              [1, 0], [-1, 1], [0, 1], [1, 1]]
        for s in ad:
            try:
                if self.grid[s[1] + y][s[0] + x] == 1:
                    z += 1
            except IndexError:
                pass
        return z

    # Apply rules on grid
    def rules(self):
        newgrid = [x[:] for x in self.grid]
        for y in range(0, len(self.grid)):
            for x in range(0, len(self.grid[y])):
                z = self.neighbours(y, x)
                if self.grid[y][x] == 1 and z <= 1 or z >= 4:
                    newgrid[y][x] = 0
                elif self.grid[y][x] == 0 and z == 3:
                    newgrid[y][x] = 1
        return newgrid


if __name__ == '__main__':
    run = gol()
