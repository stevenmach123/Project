from networks import *

# header
print('*'*62)
print('*'*23 + ' SIG BLOCKCHAIN ' + '*'*23)
print('*'*62)
print('*'*25 + ' P2P Chat ' + '*'*27)
print('*'*62)

def chat(n):
    ui = input("\n>> : ")
    while not ui == "q":
        n.send_message(ui)
        ui = input("\n>> : ")

    n.disconnect()

ui = int(input("\n>> Select 0 for Server or 1 for Client: "))
while not ui == 0 and not ui == 1:
    ui = int(input(">> Please select either 0 (server) or 1 (client): "))

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
    ip = input(">> Server IP? (xxx.xxx.x.x): ")
    port = int(input(">> Server port?: "))
    server = {
        'ip': ip,
        'port': port
    }
    n.integrate(server)

n.integrated.wait()

input_thread = threading.Thread(
    target=chat, name="Chat", args=(n,))
input_thread.start()



