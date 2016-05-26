"""Perform search of dataset on IP2."""
from .ip2 import IP2
import json
import time


class Search:
    """Perform search of dataset on IP2."""

    def __init__(self, name):
        """Initialize Search with dataset name."""
        self.name = name

    def login(self, username, password):
        """Login to IP2 and keep reference to session."""
        self._ip2 = IP2(self.name)
        return self._ip2.login(username, password)

    def search(self, organism, experiment_type, file_paths):
        """Initiate search on IP2."""
        params = self._get_params(experiment_type)
        database = self._get_database_path(organism)

        self._ip2.protein_database_user_id = database['user_id']
        self._ip2.protein_database_id = database['database_id']

        self._ip2.search(params, file_paths)
        link = self._check_search_status()

        return link

    def _get_params(self, experiment_type):
        with open('cravattdb/auto/search_params/search_params.json') as f:
            params_map = json.loads(f.read())

        if experiment_type not in params_map:
            raise KeyError('Search params are not available for this experiment_type')

        with open('cravattdb/auto/search_params/' + params_map[experiment_type]) as f:
            params = json.loads(f.read())

        return params

    def _get_database_path(self, organism):
        with open('cravattdb/auto/search_params/databases.json') as f:
            database_map = json.loads(f.read())

        if organism not in database_map:
            raise KeyError('There is no database set for this organism')

        return database_map[organism]

    def _check_search_status(self):
        polling_interval = 180

        # wait a bit before we poll for status
        time.sleep(polling_interval)

        while True:
            start = time.clock()

            try:
                self._ip2.check_job_status()
            except LookupError:
                # job was not found, the job is finished or something went
                # horribly wrong
                return self._ip2.get_dtaselect()

            work_duration = time.clock() - start
            time.sleep(polling_interval - work_duration)
