#
# 
# SIG Blockchain
# Author: Karol Stolarski
#
# Peer to Peer Chat
#
# Run file with 'networks.py' in working directory
# Select 0 to be a server, 1 to be a client
# Servers: pick a port (number larger than 1000 is recommended)
# Client: connect to the server's ip and port
# Start Chatting!
# Exit with 'q' as input
#
#

from networks import *

# header
print('*'*62)
print('*'*23 + ' SIG BLOCKCHAIN ' + '*'*23)
print('*'*62)
print('*'*25 + ' P2P Chat ' + '*'*27)
print('*'*62)



# chat loop. Exit with 'q'
def chat(n, ip):
    print("Start chatting!")
    ui = input("\n")
    while not ui == "q":
        n.send_message("{ " + ip + " } " + ui)
        ui = input()

    n.disconnect()


# Select server or client
ui = int(input("\n>> Select 0 for Server or 1 for Client: "))
while not ui == 0 and not ui == 1:
    ui = int(input(">> Please select either 0 (server) or 1 (client): "))


# inputs for corresponding node type
if ui == 0:
    print(">> You have elected to become the server.")
    ip = get_ip()
    port = int(input(">> Select a port number > 1000: "))
    print("\n>> Your ip is: \t\t%s" % ip)
    print(">> Port selected: \t%d" % port)
    n = Server(port)
    n.integrate()
else:
    print(">> You will be a client.")
    n = Client()
    addr = input(">> Server ip:port (xxx.xxx.x.x:x) ? ")
    addr = addr.replace(" ", "")
    addr = addr.split(":")
    server = {
        'ip': addr[0],
        'port': int(addr[1])
    }
    n.integrate(server)

n.integrated.wait()

your_ip = get_ip()

# run the chat thread
input_thread = threading.Thread(
    target=chat, name="Chat", args=(n, your_ip))
input_thread.start()



