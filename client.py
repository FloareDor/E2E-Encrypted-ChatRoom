import socket
import threading as thr
import PySimpleGUI as sg
import rsa
from rsa import PublicKey, PrivateKey
import random
HOST = '127.0.0.1'
PORT = 42042
publicKey, privateKey = rsa.newkeys(2048)
publicKeys = []	
caesar_Key = 69
header_Size = 10
def caesar_Encrypt(string,s):
	result = ""
	for c in string:
		if c.isalpha():
			if c.isupper():
				result += chr((ord(c) + s - 65) % 26 + 65)
			else:
				#result += chr(ord(c) + s)
				result += chr((ord(c) + s - 97) % 26 + 97)
		else:
			result += c
	return result

def caesar_Decrypt(string,s):
	result = ""
	for c in string:
		if c.isalpha():
			if c.isupper():
				result += chr((ord(c) - s - 65) % 26 + 65)
			else:
				#result += chr(ord(c) + s)
				result += chr((ord(c) - s - 97) % 26 + 97)
		else:
			result += c
	return result
def turn_pub_key_to_string(pub_key):
	a = str(pub_key['n'])
	b = str(pub_key['e'])
	return (a + ',' + b).encode('ISO-8859-1')

def assemble_pub_key_from_string(pub_key):
	k = list(pub_key.decode('ISO-8859-1').split(','))
	pub_key = PublicKey(int(k[0]),int(k[1]))
	return pub_key

QT_ENTER_KEY1 =  'special 16777220'
QT_ENTER_KEY2 =  'special 16777221'


name = input("Choose a nickname: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
def has_alpha(s):
	for character in s:
		if character.isalpha():
			return True
	return False

def receive():
	while True:
		try:

			message = client.recv(2048)

			decoded_Msg = message.decode('ISO-8859-1')
			if message == b'NAME':
				client.send(name.encode('ISO-8859-1'))
				print('Connected to the server!')

				pass
			elif decoded_Msg == 'COLLECT_KEY':
				client.send(turn_pub_key_to_string(publicKey))
			elif decoded_Msg[-15:] == "420420420696969" and not has_alpha(decoded_Msg):
				msg = decoded_Msg[:-15]

				if msg.encode('ISO-8859-1') not in publicKeys:
					publicKeys.append(msg.encode('ISO-8859-1'))

			else:
				if message != b'':

					if message == b'Connected to the server!' or 'joined the chat!' in decoded_Msg or 'left the chat.' in decoded_Msg:
						print(message.decode('ISO-8859-1'))
					else:
						try:
							decMessage = rsa.decrypt(message, privateKey).decode()
							decMessage = caesar_Decrypt(decMessage, int(turn_pub_key_to_string(publicKey).decode('ISO-8859-1')[caesar_Key]))
							print(decMessage)
						except Exception as e:
							pass
		except Exception as e:
			print(f"total: {e}")
			print("An Error Occurred!")
			client.close()
			break

receive_thread = thr.Thread(target = receive)

sg.theme('Black')   # Add a touch of color

# All the stuff inside the window.
layout = [  [sg.Text('Your Message:'), sg.InputText(key = "Input")],
            [sg.Button('Send', key = "Send"), sg.Button('Cancel')], 
			[sg.Button('Show Encrypted Message', key = "Show_Encrypted_Message")]]

# Create the Window
window = sg.Window('ChatRoom', layout, return_keyboard_events=True, use_default_focus=True)

sg.Print('Chat Room Initializing....', do_not_reroute_stdout=False)

printf = sg.Print

printf('You have entered the Chat Room.')
receive_thread.start()
# Event Loop to process "events" and get the "values" of the inputs
while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
		break
	if event in ('\r', QT_ENTER_KEY1, QT_ENTER_KEY2):
		elem = window.FindElementWithFocus()
		if elem is not None and elem.Type == sg.ELEM_TYPE_BUTTON:
			window.Element("Send").Click()
	elif event == 'Send':
		message = f"{name}: {values['Input']}"
		if values["Input"] != "":
			for key in publicKeys:
				encMessage = caesar_Encrypt(message, int(key.decode('ISO-8859-1')[caesar_Key]))
				encMessage = rsa.encrypt(encMessage.encode('ISO-8859-1'), assemble_pub_key_from_string(key))
				client.send(encMessage)
			window["Input"].Update('')
	elif event == "Show_Encrypted_Message":
		message = f"{name}: {values['Input']}"
		if values["Input"] != "":
			x = caesar_Encrypt(message, int(turn_pub_key_to_string(publicKey).decode('ISO-8859-1')[caesar_Key]))
			xy = rsa.encrypt(x.encode('ISO-8859-1'), publicKey)
			print(f"Your Encrypted Message: {xy.decode('ISO-8859-1')}")
			for key in publicKeys:
				encMessage = caesar_Encrypt(message, int(key.decode('ISO-8859-1')[caesar_Key]))
				encMessage = rsa.encrypt(encMessage.encode('ISO-8859-1'), assemble_pub_key_from_string(key))

				client.send(encMessage)
			window["Input"].Update('')
window.close()
client.close()