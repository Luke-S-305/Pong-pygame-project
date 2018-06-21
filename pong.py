import pygame
#Importing modules needed

#Defining colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 0)

#Initilising pygame
pygame.init()

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
        if ballType = normal:
            self.width = 20
            self.height = 20
            self.image = pygame.Surface([self.width, self.height])
            self.image.fill(WHITE)
            self.rect = self.image.get_rect()
    
#Creating the groups
all_sprites_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

#Creating the players
player1 = Paddle(WHITE, 1)

#Adding the classes to groups
all_sprites_group.add(player1)
player_group.add(player1)

#Setting the size of the screen
size = (640, 480)
screen = pygame.display.set_mode(size)

#Seting the title of the window
pygame.display.set_caption("Pong")


done = False
#Setting the positional values of the ball
x_val = 150
y_val = 200

x_direction = 1
y_direction = 1



clock = pygame.time.Clock()

###MAIN LOOP
while not done:
    #Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    #Check keypresses
    keys = pygame.key.get_pressed()
    keyPressed = 0 #keyPressed checks if a key has been pressed
    if keys[pygame.K_UP] and player1.rect.y > 0:
        player1.moveY(-5)
        keyPressed = 1
    if keys[pygame.K_DOWN] and player1.rect.y < 420:
        player1.moveY(5)
        keyPressed = 1
    if keyPressed == 0:
        #If no keys have been pressed
        player1.moveY(0)

    #Ball physics
    if x_val > 620:
        x_direction = -1

    if x_val < 0:
        x_val = 150
        y_val = 200
        x_direction = 1
        y_direction = 1
        
    if y_val < 0 or y_val > 460:
        y_direction = y_direction * -1

    #collision with player1
    if x_val < player1.rect.x + 15 and y_val > player1.rect.y and y_val < player1.rect.y + 60:
        x_direction = 1
        
    x_val = x_val + x_direction
    y_val = y_val + y_direction
    
    #Update sprites
    all_sprites_group.update()
    
    #Create the black background
    screen.fill(BLACK)

    #Drawing the sprites
    pygame.draw.rect(screen, WHITE, (x_val, y_val, 20, 20))
    all_sprites_group.draw(screen)
    
    #Flip display
    pygame.display.flip()

    #Set clock speed
    clock.tick(60)
pygame.quit()
