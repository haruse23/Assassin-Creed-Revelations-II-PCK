import struct
import os
import sys

def Extract_PCK(path, out_dir):
    with open(path, "rb") as f:
        data = f.read(16)

        Magic = data[0:4] # AKPK

        PCK_Header_Size = struct.unpack_from("<I", data, 0x4)[0]

        # Unknown Field

        Version = struct.unpack_from("<I", data, 0xC)[0] # Likely Version (0x34)

        f.seek(60, 1)

        BNK_Count_Bytes = f.read(4)
        BNK_Count = struct.unpack_from("<I", BNK_Count_Bytes, 0x00)[0]
        print(BNK_Count)

        BNK_Entries = []
        for i in range(BNK_Count):
            Entry = f.read(24)

            Hash = struct.unpack_from("<I", Entry, 0x0)[0]

            # Unknown Field

            BNK_Size = struct.unpack_from("<I", Entry, 0x8)[0]

            # Unknown Field
            
            # Unknown Field

            # Unknown Field

            BNK_Entries.append((Hash, BNK_Size))

        offsets = []
        pos = 0
        data = f.read()
        while True:
            pos = data.find(b"BKHD", pos)
            if pos == -1:
                break
            offsets.append(pos)
            pos += 1  # move forward to avoid infinite loop

        for offset, (Hash, BNK_Size) in zip(offsets, BNK_Entries):
             print(f"BNK at {offset:x}, Hash={Hash:x}, Size={BNK_Size}")

             BNK_data = data[offset : offset + BNK_Size]
             
             STID_pos = BNK_data.rfind(b"STID")
             
             STID_Magic = BNK_data[STID_pos: STID_pos + 4] # STID (String ID Section)

             STID_BNKName_Length = BNK_data[STID_pos + 20]

             BNKName = BNK_data[STID_pos + 20 + 1: STID_pos + 20 + 1 + int(STID_BNKName_Length)]
            
             BNKName = BNKName.decode("ascii", errors="replace")
             print(BNKName)

             os.makedirs(out_dir, exist_ok=True)  
             out_path = os.path.join(out_dir, f"{BNKName}.bnk")
             with open(out_path, "wb") as out:
                out.write(BNK_data)


if __name__ == "__main__":
    # Drag-and-drop support: take first file argument
    if len(sys.argv) < 2:
        print("Drag and drop a PCK file or more onto this script.")
        input("Press Enter to exit...")
        sys.exit(0)

    pck_path = sys.argv[1]
    output_folder = os.path.join(os.path.dirname(pck_path), "Extracted_BNKs")
    Extract_PCK(pck_path, output_folder)


            
        