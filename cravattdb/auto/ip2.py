"""Rough interface to IP2."""
from bs4 import BeautifulSoup
from distutils.util import strtobool
from urllib.parse import parse_qs, urlparse, urljoin
import config.config as config
import requests
import re


class IP2:
    """Helper class to programatically upload and search datasets on IP2."""

    def __init__(self, name=None):
        """Provide sensible defaults."""
        self.dataset_name = name
        self.project_id = 0
        self.loggedOn = False
        self.project_name = 'cravattdb'
        self.search_id = None

    def search(self, params, file_paths):
        """Convenience method."""
        self.project_id = self.get_project_id()
        self.create_experiment()
        self.experiment_id = self.get_experiment_id()
        self.experiment_path = self.get_experiment_path()
        self.upload_spectra(file_paths)
        self.prolucid_search(params)

    def login(self, username, password):
        """Login to IP2."""
        login_req = requests.post(
            urljoin(config.IP2_URL, 'ip2/j_security_check'), 
            {
                'j_username': username,
                'j_password': password,
                'rememberMe': 'remember-me'
            }
        )

        self.cookies = login_req.history[0].cookies
        return 'error' not in login_req.url

    def logout(self):
        """Log out of IP2."""
        requests.get(urljoin(config.IP2_URL, 'logout.jsp'), cookies=self.cookies)

    def get_project_id(self):
        """Get project id for cravattdb project or else create new project."""
        project_id = self._find_project_id()

        if not project_id:
            self._create_new_project()
            project_id = self._find_project_id()

        return project_id

    def get_experiment_id(self):
        """After uploading experiment, fetch the id."""
        exp_req = requests.get(
            urljoin(config.IP2_URL, 'ip2/viewExperiment.html'),
            {
                'projectName': self.project_name,
                'pid': self.project_id
            },
            cookies=self.cookies
        )

        soup = BeautifulSoup(exp_req.text)
        forms = soup.find_all('form', action='editExperiment.html')

        for form in forms:
            sample_input = form.find('input', attrs={'name': 'sampleName'}, value=self.dataset_name)
            if sample_input:
                return int(form.find('input', attrs={'name': 'expId'})['value'])

    def get_experiment_path(self):
        """Get path to experiment and save as property."""
        path_req = requests.get(
            urljoin(config.IP2_URL, 'ip2/eachExperiment.html'),
            {
                'experimentId': self.experiment_id,
                'projectName': self.project_name,
                'pid': self.project_id
            },
            cookies=self.cookies
        )

        soup = BeautifulSoup(path_req.text)
        wrap = soup.find('div', class_='add_quality_check_details')
        link = wrap.find_all('a')[1].attrs['href']
        query_string = urlparse(link).query
        return parse_qs(query_string)['expPath'][0]

    def create_experiment(self):
        """Create experiment under project."""
        requests.post(
            urljoin(config.IP2_URL, 'ip2/addExperiment.html'),
            {
                'pid': self.project_id,
                'projectName': self.project_name,
                'sampleName': self.dataset_name,
                'sampleDescription': '',
                'instrumentId': 34,
                'month': 6,
                'date': '03',
                'year': 2015,
                'description': ''
            },
            cookies=self.cookies
        )

    def remove_experiment(self):
        """Remove experiment from project."""
        requests.post(
            urljoin(config.IP2_URL, 'ip2/deleteExperiment.html'),
            {
                'pid': self.project_id,
                'projectName': self.project_name,
                'expId': self.experiment_id,
                'delete': 'true'
            }
        )

    def upload_spectra(self, file_paths):
        """Upload .ms2 files."""
        for path in file_paths:
            with open(str(path), 'rb') as f:
                requests.post(
                    urljoin(config.IP2_URL, 'ip2/fileUploadAction.html'),
                    params={
                        'filePath': self.experiment_path
                    },
                    data={
                        'name': path.name,
                        'chunk': 0,
                        'chunks': 1
                    },
                    cookies=self.cookies,
                    files={'file': (path.name, f, 'application/octet-stream')}
                )

                requests.post(
                    urljoin(config.IP2_URL, 'ip2/fileUploadAction.html'),
                    params={
                        'fileFileName': path.name,
                        'filePath': self.experiment_path,
                        'startProcess': 'completed',
                        'type': 'spectra'
                    },
                    cookies=self.cookies
                )

                requests.post(
                    urljoin(config.IP2_URL, 'ip2/fileUploadAction.html'),
                    params={
                        'fileFileName': path.name,
                        'filePath': self.experiment_path,
                        'startProcess': 'post',
                        'type': 'spectra',
                        'flag': 'ko'
                    },
                    cookies=self.cookies
                )

    def prolucid_search(self, params):
        """Perform prolucid search."""
        params.update({
            'expId': self.experiment_id,
            'expPath': self.experiment_path,
            'sampleName': self.dataset_name,
            'pid': self.project_id,
            'projectName': self.project_name,
            'sp.proteinUserId': self.protein_database_user_id,
            'sp.proteinDbId': self.protein_database_id
        })

        requests.post(
            urljoin(config.IP2_URL, 'ip2/prolucidProteinId.html'),
            params,
            cookies=self.cookies
        )

    def check_job_status(self):
        """Check if job is finished."""
        session_text = requests.get(urljoin(config.IP2_URL, 'ip2/dwr/engine.js')).text
        session_id = re.search('_origScriptSessionId\s=\s"(\w+)"', session_text).group(1)

        status_req = requests.post(
            urljoin(config.IP2_URL, 'ip2/dwr/call/plaincall/JobMonitor.getSearchJobStatus.dwr'),
            {
                'callCount': 1,
                'page': '/ip2/jobstatus.html',
                'httpSessionId': '',
                'scriptSessionId': session_id,
                'c0-scriptName': 'JobMonitor',
                'c0-methodName': 'getSearchJobStatus',
                'c0-id': 0,
                'batchId': 0
            },
            cookies=self.cookies,
            headers={'content-type': 'plain/text'}
        )

        # find sample and get identifier
        result = re.search('s(\d+)\.sampleName="' + self.dataset_name + '"', status_req.text)

        if result:
            id = result.group(1)
        else:
            raise LookupError('There is no IP2 search job for {}'.format(self.dataset_name))

        # now collect all the information
        info = re.findall('s' + id + '\.(\w+)=([\w"\._\-\s]+);', status_req.text)
        info = dict(info)

        # massaging
        info['finished'] = bool(strtobool(info['finished']))
        info['jobId'] = int(info['jobId'])
        info['progress'] = float(info['progress'])

        # the first time we check, jot down the search id
        if not self.search_id:
            self.search_id = info['jobId']

        return info

    def get_dtaselect(self):
        """Finally grab what we came for."""
        path_req = requests.get(
            urljoin(config.IP2_URL, 'ip2/eachExperiment.html'),
            {
                'experimentId': self.experiment_id,
                'projectName': self.project_name,
                'pid': self.project_id
            },
            cookies=self.cookies
        )

        soup = BeautifulSoup(path_req.text)

        search_td = soup.find('td', text=re.compile(str(self.search_id)))

        for el in search_td.next_siblings:
            if el.name == 'td':
                link = el.find('a', text='View').attrs['href']
                break

        dta_req = requests.get(urljoin(config.IP2_URL, link), cookies=self.cookies)
        soup = BeautifulSoup(dta_req.text)
        dta_link = urljoin(config.IP2_URL, soup.find('a', text=re.compile('DTASelect-filter')).attrs['href'])

        return dta_link

    def _find_project_id(self):
        project_req = requests.get(
            urljoin(config.IP2_URL, 'ip2/viewProject.html'),
            cookies=self.cookies
        )

        text = project_req.text
        index = text.find(self.project_name)

        if index != -1:
            text = text[index:]
            return int(re.search('viewExperiment\.html\?pid=(\d+)', text).group(1))
        else:
            return False

    def _create_new_project(self):
        """Create new ip2 project for cravattdb experiments."""
        requests.post(
            urljoin(config.IP2_URL, 'ip2/addProject.html'),
            {
                'projectName': self.project_name,
                'desc': ''
            },
            cookies=self.cookies
        )
