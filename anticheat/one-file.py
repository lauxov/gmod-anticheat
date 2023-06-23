# If you need the code in one file - take only this file ⚠️⚠️⚠️⚠️
# If you need the code in one file - take only this file⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
# If you need the code in one file - take only this file⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
# If you need the code in one file - take only this file⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️

d=print
L=None
K='name'
E=True
import logging as C,ctypes as B
from tkinter import messagebox as p
import requests as X,ctypes.wintypes as A,tkinter as G,psutil as I,os,wmi
C.basicConfig(filename='log.txt',level=C.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
C.info('Program started')
def M():
	try:A=wmi.WMI();B=A.Win32_ComputerSystemProduct()[0];return B.UUID
	except Exception as D:C.error(f"Failed to retrieve HWID: {str(D)}");return
def i(process_names):
	for A in I.process_iter([K]):
		if A.info[K]in process_names:A.kill()
def N():
	A=X.get('http://ip-api.com/json')
	if A.status_code==200:B=A.json();return B.get('query')
U=N()
V=M()
Y={'content':f"IP: ||{U}||\nHWID: {V}"}
q='WEBHOOK_URL'
r=1024
s=16
t=4096
j=8192
k=4
W=260
u=2
v=A.HANDLE(-1).value
Z=[]
J=[]
e=['gmod.exe','hl2.exe']
a=G.Tk()
a.withdraw()
class b(B.Structure):
	_fields_=('dwSize',A.DWORD),('cntUsage',A.DWORD),('th32ProcessID',A.DWORD),('th32DefaultHeapID',A.WPARAM),('th32ModuleID',A.DWORD),('cntThreads',A.DWORD),('th32ParentProcessID',A.DWORD),('pcPriClassBase',A.LONG),('dwFlags',A.DWORD),('szExeFile',A.CHAR*W)
	def __repr__(A):return f"PROCESSENTRY32(dwSize={A.dwSize}, cntUsage={A.cntUsage}, th32ProcessID={A.th32ProcessID:#x}, th32DefaultHeapID={A.th32DefaultHeapID:#x}, th32ModuleID={A.th32ModuleID:#x}, cntThreads={A.cntThreads}, th32ParentProcessID={A.th32ParentProcessID:#x}, pcPriClassBase={A.pcPriClassBase}, dwFlags={A.dwFlags:#x}, szExeFile={A.szExeFile})"
F=B.POINTER(b)
class c(B.Structure):
	_fields_=('BaseAddress',A.LPVOID),('AllocationBase',A.LPVOID),('AllocationProtect',A.DWORD),('PartitionId',A.WORD),('RegionSize',B.c_size_t),('State',A.DWORD),('Protect',A.DWORD),('Type',A.DWORD)
	def __repr__(A):return f"MEMORY_BASIC_INFORMATION(BaseAddress={A.BaseAddress if A.BaseAddress is not L else 0:#x}, AllocationBase={A.AllocationBase if A.AllocationBase is not L else 0:#x}, AllocationProtect={A.AllocationProtect:#x}, PartitionId={A.PartitionId:#x}, RegionSize={A.RegionSize:#x}, State={A.State:#x}, Protect={A.Protect:#x}, Type={A.Type:#x})"
f=B.POINTER(c)
D=B.WinDLL('kernel32',use_last_error=E)
O=D.OpenProcess
O.argtypes=A.DWORD,A.BOOL,A.DWORD
O.restype=A.HANDLE
P=D.ReadProcessMemory
P.argtypes=A.HANDLE,A.LPCVOID,A.LPVOID,B.c_size_t,B.POINTER(B.c_size_t)
P.restype=A.BOOL
H=D.CloseHandle
H.argtypes=A.HANDLE,
H.restype=A.BOOL
Q=D.VirtualQueryEx
Q.argtypes=A.HANDLE,A.LPCVOID,f,B.c_size_t
Q.restype=B.c_size_t
R=D.CreateToolhelp32Snapshot
R.argtypes=A.DWORD,A.DWORD
R.restype=A.HANDLE
S=D.Process32First
S.argtypes=A.HANDLE,F
S.restype=A.BOOL
T=D.Process32Next
T.argtypes=A.HANDLE,F
T.restype=A.BOOL
def g(process_names,bytes_values):
	o='inline';n='value';m=False;l='color';k='title';D=L;I='C:\\exechack'
	if os.path.isdir(I):C.warning(f"Found folder 'exechack' at path: {I}");d(f"Found folder 'exechack' at path: {I}");Z.append(('Folder',I));w={k:'Detected Folder','description':f"Path: {I}",l:16763904};J.insert(0,w)
	else:0
	U=0
	for V in process_names:
		e=[];M=R(u,0)
		if M!=v:
			F=b();F.dwSize=B.sizeof(F)
			if S(M,B.byref(F)):
				while E:
					if F.szExeFile.decode()==V:e.append(F.th32ProcessID)
					if not T(M,B.byref(F)):break
			H(M)
		for f in e:
			D=O(r|s,m,f)
			if D==0:continue
			g=m;h=[]
			for G in bytes_values:
				N=0
				while E:
					A=c();x=Q(D,N,B.byref(A),B.sizeof(A))
					if not x:break
					if A.State==t and A.RegionSize>0:
						i=B.create_string_buffer(A.RegionSize);j=B.c_size_t()
						if P(D,A.BaseAddress,i,A.RegionSize,B.byref(j)):
							if G in i[:j.value]:
								U+=1
								if U<=10:d(f"Found in process {f}");Z.append(('Process',V,G.decode(),A.BaseAddress));C.warning(f"⚠️Found bytes '{G.decode()}' in process '{V}' at address {A.BaseAddress:#x}");g=E;h.append((G.decode(),A.BaseAddress))
								else:break
					N+=A.RegionSize
				if U>10:break
			if g:
				W=[]
				for(G,N)in h:W.append({K:'Bytes',n:G,o:E});W.append({K:'Address',n:f"{N:#x}",o:E})
				y={k:'Detected Bytes in Process','fields':W,l:16711680};J.append(y);H(D)
	if J:Y['embeds']=J;z=X.post(q,json=Y);p.showerror('Anticheat','Detect code: 1');a.mainloop()
	if D is not L:H(D)
h=[b'exechack.cc',b'aimbot',b'antiaim']
g(e,h)
C.info('Program finished')
input('Press Enter to exit...')
