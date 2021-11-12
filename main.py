import pygame
from pygame.locals import *
from random import *

# game setup
pygame.init()

clock = pygame.time.Clock()
fps = 60

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# screen ratio 16:9
# art pixel to screen pixel 1:8

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Monarch')


# define font
score_font = pygame.font.Font('fonts/PixelPowerline-11Mg.ttf', 100)
heart_font = pygame.font.Font('fonts/PixelPowerline-11Mg.ttf', 40)
font = 'fonts/PixelPowerline-11Mg.ttf'

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 150)

# load images
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')

# define game variables
run = False
menu = True
game_over = False
score = 0
last_score = 0
hearts = 3
ground_height = SCREEN_HEIGHT - 128
ground_scroll = 0
initial_scroll_speed = 4
scroll_speed = initial_scroll_speed
total_distance = 0
flying = True
last_flower = 0
flower_frequency = SCREEN_WIDTH // 3 # flower every third of the screen
bee_probability = 0.20
bird_probability = 0
game_over_screen = False




# draws text to the screen
def draw_text(text, font, text_size, text_col):
	new_font = pygame.font.Font(font, text_size)
	new_text = new_font.render(text, 0, text_col)

	return new_text


# This class represents the Butterfly sprite -- what the player controls
class Butterfly(pygame.sprite.Sprite):

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.index = 0
		self.counter = 0 
		for num in range(1, 8):
			img = pygame.image.load(f'img/monarch{num}.png')
			self.images.append(img)
		self.image = self.images[self.index]
		self.rect = pygame.Rect(x, y, 72, 80)
		self.rect.center = [x, y]
		self.gravity = 1
		self.dx = 5
		self.dy = 8
		self.collided = False
		self.knockback_duration = (0.30 * fps)
		self.knockback_counter = 0

	def update(self):

		global scroll_speed
				
		if not game_over and not menu:

			# when in the air, gravity applies
			if self.rect.bottom < ground_height:
				self.rect.y += self.gravity

			else:
				# move backwards when touching the ground 
				self.rect.x -= scroll_speed

			# movement
			keys = pygame.key.get_pressed()

			# moves backwards
			if keys[pygame.K_LEFT]:
			    self.rect.x -= self.dx

			# can't move off to the right of the screen
			if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH and not self.collided:
			    self.rect.x += self.dx

			# can't move above screen
			if keys[pygame.K_UP] and self.rect.top > 0:
			    self.rect.y -= self.dy

			# can't move below ground
			if keys[pygame.K_DOWN] and self.rect.bottom < ground_height:
				self.rect.y += self.dy
			
			# handle the knockback from collisions
			if self.collided and self.knockback_counter < self.knockback_duration:
				self.rect.x -= (self.dx + (self.knockback_duration - self.knockback_counter) + scroll_speed)
				self.knockback_counter += 1

			if self.knockback_counter >= self.knockback_duration:
				self.collided = False
				self.knockback_counter = 0

			# handle the animation
			self.counter += 1 
			anim_cooldown = 2

			if self.counter > anim_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images):
					self.index = 0

			self.image = self.images[self.index]



