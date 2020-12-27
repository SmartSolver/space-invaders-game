import yaml
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
        self.nodes.append(Text("Play",     60, (230, 230,   0), pos=(App.screen.get_width()/2, 350)))
        self.nodes.append(Text("Settings", 60, (255, 255, 255), pos=(App.screen.get_width()/2, 415)))
        self.nodes.append(Text("Exit",     60, (255, 255, 255), pos=(App.screen.get_width()/2, 480)))

        self._selected = 1

    @property   
    def selected(self):
        
        return self._selected

    @selected.setter
    def selected(self, val):
        
        self.nodes[self._selected].change_color((255, 255, 255))
        self.nodes[val].change_color((230, 230, 0))

        self._selected = val

    def do_event(self, e):

        """Handle the events of the scene."""
        
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP or e.key == pygame.K_w:
                if self.selected == 1: self.selected = 3
                else: self.selected -= 1

            elif e.key == pygame.K_DOWN or e.key == pygame.K_s:
                if self.selected == 3: self.selected = 1
                else: self.selected += 1

            # elif e.key == pygame.K_RETURN and self.selected == 1: App.scene = Game()
            elif e.key == pygame.K_RETURN and self.selected == 2: App.scene = Settings()
            elif e.key == pygame.K_RETURN and self.selected == 3: App.running = False

class Settings(Scene):

    def __init__(self, caption=""):

        super().__init__(caption)

        self._config = yaml.safe_load(open("config.yaml"))

        self.nodes.append(Text("Settings", 70, (255, 255, 255), pos=(App.screen.get_width()/2, 200)))  
        
        self.nodes.append(Text(f"Player speed: {self.config['settings']['player_velocity']}", 50, (230, 230,   0), pos=(App.screen.get_width()/2, 300)))
        self.nodes.append(Text(f"Enemy speed: {self.config['settings']['enemy_velocity']}",   50, (255, 255, 255), pos=(App.screen.get_width()/2, 360)))
        self.nodes.append(Text(f"Wave length: {self.config['settings']['wave_length']}",      50, (255, 255, 255), pos=(App.screen.get_width()/2, 420)))
        self.nodes.append(Text(f"Player ship: {self.config['settings']['player_color']}",     50, (255, 255, 255), pos=(App.screen.get_width()/2, 480)))

        self.nodes.append(Node(YELLOW_SPACE_SHIP, size=(100,100), pos=(App.screen.get_width()/2, 550)))

        self.nodes.append(Text("[ENTER] Save", 40, (255, 255, 255), pos=(120, App.screen.get_height()-40)))
        self.nodes.append(Text("[ESC] Exit",   40, (255, 255, 255), pos=(App.screen.get_width()-100, App.screen.get_height()-40)))

        self._selected = 1

    @property   
    def selected(self):
        
        return self._selected

    @selected.setter
    def selected(self, val):
        
        self.nodes[self._selected].change_color((255, 255, 255))
        self.nodes[val].change_color((230, 230, 0))
        self._selected = val

    @property   
    def config(self):
        
        return self._config

    @config.setter
    def config(self, val):
        
        print("setter", val)
        self.nodes[self.selected].change_text(f"{val}")
        self._config = val

    def do_event(self, e):

        """Handle the events of the scene."""

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP or e.key == pygame.K_w:
                if self.selected == 1: self.selected = 4
                else: self.selected -= 1

            elif e.key == pygame.K_DOWN or e.key == pygame.K_s:
                if self.selected == 4: self.selected = 1
                else: self.selected += 1

            elif e.key == pygame.K_LEFT or e.key == pygame.K_a:
                if self.selected == 1: self.config["settings"]["player_velocity"] -= 1
                if self.selected == 2: self.config["settings"]["enemy_velocity"] -= 1
                if self.selected == 3: self.config["settings"]["wave_length"] -= 5

            elif e.key == pygame.K_RIGHT or e.key == pygame.K_d:
                if self.selected == 1: self.config["settings"]["player_velocity"] += 1
                if self.selected == 2: self.config["settings"]["enemy_velocity"] += 1
                if self.selected == 3: self.config["settings"]["wave_length"] += 5

            elif e.key == pygame.K_RETURN: 
                yaml.dump(self.config, open("config.yaml", "w"))
                App.scene = MainMenu()

            elif e.key == pygame.K_ESCAPE: App.scene = MainMenu()

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

    def change_text(self, text):

        """Change the text of the node"""

        self.text = text
        self.img = self.font.render(self.text, True, self.fcolor)
        self.size = self.img.get_size()
        self.pos = (self.pos[0] - self.size[0]/2, self.pos[1] - self.size[1]/2)

    def change_color(self, color):

        """Change the color of the text"""
 
        self.fcolor = color
        self.img = self.font.render(self.text, True, self.fcolor)

if __name__ == "__main__":
    App().run()