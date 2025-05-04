import re
from multiprocessing import cpu_count, Pool

from src.settings import base_save_path, rgb_replace_regex, rgb_replacer


async def replace_colors():
    """Process all files in the given directory using multiple processes."""
    # Get a list of all files in the directory
    all_files = [f for f in base_save_path.glob('**/*') if f.is_file() and f.suffix not in {".zip", ".png"}]

    if not all_files:
        print(f"No files found in {base_save_path}")
        return

    # Use the number of CPU cores if num_processes is not specified
    num_processes = cpu_count()
    print(f"Starting to process {len(all_files)} files using {num_processes} processes...")

    # Create a pool of worker processes
    with Pool(num_processes) as pool:
        # Map the process_file function to each file
        results = pool.map(replace_colors_in_file, all_files)

    print(f"Completed processing {len(all_files)} files.")
    print(f"{sum([1 for it in results if it is True])} files were updated.")
    print(f"{sum([1 for it in results if it is False])} files were ignored.")
    print(f"{sum([1 for it in results if it is None])} files failed.")



def replace_colors_in_file(file_path) -> bool | None:
    def replacement(m):
        return rgb_replacer[m.group(0)]

    try:
        with open(file_path, 'r', errors='replace') as file:
            content = file.read()

        new_content = rgb_replace_regex.sub(replacement, content)
        for it in rgb_replacer.keys():
            assert it not in new_content

        with open(file_path, 'w') as f:
            f.write(new_content)

        return True


    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return None
