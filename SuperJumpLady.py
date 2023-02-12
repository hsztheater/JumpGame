import pgzrun
import random
from pgzhelper import *

# Screen dimensions and title
TITLE = "SuperJumpLady"
WIDTH = 800
HEIGHT = 600
music.play('go')
music.set_volume(.3)

velocity = 0
gravity = 0.9

score = 0
score_win = 20
code = 1234

losesound = False
STARTED = False
END = False
WIN = False
MENU = True

USED_PRESSED_SPACE = False

# Coin Collectible
coin = Actor("coin1")
coin.scale = 0.5
coin.x = random.randint(900, 2000)
coin.y = random.randint(350, 450)
coin.fps = 6
coin.images = ["coin1", "coin2", "coin3", "coin4"]

# Player
player = Actor("player")
player.scale = 0.5
player.x = 200
player.y = 525

# Obstacles
obstacles=[]
obstacles_timeout = 0

###########################################################################################

def update():
    global velocity, obstacles_timeout, code, END, losesound, score, WIN, MENU
    
    if !keyboard[keys.SPACE]:
        clear_used_pressed _space()
    
    if END:
        score = 0
        gameover()

    elif WIN:
        score = 0
        win()

    elif STARTED:
    ######Collectibles#####
        coin.animate()
        coin.x -= 5
        if coin.x < -50:
            coin.x = random.randint(900, 2000)
            coin.y = random.randint(350, 450)

        ######Collision and score update#####
        if player.colliderect(coin):
            sounds.collect.play()
            score += 5
            coin.x = random.randint(900, 2000)
            coin.y = random.randint(350, 450)

        ######Player physic#####
        if keyboard.up and player.y == 525:
            sounds.jump.play()
            velocity = -15
        player.y += velocity
        velocity += gravity

        if player.y > 525:
            velocity = 0
            player.y = 525

        ######Obstacles#####
        obstacles_timeout += 1
        if obstacles_timeout > random.randint(60, 7000):
            obstacle = Actor('obstacle')
            obstacle.scale = .3
            obstacle.x = 800
            obstacle.y = 525
            if END == False:
                obstacles.append(obstacle)
                obstacles_timeout = 0

        ######Move obstacles#####
        for obstacle in obstacles:
            obstacle.x -= 8
            if obstacle.x < -50:
                obstacles.remove(obstacle)
                score += 5

        ######Collision obstacle#####
        if player.collidelist(obstacles) != -1:
            END = True
            obstacles.remove(obstacle)
            if losesound == False:
                sounds.blow.play()
                losesound = True

        ######Win condition#####
        if score >= score_win:
            WIN = True

    else:  # Just display the intro screen
        menu()


def menu():
    global STARTED
    if !space_has_been_used() && keyboard[keys.SPACE]:
        set_used_pressed_space()
        STARTED = True

def gameover():
    global STARTED
    global END
    if !space_has_been_used() && keyboard[keys.SPACE]:
        set_used_pressed_space()
        STARTED = True
        END = False

def win():
    global STARTED
    global WIN
    global END
    global MENU
    if !space_has_been_used() && keyboard[keys.SPACE]:
        set_used_pressed_space()
        STARTED = False
        END = False
        WIN = False
        MENU = True

def space_has_been_used():
    global USED_PRESSED_SPACE
    return USED_PRESSED_SPACE
        
def set_used_pressed_space():
    global USED_PRESSED_SPACE
    USED_PRESSED_SPACE = True

def clear_used_pressed_space():
    global USED_PRESSED_SPACE
    USED_PRESSED_SPACE = False

##############################################DRAW#################################################

def draw():
    screen.clear
    #screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN) #Remove the # to make it fullscreen, ctrl Q to quit
    screen.blit("sky", (0, 0))

    if END:
        draw_gameover()

    elif WIN:
        draw_win()

    elif STARTED:
        screen.draw.filled_rect(Rect(0, 550, 800, 50), 'grey')
        player.draw()
        coin.draw()

        for obstacle in obstacles:
            obstacle.draw()

        screen.draw.text('Score:' + str(score), (20, 20), color = 'white', fontname = 'pixeloidsansbold', fontsize = 30)

    else:  # Just display the intro screen
        draw_menu()


def draw_menu():
    screen.draw.text('Super Jump Lady 7', centerx = 400, centery = 100, shadow = (1,1), color = 'white', fontname = 'pixeloidsansbold', fontsize = 60)
    screen.draw.text('Press Space to start', centerx = 400, centery = 300, color ='white', fontname = 'pixeloidsansbold', fontsize = 40)
    screen.draw.text('Reach ' + str(score_win) + ' points for a surprise!', centerx = 400, centery = 370, color ='white', fontname = 'pixeloidsansbold', fontsize = 20)

def draw_gameover():
    screen.draw.text('Game Over :(', centerx = 400, centery = 300, shadow = (1,1), color ='white', fontname = 'pixeloidsansbold', fontsize = 80)
    screen.draw.text('Press Space to retry', centerx = 400, centery = 370, color ='white', fontname = 'pixeloidsansbold', fontsize = 40)


def draw_win():
    screen.draw.text('Yay! The code is ' + str(code), centerx = 400, centery = 300, shadow = (1,1), color ='white', fontname = 'pixeloidsansbold', fontsize = 50)
    screen.draw.text('Press Space to retry', centerx = 400, centery = 370, color ='white', fontname = 'pixeloidsansbold', fontsize = 40)
