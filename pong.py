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
            self.x_direction = -1

        if self.rect.x < 0:
            self.rect.x = 150
            self.rect.y = 200
            self.x_direction = 1
            self.y_direction = 1
            
        if self.rect.y < 0 or self.rect.y > 460:
            self.y_direction = self.y_direction * -1
            
        self.rect.x += self.speed * self.x_direction
        self.rect.y += self.speed * self.y_direction
                
    
#Creating the groups
all_sprites_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
ball_group = pygame.sprite.Group()

#Creating the players
player1 = Paddle(WHITE, 1)
mainBall = Ball("normal")

#Adding the classes to groups
all_sprites_group.add(player1)
player_group.add(player1)
all_sprites_group.add(mainBall)
ball_group.add(mainBall)

#Setting the size of the screen
size = (640, 480)
screen = pygame.display.set_mode(size)

#Seting the title of the window
pygame.display.set_caption("Pong")


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
        
    #Collision checking
    for player1 in player_group:
        ball_hit_group = pygame.sprite.spritecollide(player1, ball_group, False)
        for mainBall in ball_hit_group:
            mainBall.x_direction = 1
    
    #Update sprites
    all_sprites_group.update()
    
    #Create the black background
    screen.fill(BLACK)

    #Drawing the sprites
    all_sprites_group.draw(screen)
    
    #Flip display
    pygame.display.flip()

    #Set clock speed
    clock.tick(60)
pygame.quit()
