import os
import pickle
import time



class network():
    def __init__(self, SSID, password):
        self.SSID = str(SSID)
        self.password = password
        self.priority = 0
        self.number = None

    def __repr__(self):
        return self.SSID


saved_networks = []

def wifi_find():
    try:
        a = os.popen("sudo iwlist wlan0 scan | perl -nle '/ESSID:(.*)$/ && print $1'").read()
    except:
        time.sleep(5)
        a = os.popen("sudo iwlist wlan0 scan | perl -nle '/ESSID:(.*)$/ && print $1'").read()
        #os.system('sudo reboot')
    network_list = []
    capture = False
    network = ''
    for i in range(len(a)):
        if a[i] == '"' and capture == True:
            capture = not capture
            if network[0:2] != '\\' and network[0:2] != '\\x' and network not in network_list:
                network_list.append(network)
        elif a[i] == '"' and capture == False:
            capture = not capture
            network = ''
        elif capture == True:
            network += a[i]
    return network_list


def scan():
    wifi_list = wifi_find()
    display_list = []
    for networks in wifi_list:
            display_list.append(network(networks, 'unknown'))
    return display_list


def dump(saved_networks):
    network_file = open('/home/pi/touchscreen-main/Saved_wifi', 'wb')
    pickle.dump(saved_networks, network_file)
    network_file.close()

def save_get():
    network_file = open('/home/pi/touchscreen-main/Saved_wifi', 'rb')
    saved_networks = pickle.load(network_file)
    network_file.close()
    return saved_networks

def save_conf(*args):
    candidate_network = args[0]
    os.popen('wpa_cli list_networks').read()
    #insert stuff to find all networks then delete them all from wpa_cli
    a = 'wpa_cli set_network 0 ssid '+"'"+'"'+candidate_network.SSID+'"'+"'"
    os.popen(a).read()
    b = 'wpa_cli set_network 0 psk '+"'"+'"'+candidate_network.password+'"'+"'"
    os.popen(b).read()
    os.popen('wpa_cli save_conf').read()
    os.popen('wpa_cli -i wlan0 reconfigure').read()
    time.sleep(2)
    c = connect()
    if c == True:
        saved_networks.append(candidate_network)
        if args[1] == 1:
            dump(saved_networks)
        return True
    else:
        return False

    #os.system('wpa_passphrase '+ str(candidate_network.SSID)+' ' + str(candidate_network.password) +' >> /etc/wpa_supplicant/wpa_supplicant.conf')

'''
def change_priority(network):
    global saved_networks
    for i in saved_networks:
        if i == network:
            i.priority = 1
        else:
            i.priority = 0
'''



def connect():
    os.system('sudo rfkill block wifi')
    os.system('sudo rfkill unblock wifi')
    time.sleep(8)
    a = os.popen('ifconfig wlan0').read()
    if 'inet' in a:
        return True

def disconnect():
    os.system('sudo rfkill block wifi')

#home = network('BT-5HAC5X', 'TpUrbaEcGg9gFL')
#phone = network('AndroidAP0A38','pgzw6963')
#connect()
#wifi_find()

#dump([])
