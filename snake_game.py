import pygame
import time
from pygame.locals import *
import random
#use surface.blit to display something
SIZE = 40
Background_colour = (110, 110, 5)

class Apple:
    def __init__ (self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("Resources/apple.jpg")
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image,(self.x,self.y))#draws block
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 24)*SIZE
        self.y = random.randint(1, 19)*SIZE
    

class Snake:
    def __init__(self, parent_screen, length):    #fuction with two arrguments  
        self.parent_screen = parent_screen #stops having duplicate blocks from appering
        self.block = pygame.image.load("Resources/block.jpg").convert() #loads image 
        self.direction = 'down'

        self.length = 1
        self.x = [40]*length
        self.y = [40]*length

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    
    def walk(self):
        #update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        #updates head
        if self.direction == 'left':
            self.x[0] -=SIZE
        if self.direction == 'right':
            self.x[0] +=SIZE
        if self.direction == 'up':
            self.y[0] -=SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):      
      

        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))#draws block
        pygame.display.flip()

    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)
        
class Game:
    def __init__(self):
        pygame.init()   #intialises pygame module
        pygame.display.set_caption("Snake")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1000, 800))#intialise window 
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2): 
        if x1 >= x2 and x1 < x2 + SIZE: #check for collison
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False
    
    def play_background_music(self):
        pygame.mixer.music.load("Resources/bg_music_1.mp3")
        pygame.mixer.music.play()

    def play_sound(self, sound):        #function to play sound
        sound = pygame.mixer.Sound(f"Resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("Resources/background.jpg")
        self.surface.blit(bg, (0,0))

    def play(self): #doing all drawing
        self.render_background()
        self.snake.walk() #snake walks on its own
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

         #snake colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()            
            self.apple.move()

        #snake colliding with itslef
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0], self.snake.x[i], self.snake.y[i]):
               self.play_sound("crash")
               raise "Game Over"
           #snake goes put of bounds
        if not (0 <= self.snake.x[0] < 1000 and 0 <= self.snake.y[0] < 800):
            self.play_sound('crash')
            raise "Hit the boundry error"

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}",True, (255, 0, 0)) #displaying snakes length
        self.surface.blit(score, (850,10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game Over! Your Score: {self.snake.length}", True, (255, 0, 0))
        self.surface.blit(line1, (200,300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 0, 0))
        self.surface.blit(line2, (200,350))   
        
        pygame.display.flip()
        pygame.mixer.music.pause()
    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
                    
            try:

                if not pause:
                   self.play()

            except Exception as e:
               self.show_game_over()
               pause = True
               self.reset()

            time.sleep(.1)

if __name__ == "__main__":  # doublecheck:
    game = Game()
    game.run()
    
   
    
   
    
   
    
    

            

