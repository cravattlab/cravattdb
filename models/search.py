import json
import xmltodict
import time
import requests
from models.ip2 import IP2
from models.upload import Upload
from functools import partial

class Search:
    def __init__(self, name):
        self.name = name

    def login(self, username, password):
        self._ip2 = IP2()
        self._ip2.login(username, password)
        self.username = username

    def search(self, files, organism, experiment_type, param_mods):
        # save RAW files to disk
        upload = Upload(files, self.username, self.name)

        # setup search params
        params = self._get_params(experiment_type, param_mods)
        database = self._get_database_path(organism)
        params.update({'database_name': database['name']})

        # convert to .ms2 and start ip2 search when done
        self.files = self._convert(
            upload.files,
            partial(self._ip2.search, params, database['user_id'], database['database_id'])
        )

    def _get_params(self, experiment_type, param_mods):
        with open('static/search_params/search_params.json') as f:
            params_map = json.loads(f.read())

        if experiment_type not in params_map:
            raise KeyError('Search params are not available for this experiment_type')

        with open('static/search_params/' + params_map[experiment_type]) as f:
            params = xmltodict.parse(f.read())

        # if param_mods:
        #     params.update(json.loads(param_mods))

        return params

    def _get_database_path(self, organism):
        with open('static/search_params/databases.json') as f:
            database_map = json.loads(f.read())

        if organism not in database_map:
            print organism
            raise KeyError('There is no database set for this organism')

        return database_map[organism]

    def _convert(self, files, callback):
        # start conversion
        requests.get(
            'http://localhost:5001/convert/' + self.username + '/' + self.name,
        )

        # poll every 30 seconds
        polling_interval = 30
        running = True

        while running:
            start = time.clock()
            status = self._check_convert_status()

            if 'success' in status:
                running = false
                callback()
                break

            work_duration = time.clock() - start
            time.sleep(polling_interval - work_duration)

    def _check_convert_status(self):
        r = requests.get(
            'http://localhost:5001/status/' + self.username + '/' + self.name,
        )

        return r.json()