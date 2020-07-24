import pygame
import random
from backend import leaderboard
from backend.table import Table
from backend.input_box import InputBox
from backend.timer import Timer
from backend.engine import Engine
from backend.object import Object
from backend.text import Text
from backend.audio import Audio
from backend.button import Button

#####################################
######### Constants  ################
#####################################

COLLUMNS = 4
ROWS = 2
FIRSTENEMYYPOS = 100
FIRSTENEMYXPOS = 100
XDISTANCEBETWEENENEMIES = 75
YDISTANCEBETWEENENEMIES = 50

PLAYERXSPEED = 200

STARTINGNUMOFHEARTS = 3
STARTINGXPOS = 758
STARTINGYPOS = 10
XDISTACEBETWEENHEARTS = 40

MINTIMETOSPAWN_P_UP = 6
MAXTIMETOSPAWN_P_UP = 12

MAXROWS_O_ENEMIES = 5

MAXCOLUMNS_O_ENEMIES = 8

TIMEBETWEENWAVE = 0.5

AMMO_P_TIME = 2

MINTIMETODROPBOMB = 4
MAXTIMETODROPBOMB = 8

WINDOWSWIDTH = 800

POWERUPSPEED = 100

BOMBSPEED = 350

ENEMYXSPEED = 50

COLLUMSOFENEMIESADDER = 0.25

ROWSOFENEMIESADDER = 0.25

ENEMYYSPEED = 40

BULLETSPEED = 400

SCALEFACTOR = 0.5
#####################################
######### Global Varibale ###########
#####################################

columns_of_enemies_multiplier = 1.0

rows_of_enemies_multiplier = 1.0

score = 0

enemy_dir = 1

enemies = []

bombs = []

bullets = []

hearts = []

ammo_collected = False

can_shoot = True

powerup_types = ["heart", "ammo", "speed"]

powerups = []

powerup_timer = None

speed_collected = False
speed_powerup_time = 5


player = None
score_text = None

leaderboard_text = None

leaderboard_table = None

username = None
#####################################
######### FUNCTIONS #################
#####################################


def start_game():
    global player, score_text, username
    space_invaders_text.destroy()
    play_button.destroy()
    username = username_input_box.text
    username_input_box.destroy()
    engine.set_background("images/background.png")
    background_music = Audio("audio/background.wav", True, True, 0.15)

    player = Object("images/spaceship.png", 400-32, 450, 0.5)

    create_hearts(STARTINGNUMOFHEARTS)

    score_text = Text("Score: " + str(score))
    engine.on_key_pressed(pygame.K_SPACE, fire_bullet)

    engine.on_key_down(pygame.K_a, move_left)
    engine.on_key_down(pygame.K_d, move_right)

    create_powerup_timer()

    spawn_enemies()


def try_again():
    global score, rows_of_enemies_multiplier, columns_of_enemies_multiplier
    rows_of_enemies_multiplier = 1.0
    columns_of_enemies_multiplier = 1.0
    spawn_enemies()
    score = 0
    score_text.change_text("Score: " + str(score))
    create_hearts(STARTINGNUMOFHEARTS)
    create_powerup()
    leaderboard_text.destroy()
    leaderboard_table.destroy()


def beat_wave():
    global columns_of_enemies_multiplier, rows_of_enemies_multiplier
    columns_of_enemies_multiplier += COLLUMSOFENEMIESADDER
    rows_of_enemies_multiplier += ROWSOFENEMIESADDER
    engine.add_timer(TIMEBETWEENWAVE, spawn_enemies)


def create_hearts(num_of_hearts):
    global hearts
    reset_hearts()
    for i in range(num_of_hearts):
        heart = Object("images/heart.png", STARTINGXPOS -
                       XDISTACEBETWEENHEARTS * i, STARTINGYPOS)
        hearts.append(heart)


def reset_hearts():
    global hearts
    for heart in hearts:
        heart.destroy()
        heart = None
    hearts = []


