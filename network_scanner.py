import optparse
import argparse
import scapy.all as scapy

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target', help='Target IP address')
    options = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify an IP/IP range")
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)
    # print(answered_list.summary())

    clients_list = []

    # prints IP and MAC addresses for each answered packet
    for _, reply in answered_list:
        client_dict = {"ip": reply.psrc, "mac": reply.hwsrc}
        clients_list.append(client_dict)

    return clients_list

    # print(clients_list)

    # prints all data from each answered packet
    # for i in answered_list:
    #     print(i)
    #     print("-------------------------------------------------------------------------------")

def print_results(results_list):
    # print header
    print("IP\t\t\tMAC")
    print("-"*50)

    for results in results_list:
        print(results["ip"] + "\t\t" + results["mac"])

ip_range = get_arguments()

scan_result = scan(ip_range.target)

print_results(scan_result)
