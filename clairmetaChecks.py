#!/usr/bin/env python3

import json
import importlib
from inspect import getmembers, isfunction
from clairmeta.settings import DCP_CHECK_SETTINGS


all_checks = {}

print("""---
documentclass: book
papersize: a4
geometry: margin=1.0in
indent: true
fontfamily: helvet
header-includes:
  - \\renewcommand{\\familydefault}{\\sfdefault}
...
""")

print("# ClairMeta v1.5.0 list of checks")

prefix = DCP_CHECK_SETTINGS['module_prefix']
moduleNumber = 1
for k, v in DCP_CHECK_SETTINGS['modules'].items():
    try:
        module_path = 'clairmeta.' + prefix + k
        module = importlib.import_module(module_path)
        funcs = getmembers(module.Checker, isfunction)
        funcs = [f for f in funcs if f[0].startswith("check_")]
        checks = [(f[0], f[1].__doc__) for f in funcs]

        all_checks[module.__name__] = checks

        functionNumber = 1
    
        print("## "+str(moduleNumber)+" "+k)

        for f in funcs:
            name = f[0]
            doc = f[1].__doc__    
           
            print("### "+str(moduleNumber)+"."+str(functionNumber)+" "+name)
            print("```")
            print(doc)
            print("```")
            print("")
            functionNumber += 1
        moduleNumber += 1
        print("\n---\n")

    except Exception as e:
        print(str(e))
