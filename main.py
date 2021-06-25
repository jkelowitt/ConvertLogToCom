"""
@Author: Jackson Elowitt
@Date: 6/18/21
@Contact: jkelowitt@protonmail.com

Take all the .log files in a given directory and make a new
directory which has .com files for the log files.
"""
from glob import glob

from classes import Atom, Molecule
from parsing import parsing_dict, yes_no, change_dict_values, write_job_to_com


def main():
    # From where to where
    files = []
    while not files:
        # Get the directory from the user
        print("\nEnter the directory which contains one of the following files.")
        print("Valid file types:")
        for ext in parsing_dict:
            print(f"\t.{ext}")
        directory = input("Directory: ")

        # Get all the files
        # which have a parsing function.
        for ext in parsing_dict:
            files += glob(f"{directory}/*.{ext}")

        files.sort(key=lambda x: len(x))

        # Check that there are valid files to be found.
        if not files:
            print("\nNo valid files found in the selected directory.")

    # Choose a new folder location
    new_dir = input("Enter the name of the folder you'd like to save the com files to: ")

    # Get the parameters for the com file

    settings = {
        "charge": "0",
        "mul": "1",
        "job": "Opt Freq",
        "theory": "B3LYP",
        "basis": "6-311G(2df,2p)",
        "cores": "8",
        "memory": "20gb",
        "linda": "1",
    }

    # Display default settings
    print("\nDefault Settings: ")
    for item in settings:
        print(f"\t{item} = {settings[item]}")

    non_default = yes_no("\nUse the default settings")

    # Change default options if desired
    if not non_default:
        done = False
        while not done:
            settings, done = change_dict_values(settings)

    # Parse geometry and write the files
    for file in files:
        data = parsing_dict[file[file.index(".") + 1:]](file)
        atoms = [Atom(a[0], (a[1], a[2], a[3])) for a in data]
        name = file.split("\\")[-1][:-4]
        molecule = Molecule(name, atoms)
        write_job_to_com(molecule.atoms, title=molecule.name, output=new_dir, **settings)

    return new_dir


if __name__ == "__main__":
    print("ConvertToCom".center(50, "~"))
    print("Author: Jackson Elowitt")
    print("Repo: https://github.com/jkelowitt/ConvertToCom")
    print("Version: v2")
    print("".center(50, "~"))

    new_dir = main()

    input(f"Com files saved to {new_dir}. Press enter to exit.")
