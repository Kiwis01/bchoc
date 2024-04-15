import os
import sys
import struct
import hashlib
from datetime import datetime

# non-standard Libs
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# import maya

###Hardcoded Key###########
key = b"R0chLi4uLi4uLi4="


def add(filePath, caseID, itemID, creator, owner):
    # Encrypt the caseID
    cipher = AES.new(key, AES.MODE_ECB)
    encryptCID = cipher.encrypt(pad(caseID.encode("ascii"), 16))
    # encryptIID = []

    # open the file to read
    f = open(filePath, "rb")

    # Struct format of block head
    blockHeadFormat = struct.Struct("32s d 32s 32s 12s 12s 12s I")
    blockHash = ""  # Holds previous blocks hash
    blockHead = ""  # Holds previous blocks head
    blockDataContent = ""  # Holds previous blocks data
    blockIDs = []  # Holds previous blocks id's to check for dupes
    while True:
        try:
            blockHead = f.read(blockHeadFormat.size)
            currBlock = blockHeadFormat.unpack(blockHead)
            prevID = currBlock[3]
            blockIDs.append(prevID)
            dataLength = currBlock[7]
            blockDataFormat = struct.Struct(str(dataLength) + "s")
            blockDataContent = f.read(blockDataFormat.size)
            # print(blockDataContent)

        except:
            break  # This indicates final block has been reached

    # for id in blockIDs:
    #     print(cipher.decrypt(bytes(id).rstrip(b'\x00')).rstrip(b'\x0c'))
    #     if cipher.decrypt(bytes(id).rstrip(b'\x00')).rstrip(b'\x0c') in itemID:
    #         sys.exit("Error: Duplicate Item ID detected")

    # Check for duplicate IDs
    for id in itemID:
        # if pad(cipher.encrypt(pad(id.encode("ascii"), 16)), 32) in blockIDs:
        #     sys.exit("Error: Duplicate Item ID detected")
        
        # Begin to build the new block
        blockHash = hashlib.sha1(blockHead + blockDataContent).digest()
        timestamp = datetime.timestamp(datetime.now())
        # encryptCID
        encryptIID = cipher.encrypt(pad(id.encode("ascii"), 16))
        blockState = b"CHECKEDIN"
        creator = creator.encode("ascii")
        owner = owner.encode("ascii")
        dataLength = 0
        newBlockData = b""

        packedBlockHead = blockHeadFormat.pack(
            blockHash,
            timestamp,
            encryptCID,
            encryptIID,
            blockState,
            creator,
            owner,
            dataLength,
        )
        # packedBlockData = blockDataFormat.pack(newBlockData)

        f = open(filePath, "ab")
        f.write(packedBlockHead)
        # f.write(packedBlockData)
        f.close()

        print("Added item: " + id)
        print("Status: CHECKEDIN")
        print("Time of action:", datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z")
