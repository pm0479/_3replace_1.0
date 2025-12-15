''' _3replace.py

    This is the original function for 3replace, where
    the user defines a parent directory, a string to find
    in filenames, and a string to replace with. Function is
    recursive only.
'''
import os

           
def replaceAll(directory, findString, replaceString):
    # Creates list to store the changed file names
    renamed = []

    # For every file within a parent folder path, finds/replaces
    # strings in all filenames with user defined input. Is recursive.
    for root, dirs, files in os.walk(directory):
        for file in files:
            if findString in file:
                oldName = os.path.join(root, file)
                newName = os.path.join(root, file.replace(findString, replaceString))
                os.rename(oldName, newName)
                renamed.append((file, os.path.basename(newName)))
    return renamed


# If the script is being run directly, prompts user for variable input.
if __name__ == "__main__":
    directory = input("\nEnter the directory to search: ")
    findString = input("Enter the string to find: ")
    replaceString = input("Enter the string to replace with: ")
    
    # Runs the function, returns list of renamed files
    renamed = replaceAll(directory, findString, replaceString)
    
    # Column headers
    print(f"\n{'Old Name':40} | {'New Name'}")
    print("-" * 80)


    for old, new in renamed:
        print(f"{old:40} | {new}")