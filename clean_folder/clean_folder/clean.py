import re
import sys
from pathlib import Path
import shutil

# Define a string containing Ukrainian symbols and their corresponding translations
UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r",
               "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

# Create a dictionary to store the translation mappings
TRANS = {}

images_files = list()
video_files = list()
documents_files = list()
audio_files = list()
archives_files = list()
folders = list()
others = list()
unknown = list()
extensions = set()

registered_extensions = {
    "JPEG": images_files, "PNG": images_files, "JPG": images_files, "SVG": images_files,

    "AVI": video_files, "MP4": video_files, "MOV": video_files, "MKV": video_files,

    "DOC": documents_files, "DOCX": documents_files, "TXT": documents_files, "PDF": documents_files,
    "XLSX": documents_files, "PPTX": documents_files,

    "MP3": audio_files, "OGG": audio_files, "WAV": audio_files, "AMR": audio_files,

    "GZ": archives_files, "TAR": archives_files, "ZIP": archives_files,
    '': unknown
}


# Populate the dictionary with Unicode code points of Ukrainian symbols as keys and their translations as values
for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()


def normalize(name):
    """
    Normalize a string by replacing Ukrainian symbols and non-word characters.

    This function takes a string and replaces Ukrainian symbols with their Latin counterparts,
    as defined in the `TRANS` dictionary. Additionally, it replaces non-word characters with
    underscores to ensure a valid filename.
    :param name: The string to be normalized.
    :return: The normalized string.
    """
    # Split the string into name and extension
    name, *extension = name.split('.')

    # Translate Ukrainian symbols and replace non-word characters with underscores
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', '_', new_name)

    return f"{new_name}"


def get_extensions(file_name):
    """
    Extracts the file extension from the given file name and converts it to uppercase.

    :param file_name: The name of the file.
    :return: The uppercase file extension.
    """
    return Path(file_name).suffix[1:].upper()


def scan(folder):
    """
    This function iterates through the items within the specified folder. If an item is a directory,
    it recursively scans its subdirectories. If an item is a file, it uses the `get_extensions`
    function to extract its file extension. The file is then categorized into appropriate lists
    based on its extension, using the `registered_extensions` dictionary. The function also keeps
    track of different file extensions in the `extensions` set.

    :param folder:
    :return:
    """
    for item in folder.iterdir():
        if item.is_dir():
            # If the item is a directory and not one of the special folders, continue scanning
            if item.name not in ("Images", "Documents", "Audio", "Video", "Archives", "Others", "Unknown"):
                folders.append(item)
                scan(item)
            continue

        # Get the file extension using the `get_extensions` function
        extension = get_extensions(file_name=item.name)
        new_name = folder / item.name
        try:
            # Use the `registered_extensions` dictionary to categorize the file
            container = registered_extensions[extension]
            extensions.add(extension)
            container.append(new_name)
        except KeyError:
            # If the extension is not found in the dictionary, categorize it as 'Others'
            others.append(new_name)
            extensions.add(extension)


def handle_file(path, root_folder, dist):
    """
    Move and normalize a file to a specific directory.

    :param path: The path to the file.
    :param root_folder: The root folder where the target folder will be created.
    :param dist: The sub-folder where the file will be moved
    :return: None
    """
    # Creates the target folder if it doesn't exist
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    # Normalize the file name and combine this with origin extension
    new_path = target_folder / (normalize(path.name) + path.suffix)

    # Move the file to the new path
    path.replace(new_path)


def handle_archive(path, root_folder):
    """
    Handle the extraction and organization of an archive file.

    This function takes an archive file path and a root folder path as input. It creates a normalized sub-folder name
    using the base name of the archive file (without extension) and attempts to unpack the contents of the archive
    into the newly created sub-folder within the specified root folder. If the unpacking is successful, the original
    archive file is removed. If any errors occur during unpacking or folder creation, the function handles them
    gracefully by removing any newly created sub-folders and ignoring the error.

    :param path: The path to the file.
    :param root_folder: The root folder where the target folder will be created.
    :return: None
    """
    #
    new_name = normalize(path.with_suffix('').name)

    # Creates the archive folder if it doesn't exist
    archive_folder = root_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        # Unpack the archive into the sub-folder
        shutil.unpack_archive(str(path.resolve()), str(archive_folder))

        # Handle any potential errors during unpacking or folder operations
        # by removing the sub-folder and ignoring the error
    except shutil.ReadError:
        archive_folder.rmdir()
    except FileNotFoundError:
        archive_folder.rmdir()
    except OSError:
        pass

    # Remove the original archive file
    path.unlink()


def remove_empty_folders(path):
    """
    Recursively remove empty folders within a given path.

    This function traverses the specified path and its subdirectories to identify and remove empty folders. It first
    recursively calls itself to ensure that all subdirectories are processed before their parent directories. If an
    empty folder is encountered, it attempts to remove it using the 'rmdir' method. If the folder is not empty or if
    an error occurs during removal, the function continues to the next iteration.

    :param path: The root path to start the search for empty folders.
    :return: None
    """
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def get_folder_object(root_path):
    """
    Recursively remove empty folders and specific folders within a given root path.

    This function traverses the specified root path to identify and remove specific folders that were created during
    the organization process but remain empty or no longer needed. It uses the 'remove_empty_folders' function to
    perform the removal of empty folders. If the folder is not empty or if an error occurs during removal, the
    function continues to the next iteration.

    :param root_path: The root path to start the search for empty folders.
    :return: None
    """
    for folder in root_path.iterdir():
        if folder.is_dir():
            remove_empty_folders(folder)
            try:
                folder.rmdir()
            except OSError:
                pass


def main():
    path = sys.argv[1]
    print(f'Start in {path}')

    folder_path = Path(path)
    """
    Organize files within a specified folder by categorizing and moving them to appropriate sub-folders.

    This function orchestrates the entire organization process. It first uses the 'scan' module to identify different
    types of files and their extensions within the specified folder. Then, it iterates through each categorized list
    of files (images, documents, audio, video, others, unknown, archives).

    :param folder_path: The path to the folder containing the unorganized files.
    :return: None
    """
    scan(folder_path)

    for file in images_files:
        file = Path(file)
        handle_file(file, folder_path, "Images")

    for file in documents_files:
        file = Path(file)
        handle_file(file, folder_path, "Documents")

    for file in audio_files:
        file = Path(file)
        handle_file(file, folder_path, "Audio")

    for file in video_files:
        file = Path(file)
        handle_file(file, folder_path, "Video")

    for file in others:
        file = Path(file)
        handle_file(file, folder_path, "Others")

    for file in unknown:
        file = Path(file)
        handle_file(file, folder_path, "Unknown")

    for file in archives_files:
        file = Path(file)
        handle_archive(file, folder_path)

        get_folder_object(folder_path)


if __name__ == '__main__':
    path = sys.argv[1]
    print(f'Start in {path}')

    arg = Path(path)
    main(arg.resolve())