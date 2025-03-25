import socket
import signal
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 8090))
server.listen(5)
server.setblocking(False)  # Make the socket non-blocking

print("Server is listening")

running = True


def signal_handler(sig, frame):
    global running
    print("Stopping server...")
    running = False
    server.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

while running:
    try:
        client, addr = server.accept()
        print(f"Connection from {addr}")
        data = client.recv(1024).decode()
        print(f"Received: {data}")
        client.send("Server received your message".encode())
        client.close()
    except BlockingIOError:  # handle when no client connections are available
        pass  # keep trying until a connection or signal is received.
    except OSError as e:  # Handle socket errors, especially after closing.
        if running:
            print(f"Error: {e}")
        pass

print("Server stopped.")
