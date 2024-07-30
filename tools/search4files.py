import os
import sys
import glob
import math
import keyboard
from os import walk
from process import get_valid_file_suffixes

class Search4files:
    def __init__(self):
        # Top levels directories for walking files
        self.rough_directories = None
        # Walking index for above directories
        self.rough_index = 0
        # When walking in a directory, we search for the files by their suffix one after another
        # This is the index of walking suffixes
        self.file_suffix_walk_index = 0
        # Walked files counter inside each rough directory for each suffix
        self.walking_files = None;
        self.walking_files_index = 0;
        self.animation_frames = ["|", "/", "-", "\\"]
        self.animation_index = 0
        # The sum of files processed
        self.walking_files_count = 0

    """
    Walks through all files on local disks one by one
    """
    def search(self):
        while True:
            if (self.rough_directories is None):
                self.get_rough_directories()
            else:
                while True:
                    if ((self.walking_files is not None) and (self.walking_files_index < len(self.walking_files))):
                        # Return 1 file's path
                        filepath = self.walking_files[self.walking_files_index]
                        self.show_progress()
                        self.walking_files_index += 1
                        self.walking_files_count += 1
                        return filepath
                    else:
                        if (self.rough_index < len(self.rough_directories)):
                            # Walk through rough directories
                            filedir = self.rough_directories[self.rough_index]
                            self.walk_through_suffixes(filedir)
                        else:
                            # Search done
                            self.rough_directories = None
                            self.rough_index = 0
                            self.file_suffix_walk_index = 0
                            self.walking_files = None;
                            self.walking_files_index = 0;
                            self.animation_index = 0
                            self.walking_files_count = 0
                            print("Inserted ", self.walking_files_count, " files.")
                            return None

    # Show walking progress bar
    def show_progress(self):
        valid_file_suffixes = get_valid_file_suffixes()
        f1 = 1.0 / len(self.rough_directories)
        f2 = 1.0 / len(valid_file_suffixes)
        f3 = 1.0 / len(self.walking_files)
        walked_percentage = self.rough_index * f1 + self.file_suffix_walk_index * f2 * f1 + self.walking_files_index * f3 * f2 * f1

        # Small animation showing the program is active
        animation_item = self.get_animation_item()
        info_text = "(" + animation_item + ") | "
        info_text2 = (str(math.floor(walked_percentage * 100)) + "% | " +
              str(self.rough_index) + "/" + str(len(self.rough_directories)) + " | " +
              str(self.file_suffix_walk_index) + "/" + str(len(valid_file_suffixes)) + " | " +
              str(self.walking_files_index) + "/" + str(len(self.walking_files)) + " ");
        info_text += info_text2

        terminal_size = os.get_terminal_size()
        progress_bar_length = terminal_size.columns - len(info_text) - 2
        progress_bar_length_front = math.floor(progress_bar_length * walked_percentage)
        progress_bar_length_back = progress_bar_length - progress_bar_length_front
        progress_bar = ["█" for element in range(progress_bar_length_front)]
        progress_bar += ["░" for element in range(progress_bar_length_back)]

        sys.stdout.write("\r" + info_text + "|" + "".join(progress_bar) + "|")
        sys.stdout.flush()

    # Get the next rotating charater in the progress bar
    def get_animation_item(self):
        animation_item = self.animation_frames[self.animation_index]
        self.animation_index += 1
        self.animation_index = 0 if (self.animation_index >= len(self.animation_frames)) else self.animation_index
        return animation_item

    def walk_through_suffixes(self, filedir):
        valid_file_suffixes = get_valid_file_suffixes()
        if (self.file_suffix_walk_index < len(valid_file_suffixes)):
            # Search for files in the rough directory by suffix
            filetype = valid_file_suffixes[self.file_suffix_walk_index]
            self.walking_files = self.search_for_files(filedir, filetype)
            self.walking_files_index = 0;
            self.file_suffix_walk_index += 1
        else:
            self.rough_index += 1
            self.file_suffix_walk_index = 0

    def get_rough_directories(self):
        directories = self.search_for_initial_folders()
        # Found None resources
        if (len(directories) == 0):
            return None
        # Get ready to walk all the files in sub-folders
        self.rough_directories = directories
        self.rough_index = 0
        self.file_suffix_walk_index = 0
        self.animation_index = 0

    # Collect first a few levels of folders for walking and for showing walking progress
    def search_for_initial_folders(self):
        MINIMAL_DIR_NUM_FOR_PROGRESS_BAR = 20
        # Get all available drives
        directories = [ chr(x) + ":\\" for x in range(65,91) if os.path.exists(chr(x) + ":") ]
        directories.sort()
        # Get sub-folder paths
        def walk_directories(dirs):
            folderpaths = []
            for dir in dirs:
                folders = []
                # Walk sub-folders under the dir
                for (dirpath, dirnames, filenames) in walk(dir):
                    folders.extend(dirnames)
                    break
                # Join parent path and sub-folder name to make a complete path
                folderpaths.extend([ dir + folder for folder in folders])
            folderpaths.sort()
            return folderpaths
        while True:
            dirs = walk_directories(directories)
            # No more sub-folders
            if directories == dirs:
                break
            directories = dirs
            # Enough segments to show the resources searching progress
            if len(dirs) >= MINIMAL_DIR_NUM_FOR_PROGRESS_BAR:
                break
        # With it we can show walking progress on progress bar
        directories.sort()
        return directories

    # Walk all files of a certain suffix in a folder
    def search_for_files(self, filepath, filetype):
        searchKey = filepath + "\\**\\*." + filetype
        dirs = glob.glob(searchKey, recursive = True)
        return dirs
