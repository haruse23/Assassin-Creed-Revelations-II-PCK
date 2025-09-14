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

        if "eng" in path.lower():
            # Skip extra bytes for English variant
            f.seek(20, 1)

            Length = struct.unpack_from("<I", f.read(4), 0x00)[0]
            print(Length)
            f.seek(Length-8, 1)

        else:
            # Skip standard bytes
            f.seek(12, 1)

            Length = struct.unpack_from("<I", f.read(4), 0x00)[0]

            f.seek(Length, 1)




       

        BNK_Count_Bytes = f.read(4)
        BNK_Count = struct.unpack_from("<I", BNK_Count_Bytes, 0x00)[0]
        print(BNK_Count)

        BNK_Entries = []
        for i in range(BNK_Count):
            Entry = f.read(24)

            Hash = struct.unpack_from("<I", Entry, 0x0)[0]

            # Unknown Field, the value BNK_Offset Multiplied by maybe ?

            BNK_Size = struct.unpack_from("<I", Entry, 0x8)[0]

            # Unknown Field
            
            BNK_Offset = struct.unpack_from("<I", Entry, 0x10)[0] * 2048 

            # Unknown Field

            BNK_Entries.append((Hash, BNK_Size, BNK_Offset))


        for Hash, BNK_Size, BNK_Offset in BNK_Entries:
            print(f"BNK at {BNK_Offset:x}, Hash={Hash:x}, Size={BNK_Size}")
            
            if BNK_Size == 0:
                print(f"Skipping empty BNK...")
                continue

            f.seek(BNK_Offset)

            BNK_data = f.read(BNK_Size)
            
            BNKName = f"BNK_{Hash}"

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

    # Folder next to PCK, named after the BNK file (without extension)
    output_folder = os.path.join(
        os.path.dirname(pck_path),
        os.path.splitext(os.path.basename(pck_path))[0]
    )

Extract_PCK(pck_path, output_folder)

            
        

