# Chatroom

#### Video Demo : https://www.youtube.com/watch?v=Le1i56IHF7k
#### Description :

The modern chatroom is an online chatroom application with the ultimate goal of being very user friendly after a server is setup ,In the folder you will find two files, Server.py and Client.py ,*BOTH OF WHICH HAVE HARDCODED IPS AND PORT* (occurring only once per file) ,change that to suit your needs ,you also MUST start Server.py before Client.py.


# How it works : 

Server.py is a file that when opened will start a thread that listens for incoming connections on the hardcoded port and IP addresses ,when a client tries to connect ,that thread sends a message asking for a name ,when a name is given it will start another thread that will continuously listen for that one client's messages ,which when received will be sent to all connected clients (including the server itself) to be displayed on their chatboxes ,it also displays to everyone that a client  has connected/disconnected ,the Admin (whoever has the server opened) will be allowed to send messages at any point during it's lifetime.

Client.py is a file that ,when opened, will automatically attempt to connect to the hardcoded ip address/port ,and when it does will wait to receive a message asking for a name ,after which will wait for user input ,then will send that message to the server and will start a thread to continue receiving messages from the server ,the user will be allowed to send messages at any point during the program's lifetime.


# Why does it work the way it does ? :

due to wanting to be as user friendly as I could be ,I abstracted away as much as I could ,and so instead of the user putting in a server IP there's a hardcoded server IP address ,which you'd need to change to whatever server you have available seeing as I don't have any ,and while it would've been easier trivial to give the user the ability to put in their own ip/port ,though that wouldn't be as user friendly ,I wanted my app to be more pleasant to use ,something similar to Discord ,where the server is ideally ALWAYS online and users come and go as they please ,though that did come with the downside of the client program refusing to launch if the server wasn't online.

