import pygame
import os
pygame.font.init()
# Lengths of the window. they are with big letters, because they are constant!
WIDTH, HEIGHT = 900, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My first game!")

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60
MAX_BULLETS = 5
MOVE = 6
BULLET_MOVE = 8  # it should be faster than a spaceship
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
SPACESHIP_SIZE = (55, 40)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


SPACESHIP1 = pygame.image.load(os.path.join('spaceship_yellow.png'))  # yellow spaceship
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(SPACESHIP1, SPACESHIP_SIZE), 90)
SPACESHIP2 = pygame.image.load(os.path.join('spaceship_red.png'))  # red spaceship
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(SPACESHIP2, SPACESHIP_SIZE), 270)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('space.png')), (WIDTH, HEIGHT))


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_MOVE
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_MOVE
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WINDOW.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT / 2 - draw_text.get_height()))
    pygame.display.update()
    pygame.time.delay(5000)

def yellow_movement(keys_pressed, yellow):
    """ Handles movement of the Yellow spaceship"""

    if keys_pressed[pygame.K_a] and yellow.x - MOVE > 0:  # Left
        yellow.x -= MOVE
    if keys_pressed[pygame.K_d] and yellow.x + MOVE + yellow.width < BORDER.x:  # Right
        yellow.x += MOVE
    if keys_pressed[pygame.K_w] and yellow.y - MOVE > 0:  # Top
        yellow.y -= MOVE
    if keys_pressed[pygame.K_s] and yellow.y + MOVE + yellow.height < HEIGHT - 15:  # Down
        yellow.y += MOVE


def red_movement(keys_pressed, red):
    """ Handles movement of the Yellow spaceship"""

    if keys_pressed[pygame.K_LEFT] and red.x - MOVE > BORDER.x + BORDER.width:  # Left
        red.x -= MOVE
    if keys_pressed[pygame.K_RIGHT] and red.x + MOVE + red.width < WIDTH:  # Right
        red.x += MOVE
    if keys_pressed[pygame.K_UP] and red.y - MOVE > 0:  # Top
        red.y -= MOVE
    if keys_pressed[pygame.K_DOWN] and red.y + MOVE + red.height < HEIGHT - 15:  # Down
        red.y += MOVE


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WINDOW.blit(SPACE, (0, 0))
    pygame.draw.rect(WINDOW, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render("HEALTH: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("HEALTH: " + str(yellow_health), 1, WHITE)
    WINDOW.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WINDOW.blit(yellow_health_text, (10, 10))
    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)
    pygame.display.update()


def main():
    red = pygame.Rect(700, 300, SPACESHIP_SIZE[0], SPACESHIP_SIZE[1])
    yellow = pygame.Rect(100, 300, SPACESHIP_SIZE[0], SPACESHIP_SIZE[1])

    red_bullets = []
    red_health = 10
    yellow_bullets = []
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    # While game is going.
    while run:
        clock.tick(FPS)
        # Checking for events in game.
        for event in pygame.event.get():
            # We check if user quited or not.
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)


            if event.type == RED_HIT:
                red_health -= 1
            if event.type == YELLOW_HIT:
                yellow_health -= 1

        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    # This will quit the game.
    pygame.quit()
    # recalling the function
    main()

# It is making sure it only runs main() function when this file runs.


if __name__ == "__main__":
    main()
