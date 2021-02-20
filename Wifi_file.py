import os
import pickle
from wifi import Cell



class network():
    def __init__(self, SSID, password, encryption):
        self.SSID = str(SSID)
        self.password = password
        self.priority = 0
        self.encryption = encryption

saved_networks = []

def scan():
    wifi_list = list(Cell.all('wlan0'))
    display_list = []
    for networks in wifi_list:
        if networks.ssid == 'X/X/X/X/X/X/X/X/X/X/X':
            print('hidden network')
        else:
            if networks.encrypted == True:
                display_list.append(network(networks.ssid, 'unknown', networks.encryption_type))
            else:
                display_list.append(network(networks.ssid, 'N/A', 'None'))
    return display_list


def dump():
    global saved_networks
    network_file = open('Saved_wifi', 'wb')
    pickle.dump(saved_networks, network_file)
    network_file.close()

def save_get():
    global saved_networks
    network_file = open('Saved_wifi', 'rb')
    saved_networks = pickle.load(network_file)
    network_file.close()

def save_conf(*args):
    global saved_networks
    candidate_network = args[0]
    if candidate_network in saved_networks:
        print('This network has already been saved')
    elif candidate_network != 'none':
        saved_networks.append(candidate_network)
        change_priority(candidate_network)
    conf_file = open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w')
    conf_file.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev')
    conf_file.write('\n')
    conf_file.write('update_config=1')
    conf_file.write('\n')
    conf_file.write('country=GB')
    conf_file.write('\n')
    for networks in saved_networks:
        conf_file.write('\n')
        conf_file.write('network = {')
        conf_file.write('\n')
        conf_file.write('ssid="'+networks.SSID+'"')
        conf_file.write('\n')
        conf_file.write('psk="'+networks.password+'"')
        conf_file.write('\n')
        if networks.priority == 1:
            conf_file.write('priority=1')
            conf_file.write('\n')
        conf_file.write('}')
    conf_file.close()

def change_priority(network):
    global saved_networks
    for i in saved_networks:
        if i == network:
            i.priority = 1
        else:
            i.priority = 0

def connect():
    os.system('sudo ifconfig wlan0 down')
    os.system('sudo ifconfig wlan0 up')

def disconnect():
    os.system('sudo ifconfig wlan0 down')

#conf_file_read = open('/etc/wpa_supplicant/wpa_supplicant.conf', 'r')

#home = network('Glide0028763-2G', 'B47E0A0FD2')