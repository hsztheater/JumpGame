import pgzrun
import random
from pgzhelper import *

# Joystick init
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

# Screen dimensions and title
TITLE = "Hoydepunkt Run"
WIDTH = 800
HEIGHT = 600

# Music
music.play("go")
music.set_volume(0.3)

# Scrolling Background
BACKGROUND0 = 'sky1'
BACKGROUND1 = 'sky2'
BACKGOUND_TIME = 12.0

back0 = Actor(BACKGROUND0, (800, 600))
back1 = Actor(BACKGROUND1, (800, 600))
g_backgrounds = [back0, back1]

# Physic
velocity = 0
gravity = 0.8

# Score
score = 0
score_win = 50

# Init
losesound = False
winsound = False
STARTED = False
END = False
WIN = False
MENU = True

# Coin Collectible
coin = Actor("coin1")
coin.scale = 0.5
coin.x = random.randint(900, 2000)
coin.y = random.randint(350, 475)
coin.fps = 6
coin.images = ["coin1", "coin2", "coin3", "coin4"]

# Player
player = Actor("player1")
player.scale = 0.5
player.x = 200
player.y = 525
player.fps = 12
player.images = ["player1", "player2", "player3"]

# Clouds
clouds = Actor("cloud")
clouds.scale = 0.2
clouds.x = random.randint(900, 1500)
clouds.y = random.randint(50, 150)
clouds.images = ["cloud"]


# QR
qr = Actor("testqr")
qr.scale = 0.2
qr.x = WIDTH / 2
qr.y = HEIGHT / 2

# Obstacles
obstacles = []
obstacles_timeout = 0

###########################################################################################


def update():

    global velocity, obstacles_timeout, END, losesound, winsound, score, WIN, MENU
    if END:
        score = 0
        losesound = False
        winsound = False
        gameover()

    elif WIN:
        score = 0
        losesound = False
        winsound = False
        win()

    elif STARTED:
        coin.animate()
        player.animate()
        if END == False:
            coin.x -= 6
            clouds.x -= 3
        if coin.x < -50:
            coin.x = random.randint(900, 2000)
            coin.y = random.randint(370, 475)
        if clouds.x < -150:
            clouds.x = random.randint(900, 1500)
            clouds.y = random.randint(50, 150)


        ######Collision and score update#####
        if player.colliderect(coin):
            sounds.collect.play()
            score += 5
            coin.x = random.randint(900, 2000)
            coin.y = random.randint(370, 420)

        ######Player physic#####
        if pygame.joystick.Joystick(0).get_button(1) and player.y == 525:
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
            obstacle = Actor("obstacle")
            obstacle.scale = 0.5
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
                sounds.lose.play()
                losesound = True

        if score >= score_win:
            WIN = True
            if winsound == False:
                sounds.win.play()
                winsound = True
            if music.is_playing("go"):
                music.pause()

    else:  # Just display the intro screen
        menu()


def menu():
    global STARTED
    global END
    music.unpause()
    if pygame.joystick.Joystick(0).get_button(9):
        STARTED = True
        END = False


def gameover():
    global STARTED
    global END
    if pygame.joystick.Joystick(0).get_button(9):
        STARTED = True
        END = False


def win():
    global STARTED
    global WIN
    global END
    global MENU

    STARTED = False
    END = False
    WIN = True

    if pygame.joystick.Joystick(0).get_axis(4) == -1 and pygame.joystick.Joystick(0).get_button(8):
        WIN = False
        MENU = True

def background_repeat():
    b0 = g_backgrounds.pop(0)
    g_backgrounds.append(b0)
    scroll_backgrounds(g_backgrounds)
    return

def scroll_backgrounds(backs):
    left = 400
    bottom = 300
    b0, b1 = backs

    b0.pos = (left, bottom)
    animate(b0,
        tween= 'linear',
        duration= BACKGOUND_TIME,
        on_finished= background_repeat,
        pos= (left - 800, bottom))

    b1.pos = (left + 800, bottom)
    animate(g_backgrounds[1],
        tween= 'linear',
        duration= BACKGOUND_TIME,
        on_finished= None,
        pos= (left, bottom))

scroll_backgrounds(g_backgrounds)

##############################################DRAW#################################################


def draw():
    screen.clear()
    #screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    b0, b1 = g_backgrounds
    b0.draw()
    b1.draw()

    if END:
        draw_gameover()

    elif WIN:
        draw_win()

    elif STARTED:
        screen.draw.filled_rect(Rect(0, 550, 800, 50), "grey")
        player.draw()
        coin.draw()
        clouds.draw()

        for obstacle in obstacles:
            obstacle.draw()

        screen.draw.text(
            "Score: " + str(score),
            (20, 20),
            color="white",
            shadow=(1, 1),
            fontname="pixeloidsansbold",
            fontsize=30,
        )
        screen.draw.text(
            "HighScore: 850 - Anders",
            (330, 20),
            color="white",
            shadow=(1, 1),
            fontname="pixeloidsansbold",
            fontsize=30,
        )

    else:  # Just display the intro screen
        draw_menu()


def draw_menu():
    screen.draw.text(
        "Super Jump Lady 7",
        centerx=400,
        centery=100,
        shadow=(1, 1),
        color="white",
        fontname="pixeloidsansbold",
        fontsize=60,
    )
    screen.draw.text(
        "Press START",
        centerx=400,
        centery=300,
        shadow=(1, 1),
        color="white",
        fontname="pixeloidsansbold",
        fontsize=40,
    )
    screen.draw.text(
        "Reach " + str(score_win) + " points for a surprise!",
        centerx=400,
        centery=370,
        shadow=(1, 1),
        color="white",
        fontname="pixeloidsansbold",
        fontsize=20,
    )


def draw_gameover():
    screen.draw.text(
        "Game Over :(",
        centerx=400,
        centery=300,
        shadow=(1, 1),
        color="white",
        fontname="pixeloidsansbold",
        fontsize=80,
    )
    screen.draw.text(
        "Press START to retry",
        centerx=400,
        centery=370,
        shadow=(1, 1),
        color="white",
        fontname="pixeloidsansbold",
        fontsize=40,
    )


def draw_win():
    screen.draw.text(
        "SCAN ME",
        centerx=WIDTH/2,
        centery=100,
        shadow=(1, 1),
        color="white",
        fontname="pixeloidsansbold",
        fontsize=40,
    )
    screen.draw.text(
        "SCAN ME",
        centerx=WIDTH/2,
        centery=500,
        shadow=(1, 1),
        color="white",
        fontname="pixeloidsansbold",
        fontsize=40,
    )
    qr.draw()
