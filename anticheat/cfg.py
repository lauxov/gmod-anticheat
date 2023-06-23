import ctypes as ct
import ctypes.wintypes as w
import tkinter as tk

WEBHOOK_URL = 'WEBHOOK_URL'

PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010

MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000

PAGE_READWRITE = 0x04
MAX_PATH = 260

TH32CS_SNAPPROCESS = 0x2
INVALID_HANDLE_VALUE = w.HANDLE(-1).value 
detected_elements = []
embeds = []

process_names = ['gmod.exe', 'hl2.exe']

root = tk.Tk()
root.withdraw()

class PROCESSENTRY32(ct.Structure):

    _fields_ = (('dwSize', w.DWORD),
                ('cntUsage', w.DWORD),
                ('th32ProcessID', w.DWORD),
                ('th32DefaultHeapID', w.WPARAM),
                ('th32ModuleID', w.DWORD),
                ('cntThreads', w.DWORD),
                ('th32ParentProcessID', w.DWORD),
                ('pcPriClassBase', w.LONG),
                ('dwFlags', w.DWORD),
                ('szExeFile', w.CHAR * MAX_PATH))

    def __repr__(self):
        return f'PROCESSENTRY32(dwSize={self.dwSize}, ' \
                              f'cntUsage={self.cntUsage}, ' \
                              f'th32ProcessID={self.th32ProcessID:#x}, ' \
                              f'th32DefaultHeapID={self.th32DefaultHeapID:#x}, ' \
                              f'th32ModuleID={self.th32ModuleID:#x}, ' \
                              f'cntThreads={self.cntThreads}, ' \
                              f'th32ParentProcessID={self.th32ParentProcessID:#x}, ' \
                              f'pcPriClassBase={self.pcPriClassBase}, ' \
                              f'dwFlags={self.dwFlags:#x}, ' \
                              f'szExeFile={self.szExeFile})'

PPROCESSENTRY32 = ct.POINTER(PROCESSENTRY32)

class MEMORY_BASIC_INFORMATION(ct.Structure):

    _fields_ = (("BaseAddress", w.LPVOID),
                ("AllocationBase", w.LPVOID),
                ("AllocationProtect", w.DWORD),
                ("PartitionId", w.WORD),
                ("RegionSize", ct.c_size_t),
                ("State", w.DWORD),
                ("Protect", w.DWORD),
                ("Type", w.DWORD))

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
VirtualQueryEx.argtypes = w.HANDLE, w.LPCVOID, PMEMORY_BASIC_INFORMATION, ct.c_size_t
VirtualQueryEx.restype = ct.c_size_t

CreateToolhelp32Snapshot = k32.CreateToolhelp32Snapshot
CreateToolhelp32Snapshot.argtypes = w.DWORD, w.DWORD
CreateToolhelp32Snapshot.restype = w.HANDLE

Process32First = k32.Process32First
Process32First.argtypes = w.HANDLE, PPROCESSENTRY32
Process32First.restype = w.BOOL

Process32Next = k32.Process32Next
Process32Next.argtypes = w.HANDLE, PPROCESSENTRY32
Process32Next.restype = w.BOOL