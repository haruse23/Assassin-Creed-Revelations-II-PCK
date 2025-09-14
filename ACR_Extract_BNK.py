import struct
import os
import sys

def Extract_BNK(path, out_dir):
    with open(path, "rb") as f:
        #BKHD Section

        BKHD_data = f.read(8)
        
        Magic = BKHD_data[0:4] # BKHD

        BKHD_Size = struct.unpack_from("<I", BKHD_data, 0x4)[0]

        f.seek(BKHD_Size, 1)

        # DIDX Section
        DIDX_data = f.read(8)
        
        Magic = DIDX_data[0:4] # DIDX

        DIDX_Size = struct.unpack_from("<I", DIDX_data, 0x4)[0]
        
        WEM_Entries = []
        while True:
            data = f.read(4)

            if data == b"DATA":
                break
            
            else:
                WEM_ID = struct.unpack_from("<I", data, 0x00)[0]

                WEM_Entry = f.read(8)

                WEM_Offset =  struct.unpack_from("<I", WEM_Entry, 0x00)[0] # Relative to Size Field of DATA Section

                WEM_Size = struct.unpack_from("<I", WEM_Entry, 0x04)[0]

                WEM_Entries.append((WEM_ID, WEM_Offset, WEM_Size))

        #DATA Section
        Magic = data # DATA

        DATA_Size = struct.unpack_from("<I", f.read(4), 0x00)[0]

        DATA_Size_pos = f.tell()

        counter = 0
        for WEM_ID, WEM_Offset, WEM_Size in WEM_Entries:
            f.seek(WEM_Offset + DATA_Size_pos)

            WEM_Data = f.read(WEM_Size)

            os.makedirs(out_dir, exist_ok=True)  
            out_path = os.path.join(out_dir, f"chunk_{counter}.wem")
            with open(out_path, "wb") as out:
             out.write(WEM_Data)

            counter+=1


if __name__ == "__main__":
    # Drag-and-drop support: take first file argument
    if len(sys.argv) < 2:
        print("Drag and drop a BNK file or more onto this script.")
        input("Press Enter to exit...")
        sys.exit(0)

    bnk_path = sys.argv[1]

    # Folder next to BNK, named after the BNK file (without extension)
    output_folder = os.path.join(
        os.path.dirname(bnk_path),
        os.path.splitext(os.path.basename(bnk_path))[0]
    )

    Extract_BNK(bnk_path, output_folder)
