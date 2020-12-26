import pygame

from engine import GameEngine
from assets import *

pygame.font.init()

class App:
    
    """Create a single-window app with multiple scenes having multiple objects."""
    
    clock = pygame.time.Clock()
    running = True
    screen = None
    scene = None

    def __init__(self, size=(700, 700)):

        """Initialize pygame and the application."""

        pygame.init()

        self.FPS = 120
        self.flags = 0
        self.rect = pygame.Rect(0, 0, *size)

        App.screen = pygame.display.set_mode(self.rect.size, self.flags)
        App.scene = MainMenu()

    def run(self):

        """Run the main event loop."""

        while App.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    App.running = False

                App.scene.do_event(event)

            App.scene.draw()
            App.clock.tick(self.FPS)

        pygame.quit()

class Scene:

    """Create a new scene."""

    def __init__(self, caption="Space Invaders"):
        
        self.bg = pygame.transform.scale(BACKGROUND, App.screen.get_size())
        self.nodes = []

        self.y1 = 0
        self.y2 = - App.screen.get_height()

        App.scene = self
        pygame.display.set_caption(caption)

    def draw(self):

        """Draw all objects in the scene."""

        App.screen.blit(self.bg, (0, self.y1))
        App.screen.blit(self.bg, (0, self.y2))

        self.y1 += 1
        self.y2 += 1

        if self.y1 > App.screen.get_height(): self.y1 = -App.screen.get_height()
        if self.y2 > App.screen.get_height(): self.y2 = -App.screen.get_height()

        for node in self.nodes: 
            node.draw()
        
        pygame.display.flip()

class MainMenu(Scene):

    def __init__(self, caption=""):

        super().__init__(caption)

        self.nodes.append(Node(LOGO, size=(450, 175), pos=(App.screen.get_width()/2, 180)))
        self.nodes.append(Text("Play", 60, (255,255,255), pos=(App.screen.get_width()/2, 350)))
        self.nodes.append(Text("Settings", 60, (255,255,255), pos=(App.screen.get_width()/2, 415)))
        self.nodes.append(Text("Exit", 60, (255,255,255), pos=(App.screen.get_width()/2, 480)))

        self.selected = 0

    def do_event(self, e):

        """Handle the events of the scene."""
        
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP or e.key == pygame.K_w:
                if self.selected == 0: self.selected = len(self.options) - 1
                else: self.selected -= 1

            elif e.key == pygame.K_DOWN or e.key == pygame.K_s:
                if len(self.options) - 1 == self.selected: self.selected = 0
                else: self.selected += 1

            # elif e.key == pygame.K_RETURN and self.selected == 0: App.scene = Game()
            # elif e.key == pygame.K_RETURN and self.selected == 1: App.scene = Settings()
            elif e.key == pygame.K_RETURN and self.selected == 2: App.running = False

class Node:

    """Create a node object with automatic position and inherited size."""

    def __init__(self, img=None, size=(0,0), pos=(0,0)):

        self.img = img
        self.size = size
        self.pos = (pos[0] - self.size[0]/2, pos[1] - self.size[1]/2)

        if img != None and img.get_size() != size:
            self.img = pygame.transform.scale(self.img, self.size)

    def draw(self):

        """Draw object in the scene."""

        App.screen.blit(self.img, self.pos)

class Text(Node):

    """Create a text surface image."""

    def __init__(self, text, fsize, fcolor, fname="comicsans", *args, **kwargs):
        
        super().__init__(*args, **kwargs)

        self.text = text
        self.fsize = fsize
        self.fname = fname
        self.fcolor = fcolor
        
        self.font = pygame.font.SysFont(self.fname, self.fsize)    
        self.img = self.font.render(self.text, True, self.fcolor)

        self.size = self.img.get_size()
        self.pos = (self.pos[0] - self.size[0]/2, self.pos[1] - self.size[1]/2)

    def change_font(self, fname, fsize):

        """Change the font and render new surface."""

        self.fsize = fsize
        self.fname = fname
        self.font = pygame.font.SysFont(self.fname, self.fsize)
        self.img = self.font.render(self.text, True, self.fcolor)

if __name__ == "__main__":
    App().run()