from scapy.packet import Packet   # Import the base Packet class
from scapy.layers.inet import IP, TCP  # Import the IP layer
from scapy.sendrecv import sniff  # Import the sniff function
from scapy.layers.http import HTTP, HTTPResponse, HTTPRequest

 

# Initialize a global variable to count the number of TCP packets read
iPkt: int = 0

# Define a function to process each captured packet
def process_packet(pkt: Packet):
    # Use the global variable iPkt within the function
    global iPkt
    
    # Increment the packet count by 1
    iPkt += 1
    
    # Print a message showing the number of TCP packets read
    print(f"I've read a TCP packet on your PC: {iPkt}")

    # Check if the packet contains an IP layer, return if it doesn't
    if not pkt.haslayer(IP):
        return
    
    # Extract the source and destination IP addresses and the protocol, then store them in a string
    ip_layer = "IP_SRC: " + pkt[IP].src + " IP_DST: " + pkt[IP].dst + " PROTO: " + str(pkt[IP].proto) + " " + "IP_LEN " + str(pkt[IP].len)   
    
    # Print the IP source, destination, and protocol information
    print(ip_layer)

    if pkt[IP].proto == 6:
        print("Source port:", (pkt[TCP]).sport, "  ", "Destination port:", (pkt[TCP]).dport)
        print()

        if pkt[TCP].sport==80 or pkt[TCP].dport == 80:
            print("E' un pacchetto http")

            if pkt[TCP].sport==80:
                print("ed è una risposta")
                print()

                if pkt.haslayer(HTTPResponse):
                    print(pkt[HTTPResponse].show())

            elif pkt[TCP].dport == 80:
                print("ed è una domanda")
                print()
                
                if pkt.haslayer(HTTPRequest):
                    print(pkt[HTTPRequest].show())

        elif pkt[TCP].sport== 443 or pkt[TCP].dport == 443:
            print("E' un pacchetto tls")
            print()

# Start sniffing TCP packets on the "eth0" interface and call process_packet on each captured packet
sniff(iface="enp0s1", filter="tcp", prn=process_packet)

