import yaml
import collections
from location_data import datafiles

stats = collections.Counter()
types = collections.Counter()

for file in datafiles:
    full_filename = f'data/{file}.yaml'
    data = yaml.load(open(full_filename))
    for d in data:
        for key, value in d.items():
            stats[key] += 1
            if key == 'type':
                types[value] += 1
    yaml.dump(data, open(full_filename, 'w'), allow_unicode=True, default_flow_style=False)

for k, v in stats.most_common():
    print(k, v)
print()
for k, v in types.most_common():
    print(k, v)
