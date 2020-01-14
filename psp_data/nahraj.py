import csv
import json
import os
import sqlite3

from glob import glob

from generuj_csv import main as generuj_csv
from sql_schema import main as sql_schema

def main():
    generuj_csv()
    sql_schema()

    cdr = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cdr, 'mapping.json')) as f:
        mapping = json.load(f)

    conn = sqlite3.connect('data.db')
    conn.executescript(open(os.path.join(cdr, 'schema.sql')).read())

    for mp in mapping:
        tabulka = f'{mp["tema"]}_{mp["tabulka"]}'

        drn = os.path.join(cdr, 'data/csv')
        fn = os.path.join(drn, tabulka + '.csv')

        qs = ', '.join(['?']*len(mp['sloupce']))
        query = 'INSERT INTO {} VALUES({})'.format(tabulka, qs)
        with open(fn) as f:
            cr = csv.reader(f)
            next(cr)
            for row in cr:
                row = [None if j == '' else j for j in row] # empty -> NULL
                conn.execute(query, row)

    for fn in glob(os.path.join(cdr, 'views', '*.sql')):
        conn.executescript(open(fn).read())

    conn.commit()


if __name__ == '__main__':
    main()
