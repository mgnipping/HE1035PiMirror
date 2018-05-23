import wifi
import netifaces

current_ssid = None
current_ip = None

def configure(ssid, pwd):
    print("connecting to "+ssid)

    cell_list = wifi.Cell.all('wlan0')

    for cell in cell_list:
        if cell.ssid ==ssid:
            saved_cell = wifi.Scheme.find('wlan0', ssid)
            if saved_cell:
                #known network
                try:
                    saved_cell.activate()
                except Exception:
                    return False      
                global current_ssid
                current_ssid = ssid
                return True

            else:
                #new network
                if cell.encrypted: 
                    try:
                        scheme = wifi.Scheme.for_cell('wlan0', cell.ssid, cell, pwd)
                        scheme.save()
                        scheme.activate()
                    
                    except Exception:
                        cell.delete()
                        return False
                    global current_ssid
                    current_ssid = ssid
                    return True
                else:
                    
                    try:
                        scheme = wifi.Scheme.for_cell('wlan0', cell.ssid, cell, None)
                        scheme.save()
                        scheme.activate()         
                    except Exception:
                        cell.delete()
                        return False
                    global current_ssid
                    current_ssid = ssid
                    return True
    global current_ip
    current_ip = getIP()

def isConnected():

    if getIP() is not None:
        return True
    else:
        return False

def getSSID():
    
    try:
        cell = list(wifi.Cell.all('wlan0'))[0]
        global current_ssid
        return cell.ssid
    except Exception:
        return None
    

def getIP():

    try:
        netifaces.ifaddresses('wlan0')
        ipaddr = None
        ipaddr = netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']
        return ipaddr
    except Exception:
        return None

current_ssid = getSSID()
current_ip = getIP()
