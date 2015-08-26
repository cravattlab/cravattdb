import requests, time
import config.config as config

def convert(path, callback = None):
    # start conversion
    requests.get(config.CONVERT_URL + '/convert/' + path)

    # poll every 30 seconds
    polling_interval = 30
    running = True

    if not callback: return True

    # if we are passed a callback then return only when conversion is done
    while running:
        start = time.clock()
        status = get_status(path)

        if status['status'] == 'success':
            running = False
            if callback: callback(status)
            return status
            break

        work_duration = time.clock() - start
        time.sleep(polling_interval - work_duration)

def get_status(path):
    r = requests.get(config.CONVERT_URL + '/status/' + path)
    return r.json()