# This class represents a Bee sprite
class Bee(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/bee.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.dx = 2
		self.initial_y = self.rect.y
		self.dy = 2
		self.amplitude = randint(10, 151)
		self.time_spawned = pygame.time.get_ticks()
		self.time_until_move = randint(0,1000) # 0 to 1 second until bee starts to move
		self.moving = False

	def update(self):
		if not game_over:

			if not self.moving:
				time_now = pygame.time.get_ticks()
				if (time_now - self.time_spawned) >= self.time_until_move:
					self.moving = True

			self.rect.x -= scroll_speed

			if self.moving:

				# move the bee vertically based on a zig-zag pattern
				if (self.initial_y - self.rect.y >= self.amplitude) or (self.rect.y - self.initial_y >= self.amplitude) or (self.rect.bottom >= ground_height):
					self.dy *= -1 # reverse the direction of movement at the apex

				self.rect.x -=  self.dx
				self.rect.y -= self.dy

			# remove sprite after exits the screen
			if (self.rect.right < 0):
				self.kill()



# This class represents a Bird which spawns above the screen and moves toward the butterfly sprite
class Bird(pygame.sprite.Sprite):
	def __init__(self, x, y, target):
		pygame.sprite.Sprite.__init__(self)

		self.images = []
		self.index = 0
		self.counter = 0 
		for num in range(1, 9):
			img = pygame.image.load(f'img/bird{num}.png')
			self.images.append(img)
		self.image = self.images[self.index]

		self.rect = pygame.Rect(0, 32, 128, 64)
		self.rect.center = [x, y]
		self.initial_x = x
		self.initial_y = y
		self.dx = 0
		self.dy = 0
		self.speed_ratio = 50
		self.target = target
		self.collided = False
		self.passed_butterfly = False

	def update(self):

		global hearts

		if not game_over:

			# pathfind towards target 
			if (not self.passed_butterfly and self.rect.y >= self.target.rect.bottom and self.rect.x <= self.target.rect.left) or self.rect.bottom >= ground_height:
				self.passed_butterfly = True

			if self.passed_butterfly:
				self.dx = 10
				self.dy = -5
			else:
				self.dx = (self.initial_x - self.target.rect.x) // self.speed_ratio
				self.dy = (self.target.rect.y - self.initial_y) // self.speed_ratio

			self.rect.x -= self.dx
			self.rect.y += self.dy

			
			if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
				self.kill()


			# handle the animation
			self.counter += 1 
			anim_cooldown = 2

			if self.counter > anim_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images):
					self.index = 0

			self.image = self.images[self.index]


# TODO: Add visual representation of hearts
# TODO: Add visual representation when lose heart from bird
# TODO: Add another bird type which grabs you and takes you off the screen -- automatically lose



# TODO: Use OOP to make flower superclass and all flower types subclass of Flower

"""
class Flower(pygame.sprite.Sprite):
	def __init__(self, x, y):
		
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(rect)
		self.flower_type = flower_type
		self.image = pygame.image.load(f'img/{self.flower_type}_unpollinated.png')
		self.rect.center = [x, y]
		self.point_value = pt_value
		self.pollinated = False
		self.pollinte_index = 0
		self.counter = 0
		self.pollinate_cooldown = 3

		self.pollinated_images = []
		for num in range(1, 6):
			img = pygame.image.load(f'img/{self.flower_type}_pollinated{num}.png')
			self.pollinated_images.append(img)
		
"""
	


