"""
Classes used to facilitate Rotapy.

Atom: Data class containing all the pertinent information about an atom.
Molecule: A molecule class used to hold atoms and the bonds between those atoms.
"""

from dataclasses import dataclass, field


@dataclass(eq=True, unsafe_hash=True)
class Atom:
    """
    Data class containing all the pertinent information about an atom.
    eq = True: allows the comparison of atoms to each other
    unsafe_hash = True: allows the Atoms to be used as the keys of dictionaries

    If any parameter of the atom is changed, it will no longer work as the key of the dictionary.
        hence, 'unsafe' hash.

    Parameters
    ----------
    name: Atomic symbol of the atom

    pos: (x, y, z) position of the atom in global space

    color: Color of the atom. Defined in __post_init__ using a color dictionary

    cov_radius: Covalent Radius of the atom. Defines the distance at which the atom can bond.

    """

    name: str
    pos: tuple[float, float, float] = field(default=(0, 0, 0))


class Molecule:
    """
    A molecule class used to hold atoms and the bonds between those atoms.

    Parameters
    ----------
    name: The name of the molecule.

    atoms: A list of atoms containing Atom objects which form the molecule

    bonds: A dictionary with Atoms as keys, and other Atoms as values.
           The key represents the current atom.
           The value represents every other atom which it is currently bonded to.

    Methods
    -------
    add_atom: Adds an atom to the molecule

    remove_atom: Removes an atom from the molecule

    replace_atom: Replaces an atom in the molecule, so that the new atom retains the index in
                  Molecule.atoms that the removed atom previously had.

    make_bond_graph: Generates self.bonds. Used after all atom adjustments.

    """

    def __init__(self, name: str, atoms: list):
        self.name = name
        self.atoms = atoms.copy()  # No mutability please
        self.bonds: dict = dict()

    def add_atom(self, other: Atom) -> None:
        """Add an atom to the molecule"""
        if isinstance(other, type(Atom)):
            raise TypeError(f"Must add an Atom to the molecule, not {type(other)}")

        self.atoms.append(other)

    def remove_atom(self, a) -> None:
        """Remove an atom from the molecule"""
        if isinstance(a, type(Atom)):
            raise TypeError(f"Must add an Atom to the molecule, not {type(a)}")

        self.atoms.remove(a)

    def replace_atom(self, old_num, new_atom) -> None:
        """
        Removes one atom and adds another in its place.
        This ensures that the numbering for the atoms in the molecule remain constant.
        Atom 2 will remain atom 2 even if atom 1 is replaced.
        """
        self.atoms[old_num] = new_atom
