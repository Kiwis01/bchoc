import argparse
import struct
from collections import namedtuple
import os

def show_items(case_id):
    # Hardcoded file path or use an environment variable
    file_path = os.environ.get("BCHOC_FILE_PATH", "blockchain")
    
    block_format = struct.Struct("32s d 32s 32s 12s 12s 12s I")
    block_head = namedtuple('Block_Head', 'hash timestamp case_id item_id state length')

    items = []

    with open(file_path, 'rb') as fp:
        while True:
            try:
                block_content = fp.read(block_format.size)
                if not block_content:
                    break
                block_head_data = block_format.unpack(block_content)
                curr_block_head = block_head(*block_head_data)
                if curr_block_head.case_id.rstrip(b'\x00').decode() == case_id:
                    items.append(curr_block_head.item_id.rstrip(b'\x00').decode())
            except Exception as e:
                print("Error:", e)
                break

    print(f"Items in Case {case_id}: {items}")
