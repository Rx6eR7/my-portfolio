try:
    import msvcrt
    WINDOWS = True
except ImportError:
    msvcrt = None
    WINDOWS = False

try:
    from colorama import init, Fore
except ImportError:
    import subprocess
    import sys
    print("Installing 'colorama'...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    from colorama import init, Fore

import random
import os
import sys
import socket
import string
import tempfile

init(autoreset=True)
temp_dir = tempfile.gettempdir()

ascii_art = r"""
 ________  ________  ________  _______   ________  _________  ___       __   ________  ________  _______      
|\   __  \|\   __  \|\   __  \|\  ___ \ |\   __  \|\___   ___\\  \     |\  \|\   __  \|\   __  \|\  ___ \     
\ \  \|\  \ \  \|\  \ \  \|\ /\ \   __/|\ \  \|\  \|___ \  \_\ \  \    \ \  \ \  \|\  \ \  \|\  \ \   __/|    
 \ \   _  _\ \  \\\  \ \   __  \ \  \_|/_\ \   _  _\   \ \  \ \ \  \  __\ \  \ \   __  \ \   _  _\ \  \_|/__  
  \ \  \\  \\ \  \\\  \ \  \|\  \ \  \_|\ \ \  \\  \|   \ \  \ \ \  \|\__\_\  \ \  \ \  \ \  \\  \\ \  \_|\ \ 
   \ \__\\ _\\ \_______\ \_______\ \_______\ \__\\ _\    \ \__\ \ \____________\ \__\ \__\ \__\\ _\\ \_______\
    \|__|\|__|\|_______|\|_______|\|_______|\|__|\|__|    \|__|  \|____________|\|__|\|__|\|__|\|__|\|_______|
"""

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_password(min_length, numbers=True, special_characters=True):
    letters = string.ascii_letters
    digits = string.digits
    special = string.punctuation

    characters = letters
    if numbers:
        characters += digits
    if special_characters:
        characters += special

    pwd = ""
    meets_criteria = False
    has_number = False
    has_special = False

    while not meets_criteria or len(pwd) < min_length:
        new_char = random.choice(characters)
        pwd += new_char

        if new_char in digits:
            has_number = True
        elif new_char in special:
            has_special = True

        meets_criteria = True
        if numbers:
            meets_criteria = has_number
        if special_characters:
            meets_criteria = meets_criteria and has_special

    return pwd

def clean_temp():
    clear_console()
    deleted_files = 0
    skipped_files = 0
    for f in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, f)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                deleted_files += 1
            except PermissionError:
                skipped_files += 1
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
    print(f"Deleted {deleted_files} files in temp folder: {temp_dir}")
    if skipped_files > 0:
        print(f"Skipped {skipped_files} files (in use or permission denied)")

def scan_ports():
    clear_console()
    target = input("Enter an IP to scan: ")
    def pscan(port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((target, port))
            s.close()
            return True
        except:
            return False
    for x in range(1, 26):
        if pscan(x):
            print(f"[+] Port {x} is OPEN")
        else:
            print(f"[-] Port {x} is closed")

def scan_wifi():
    clear_console()
    subnet = input("Enter a subnet (e.g., 192.168.1): ")
    if not subnet.endswith('.'):
        subnet += '.'
    print("Scanning...")
    for i in range(1, 255):
        ip = subnet + str(i)
        response = os.system(f"ping -n 1 -w 200 {ip} >nul")
        if response == 0:
            print(f"Device found at: {ip}")

def password_menu():
    clear_console()
    min_length = int(input("Enter the minimum length: "))
    has_number = input("Do you want to have numbers? (y/n): ").lower() == "y"
    has_special = input("Do you want to have special characters? (y/n): ").lower() == "y"
    pwd = generate_password(min_length, has_number, has_special)
    print("The generated password is:", pwd)

def main():
    print(Fore.GREEN + ascii_art)
    while True:
        print("\nWhat would you like to do today?\n")
        print("1. Clean up Temp")
        print("2. See open ports on an IP address")
        print("3. Scan a WiFi for devices")
        print("4. Generate a password")
        print("\nPress ESC to exit at any time.\n")

        # Only check for ESC on Windows with msvcrt available
        if WINDOWS and msvcrt and msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'\x1b':  # ESC key
                print("Exiting...")
                sys.exit()

        option = input("Option you want: ")

        if option == "1":
            clean_temp()
        elif option == "2":
            scan_ports()
        elif option == "3":
            scan_wifi()
        elif option == "4":
            password_menu()
        else:
            print("Not valid")
            continue

        choice = input("\nDo you want anything else? (y/n): ").lower()
        if choice != "y":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
