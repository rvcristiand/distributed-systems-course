# server.py
import os
import socket
import threading

def recv_bytes(sock, size):
    data = b''

    while len(data) < size:
        packet = sock.recv(size - len(data))
        
        if not packet:
            raise RuntimeError("La conexión del socket está rota")

        data += packet

    return data

def handle_client(client_socket, output_dir):
    # recibir el tamaño de la imagen primero (4 bytes)
    size_data = recv_bytes(client_socket, 4)
    size = int.from_bytes(size_data, 'big')
    print(f"Recibiendo imagen de tamaño {size} bytes")

    # recibir la imagen
    img_bytes = recv_bytes(client_socket, size)

    outout_path = os.path.join(output_dir,
                               f"imagen_recibida_{address[0]}_{address[1]}_{size}.jpg")
    with open(outout_path, "wb") as img_file:
        img_file.write(img_bytes)

    print(f"Imagen guardada en {outout_path}")

    client_socket.close()

def start_server(host: str, port: int, output_dir: str = "./"):
    """
    Inicia un servidor para recibir imágenes a través de TCP.

    Parameters
    ----------
    host : str
        Dirección IP del servidor.
    port : int
        Puerto donde el servidor estará escuchando.
    output_dir : str
        Directorio donde se guardará la imagen recibida.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor escuchando en {host}:{port}...")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Conexión establecida con {address}")
        
        client_handler = threading.Thread(target=handle_client, args=(client_socket, output_dir))
        client_handler.start()

if __name__ == "__main__":
    import typer
    app = typer.Typer()

    @app.command()
    def run_server(host: str = "0.0.0.0", port: int = 12299):
        """
        Inicia el servidor TCP para recibir imágenes.

        Parameters
        ----------
        host : str
            Dirección IP del servidor (por defecto "0.0.0.0" para escuchcar en todas las interfaces).
        port : int
            Puerto donde el servidor estará escuchando (por defecto 12299).
        output_dir : str
            Directorio donde se guardará la imagen recibida (por defecto "./").
        """
        start_server(host, port)

    app()
