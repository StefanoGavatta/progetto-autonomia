import pygame
import random

# Inizializzazione Pygame
pygame.init()

# Configurazione finestra
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong by Python")

# Colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configurazione paddle
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5

# Configurazione palla
BALL_SIZE = 20
ball_speed_x = 5 * random.choice((1, -1))
ball_speed_y = 5 * random.choice((1, -1))

# Inizializzazione paddle
left_paddle = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Inizializzazione palla
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# Punteggi
score_a = 0
score_b = 0

# Font
font = pygame.font.Font(None, 74)

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Gestione eventi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimento paddle
    keys = pygame.key.get_pressed()
    
    # Player A (sinistra - W/S)
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED

    # Player B (destra - Frecce su/giù)
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += PADDLE_SPEED

    # Movimento palla
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Collisioni con i bordi
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Collisioni con paddle
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x *= -1
        # Aumenta velocità dopo ogni colpo
        ball_speed_x *= 1.1
        ball_speed_y *= 1.1

    # Punti
    if ball.left <= 0:
        score_b += 1
        ball_reset()
    if ball.right >= WIDTH:
        score_a += 1
        ball_reset()

    def ball_reset():
        global ball_speed_x, ball_speed_y
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed_x = 5 * random.choice((1, -1))
        ball_speed_y = 5 * random.choice((1, -1))

    # Disegno elementi
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    # Disegno punteggi
    text = font.render(str(score_a), True, WHITE)
    screen.blit(text, (WIDTH//4, 20))
    text = font.render(str(score_b), True, WHITE)
    screen.blit(text, (3*WIDTH//4, 20))

    # Aggiornamento schermo
    pygame.display.flip()
    clock.tick(60)

pygame.quit()