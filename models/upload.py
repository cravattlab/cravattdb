import os
from werkzeug import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['raw', 'RAW'])

class Upload:
    def __init__(self, files):
        self.files = files
        self.move()

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    def move(self):
        file = self.files

        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            print 'moving files'
            print self.files