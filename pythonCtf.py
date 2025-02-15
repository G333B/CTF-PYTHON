import socket
import datetime

# Paramètres du serveur (à modifier selon ton besoin)
IP = "148.113.42.34"
PORT = 35971

message = "Clement/Languedoc/3SI5"

def connect_and_get_flag():
    try:
        # Création d'un socket TCP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connexion au serveur
        client_socket.connect((IP, PORT))
        print(">>Connecté au serveur")
        client_socket.sendall(message.encode())

        # Réception de la réponse (flag)
        response = client_socket.recv(1024).decode()
        print(f">>Réponse du serveur : {response}")

        # Vérification de la réponse du serveur
        if "Question 1: Quel est votre prénom/nom/classe ?" in response:
            client_socket.sendall(message.encode())
            final_response = client_socket.recv(1024).decode()
            print(f"{final_response}")

        if "Question 2: Quelle est la date du jour ?" in message:
                print(">>Question 2 reçue : Quelle est la date du jour ?")
                today = datetime.datetime.today()
                date_message = f"{today.day}/{today.month}"
                client_socket.sendall(date_message.encode())
                final_response = client_socket.recv(1024).decode()
                print(f">>Réponse finale du serveur : {final_response}")

        client_socket.close()
        print(">>Closing...")

    except socket.error as e:
        print(f"[!] Erreur de connexion : {e}")

# Exécution de la fonction
if __name__ == "__main__":
    connect_and_get_flag()