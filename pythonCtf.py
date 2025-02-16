import socket
from datetime import date
import re
import base64
import webcolors

# Paramètres du serveur
IP = "148.113.42.34"
PORT = 57207
LOCAL_PORT = 33148
    
    
#Pour flag3
def calc(response):
    calcul = re.findall(r"(\d+)\s*([\+\-\*/])\s*(\d+)", response)
    if calcul:
        n1, op, n2 = calcul[0]
        n1, n2 = int(n1), int(n2)
        
        if op == '+':
            return n1 + n2
        elif op == '-':
            return n1 - n2
        elif op == '*':
            return n1 * n2
        elif op == '/':
            return n1 / n2
    return 0
#Pour flag4
def decode_base64(response):
    code = re.findall(r"Décoder ce message:\s*([a-zA-Z0-9+/=]+)", response)
    if code:
        print(f"Base64 code found: {code[0]}") 
        code_bytes = code[0].encode("ascii")
        same_code = base64.b64decode(code_bytes)
        same_codebase = same_code.decode("ascii") 
        return same_codebase
    return ""

# Pour flag5
def decode_hex(hex_string):
    bytes_data = bytes.fromhex(hex_string)
    return bytes_data.decode("ascii")

def decode_morse(morse_code):
    morse_dict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
        'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
        'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
        '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----', ',': '--..--', '.': '.-.-.-',
        '?': '..--..', '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-'
    }
    morse_dict_reversed = {v: k for k, v in morse_dict.items()}
    words = morse_code.split('   ')
    decoded_message = ''
    for word in words:
        for char in word.split():
            decoded_message += morse_dict_reversed.get(char, '')
        decoded_message += ' '
    return decoded_message.strip()

def morse(response):
    code = re.findall(r"Décoder ce message en majuscule:\s*([a-fA-F0-9]+)", response)
    if code:
        hex_string = code[0]
        ascii_string = decode_hex(hex_string)
        print(f"ASCII string: {ascii_string}")
        morse_decoded = decode_morse(ascii_string)
        return morse_decoded
    return ""

# Pour flag6
def decode_braille(hex_string):
    try:
        bytes_code = bytes.fromhex(hex_string)
        braille_code = bytes_code.decode('utf-8')

        braille_translation = {
            '⠁': 'A', '⠃': 'B', '⠉': 'C', '⠙': 'D', '⠑': 'E',
            '⠋': 'F', '⠛': 'G', '⠓': 'H', '⠊': 'I', '⠚': 'J',
            '⠅': 'K', '⠇': 'L', '⠍': 'M', '⠝': 'N', '⠕': 'O',
            '⠏': 'P', '⠟': 'Q', '⠗': 'R', '⠎': 'S', '⠞': 'T',
            '⠥': 'U', '⠧': 'V', '⠺': 'W', '⠭': 'X', '⠽': 'Y',
            '⠵': 'Z', ' ': ' '
        }

        decoded_message = ''.join(braille_translation.get(char, '?') for char in braille_code).replace(' ', '')
        return decoded_message.strip()

    except Exception as e:
        return f"Erreur: {e}"

def braille(response):
    code = re.findall(r"Décoder ce message en majuscule:\s*([a-fA-F0-9]+)", response)
    if code:
        hex_string = code[0]
        decoded_text = decode_braille(hex_string)
        print(f"Braille decoded: {decoded_text}")
        return decoded_text
    return ""

# Pour flag7
def rgb_color(response):
    code = re.findall(r"Quelle est la couleur pour les valeurs RGB \((\d+), (\d+), (\d+)\)", response)
    if code:
        r, g, b = code[0]
        color_name = webcolors.rgb_to_name((int(r), int(g), int(b)))
        return color_name
    return ""

def connect_and_get_flag():
    try:
        # Création d'un socket TCP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.bind(('', LOCAL_PORT))
        print(f"Socket lié au port local {LOCAL_PORT}")

        # Connexion au serveur
        client_socket.connect((IP, PORT))
        print(">> Connecté au serveur")

        # Réception de la réponse du serveur
        response = client_socket.recv(1024).decode()
        print(f">> Réponse du serveur : {response}")

        # QUESTION1
        if "Question 1: Quel est votre prénom/nom/classe ?" in response:
            message = "Clement/Languedoc/3SI5"
            client_socket.sendall(message.encode())
            print(f">> Réponse envoyée : {message}")
            response = client_socket.recv(1024).decode()
            print(f">> Réponse du serveur : {response}")

        #QUESTION2
        if "Quelle est la date du jour" in response:
            current_date = date.today().strftime("%d/%m")
            client_socket.sendall(current_date.encode("utf-8"))
            print(f">> Date envoyée : {current_date}")
            response = client_socket.recv(1024).decode()
            print(f">> Réponse du serveur : {response}")
            
        #QUESTION3   
        if "Quel est le résultat de " in response:
            multiplication = calc(response)
            client_socket.sendall(str(multiplication).encode())
            print(f">> Réponse envoyée : {multiplication}")
            response = client_socket.recv(1024).decode()
            print(f">> Réponse du serveur : {response}")
            
        #QUESTION4    
        if "Décoder ce message:" in response:
            decode_base = decode_base64(response)
            client_socket.sendall(decode_base.encode())
            print(f">> Réponse envoyée : {decode_base}")
            response = client_socket.recv(1024).decode()
            print(f">> Réponse du serveur : {response}")
            
        #QUESTION5
        if "Décoder ce message en majuscule:" in response:
            morse_decoded = morse(response)
            client_socket.sendall(morse_decoded.encode())
            print(f">> Réponse envoyée : {morse_decoded}")
            response = client_socket.recv(1024).decode()
            print(f">> Réponse du serveur : {response}")
            
        #QUESTION6
        if "Décoder ce message en majuscule:" in response:
            braille_decoded = braille(response)
            client_socket.sendall(braille_decoded.encode())
            print(f">> Réponse envoyée : {braille_decoded}")
            response = client_socket.recv(1024).decode()
            print(f">> Réponse du serveur : {response}")
            
        #QUESTION7
        if "Quelle est la couleur pour les valeurs RGB" in response:
            braille_decoded = braille(response)
            client_socket.sendall(braille_decoded.encode())
            print(f">> Réponse envoyée : {braille_decoded}")
            response = client_socket.recv(1024).decode()
            print(f">> Réponse du serveur : {response}")
            
        client_socket.close()
        print(">> Closing...")

    except socket.error as e:
        print(f"[!] Erreur de connexion : {e}")

# Exécution de la fonction
if __name__ == "__main__":
    connect_and_get_flag()



