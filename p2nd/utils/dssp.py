# p2nd.utils.dssp.py
from Bio.PDB import DSSP


def model_to_dssp(model, in_file):
    """
    Convert a Bio.PDB model to DSSP labels.
    :param model: Bio.PDB model
    :param in_file: Path to the mmCIF file
    :return: list of DSSP labels
    """
    dssp = DSSP(model=model, in_file=in_file, dssp="mkdssp", file_type="mmCIF")
    
    return dssp


def dssp_to_chain_labels(dssp, chain="A"):
    """
    Convert DSSP labels to chain labels.
    :param dssp: DSSP object
    :param chain: chain ID
    :return: list of chain labels
    """
    labels = []
    for key in dssp.keys():
        if key[0] == chain:
            ss = dssp[key][2]
            labels.append(ss)
    return labels
