import os


def get_file_codes(folder):
    """Return a set of file codes extracted from filenames in the given folder."""
    codes = set()
    for filename in os.listdir(folder):
        if '_' in filename:
            code = filename.split('_', 1)[0]
            codes.add(code)
    return codes


def delete_matching_files(reference_folder, target_folder):
    """Delete files in the target folder if their code matches any code in the reference folder."""
    reference_codes = get_file_codes(reference_folder)

    for filename in os.listdir(target_folder):
        if '_' in filename:
            code = filename.split('_', 1)[0]
            if code in reference_codes:
                file_path = os.path.join(target_folder, filename)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
            else:
                print(f"Kept: {filename}")


# Paths to the reference and target folders
# Replace with the actual path to the reference folder
reference_folder = 'final_milano_Bella-Sposa_All'
# Replace with the actual path to the target folder
target_folder = 'final_milano_Glitterati_All_copy'

# Delete matching files
delete_matching_files(reference_folder, target_folder)
