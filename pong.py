import pygame
#

#
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 0)

#
pygame.init()

#
size = (640, 480)

screen = pygame.display.set_mode(size)
#

pygame.display.set_caption("Snow")
#

done = False
#
x_val = 150
y_val = 200

x_padd = 0
y_padd = 20

x_direction = 1
y_direction = 1

clock = pygame.time.Clock()

###
while not done:
    #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
            
        #
    #
    #
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and y_padd > 0:
        y_padd = y_padd - 5
    if keys[pygame.K_DOWN] and y_padd < 420:
        y_padd = y_padd + 5
    
    if x_val > 620:
        x_direction = -1

    if x_val < 0:
        x_val = 150
        y_val = 200
        x_direction = 1
        y_direction = 1
        
    if y_val < 0 or y_val > 460:
        y_direction = y_direction * -1

    #collision with paddle
    if x_val < 15 and y_val > y_padd and y_val < y_padd + 60:
        x_direction = 1
        
    x_val = x_val + x_direction
    y_val = y_val + y_direction
    #
    screen.fill(BLACK)
    #
    pygame.draw.rect(screen, BLUE, (x_val, y_val, 20, 20))
    pygame.draw.rect(screen, WHITE, (x_padd, y_padd, 15, 60))
    #
    pygame.display.flip()
    #
    clock.tick(60)
    #
pygame.quit()
