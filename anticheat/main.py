import ctypes as ct
from tkinter import messagebox
import requests

from cfg import *
from functions.ip_get import *
from functions.kill_process import *

# Function to detect bytes in memory and kill the process
def find_bytes(process_names, bytes_values):
    for process_name in process_names:
        # Get a handle to each process with the specified name
        process_ids = []
        # Create a snapshot of the system processes
        snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
        if snapshot != INVALID_HANDLE_VALUE:
            # Get the first process entry in the snapshot
            entry = PROCESSENTRY32()
            entry.dwSize = ct.sizeof(entry)
            if Process32First(snapshot, ct.byref(entry)):
                # Loop through all process entries
                while True:
                    if entry.szExeFile.decode() == process_name:
                        # Add the process ID to the list
                        process_ids.append(entry.th32ProcessID)
                    if not Process32Next(snapshot, ct.byref(entry)):
                        break
            CloseHandle(snapshot)

        # Loop through all the process IDs
        for pid in process_ids:
            # Open a handle to the process
            process_handle = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
            if process_handle == 0:
                continue

            # Loop through all the byte values to search for
            for bytes_value in bytes_values:
                address = 0
                # Loop through all the memory regions of the process
                while True:
                    # Get information about the memory region
                    mbi = MEMORY_BASIC_INFORMATION()
                    result = VirtualQueryEx(process_handle, address, ct.byref(mbi), ct.sizeof(mbi))
                    if not result:
                        break

                    # If the memory region is committed and has a positive size, read the memory into a buffer
                    if mbi.State == MEM_COMMIT and mbi.RegionSize > 0:
                        buffer = ct.create_string_buffer(mbi.RegionSize)
                        bytes_read = SIZE_T()
                        if ReadProcessMemory(process_handle, mbi.BaseAddress, buffer, mbi.RegionSize, ct.byref(bytes_read)):
                            # Search the buffer for the bytes value
                            if bytes_value in buffer[:bytes_read.value]:
                                # If the bytes value is found, send a notification to a webhook
                                response = requests.post(WEBHOOK_URL, json=payload)

                                # Kill the process (remove this if you don't want to kill the process)
                                kill_processes(process_names)
                                messagebox.showerror("Anticheat", "Access denied")
                                root.mainloop()

                                # Stop searching for the byte value in this process
                                break

                    address += mbi.RegionSize

            CloseHandle(process_handle)

# List of byte values to search for in memory
bytes_values = [b'exechack.cc', b'aimbot', b'antiaim']
# Call the find_bytes function with the process names and byte values to search for
find_bytes(process_names, bytes_values)
# Wait for user input before exiting
input("Press Enter to exit...")