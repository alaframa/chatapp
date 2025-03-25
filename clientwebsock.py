import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 8090))

client.send("Hello, I am a client".encode())
data = client.recv(1024).decode()  # receive data from server.
print(f"Received: {data}")

client.close()  # close the client connection.
