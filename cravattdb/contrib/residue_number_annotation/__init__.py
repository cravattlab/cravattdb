"""Blergh."""
from cravattdb.contrib.residue_number_annotation import uniprot
from urllib.parse import urlparse
from functools import partial
import ftplib
import pathlib
import gzip

SWISSPROT_URL = urlparse(
    'ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/taxonomic_divisions/uniprot_sprot_human.dat.gz'
)
ABS_PATH = pathlib.Path(__file__).parents[0]
SWISSPROT_DAT = pathlib.Path(ABS_PATH, 'data/uniprot_sprot_human.dat')
DATA_PATH = pathlib.Path(ABS_PATH, 'data/uniprot.json')


def get_residue_number(experiment_type):
    if experiment_type == 'isotop':
        return partial(_get_residue_number, db=get_db())
    else:
        return None


def _get_residue_number(uniprot_id, peptide, db=None):
    """Return residue number for labeled cysteine in a given protein."""
    residue = None

    if not db:
        db = get_db()

    try:
        residue = uniprot.get_residue_number(db, uniprot_id, peptide)
    except:
        pass
    finally:
        return residue


def get_db():
    """Get a handle to uniprot db, downloading if necessary."""
    if not DATA_PATH.exists() and not SWISSPROT_DAT.exists():
        download_database()

    db = uniprot.init(
        data_path=str(DATA_PATH),
        input_data_path=str(SWISSPROT_DAT)
    )

    cleanup_database_files()

    return db


def download_database():
    # heard you like context managers
    db_path = pathlib.Path(SWISSPROT_URL.path)
    archive_path = pathlib.Path('data', db_path.name)

    with ftplib.FTP(SWISSPROT_URL.netloc) as ftp:
        ftp.login()
        ftp.cwd(str(db_path.parent))
        retr_command = 'RETR {}'.format(str(db_path.name))

        ftp.retrbinary(retr_command, open(str(archive_path), 'wb').write)

        with gzip.open(str(archive_path), 'r') as z:
            with open(str(SWISSPROT_DAT), 'wb') as f:
                f.writelines(z)


def cleanup_database_files():
    """If there are any giant downloaded files, delete them."""
    pass
