# import os
# import glob
# import re


# def remove_files_with_suffix(directory, suffix):
#     # Regular expression to match filenames that end with "_number.jpg"
#     pattern = re.compile(r".*_\d+\.jpg$")

#     # Iterate over all files in the specified directory
#     for filename in os.listdir(directory):
#         file_path = os.path.join(directory, filename)

#         # Check if it's a file and does not match the pattern
#         if os.path.isfile(file_path) and not pattern.match(filename):
#             try:
#                 os.remove(file_path)
#                 print(f"Removed: {file_path}")
#             except Exception as e:
#                 print(f"Error removing {file_path}: {e}")
#     # Create a pattern to match files with the specified suffix
#     # pattern = os.path.join(directory, f"*{suffix}")

#     # # Get a list of all files that match the pattern
#     # files_to_remove = glob.glob(pattern)

#     # # Remove each file
#     # for file_path in files_to_remove:
#     #     try:
#     #         os.remove(file_path)
#     #         print(f"Removed: {file_path}")
#     #     except Exception as e:
#     #         print(f"Error removing {file_path}: {e}")


# # Directory containing the files
# # Replace with the actual path to your folder


import os
import re


def remove_files_without_suffix(directory):
    # Regular expression to match filenames that end with "_number.jpg"
    pattern = re.compile(r".*_\d+\.jpg$")

    # Iterate over all files in the specified directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Check if it's a file and does not match the pattern
        if os.path.isfile(file_path) and not pattern.match(filename):
            try:
                os.remove(file_path)
                print(f"Removed: {file_path}")
            except Exception as e:
                print(f"Error removing {file_path}: {e}")

# Directory containing the files
# directory = "/path/to/your/folder"  # Replace with the actual path to your folder


# Remove the files
directory = "final_milano_Bella-Sposa_copy"
remove_files_without_suffix(directory)


# Remove the files
# remove_files_with_suffix(directory, suffix)
