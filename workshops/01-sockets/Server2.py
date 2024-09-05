# server.py
import socket
import threading

def handle_client(client_socket):
    while True:
        # Recibir datos del cliente
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break
        print(f"Recibido: {message}")
        
        # Enviar una respuesta al cliente
        response = f"Mensaje recibido: {message}"
        client_socket.send(response.encode('utf-8'))
    
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Servidor escuchando en puerto 9999...")

    while True:
        client_socket, addr = server.accept()
        print(f"Conexión establecida con {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()