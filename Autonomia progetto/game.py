import pygame
import sys

# Inizializzazione di pygame
pygame.init()

# Dimensioni della finestra
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

# Colori
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Parametri del gioco
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 15
PADDLE_SPEED = 10
BALL_SPEED_X, BALL_SPEED_Y = 10, 10

# Creazione degli oggetti
player1 = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Punteggi
score1 = 0
score2 = 0
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

def reset_ball():
    ball.center = (WIDTH // 2, HEIGHT // 2)
    return BALL_SPEED_X if pygame.time.get_ticks() % 2 == 0 else -BALL_SPEED_X, BALL_SPEED_Y

ball_speed_x, ball_speed_y = reset_ball()

# Game loop
running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Movimento dei giocatori
    keys = pygame.key.get_pressed()
    
    # Giocatore 1 (W e S)
    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= PADDLE_SPEED
    if keys[pygame.K_s] and player1.bottom < HEIGHT:
        player1.y += PADDLE_SPEED
    
    # Giocatore 2 (Frecce su e giù)
    if keys[pygame.K_UP] and player2.top > 0:
        player2.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
        player2.y += PADDLE_SPEED
    
    # Movimento della pallina
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    
    # Collisioni con i bordi
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
    
    # Collisioni con le racchette
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speed_x *= -1
    
    # Punteggio
    if ball.left <= 0:
        score2 += 1
        ball_speed_x, ball_speed_y = reset_ball()
    if ball.right >= WIDTH:
        score1 += 1
        ball_speed_x, ball_speed_y = reset_ball()
    
    # Disegno
    pygame.draw.rect(screen, WHITE, player1)
    pygame.draw.rect(screen, WHITE, player2)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    
    # Testo del punteggio
    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()