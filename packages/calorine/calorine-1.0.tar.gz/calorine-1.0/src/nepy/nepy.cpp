#include "nep.cpp"
#include "nep.h"
#include <cmath>
#include <unistd.h>
#include "pybind11/include/pybind11.h"
#include "pybind11/include/numpy.h"
#include "pybind11/include/stl.h"
#include "pybind11/include/iostream.h"

namespace py = pybind11;

/// Local struct to hold an atomic configuration.
struct Atom
{
  int N;
  std::vector<int> type;
  std::vector<double> box, position;
};

std::vector<std::string> getAtomSymbols(std::string potential_filename)
/**
 @brief Fetches atomic symbols
 @details This function fetches the atomic symbols from the header of a NEP model. These are later used to ensure consistent indices for the atom types.
 @param potential_filename Path to the NEP model (/path/nep.txt).
 */
{
  std::ifstream input_potential(potential_filename);
  if (!input_potential.is_open())
  {
    std::cout << "Error: cannot open nep.txt.\n";
    exit(1);
  }
  std::string potential_name;
  input_potential >> potential_name;
  int number_of_types;
  input_potential >> number_of_types;
  std::vector<std::string> atom_symbols(number_of_types);
  for (int n = 0; n < number_of_types; ++n)
  {
    input_potential >> atom_symbols[n];
  }
  input_potential.close();
  return atom_symbols;
}

void convertAtomTypeNEPIndex(int N, std::vector<std::string> atom_symbols, std::vector<std::string> model_atom_symbols, std::vector<int> &type)
{
  for (int n = 0; n < N; n++)
  {
    // Convert atom type to index for consistency with nep.txt (potential_filename)
    std::string atom_symbol = atom_symbols[n];
    std::cout << atom_symbol << "\n";
    bool is_allowed_element = false;
    for (int t = 0; (unsigned)t < model_atom_symbols.size(); ++t)
    {
      if (atom_symbol == model_atom_symbols[t])
      {
        type[n] = t;
        is_allowed_element = true;
        std::cout << type[n] << "\n";
      }
    }
    if (!is_allowed_element)
    {
      std::cout << "Error: Atom type " << atom_symbols[n] << " not used in the given NEP potential.\n";
      exit(1);
    }
  }
}

std::vector<double> getDescriptors(std::string potential_filename, int N_atoms, std::vector<double> box, std::vector<std::string> atom_symbols, std::vector<double> positions)
{
  /**
  @brief Get descriptors for structure.
  @details This function computes the NEP descriptors given a structure and a NEP model defined by a `nep.txt` file.
  @param potential_filename   Path to the NEP model (/path/nep.txt).
  @param N_atoms              The number of atoms in the structure.
  @param box                  The cell vectors for the structure.
  @param atom_symbols         The atomic symbol for each atom in the structure.
  @param positions            The position for each atom in the structure.
*/

  /* Initialize atoms object */
  Atom atom;
  atom.N = N_atoms;
  atom.type.resize(atom.N);
  atom.position.resize(atom.N * 3);
  atom.box.resize(9);
  /* Write positions, cell and atom types */
  atom.position = positions;
  atom.box = box;
  std::vector<std::string>
      model_atom_symbols = getAtomSymbols(potential_filename); // load atom symbols used in model
  convertAtomTypeNEPIndex(atom.N, atom_symbols, model_atom_symbols, atom.type);

  /* Define NEP model and get descriptors */
  NEP3 nep(potential_filename);
  std::vector<double> descriptor(atom.N * nep.annmb.dim);
  nep.find_descriptor(
      atom.type, atom.box, atom.position, descriptor);
  return descriptor;
}

std::tuple<std::vector<double>, std::vector<double>, std::vector<double>> getPotentialForcesAndVirials(std::string potential_filename, int N_atoms, std::vector<double> box, std::vector<std::string> atom_symbols, std::vector<double> positions)
{
  /**
  @brief Get per atom potential, forces and virials for a structure.
  @details This function computes the NEP descriptors given a structure and a NEP model defined by a `nep.txt` file.
  @param potential_filename   Path to the NEP model (/path/nep.txt).
  @param N_atoms              The number of atoms in the structure.
  @param box                  The cell vectors for the structure.
  @param atom_symbols         The atomic symbol for each atom in the structure.
  @param positions            The position for each atom in the structure.
*/

  /* Initialize atoms object */
  Atom atom;
  atom.N = N_atoms;
  atom.type.resize(atom.N);
  atom.position.resize(atom.N * 3);
  atom.box.resize(9);
  /* Write positions, cell and atom types */
  atom.position = positions;
  atom.box = box;
  std::vector<std::string>
      model_atom_symbols = getAtomSymbols(potential_filename); // load atom symbols used in model
  convertAtomTypeNEPIndex(atom.N, atom_symbols, model_atom_symbols, atom.type);
  /* Define NEP model and get descriptors */
  NEP3 nep(potential_filename);
  std::vector<double> potential(atom.N);
  std::vector<double> force(atom.N * 3);
  std::vector<double> virial(atom.N * 9);
  nep.compute(
      atom.type, atom.box, atom.position, potential, force, virial);
  return std::make_tuple(potential, force, virial);
}

PYBIND11_MODULE(_nepy, m)
{
  m.doc() = "Pybind11 interface for NEP";
  m.def(
      "get_descriptors",
      &getDescriptors,
      "A function for extracting NEP descriptors",
      py::arg("potential_filename"),
      py::arg("N_atoms"),
      py::arg("box"),
      py::arg("atom_symbols"),
      py::arg("positions"),
      py::call_guard<py::scoped_ostream_redirect, py::scoped_estream_redirect>());
  m.def(
      "get_potential_forces_and_virials",
      &getPotentialForcesAndVirials,
      "A function for extracting energies, forces and virials for a system with a given NEP potential",
      py::arg("potential_filename"),
      py::arg("N_atoms"),
      py::arg("box"),
      py::arg("atom_symbols"),
      py::arg("positions"),
      py::call_guard<py::scoped_ostream_redirect, py::scoped_estream_redirect>());
}