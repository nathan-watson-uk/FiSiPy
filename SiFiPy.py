import getopt
import sys
import time

from file_signature_dict import file_signature_dict, help_menu_text


def get_file_signature_from_file_object(file_obj, block_size=16):
    block = file_obj.read(block_size).hex().upper()  # Convert the
    return " ".join(block[i:i + 2] for i in range(0, len(block), 2))


def get_file_signature_from_directory(directory, block_size=16):
    with open(f"{directory}", "rb") as f:
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

    try:
        return dictionary[file_signature_found]

    except KeyError:
        sys.exit("Unable To Find Matching File Signature -"
                 " Please Submit Your File Signature to the Discord for Manual Inspection")


def main():
    short_opts = "hf:b:"

    long_opts = ["help", "file=", "block_size="]

    argument_list = sys.argv[1:]

    # Block size is automatically set to the largest one in the file signature dictionary unless changed.
    dependent_block_size = len(max(file_signature_dict, key=len))

    filename = None

    try:
        arguments, values = getopt.getopt(argument_list, short_opts, long_opts)

    except getopt.error as error:
        sys.exit(f"{error}\n")

    for argument, value in arguments:
        if argument in ("-h", "--help"):
            print(f"\n{help_menu_text}\n")

        elif argument in ("-f", "file="):
            filename = str(value)

        elif argument in ("-b", "block_size="):
            dependent_block_size = int(value)

    if not filename:
        sys.exit("File Signature Match Failed - No File Provided - Try Using -f [filename]")

    header = get_file_signature_from_directory(filename, block_size=dependent_block_size)

    find_signature_in_dict(dictionary=file_signature_dict, file_header=header)


if __name__ == "__main__":
    main()
