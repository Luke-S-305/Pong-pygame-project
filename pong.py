#Importing modules needed
import pygame
import random
import math
import decimal

#Defining colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 0)

#defining some variables before classes
global timer
timer = 0

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
        self.dy = dy * self.speed

    def returnDy(self):
        #a function to return what direction and what speed the paddle is moving at
        return self.dy

    def poweringUp(self, powerType):
        if powerType == "increase size":
            global timer
            self.startTimer = timer
            print(self.startTimer)
            self.height = 90
            self.width = 15
            self.image = pygame.Surface([self.width, self.height])
            self.image.fill(WHITE)

        if powerType == "increase speed":
            self.startTimer = timer
            self.speed = 1.5

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
            self.angle = math.pi * float(decimal.Decimal(random.randrange(5, 25))/100) #generating random decimal between 0.05 and 0.25
            self.speed = 4
            self.x_direction = 1
            self.y_direction = 1

            self.speed = 4
            self.image = pygame.Surface([self.width, self.height])
            self.image.fill(WHITE)
            self.rect = self.image.get_rect()
            self.reset()
            
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

        self.getComponents()
        self.rect.x += self.dx
        self.rect.y += self.dy

    def reset(self):
        #Put the ball back in the middle of the screen
        self.rect.x = 150
        self.rect.y = 200
        self.x_direction = 1
        self.y_direction = 1
        self.angle = math.pi * float(decimal.Decimal(random.randrange(5, 25))/100) #generating random decimal between 0.05 and 0.25

    def getComponents(self):
        #Set dy and dx based off angle generated with trigonometry
        self.dx = self.speed * math.cos(self.angle) * self.x_direction
        print(math.cos(self.angle))
        self.dy = self.speed * math.sin(self.angle) * self.y_direction
        print(math.sin(self.angle))   

            
##        self.rect.x += self.speed * self.x_direction
##        self.rect.y += self.speed * self.y_direction

        self.getComponents()
        #print(self.dx)
        #print(self.dy)
        self.rect.x += self.dx
        self.rect.y += self.dy

    def getComponents(self):
        #Set dy and dx based off angle generated with trigonometry
        self.dx = self.speed * math.cos(self.angle) * self.x_direction
        #print(math.cos(self.angle))
        self.dy = self.speed * math.sin(self.angle) * self.y_direction
        #print(math.sin(self.angle))

    def changeAngle(self, movement):
        if movement < 0:
            #change angle here
            if self.y_direction == -1:
                self.angle += 0.3
                if self.angle > 1.5:
                    self.angle = 1.5
            if self.y_direction == 1:
                self.angle += -0.3
                if self.angle < 0:
                    #make sure the angle is always positive
                    self.angle = self.angle * -1
                    self.y_direction = self.y_direction * -1
            #need code for if the ball is going straight
                
        if movement > 0:
            #change angle here
            if self.y_direction == -1:
                self.angle += -0.3
                if self.angle < 0:
                    #make sure the angle is always positive
                    self.angle = self.angle * -1
                    self.y_direction = self.y_direction * -1
            if self.y_direction == 1:
                self.angle += 0.3
                if self.angle > 1.5:
                    self.angle = 1.5
            #need code for if the ball is going straight

        #do nothing if movement is 0

    def reset(self):
        #Put the ball back in the middle of the screen
        self.rect.x = 320
        self.rect.y = 240
        self.angle = math.pi * float(decimal.Decimal(random.randrange(5, 25))/100) #generating random decimal between 0.05 and 0.25
        self.x_direction = random.choice([-1, 1])
        self.y_direction = random.choice([-1, 1])

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #defining base characteristics which are the same for all power ups
        self.width = 30
        self.height = 30
        self.direction = 0
        self.powerUpType = 0
        self.randomPowerUp()
        #determine the state that the powerup is in
        self.state = "not hit"
        #position is defined after the sprite has been determined
        self.randomLocation()

    def hit(self, direction):
        self.direction = direction
        self.state = "hit"

        #Change the look of the powerup once it has been hit
        self.height = 10
        self.width = 20
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLUE)

    def randomPowerUp(self):
        seed = random.randint(1,2)
        if seed == 1:
            self.powerUpType = "increase size"
            print("working")
        if seed == 2:
            self.powerUpType = "increase speed"
            print("working")

        #visuals for each powerup
        if self.powerUpType == "increase size":
            self.image = pygame.Surface([self.width, self.height])
            self.image.fill(BLUE)
            self.rect = self.image.get_rect()

        if self.powerUpType == "increase speed":
            self.image = pygame.Surface([self.width, self.height])
            self.image.fill(BLUE)
            self.rect = self.image.get_rect()

    def randomLocation(self):
        self.rect.x = random.randint(100, 500)
        self.rect.y = random.randint(100, 340)
        
    def update(self):
        self.rect.x += self.direction * 4
    
