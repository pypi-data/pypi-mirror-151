import qml
import numpy as np
import qmlspectrum

def qml_fchl_rep(geom_path, read_X, file_X, cut_distance):

    geom_files=qmlspectrum.read_files(geom_path)

    max_size=qmlspectrum.max_size(geom_path, geom_files)
    print('Max. number of atoms in the dataset is ',max_size)

    if read_X:
        print('Loading FCHL representation from ', file_X)
        X = np.load(file_X)
    else:
        print('Calculating FCHL representation')
        N_file=len(geom_files)
        i_file=0
        X=[]
        for i_geom in range(N_file):
            if np.mod(i_file, 100) == 0:
                print(i_file,' molecules out of ', N_file, ' done')
            xyz_file=geom_path+'/'+geom_files[i_geom]
            mol=qml.Compound(xyz=xyz_file)
            representation=qml.fchl.generate_representation(mol.coordinates, mol.nuclear_charges, max_size=max_size, cut_distance=cut_distance)
            X.append(representation)
            i_file=i_file+1
        np.save(file_X, X)
        print('FCHL representation is stored in ', file_X)

    N_mol = len(X)
    return N_mol, max_size, X

def qml_slatm_rep(geom_path, read_X, file_X):

    geom_files=qmlspectrum.read_files(geom_path)

    max_size=qmlspectrum.max_size(geom_path, geom_files)
    print('Max. number of atoms in the dataset is ',max_size)

    if read_X:
        print('Loading SLATM representation from ', file_X)
        X = np.loadtxt(file_X)
    else:
        print('Calculating SLATM representation')
        N_file=len(geom_files)
        i_file=0
        X=[]
        for i_geom in range(N_file):
            if np.mod(i_file, 100) == 0:
                print(i_file,' molecules out of ', N_file, ' done')
            xyz_file=geom_path+'/'+geom_files[i_geom]
            mol=qml.Compound(xyz=xyz_file)
            mbtypes = qml.representations.get_slatm_mbtypes(np.array([mol.nuclear_charges]))
            representation=qml.representations.generate_slatm(mol.coordinates, mol.nuclear_charges, mbtypes, sigmas=[0.05, 0.05], dgrids=[0.03, 0.03], rcut=5.0, pbc='000', alchemy=False, rpower=6)
            X.append(representation)
            i_file=i_file+1
        np.save(file_X, X)
        print('SLATM representation is stored in ', file_X)

    N_mol = len(X)
    return N_mol, max_size, X

