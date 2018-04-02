import pygame

pygame.init()

window_height = 1024
window_width = 577

window = pygame.display.set_mode((window_height, window_width))

pygame.display.set_caption('Winter Olympics - Brawlers')

# Example of putting images in a separate folder
# pygame.image.load(pygame.path.join('pics','R1.png'))

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
pikaRight = [pygame.image.load('pikaRight.png')]
pikaLeft = [pygame.image.load('pikaLeft.png')]
bg = pygame.image.load('winter.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

class player:

    def __init__(self, x, y, width, height):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 20, self.y, 28, 60)

    def draw(self,window, pika):

        if pika:
            

            if self.walkCount + 1 >= 27:
            
                self.walkCount = 0

            if not(self.standing):

                if self.left:

                    window.blit(pikaLeft[0], (self.x, self.y))
                    self.walkCount += 1

                elif self.right:

                    window.blit(pikaRight[0], (self.x, self.y))
                    self.walkCount += 1

            else:

                if self.right:

                    window.blit(walkRight[0], (self.x, self.y))

                else:

                    window.blit(walkLeft[0], (self.x, self.y))

            self.hitbox = (self.x + 20, self.y, 28, 60)

        else:

            if self.walkCount + 1 >= 27:
        
                self.walkCount = 0

        if not(self.standing):

            if self.left:

                window.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1

            elif self.right:

                window.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1

        else:

            if self.right:

                window.blit(walkRight[0], (self.x, self.y))

            else:

                window.blit(walkLeft[0], (self.x, self.y))

        self.hitbox = (self.x + 20, self.y, 28, 60)
    
    def hit(self):

        self.x += 50

class projectile:

    def __init__(self, x, y, radius, colour, facing):

        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour 
        self.facing = facing
        self.speed = 8 * facing

    def draw(self,window):

        pygame.draw.circle(window, self.colour, (self.x,self.y), self.radius)

class platform:

    def __init__(self, x, y, width, height, colour):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour

    def draw(self, window):

        pygame.draw.rect(window, self.colour, (self.x,self.y,self.width,self.height), 1)

def redrawGameWindow():

    global walkCount

    # Applying background adds lag to game
    window.blit(bg, (0,0))
    # window.fill((255,0,0))

    platform.draw(window)

    man.draw(window, False)
    anti_man.draw(window, True)

    for bullet in bullets:

        bullet.draw(window)
        
    pygame.display.update()
    
platform = platform(100, 365, 800, 10, (60,200,200))
man = player(300, 301, 64, 64)
anti_man = player(400, 301, 64, 64)
bullets = []
shootLoop = 0

run = True

