import json, os, time
import config.config as config
from models.ip2 import IP2

class Search:
    def __init__(self, name):
        # dataset name
        self.name = name

    def login(self, username, password):
        self._ip2 = IP2(self.name)
        return self._ip2.login(username, password)

    def search(self, organism, experiment_type, path, convert_status):
        # setup search params
        params = self._get_params(experiment_type)
        database = self._get_database_path(organism)

        self._ip2.protein_database_user_id = database['user_id']
        self._ip2.protein_database_id = database['database_id']

        files = []

        for f in convert_status['files_converted']:
            if f.endswith('.ms2'):
                files.append(os.path.join(config.UPLOAD_FOLDER, path, f))

        self._ip2.search(params, files)
        link = self._check_search_status()

        return link

    def _get_params(self, experiment_type):
        with open('static/search_params/search_params.json') as f:
            params_map = json.loads(f.read())

        if experiment_type not in params_map:
            raise KeyError('Search params are not available for this experiment_type')

        with open('static/search_params/' + params_map[experiment_type]) as f:
            params = json.loads(f.read())

        return params

    def _get_database_path(self, organism):
        with open('static/search_params/databases.json') as f:
            database_map = json.loads(f.read())

        if organism not in database_map:
            raise KeyError('There is no database set for this organism')

        return database_map[organism]

    def _check_search_status(self):
        polling_interval = 180
        running = True

        # wait a bit before we poll for status
        time.sleep(polling_interval)

        while running:
            start = time.clock()

            try:
                info = self._ip2.check_job_status()
            except LookupError as e:
                # job was not found, the job is finished or something went
                # horribly wrong
                running = False
                dta_link = self._get_dtaselect()
                return dta_link

        work_duration = time.clock() - start
        time.sleep(polling_interval - work_duration)

    def _get_dtaselect(self):
        link = self._ip2.get_dtaselect()
        return link