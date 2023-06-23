'''
🔍 This program will absolutely find cheats if they have been injected into the game.
It does not even help to "Unload", to try to hide the cheat from the program
Tested on many popular cheats
'''

# https://discord.gg/qPQTpwqayc
# https://youtube.com/@lauxov

import logging
from cfg import *
from functions.kill_process import *
from functions.hwid import *
from functions.ip_get import *
from detect import find_bytes

print("Executing ctypes...")
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Program started')

'''
⚠️Be careful about adding new bytes because this can cause "false detects"
and then the program will say that a person has cheats when he does not.
I recommend leaving it as it is. If you want to change it, run tests without and with the cheat 
'''
bytes_values = [b'exechack.cc', b'aimbot', b'antiaim']

find_bytes(process_names, bytes_values)
logging.info('Program finished')
input("Press Enter to exit...")
