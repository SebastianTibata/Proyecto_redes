import socket
import threading


MI_IP = "192.168.100.1" 
PORT = 5005       
DESTINOS = [
    "192.168.100.4"
]

BUFFER_SIZE = 1024


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((MI_IP, PORT))


def recibir():
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        print(f"\n📨 De {addr[0]}: {data.decode()}\n> ", end="")


threading.Thread(target=recibir, daemon=True).start()

print(f"Chat BATMAN activo en {MI_IP}. Enviando a: {', '.join(DESTINOS)}")
print("Escribe tu mensaje. Escribe 'salir' para terminar.")


while True:
    mensaje = input("> ")
    if mensaje.lower() == "salir":
        break
    for ip in DESTINOS:
        sock.sendto(mensaje.encode(), (ip, PORT))
