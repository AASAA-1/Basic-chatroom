import tkinter, socket, threading, json
from tkinter import ttk

# Define constants.

white = "#ffffff"
hexcolors = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
grey = "#1f1f1f"
light_grey = "#3f3f3f"
font = ("Ariel" ,14,)
font_color = "#ffffff"
# Randomly generated hexcolor value.
admin_color = "#8be01c"
client_font = ("Ariel" ,14)
server_color =  "#7d7676"


# Creating "server" class for ease of use with functions later.
class theservers():
    def __init__(self):
        self.ip = "192.168.8.105"
        self.port = 44044
        self.bytesize = 8192 # 8 megabytes message size limit
        self.server_socket = None
        self.client_sockets = []
        self.client_addresses = []
        self.counter = 20
        self.scrollbar = None


# Create a server instance, then create an unbound server socket ,then bind it ,
# and save the bound socket to my server instance.


# Define functions

# "flag" is the message's type.
def create_message(flag ,name ,color ,message) :
    '''Turns passed arguments into a dict, then turns that dict into json string and returns it'''
    message_packet = {
        "flag" : flag,
        "name" : name,
        "color" : color,
        "message" : message
    }
    message_json = json.dumps(message_packet)
    return message_json

def start_server(server):
    '''Start server.'''
    server.server_socket= socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
    server.server_socket.bind((server.ip, server.port))
    server.server_socket.listen()
    connect_thread = threading.Thread(target=connect_client ,args=(server,))
    connect_thread.start()


    

def connect_client(server):
    '''used in start_server as a thread to keep connecting clients and then recieve their messages.'''
    try:
        while True:
            clientSocket, clientAddress = server.server_socket.accept()
            server.client_sockets.append(clientSocket)
            server.client_addresses.append(clientAddress)
            message_json = create_message("INFO","Server",white, "Please enter your name.").encode()
            clientSocket.send(message_json)
            message_json = clientSocket.recv(server.bytesize)
            process_message(server, message_json ,clientSocket)
    except:
        pass
    
def process_message(server, message_json ,clientSocket):
    '''Recieves ENCODED messages.'''
    try:
        message_packet = json.loads(message_json)
        if message_packet["flag"] == "INFO":
            # Do something here to get name and store it.
            message_json = create_message("MESSAGE","Server",white, f"{message_packet['name']} has joined the server !").encode()
            broadcast_message(server ,message_json)
            autoscroll()
            process_thread = threading.Thread(target=recieve_message, args=(server,clientSocket))
            process_thread.start()
            
        elif message_packet["flag"] == "MESSAGE":
            broadcast_message(server, message_json)
            
        elif message_packet["flag"] == "DISCONNECT" :
            index = server.client_sockets.index(clientSocket)
            message_json = create_message("DISCONNECT","Server",white ,"Disconnect").encode()
            clientSocket.send(message_json)
            clientSocket.close()
            del server.client_sockets[index]
            del server.client_addresses[index]
            message_json = create_message("MESSAGE","Server",white, f"{message_packet['name']} has left the server.").encode()
            broadcast_message(server, message_json)

        else :
            # Error handling else
            pass
    except:
        pass


def broadcast_message(server ,message_json):
    '''broadcasts recieved ENCODED messages ,used in recieve_messages()'''
    message = message_json
    for socket in server.client_sockets:
        socket.send(message)
    message_packet = json.loads(message_json)
    name = message_packet["name"]
    message = message_packet["message"]
    try:
        chatentry.bind('<Return>',  lambda event:send_message('',server ,"MESSAGE"))
    except:
        pass     
    if name == "Server" :
        chathistory.insert(tkinter.END, f"{name}: {message}")
        chathistory.itemconfig(tkinter.END, fg=server_color)
        autoscroll()
    else :
        chathistory.insert(tkinter.END, f"{name}:")
        chathistory.itemconfig(tkinter.END, fg=message_packet["color"])
        chathistory.insert(tkinter.END, f"  {message}")
        chathistory.itemconfig(tkinter.END, )
        autoscroll(2)
               
def send_message(a,server ,flag="MESSAGE" ) :
    '''sends a message when Enter is pressed'''
    message_text = chatentry.get()
    message_json = create_message(flag, "Admin " ,admin_color, message_text) 
    broadcast_message(server,message_json.encode())
    chatentry.delete(0, tkinter.END)

def recieve_message(server ,clientSocket):
    while True:
        try :
            message_json = clientSocket.recv(server.bytesize)
            process_message(server, message_json ,clientSocket)
        except :
             break

         
def autoscroll(num=0):
    # Arbitrarily chosen counter (in this case 20) means it will automatically scroll no matter what
    # for the first 20 times this function is called (so for the first 20 messages) ,after that the formula below is used.
    if server.counter > 0:
        server.counter = server.counter - 1
        chathistory.yview_scroll(2,"units")
    # Uses scrollbar.get values to give a percentage ,if that percentage is above 92 ,then it means the user is at the bottom of the page
    # and it should autoscroll ,why 92 ? because I tested it and it felt fine, I could find a pattern percentage likely, but too lazy.
    coordinate0 = server.scrollbar.get()[0]
    coordinate1 = server.scrollbar.get()[1]
    if coordinate1 != 0 and coordinate0 != 0:
        if ((coordinate1 * coordinate0) / coordinate0) * 100 > 92 :
            chathistory.yview_scroll(num,"units")
# Define windows


# the GUI is pretty much just copy pasted from client.
root = tkinter.Tk()
root.title("The server ")
root.geometry('700x700')

chatframe = tkinter.Frame(root ,bg=grey ,borderwidth=0)
chatframe.columnconfigure(0, weight=1)
chatframe.columnconfigure(1, weight=99)
chatframe.columnconfigure(2, weight=1)

chathistory = tkinter.Listbox(chatframe ,bg=grey ,height=25 ,font=client_font ,fg=font_color ,borderwidth=0 ,highlightthickness=0)
chatentry = tkinter.Entry(chatframe, bg=light_grey, font=client_font ,fg=font_color,borderwidth=0, highlightthickness=0)

chatframe.pack(expand=True ,fill="both")
chathistory.grid(row=0,column=1,sticky="WENS")
chatentry.grid(row=1,column=1,sticky="WENS")


historyscrolly = tkinter.Scrollbar(chatframe,orient="vertical")
historyscrolly.config(command=chathistory.yview ,bg=light_grey ,troughcolor=light_grey )
chathistory.config(yscrollcommand=historyscrolly.set)
historyscrolly.grid(row=0,column=2, sticky="ENS")





# The program
server = theservers()
server.scrollbar = historyscrolly

start_server(server)

# Starts the GUI
root.mainloop()