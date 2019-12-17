import csv
import json
import os
import sqlite3

from glob import glob

with open('mapping.json') as f:
    mapping = json.load(f)

conn = sqlite3.connect('data.db')
conn.executescript(open('schema.sql').read())

for mp in mapping:
    tabulka = f'{mp["tema"]}_{mp["tabulka"]}'

    drn = 'data/csv'
    fn = os.path.join(drn, tabulka + '.csv')

    qs = ', '.join(['?']*len(mp['sloupce']))
    query = 'INSERT INTO {} VALUES({})'.format(tabulka, qs)
    with open(fn) as f:
        cr = csv.reader(f)
        next(cr)
        for row in cr:
            conn.execute(query, row)

for fn in glob('views/*.sql'):
    conn.execute(open(fn).read())

conn.commit()