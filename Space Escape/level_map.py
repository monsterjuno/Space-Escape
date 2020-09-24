import pygame

pygame.init()  # initiates pygame

pygame.display.set_caption('STEALTH GAME')

WINDOW_SIZE = (1000, 600)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate the window

display = pygame.Surface((1000, 600))  # used as the surface for rendering,
display_text = pygame.Surface((1000, 600))  # used as the surface for rendering,

# IMAGES#
grass_img = pygame.image.load('grass.png')
end_img = pygame.image.load('end.png')
wall_img = pygame.image.load('wall.png')
level_bg = pygame.image.load('scene1.jpg')


pygame.display.set_icon(wall_img)


class portal_obj():
    def __init__(self, loc):
        self.loc = loc

    def render(self, portal_surf, scroll):
        portal_surf.blit(end_img, (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))

    def get_rect(self):
        return pygame.Rect(self.loc[0], self.loc[1], 100, 100)

    def collision_test(self, rect):
        portal_rect = self.get_rect()
        return portal_rect.colliderect(rect)


def load_level(path):  # to read the level dat file
    f = open('level_map.txt')
    data = f.read()
    f.close()
    data = data.split('\n')  # splits the text file into lines that are y values
    level_map = []
    for row in data:
        level_map.append(list(row))
    return level_map


level_map = load_level('level_map')

scroll = [0,0]

running = True
while running:
    display.blit(level_bg, (0, 0))
    player_rect = pygame.Rect(100,100,43,70)

    scroll[0] += (player_rect.x - scroll[0] - 519) / 10  # center of the screen is 500,300 ie 500 + 19 that is the center of the player
    scroll[1] += (player_rect.y - scroll[1] - 332) / 10  # 300 + 32 that is the center of the player

    # MAP LOADING#

    tile_rects = []
    y = 0
    for layer in level_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(grass_img, (x * 100 - scroll[0], y * 100 - scroll[1]))
            if tile == '0':
                display.blit(wall_img, (x * 100 - scroll[0], y * 100 - scroll[1]))
            if tile == 'X':
                display.blit(end_img, (x * 100 - scroll[0], y * 100 - scroll[1]))
            if tile != 'X':
                tile_rects.append(pygame.Rect(x * 100, y * 100, 100, 100))
            x += 1
        y += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
