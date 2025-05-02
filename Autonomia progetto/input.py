import RPi.GPIO as GPIO
import time

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

# Stato precedente dei pulsanti (False = non premuto, True = premuto)
# Con resistenze pull-up, 0 (LOW) significa pulsante premuto, 1 (HIGH) significa non premuto
button_states = {
    PLAYER1_UP: False,
    PLAYER1_DOWN: False,
    PLAYER2_UP: False,
    PLAYER2_DOWN: False
}

# Mappatura dei pulsanti ai messaggi
button_messages = {
    PLAYER1_UP: "Giocatore 1: su",
    PLAYER1_DOWN: "Giocatore 1: giu",
    PLAYER2_UP: "Giocatore 2: su",
    PLAYER2_DOWN: "Giocatore 2: giu"
}

def check_button(pin):
    """Verifica lo stato di un pulsante e restituisce True se è stato premuto"""
    # Con resistenze pull-up, GPIO.LOW (0) significa pulsante premuto
    return GPIO.input(pin) == GPIO.LOW

try:
    print("Sistema controller avviato. Premi CTRL+C per uscire.")
    
    while True:
        # Controlla ogni pulsante
        for pin in button_states:
            # Leggi lo stato attuale
            current_state = check_button(pin)
            
            # Se lo stato è cambiato da non premuto a premuto
            if current_state and not button_states[pin]:
                print(button_messages[pin])
            
            # Se lo stato è cambiato da premuto a non premuto
            elif not current_state and button_states[pin]:
                print(f"Rilasciato: {button_messages[pin]}")
                
            # Aggiorna lo stato precedente
            button_states[pin] = current_state
            
        # Piccola pausa per evitare utilizzo eccessivo della CPU
        time.sleep(0.05)
        
except KeyboardInterrupt:
    print("\nProgramma terminato.")
finally:
    GPIO.cleanup()