"""Helper methods for creating datasets."""
from models.database import db
from csv import reader
from re import sub
import io


def populate_dataset(dataset_type, id, file):
    dataset = create_dataset(dataset_type, id)
    raw_data = preprocess(file)
    data = []

    tsv = io.StringIO(raw_data)

    for line in reader(tsv, delimiter='\t'):
        data.append(dataset(
            peptide_index=line[0],
            ipi=line[1],
            description=line[2],
            symbol=line[3],
            sequence=line[4],
            mass=line[5],
            mr=line[6],
            sd=line[7],
            run=line[8],
            charge=line[9],
            segment=line[10],
            link=line[11]
        ))

    db.session().save(data)


def preprocess(file):
    with open(file) as raw_file:
        next(raw_file)  # skip first line
        raw_data = raw_file.read()

    # remove headers from each individual grouping
    processed = sub('.+\d\s+\n', '', raw_data)
    # extract out actual link
    processed = sub('=HYPERLINK\("(.+)","(\d+)\.\d+"\)', r'\1\t\2', processed)
    # I forget what this does...
    processed = sub('\s+(.+)\t(\d+)\n', r'\2\t\1\n', processed)

    return processed


def create_dataset(dataset_type, id):
    """Return new Dataset objects for SQLAlchemy.

    Takes advantage of inheritance and segregates datasets by type and
    experiment id.

    Arguments:
        dataset_type {Integer} -- Type of dataset as defined in ExperimentType
        id {Integer} -- Corresponds to experiment id
    """
    dataset_name = 'dataset_{}'.format(id)

    props = {
        '__tablename__': dataset_type,
        '__mapper_args__': {'polymorphic_identify': dataset_name},
        id: db.Column(db.Integer, db.ForeignKey('datasets.id'), primary_key=True)
    }

    # "the dark side of type"
    return type(
        dataset_name,
        (db.Model,),
        props
    )
