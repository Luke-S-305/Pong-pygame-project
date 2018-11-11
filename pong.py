#Importing modules needed
import pygame
import random
import math
import decimal
import time

#Defining colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

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

    def returnY(self):
        return self.rect.y

    def returnWidth(self):
        return self.width

    def update(self):
        self.rect.y += self.dy
        if self.rect.y > (screenHeight - self.height):
            self.rect.y = screenHeight - self.height
        if self.rect.y < 0:
            self.rect.y = 0

class Ball(pygame.sprite.Sprite):
    def __init__(self, ballType):
        super().__init__()
        #Deciding what type of ball it should be
        self.ballType = ballType
        if self.ballType == "normal":
            self.width = 20
            self.height = 20
            self.angle = math.pi * float(decimal.Decimal(random.randrange(5, 25))/100) #generating random decimal between 0.05 and 0.25
            self.x_direction = 1
            self.y_direction = 1

            self.speed = 4
            self.image = pygame.Surface([self.width, self.height])
            self.image.fill(WHITE)
            self.rect = self.image.get_rect()
            self.reset()

        if self.ballType == "shadow":
            #Set basic values, others will be set in shadowReset()
            self.width = 20
            self.height = 20
            self.speed = 4
            self.image = pygame.Surface([self.width, self.height])
            self.image.fill(RED)
            self.rect = self.image.get_rect()
            #some placeholders
            self.angle = 0
            self.x_direction = 0
            self.y_direction = 0
            
    def update(self):
        #Ball physics
        if self.rect.x > 620:
            if self.ballType == "normal":
                self.reset()
                scored("player1")
                
            if self.ballType == "shadow":
                self.speed = 0

        if self.rect.x < 0:
            if self.ballType == "normal":
                self.reset()
                scored("player2")
                
            if self.ballType == "shadow":
                self.speed = 0
            
        if self.rect.y < 0:
            self.bounce("down")
            self.rect.y = 0
        if self.rect.y > 460:
            self.bounce("up")
            self.rect.y = 460

        self.getComponents()

        #First update x direction
        self.rect.x += self.dx
        #Check for collisons with walls
        wall_hit_list = pygame.sprite.spritecollide(self, wall_group, False)
        for wall in wall_hit_list:
            #if moving right, move the right edge of the ball to the left edge of the wall hit
            if self.dx > 0:
                self.rect.right = wall.rect.left
                self.bounce("left")
            else:
                #do the opposite for the opposite direction
                self.rect.left = wall.rect.right
                self.bounce("right")
        
        #Then update y direction
        self.rect.y += self.dy
        #Check for collisions with walls again
        wall_hit_list = pygame.sprite.spritecollide(self, wall_group, False)
        for wall in wall_hit_list:
            #if moving down, move the bottom edge of the ball to the top edge of the wall hit
            if self.dy > 0:
                self.rect.bottom = wall.rect.top
                self.bounce("up")
            else:
                #do the opposite for the opposite direction
                self.rect.top = wall.rect.bottom
                self.bounce("down")

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
                if self.angle > 1.2:
                    self.angle = 1.2
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
                if self.angle > 1.2:
                    self.angle = 1.2
            #need code for if the ball is going straight

        #do nothing if movement is 0

    def bounce(self, direction):
        if direction == "up":
            self.y_direction = -1
        if direction == "down":
            self.y_direction = 1
        if direction == "left":
            self.x_direction = -1
        if direction == "right":
            self.x_direction = 1

    def returnY(self):
        return self.rect.y

    def returnX(self):
        return self.rect.x

    def shadowReset(self, angle = -1, x = 0, y = 0, y_dir = 0):
        #make the shadow ball take the data from the main ball
        self.width = 20
        self.height = 20
        self.angle = angle
        self.x_direction = 1
        self.y_direction = y_dir
        self.speed = 4
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #give the shadow ball a head start by a random value between 
        for i in range(random.randint(1, 50)):
            self.update()
    
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

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

#Creating the groups
all_sprites_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
powerUp_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()

#Creating the players
player1 = Paddle(WHITE, 1)
player2 = Paddle(WHITE, 2)
mainBall = Ball("normal")
#create a shadow ball for the "hard AI"
shadowBall = Ball("shadow")
shadowBall.shadowReset(mainBall.angle, mainBall.rect.x, mainBall.rect.y, mainBall.y_direction)

