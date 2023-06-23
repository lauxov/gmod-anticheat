import logging
import ctypes as ct
from tkinter import messagebox
import requests
import os
from cfg import *
from functions.kill_process import *
from functions.hwid import payload

def find_bytes(process_names, bytes_values):
    process_handle = None
    folder_path = "C:\\exechack"
    if os.path.isdir(folder_path):
        logging.warning(f"Found folder 'exechack' at path: {folder_path}")
        print(f"Found folder 'exechack' at path: {folder_path}")
        detected_elements.append(("Folder", folder_path))
        folder_embed = {
            "title": "Detected Folder",
            "description": f"Path: {folder_path}",
            "color": 16763904  
        }
        embeds.insert(0, folder_embed)
    else:
        pass

    num_detected_bytes = 0
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

            process_found = False
            process_bytes = []

            for bytes_value in bytes_values:
                address = 0

                while True:
                    mbi = MEMORY_BASIC_INFORMATION()
                    result = VirtualQueryEx(process_handle, address, ct.byref(mbi), ct.sizeof(mbi))
                    if not result:
                        break

                    if mbi.State == MEM_COMMIT and mbi.RegionSize > 0:
                        buffer = ct.create_string_buffer(mbi.RegionSize)
                        bytes_read = ct.c_size_t()
                        if ReadProcessMemory(process_handle, mbi.BaseAddress, buffer, mbi.RegionSize, ct.byref(bytes_read)):
                            if bytes_value in buffer[:bytes_read.value]:
                                num_detected_bytes += 1 
                                '''
                                ⚠️If you need more detects, then increase the number 10 by the one you want
                                Note that if you do this, then you will have problems with "Embed"
                                because the maximum allowed characters will be exceeded
                                
                                Remember that you do not need to increase this value unnecessarily
                                because 10 detects will be enough to be sure of cheating
                                '''
                                if num_detected_bytes <= 10: #That one
                                    print(f"Found in process {pid}")
                                    detected_elements.append(("Process", process_name, bytes_value.decode(), mbi.BaseAddress))
                                    logging.warning(f"⚠️Found bytes '{bytes_value.decode()}' in process '{process_name}' at address {mbi.BaseAddress:#x}")
                                    process_found = True
                                    process_bytes.append((bytes_value.decode(), mbi.BaseAddress))
                                else:
                                    break

                    address += mbi.RegionSize

                if num_detected_bytes > 10:
                    break

            if process_found:
                embed_fields = []
                for bytes_value, address in process_bytes:
                    embed_fields.append({"name": "Bytes", "value": bytes_value, "inline": True})
                    embed_fields.append({"name": "Address", "value": f"{address:#x}", "inline": True})

                embed = {
                    "title": "Detected Bytes in Process",
                    "fields": embed_fields,
                    "color": 16711680
                }

                embeds.append(embed)
                CloseHandle(process_handle)

    if embeds:
        payload['embeds'] = embeds
        response = requests.post(WEBHOOK_URL, json=payload)
        # kill_processes(process_names)
        messagebox.showerror("Anticheat", "Detect code: 1")
        root.mainloop()

    if process_handle is not None:
        CloseHandle(process_handle)