import os
from werkzeug import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['raw', 'RAW'])

class Upload:
    def __init__(self, files, username, name):
        self.files = files
        self.move(username, name)

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    def move(self, username, name):
        dir_path = os.path.join(UPLOAD_FOLDER, username, name)
        os.makedirs(dir_path)

        for file in self.files:
            if file and self.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, dir_path, filename))

                print 'moving files'
                print self.files