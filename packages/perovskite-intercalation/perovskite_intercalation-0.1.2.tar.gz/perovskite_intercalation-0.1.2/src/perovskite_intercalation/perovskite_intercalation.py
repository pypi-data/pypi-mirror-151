import os  # os.scandir
from ase import Atoms
from ase.parallel import parprint
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.io import cif  # self.read_cif_file
from pymatgen.transformations.advanced_transformations import SQSTransformation  # order_structure
from pymatgen.core.lattice import Lattice
from pymatgen.analysis.local_env import CutOffDictNN, JmolNN  # self.structure_to_graph
from pymatgen.analysis.graphs import StructureGraph  # self.structure_to_graph
import networkx as nx  # self.structure_to_graph, self.structure_graph_to_subgraphs
import numpy as np  # self.make_slabs
from pymatgen.core.surface import SlabGenerator  # self.make_slabs
from pymatgen.analysis.adsorption import plot_slab  # visualize_slabs
import matplotlib.pyplot as plt  # visualize_slabs
import warnings  # ignore pymatgen.io.cif warnings

# for visualize_bonding
from pymatgen.vis.structure_vtk import StructureVis
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image


class Intercalator:
    def __init__(self, debug=1):

        # Set a debug level
        # python's warnings module won't work here becuase
        # some debug code outputs files, not just strings
        # Debug levels:
        #    0 - no debug output
        #    1 - basic informational strings
        #    2 - more informational strings
        #    3 - output images, plots, files for debugging
        self.DEBUG = debug

    def read_cif_file(self, cif_file):
        """
        Convert a cif file to a pymatgen Structure object
        """
        structure = None

        try:
            crystal = cif.CifParser(cif_file)

            if crystal.has_errors:
                parprint(f'Error parsing {cif_file}')
            elif not len(crystal.as_dict()):
                parprint(f'No structures found in {cif_file}')
            else:
                try:
                    structures = crystal.get_structures(primitive=False)

                    if len(structures) > 1:
                        if self.DEBUG > 0:
                            parprint(f'Using first structure found in {cif_file}')

                    structure = structures[0]

                    if not len(structure):
                        parprint(f'Empty structure found in {cif_file}')
                        structure = None

                    if self.DEBUG >= 1:
                        parprint(f'Created a structure with {len(structure)} atoms from {cif_file}')
                except:
                    pass

                # debug, to check the structure in VESTA
                if self.DEBUG >= 3:
                    writer = cif.CifWriter(structure)
                    writer.write_file('original_structure.cif')
        except:
            parprint(f'Error opening {cif_file}')

        return structure

    def order_structure(self, structure):
        """
        SQSTransform is probably not the way to order hybrid organic-inorganic crystals
        :param structure:
        :return:
        """
        if not structure.is_ordered:
            # Create a structure where partially occupied disordered sites
            # are quasi-randomly replaced with ordered sites
            # a supercell can be created to accommodate the partial occupancies
            #
            # scaling determines the number of cells to create in a supercell structure
            #     set to 1 for now, but larger supercells may be needed
            # search_time is time in minutes to calculate new structure
            sqstransform = SQSTransformation(structure, scaling=1, search_time=5, best_only=True)
            sqstransform.apply_transformation(structure)

        return structure

    def structure_to_graph(self, structure, bonds=None):
        """
        Analyze bonding in structure and create graph networks
        :param structure: pymatgen structure
        :param bonds: dict specifying cut-off distances for bonds e.g. {'Pb-I': 4.0, ...}
        :return: pymatgen structure graph
        """
        # To make space for intercalation, we need to find a plane
        # where the perovskite crystal can be split into slabs
        # To do this, we specify bonds to avoid breaking bonds
        # when the crystal is split.
        # We want to split at the Van der Waals gallery between ligands in
        # Ruddlesden-Popper 2D perovskites. There is an issue when the
        # ligands interdigitate, it is difficult to find a plane where no
        # bonds will be broken.
        # One option is to tell pymatgen to 'repair' bonds by moving atoms
        # that were cleaved back where they belong.
        # Another option is to pull the crystal apart by translating all 'connected' atoms
        # where connections include ammonium-halide hydrogen bonds.
        # This is in effect finding which atoms belong in which slabs by creating
        # bonding networks. The key is to avoid 'bonding' atoms across the Van der Waals gap.

        if not bonds:
            # load default bond strategy from a file
            # with open('perovskite_bonds_cutoff.pkl', 'rb') as f:
            #    bonds = pickle.load(f)
            bond_strategy = JmolNN()
        else:
            bond_strategy = CutOffDictNN(bonds)

        structure_graph = StructureGraph.with_local_env_strategy(structure, bond_strategy)

        # Debugging
        if self.DEBUG >= 2:
            # Convert directed structure graph to an undirected graph
            # undirected graphs are required to find subgraphs with nx.connected_components
            # u_graph = nx.Graph(structure_graph.graph)
            u_graph = structure_graph.graph.to_undirected(as_view=True)

            all_subgraphs = [u_graph.subgraph(c) for c in nx.connected_components(u_graph)]

            parprint(f'Found {len(all_subgraphs)} subgraphs of lengths: {[len(sg) for sg in all_subgraphs]}')

        # For debugging
        # Draw an image of the graph network
        if self.DEBUG >= 3:
            structure_graph.draw_graph_to_file(filename='test_graph.png', hide_image_edges=False)

        return structure_graph

    def structure_graph_to_subgraphs(self, structure_graph):
        # structure_graph.get_subgraphs_as_molecules will not work because it does not return
        # graphs that extend through periodic boundaries
        # parprint(structure_graph.get_subgraphs_as_molecules())

        # Convert directed structure graph to an undirected graph
        # undirected graphs are required to find subgraphs with nx.connected_components
        # u_graph = nx.Graph(structure_graph.graph)
        u_graph = structure_graph.graph.to_undirected(as_view=True)

        all_subgraphs = [u_graph.subgraph(c) for c in nx.connected_components(u_graph)]

        if self.DEBUG >= 2:
            parprint(f'Found {len(all_subgraphs)} subgraphs of lengths: {[len(sg) for sg in all_subgraphs]}')

        # For debugging
        # Draw an image of the sub graphs
        if self.DEBUG >= 3:
            structure_graph.draw_graph_to_file(filename='test_sub_graphs.png', node_labels=False, image_labels=False,
                                               hide_image_edges=False)

        return all_subgraphs

    def remove_graph_fragments(self, structure, structure_graph, periodic_boundaries=(False, False, False), ignore_atom_symbols=()):
        '''
        Removes molecular fragments that span non-periodic boundaries.

        :param structure: pymatgen Structure to remove fragments from
        :param structure_graph: graph of structure
        :param periodic_boundaries: sequence of three boolean values i.e. (True,True,False)
        :param ignore_atom_symbols: do not remove atoms with these symbols i.e. ('Pb', 'I')
        :return: pymatgen Structure
        '''

        clean_structure = structure.copy()
        subgraphs = self.structure_graph_to_subgraphs(structure_graph)
        sites_to_remove = []

        for sg in subgraphs:
            # Ignore subgraphs containing certain atoms
            sg_species = [str(structure[i].specie) for i in sg]
            if not any([symbol in sg_species for symbol in ignore_atom_symbols]):
                # Remove fragments that span a non-periodic boundary
                sg_removed = False
                for site in sg.nodes:
                    connected_sites = structure_graph.get_connected_sites(site)
                    for cs in connected_sites:
                        #print(f'Bond {site} to {cs.index}:', cs.jimage)
                        if any([a & (not b) for a,b in zip(cs.jimage, periodic_boundaries)]):
                            # There is a bond in this subgraph across a non-periodic boundary
                            #print('Removed')
                            sites_to_remove += [i for i in sg]
                            sg_removed = True
                            break

                    if sg_removed:
                        break

        if self.DEBUG > 1:
            parprint('Removing sites:', sites_to_remove)

        clean_structure.remove_sites(sites_to_remove)
        return clean_structure

    def get_mean_c_coords_from_structure_graph(self, graph, structure):
        # Figure out which subgraph needs to be translated up
        # and which subgraph needs to be translated down
        # Use the mean third-axis coordinate to figure out which
        # group of atoms are at the top and which are at the bottom
        # Look at the two largest subgraphs
        c_coordinates = []
        for node in graph.nodes():
            c_coordinates.append(structure.sites[node].c)

        mean_c_coord = np.mean(c_coordinates)

        if self.DEBUG >= 2:
            parprint(f'Mean c-axis coordinates for graph: {mean_c_coord}')

        return mean_c_coord

    def translate_subgraph_sites(self, structure, subgraphs, vacuum_distance):
        if len(subgraphs) == 2:
            two_largest_subgraphs = sorted(subgraphs, key=len, reverse=True)[:2]

            mean_c_coordinates = []
            for graph in two_largest_subgraphs:
                mean_c_coordinates.append(self.get_mean_c_coords_from_structure_graph(graph, structure))

            # first move the lower sites down, then the upper sites up
            translation_distance = vacuum_distance / 2.0 * np.array([[0, 0, -1], [0, 0, 1]], dtype=float)

            # First the lower sites, then the upper sites,
            # so sort the subgraphs by mean c coordinate, ascending
            if mean_c_coordinates[0] < mean_c_coordinates[1]:
                structure.translate_sites(indices=two_largest_subgraphs[0].nodes(), vector=translation_distance[0],
                                          frac_coords=False, to_unit_cell=False)
                structure.translate_sites(indices=two_largest_subgraphs[1].nodes(), vector=translation_distance[1],
                                          frac_coords=False, to_unit_cell=False)
            else:
                structure.translate_sites(indices=two_largest_subgraphs[1].nodes(), vector=translation_distance[0],
                                          frac_coords=False, to_unit_cell=False)
                structure.translate_sites(indices=two_largest_subgraphs[0].nodes(), vector=translation_distance[1],
                                          frac_coords=False, to_unit_cell=False)
        else:
            parprint('Structure must have exactly 2 bonding networks or subgraphs. Is this a Dion-Jacobsen structure?')

        return structure

    def make_slabs(self, structure, bonds=None):
        if self.DEBUG > 0:
            parprint('Remember to cite these works when using pymatgen surface/slab generator code:')
            parprint(
                'R. Tran, Z. Xu, B. Radhakrishnan, D. Winston, W. Sun, K. A. Persson, S. P. Ong, "Surface Energies of Elemental Crystals", Scientific Data,2016, 3:160080, doi: 10.1038/sdata.2016.80.)')
            parprint(
                'Sun, W.; Ceder, G. Efficient creation and convergence of surface slabs, Surface Science, 2013, 617, 53–59, doi:10.1016/j.susc.2013.05.016.\n')

        # Need to tell the slab generator which direction to cut the slab
        # simple guess is that the Van der Waals plane is normal to the greatest lattice vector
        abc = np.array([structure.lattice.a, structure.lattice.b, structure.lattice.c])
        slab_direction = np.floor_divide(abc, np.max(abc))
        slab_direction = slab_direction.astype(int)
        slab_direction = slab_direction.tolist()

        # min_slab_size is the minimum thickness of a slab, this might be estimated from
        # the number of octahedral layers (n=1,2,3,...)
        # for now set min_slab_size to about 2 Pb-halide bond lengths (7.4 Angstroms)
        #
        # Minimum vacuum size could be scaled by the size of the intercalate molecule
        slab_gen = SlabGenerator(initial_structure=structure, miller_index=slab_direction,
                                 min_slab_size=7.4, min_vacuum_size=0.0, reorient_lattice=True, primitive=True)

        # Find the Van der Waals plane and create a slab structure
        slabs = slab_gen.get_slabs(bonds=bonds, max_broken_bonds=0, repair=False)

        if self.DEBUG >= 2:
            parprint(f'Found {len(slabs)} slabs')

        return slabs

    def combine_cif_files(self, list_of_cif_files, combined_cif_filename='combined_cif_files.cif'):
        with open(combined_cif_filename, 'w') as out_file:
            for cif_filename in list_of_cif_files:
                with open(cif_filename, 'r') as in_file:
                    text = in_file.read()

                out_file.write(text)
                out_file.write('\n\n')

            if self.DEBUG >= 1:
                parprint(f'Combined {len(list_of_cif_files)} cif files as {combined_cif_filename}')

    def visualize_slabs(self, slabs):
        plot_limit = min(5, len(slabs))

        for i, slab in enumerate(slabs[:plot_limit]):
            #fig, ax = plt.subplots()
            #plot_slab(slab, ax, repeat=1, adsorption_sites=False)

            # debug
            #plt.title(f'Slab miller index {slab.miller_index} and shift {slab.shift:.4g}')

            writer = cif.CifWriter(slab)
            writer.write_file(f'test_slab_{i}.cif')

        # combine cif files
        list_of_cif_files = []
        for file_num in range(plot_limit):
            list_of_cif_files.append(f'test_slab_{file_num}.cif')

        list_of_cif_files = ['original_structure.cif'] + list_of_cif_files
        self.combine_cif_files(list_of_cif_files, 'combined_test_slabs.cif')

    def visualize_bonding(self, structure, structure_graph, title=''):
        """
        Creates side-by-side images of the 3D unit cell and the bonding graph of a structure
        """

        # Make an image of the unit cell
        sv = StructureVis(show_bonds=True, show_polyhedron=False)
        sv.set_structure(structure)
        sv.helptxt_actor.VisibilityOff()

        sv.write_image('structure.png', image_format='png', magnification=3)

        # Make an image of the graph
        structure_graph.draw_graph_to_file(filename='structure_graph.png', node_labels=False, image_labels=False,
                                           hide_image_edges=False)

        # Combine the two images into one
        fig = plt.figure()
        ax = fig.add_subplot(1, 2, 1)
        img = Image.open('structure.png')
        plt.imshow(img)
        ax.set_axis_off()
        ax = fig.add_subplot(1, 2, 2)
        img = Image.open('structure_graph.png')
        plt.imshow(img)
        ax.set_axis_off()
        plt.title(title)
        plt.savefig(fname=f'{title}.png', dpi=300)

    def intercalate_crystal(self, crystal, intercalate, distance=3.0):
        """
        Stack intercalate molecule and crystal structure in one simulation box

        params:
            crystal: ASE Atoms object describing crystal to intercalate
            intercalate: ASE Atoms object describing intercalate molecule
            distance: vaccum space above and below intercalate molecule (Angstroms)

        returns:
            stacked structure
        """

        # Initialize structure with the crystal to intercalate
        structure = crystal.copy()

        if self.DEBUG >= 3:
            crystal.write('crystal.cif')
            parprint('Saved crystal before adjusting unit cell as crystal.cif')

        if self.DEBUG > 0:
            parprint('Cell before intercalation: ', structure.cell.cellpar())

        # Increase c-axis of crystal cell to accomodate intercalate
        crystal_cell = structure.get_cell()
        crystal_original_height = np.linalg.norm(crystal_cell[2])
        crystal_cell[2] *= (crystal_original_height + distance * 2.0) / crystal_original_height
        structure.set_cell(crystal_cell)

        if self.DEBUG >= 3:
            structure.write('crystal_expanded_cell.cif')
            parprint('Saved crystal with expanded cell as crystal_expanded_cell.cif')

        # Chage intercalate cell to match structure before moving atoms
        # Change intercalate unit cell to match symmetry of the crystal
        # Shorten c-axis to minimum height required to fit the molecule
        molecule = intercalate.copy()

        # Align the molecule's x,y,z axes to the structure's x,y,z axes
        # This assumes orthorhombic cells...
        molecule.rotate('x', structure.get_cell()[0])
        molecule.rotate('y', structure.get_cell()[1])
        molecule.rotate('z', structure.get_cell()[2])
        molecule.set_cell(structure.get_cell())
        molecule.center(about=0.0)

        # create a gap in the z direction
        molecule.translate([0, 0, -distance])

        # Center in the xy plane
        molecule.center(axis=(0, 1))

        if self.DEBUG > 0:
            parprint('Translating intercalate by: ', crystal_original_height)

        if self.DEBUG >= 3:
            molecule.write('intercalant.cif')
            parprint('Saved intercalant as intercalant.cif')

        # Copy intercalate molecule atoms to structure
        for a in molecule:
            structure.append(a)

        if self.DEBUG > 0:
            parprint('Cell after intercalation: ', structure.cell.cellpar())

        return structure

    def intercalate_gallery(self, crystal_file, intercalant_file, vacuum_gap=3.0, supercell_dimensions=(1, 1, 1)):
        '''
        Creates an structure by placing an intercalant molecule in the van der Waals gap (or gallery) of
        a crystal. The c-axis of the molecule will be aligned with the c-axis of the crystal.
        Outputs files:
            intercalated_structure.cif         Intercalated crystal

            With self.DEBUG >= 3
                original_structure.cif         Crystal as imported
                crystal.cif                    Crystal slab without vacuum gap
                crystal_expanded_cell.cif      Crystal slab with vacuum gap
                intercalant.cif                Intercalant molecule
                test_slab_i.cif                Crystal slabs with surfaces parallel to (001) planes
                combined_test_slabs.cif        Crystal as imported (original_structure.cif) and all slabs (test_slab_i.cif)

        params:
            crystal_file: path to file describing the crystal
            intercalant_file: path to file describing the intercalant molecule
            vacuum_gap: size of the gap (in Angstroms) to create in the gallery
            supercell_dimensions: size of supercell to create more space for intercalant e.g. (2,1,1)

        returns:
            None
        '''

        # Values for building the crystal model
        vacuum_distance = 0.1  # Angstroms

        # N-halide bond lengths are about:
        # N-Br  4 Ang
        # N-I   4 Ang
        # We could do a smarter analysis by looking at the distribution of N-halide
        # distances.
        bonds = {('Pb', 'I'): 3.7,
                 ('Pb', 'Br'): 3.7,
                 ('Pb', 'Cl'): 3.7,
                 ('Sn', 'I'): 3.7,
                 ('Sn', 'Br'): 3.7,
                 ('Sn', 'Cl'): 3.7,
                 ('Ge', 'I'): 3.7,
                 ('Ge', 'Br'): 3.7,
                 ('Ge', 'Cl'): 3.7,
                 ('C', 'C'): 1.9,
                 ('C', 'N'): 1.8,
                 ('C', 'H'): 1.2,
                 ('N', 'H'): 1.2,
                 ('N', 'Br'): 4.0,
                 ('N', 'I'): 4.0,
                 ('C', 'O'): 2.0,
                 ('O', 'H'): 1.5,
                 }

        cif_files = []

        # old code, could be used with a database instead of passing the crystal in
        #with os.scandir('./nmse_database/structures/') as file_iter:
        #    for entry in file_iter:
        #        if entry.is_file():
        #            if os.path.splitext(entry.path)[1] == '.cif':
        #                cif_files.append(entry.path)

        cif_files = [crystal_file]
        intercalate_molecule = self.read_cif_file(intercalant_file)

        for i, file in enumerate(cif_files):

            # ignore UserWarning from cif reader about extra data in cif files
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                structure = self.read_cif_file(file)

            if structure and intercalate_molecule:

                # debug
                # sv = StructureVis(show_bonds=True, show_polyhedron=False)
                # sv.set_structure(structure)
                # view(sv)
                # sv.show()

                # if not structure.is_ordered:
                # skip the disorder problem for now
                # structure = self.order_structure(structure)

                # Optionally, try to make a gap in the structure using graphs
                # structure_graph = self.structure_to_graph(structure, bonds=None)
                # subgraphs = self.structure_graph_to_subgraphs(structure_graph)
                # structure = self.translate_subgraph_sites(structure, subgraphs, vacuum_distance)

                # Pymatgen has a slab generator which might be able to find
                # a plane in the structure that does not intersect any bonds
                # This will work without using the above graph algorithm
                # if the organic ligands are not interdigitated
                slabs = self.make_slabs(structure, bonds=bonds)

                # assume the first slab is the best (slabs are sorted by ascending number of broken bonds)
                # Had to convert to ASE atoms object to do the stacking
                # could not figure out how to do it with pymatgen, way too complicated
                # may need to use more than one slab if the unit cell has more than one van der waals gap
                # as most hybrid perovskites do
                best_slab = AseAtomsAdaptor.get_atoms(slabs[0])

                # could check here if the intercalate molecule will fit in the crystal unit cell
                # if not, then make a supercell
                # for now, just hard code it for testing
                best_slab = best_slab * supercell_dimensions

                intercalate_molecule = AseAtomsAdaptor.get_atoms(intercalate_molecule)

                intercalated_structure = self.intercalate_crystal(crystal=best_slab, intercalate=intercalate_molecule,
                                                                  distance=vacuum_gap)

                intercalated_structure = AseAtomsAdaptor.get_structure(intercalated_structure)

                # Output structure
                cw = cif.CifWriter(intercalated_structure)
                cw.write_file('intercalated_structure.cif')

                if self.DEBUG > 0:
                    parprint('Saved intercalated crystal as intercalated_structure.cif')

                if self.DEBUG >= 3:
                    self.visualize_slabs(slabs)

