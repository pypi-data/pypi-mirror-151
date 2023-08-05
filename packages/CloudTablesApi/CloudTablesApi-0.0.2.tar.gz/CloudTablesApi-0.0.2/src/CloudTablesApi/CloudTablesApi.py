import requests
import json


##############################################
default_options =  {
    'clientId': None,
    'clientMeta': None,
    'clientName': None,
    'conditions': None,
    'domain': 'cloudtables.io',
    'duration': None,
    'role': None,
    'roles': None,
    'ssl': True
}


##############################################
# https://stackoverflow.com/questions/38987
def merge_two_dicts(x, y):
    if (y == None):
        return x

    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z


##############################################
class Row:
    def __init__(self, dataset, id):
        self._dataset = dataset
        self._id = id

    def data(self):
        return self._dataset._api._request('/api/1/dataset/' + self._dataset.id() + '/' + str(self._id), 'GET')

    def delete(self):
        return self._dataset._api._request('/api/1/dataset/' + self._dataset.id() + '/' + str(self._id), 'DELETE')

    def id(self):
        return self._id

    def update(self, data):
        return self._dataset._api._request('/api/1/dataset/' + self._dataset.id() + '/' + str(self._id), 'PUT', data)


##############################################
class Dataset:
    def __init__(self, api, id):
        self._api = api
        self._id = id

    def api(self):
        return self._api

    def data(self):
        return self._api._request('/api/1/dataset/' + self._id, 'GET')

    def id(self):
        return self._id

    def insert(self, data):
        return self._api._request('/api/1/dataset/' + self._id, 'POST', data)

    def row(self, id):
        return Row(self, id)

    def schema(self):
        return self._api._request('/api/1/dataset/' + self._id + '/schema', 'GET')

    def script_tag(self, token, style='d'):
        opts = self._api.options()
        protocol = 'https://' if opts['ssl'] else 'http://'
        subdomain = self._api.subdomain()

        script = '/loader/' + self._id + '/table/' + style + '" data-token="' + token + '"></script>'

        if subdomain:
            script = '<script src="' + protocol + subdomain + '.' + opts['domain'] + script
        else:
            script = '<script src="' + protocol + opts['domain'] + '/io' + script

        return script


##############################################
class CloudTablesApi:
    def __init__(self, key, options=None, subdomain=None):
        self._key = key
        self._subdomain = subdomain
        self._options = merge_two_dicts(default_options, options)
        self._condition = None

    def _request(self, path, type, data=None):
        opts = self._options

        if self._condition is not None:
            opts['conditions'] = self._condition

        if data is None:
            data = {}

        data['key'] = self._key

        if self._subdomain:
            host = self._subdomain + '.' + self._options['domain']
        else:
            host = self._options['domain']
            path = '/io' + path

        protocol = 'https' if self._options['ssl'] else 'http'
        url = protocol + '://' + host + path

        if type == 'POST':
            r = requests.post(url, data=data, params=opts)
        elif type == 'PUT' :
            r = requests.put(url, data=data, params=opts)
        elif type == 'DELETE':
            r = requests.delete(url, data=data, params=opts)
        elif type == 'GET':
            r = requests.get(url, data=data, params=opts)
        else:
            raise Exception('Internal error: unknown type - ' + type)

        return r.json()

    def options(self):
        return self._options

    def subdomain(self):
        return self._subdomain

    def condition(self, condition):
        self._condition = json.dumps(condition)

    def dataset(self, id):
        return Dataset(self, id)

    def datasets(self):
        return self._request('/api/1/datasets', 'GET')

    def token(self):
        return self._request('/api/1/access', 'POST')

