import pathlib, requests, subprocess

def quantify(name, dta_link, experiment_type, path):
    r = requests.get(dta_link)

    dta_path = path.joinpath('dta')
    dta_filename = 'DTASelect-filter_{}_foo.txt'.format(name)
    dta_path.mkdir()

    with open(str(dta_path.joinpath(dta_filename)), 'w') as f:
        f.write(r.text)

    return_code = subprocess.Popen([
        'cimage2',
        _get_params_path(experiment_type),
        name
    ], cwd=dta_path).wait()

    if return_code:
        combine(path, experiment_type)
    else:
        return False

def combine(path, experiment_type):
    args = [
        'cimage_combine',
        'output_rt_10_sn_2.5.to_excel.txt',
        'dta'
    ]

    if experiment_type is not 'isotop':
        args.insert(1, 'by_protein')

    return subprocess.Popen(args, cwd=path).wait()

def _get_params_path(experiment_type):
    return os.path.join('static', 'cimage_params', experiment_type + '.params')