def create_powerup():
    random_powerup_index = random.randint(0, len(powerup_types) - 1)
    random_powerup_type = powerup_types[random_powerup_index]
    random_x = random.random() * WINDOWSWIDTH - 64
    if random_powerup_type == "heart":
        heart = Object("images/heart.png", x=random_x, y=0, scale=1.5)
        powerups.append(heart)
        engine.on_collision(heart, player, heart_player_colllision)
    elif random_powerup_type == "ammo":
        ammo = Object("images/ammo.png", x=random_x, y=0, scale=1.5)
        powerups.append(ammo)
        engine.on_collision(obj_1=ammo, obj_2=player,
                            handler=ammo_player_collision)
    elif random_powerup_type == "speed":
        speed = Object("images/speed.png", x=random_x, y=0, scale=1.5)
        powerups.append(speed)
        engine.on_collision(speed, player, speed_player_collision)
    create_powerup_timer()


def set_speed_to_false():
    global speed_collected
    speed_collected = False


def speed_player_collision(speed, player):
    global speed_collected
    powerups.remove(speed)
    speed.destroy()
    speed = None
    speed_collected = True
    engine.add_timer(speed_powerup_time, set_speed_to_false)


def ammo_player_collision(ammo, player):
    global powerups, ammo_collected
    powerups.remove(ammo)
    ammo.destroy()
    ammo = None
    ammo_collected = True
    engine.add_timer(AMMO_P_TIME, set_ammo_to_false)


def set_ammo_to_false():
    global ammo_collected
    ammo_collected = False


def create_powerup_timer():
    global powerup_timer
    random_powerup_time = random.random() * (MAXTIMETOSPAWN_P_UP -
                                             MINTIMETOSPAWN_P_UP) + MINTIMETOSPAWN_P_UP
    powerup_timer = Timer(random_powerup_time, create_powerup)
    engine.add_timer_instance(powerup_timer)


def heart_player_colllision(heart, player):
    global powerups
    powerups.remove(heart)
    heart.destroy()
    heart = None
    create_hearts(len(hearts)+1)


def subtract_heart():
    global hearts
    last_heart = hearts.pop()
    last_heart.destroy()
    last_heart = None

    if len(hearts) == 0:
        game_over()


def game_over():
    global enemies, bombs, bullets, powerups, leaderboard_table, leaderboard_text
    for enemy1 in enemies:
        enemy1.destroy()
    enemies = []
    for bomb in bombs:
        bomb.destroy()
    bombs = []
    for bullet in bullets:
        bullet.destroy()
    bullets = []
    for powerup in powerups:
        powerup.destroy()
    powerups = []
    reset_powerup_timer()
    try_again_button = Button(pos_x=300, pos_y=275, width=200, height=50, handler=try_again,
                              text="Try Again", font_size=32, hidden=False, font_color=(0, 0, 0),
                              button_color=(255, 255, 255), hover_color=(211, 211, 211), destroy_on_click=True)
    leaderboard.save_score(username, score)
    leaderboard_text = Text(
        text="Leaderboard", x_position=200, y_position=10, size=60)
    leaderboard_table = Table(x=200, y=100, columns=3, column_width=[100, 200, 125],
                              row_height=35, background_color=(255, 255, 255), font_color=(0, 0, 0), font_size=24)
    leaderboard_table.add_row([" Rank", "Username", "Score"])
    results = leaderboard.get_scores()
    rank = 1
    for result in results:
        leaderboard_table.add_row(
            [" "+str(rank), result['username'], str(result['score'])])
        rank = rank+1


def reset_powerup_timer():
    global powerup_timer
    if powerup_timer is not None:
        powerup_timer.stop()
        powerup_timer = None


def player_enemy_collision(player, enemy):
    subtract_heart()


def drop_bomb(enemy):
    if not enemy.destroyed:
        bomb = Object("images/bomb.png", enemy.pos_x, enemy.pos_y)
        bombs.append(bomb)
        engine.on_collision(bomb, player, bomb_player_collision)
        set_timer_to_drop_bomb(enemy)


def bomb_player_collision(bomb, player):
    global score
    global bombs
    bombs.remove(bomb)
    bomb.destroy()
    bomb = None
    Audio("audio/explosion.wav", False, True, 0.20)
    subtract_heart()


def set_timer_to_drop_bomb(enemy):
    random_time = (random.random() * (MAXTIMETODROPBOMB -
                                      MINTIMETODROPBOMB)) + MINTIMETODROPBOMB
    engine .add_timer(random_time, drop_bomb, enemy)


