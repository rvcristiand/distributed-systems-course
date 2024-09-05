# client.py
import socket

def main():
    # Aquí se usa la IP pública del servidor
    server_ip = input("Introduce la IP pública del servidor: ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, 12299))
    
    while True:
        message = input("Escribe un mensaje para enviar al servidor (o 'salir' para terminar): ")
        if message.lower() == 'salir':
            break
        client.send(message.encode('utf-8'))
        response = client.recv(4096).decode('utf-8')
        print(f"Respuesta del servidor: {response}")
    
    client.close()

if __name__ == "__main__":
    main()
