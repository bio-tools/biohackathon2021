import json, re
from boltons.iterutils import remap
from collections import defaultdict
import operator


def read_local_tools():
    with open('../RScriptVeit/bio.toolsFullDump.json') as f:
      return json.load(f)


def clean_tools_list(tools_list):
    drop_false = lambda path, key, value: bool(value)
    return [remap(tool, visit=drop_false) for tool in tools_list]

def has_data_with_format(tool):
    for f in tool.get('function',[]):
        for i in f.get('input',[]):
            if i.get('data') and i['data']['uri'].lower() == 'http://edamontology.org/data_0006' and i.get('format'):
                return True
        for o in f.get('output',[]):
            if o.get('data') and o['data']['uri'].lower() == 'http://edamontology.org/data_0006' and o.get('format'):
                return True
    return False

all_tools = clean_tools_list(read_local_tools())

for tool in all_tools:
    if has_data_with_format(tool):
        print(tool['biotoolsID'])
