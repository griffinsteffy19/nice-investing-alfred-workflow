import sys
import json

query = sys.argv[1]

f = open('tkrData.json')
tkrData = json.load(f)

try:
    sys.stdout.write(tkrData[query.upper()]['bsURL'])
except:
    if ('' == query):
        sys.stdout.write('https://www.bamsec.com')
    else:
        None
