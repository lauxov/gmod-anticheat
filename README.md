# Memory Scanner AC

DEMO: https://youtu.be/k8tIRj6HT_0

⚠️ The webhook link is not protected in any way. It can be easily dumped or found in the Net logger

This Python script provides a memory scanning functionality for finding sequences of bytes within the memory of running processes on Windows. It utilizes the Windows API and performs low-level memory operations using the `ctypes` module.

## Requirements

- `ctypes`
- `ctypes.wintypes`
- `winsound`

![image](https://github.com/lauxov/gmod-anticheat/assets/110423050/c1b92411-4be7-43a2-b5e6-f71029036288) ![image](https://github.com/lauxov/gmod-anticheat/assets/110423050/1c6b481e-a7fa-4684-a9f9-0d721b2fcdad)
![image](https://github.com/lauxov/gmod-anticheat/assets/110423050/39a25d29-0b11-446d-a4b2-9853c8ef56d7)



## Usage

To use this script, follow these steps:

1. Install the required modules mentioned above, if not already installed.
2. Call the `find_bytes` function, providing a list of process names and a list of bytes to search for in the memory of those processes.
3. The script will loop over each process with a matching name, open a handle to it, and search for the specified bytes within its memory using the `ReadProcessMemory` function.
4. If the bytes are found, the script will play a sound using the `winsound` module.

Please note that this script is intended for educational purposes only and should not be used to modify the memory of a running process without proper authorization.

## Code

The script defines the following structures, constants, and functions:

### Structures

- `PROCESSENTRY32`: Represents a process entry in a system snapshot and is used to iterate over all running processes on the system.
- `MEMORY_BASIC_INFORMATION`: Represents a block of memory in a process and is used to query information about the memory layout of a process.

### Functions

- `OpenProcess`: Obtains a handle to a process with the specified access rights.
- `ReadProcessMemory`: Reads data from the memory of a process.
- `CloseHandle`: Closes a handle to a process.
- `VirtualQueryEx`: Queries information about a block of memory in a process.
- `CreateToolhelp32Snapshot`: Creates a snapshot of the system and allows iterating over all running processes.

## Disclaimer

This script is not intended for malicious purposes. It is designed for educational and research purposes to understand memory scanning techniques. Use it responsibly and with proper authorization.
