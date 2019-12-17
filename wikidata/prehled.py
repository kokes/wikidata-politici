import csv
import json
import os
from urllib.request import urlopen
from urllib.parse import urlencode

import sqlite3

# nahraj z query service do CSV
url = 'https://query.wikidata.org/sparql'

query = '''SELECT ?item ?itemLabel ?Czech_parliament_ID ?official_website ?date_of_birth ?sex_or_genderLabel ?place_of_birthLabel ?given_nameLabel ?Facebook_ID ?Twitter_username ?Instagram_username WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  OPTIONAL { ?item wdt:P6828 ?Czech_parliament_ID. }
  OPTIONAL {  }
  OPTIONAL { ?item wdt:P856 ?official_website. }
  OPTIONAL { ?item wdt:P569 ?date_of_birth. }
  OPTIONAL { ?item wdt:P21 ?sex_or_gender. }
  OPTIONAL { ?item wdt:P19 ?place_of_birth. }
  OPTIONAL { ?item wdt:P735 ?given_name. }
  OPTIONAL { ?item wdt:P2013 ?Facebook_ID. }
  OPTIONAL { ?item wdt:P2002 ?Twitter_username. }
  OPTIONAL { ?item wdt:P2003 ?Instagram_username. }
}
LIMIT 10000'''

tdr = 'wikidata'
os.makedirs(tdr, exist_ok=True)

r = urlopen(url + '?' + urlencode({'query': query, 'format': 'json'}))

dt = json.load(r)

tfn = os.path.join(tdr, 'prehled.csv')
with open(tfn, 'w', encoding='utf8') as fw:
    cw = csv.writer(fw)
    hd = dt['head']['vars']
    cw.writerow(hd)
    for row in dt['results']['bindings']:
        cw.writerow(row.get(col, {}).get('value') for col in hd)


# nahraj do SQLite
db = 'data.db'
conn = sqlite3.connect(db)

conn.executescript('''
drop table if exists wikidata_prehled;
create table wikidata_prehled (
    {}
);
'''.format(', '.join([j + ' string' for j in hd])))

query = 'INSERT INTO wikidata_prehled VALUES({})'.format(', '.join(['?']*len(hd)))

with open(tfn) as f:
    cr = csv.reader(f)
    next(cr)
    for row in cr:
        row = [None if j == '' else j for j in row]
        conn.execute(query, row)
conn.commit()
