import socket 
import threading

# define the size of message, it defined 64 bytes
HEADER = 64

PORT = 5050

# automatical get your ipv4 address. you can also define manual, "192.168.x.x"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

# stop server if client send disconnenction message
DISCONNECT_MESSAGE = "!DISCONNECT"

# AF_INET is ipv4 protocol, you can alse use ipv6, bluetooth and other protocols
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# socket bind with special ip and port, prepare for receive message from client
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        # recevive the message from HEADER and decode into utf-8
        msg_length = conn.recv(HEADER).decode(FORMAT)
        # avoid program stop if no message sent by client
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            # server send message back to client
            conn.send("Msg received".encode(FORMAT))

    print("CONNECTIONS END.")
    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        # conn: contents with binary form, has to convert to utf-8 later. address shows client ip and port
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
