# from db.db import Database
from bs4 import BeautifulSoup
from distutils.util import strtobool
import flask.json, requests, re

class IP2:
    ''' 
    Helper class to programatically upload and search datasets on IP2.
    Each instance of the class is tied to an experiment
    '''
    def __init__(self, name=None):
        # self._db = Database()
        self.dataset_name = name
        self.project_id = 0
        self.loggedOn = False
        self.project_name = 'cravatdb'

    def search(self, params):
        ''' convenience method '''
        self.login(params['username'], params['password'])
        self.set_project_id()
        self.set_experiment_id()
        self.set_experiment_path()
        self.upload_spectra(params['files'])
        self.prolucid_search()
        self.check_job_status()

    def login(self, username, password):
        ''' login to IP2 '''
        login_req = requests.post('http://goldfish.scripps.edu/ip2/j_security_check', {
            'j_username': username,
            'j_password': password,
            'rememberMe': 'on',
            'login': 'Login'
        })

        self.cookies = login_req.history[0].cookies

        return True

    def logout(self):
        ''' log out of IP2 '''
        requets.get('http://goldfish.scripps.edu/ip2/logout.jsp', cookies=self.cookies)

    def set_project_id(self):
        ''' get project id for cravattdb project or else create new project '''
        project_id = self._find_project_id()

        if not project_id:
            self._create_new_project()
            project_id = self._find_project_id()

        self.project_id = project_id
        return project_id

    def set_experiment_id(self, name):
        exp_req = requests.get(
            'http://goldfish.scripps.edu/ip2/viewExperiment.html', 
            {
                'projectName': self.project_name,
                'pid': self.project_id
            }, 
            cookies=self.cookies
        )

        soup = BeautifulSoup(exp_req.text)
        table = soup.find('table', id='experimentO')
        forms = table.find_all('form', action='editExperiment.html')

        for form in forms:
            sampleInput = form.find('input', attrs={'name':'sampleName'}, value=name)

            if sampleInput:
                self.experiment_id = int(form.find('input', attrs={'name': 'expId'})['value'])
                return

    def set_experiment_path(self):
        path_req = requests.get(
            'http://goldfish.scripps.edu/ip2/eachExperiment.html', 
            {
                'experimentId': self.experiment_id,
                'projectName': self.project_name,
                'pid': self.project_id
            },
            cookies = self.cookies
        )

        soup = BeautifulSoup(path_req.text)

        # soup.find('b', text="Spectra Path:").next_sibling.string.strip().replace('/spectra', '')
        text = soup.find('div', class_='add_spectra').find('script', text=re.compile(r'.+expPath.+')).contents[0]
        path = re.search('"expPath":\s"([\w/]+)"', text)
        self.experiment_path = path.group(1)


    def create_experiment(self, name):
        ''' create experiment under project '''

        requests.post(
            'http://goldfish.scripps.edu/ip2/addExperiment.html',
            {
                'pid': self.project_id,
                'projectName': self.project_name,
                'sampleName': name,
                'sampleDescription': '',
                'instrumentId': 34,
                'month': 6,
                'date': '03',
                'year': 2015,
                'description': ''
            },
            cookies=self.cookies
        )

    def upload_spectra(self, files):
        ''' upload .ms2 files '''
        for f in files:
            requests.post(
                'http://goldfish.scripps.edu/helper/spectraUpload.jsp',
                {
                    'Filename': f.name,
                    'expPath': self.experiment_path,
                    'Filedata': f,
                    'Upload': 'Submit Query'
                },
                cookies=self.cookies,
                files={ f.name: f}
            )

    def prolucid_search(self, params, protein_database_user_id, protein_database_id):
        ''' perform prolucid search '''

        params.update({
            'expId': self.experiment_id,
            'expPath': self.experiment_path,
            'sampleName': self.experiment_name,
            'pid': self.project_id,
            'projectName': self.project_name,
            'sp.proteinUserId': protein_database_user_id,
            'sp.proteinDbId': protein_database_id  
        })

        requests.post(
            'http://goldfish.scripps.edu/ip2/prolucidProteinId.html',
            params,
            cookies=self.cookies
        )

    def check_job_status(self, name):
        ''' check if job is finished '''
        session_text = requests.get('http://goldfish.scripps.edu/ip2/dwr/engine.js').text
        session_id = re.search('_origScriptSessionId\s=\s"(\w+)"', session_text).group(1)

        status_req = requests.post(
            'http://goldfish.scripps.edu/ip2/dwr/call/plaincall/JobMonitor.getSearchJobStatus.dwr',
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
            headers={ 'content-type': 'plain/text' }
        )

        # find sample and get identifier
        id = re.search('s(\d+)\.sampleName="' + name + '"', status_req.text).group(1)

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
        ''' finally grab what we came for '''
        path_req = requests.get(
            'http://goldfish.scripps.edu/ip2/eachExperiment.html', 
            {
                'experimentId': self.experiment_id,
                'projectName': self.project_name,
                'pid': self.project_id
            },
            cookies = self.cookies
        )

        soup = BeautifulSoup(path_req.text)

        search_td = soup.find('td', text=re.compile(self.search_id))

        for el in search_td.next_siblings:
            if el.name == 'td':
                link = el.find('a', text='View').attrs['href']
                break

        # if not link:
        dta_req = requests.get('http://goldfish.scripps.edu' + link, cookies=self.cookies)
        soup = BeautifulSoup(dta_req.text)
        dta_link = 'http://goldfish.scripps.edu' + soup.find('a', text=re.compile('DTASelect-filter')).attrs['href']

        return requests.get(dta_link, cookies=self.cookies)


    def _find_project_id(self):
        project_req = requests.get(
            'http://goldfish.scripps.edu/ip2/viewProject.html',
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
        ''' create new ip2 project for cravattdb experiments '''
        requests.post(
            'http://goldfish.scripps.edu/ip2/addProject.html', 
            {
                'projectName': self.project_name,
                'desc': ''
            },
            cookies=self.cookies
        )