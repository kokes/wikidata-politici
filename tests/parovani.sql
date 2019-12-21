SELECT
	os.id_osoba, os.jmeno, os.prijmeni,
	nullif(nullif(substr(os.narozeni, 1, 10), '1900-01-01'), '') narozeni,
	nullif(nullif(substr(os.umrti, 1, 10), '1900-01-01'), '') umrti,
	zkratka, nazev_organu_cz,
	"od", "do",
	v_ids.*
FROM
	poslanci_osoby os
	INNER JOIN v_poslanci_organy USING (id_osoba)
	LEFT JOIN v_ids ON v_ids.psp_id = os.id_osoba
WHERE
	(zkratka like 'PSP%' or zkratka like 'SE%' or zkratka = 'VládaČR')
	and zkratka != 'PSPC'
	AND v_ids.wikidata_id IS NULL