#Creating the groups
all_sprites_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
powerUp_group = pygame.sprite.Group()

#Creating the players
player1 = Paddle(WHITE, 1)
player2 = Paddle(WHITE, 2)
ball = Ball("normal")
powerUp = PowerUp()

#Adding the classes to groups
all_sprites_group.add(player1)
player_group.add(player1)

all_sprites_group.add(player2)
#player_group.add(player2) ---Movement is lost when this line is added

all_sprites_group.add(ball)
ball_group.add(ball)

all_sprites_group.add(powerUp)
powerUp_group.add(powerUp)

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
        player1.moveY(-6)
        plr1KeyPressed = 1
    if keys[pygame.K_s] and player1.rect.y < 420:
        player1.moveY(6)
        plr1KeyPressed = 1
    if plr1KeyPressed == 0:
        #If no keys have been pressed
        player1.moveY(0)

    plr2KeyPressed = 0 #Checks if a key has been pressed by player 2
    if keys[pygame.K_UP] and player2.rect.y > 0:
        player2.moveY(-6)
        plr2KeyPressed = 1
    if keys[pygame.K_DOWN] and player2.rect.y < 420:
        player2.moveY(6)
        plr2KeyPressed = 1
    if plr2KeyPressed == 0:
        #If no keys have been pressed
        player2.moveY(0)

    #Spawning powerups
    spawnChance = random.random()
    if spawnChance < 0.001:
        powerUp = PowerUp()
        powerUp_group.add(powerUp)
        all_sprites_group.add(powerUp)
    
    #Collision checking
    player1_ball_hit_group = pygame.sprite.spritecollide(player1, ball_group, False)
    #For each "main ball" hit, direction change
    for mainBall in player1_ball_hit_group:
        mainBall.x_direction = 1

    player2_ball_hit_group = pygame.sprite.spritecollide(player2, ball_group, False)
    #For each "main ball" hit, direction change
    for mainBall in player2_ball_hit_group:
        mainBall.x_direction =  -1

    for ball in player1_ball_hit_group:
        ball.x_direction = 1
        #find and store what direction player 1 is moving
        playerMovement = player1.returnDy()
        ball.changeAngle(playerMovement)


    player2_ball_hit_group = pygame.sprite.spritecollide(player2, ball_group, False)
    #For each "main ball" hit, direction change
    for ball in player2_ball_hit_group:
        ball.x_direction = -1
        #find and store what direction player 2 is moving
        playerMovement = player2.returnDy()
        ball.changeAngle(playerMovement)


    #When a ball hits the powerup
    #Go through all powerups in the powerup group one by one
    for x in powerUp_group:
        #Now that one powerup has been isolated, create another group for that single powerup
        powerUp_hit_group = pygame.sprite.spritecollide(powerUp, ball_group, False)
        #Now going through the newly created group to isolate each ball that has collided with that single powerup
        for y in powerUp_hit_group:
            #Find the direction the ball is travelling in
            direction = ball.x_direction
            #Reverse the direction (so the power up travels back from where the ball is coming from)
            direction = direction * -1
            powerUp.hit(direction)
            print("powerup hit detection working")

    #Collision checking between powerups FOR PLAYER 1 (see collisions code comments above for more detail)
    for x in player_group:
        #Isolate each player
        player_hit_group = pygame.sprite.spritecollide(player1, powerUp_group, False)
        #Go through powerup collisions induvidually
        for y in player_hit_group:
            #Find what type of powerup it is
            powerType = powerUp.powerUpType
            player1.poweringUp(powerType)
            powerUp_group.remove(powerUp)
            all_sprites_group.remove(powerUp)

    #Collision checking between powerups FOR PLAYER 2
    for x in player_group:
        #Isolate each player
        player_hit_group = pygame.sprite.spritecollide(player2, powerUp_group, False)
        #Go through powerup collisions induvidually
        for y in player_hit_group:
            #Find what type of powerup it is
            powerType = powerUp.powerUpType
            player2.poweringUp(powerType)
            powerUp_group.remove(powerUp)
            all_sprites_group.remove(powerUp)

    

    
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
    
    #Test values
##    print(math.radians(45))
##    print(math.cos(math.radians(45)))
##    print(math.sin(math.radians(45)))

    timer += 1
    #Set clock speed
    clock.tick(60)
pygame.quit()

