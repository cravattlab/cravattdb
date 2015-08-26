import json, time, requests, os
import models.convert as convert
from functools import partial
from models.ip2 import IP2
from models.upload import Upload
from glob import glob

class Search:
    def __init__(self, name):
        self.name = name

    def login(self, username, password):
        self.username = username
        self._ip2 = IP2(self.name)
        return self._ip2.login(username, password)

    def search(self, files, organism, experiment_type, param_mods=None):
        # save RAW files to disk
        self.path = os.path.join(self.username, self.name)
        Upload(files, self.path)

        # setup search params
        params = self._get_params(experiment_type, param_mods)
        database = self._get_database_path(organism)

        self._ip2.protein_database_user_id = database['user_id']
        self._ip2.protein_database_id = database['database_id']

        # convert to .ms2 and start ip2 search when done
        convert.convert(self.path, partial(self._search, params))
        link = self._check_search_status()

        print(link)

    def _search(self, params):
        ms2_files = self._get_ms2_files()
        self._ip2.search(params, ms2_files)

    def _get_params(self, experiment_type, param_mods=None):
        with open('static/search_params/search_params.json') as f:
            params_map = json.loads(f.read())

        if experiment_type not in params_map:
            raise KeyError('Search params are not available for this experiment_type')

        with open('static/search_params/' + params_map[experiment_type]) as f:
            params = json.loads(f.read())

        # if param_mods:
        #     params.update(json.loads(param_mods))

        return params

    def _get_database_path(self, organism):
        with open('static/search_params/databases.json') as f:
            database_map = json.loads(f.read())

        if organism not in database_map:
            raise KeyError('There is no database set for this organism')

        return database_map[organism]

    def _get_ms2_files(self):
        paths = glob(os.path.join('uploads', self.username, self.name, '*.ms2'))
        files = []

        for path in paths:
            files.append(open(path, 'rb'))

        return files

    def _check_search_status(self):
        polling_interval = 180
        running = True

        while running:
            try:
                info = self._ip2.check_job_status()
            except LookupError as e:
                # job was not found, the job is finished or something went
                # horribly wrong
                running = False
                dta_link = self._get_dtaselect()
                return dta_link

    def _get_dtaselect(self):
        link = self._ip2.get_dtaselect()
        return link