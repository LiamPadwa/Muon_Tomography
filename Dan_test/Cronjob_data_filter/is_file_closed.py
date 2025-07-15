import argparse
import sys


def check_file_closed(file_path: str) -> bool:
    try:
        file_obj = open(file_path, "r")
        if file_obj.closed:
            print(f'File {file_path} is closed and safe to use')
            file_obj.close()
            return True
        print(f'File {file_path} is opened and cannot be used')
        return False

    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f'Error checking file: {e}')
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check if a file is closed")
    parser.add_argument("file", help="Path to the file to check")
    args = parser.parse_args()

    # script returns True/False when ran from the terminal
    if check_file_closed(args.file):
        sys.exit(0)
    else:
        sys.exit(1)



# if __name__ == '__main__':
#     # check if file is closed
#     check_file_closed(file_obj)

#     print("Now closing the file.")
#     # close the file
#     file_obj.close()

#     # again check if file is closed
#     check_file_closed(file_obj)