SELECT
	id_osoba, v_ids.wikidata_id, jmeno, prijmeni, min(od), min(do)
FROM
	v_poslanci_organy org
	inner join v_ids on v_ids.psp_id = org.id_osoba
	where zkratka like 'SE%' and zkratka != 'SEI'
	and wikidata_id not in (select substr(senator, instr(senator, '/Q') + 1)from wikidata_senatori)
	group by 1
LIMIT 1000;
