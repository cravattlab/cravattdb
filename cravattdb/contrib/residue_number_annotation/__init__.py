"""Blergh."""
import cravattdb.contrib.residue_number_annotation.uniprot as uniprot
import requests
import pathlib
import zipfile


SWISSPROT_DAT = 'data/uniprot_sprot_human.dat'
DATA_PATH = 'data/uniprot.json'
SWISSPROT_URL = 'ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz'


if not pathlib.Path(SWISSPROT_DAT).exists():
    db_request = requests.get(SWISSPROT_URL)

    with open(pathlib.Path(SWISSPROT_DAT, '.gz'), 'wb') as f:
        f.write(db_request.text)

    with zipfile.ZipFile(f, 'rb') as z:
        z.extractall(DATA_PATH)

db = uniprot.init(
    data_path=DATA_PATH,
    input_data_path=SWISSPROT_DAT
)


def get_residue_number(uniprot_id, peptide):
    """Return residue number for labeled cysteine in a given protein."""
    residue = None

    try:
        residue = uniprot.get_residue_number(db, uniprot_id, peptide)
    except:
        pass

    return residue
