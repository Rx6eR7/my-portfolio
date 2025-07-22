import os

subnet = "enter a subnet"

for i in range(1, 255):
    ip = subnet + str(i)

    response = os.system(f"ping -n 1 -w 200 {ip} >nul")

    if response == 0:
        print(f"Device found at: {ip}")
