import pygame
import random
import time
pygame.init()

# setup
window = pygame.display.set_mode((500,650))
pygame.display.set_caption("Meteor Dash!")
alienC = pygame.image.load('alienC.png')
meteorS = pygame.image.load('meteorS.png')
bg = pygame.image.load('crispyStars.jpg')
font = pygame.font.SysFont("comicsans", 30, True)
titleFont = pygame.font.SysFont("comicsans", 80, True)
file = open('highScore.txt','r')
highScore = file.read()
file.close()
clock = pygame.time.Clock()
global score
score = 0
lastScore = 0
intro = True


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.hitbox = (self.x, self.y, 64, 64)

    def draw(self, window):
        self.hitbox = (self.x, self.y, 64, 64)
        window.blit(alienC, (self.x,self.y))
        #pygame.draw.rect(window, (0,0,255), self.hitbox, 2)
        
    def hit(self):
        global highScore
        global lastScore
        global intro
        global score
        print("you died")
        fontDeath = pygame.font.SysFont('comicsans', 100)
        textDeath = fontDeath.render('You Died!!', 1, (255,0,0))
        window.blit(textDeath, (250 - (textDeath.get_width()/2), 200))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
        highScore = int(highScore)
        if score > highScore:
            file = open('highScore.txt','w')
            file.write(str(score))
            print("New high score")
            highScore = score
            file.close()
        intro = True
        lastScore = score
        homeScreen()

class projectile(object):
    def __init__(self, x, y, radius, color, vel):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel= vel

    def draw(self, window):
        window.blit(meteorS, (self.x,self.y))
        #pygame.draw.circle(window, self.color, (self.x + 32, self.y + 32), self.radius, 2)


def button(text,x,y,width,height,action):
    global intro
    global score
    global upTime
    global speed
    global level
    global run
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    playText = font.render(text, False, (255,255,255),20) 
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        playText = font.render(text, False, (255,0,0), 20)
        if click[0] == 1:
            if action == "play":
                intro = False
                score = 0
                upTime = 0
                speed = 1
                level = 0

            elif action == "exit":
                intro = False
                run = False
        
    window.blit(playText, ((250 - playText.get_width()/2),y))    # text, (x,y)
    #pygame.draw.rect(window, (255,0,0), ((250 - playText.get_width()/2),y,width,height), 0)


def homeScreen():
    global intro
    global score
    global highScore
    global lastScore
    global run
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                run = False

        window.blit(bg, (0,0))       
        titleText = titleFont.render("Meteor Dash!", False, (255,0,0), 20)
        window.blit(titleText, (250 - titleText.get_width()/2,200))
        button("Play",200,400,50,20,"play")
        button("Exit",200,450,100,20,"exit")
        high = font.render("High Score: " + str(highScore), False, (255,255,255), 20)
        previousScore = font.render("Previous Score: " + str(lastScore), False, (255,255,255), 20)
        window.blit(previousScore, (10, 30))
        window.blit(high, (10,10))
        pygame.display.update()


def levelUp():
    global speed
    global level
    global upTime
    if upTime <= 0:
        speed = 1
        
    elif upTime <= 3:
        speed = 2

    elif upTime <= 6:
        speed = 3
        level = 1   # (level 2, working with computers here Angus, they have no brain remember...)

    elif upTime <= 10:    # make all this nonsens a class or definition loop for goodness sake!!!!!
        speed = 4

    elif upTime <= 20:
        speed = 5
        level = 2

    elif upTime <= 30:
        level = 3

    elif upTime <= 40:
        level = 4

    elif upTime <= 60:
        level = 5
        speed = 6

    elif upTime <= 90:
        level = 5
        speed = 7

    elif upTime <= 120:
        level = 6
        speed = 7

    elif upTime <= 150:
        level = 7
        speed = 8

    elif upTime <= 180:
        level = 8
        speed = 9

    elif upTime > 210:
        if str(level)[-1] == "0":
            choice = random.randint(1,2)
            if choice == 1:
                speed += 1
            else:
                level += 1

        
def redrawGameWindow():
    global highScore
    global score
    window.blit(bg, (0,0))
    textScore = font.render("Score: " + str(score), 1, (255,255,255))
    if int(score) <= int(highScore):
        textHighScore = font.render("High Score: " + str(highScore), 1, (255,255,255))
    else:
        textHighScore = font.render("High Score: " + str(score), 1, (255,255,0))
    window.blit(textScore, (10, 10))
    window.blit(textHighScore, (10, 30))
    alien.draw(window)

    for meteor in meteors:
        meteor.draw(window)
        
    pygame.display.update()


# mainloop
alien = player(250, 550, 64, 64)
meteors = []
upTime = 0
level = 0
speed = 1
run = True

while run:
    clock.tick(144)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if len(meteors) > 0:
        for meteor in meteors:
            meteor.y += meteor.vel
            if meteor.y > 650:
                meteors.pop(0)
                upTime += 1
                levelUp()
        
            if (meteor.y + 32) - meteor.radius < alien.hitbox[1] + alien.hitbox[3] and (meteor.y + 32) + meteor.radius > alien.hitbox[1]:
                if (meteor.x + 32) + meteor.radius > alien.hitbox[0] and (meteor.x + 32) - meteor.radius < alien.hitbox[0] + alien.hitbox[2]:
                    meteors.pop(meteors.index(meteor))
                    meteors.clear()
                    alien.hit()

    if len(meteors) <= level:
        if random.randint(1, 75) == 1:
            meteors.append(projectile(random.randint(1,436), -64, 32, (255,0,0), speed))

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and alien.x > alien.vel:
        alien.x -= alien.vel
        
    if keys[pygame.K_RIGHT] and alien.x < 500 - alien.width - alien.vel :
        alien.x += alien.vel

    score = upTime
    redrawGameWindow()
    homeScreen()
  
pygame.quit()
