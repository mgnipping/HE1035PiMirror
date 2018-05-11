import wifi
import netifaces

current_ssid = None


def configure(ssid, pwd):
    print("connecting to "+ssid)

    cell_list = wifi.Cell.all('wlan0')

    for cell in cell_list:
        if cell.ssid ==ssid:
            saved_cell = wifi.Scheme.find('wlan0', ssid)
            if saved_cell:
                try:
                    saved_cell.activate()
                except Exception:
                    return False      
                global current_ssid
                current_ssid = ssid
                return True
            else:
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
def getIP():
    netifaces.ifaddresses('wlan0')
    ipaddr = netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']
    return ipaddr
