import os
import shutil
import time

# Function to move file and handle duplicates using timestamp
def duplicate_file_handler(src_path, dest_dir):
    try:
        filename = os.path.basename(src_path)
        dest_path = os.path.join(dest_dir, filename)

        # Check if a file with the same name exists in the destination directory
        if os.path.exists(dest_path):
            # Append the current timestamp to the filename
            base, ext = os.path.splitext(filename)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            new_filename = f"{base}_{timestamp}{ext}"
            dest_path = os.path.join(dest_dir, new_filename)
            print(f"Duplicate found, renaming to: {new_filename}")

        # Move the file to the destination directory
        shutil.move(src_path, dest_path)
        print(f"Moved: {src_path} -> {dest_path}")

    except FileNotFoundError:
        print(f"File not found: {src_path}")
    except PermissionError:
        print(f"Permission denied for file: {src_path}")
    except Exception as e:
        print(f"An error occurred while moving {src_path}: {str(e)}")

# Organize and move files based on their extension
def organize_downloaded_files(download_dir, csv_dir, dat_dir, others_dir):
    # Loop through all files in the source directory
    try:
        for filename in os.listdir(download_dir):
            file_path = os.path.join(download_dir, filename)
            
            if os.path.isfile(file_path):
                file_extension = os.path.splitext(filename)[1].lower()

                if file_extension == '.csv':
                    duplicate_file_handler(file_path, csv_dir)
                elif file_extension == '.dat':
                    duplicate_file_handler(file_path, dat_dir)
                else:
                    # Move files with other extensions to the 'others' folder
                    duplicate_file_handler(file_path, others_dir)

    except Exception as e:
        print(f"An error occurred while organizing the files: {str(e)}")

# Main code to execute the organization process
if _name_ == "_main_":
    download_dir = "downloads"
    
    # Create subdirectories for CSV, DAT, and others files
    csv_dir = os.path.join(download_dir, 'csv_files')
    dat_dir = os.path.join(download_dir, 'dat_files')
    others_dir = os.path.join(download_dir, 'others')  # Directory for other files

    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
        print(f"Created directory: {csv_dir}")
    if not os.path.exists(dat_dir):
        os.makedirs(dat_dir)
        print(f"Created directory: {dat_dir}")
    if not os.path.exists(others_dir):
        os.makedirs(others_dir)
        print(f"Created directory: {others_dir}")

    # Organize the downloaded files
    organize_downloaded_files(download_dir, csv_dir, dat_dir, others_dir)