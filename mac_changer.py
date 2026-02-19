#!/usr/bin/env python
import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option('-m', '--mac', dest='address', help='New MAC address')
    (options,arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface")
    elif not options.address:
        parser.error("[-] Please specify a new MAC address")
    return options

def change_mac(interface, address):
    print('[+] changing MAC address for ' + interface + ' to ' + address)

    subprocess.call('ifconfig ' + interface + ' down', shell=True)
    subprocess.call('ifconfig ' + interface + ' hw ether ' + address, shell=True)
    subprocess.call('ifconfig ' + interface + ' up', shell=True)
    subprocess.call('ifconfig', shell=True)

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode()

    mac_address_search_result = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print('[-] Could not read MAC address')

options = get_arguments()
# change_mac(options.interface, options.address)
get_current_mac(options.interface)