import socket
import threading as thr
import time

# local host
host = '127.0.0.1' # Change the host 
port = 42042
print(host,port)
header_Size = 10
publicKeys = []
# internet, TCP protocol
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# binding the server to the local host
server.bind((host, port))
# looks for clients
server.listen()
names = []
clients = []

def broadcast(message):
	for client in clients:
		client.send(message) # sending a msg to everyone

def handle(client):
	while True:
		try:
			message = client.recv(256) # 1024 bytes
			broadcast(message)
			broadcast(b'')
			#print(message)
			#for pk in publicKeys:
				#broadcast(pk)
		except:
			index = clients.index(client)
			clients.remove(client)
			client.close()
			name = names[index]
			key = publicKeys[index]
			publicKeys.remove(key)

			left_Message = f"{name} left the chat."
			broadcast(left_Message.encode('ISO-8859-1'))
			names.remove(name)
			break

def recieve():
	while True:
		client, address = server.accept()
		print(f"Connected with {str(address)}")
		client.send('NAME'.encode('ISO-8859-1'))
		try:
			name = client.recv(1024).decode('ISO-8859-1')
			names.append(name)
		except:
			pass
		clients.append(client)
		client.send('COLLECT_KEY'.encode('ISO-8859-1'))
		key = client.recv(2048)
		#print(key.decode('ISO-8859-1'))
		key = key.decode('ISO-8859-1') + "420420420696969"
		#broadcast(key.encode('ISO-8859-1'))

		if key.encode('ISO-8859-1') not in publicKeys:
			publicKeys.append(key.encode('ISO-8859-1'))
			for pk in publicKeys:
				broadcast(pk)
				time.sleep(1)
		print(f"name of the client is {name}!")
		broadcast_msg = f"{name} joined the chat!"
		time.sleep(1.5)
		
		broadcast(broadcast_msg.encode('ISO-8859-1'))
		#client.send('Connected to the server!\n'.encode('ISO-8859-1'))
		
		thread = thr.Thread(target = handle, args = (client,))
		thread.start()

print("Server is running")
recieve()





