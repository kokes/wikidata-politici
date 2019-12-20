import csv
import json
import os
import sys
from glob import glob
from urllib.request import urlopen
from urllib.parse import urlencode

import sqlite3

def query_wikidata(query):
    url = 'https://query.wikidata.org/sparql'
    r = urlopen(url + '?' + urlencode({'query': query, 'format': 'json'}))
    dt = json.load(r)

    hd = dt['head']['vars']
    for row in dt['results']['bindings']:
        data = [row.get(col, {}).get('value') for col in hd]
        yield dict(zip(hd, data))

if __name__ == '__main__':
    db = 'data.db'
    conn = sqlite3.connect(db)
    wanted = None
    if len(sys.argv) > 1:
        wanted = sys.argv[1]

    tdr = os.path.dirname(os.path.abspath(__file__))
    qdr = os.path.join(tdr, 'queries', '*.sparql')
    cdr = os.path.join(tdr, 'csv')
    os.makedirs(cdr, exist_ok=True)

    for fn in glob(qdr):
        _, sfn = os.path.split(fn)
        table, _, _ = sfn.rpartition('.')
        if wanted and table != wanted:
            continue
        full_table = f'wikidata_{table}'
        print('Nahravam', table, 'do', full_table)

        with open(fn) as f:
            query = f.read()

        tcf = os.path.join(cdr, table + '.csv')
        data = query_wikidata(query)
        with open(tcf, 'wt', encoding='utf8') as fw:
            first_row = next(data)
            cw = csv.DictWriter(fw, fieldnames=first_row.keys())
            cw.writeheader()
            cw.writerow(first_row)
            for row in data:
                cw.writerow(row)

        with open(tcf, 'rt', encoding='utf8') as f:
            cr = csv.reader(f)
            hd = next(cr)

            conn.executescript('''
            drop table if exists {0};
            create table {0} (
                {1}
            );
            '''.format(full_table, ', '.join([j + ' string' for j in hd])))

            query = 'INSERT INTO {} VALUES({})'.format(full_table, ', '.join(['?']*len(hd)))

            for row in cr:
                row = [None if j == '' else j for j in row]
                conn.execute(query, row)
            conn.commit()
