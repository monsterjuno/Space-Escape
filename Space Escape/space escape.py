import pygame, sys
import time

clock = pygame.time.Clock()
game_timer = 7500


from pygame.locals import *
pygame.init() 						# initiates pygame

pygame.display.set_caption('SPACE ESCAPE')

WINDOW_SIZE = (1000,600)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

display = pygame.Surface((1000,600)) # used as the surface for rendering,
display_text = pygame.Surface((1000,600)) # used as the surface for rendering,


#FONTS
font = pygame.font.Font("PaladinsGradient-R6VW.otf", 40)		# Font for the text IN COUNTDOWN
font1 = pygame.font.Font("PaladinsStraight-2a7v.otf", 200)		# Font for the text IN COUNTDOWN
font_game = pygame.font.Font("Xolonium-nGqP.otf", 25)		# Font for the text IN GAME
font_menu = pygame.font.Font("NebulousRegular-54aV.ttf", 50)
PINK = (255, 51, 128)
WHITE = (255, 255, 255)


#JUMP
moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0

#IMAGES#
grass_img = pygame.image.load('grass.png')
dirt_img = pygame.image.load('dirt.png')
end_img = pygame.image.load('end.png')

level_bg = pygame.image.load('scene1.jpg')
main_bg = pygame.image.load('scene2.jpg')
win_bg = pygame.image.load('scene3.jpg')


#PLAYER IMAGES
player_imgR = pygame.image.load('player_moveR.png')
player_imgL = pygame.image.load('player_moveL.png')
player_img = player_imgR

#portal
portal = []

#SCROLL
scroll = [0,0]

#counter
counter = 0
class portal_obj():
	def __init__ (self, loc):
		self.loc = loc

	def render(self, portal_surf, scroll):
		portal_surf.blit(end_img, (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))

	def get_rect(self):
		return pygame.Rect(self.loc[0], self.loc[1], 100, 100)

	def collision_test(self, rect):
		portal_rect = self.get_rect()
		return portal_rect.colliderect(rect)


def main_menu():
	running = True
	while running:
		screen.blit(main_bg,(0,0))

		print_font = font_menu.render('PRESS ENTER TO START', 1, PINK) 
		screen.blit(print_font,(380,275))

		print_font1 = font_menu.render('PRESS Q TO QUIT', 1, PINK) 
		screen.blit(print_font1,(525,340))

		for event in pygame.event.get(): # event loop
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == KEYDOWN:
				if event.key == K_RETURN:
					game_timer = 7500
					main_loop()
					break
				if event.key == K_q:
					pygame.quit()
					sys.exit()

		pygame.display.update()

def win_menu():
    global game_timer
    running = True
    while running:
        screen.blit(win_bg,(0,0))
        print_font = font_menu.render('PRESS ENTER TO REPLAY', 1, PINK)
        screen.blit(print_font,(370,275))

        print_font1 = font_menu.render('PRESS Q TO QUIT', 1, PINK)
        screen.blit(print_font1,(525,340))


        for event in pygame.event.get(): # event loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    game_timer= 7500
                    main_loop()
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def end_game():
    global game_timer
    running = True
    while running:
        screen.blit(main_bg,(0,0))
        print_font = font_menu.render('PRESS ENTER TO RESTART', 1, PINK)
        screen.blit(print_font,(370,275))
        print_font1 = font_menu.render('PRESS Q TO QUIT', 1, PINK)
        screen.blit(print_font1,(525,340))
        for event in pygame.event.get(): # event loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    game_timer= 7500
                    main_loop()
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def load_level(path):				#to read the level dat file
	f = open(path + '.txt', 'r')
	data = f.read()
	f.close()
	data = data.split('\n')		#splits the text file into lines that are y values
	level_map = []
	for row in data:
		level_map.append(list(row))
	return level_map

level_map = load_level('level_map')

def collision_test(rect,tiles):
    global game_timer
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

def count_timer(timer):
	countdown = True
	while countdown == True:
		if timer != 0:
			screen.blit(level_bg,(0,0))

			print_font = font.render('SPACE ESCAPE STARTS IN', 1, PINK) 
			screen.blit(print_font,(100,200))

			print_font1 = font1.render(str(timer), 1, PINK) 
			screen.blit(print_font1,(400,250))

			pygame.display.update()
			timer = timer - 1
			time.sleep(1)
		else:
			print('You have run out of time')
			countdown == False
			break

for i in range(1):
	portal.append(portal_obj((2900,1500)))

def  main_loop():
    global moving_right,moving_left,vertical_momentum ,air_timer ,player_img,game_timer,counter
    # game loop
    running = False
    count_timer(3)
    running = True
    player_rect = pygame.Rect(100,100,43,70)
    while running: 
        display.blit(level_bg,(0,0))
        scroll[0] += (player_rect.x-scroll[0]-519)/10			#center of the screen is 500,300 ie 500 + 19 that is the center of the player
        scroll[1] += (player_rect.y-scroll[1]-332)/10			#300 + 32 that is the center of the palyer

        # MAP LOADING#

        tile_rects = []
        y = 0
        for layer in level_map:
            x = 0
            for tile in layer:
                if tile == '1':
                    display.blit(grass_img,(x*100-scroll[0],y*100-scroll[1]))
                if tile == '0':            	
                    display.blit(dirt_img,(x*100-scroll[0],y*100-scroll[1]))
                if tile == 'X':
                	display.blit(end_img,(x*100-scroll[0],y*100-scroll[1]))					;#tile_rects.append(pygame.Rect(x*10,y*100,100,100));portal_rect=pygame.Rect(x*10,y*100,100,100)
                if tile != '2' and tile != 'X':
                    tile_rects.append(pygame.Rect(x*100,y*100,100,100))
                x += 1
            y += 1

        player_movement = [0,0]					#player will start from here
        if moving_right == True:
            player_movement[0] += 11
        if moving_left == True:
            player_movement[0] -= 11
        player_movement[1] += vertical_momentum
        vertical_momentum += 1
        if vertical_momentum > 15:
            vertical_momentum = 15

        for p in portal:
        	p.render(display,scroll)
        	if p.collision_test(player_rect):
        		game_timer = 0
        		counter = 1

        #GAME TIMER #
        game_timer -= 1
        if game_timer <= 0:
        	if counter == 1:
        		running = False
        		win_menu()
        	else:
        		running = False
        		end_game()
        else:
        	print_font = font_game.render("YOU HAVE ONLY " + str(game_timer //25) +" SECONDS LEFT                                          Q TO QUIT", 1, WHITE)
        	pygame.display.update()


        player_rect,collisions = move(player_rect,player_movement,tile_rects)

        if collisions['bottom'] == True or collisions['top'] == True:
            air_timer = 0
            vertical_momentum = 0
        else:
            air_timer += 1

        display.blit(player_img,(player_rect.x-scroll[0],player_rect.y-scroll[1]))
        done = False



        #MAIN KEY LOOP#

        for event in pygame.event.get(): # event loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_RIGHT or event.key == K_d:
                    moving_right = True
                    player_img = player_imgR
                if event.key == K_LEFT or event.key == K_a:
                    moving_left = True
                    player_img = player_imgL
                if event.key == K_UP or event.key == K_w:
                    if air_timer < 6:
                        vertical_momentum = -25
                if event.key == K_q:
                	running = False
                	game_timer = 7500
                	main_menu()
                        
            if event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_d:
                    moving_right = False
                if event.key == K_LEFT or event.key == K_a:
                    moving_left = False
            

        screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
        screen.blit(print_font,(10,10))
        pygame.display.update()
        clock.tick(100)


main_menu()
