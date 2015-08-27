import os, requests, subprocess

def quantify(name, dta_link, experiment_type, path):
    r = requests.get(dta_link)

    dta_path = os.path.join(path, 'dta')
    dta_filename = 'DTASelect-filter_{}_foo.txt'.format(name)
    os.makedirs(dta_path)

    with open(os.path.join(dta, dta_filename), 'rb') as f:
        f.write(r.text)

    return_code = subprocess.call([
        'cimage2',
        _get_params_path(experiment_type),
        name
    ], cwd=dta_path).return_code

    if return_code:
        combine(path, experiment_type)
    else:
        return False

def combine(path, experiment_type):
    return subprocess.call([
        'cimage_combine',
        'by_protein',
        'output_rt_10_sn_2.5.to_excel.txt',
        'dta'
    ], cwd=path).return_code

def _get_params(experiment_type):
    return 'blergh'