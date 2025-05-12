import socket
import json
import time
from datetime import datetime

SERVER_IP = '0.0.0.0'  # Ascolta su tutte le interfacce di rete
SERVER_PORT = 12345

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(1)  # Accetta una sola connessione

    print(f"Server datalogger in ascolto su {SERVER_IP}:{SERVER_PORT}...")

    conn, addr = server_socket.accept()
    print(f"Connessione ricevuta da: {addr}")

    try:
        while True:
            data = conn.recv(1024)  # Riceve fino a 1024 byte di dati
            if not data:
                break  # Connessione chiusa dal client

            try:
                game_data = json.loads(data.decode('utf-8'))
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = f"[{timestamp}] Buttons: {game_data['buttons']}, Ball: {game_data['ball']}, Score: {game_data['score1']}-{game_data['score2']}"
                print(log_entry)

                # Qui potresti scrivere i dati su un file
                with open("pong_data.log", "a") as f:
                    f.write(log_entry + "\n")

            except json.JSONDecodeError:
                print(f"Dati ricevuti non in formato JSON: {data.decode('utf-8')}")
            except KeyError as e:
                print(f"Chiave mancante nei dati JSON: {e}")

    except ConnectionResetError:
        print(f"Connessione con {addr} interrotta.")
    finally:
        conn.close()
        server_socket.close()
        print("Server datalogger terminato.")

if __name__ == "__main__":
    run_server()