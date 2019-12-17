CREATE VIEW v_poslanci_funkce AS
SELECT
	os.id_osoba, jmeno, prijmeni, substr(narozeni, 0, 11) as narozeni,
	substr(od_o, 0, 11) as od_o, substr(do_o, 0, 11) as do_o,
	nazev_funkce_cz, zkratka, nazev_organu_cz
FROM
	poslanci_osoby os
	inner join poslanci_zarazeni zr
		ON zr.id_osoba = os.id_osoba
	inner join poslanci_funkce fn
		ON fn.id_funkce = zr.id_of
	inner join poslanci_organy org
		ON org.id_organ = fn.id_organ
	
where cl_funkce = 1
-- and nazev_organu_cz in ('Vláda České republiky', 'Poslanecká sněmovna', 'Národní shromáždění', 'Evropský parlament', 'Bankovní rada České národní banky')

order by zkratka, nazev_funkce_cz, od_o