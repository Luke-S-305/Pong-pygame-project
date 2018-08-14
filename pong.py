#Importing modules needed
import pygame
import random

#Defining colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 0)

#Initilising pygame
pygame.init()
#Initialize text module
pygame.font.init() 

#Adding classes
class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, playerNum):
        super().__init__()
        #Adding a speed attribute for power-ups
        self.speed = 1
        #Adding an attribute for change in x/y
        self.dx = 0
        self.dy = 0
        #Creating the paddle
        self.width = 15
        self.height = 60
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        #Placing the paddle on the screen depending on which player it is
        #NOTE: change the coordinates to be relative to the screen size
        if playerNum == 1:
            self.rect.x = 10
        elif playerNum == 2:
            self.rect.x = 615
        self.rect.y = 20

    def moveY(self, dy):
        #setting the change in Y
        self.dy = dy
                

    def update(self):
        self.rect.y += self.dy
        self.rect.x += self.dx

class Ball(pygame.sprite.Sprite):
    def __init__(self, ballType):
        super().__init__()
        #Deciding what type of ball it should be
        if ballType == "normal":
            self.width = 20
            self.height = 20
            self.speed = 1
            self.x_direction = 1
            self.y_direction = 1
            self.image = pygame.Surface([self.width, self.height])
            self.image.fill(WHITE)
            self.rect = self.image.get_rect()
            self.rect.x = 200
            self.rect.y = 200

    def update(self):
        #Ball physics
        if self.rect.x > 620:
            self.reset()
            scored("player1")

        if self.rect.x < 0:
            self.reset()
            scored("player2")
            
        if self.rect.y < 0 or self.rect.y > 460:
            self.y_direction = self.y_direction * -1
            
        self.rect.x += self.speed * self.x_direction
        self.rect.y += self.speed * self.y_direction

    def reset(self):
        #Put the ball back in the middle of the screen
        self.rect.x = 150
        self.rect.y = 200
        self.x_direction = 1
        self.y_direction = 1
                
    
#Creating the groups
all_sprites_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
ball_group = pygame.sprite.Group()

#Creating the players
player1 = Paddle(WHITE, 1)
player2 = Paddle(WHITE, 2)
mainBall = Ball("normal")

#Adding the classes to groups
all_sprites_group.add(player1)
player_group.add(player1)

all_sprites_group.add(player2)
#player_group.add(player2) ---Movement is lost when this line is added

all_sprites_group.add(mainBall)
ball_group.add(mainBall)

#Setting the size of the screen
screenWidth = 640
screenHeight = 480
size = (screenWidth, screenHeight)
screen = pygame.display.set_mode(size)

#Seting the title of the window
pygame.display.set_caption("Pong")

#define variables
player1Score = 0
player2Score = 0


#define functions
def scored(player):
    if player == "player1":
        print("player 1 scored!")
        global player1Score
        player1Score += 1
    if player == "player2":
        print("player 2 scored!")
        global player2Score
        player2Score += 1

done = False
clock = pygame.time.Clock()

###MAIN LOOP
while not done:
    #Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    #Check keypresses
    keys = pygame.key.get_pressed()
    plr1KeyPressed = 0 #Checks if a key has been pressed by player 1
    if keys[pygame.K_w] and player1.rect.y > 0:
        player1.moveY(-5)
        plr1KeyPressed = 1
    if keys[pygame.K_s] and player1.rect.y < 420:
        player1.moveY(5)
        plr1KeyPressed = 1
    if plr1KeyPressed == 0:
        #If no keys have been pressed
        player1.moveY(0)

    plr2KeyPressed = 0 #Checks if a key has been pressed by player 2
    if keys[pygame.K_UP] and player2.rect.y > 0:
        player2.moveY(-5)
        plr2KeyPressed = 1
    if keys[pygame.K_DOWN] and player2.rect.y < 420:
        player2.moveY(5)
        plr2KeyPressed = 1
    if plr2KeyPressed == 0:
        #If no keys have been pressed
        player2.moveY(0)

    #Collision checking
    player1_ball_hit_group = pygame.sprite.spritecollide(player1, ball_group, False)
    #For each "main ball" hit, direction change
    for mainBall in player1_ball_hit_group:
        mainBall.x_direction = mainBall.x_direction * -1

    player2_ball_hit_group = pygame.sprite.spritecollide(player2, ball_group, False)
    #For each "main ball" hit, direction change
    for mainBall in player2_ball_hit_group:
        mainBall.x_direction = mainBall.x_direction * -1
    
    #Update sprites
    all_sprites_group.update()
    
    #Create the black background
    screen.fill(BLACK)

    #Drawing the sprites
    all_sprites_group.draw(screen)

    #Drawing text
    myfont = pygame.font.SysFont("Comic Sans MS", 50)
    textsurface = myfont.render(str(player1Score) + " - " + str(player2Score), False, WHITE)
    screen.blit(textsurface,(270,10))
    
    #Flip display
    pygame.display.flip()

    #Set clock speed
    clock.tick(60)
pygame.quit()

