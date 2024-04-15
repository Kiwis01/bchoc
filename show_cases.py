
import struct
import os

def show_cases():
    # Hardcoded file path or use an environment variable
    file_path = os.environ.get("BCHOC_FILE_PATH", "blockchain")

    block_format = struct.Struct("32s d 32s 32s 12s 12s 12s I")
    block_head = struct.Struct("32s d 32s 32s 12s 12s 12s I")

    cases = []

    with open(file_path, 'rb') as fp:
        while True:
            try:
                block_content = fp.read(block_format.size)
                if not block_content:
                    break
                block_head_data = block_format.unpack(block_content)
                cases.append(block_head_data[2].decode('utf-8').strip('\x00'))
            except Exception as e:
                print("Error:", e)
                break

    print("Cases in Blockchain:", cases)


