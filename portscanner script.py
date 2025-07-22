import socket

target = input("Enter an IP to scan: ")

def pscan(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)  # avoid hanging
        s.connect((target, port))
        s.close()
        return True
    except:
        return False

for x in range(1, 26):  # 1-25
    if pscan(x):
        print(f"[+] Port {x} is OPEN")
    else:
        print(f"[-] Port {x} is closed")
