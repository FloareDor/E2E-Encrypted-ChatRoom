# E2E-Encrypted-ChatRoom
### An End to End Encrypted ChatRoom built using sockets, based on RSA algorithm (PKCS#1 version 1.5).
#### The messages are encrypted by rsa (2048 bytes key) and caesar cipher. A new key pair is generated everytime a client connects to the server and the private key will only be with the respective client only.So, the privacy is indeed very strong. No one else but the sender and the recipient can see the messages. In addition, the caesar shift number is also randomly generated for each client.

### How to host your own Encrypted ChatRoom?
* Input the IP address of the public server you want to host the chatroom on, in server.py file and run the file.
* Share the client.py file with all of the people you wanna invite over to the chat room.
* Install the necessary libraries that are mentioned in the Requirements.txt file on the client side.
* Run the client.py file.
* Input a temporary nickname.
  