def spawn_enemies():
    columns_of_enemies = (int(COLLUMNS * columns_of_enemies_multiplier))
    if columns_of_enemies > MAXCOLUMNS_O_ENEMIES:
        columns_of_enemies = MAXCOLUMNS_O_ENEMIES
    rows_of_enemies = (int(ROWS * rows_of_enemies_multiplier))
    if rows_of_enemies > MAXROWS_O_ENEMIES:
        rows_of_enemies = MAXROWS_O_ENEMIES
    for row in range(rows_of_enemies):
        for column in range(columns_of_enemies):
            enemy = Object("images/ufo.png", FIRSTENEMYXPOS +
                           column * XDISTANCEBETWEENENEMIES, FIRSTENEMYYPOS + row * YDISTANCEBETWEENENEMIES, scale=SCALEFACTOR)
            enemies.append(enemy)
            set_timer_to_drop_bomb(enemy)
            engine.on_collision(player, enemy, player_enemy_collision)

# move the player left


def move_left():
    player.pos_x -= get_current_speed() * engine.delta_time

    if player.pos_x < 0:
        player.pos_x = 0

# move the player right


def move_right():
    player.pos_x += get_current_speed() * engine.delta_time

    if player.pos_x > 736:
        player.pos_x = 736


def get_current_speed():
    current_speed = PLAYERXSPEED
    if speed_collected:
        current_speed = PLAYERXSPEED * 2
    return current_speed


def bullet_enemy_collision(bullet, enemy):
    global score
    bullets.remove(bullet)
    bullet.destroy()
    enemies.remove(enemy)
    enemy.destroy()
    enemy = None
    explosion_sound = Audio("audio/explosion.wav", False, True, 0.20)
    score += 1
    score_text.change_text("Score: " + str(score))
    if len(enemies) is 0:
        beat_wave()


def set_can_shoot_to_true():
    global can_shoot

    can_shoot = True


def fire_bullet():
    global can_shoot
    if can_shoot or ammo_collected:
        bullet = Object("Images/bullet.png", player.pos_x +
                        16, player.pos_y - 32, scale=SCALEFACTOR)
        bullets.append(bullet)
        laser_sound = Audio("audio/laser.wav", False, True, 0.15)
        for enemy in enemies:
            engine.on_collision(bullet, enemy, bullet_enemy_collision)
        can_shoot = False
        engine.add_timer(0.5, set_can_shoot_to_true)


def update():
    global enemy_dir

    at_left_boundary = False
    at_right_boundary = False

    for enemy in enemies:
        enemy.pos_x += ENEMYXSPEED * enemy_dir * engine.delta_time
        if enemy.pos_x < 0:
            at_left_boundary = True

        if enemy.pos_x > 736:
            at_right_boundary = True

    if at_left_boundary:
        enemy_dir = 1

    if at_right_boundary:
        enemy_dir = -1

    for enemy in enemies:
        if at_left_boundary or at_right_boundary:
            enemy.pos_y += ENEMYYSPEED
            if enemy.pos_y - enemy.height < 0:
                game_over()

    # move bullets up
    for bullet in bullets:
        bullet.pos_y -= BULLETSPEED * engine.delta_time

    for bomb in bombs:
        bomb.pos_y += BOMBSPEED * engine.delta_time

    for powerup in powerups:
        powerup.pos_y += POWERUPSPEED * engine.delta_time


#####################################
######### GAME SETUP ################
#####################################
leaderboard.join_leaderboard("smellcheese123")

engine = Engine()
engine.create_screen(800, 600)
engine.set_name("Space Invaders")
engine.set_background("images/space.jpg")
space_invaders_text = Text(text="SPACE INVADERS", x_position=115, y_position=100,
                           size=64)
play_button = Button(pos_x=350, pos_y=450, width=100, height=50, handler=start_game,
                     text="PLAY", font_size=32, hidden=False, font_color=(0, 0, 0),
                     button_color=(255, 255, 255), hover_color=(211, 211, 211), destroy_on_click=False)
username_input_box = InputBox(
    x=275, y=350, width=250, height=37.5, text="username", enter_handler=start_game)
engine.start(update)
