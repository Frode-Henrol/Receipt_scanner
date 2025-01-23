import os

def rename_images_in_folder(folder_path):
    # List all files in the directory
    files = os.listdir(folder_path)

    # Sort files to maintain order (optional, based on file names)
    files.sort()

    # Loop through all files in the folder
    for file_name in files:
        # Get the full path of the file
        file_path = os.path.join(folder_path, file_name)

        # Check if it's a file (and not a directory)
        if os.path.isfile(file_path):
            # Get the file extension (e.g., .jpg, .png)
            file_extension = os.path.splitext(file_name)[1]

            # Check if the file is an image (you can customize the extensions)
            if file_extension.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
                # Find the next available number for the new file name
                counter = 1
                while True:
                    new_file_name = f"picture{counter}{file_extension}"
                    new_file_path = os.path.join(folder_path, new_file_name)

                    # Check if the new file path already exists
                    if not os.path.exists(new_file_path):
                        break
                    counter += 1

                # Rename the file
                os.rename(file_path, new_file_path)

                # Print a message (optional)
                print(f"Renamed: {file_name} -> {new_file_name}")


# Example usage
folder_path = os.path.join(os.getcwd(),"images")

rename_images_in_folder(folder_path)
