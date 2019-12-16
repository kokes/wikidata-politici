import json
import os

with open('mapping.json') as f:
    mapping = json.load(f)

typemap = {
    'int': 'int',
    'char(X)': 'varchar',
    'date': 'date',
    'datetime(year to hour)': 'timestamp',
    'datetime(hour to minute)': 'time',
    'datum': 'timestamp',
    'datetime(year to minute)': 'timestamp',
    'char(1)': 'char(1)',
    'datetime(year to second, fraction)': 'timestamp',
    'datetime year to hour': 'timestamp',
    'datetime year to minute': 'timestamp',
    'char(Y)': 'varchar',
    'datetime year to day': 'date',
    'datetime(year to second)': 'timestamp',
}

csv_dir = 'data/csv'
q, idx, fk = [], [], []  # CTEs, indexes, fkeys

for mp in mapping:
    tbl = f'{mp["tema"]}_{mp["tabulka"]}'

    tfn = os.path.abspath(os.path.join(csv_dir, f'{tbl}.csv'))

    print(tbl)

    q.append(f'DROP TABLE IF EXISTS {tbl};')
    q.append(f'CREATE TABLE {tbl} (')
    for j, col in enumerate(mp['sloupce']):
        # CTE
        comma = ',' if j < len(mp['sloupce'])-1 else ''
        typ = typemap[col["typ"]]
        null = '' if col.get('nullable', True) else ' NOT NULL '
        q.append(f'\t"{col["sloupec"]}" {typ}{null}{comma}')

        # comments
        desc = (col['popis'] or '').replace("'", '')

        # indexes
        if col.get('unique'):
            idx.append(
                f'CREATE UNIQUE INDEX {tbl}_{col["sloupec"]}_unique_idx ON {tbl}({col["sloupec"]});')

        # foreign keys
        if col.get('fkey'):
            reftable, refcolumn = col['fkey']
            fkname = 'fk_{}_{}_{}__{}_{}'.format(mp['tema'], mp['tabulka'], col['sloupec'], reftable, refcolumn)

            # TODO: promazat?
            # fk.append(f'ALTER TABLE {tbl} ADD CONSTRAINT {fkname} FOREIGN KEY ({col["sloupec"]}) REFERENCES {reftable} ({refcolumn});')

    # more indexes (non unique)
    for el in mp.get('index', []):
        idx.append(f'CREATE INDEX {tbl}_{"_".join(el)}_idx ON {tbl}({", ".join(el)});')

    q.append(');\n')

# one-time updates
otu = []
otu.append("UPDATE poslanci_osoby SET narozeni = NULL WHERE narozeni = '1900-01-01';")

with open('schema.sql', 'w') as fw:
    fw.write('\n'.join(q + otu + idx + fk))
