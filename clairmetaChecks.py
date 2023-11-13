#!/usr/bin/env python3

import ast
import textwrap
import json
import importlib
import traceback
from inspect import getmembers, isfunction, getsource
from clairmeta.settings import DCP_CHECK_SETTINGS


def extract_error_msg(func):
    errors = []

    ast_func = ast.parse(textwrap.dedent(getsource(func)))
    for node in ast.walk(ast_func.body[0]):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                func_name = node.func.attr
            else:
                func_name = node.func.id

            if func_name in ["error", "fatal_error"]:
                if isinstance(node.args[0], ast.Constant):
                    errors += [node.args[0].value]
                elif isinstance(node.args[0], ast.Call):
                    #print("###: "+ast.dump(node.args[0].func.value.s))
                    errors += [node.args[0].func.value.s]

    return errors

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
        funcs2 = [f for f in funcs if f[0].startswith("check_")]

        functionNumber = 1
    
        print("## "+str(moduleNumber)+" "+k)

        for f in funcs2:
            name = f[0]
            doc = f[1].__doc__
            error_msgs = extract_error_msg(f[1])
           
            print("### "+str(moduleNumber)+"."+str(functionNumber)+" "+name)
            print("```")
            print(doc)
            print("```")
            print("")
            print("#### Error messages")
            print("```")
            for msg in error_msgs:
                print(msg)
            print("```")
            print("")
            functionNumber += 1
        moduleNumber += 1
        print("\n---\n")

    except Exception as e:
        print(str(e))
        traceback.print_exc()
