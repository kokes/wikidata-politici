DROP VIEW IF EXISTS v_poslanci_organy;
CREATE VIEW v_poslanci_organy AS
SELECT
	os.id_osoba,
	os.jmeno, os.prijmeni, os.narozeni,
	org.id_organ, org.zkratka, org.nazev_organu_cz,
	nullif(substr(zr.od_o, 1, 10), '') "od",
	nullif(substr(zr.do_o, 1, 10), '') "do"
FROM
	poslanci_osoby os
	inner join poslanci_zarazeni zr
		ON zr.id_osoba = os.id_osoba
	inner join poslanci_organy org
		ON org.id_organ = zr.id_of
where cl_funkce = 0
