import os


class FileOperator:
    """
    Operating files

    Methods:
        read_file(file_path): Read file
        create_file(file_path): Create file
        write_file(file_path): Write file
        delete_file(file_path): Delete file
    """
    @staticmethod
    def read_file(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error：file not found: '{file_path}'")
            return None
        except Exception as e:
            print(f"Unexpected error when reading file: {e}")
            return None

    @staticmethod
    def create_file(file_path):
        try:
            with open(file_path, 'x', encoding='utf-8'):
                # print(f"file created: '{file_path}'")
                return True
        except FileExistsError:
            print(f"file exist: '{file_path}'")
            return False
        except Exception as e:
            print(f"Unexpected error when creating file: {e}")
            return False

    @staticmethod
    def write_file(file_path, content, mode='w'):
        if mode not in ('w', 'a'):
            print("Write mode no allowed")
            return False
        try:
            with open(file_path, mode, encoding='utf-8') as file:
                file.write(content)
                # print(f"Write file: '{file_path}'")
                return True
        except Exception as e:
            print(f"Unexpected error when writing file: {e}")
            return False

    @staticmethod
    def delete_file(file_path):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                # print(f"Delete file: '{file_path}'")
                return True
            else:
                print(f"Error：file not exist'{file_path}'")
                return False
        except Exception as e:
            print(f"Unexpected error when deleting file:  {e}")
            return False
