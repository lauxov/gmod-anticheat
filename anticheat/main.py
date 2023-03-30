import ctypes as ct
import ctypes.wintypes as w
import psutil
import tkinter as tk
from tkinter import messagebox
import requests
import time

WEBHOOK_URL = 'DISCORD_WEBHOOK_HERE'

PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
PAGE_READWRITE = 0x04
MAX_PATH = 260
TH32CS_SNAPPROCESS = 0x2
INVALID_HANDLE_VALUE = w.HANDLE(-1).value # 0xffffffff on 32-bit
                                          # 0xffffffffffffffff on 64-bit
SIZE_T = ct.c_size_t
ULONG_PTR = w.WPARAM  # WPARAM is ULONG on 32-bit and ULONGLONG on 64-bit.

process_names = ['gmod.exe', 'hl2.exe']

root = tk.Tk()
root.withdraw()

class PROCESSENTRY32(ct.Structure):

    _fields_ = (('dwSize', w.DWORD),
                ('cntUsage', w.DWORD),
                ('th32ProcessID', w.DWORD),
                ('th32DefaultHeapID', ULONG_PTR),
                ('th32ModuleID', w.DWORD),
                ('cntThreads', w.DWORD),
                ('th32ParentProcessID', w.DWORD),
                ('pcPriClassBase', w.LONG),
                ('dwFlags', w.DWORD),
                ('szExeFile', w.CHAR * MAX_PATH))

    # Allow this structure to print itself
    def __repr__(self):
        return f'PROCESSENTRY32(dwSize={self.dwSize}, ' \
                              f'cntUsage={self.cntUsage}, ' \
                              f'th32ProcessID={self.th32ProcessID:#x}, ' \
                              f'th32DefaultHeapID={self.th32DefaultHeapID:#x}, ' \
                              f'th32ModuleID={self.th32ModuleID:#x}, ' \
                              f'cntThreads={self.cntThreads}, ' \
                              f'th32ParentProcessID={self.th32ParentProcessID:#x}, ' \
                              f'dwFlags={self.dwFlags:#x}, ' \
                              f'szExeFile={self.szExeFile})'

PPROCESSENTRY32 = ct.POINTER(PROCESSENTRY32)

class MEMORY_BASIC_INFORMATION(ct.Structure):

    _fields_ = (("BaseAddress", w.LPVOID),
                ("AllocationBase", w.LPVOID),
                ("AllocationProtect", w.DWORD),
                ("PartitionId", w.WORD),
                ("RegionSize", SIZE_T),
                ("State", w.DWORD),
                ("Protect", w.DWORD),
                ("Type", w.DWORD))

    # Allow this structure to print itself
    def __repr__(self):
        return f'MEMORY_BASIC_INFORMATION(BaseAddress={self.BaseAddress if self.BaseAddress is not None else 0:#x}, ' \
                                        f'AllocationBase={self.AllocationBase if self.AllocationBase is not None else 0:#x}, ' \
                                        f'AllocationProtect={self.AllocationProtect:#x}, ' \
                                        f'PartitionId={self.PartitionId:#x}, ' \
                                        f'RegionSize={self.RegionSize:#x}, ' \
                                        f'State={self.State:#x}, ' \
                                        f'Protect={self.Protect:#x}, ' \
                                        f'Type={self.Type:#x})'

PMEMORY_BASIC_INFORMATION = ct.POINTER(MEMORY_BASIC_INFORMATION)

k32 = ct.WinDLL('kernel32', use_last_error=True)
OpenProcess = k32.OpenProcess
OpenProcess.argtypes = w.DWORD, w.BOOL, w.DWORD
OpenProcess.restype = w.HANDLE

ReadProcessMemory = k32.ReadProcessMemory
ReadProcessMemory.argtypes = w.HANDLE, w.LPCVOID, w.LPVOID, ct.c_size_t, ct.POINTER(ct.c_size_t)
ReadProcessMemory.restype = w.BOOL

CloseHandle = k32.CloseHandle
CloseHandle.argtypes = w.HANDLE,
CloseHandle.restype = w.BOOL

VirtualQueryEx = k32.VirtualQueryEx
VirtualQueryEx.argtypes = w.HANDLE, w.LPCVOID, PMEMORY_BASIC_INFORMATION, SIZE_T
VirtualQueryEx.restype = SIZE_T

CreateToolhelp32Snapshot = k32.CreateToolhelp32Snapshot
CreateToolhelp32Snapshot.argtypes = w.DWORD, w.DWORD
CreateToolhelp32Snapshot.restype = w.HANDLE

Process32First = k32.Process32First
Process32First.argtypes = w.HANDLE, PPROCESSENTRY32
Process32First.restype = w.BOOL

Process32Next = k32.Process32Next
Process32Next.argtypes = w.HANDLE, PPROCESSENTRY32
Process32Next.restype = w.BOOL

def get_global_ip():
    response = requests.get('http://ip-api.com/json')
    if response.status_code == 200:
        data = response.json()
        return data.get('query')
    return None

ip_address = get_global_ip()

payload = {
    "content": f"IP: {ip_address}"
}

def kill_processes(process_names):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] in process_names:
            proc.kill()

def find_bytes(process_names, bytes_values):
    for process_name in process_names:
        # Get a handle to each process with the specified name
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
                            # Search the buffer for the bytes value
                            if bytes_value in buffer[:bytes_read.value]:
                                print(f"Found in process {pid}")
                                response = requests.post(WEBHOOK_URL, json=payload)

                                # Kill the process (remove this if you don't want to kill the process)
                                kill_processes(process_names)
                                messagebox.showerror("Anticheat", "Access denied")
                                root.mainloop()

                                break

                    address += mbi.RegionSize

            CloseHandle(process_handle)

bytes_values = [b'exechack.cc', b'aimbot', b'antiaim']
find_bytes(process_names, bytes_values)
input("Press Enter to exit...")
