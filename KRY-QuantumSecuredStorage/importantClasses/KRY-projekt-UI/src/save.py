""" Saving keys to archive.

    Author: Pavel Podlužanský
    email: xpodlu01@vutbr.cz
"""


import pyzipper
import os

# Zip the files from given directory that matches the filter
def save():
    folder_path="./out/"
    parent_folder = os.path.dirname(folder_path)
    # Retrieve the paths of the folder contents.
    contents = os.walk(folder_path)
    try:
        zip_file = pyzipper.AESZipFile('save.7z','w',compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES)
        zip_file.setpassword(b"PASSWORD")
        for root, folders, files in contents:
            # Include all subfolders, including empty ones.
            for folder_name in folders:
                absolute_path = os.path.join(root, folder_name)
                relative_path = absolute_path.replace(parent_folder + '\\',
                                                    '')
                print ("Adding '%s' to archive." % absolute_path)
                zip_file.write(absolute_path, relative_path)
            for file_name in files:
                absolute_path = os.path.join(root, file_name)
                relative_path = absolute_path.replace(parent_folder + '\\',
                                                    '')
                print ("Adding '%s' to archive." % absolute_path)
                zip_file.write(absolute_path, relative_path)

        print ("created successfully save.7z." )

    except IOError as message:
        print (message)
        sys.exit(1)
    except OSError as message:
        print(message)
        sys.exit(1)
    except zipfile.BadZipfile as message:
        print (message)
        sys.exit(1)
    finally:
        zip_file.close()