#Adding the classes to groups
all_sprites_group.add(player1)
player_group.add(player1)

all_sprites_group.add(player2)
#player_group.add(player2) ---Movement is lost when this line is added

all_sprites_group.add(mainBall)
ball_group.add(mainBall)

all_sprites_group.add(shadowBall)
ball_group.add(shadowBall)

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
powerUpInPlay = 0
gameStage = "watch example gameplay select"
numberOfPlayers = 0
difficulty = "medium" #Default normal for 2 player

#define menu variables
instructionsPointer = 0
playerSelectPointer = 0
menuSelectPointer = 0 
difficultySelectPointer = 0
exampleGameplaySelectPointer = 0
easyMapSelectionPointer = 0
mediumMapSelectionPointer = 0



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
    shadowBall.shadowReset(mainBall.angle, mainBall.rect.x, mainBall.rect.y, mainBall.y_direction)

#Take in a map to draw and then place blocks
def drawMap(map):
    for x in range(12):
        for y in range(16):
            if map[x][y] == 1:
                #fixed by swapping the x and y values in the constructor
                my_wall = Wall(y*40, x*40, 40, 40)
                wall_group.add(my_wall)
                all_sprites_group.add(my_wall)

def createMap(number):
    #Creating maps
    map1 = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

    map2 = [[0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0],
           [0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0],
           [0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0],
           [0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0],
           [0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0]]

    map3 = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0],
           [0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0],
           [0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0],
           [0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0],
           [0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    
    if number == 1:
        drawMap(map1)
    elif number == 2:
        drawMap(map2)
    elif number == 3:
        drawMap(map3)

done = False
clock = pygame.time.Clock()
#drawMap(map3)

#Creating AI players
def antiJitter(paddleY, ballY, paddleHeight):
    if ballY >= paddleY and ballY <= paddleY + paddleHeight:
        return True
    else:
        return False
    
def easyAI(paddleXLocation):
    global screenHeight
    #probability is the chance that the paddle moves down. It will otherwise move up
    probability = (screenHeight - paddleXLocation)/(screenHeight - 60)
    if probability >= random.random():
        return "down"
    else:
        return "up"

def mediumAI(ballX,ballY,paddleY, paddleHeight, side):
    #side is which side the paddle is situated on
    if side == "right":
        #if the ball is in the latter quarter of the screen
        if ballX > screenWidth * 0.8: #follow ball
            if not antiJitter(paddleY, ballY, paddleHeight): #check if the ball is within the paddle range
                if ballY > paddleY+(paddleHeight/2):
                    return "down" #remember y = o at the top of the screen
                elif ballY < paddleY+(paddleHeight/2):
                    return "up" #remember y = o at the top of the screen
            else:
                return "none"
        else: #Move towards middle
            if paddleY+(paddleHeight/2) > (screenHeight*(3/4)):
                return "up" #remember y = o at the top of the screen
            elif paddleY+(paddleHeight/2) < (screenHeight*(1/4)):
                return "down" #remember y = o at the top of the screen
            else:
                return "none"
            
    if side == "left":
        #if the ball is in the first quarter of the screen
        if ballX < screenWidth * 0.2: #follow ball
            if not antiJitter(paddleY, ballY, paddleHeight): #check if the ball is within the paddle range
                if ballY > paddleY+(paddleHeight/2):
                    return "down" #remember y = o at the top of the screen
                elif ballY < paddleY+(paddleHeight/2):
                    return "up" #remember y = o at the top of the screen
            else:
                return "none"
        else: #Move towards middle
            if paddleY+(paddleHeight/2) > (screenHeight*(3/4)):
                return "up" #remember y = o at the top of the screen
            elif paddleY+(paddleHeight/2) < (screenHeight*(1/4)):
                return "down" #remember y = o at the top of the screen
            else:
                return "none"


def hardAI(shadowballX,shadowballY,paddleY, paddleHeight, side):
    #side is which side the paddle is situated on
    if side == "right":
        #if the ball is in the latter quarter of the screen
        if shadowballX > screenWidth * 0.6: #follow ball
            if not antiJitter(paddleY, shadowballY, paddleHeight): #check if the ball is within the paddle range
                if shadowballY > paddleY+(paddleHeight/2):
                    return "down" #remember y = o at the top of the screen
                elif shadowballY < paddleY+(paddleHeight/2):
                    return "up" #remember y = o at the top of the screen
            else:
                return "none"

            
    if side == "left":
        #if the ball is in the first quarter of the screen
        if ballX < screenWidth * 0.4: #follow ball
            if not antiJitter(paddleY, shadowballY, paddleHeight): #check if the ball is within the paddle range
                if ballY > paddleY+(paddleHeight/2):
                    return "down" #remember y = o at the top of the screen
                elif ballY < paddleY+(paddleHeight/2):
                    return "up" #remember y = o at the top of the screen
            else:
                return "none"

    

#the menu select function used to navigate menus
def menuSelect(noOfOptions, selectedOptionNumber):
    #Check keypresses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        #Using the mod function
        selectedOptionNumber = (selectedOptionNumber + 1) % noOfOptions
    if keys[pygame.K_s]:
        #If the selected option has the number 0,
        if selectedOptionNumber == 0:
            #Set the selection to the highest value possible (the reverse of the mod function)
            selectedOptionNumber = noOfOptions - 1
        else:
            #If selection is not 0, reduce it by 1
            selectedOptionNumber = selectedOptionNumber - 1
    return selectedOptionNumber
            

#Defining different modules that will make up the game:
def instructions():

    #no need for menuSelect() as there is only 1 option
        
    #Display elements
    screen.fill(BLACK)
    titleFont = pygame.font.SysFont("Andale mono", 100)
    textFont = pygame.font.SysFont("Andale mono", 30)
    optionFont = pygame.font.SysFont("Andale mono", 50)
    
    title = titleFont.render("instructions", False, WHITE)
    mainText = textFont.render("Use the <w> and <s> keys to move your paddle up and down", False, WHITE)
    exitText = textFont.render("Press the <ENTER> key to continue", False, RED)

    #Check keypresses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        #Make sure variables being changed are global
        global gameStage
        gameStage = "player select"
        
    #drawing the text
    screen.blit(title,(100,10))
    screen.blit(mainText,(10,150))
    screen.blit(exitText,(10,250))
    pygame.display.update()

    #Set clock speed
    clock.tick(10)

def watchExampleGameplaySelect():
    #Display elements
    screen.fill(BLACK)
    titleFont = pygame.font.SysFont("Andale mono", 100)
    textFont = pygame.font.SysFont("Andale mono", 30)
    optionFont = pygame.font.SysFont("Andale mono", 50)

    #run menu selection function
    global exampleGameplaySelectPointer
    exampleGameplaySelectPointer = menuSelect(2, exampleGameplaySelectPointer)
    
    mainText = textFont.render("Would you like to watch some example gameplay?", False, WHITE)
    instructionText1 = textFont.render("Use the <w> and <s> keys select an option", False, WHITE)
    instructionText2 = textFont.render("Press enter to confirm your option", False, WHITE)
    #logic to determine which option should be highlighted
    if exampleGameplaySelectPointer == 0:
        yes = optionFont.render("yes", False, RED)
        no = optionFont.render("no", False, WHITE)
    elif exampleGameplaySelectPointer == 1:
        yes = optionFont.render("yes", False, WHITE)
        no = optionFont.render("no", False, RED)

    #Check keypresses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        #Make sure variables being changed are global
        global gameStage
        if exampleGameplaySelectPointer == 0:
            gameStage = "example gameplay"
        elif exampleGameplaySelectPointer == 1:
            gameStage = "instructions"

    #drawing the text
    screen.blit(mainText,(50,10))
    screen.blit(instructionText1, (10, 100))
    screen.blit(instructionText2, (10, 150))
    screen.blit(yes,(50,200))
    screen.blit(no,(400,200))
    pygame.display.update()

    #Set clock speed
    clock.tick(10)

def exampleGameplay():
    ###similar to main gameplay only missing some elements to simplify the gameplay
    #Ensure global variables are used
    global powerUpInPlay
    global player1Score
    global player2Score

    #Uses medium difficulty AI
    global mainBall
    #AI number 1
    if mediumAI(mainBall.returnX(), mainBall.returnY(), player1.returnY(), player1.returnWidth(), "left") == "up":
        player1.moveY(-6)
    elif mediumAI(mainBall.returnX(), mainBall.returnY(), player1.returnY(), player1.returnWidth(), "left") == "down":
        player1.moveY(6)
    elif mediumAI(mainBall.returnX(), mainBall.returnY(), player1.returnY(), player1.returnWidth(), "left") == "none":
        player1.moveY(0)
    
    #AI number 2
    if mediumAI(mainBall.returnX(), mainBall.returnY(), player2.returnY(), player2.returnWidth(), "right") == "up":
        player2.moveY(-6)
    elif mediumAI(mainBall.returnX(), mainBall.returnY(), player2.returnY(), player2.returnWidth(), "right") == "down":
        player2.moveY(6)
    elif mediumAI(mainBall.returnX(), mainBall.returnY(), player2.returnY(), player2.returnWidth(), "right") == "none":
        player2.moveY(0)
    
    #Collision checking
    player1_ball_hit_group = pygame.sprite.spritecollide(player1, ball_group, False)
    for ball in player1_ball_hit_group:
        ball.bounce("right")
        #find and store what direction player 1 is moving
        playerMovement = player1.returnDy()
        ball.changeAngle(playerMovement)


    player2_ball_hit_group = pygame.sprite.spritecollide(player2, ball_group, False)
    for ball in player2_ball_hit_group:
        ball.bounce("left")
        #find and store what direction player 2 is moving
        playerMovement = player2.returnDy()
        ball.changeAngle(playerMovement)

    #User input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]: #on pressing enter
        #Make sure variables being changed are global
        global gameStage
        gameStage = "instructions" #move on to instruction stage
        time.sleep(0.1) #Sleep statement used to prevent enter keypress being registered in the next menu    
    
    #Update sprites
    all_sprites_group.update()
    
    #Create the black background
    screen.fill(BLACK)

    #Drawing the sprites
    all_sprites_group.draw(screen)

    #Drawing text
    myfont = pygame.font.SysFont("Andale mono", 100)
    textsurface = myfont.render(str(player1Score) + " - " + str(player2Score), False, WHITE)
    screen.blit(textsurface,(270,10))

    #Text graphic showing how to get out the example gameplay
    textFont = pygame.font.SysFont("Andale mono", 30)
    exitText = textFont.render("Press the <ENTER> key to continue", False, RED)
    screen.blit(exitText,(145,400))

def playerSelect():
    #Display elements
    screen.fill(BLACK)
    titleFont = pygame.font.SysFont("Andale mono", 100)
    textFont = pygame.font.SysFont("Andale mono", 30)
    optionFont = pygame.font.SysFont("Andale mono", 50)

    #run menu selection function
    global playerSelectPointer
    playerSelectPointer = menuSelect(2, playerSelectPointer)
    
    title = titleFont.render("Player Select", False, WHITE)
    #logic to determine which option should be highlighted
    if playerSelectPointer == 0:
        onePlayer = optionFont.render("1 player", False, RED)
        twoPlayer = optionFont.render("2 players", False, WHITE)
    elif playerSelectPointer == 1:
        onePlayer = optionFont.render("1 player", False, WHITE)
        twoPlayer = optionFont.render("2 players", False, RED)

    #Check keypresses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        #Make sure variables being changed are global
        global numberOfPlayers
        global gameStage
        if playerSelectPointer == 0:
            numberOfPlayers = 1
            gameStage = "difficulty select"
        elif playerSelectPointer == 1:
            numberOfPlayers = 2
            gameStage = "second player instructions"

    #drawing the text
    screen.blit(title,(50,10))
    screen.blit(onePlayer,(50,200))
    screen.blit(twoPlayer,(400,200))

    pygame.display.update()

    #Set clock speed
    clock.tick(10)
    
def difficultySelect():
    #Display elements
    screen.fill(BLACK)
    titleFont = pygame.font.SysFont("Andale mono", 100)
    textFont = pygame.font.SysFont("Andale mono", 30)
    optionFont = pygame.font.SysFont("Andale mono", 50)

    #run menu selection function
    global difficultySelectPointer
    difficultySelectPointer = menuSelect(3, difficultySelectPointer)
    
    title = titleFont.render("Difficulty Select", False, WHITE)
    #logic to determine which option should be highlighted
    if difficultySelectPointer == 0:
        easy = optionFont.render("easy", False, RED)
        medium = optionFont.render("medium", False, WHITE)
        hard = optionFont.render("hard", False, WHITE)
    elif difficultySelectPointer == 1:
        easy = optionFont.render("easy", False, WHITE)
        medium = optionFont.render("medium", False, RED)
        hard = optionFont.render("hard", False, WHITE)
    elif difficultySelectPointer == 2:
        easy = optionFont.render("easy", False, WHITE)
        medium = optionFont.render("medium", False, WHITE)
        hard = optionFont.render("hard", False, RED)

    #Check keypresses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        #Make sure variables being changed are global
        global difficulty
        global gameStage
        if difficultySelectPointer == 0:
            difficulty = "easy"
        elif difficultySelectPointer == 1:
            difficulty = "medium"
        elif difficultySelectPointer == 2:
            difficulty = "hard"
        gameStage = "gameplay"

    #drawing the text
    screen.blit(title,(50,10))
    screen.blit(easy,(30,200))
    screen.blit(medium,(220,200))
    screen.blit(hard,(520,200))

    pygame.display.update()

    #Set clock speed
    clock.tick(10)

def secondPlayerInstructions():
    #Display elements
    screen.fill(BLACK)
    titleFont = pygame.font.SysFont("Andale mono", 100)
    textFont = pygame.font.SysFont("Andale mono", 30)
    optionFont = pygame.font.SysFont("Andale mono", 50)
    
    title = titleFont.render("instructions", False, WHITE)
    mainText1 = textFont.render("Use the <UP ARROW> and <DOWN ARROW> keys to move your", False, WHITE)
    mainText2 = textFont.render("paddle up and down", False, WHITE)
    exitText = textFont.render("Press the <ENTER> key to continue", False, RED)

    #Check keypresses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        #Make sure variables being changed are global
        global gameStage
        gameStage = "easy map selection"
        
    #drawing the text
    screen.blit(title,(100,10))
    screen.blit(mainText1,(10,150))
    screen.blit(mainText2,(10,180))
    screen.blit(exitText,(10,250))
    pygame.display.update()

    #Set clock speed
    clock.tick(10)

def easyMapSelection():
    #Display elements
    screen.fill(BLACK)
    titleFont = pygame.font.SysFont("Andale mono", 100)
    textFont = pygame.font.SysFont("Andale mono", 30)
    optionFont = pygame.font.SysFont("Andale mono", 50)

    #run menu selection function
    global easyMapSelectionPointer
    easyMapSelectionPointer = menuSelect(3, easyMapSelectionPointer)
    
    title = titleFont.render("Select a map", False, WHITE)
    #logic to determine which option should be highlighted
    if easyMapSelectionPointer == 0:
        map1 = optionFont.render("map 1", False, RED)
        map2 = optionFont.render("map 2", False, WHITE)
        map3 = optionFont.render("map 3", False, WHITE)
    elif easyMapSelectionPointer == 1:
        map1 = optionFont.render("map 1", False, WHITE)
        map2 = optionFont.render("map 2", False, RED)
        map3 = optionFont.render("map 3", False, WHITE)
    elif easyMapSelectionPointer == 2:
        map1 = optionFont.render("map 1", False, WHITE)
        map2 = optionFont.render("map 2", False, WHITE)
        map3 = optionFont.render("map 3", False, RED)

    #Check keypresses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        #Make sure variables being changed are global
        global gameStage
        if easyMapSelectionPointer == 0:
            mapChosen = 1
        elif easyMapSelectionPointer == 1:
            mapChosen = 2
        elif easyMapSelectionPointer == 2:
            mapChosen = 3
        createMap(mapChosen)
        gameStage = "gameplay"

    #drawing the text
    screen.blit(title,(50,10))
    screen.blit(map1,(10,200))
    screen.blit(map2,(200,200))
    screen.blit(map3,(500,200))

    pygame.display.update()

    #Set clock speed
    clock.tick(10)

def fullMapSelection():
    print("working")
    
    
def mainGame():
    #Ensure global variables are used
    global powerUpInPlay
    global player1Score
    global player2Score
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

    global numberOfPlayers
    if numberOfPlayers == 2:
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
    elif numberOfPlayers == 1:
        global difficulty
        global mainBall
        if difficulty == "easy":
            if easyAI(player2.returnY()) == "up":
                player2.moveY(-6)
            elif easyAI(player2.returnY()) == "down":
                player2.moveY(6)
        if difficulty == "medium":
            if mediumAI(mainBall.returnX(), mainBall.returnY(), player2.returnY(), player2.returnWidth(), "right") == "up":
                player2.moveY(-6)
            elif mediumAI(mainBall.returnX(), mainBall.returnY(), player2.returnY(), player2.returnWidth(), "right") == "down":
                player2.moveY(6)
            elif mediumAI(mainBall.returnX(), mainBall.returnY(), player2.returnY(), player2.returnWidth(), "right") == "none":
                player2.moveY(0)
        if difficulty == "hard":
            if hardAI(shadowBall.returnX(), shadowBall.returnY(), player2.returnY(), player2.returnWidth(), "right") == "up":
                player2.moveY(-6)
            elif hardAI(shadowBall.returnX(), shadowBall.returnY(), player2.returnY(), player2.returnWidth(), "right") == "down":
                player2.moveY(6)
            elif hardAI(shadowBall.returnX(), shadowBall.returnY(), player2.returnY(), player2.returnWidth(), "right") == "none":
                player2.moveY(0)

    #Spawning powerups
    spawnChance = random.random()
    if spawnChance < 0.001 and powerUpInPlay == 0:
        powerUp = PowerUp()
        powerUp_group.add(powerUp)
        all_sprites_group.add(powerUp)
        powerUpInPlay = 1
    
    #Collision checking
    player1_ball_hit_group = pygame.sprite.spritecollide(player1, ball_group, False)
    for ball in player1_ball_hit_group:
        if ball.ballType == "normal":
            ball.bounce("right")
            #find and store what direction player 1 is moving
            playerMovement = player1.returnDy()
            ball.changeAngle(playerMovement)
            #Reset shadow ball to normal ball position
            shadowBall.shadowReset(mainBall.angle, mainBall.rect.x, mainBall.rect.y, mainBall.y_direction)



    player2_ball_hit_group = pygame.sprite.spritecollide(player2, ball_group, False)
    for ball in player2_ball_hit_group:
        if ball.ballType == "normal":
            ball.bounce("left")
            #find and store what direction player 2 is moving
            playerMovement = player2.returnDy()
            ball.changeAngle(playerMovement)
            #Reset shadow ball to normal ball position
            shadowBall.shadowReset(mainBall.angle, mainBall.rect.x, mainBall.rect.y, mainBall.y_direction)


    #When a ball hits the powerup
    #Go through all powerups in the powerup group one by one
    for x in powerUp_group:
        #Now that one powerup has been isolated, create another group for that single powerup
        powerUp_hit_group = pygame.sprite.spritecollide(x, ball_group, False)
        #Now going through the newly created group to isolate each ball that has collided with that single powerup
        if x:
            for y in powerUp_hit_group:
                #Find the direction the ball is travelling in
                direction = mainBall.x_direction
                #Reverse the direction (so the power up travels back from where the ball is coming from)
                direction = direction * -1
                powerUp.hit(direction)
                #After the collision, allow another powerup to spawn
                powerUpInPlay = 0

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
    myfont = pygame.font.SysFont("Andale mono", 100)
    textsurface = myfont.render(str(player1Score) + " - " + str(player2Score), False, WHITE)
    screen.blit(textsurface,(270,10))
        
###MAIN LOOP
while not done:
    #Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    if gameStage == "instructions":
        instructions()
    elif gameStage == "player select":
        playerSelect()
    elif gameStage == "watch example gameplay select":
        watchExampleGameplaySelect()
    elif gameStage == "example gameplay":
        exampleGameplay()
    elif gameStage == "difficulty select":
        difficultySelect()
    elif gameStage == "second player instructions":
        secondPlayerInstructions()
    elif gameStage == "easy map selection":
        easyMapSelection()
    elif gameStage == "full map selection":
        fullMapSelection()
    elif gameStage == "gameplay":
        mainGame()

    
    #Flip display
    pygame.display.flip()

    timer += 1
    #Set clock speed
    if difficulty == "easy":
        clock.tick(40)
    if difficulty == "medium":
        clock.tick(60)
    if difficulty == "hard":
        clock.tick(80)
pygame.quit()

