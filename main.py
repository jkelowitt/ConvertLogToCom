"""
@Author: Jackson Elowitt
@Date: 6/18/21
@Contact: jkelowitt@protonmail.com

Take all the .log files in a given directory and make a new
directory which has .com files for the log files.
"""
from glob import glob

from classes import Atom, Molecule
from parsing import parsing_dict


def main():
    # From where to where
    dir = input("Enter the directory of the .log files: ")
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

    # Get the files to parse
    files = glob(dir + "/*.log")

    # Parse geometry and write the files
    for file in files:
        data = parse_opt_geom_from_log(file)
        atoms = [Atom(a[0], (a[1], a[2], a[3])) for a in data]
        name = file.split("\\")[-1][:-4]
        molecule = Molecule(name, atoms)
        write_job_to_com(molecule.atoms, title=molecule.name, output=new_dir, **settings)

    return new_dir


if __name__ == "__main__":
    print("ConvertLogToCom".center(50, "~"))
    print("Author: Jackson Elowitt")
    print("Repo: https://github.com/jkelowitt/ConvertLogToCom")
    print("Version: v2")
    print("".center(50, "~"))
    print()

    new_dir = main()

    input(f"Com files saved to {new_dir}. Press enter to exit.")