class Poppy(pygame.sprite.Sprite):

	def __init__(self, x, y):
		#Flower.__init__(self, x, y, 'poppy', 5, (x + 32, y + 24, 24, 24))
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/poppy_unpollinated.png')
		self.rect = pygame.Rect(x + 32, y + 24, 24, 24) # rect refers to the center of the flower 
		self.rect.center = [x, y]
		self.point_value = 5
		self.pollinated = False
		self.pollinate_index = 0
		self.counter = 0
		self.pollinate_cooldown = 3
		self.score_text_duration = int(0.5 * fps)
		self.score_text_duration_counter = 0
		self.score_text_y_offset = 0
		self.text_color_change_duration = int(0.1 * fps)
		self.text_color_change_duration_counter = 0
		self.text_color = (0,0,255)

		self.pollinated_images = []
		for num in range(1, 6):
			img = pygame.image.load(f'img/poppy_pollinated{num}.png')
			self.pollinated_images.append(img)
		
	def update(self):
		if not game_over:
			self.rect.x -= scroll_speed

			# the time it takes to pollinate a flower decreases as scroll_speed increases 
			if (scroll_speed < 12): # based off linear function
				self.pollinate_cooldown = -(scroll_speed // 2) + initial_scroll_speed + 1
			else:
				self.pollinate_cooldown = 0


			# remove flower when exits the screen
			if self.rect.right < -75:
				self.kill()

			# handle the visual representation of the score increase
			if self.pollinated and self.score_text_duration_counter < self.score_text_duration:
				self.score_text_duration_counter += 1
				if self.text_color_change_duration_counter >= self.text_color_change_duration:
					if self.text_color == (255,0,0):
						self.text_color = (0,0,255)
					else:
						self.text_color = (255,0,0)
					self.text_color_change_duration_counter = 0
					
				else:
					self.text_color_change_duration_counter += 1

				font = pygame.font.Font('fonts/PixelPowerline-9xOK.ttf', 40)
				text = font.render("+"+str(self.point_value), True, (self.text_color[0], self.text_color[1], self.text_color[2]))
				text_rect = text.get_rect(center=(self.rect.x + 48, self.rect.y - self.score_text_y_offset))
				screen.blit(text, text_rect)
				self.score_text_y_offset += 1


	def pollinate(self):
		if not self.pollinated:
			self.counter += 1
			if self.counter > self.pollinate_cooldown:
				self.counter = 0
				self.pollinate_index += 1

			self.image = self.pollinated_images[self.pollinate_index]


			if self.pollinate_index == 4:
				self.pollinated = True
				self.updateScore()
				sound = pygame.mixer.Sound('sound/flower_pollinated.wav')
				pygame.mixer.Sound.play(sound)


	def getPointValue(self):
		return self.point_value

	def updateScore(self):
		global score
		score += self.point_value


# TODO: Animate sunflower, update images
class Sunflower(pygame.sprite.Sprite):

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/sunflower_unpollinated.png')
		self.rect = pygame.Rect(x + 24, y + 24, 40, 40) # rect refers to the center of the flower 
		self.rect.center = [x, y]
		self.point_value = 10
		self.pollinated = False
		self.pollinate_index = 0
		self.counter = 0
		self.pollinate_cooldown = 3
		self.score_text_duration = 0.5 * fps
		self.score_text_duration_counter = 0
		self.score_text_y_offset = 0
		self.text_color_change_duration = int(0.1 * fps)
		self.text_color_change_duration_counter = 0
		self.text_color = (0,0,255)

		#self.pollinated_images = []
		#for num in range(1, 6):
			#img = pygame.image.load(f'img/poppy_pollinated{num}.png')
			#self.pollinated_images.append(img)
		
	def update(self):
		if not game_over:
			self.rect.x -= scroll_speed

			# the time it takes to pollinate a flower decreases as scroll_speed increases 
			if (scroll_speed < 12): # based off linear function
				self.pollinate_cooldown = -(scroll_speed // 2) + initial_scroll_speed + 1
			else:
				self.pollinate_cooldown = 0


			# remove flower when exits the screen
			if self.rect.right < -75:
				self.kill()


			# handle the visual representation of the score increase
			if self.pollinated and self.score_text_duration_counter < self.score_text_duration:
				self.score_text_duration_counter += 1
				if self.text_color_change_duration_counter >= self.text_color_change_duration:
					if self.text_color == (255,0,0):
						self.text_color = (0,0,255)
					else:
						self.text_color = (255,0,0)
					self.text_color_change_duration_counter = 0
					
				else:
					self.text_color_change_duration_counter += 1

				font = pygame.font.Font('fonts/PixelPowerline-9xOK.ttf', 40)
				text = font.render("+"+str(self.point_value), True, self.text_color)
				text_rect = text.get_rect(center=(self.rect.x + 40, self.rect.y - self.score_text_y_offset))
				screen.blit(text, text_rect)
				self.score_text_y_offset += 1


	def pollinate(self):
		if not self.pollinated:
			self.counter += 1
			if self.counter > self.pollinate_cooldown:
				self.counter = 0
				self.pollinate_index += 1

			#self.image = self.pollinated_images[self.pollinate_index]


			if self.pollinate_index == 4:
				self.pollinated = True
				self.image = pygame.image.load('img/sunflower_pollinated.png')
				self.updateScore()
				sound = pygame.mixer.Sound('sound/flower_pollinated.wav')
				pygame.mixer.Sound.play(sound)


	def getPointValue(self):
		return self.point_value

	def updateScore(self):
		global score
		score += self.point_value

# TODO: Add rose which has spikes and takes one heart away 
# TODO: Add venus fly trap which eats the butterfly -- lose all lives
# TODO: Add bee hives that spawn swarms of bees?
# TODO: Add beetles that walk on the ground and take lives?


butterfly_group = pygame.sprite.Group()
monarch = Butterfly(400, SCREEN_HEIGHT//2 + 50)
butterfly_group.add(monarch)



def main_menu():
	global run
	global menu
	fade_out = False

	selected = "start"
	menu_hover_sound = pygame.mixer.Sound('sound/menu_hover.wav')
	menu_select_sound = pygame.mixer.Sound('sound/menu_select.wav')

	while menu:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					selected = "start"
					pygame.mixer.Sound.play(menu_hover_sound)
				elif event.key == pygame.K_DOWN:
					selected = "quit"
					pygame.mixer.Sound.play(menu_hover_sound)
				if event.key == pygame.K_RETURN:
					if selected == "start":
						pygame.mixer.Sound.play(menu_select_sound)
						menu = False
						fade_out = True

						run = True
					if selected == "quit":
						pygame.quit()
						quit()


	     

	       	# Main Menu UI
			title = draw_text("Monarch", font, 90, YELLOW)
			title_outline = draw_text("Monarch", font, 90, BLACK)
			if selected == "start":
				text_start = draw_text("START", font, 90, DARK_BLUE)
				monarch.rect.x = 375
				monarch.rect.y = SCREEN_HEIGHT//2 
			else:
				text_start = draw_text("START", font, 75, WHITE)
			if selected == "quit":
				text_quit = draw_text("QUIT", font, 90, RED)
				monarch.rect.x = 425
				monarch.rect.y = SCREEN_HEIGHT//2 + 150
			else:
				text_quit = draw_text("QUIT", font, 75, WHITE)

			title_rect=title.get_rect()
			start_rect=text_start.get_rect()
			quit_rect=text_quit.get_rect()

	        # Main Menu Text
			clock.tick(fps)
			screen.blit(bg, (0,0))
			screen.blit(title_outline, (SCREEN_WIDTH/2 - (title_rect[2]/2), 100))
			screen.blit(title, (SCREEN_WIDTH/2 - (title_rect[2]/2) - + 10, 100))
			screen.blit(text_start, (SCREEN_WIDTH/2 - (start_rect[2]/2), SCREEN_HEIGHT/2))
			screen.blit(text_quit, (SCREEN_WIDTH/2 - (quit_rect[2]/2), SCREEN_HEIGHT/2 + 150))
			butterfly_group.draw(screen)
			butterfly_group.update()

			"""
			color = 255
			while fade_out:
				pygame.time.wait(10)
				screen.fill((color, color, color))
				if color >= 5:
					color -= 5
				else:
					run = True
					fade_out = False
				pygame.display.update()
			"""

			pygame.display.update()
			
			#pygame.display.set_caption("Monarch - Main Menu")



flower_group = pygame.sprite.Group()
bee_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()



main_menu()
pygame.mixer.music.load('sound/MainTheme_v3.wav')
pygame.mixer.music.play(-1)
# game loop
while run:

	clock.tick(fps)
	# draw the background
	screen.blit(bg, (0, 0))

	# game over if no more hearts or butterfly leaves the screen
	if hearts <= 0 or monarch.rect.right < 0:
		game_over = True


	if not game_over:

		# generate new flowers based on flower_frequency
		if ground_scroll == 0 or abs(ground_scroll) - last_flower > flower_frequency:

			# choose type of flower to add
			flower_type = randint(0,1)

			flowers = [Poppy(SCREEN_WIDTH, ground_height - 140), Sunflower(SCREEN_WIDTH, ground_height - 300)]

			new_flower = flowers[flower_type]
			flower_group.add(new_flower)
			last_flower = abs(ground_scroll)

			# spawn bee on flower based on probability
			# 50% chance : maybe scale with ground covered?
			if random() <= bee_probability:
				new_bee = Bee(new_flower.rect.center[0]+35, new_flower.rect.center[1])
				bee_group.add(new_bee)

			# spawn bird based on probability
			if random() <= bird_probability:
				bird_sound = pygame.mixer.Sound('sound/bird_call.wav')
				pygame.mixer.Sound.play(bird_sound)
				new_bird = Bird(SCREEN_WIDTH, 0, monarch)
				bird_group.add(new_bird)
				

		

		# scroll the ground
		ground_scroll -= scroll_speed
		if abs(ground_scroll) >= SCREEN_WIDTH:
			ground_scroll = 0

		# update total distance
		total_distance += scroll_speed

		# every 100 points, increase scroll_speed by 1 and increase the probability for bees and birds to spawn
		if score > 0 and score - last_score >= 100:
			last_score = score

			scroll_speed += 1

			if bee_probability < 1:
				bee_probability *= 1.1
			if bird_probability < 1:
				bird_probability += 0.025

			print('bee probability',bee_probability)
			print('bird_probability',bird_probability)

		


	# draw the ground
	screen.blit(ground_img, (ground_scroll, ground_height))

	flower_group.draw(screen)
	butterfly_group.draw(screen)
	bee_group.draw(screen)
	bird_group.draw(screen)

	flower_group.update()
	butterfly_group.update()
	bee_group.update()
	bird_group.update()
		
		


	# handle collision between butterfly and flower
	flower_collision = pygame.sprite.groupcollide(butterfly_group, flower_group, False, False)
	if flower_collision:
		for flower in flower_collision.values():
			flower[0].pollinate()

	# handle collision between butterfly and bee
	bee_collision = pygame.sprite.groupcollide(butterfly_group, bee_group, False, False)
	if bee_collision:
		for bee in bee_collision.values():
			#if butterfly.rect.right <= bee[0].rect.left:
			if not monarch.collided and monarch.rect.x <= bee[0].rect.x:
				monarch.collided = True
				collision_sound = pygame.mixer.Sound('sound/bee_collision_v2.wav')
				pygame.mixer.Sound.play(collision_sound)

	# handle collision between butterfly and bird
	bird_collision = pygame.sprite.groupcollide(butterfly_group, bird_group, False, False)
	if bird_collision:
		for bird in bird_collision.values():
			if not bird[0].collided:
				bird[0].collided = True
				monarch.collided = True
				hearts -= 1
				collision_sound = pygame.mixer.Sound('sound/bird_collision.wav')
				pygame.mixer.Sound.play(collision_sound)

			#monarch.rect.x -= (bird[0].dx + scroll_speed)
			if monarch.rect.bottom < ground_height:
				monarch.rect.y += (bird[0].dy)


	# Display the score and heart count on the screen
	score_text = score_font.render(str(score), True, BLACK)
	text_rect = score_text.get_rect(center=(SCREEN_WIDTH/2, 50))
	screen.blit(score_text, text_rect)

	heart_text = draw_text("Hearts: "+str(hearts), font, 50, RED)
	screen.blit(heart_text, (20, 20))

	if game_over:
		# Display "Game Over" text and stop the game
		text = score_font.render('GAME OVER', True, RED)
		text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
		screen.blit(text, text_rect)
		if not game_over_screen:
			game_over_sound = pygame.mixer.Sound('sound/game_over.wav')
			pygame.mixer.Sound.play(game_over_sound)
			pygame.mixer.music.stop()

			game_over_screen = True




	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

quit()