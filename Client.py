import tkinter, socket, threading, json ,random
from tkinter import ttk


# Creating a "client" class for ease of use with functions later.
# Instead of doing the port forwarding work myself, I'm using playit.gg ,and my clients will be redirected
# to my server IP when trying to connect to playit.gg's server using this port.

# Define constants
hexcolors = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
grey = "#1f1f1f"
light_grey = "#3f3f3f"
client_font = ("Ariel" ,14) #User_font
server_color =  "#7d7676"
font_color = "#ffffff"
# Randomly generated hexcolor value using hexcolors list ,used for username color.
client_color = "#" + ''.join(random.sample(hexcolors, 6))

class theclients():
    def __init__(self):
        self.server_ip = "192.168.8.105" 
        self.server_port = 44044   
        self.bytesize = 8192 # 8 megabytes message size limit
        self.color = client_color
        self.client_socket = None
        self.name = "default"
        self.scrollbar = None
        self.counter = 20
        
    
# Define functions

# "flag" is the message's type.
def connect_client(client):
        client.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.client_socket.connect((client.server_ip, client.server_port))
        message_json = client.client_socket.recv(client.bytesize)
        process_message(client ,message_json)
    
def create_message(flag ,name ,color ,message) :
    '''Turns passed arguments into a dict, then turns that dict into json string and returns it unencoded'''
    message_packet = {
        "flag" : flag,
        "name" : name,
        "color" : color,
        "message" : message
    }
    message_json = json.dumps(message_packet)
    return message_json

# Adding 'a' to account for .bind.
def send_message(a,client ,flag="MESSAGE" ) :
    '''sends a message when Enter is pressed'''
    if flag == "INFO" :
        message_text = chatentry.get()
        client.name = message_text
        message_json = create_message(flag , client.name, client_color, "My name is : ") 
        client.client_socket.send(message_json.encode())
        chatentry.delete(0, tkinter.END)
    else :
        message_text = chatentry.get()
        message_json = create_message(flag, client.name ,client_color, message_text) 
        client.client_socket.send(message_json.encode())
        chatentry.delete(0, tkinter.END)

def process_message(client ,message_json):
    message_packet = json.loads(message_json) 
    if message_packet["flag"] == "INFO":
        # account for the "a" argument by putting in ''
        # For bind to work with functions that need arguments ,lambda must be used like this.
        
        #bind Allows us to send an info message to give our name.
        chatentry.bind('<Return>',  lambda event:send_message('',client ,"INFO"))
        message_thread = threading.Thread(target=recieve_messages,args=(client,))
        message_thread.start()

        # Change the binding to send "MESSAGE" flags instead of info flags
    elif message_packet["flag"] == "MESSAGE":
        name = message_packet["name"]
        message = message_packet["message"]
        try:
            chatentry.bind('<Return>',  lambda event:send_message('',client ,"MESSAGE"))
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
               
    elif message_packet["flag"] == "DISCONNECT":
        client.client_socket.send(message_json)
        root.destroy()
        client.client_socket.close()
        
        
    else :
        chathistory.insert(0, "Error processing message")
        autoscroll()

def recieve_messages(client) :
    '''Recieves messages and puts them in process_message function.'''
    # Currently ,since thers's only ''INFO'' and ''MESSAGE'' flags, you could just not really use process_message inside
    # of this function ,but later if we get new flags like "DISCONNECT" or something ,this will become useful.
    
    # Client's messages now have message values instead of info.
    while True :
        try :
            message_json = client.client_socket.recv(client.bytesize)
            process_message(client, message_json)
        except :
            chathistory.insert(tkinter.END, "Connection has been closed.")
            break
            

def disconnect_client(client):
    '''once the client attempts to close main window ,send disconnect flag message to server.'''
    message_json = create_message("DISCONNECT",client.name, client.color, "I am disconnecting").encode()
    client.client_socket.send(message_json)

            

         
def autoscroll(num=0):
    # Arbitrarily chosen counter (in this case 20) means it will automatically scroll no matter what
    # for the first 20 times this function is called ,after that a formula is used.
    if client.counter > 0:
        client.counter = client.counter - 1
        chathistory.yview_scroll(2,"units")
    # Uses scrollbar.get values to give a percentage ,if that percentage is above 92 ,then it means the user is at the bottom of the page
    # and it should autoscroll ,why 95 ? because I tested it and it felt fine, I could find a pattern percentage likely, but too lazy.
    coordinate0 = client.scrollbar.get()[0]
    coordinate1 = client.scrollbar.get()[1]
    if coordinate1 != 0 and coordinate0 != 0:
        if ((coordinate1 * coordinate0) / coordinate0) * 100 > 92 :
            chathistory.yview_scroll(num,"units")
# Define windows

# Make root window
root = tkinter.Tk()
root.title("CS50's chatroom")
root.geometry('700x700')

# Make chatbox frame and its widgets

# If I want my chathistory and entry (my widgets) to automatically resize with the window ,then I need to have empty 
# columns ,put my widgets in the column between them and then change column weight to get desired result.
# I believe this for example makes my column take a bit over 98% of the screen's width.
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

# Make a popup (and button to open/close it) that shows everyone connected


# The program
client = theclients()
client.scrollbar = historyscrolly
connect_client(client)
chathistory.insert(0, "Please enter a username.")
chathistory.itemconfig(0 ,fg=server_color)
root.bind("<Destroy>" ,lambda event:disconnect_client(client))
# Starts the GUI
root.mainloop()
