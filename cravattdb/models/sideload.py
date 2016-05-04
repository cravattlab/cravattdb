"""Helper methods for creating datasets."""
from cravattdb.models.database import db, Dataset
import csv
import io


def new_dataset(dataset_id, file):
    dataset = create_dataset(dataset_id)
    db.create_all()
    raw_data = preprocess(file)
    tsv = io.StringIO(raw_data)

    for line in csv.reader(tsv, delimiter='\t'):
        db.session.add(dataset(
            peptide_index=line[0],
            ipi=line[1],
            description=line[2],
            symbol=line[3],
            sequence=line[4],
            mass=line[5],
            charge=line[6],
            segment=line[7],
            ratio=line[8],
            intensity=line[9],
            num_ms2_peaks=line[10].split('/')[0],
            num_candidate_peaks=line[10].split('/')[1],
            max_light_intensity=line[10].split('/')[2],
            light_noise=line[10].split('/')[3],
            max_heavy_intensity=line[10].split('/')[4],
            heavy_noise=line[10].split('/')[5],
            rsquared=line[11],
            entry=line[12],
            link=line[13]
        ))

    db.session.commit()


def preprocess(file):
    # skip first line
    next(file.stream)
    raw_data = file.read()
    file.close()

    return raw_data.decode()


def create_dataset(dataset_id):
    """Return new Dataset objects for SQLAlchemy.

    Takes advantage of inheritance and segregates datasets by experiment id

    Arguments:
        id {Integer} -- Corresponds to experiment id
    """
    dataset_name = 'dataset_{}'.format(dataset_id)

    props = {
        '__tablename__': dataset_name,
        '__mapper_args__': {'polymorphic_identity': dataset_id},
        'id': db.Column(db.Integer, db.ForeignKey('datasets.id'), primary_key=True)
    }

    # "the dark side of type"
    # https://jeffknupp.com/blog/2013/12/28/improve-your-python-metaclasses-and-dynamic-classes-with-type/
    return type(
        dataset_name,
        (Dataset,),
        props
    )
