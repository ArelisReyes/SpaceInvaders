import pygame
import pygame_menu

pygame.init()
pantalla = pygame.display.set_mode((600, 400))

class Game:
    screen = None
    aliens = []
    rockets = []
    lost = False
    win = False

    def __init__(self, width, height, dificultad):

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.fondo = pygame.image.load("Recursos/fondo.png")
        self.dificultad = dificultad
        done = False

        pygame.mixer.music.load("Recursos/song.wav")
        pygame.mixer.music.play(-1)

        hero = Hero(self, width / 2, height - 20)
        generator = Generator(self, self.dificultad)
        rocket = None

        while not done:
            if len(self.aliens) == 0:
                self.win = True
                self.displayText("VICTORY ACHIEVED")

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                hero.x -= 2 if hero.x > 20 else 0
            elif pressed[pygame.K_RIGHT]:
                hero.x += 2 if hero.x < width - 20 else 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and len(self.rockets)<4:
                    self.rockets.append(Rocket(self, hero.x, hero.y))

            pygame.display.flip()
            self.clock.tick(60)
            # self.screen.fill((0, 0, 0))
            self.screen.blit(self.fondo, (0, 0))

            for alien in self.aliens:
                alien.draw()
                alien.checkCollision(self)
                if (alien.y > height):
                    self.lost = True
                    self.displayText("YOU DIED")

            for rocket in self.rockets:
                if not self.win: rocket.draw()
                if rocket.y <= 0:
                    self.rockets.remove(rocket)

            if not self.lost: hero.draw()

    def displayText(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 50)
        textsurface = font.render(text, False, (0, 0, 0))
        self.screen.blit(textsurface, (150, 100))


class Alien:
    def __init__(self, game, x, y, velocity):
        self.x = x
        self.game = game
        self.y = y
        self.size = 30
        self.image = pygame.image.load("Recursos/alien.png")
        self.velocity = velocity

    def draw(self):
        # pygame.draw.rect(self.game.screen,
        # (81, 43, 88),
        # pygame.Rect(self.x, self.y, self.size, self.size))
        self.game.screen.blit(self.image, (self.x, self.y))
        self.y += self.velocity

    def checkCollision(self, game):
        for rocket in game.rockets:
            if (rocket.x < self.x + self.size and
                    rocket.x > self.x - self.size and
                    rocket.y < self.y + self.size and
                    rocket.y > self.y - self.size):
                game.rockets.remove(rocket)
                game.aliens.remove(self)


class Hero:
    def __init__(self, game, x, y):
        self.x = x
        self.game = game
        self.y = y
        self.image = pygame.image.load("Recursos/nave2.png")

    def draw(self):
        # pygame.draw.rect(self.game.screen,(210, 250, 251),pygame.Rect(self.x, self.y, 8, 5))
        self.game.screen.blit(self.image, (self.x, self.y))


class Generator:
    def __init__(self, game, velocity):
        margin = 30
        width = 50
        for x in range(margin, game.width - margin, width):
            for y in range(margin, int(game.height / 2), width):
                game.aliens.append(Alien(game, x, y, velocity))


class Rocket:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game

    def draw(self):
        pygame.draw.rect(self.game.screen,
                         (254, 52, 110),
                         pygame.Rect(self.x, self.y, 2, 4))
        self.y -= 2


def start_easy():
    Game(600,400,0.1)

def start_medium():
    Game(600, 400, 0.3)

def start_hard():
    Game(600,400,0.5)


menu = pygame_menu.Menu(height=400,
    theme=pygame_menu.themes.THEME_BLUE,
    title='Welcome',
    width=600)



menu.add.button('Easy', start_easy)
menu.add.button('Medium',start_medium)
menu.add.button('Hard', start_hard)
menu.add.button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    menu.mainloop(pantalla)