import pygame
import sys
import RPi.GPIO as GPIO
import time

# Inizializzazione di pygame
pygame.init()

# Configurazione GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Definizione pin per i pulsanti
# Controller 1
PLAYER1_UP = 16
PLAYER1_DOWN = 20
# Controller 2
PLAYER2_UP = 21
PLAYER2_DOWN = 26

# Setup pin come input con resistenze di pull-up
GPIO.setup(PLAYER1_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PLAYER1_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PLAYER2_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PLAYER2_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Funzione per verificare se un pulsante è premuto
def check_button(pin):
    """Verifica lo stato di un pulsante e restituisce True se è stato premuto"""
    # Con resistenze pull-up, GPIO.LOW (0) significa pulsante premuto
    return GPIO.input(pin) == GPIO.LOW

# Dimensioni della finestra
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong con Controller Fisici")

# Colori
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Parametri del gioco
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 15
PADDLE_SPEED = 10
BALL_SPEED_X, BALL_SPEED_Y = 5, 5

# Creazione degli oggetti
player1 = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Punteggi
score1 = 0
score2 = 0
font = pygame.font.Font(None, 36)

# Variabili per il delay
ball_in_play = True
score_time = None
SCORE_DELAY = 2000  # 2 secondi in millisecondi

clock = pygame.time.Clock()

def reset_ball():
    ball.center = (WIDTH // 2, HEIGHT // 2)
    return BALL_SPEED_X if pygame.time.get_ticks() % 2 == 0 else -BALL_SPEED_X, BALL_SPEED_Y

ball_speed_x, ball_speed_y = reset_ball()

# Game loop
running = True
try:
    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Movimento dei giocatori usando i pulsanti fisici
        
        # Giocatore 1
        if check_button(PLAYER1_UP) and player1.top > 0:
            player1.y -= PADDLE_SPEED
        if check_button(PLAYER1_DOWN) and player1.bottom < HEIGHT:
            player1.y += PADDLE_SPEED
        
        # Giocatore 2
        if check_button(PLAYER2_UP) and player2.top > 0:
            player2.y -= PADDLE_SPEED
        if check_button(PLAYER2_DOWN) and player2.bottom < HEIGHT:
            player2.y += PADDLE_SPEED
        
        # Gestione del delay dopo un punto
        current_time = pygame.time.get_ticks()
        if not ball_in_play:
            ball.center = (WIDTH // 2, HEIGHT // 2)
            if current_time - score_time > SCORE_DELAY:
                ball_in_play = True
                ball_speed_x, ball_speed_y = reset_ball()
        else:
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
                ball_in_play = False
                score_time = pygame.time.get_ticks()
                
            if ball.right >= WIDTH:
                score1 += 1
                ball_in_play = False
                score_time = pygame.time.get_ticks()
        
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
        
        # Piccola pausa per evitare utilizzo eccessivo della CPU
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nProgramma terminato.")
finally:
    pygame.quit()
    GPIO.cleanup()
    sys.exit()