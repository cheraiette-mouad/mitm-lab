from scapy.all import ARP, Ether, srp
import json

# Réseau cible
target_ip = "192.168.48.136/24"

# Création requête ARP
arp = ARP(pdst=target_ip)

# Broadcast MAC
ether = Ether(dst="ff:ff:ff:ff:ff:ff")

# Combinaison paquet
packet = ether / arp

# Envoi requête
result = srp(packet, timeout=2, verbose=0)[0]

clients = {}

print("\n[+] Machines détectées :\n")

for sent, received in result:
    ip = received.psrc
    mac = received.hwsrc

    clients[ip] = mac

    print(f"IP: {ip} | MAC: {mac}")

# Export JSON
with open("hosts.json", "w") as file:
    json.dump(clients, file, indent=4)

print("\n[+] Résultats sauvegardés dans hosts.json")
