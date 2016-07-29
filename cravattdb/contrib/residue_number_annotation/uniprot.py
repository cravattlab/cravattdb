"""Takes Swiss-Prot data file and abridges it.

Outputs JSON files compatible with mirage.py objects
"""

import os.path
import mirage
import urllib


def master_from_peptide(peptide):
    """Generate master peptide from tryptic peptides - TEV heavy/light labelling."""
    peptide = peptide.replace("(15.9949)", '')
    peptide = peptide.replace("(464.28595)", '*')
    peptide = peptide.replace("(470.29976)", '*')
    return peptide.split('.')[1]


def findresidue(seq, subseq):
    # if '*' in subseq and '.' in subseq:
    #   subseq = subseq.split('.')[1]
    #   pos = subseq.find('*')
    #   subseq = subseq.replace('*', '')
    #   aa = subseq[pos-1]
    if '*' in subseq and '.' not in subseq:
        pos = subseq.find('*')
        subseq = subseq.replace('*', '')
        aa = subseq[pos - 1]
    else:
        pos = subseq.find('C')
        aa = subseq[pos]

    if subseq in seq:
        index = seq.find(subseq)
        if pos == -1:
            return 0

        return(aa + str(index + pos))
    else:
        return(aa + str(0))


def fastasearch(uniprot_id):
    try:
        data = urllib.request.urlopen("http://www.uniprot.org/uniprot/" + uniprot_id + ".fasta").read().decode()
        return ''.join(data.split('\n')[1:])
    except:
        return ''


def get_residue_number(db, uniprot_id, peptide):
    if uniprot_id in db:
        return findresidue(db[uniprot_id].sequence, peptide)
    else:
        seq = fastasearch(uniprot_id)
        return findresidue(seq, peptide)


def uniprot_ipi(db, uniprot_id, peptide):
    if "Reverse" in uniprot_id:
        uniprot_id = uniprot_id.split('_')[1]

    if uniprot_id in db:
        seq = db[uniprot_id].sequence
        active_res = findresidue(seq, peptide)
        return uniprot_id + '_' + active_res
    else:
        return uniprot_id


def assemble(f):
    """Assemble(input file name): creates a mirage.ProteinDatabase object from a local uniprot file."""
    print("Assembling UniProtKB reference data", f)
    file = open(f)
    upkb = mirage.ProteinDatabase()

    count = 0
    c2 = 0

    # booleans for loop control
    switch = False
    acc_switch = False

    # temporary protein object
    tmp = mirage.Protein()
    # PDB = panther.loadPANTHER('panther-terms.json')
    # PDB2 = panther.loadPANTHER('RECUR_slim.json')
    for line in file:
        line = line.strip()

        if "ID   " in line and 'AA' in line:
                count += 1
                tmp.identifier = line.strip().split('   ')[1].split('_HUMAN')[0]
                # print(tmp.identifier)
                # now we record the next line
                acc_switch = True

        # signifies the beginning of accession section.
        if "AC   " in line and acc_switch:
            tmp.accession = line.split("   ")[1].split(';')[0]
            # acc_switch ensures that we only get the first line of accession info if there is more than one
            acc_switch = False

        # signifies the end of a sequence
        if "//" in line and ':' not in line:
            try:
                switch = False
                upkb + tmp
                tmp = mirage.Protein()
            except:
                    print("error", tmp)

        if switch:
            tmp.sequence += (''.join(map(str, line.strip().split(' '))))

        if "SQ   " in line:
            switch = True
            tmp.mw = int(line.split(';')[1].strip().split(' ')[0])
            # print(line)

    print(count, "protein sequences assembled")
    return upkb


SWISSPROT_DAT = 'uniprot_sprot_human.dat'
TREMBL_DAT = 'uniprot_trembl_human.dat'
DATA_PATH = '/home/lazear/bin/Python/uniprot.json'

data = []


# returns a mirage.ProteinDatabase object
def init(data_path=DATA_PATH, input_data_path=SWISSPROT_DAT):
    """Return a mirage.ProteinDatabase object."""
    if os.path.exists(DATA_PATH):
        # print("Abridged UniProtKB data already assembled, loading")
        data = mirage.ProteinDatabase.load(DATA_PATH)
    else:
        print("Abridged UniProtKB data not found...")
        data = assemble(input_data_path)
    return data