while run:

    clock.tick(40)

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            run = False

    # for bullet in bullets:

    #     if bullet.x < 1024 and bullet.x > 0:

    #         bullet.x += bullet.speed

    #     else:

    #         bullets.pop(bullets.index(bullet))
        
    #     if bullet.x == anti_man.hitbox[0] or bullet.y == anti_man.hitbox[1]:
        
    #         anti_man.x += 20

    #     if bullet.x == man.hitbox[0] or bullet.y == man.hitbox[1]:
        
    #         man.x += 20

    for bullet in bullets:
        if bullet.y - bullet.radius < anti_man.hitbox[1] + anti_man.hitbox[3] and bullet.y + bullet.radius > anti_man.hitbox[1]:
            if bullet.x + bullet.radius > anti_man.hitbox[0] and bullet.x - bullet.radius < anti_man.hitbox[0] + anti_man.hitbox[2]:
                anti_man.hit()
                bullets.pop(bullets.index(bullet))
                
        if bullet.x < 1024 and bullet.x > 0:
            bullet.x += bullet.speed
        else:
            bullets.pop(bullets.index(bullet))
        
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:

        if man.left:

            facing = -1

        else:

            facing = 1

        if len(bullets) < 100:

            bullets.append(projectile(int(man.x + man.width // 2), int(man.y + man.height // 2), 6, (255,255,255), facing))

        shootLoop = 1
            
    if keys[pygame.K_LEFT] and man.x > man.speed:

        man.x -= man.speed
        man.left = True
        man.right = False
        man.standing = False

    elif keys[pygame.K_RIGHT] and man.x < window_height - man.width - man.speed:

        man.x += man.speed
        man.left = False
        man.right = True
        man.standing = False

    else:

        man.standing = True
        man.walkCount = 0

    if not(man.isJump):

##        if keys[pygame.K_UP] and character_y > character_speed:
##
##            character_y -= character_speed
##
##        if keys[pygame.K_DOWN] and character_y < window_height - character_height - character_speed :
##
##            character_y += character_speed
##
##        if keys[pygame.K_SPACE]:
##
##            isJump = True

        if keys[pygame.K_UP]:

            man.isJump = True
            man.left = False
            man.right = False
            man.walkCount = 0

    else:

        if man.jumpCount >= -10:

            neg = 1

            if man.jumpCount < 0:

                neg = -1

            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1

        else:

            man.isJump = False
            man.jumpCount = 10

    if man.hitbox[0] + 28 < 112 or man.hitbox[0] > 912:

        man.y += 5

    elif man.hitbox[0] + 28 > 112 or man.hitbox[0] < 912:

        if man.isJump and man.hitbox[1] < 400:

            pass

        elif man.isJump and man.hitbox[1] > 400:

            man.y += 5

        elif not(man.isJump) and man.hitbox[1] < 400:

            man.hitbox = 400

        elif not(man.isJump) and man.hitbox[1] > 410:

            man.y += 5

    # Player 2 begins

    if keys[pygame.K_y]:

        if anti_man.left:

            facing = -1

        else:

            facing = 1

        if len(bullets) < 2:

            bullets.append(projectile(int(anti_man.x + anti_man.width // 2), int(anti_man.y + anti_man.height // 2), 6, (255,255,255), facing))
            
    if keys[pygame.K_a] and anti_man.x > anti_man.speed:

        anti_man.x -= anti_man.speed
        anti_man.left = True
        anti_man.right = False
        anti_man.standing = False

    elif keys[pygame.K_d] and anti_man.x < window_height - anti_man.width - anti_man.speed:

        anti_man.x += anti_man.speed
        anti_man.left = False
        anti_man.right = True
        anti_man.standing = False

    else:

        anti_man.standing = True
        anti_man.walkCount = 0

    if not(anti_man.isJump):

##        if keys[pygame.K_UP] and character_y > character_speed:
##
##            character_y -= character_speed
##
##        if keys[pygame.K_DOWN] and character_y < window_height - character_height - character_speed :
##
##            character_y += character_speed
##
##        if keys[pygame.K_SPACE]:
##
##            isJump = True

        if keys[pygame.K_w]:

            anti_man.isJump = True
            anti_man.left = False
            anti_man.right = False
            anti_man.walkCount = 0

    else:

        if anti_man.jumpCount >= -10:

            neg = 1

            if anti_man.jumpCount < 0:

                neg = -1

            anti_man.y -= (anti_man.jumpCount ** 2) * 1 * neg
            anti_man.jumpCount -= 1

        else:

            anti_man.isJump = False
            anti_man.jumpCount = 10

    if anti_man.hitbox[0] + 28 < 112 or anti_man.hitbox[0] > 912:

        anti_man.y += 5

    elif anti_man.hitbox[0] + 28 > 112 or anti_man.hitbox[0] < 912:

        if anti_man.isJump and anti_man.hitbox[1] < 400:

            pass

        elif anti_man.isJump and anti_man.hitbox[1] > 400:

            anti_man.y += 5

        elif not(anti_man.isJump) and anti_man.hitbox[1] < 400:

            anti_man.hitbox = 400

        elif not(anti_man.isJump) and anti_man.hitbox[1] > 410:

            anti_man.y += 5

    redrawGameWindow()

pygame.quit()
