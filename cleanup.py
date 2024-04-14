import os
import shutil
import glob

def remove_selenium_tmp():
    # List of temporary directories created by Selenium
    temp_dirs = [
        "/tmp/.com.google.Chrome",
        "/tmp/.com.google.Chrome.*",
        "/tmp/.org.chromium.Chromium",
        "/tmp/.org.chromium.Chromium.*",
        "/tmp/.org.chromium.Chromium.*",
        "/tmp/.selenium*"
    ]

    for temp_dir_pattern in temp_dirs:
        # Expand wildcards in directory names
        temp_dir_list = glob.glob(temp_dir_pattern)
        
        # Remove each temporary directory
        for temp_dir in temp_dir_list:
            print(f"Removing directory: {temp_dir}")
            shutil.rmtree(temp_dir, ignore_errors=True)

    print("Selenium temporary files removed.")

if __name__ == "__main__":
    remove_selenium_tmp()

