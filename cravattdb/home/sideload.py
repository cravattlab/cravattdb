"""Helper methods for creating datasets."""
from cravattdb import app, db
from cravattdb.home.models import Dataset
from zipfile import ZipFile
import csv
import pathlib


def new_dataset(dataset_id, user_id, file):

    cimage_data_path = unzip_cimage(file, user_id, dataset_id)
    output_file_path = pathlib.Path(
        cimage_data_path,
        'dta',
        'output',
        'output_rt_10_sn_2.5.to_excel.txt'
    )

    dataset = create_dataset(dataset_id)
    db.create_all()

    with output_file_path.open('r') as f:
        # skip first line
        f.readline()

        for line in csv.reader(f, delimiter='\t'):
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


def unzip_cimage(file, user_id, dataset_id):
    extract_path = pathlib.Path(
        app.instance_path,
        'legacy',
        str(user_id),
        str(dataset_id)
    )

    with ZipFile(file, 'r') as cimage_zip:
        cimage_zip.extractall(str(extract_path))

    return extract_path


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
