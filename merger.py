data = [
    {'tags__1': {'a': '1', 'b': '55'}},
    {'togs__3': {'a': '3', 'b': '59'}},
    {'tags__2': {'a': '2', 'b': '57'}},

    {'wother': {'c': '1', 'd': '22'}},
    {'togs__4': {'a': '4', 'b': '55'}},
    {'abc': {'a': '1', 'b': '55'}},
]

import re


def extract_entry(data, k):
    return [entry for entry in data if k in entry][0]


def merger(data):
    new_data = []
    temporary_map = {}
    expressionRegex = re.compile("([a-zA-Z]*)__(\d+)")

    all_keys = []
    for entry in data:
        all_keys.extend([k for k in entry])

    for k in all_keys:
        mo = expressionRegex.findall(k)
        if len(mo) == 0:
            new_data.append(extract_entry(data, k))
        else:
            key = mo[0][0]
            number = int(mo[0][1]) - 1
            if key not in temporary_map:
                temporary_map[key] = []
            temporary_map[key].insert(number, extract_entry(data, k)[k])

    for k, v in temporary_map.items():
        new_data.append({k:v})

    return new_data


print(data)
print(merger(data))
