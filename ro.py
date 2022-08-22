import sys
import json

query = sys.argv[1]

f = open('tkrData.json')
tkrData = json.load(f)

try:
    sys.stdout.write(tkrData[query.upper()]['roURL'])
except:
    if ('' == query):
        sys.stdout.write('https://ruleonetoolbox.com/dashboard')
    else:
        None
