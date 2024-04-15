#!/usr/bin/python3
import os
import sys
import argparse
import uuid
import hashlib
import struct

# non-standard Libs
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# User Modules
from init import init
from add import add

# AES_KEY = b"R0chLi4uLi4uLi4=" to be hard coded in you program
key = b"R0chLi4uLi4uLi4="  ###Hardcoded Key###########


# Check ENV Vars
# This first check should be enough to determine that it is being run in gradescope
if "BCHOC_FILE_PATH" in os.environ:
    filepath = os.environ.get("BCHOC_FILE_PATH")  # For gradescope env variable
    # passwords = {
    #     "POLICE": str(os.environ.get("BCHOC_PASSWORD_POLICE")),
    #     "LAWYER": str(os.environ.get("BCHOC_PASSWORD_LAWYER")),
    #     "ANALYST": str(os.environ.get("BCHOC_PASSWORD_ANALYST")),
    #     "EXECUTIVE": str(os.environ.get("BCHOC_PASSWORD_EXECUTIVE")),
    #     "CREATOR": str(os.environ.get("BCHOC_PASSWORD_CREATOR")),
    # }
    passwords = {
        str(os.environ.get("BCHOC_PASSWORD_POLICE")): "POLICE",
        str(os.environ.get("BCHOC_PASSWORD_LAWYER")): "LAWYER",
        str(os.environ.get("BCHOC_PASSWORD_ANALYST")): "ANALYST",
        str(os.environ.get("BCHOC_PASSWORD_EXECUTIVE")): "EXECUTIVE",
        str(os.environ.get("BCHOC_PASSWORD_CREATOR")): "CREATOR",
    }
else:
    filepath = "blockchain"  # Default
    ####PASSWORDS#######
    # passwords = {
    #     "POLICE": "P80P",
    #     "LAWYER": "L76L",
    #     "ANALYST": "A65A",
    #     "EXECUTIVE": "E69E",
    #     "CREATOR": "C67C",
    # }
    passwords = {
        "P80P": "POLICE",
        "L76L": "LAWYER",
        "A65A": "ANALYST",
        "E69E": "EXECUTIVE",
        "C67C": "CREATOR",
    }

# Grab Arguments
parse = argparse.ArgumentParser()
parse.add_argument("command", help="Command to execute")
parse.add_argument("-c", dest="caseID")
parse.add_argument("-i", dest="itemID", action="append")
parse.add_argument("-g", dest="creator")
parse.add_argument("-p", dest="password", type=str)
parse.add_argument("-n", dest="numEntries", type=int)
parse.add_argument("-r", dest="rev", action="store_true", help="Reverse show history")
parse.add_argument("-y", dest="reason")
parse.add_argument("-o", dest="owner")
args = parse.parse_args()

argDict = dict()

if args.command != "verify" and args.command != "init":
    if args.command == "add":

        caseID = args.caseID
        itemID = args.itemID
        creator = args.creator
        
        if caseID and itemID:
            # Check for correct creator password
            try:
                if passwords[args.password] != "CREATOR":
                    sys.exit("Error: Incorrect Password")
                owner = passwords[args.password]
            except:
                sys.exit("Error: Missing Password")
            if os.path.isfile(filepath):
                add(filepath, caseID, itemID, creator, owner)  # Add to blockchain
            else:
                init(filepath)
                add(filepath, caseID, itemID, creator, owner)
        else:
            sys.exit("Error: Missing one or more arguments")
elif args.command == "checkout":
    if args.itemID and args.password:
        authenticated = False
        for role, pwd in passwords.items():
            if args.password == pwd:
                authenticated = True
                break
        if not authenticated:
            sys.exit("Error: Invalid password")
        # Perform checkout action
        print(f"Performing checkout for item ID: {args.itemID}")
    # Implement the checkin action here
    else:
        sys.exit("Error: Missing itemID or password argument")
elif args.command == "checkin":
    if args.itemID and args.password:
            # Placeholder for authentication logic using passwords
        authenticated = False
        for role, pwd in passwords.items():
            if args.password == pwd:
                authenticated = True
                break
        if not authenticated:
            sys.exit("Error: Invalid password")

        # Perform checkin action
        print(f"Performing checkin for item ID: {args.itemID}")
    # Implement the checkin action here
    else:
        sys.exit("Error: Missing itemID or password argument")
elif args.command == "init":
    init(filepath)
elif args.command == "verify":
    # Run Verify Function
    print("temp")
