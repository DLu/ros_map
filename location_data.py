import yaml


ORDER = ['name', 'type', 'lat', 'long', 'address', 'description', 'link']
datafiles = ['africa', 'america', 'asia', 'australia', 'europe']


def _custom_dictorder(self, data):
    items = sorted(data.items(), key=lambda d: ORDER.index(d[0]))
    return self.represent_mapping('tag:yaml.org,2002:map', items)


def _custom_listorder(self, data):
    data = sorted(data, key=lambda d: d['name'])
    return self.represent_list(data)


yaml.add_representer(dict, _custom_dictorder)
yaml.add_representer(list, _custom_listorder)