# Utility functions
def find_ammonium_atoms(atoms):
    '''
    Returns indices of nitrogen atoms with four bonds
    :param crystal: ASE Atoms
    :return: list of int
    '''
    # Get a list of cut-off distances for checking if two atoms are bonded
    # this is based on covalent radii, easier than using pymatgens bonding strategies
    # cutoffs is a vector with the cutoff distance for each atom in the atoms object
    from ase.neighborlist import natural_cutoffs
    cutoffs = natural_cutoffs(atoms, mult=1.1)

    # Find nitrogen atoms groups
    n_atoms = [a.index for a in atoms if a.symbol == 'N']
    ammonium_atoms = []
    distances = atoms.get_all_distances(mic=any(atoms.pbc))  # mic=True for periodic systems
    for n_index in n_atoms:
        nearest_indices = np.argsort(distances[n_index])
        # Call it an ammonium group if there are four bonds to nitrogen
        if all([atoms.get_distance(n_index, i, mic=any(atoms.pbc)) <= (cutoffs[n_index]+cutoffs[i]) for i in nearest_indices[1:5]]):
            ammonium_atoms.append(n_index)

    return ammonium_atoms


def replace_ligands(crystal, new_ligand, replace_fraction=1.0):
    '''
    Replace a certain fraction of the ligands in a crystal with another ligand.
    Attempts to give the new ligands the same orientation as the old ligands.

    :param crystal: ASE or pymatgen structure
    :param new_ligand: ASE or pymatgen structure
    :param replace_fraction: fraction of ligands to replace from 0.0 to 1.0
    :return: new structure
    '''

    # Check the type of the structure objects
    # Convert to ASE for the first part

    def convert_to_ase(object):
        from pymatgen.core.structure import Structure
        from ase.atoms import Atoms

        if type(object) == Atoms:
            return object
        elif type(object) == Structure:
            return AseAtomsAdaptor.get_atoms(object)
        else:
            parprint('Unknown crystal data type.')
            return None

    crystal = convert_to_ase(crystal)

    if not crystal:
        return

    # Get the indices of the ammonium group nitrogen crystal
    nitrogen_atoms = find_ammonium_atoms(crystal)
    parprint(f'Found {len(nitrogen_atoms)} ammonium groups in crystal.')

    # Do a network analysis to find the ligand atoms
    interc = Intercalator(debug=0)
    pmg_structure = AseAtomsAdaptor.get_structure(crystal)
    crystal_graph = interc.structure_to_graph(pmg_structure)
    crystal_subgraphs = interc.structure_graph_to_subgraphs(crystal_graph)
    parprint(f'Found {len(crystal_subgraphs)} subgraphs in crystal.')

    # Identify which subgraphs contain ligand atoms
    ligand_subgraphs = [sg for sg in crystal_subgraphs if any([True for a in nitrogen_atoms if a in sg.nodes])]
    parprint(f'Found {len(ligand_subgraphs)} ligands in crystal.')

    # Choose which ligands to remove
    num_ligands_to_remove = int(np.round(replace_fraction*len(ligand_subgraphs), decimals=0))
    if num_ligands_to_remove == 0:
        parprint('Fraction to remove less than one, no changes made.')
        return crystal

    # Space out the ligands to be removed by index
    # This should be more sophisticated, eg. using spatial coordinates instead of index
    ligands_to_remove = list(range((len(ligand_subgraphs) % num_ligands_to_remove),
                                   len(ligand_subgraphs),
                                   int(len(ligand_subgraphs)/num_ligands_to_remove)))
    parprint(f'Removing {len(ligands_to_remove)} ligands with indices: {ligands_to_remove}')

    # Check type of the ligand structure
    new_ligand = convert_to_ase(new_ligand)

    # Get some info about the new ligand
    # Assume there is one ammonium group in the ligand
    ligand_nitrogen_atom = find_ammonium_atoms(new_ligand)
    parprint(f'Found {len(ligand_nitrogen_atom)} ammonium in new ligand.')
    if len(ligand_nitrogen_atom) == 1:
        ligand_nitrogen_atom = ligand_nitrogen_atom[0]
    else:
        return

    # Get the position matrix
    positions = crystal.get_positions()

    # Remove the old ligands
    new_crystal = crystal.copy()
    atoms_to_remove = []
    for ligand_index in ligands_to_remove:
        sg = ligand_subgraphs[ligand_index]
        atoms_to_remove += sg.nodes

    del new_crystal[atoms_to_remove]

    # Add the new ligands
    for ligand_index in ligands_to_remove:

        # Get the subgraph (atomic indices) of one of the deleted ligands
        sg = ligand_subgraphs[ligand_index]

        # Find the ammonium nitrogen that was in the deleted ligand
        nitrogen_location = None
        for n_atom_index in nitrogen_atoms:
            if n_atom_index in sg.nodes:
                nitrogen_location = positions[n_atom_index]

        if len(nitrogen_location):
            ligand_to_add = new_ligand.copy()

            # Move the new ligand nitrogen atom to the position of the deleted ligand
            ligand_to_add.translate(nitrogen_location-ligand_to_add.positions[ligand_nitrogen_atom])

            # Orient the new ligand like the deleted ligand
            # ligand_to_add will be rotated to match the ligand that was removed
            # Create a copy of the old ligand by copying the crystal and removing all atoms not part of the ligand
            # Preserves the periodicity and we dont need to worry about ligands that cross the periodic boundary
            old_ligand = crystal.copy()
            del old_ligand[[a.index for a in crystal if a.index not in sg.nodes]]
            ligand_to_add = align_ligands(old_ligand, ligand_to_add)

            # Add new ligand to the crystal
            for a in ligand_to_add:
                new_crystal.append(a)
        else:
            parprint('Can not get location and orientation of old ligand')
            return

    # Wrap new ligand atoms inside the unit cell
    new_crystal.wrap()
    return new_crystal


