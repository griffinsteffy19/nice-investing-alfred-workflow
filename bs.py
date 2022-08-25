import sys

query = sys.argv[1]

try:
    sys.stdout.write('https://www.bamsec.com/entity-search/search?q='+query)
except:
    if ('' == query):
        sys.stdout.write('https://www.bamsec.com')
    else:
        None
