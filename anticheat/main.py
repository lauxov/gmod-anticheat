import ctypes as ct
from tkinter import messagebox
import requests

from cfg import *
from functions.ip_get import *
from functions.kill_process import *

def find_bytes(process_names, bytes_values):
    for process_name in process_names:

        process_ids = []

        snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
        if snapshot != INVALID_HANDLE_VALUE:

            entry = PROCESSENTRY32()
            entry.dwSize = ct.sizeof(entry)
            if Process32First(snapshot, ct.byref(entry)):

                while True:
                    if entry.szExeFile.decode() == process_name:

                        process_ids.append(entry.th32ProcessID)
                    if not Process32Next(snapshot, ct.byref(entry)):
                        break
            CloseHandle(snapshot)

        for pid in process_ids:

            process_handle = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
            if process_handle == 0:
                continue

            for bytes_value in bytes_values:
                address = 0

                while True:

                    mbi = MEMORY_BASIC_INFORMATION()
                    result = VirtualQueryEx(process_handle, address, ct.byref(mbi), ct.sizeof(mbi))
                    if not result:
                        break

                    if mbi.State == MEM_COMMIT and mbi.RegionSize > 0:
                        buffer = ct.create_string_buffer(mbi.RegionSize)
                        bytes_read = SIZE_T()
                        if ReadProcessMemory(process_handle, mbi.BaseAddress, buffer, mbi.RegionSize, ct.byref(bytes_read)):

                            if bytes_value in buffer[:bytes_read.value]:

                                response = requests.post(WEBHOOK_URL, json=payload)

                                kill_processes(process_names)
                                messagebox.showerror("Anticheat", "Access denied")
                                root.mainloop()

                                break

                    address += mbi.RegionSize

            CloseHandle(process_handle)

bytes_values = [b'exechack.cc', b'aimbot', b'antiaim']

find_bytes(process_names, bytes_values)

input("Press Enter to exit...")