def align_ligands(ligand1, ligand2):
    '''
    Change the orientation of ligand2  as close as possible to ligand1

    :param ligand1: ASE Atoms object
    :param ligand2: ASE Atoms object
    :return rotated ligand2 ASE Atoms object
    '''
    from scipy.spatial.transform import Rotation as R

    l1 = ligand1.copy()
    l2 = ligand2.copy()

    # There is probably a package out there that can do this better
    # Make some assumptions to simplify the algorithm
    # Assume both molecules have one ammonium group

    # Assume there is one ammonium group in each ligand
    l1n = find_ammonium_atoms(l1)
    if len(l1n) == 1:
        l1n = l1n[0]
    else:
        parprint('Found more than one ammonium in ligand', str(l1))
        return

    l2n = find_ammonium_atoms(l2)
    if len(l2n) == 1:
        l2n = l2n[0]
    else:
        parprint('Found more than one ammonium in ligand', str(l2))
        return

    # Center the nitrogen atoms before rotation
    l1.translate(-l1.positions[l1n])
    l2.translate(-l2.positions[l2n])

    # Use as many atoms as are in the smaller ligand
    n_atoms = min(len(l1),len(l2))

    l1_nearest_indices = np.argsort(l1.get_all_distances(mic=any(l1.pbc), vector=False)[l1n])[1:n_atoms]
    l2_nearest_indices = np.argsort(l2.get_all_distances(mic=any(l2.pbc), vector=False)[l2n])[1:n_atoms]
    
    # Sum the vectors to the n_atoms nearest neighbors
    l1_vectors = l1.get_all_distances(mic=any(l1.pbc), vector=True)[l1n, l1_nearest_indices]
    l2_vectors = l2.get_all_distances(mic=any(l2.pbc), vector=True)[l2n, l2_nearest_indices]
    
    rot, rmsd = R.align_vectors(a=l1_vectors, b=l2_vectors, weights=None)

    l2.positions = rot.apply(l2.positions)
    
    # return l2 to original position
    l2.translate(ligand2.positions[l2n])

    return l2

