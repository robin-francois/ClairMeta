#!/usr/bin/env python3

import json
import importlib
from inspect import getmembers, isfunction
from clairmeta.settings import DCP_CHECK_SETTINGS


all_checks = {}

prefix = DCP_CHECK_SETTINGS['module_prefix']
for k, v in DCP_CHECK_SETTINGS['modules'].items():
    try:
        module_path = 'clairmeta.' + prefix + k
        module = importlib.import_module(module_path)
        funcs = getmembers(module.Checker, isfunction)
        funcs = [f for f in funcs if f[0].startswith("check_")]
        checks = [(f[0], f[1].__doc__) for f in funcs]

        all_checks[module.__name__] = checks

        for f in funcs:
            name = f[0]
            doc = f[1].__doc__
            pretty_name = list(filter(None, doc.split('\n')))[0].strip()
            print(",".join(['"'+pretty_name+'"',name,'"'+f[1].__doc__.replace('"',"'")+'"']))

    except Exception as e:
        print(str(e))

with open('result.json', 'w') as fp:
    json.dump(all_checks, fp)
