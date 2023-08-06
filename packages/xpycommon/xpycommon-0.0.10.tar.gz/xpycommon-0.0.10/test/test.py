#!/usr/bin/env python3.10

from xpycommon import libbluetooth, libc

def main():
    print(libbluetooth)
    print(libbluetooth.str2ba)
    
    print(libc.writev)

if __name__ == '__main__':
    main()
