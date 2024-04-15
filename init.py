import os
import sys
import struct

from datetime import datetime

blockFormat = struct.Struct("32s d 32s 32s 12s 12s 12s I")


def writeInit(filepath):
    dataFormat = struct.Struct("14s")
    f = open(filepath, "wb")  # Open File
    ############ Build Init Block#############
    # Hash = null/empty for init block
    prevHash = str.encode("")
    # Timestamp
    time = 0
    # Case and item ID
    #caseID = str.encode("")
    caseID = b"0"*32
    #itemID = str.encode("")
    itemID = b"0"*32
    # State
    bState = b"INITIAL\0\0\0\0\0"
    # Creator and Owner
    #bCreator = str.encode("")
    bCreator = b"\0"*12
    # bOwner = str.encode("")
    bOwner = b"\0"*12
    # Data: Initial Block 14 bytes
    bDataLength = 14
    bData = b"Initial block\0"

    # Pack Block Values
    packedBlock = blockFormat.pack(
        prevHash, time, caseID, itemID, bState, bCreator, bOwner, bDataLength
    )
    packedData = dataFormat.pack(bData)

    # Write to file
    f.write(packedBlock)
    f.write(packedData)

    f.close()


def init(filepath):
    # blockFormat = struct.Struct("32s d 32s 32s 12s 12s 12s I")
    if os.path.isfile(filepath):
        try:
            f = open(filepath, "rb")
            f.seek(104)
            initCheck = f.read(7).decode("ASCII")
            f.close()
        except:
            print("File Empty")
            writeInit(filepath)
        else:
            if (initCheck == "INITIAL"):
                print("Blockchain file found with INITIAL block.")
            else:
                sys.exit("Error: Invalid File")
    else:
        print("Blockchain file not found. Created INITIAL block.")
        writeInit(filepath)
