import pathlib
import config.config as config
from werkzeug import secure_filename


def upload(files, username, name):
    name = secure_filename(name)
    username = secure_filename(username)
    path = pathlib.Path(config.UPLOAD_FOLDER, username, name)
    path.mkdir(parents=True)

    for i, f in enumerate(sorted(files, key=lambda f: f.filename)):
        # only allow .raw extension
        filename = secure_filename(f.filename)
        filepath = pathlib.PurePath(filename)

        if filepath.suffix.lower() == '.raw':
            # rename raw files to reflect dataset name
            # adding _INDEX to please cimage
            filename = name + '_{}.raw'.format(i + 1)
            f.save(str(path.joinpath(filename)))

    return name, path
