from turtle import up
import pygame, sys, random
from pygame.math import Vector2 #this makes it that everytime i want to write vector2, i dont need to write pygame.math.Vector2 everytime, i just type Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load("Pictures/headup.png").convert_alpha()
        self.head_down = pygame.image.load("Pictures/headdown.png").convert_alpha()
        self.head_left = pygame.image.load("Pictures/headleft.png").convert_alpha()
        self.head_right = pygame.image.load("Pictures/headright.png").convert_alpha()

        self.tail_up = pygame.image.load("Pictures/tailup.png").convert_alpha()
        self.tail_down = pygame.image.load("Pictures/taildown.png").convert_alpha()
        self.tail_left = pygame.image.load("Pictures/tailleft.png").convert_alpha()
        self.tail_right = pygame.image.load("Pictures/tailright.png").convert_alpha()

        self.body_vertical = pygame.image.load("Pictures/bodyvertical.png").convert_alpha()
        self.body_horizontal = pygame.image.load("Pictures/bodyhorizontal.png").convert_alpha()

        self.body_tr = pygame.image.load("Pictures/bodytr.png").convert_alpha()
        self.body_tl = pygame.image.load("Pictures/bodytl.png").convert_alpha()
        self.body_br = pygame.image.load("Pictures/bodybr.png").convert_alpha()
        self.body_bl = pygame.image.load("Pictures/bodybl.png").convert_alpha()

        self.crunch_sound = pygame.mixer.Sound("Sounds/crunch1.mp3")
        self.boink_sound = pygame.mixer.Sound("Sounds/boink.wav")

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            #1. we still need a rect for the positioning
            x_pos = int(block.x * cell_size)
            y_pos = int( block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            #2. what direction is the snake heading
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block #subtracts block to get the relation between the current block and the previous/next one
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)    
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]   #using vectors subtraction to figure the relation of the body parts(if the previous of the head is on the left, right, up, or down)
        if head_relation == Vector2(1, 0): self.head = self.head_left
        elif head_relation == Vector2(-1, 0): self.head = self.head_right
        elif head_relation == Vector2(0, -1): self.head = self.head_down
        elif head_relation == Vector2(0, 1): self.head = self.head_up

    def update_tail_graphics(self):
        tail_relation = self.body[len(self.body) - 1] - self.body[len(self.body) - 2]
        if tail_relation == Vector2(1, 0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(0, -1): self.tail = self.tail_down
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_up

        #for block in self.body:
            ##create a rectangle
            #x_pos = int(block.x * cell_size)
            #y_pos = int( block.y * cell_size)
            #block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)    #no moore needed after going to add snake textures
            ##draw a rectangle
            #pygame.draw.rect(screen, (183, 111, 122), block_rect)

    def move_snake(self):
        if self.new_block == False:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
        else:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()
    
    def play_boink_sound(self):
        self.boink_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)

class FRUIT:
    def __init__(self):
        self.randomize()
        
    def draw_fruit(self):
        #create a rectangle
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int (self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)
        #draw the rectangle
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect) #not needed after the image insert

    def randomize(self):
        #create an x and a y position
        #draw a square in this position(fruit)
        self.x = random.randint(0, cell_number -1)
        self.y = random.randint(0, cell_number -1)
        self.pos = Vector2(self.x, self.y) #using vectors is way easier to animate


class MAIN: #where it will contain all the logic of the game
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update (self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
    
    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            #reposition the fruit
            self.fruit.randomize()
            #add another block to the snake
            self.snake.add_block()
            self.snake.play_crunch_sound()
        
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
        

    def check_fail(self):
        #check if snake is outside of the screen
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.snake.play_boink_sound()
            self.game_over()
        #check if snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
                
    def game_over(self):
        
        self.snake.reset()

    def draw_grass(self):
        grass_color = (73, 136, 47)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, "White")
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left - 6, apple_rect.top - 6, apple_rect.width + score_rect.width + 16, apple_rect.height + 12 )

        pygame.draw.rect(screen, (73, 136, 47), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, "White", bg_rect, 3)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 32
cell_number = 20
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
clock = pygame.time.Clock()
apple = pygame.image.load("Pictures/apple.png").convert_alpha()
game_font = pygame.font.Font("Fonts/PoetsenOne-Regular.ttf", 25)
Syntax: pygame.display.set_caption('snake by pedro :)')
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 80)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2 (0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2 (0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2 (-1, 0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2 (1, 0)

    screen.fill((79, 147, 50))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)