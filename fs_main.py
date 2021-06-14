from file_signature_dict import file_signature_dict


def get_file_signature_from_file_object(file_obj, block_size=16):
    block = file_obj.read(block_size).hex().upper()  # Convert the
    return " ".join(block[i:i + 2] for i in range(0, len(block), 2))


def get_file_signature_from_directory(directory, block_size=16):
    with open(directory, "rb") as f:
        block = f.read(block_size).hex().upper()
        return " ".join(block[i:i + 2] for i in range(0, len(block), 2))


def find_signature_in_dict(dictionary, file_header):
    split_file_header = file_header.split(" ")
    file_signature_found = ""

    for key in (dictionary.keys()):

        if ' '.join(split_file_header[0:len(key.split(" "))]) == key:
            if len(key) > len(file_signature_found):
                file_signature_found = key

            print(f"File Signature - {key}\n")
            for sig_details in dictionary[key]:
                print(f"{sig_details[0]} | {sig_details[1]}")

            print("\n")

    return dictionary[file_signature_found]

# Define the filename
filename = "work.docx"

# There's no point getting more of the 512 byte header than needed.
# To do this we find the largest header in the file signature dictionary and use that as the block size.
dependent_block_size = len(max(file_signature_dict, key=len))

# Gets the header by opening the file and converting/spliting hex --> strings
header = get_file_signature_from_directory(filename, block_size=dependent_block_size)


find_signature_in_dict(dictionary=file_signature_dict, file_header=header)
