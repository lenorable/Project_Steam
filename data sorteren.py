import json
import pprint
def jsonsorteer():
    infile = open('dummy.json', 'r')
    info = json.load(infile)
    goed = (json.dumps(info, indent = 4, sort_keys=True))
    return print(goed)

print(jsonsorteer())