def get_ligand_atoms(atoms):
    '''
    Returns a list the length of the number of ligand molecules.
    Each list member is a list of the atom indices for each ligand molecule.
    :param atoms: structure with ligand molecules (must have ammoniacal nitrogens)
    :type atoms: ASE Atoms
    :return: atom indices for atoms in each ligand molecule
    :rtype: list of lists of ints
    '''

    # Get the indices of the ammonium group nitrogen crystal
    ammonium_nitrogen_atoms = find_ammonium_atoms(atoms)
    parprint(f'Found {len(ammonium_nitrogen_atoms)} ammonium groups in crystal.')

    # Do a network analysis to find the ligand atoms
    interc = Intercalator(debug=0)
    pmg_structure = AseAtomsAdaptor.get_structure(atoms)
    crystal_graph = interc.structure_to_graph(pmg_structure)
    crystal_subgraphs = interc.structure_graph_to_subgraphs(crystal_graph)

    # Identify which subgraphs contain ligand atoms
    ligand_subgraphs = [sg for sg in crystal_subgraphs if any([True for a in ammonium_nitrogen_atoms if a in sg.nodes])]
    parprint(f'Found {len(ligand_subgraphs)} ligand molecules in crystal.')

    ligand_indices = []
    for sg in ligand_subgraphs:
        ligand_indices.append([i for i in sg.nodes])

    return ligand_indices