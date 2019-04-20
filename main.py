from Assignment.sprites import *
import sys
import math
from os import *
from Assignment.priorityQueue import *
from Assignment.Weights import *

vec = pg.math.Vector2
all_nodes = []
for x in range(2000):
    for y in range(100):
        all_nodes.append([x, y])


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption(TITLE)
        pg.key.set_repeat(500, 100)
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock.tick(FPS)
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self, 5, 5)
        self.player2 = Player2(self, 8, 34)

        # using an arrow image to point the direction to the end node from goal node
        self.arrows = {}
        icon_dir = path.join(path.dirname(__file__), 'I:/YEAR 4/AI/Tutorials/week 2/icons')
        arrow_img = pg.image.load(path.join(icon_dir, 'arrowRight.png')).convert_alpha()
        arrow_img = pg.transform.scale(arrow_img, (50, 50))
        for dir in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            self.arrows[dir] = pg.transform.rotate(arrow_img, vec(dir).angle_to(vec(1, 0)))

    def draw_text(self, text, size, color, x, y, align="topleft"):
        font_name = pg.font.match_font('hack')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for x in range(10, 20):
            Wall(self, x, 40)

        for x in range(15, 20):
            Wall(self, x, 15)

        for y in range(10, 20):
            Wall(self, 10, y)

        for y in range(18, 20):
            Wall(self, 27, y)

        for y in range(15, 20):
            Wall(self, 15, y)

        for y in range(25, 20):
            Wall(self, 35, y)

        for y in range(20, 25):
            Wall(self, 20, y)

    def run(self):
        # game loop - set self.playing =False to end the game
        self.playing = True
        while self.playing:
            self.new()
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    # moving the node on y and x axis,
    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

    def in_bounds(self, node):
        return node.x >= 0 < WIDTH and 0 <= node.y < HEIGHT

    def passable(self, node):
        return node not in self.walls

    # For any node we need to know the other nodes connected to this one by an edge. We call these neighbors
    def neighbors(self, startnode):
        dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        result = []
        for dir in dirs:
            neighbor = [startnode[0] + dir[0], startnode[1] + dir[1]]
            if neighbor in all_nodes:
                result.append(neighbor)
        return result

    # drawing the grid
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, YELLOW, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, YELLOW, (0, y), (WIDTH, y))

    # drawing the details to the screen
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        # pg.display.set_caption("{:.2f}".format(self.clock.tick()))

    # eucledian distance, returns the straight line distance
    def heuristic(self, startnode, goalnode):
        temp = self.vectoint(startnode[0], startnode[1])
        temp2 = self.vectoint(goalnode[0], goalnode[1])

        dx = abs(temp[0] - temp2[0])
        dy = abs(temp[1] - temp2[1])
        return dx + dy * 10

    # convert node vectors(0,0) to int for calculations
    def vectoint(self, x, y):
        vec = [x, y]
        return int(vec[0]), int(vec[1])

    # after searching I need to build the path:It is the backwards path, so call reverse() at the end of reconstruct_path if you need it to be stored forwards
    def reconstruct_path(self, startnode, goalnode):
        current = goalnode
        l = 0
        while current != goalnode:
            direction = path[(current.x, current.y)]
            if direction.length_squared() == 1:
                l += 10
            else:
                l += 14
            img = self.arrows[self.vectoint(direction)]
            x = current.x * TILESIZE + TILESIZE / 2
            y = current.y * TILESIZE + TILESIZE / 2
            r = img.get_rect(center=(x, y))
            self.screen.blit(img, r)
            # find next in path
            current = current + path[self.vectoint(current)]
        self.draw_text('Cost is:{}'.format(0), 25, WHITE, WIDTH - 10, HEIGHT - 10, align="bottomright")
        self.draw_text('Path length:{}'.format(l), 25, WHITE, WIDTH - 10, HEIGHT - 45, align="bottomright")
        pg.display.flip()

    def Astar(self, startnode, goalnode):
        frontier = PriorityQueue()
        frontier.put(self.vectoint(startnode[0], startnode[1]), 0)
        initialstart = {}
        currentcost = {}
        initialstart[self.vectoint(startnode[0], startnode[1])] = None
        currentcost[self.vectoint(startnode[0], startnode[1])] = 0

        while not frontier.empty():
            currentnode = frontier.get()
            if currentnode == goalnode:
                break
            for nextnode in self.neighbors(self.vectoint(currentnode[0], currentnode[1])):
                nextnode = self.vectoint(nextnode[0], nextnode[1])
                weights = Weights()
                nextnodecost = currentcost[currentnode] + weights.cost(currentnode, nextnode)
                if nextnode not in currentcost or nextnodecost < currentcost[nextnode]:
                    currentcost[nextnode] = nextnodecost
                    priority = nextnodecost + self.heuristic(goalnode, self.vectoint(nextnode[0], nextnode[1]))
                    frontier.put(nextnode, priority)
                    initialstart[nextnode] = vec(currentnode) - vec(nextnode)
                    print('path direction', initialstart)
                    print('new cost is:', currentcost)
                    return initialstart, currentcost

    def getSpriteByPosition(position, group):
        try:
            return group.sprites()[position]
        except IndexError:
            pass

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = vec(pg.mouse.get_pos()) // TILESIZE
                print(pos)
                if event.button == 1:
                    self.player = Player(self, pos.x, pos.y)
                    self.player.update()
                    self.all_sprites.draw(self.screen)
                    # self.clock.tick(FPS)
                    pg.display.update()
                if event.button == 2:
                    self.player2 = Player2(self, pos[0], pos[1])
                    self.player2.update()
                    self.all_sprites.draw(self.screen)
                    self.clock.tick(FPS)
                    pg.display.update()
                self.Astar(self.vectoint(self.player), self.vectoint(self.player2))

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass  # create the game object


g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
