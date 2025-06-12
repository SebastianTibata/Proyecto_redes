# Enrutamiento batman

# Red ad-hoc con B.A.T.M.A.N. en Debian – Proyecto de Redes Computacionales

## Hardware utilizado

- 4 computadores portátiles
- 3 USB booteables con Debian y 1 microSD con Debian (Live)

---

## Topologia del Proyecto

La red se implementó de forma **lineal**, con nodos distribuidos desde el **edificio B** hasta la **portería** de la universidad, cada uno configurado como un nodo autónomo con una IP única. La intención era simular un entorno real donde no hay conectividad directa punto a punto, y se requiere que los mensajes viajen a través de múltiples dispositivos.

---

## Configuracion de IP de cada nodo

Las IPs asignadas a cada nodo fueron las siguientes:

- Nodo 1: 192.168.100.1
- Nodo 2: 192.168.100.2
- Nodo 3: 192.168.100.3
- Nodo 4: 192.168.100.4

---

## Tipo de Red: Ad-Hoc

La red se configuró como **ad-hoc**, es decir, cada nodo se comunica directamente con otros sin necesidad de infraestructura fija. Cada nodo forma parte de la malla y coopera reenviando mensajes incluso si él no es el origen ni el destino del mensaje.

Esto fue esencial para lograr comunicación desde el primer hasta el último nodo sin conexión directa entre ellos.

---

## Proceso de Configuracioon Tecnica en Debian

### 1. Instalacion de paquetes necesarios

```bash
sudo apt update && sudo apt upgrade
sudo apt install batctl wireless-tools net-tools

```

## 2. Configuracion de red Ad-hoc

```
sudo ip link set wlan0 down
sudo iwconfig wlan0 mode ad-hoc
sudo iwconfig wlan0 essid mesh-net
sudo iwconfig wlan0 ap 02:12:34:56:78:9A
sudo ip link set wlan0 up

```

## 3. Activar B.A.T.M.A.N.

```
sudo modprobe batman-adv
sudo batctl if add wlan0
sudo ip link set up dev bat0
sudo ip addr add 192.168.100.X/24 dev bat0  # IP única por nodo

```

## 4. Verificacion de protocolo

```
sudo batctl n  # Muestra nodos vecinos conectados
```

## Chat en Python con UDP

Para validar la conexión se implementó un pequeño sistema de chat usando sockets UDP en Python. El script permite enviar mensajes de texto entre nodos ingresando la IP destino y el mensaje.

```python
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

```

## Evidencia del Funcionamiento

En la experimentación se realizo la prueba con 3 dispositivos, por falta de disponibilidad de mas de ellos, sin embargo se pueden integrar la cantidad de dispositivos que se deseen, solo teniendo en cuenta la IP con la que se configura cada uno de ellos.

Cada uno de las marcas azules fue un nodo, siendo el primero desde donde se toma la foto (segundo piso edificio B)

![Evidencia del Funcionamiento](nodos.jpg)

Evidencia de la comunicacion: Se enviaron mensajes desde el nodo 1 al nodo 4, pasando por el nodo 2, y viceversa. Recibiendo correctamente la informacion
![Evidencia de la comunicacion](prueba.jpg)

---

## Conclusiones

- El protocolo B.A.T.M.A.N. permitio una comunicacion efectiva sin depender de routers o acceso a internet.

- Los mensajes se reenviaron dinámicamente segun la calidad del enlace entre nodos vecinos.

- Se evidencio que cada computador (nodo) puede actuar como un intermediario en la entrega de informacion.

- La red es escalable y resiliente ante fallos individuales.
