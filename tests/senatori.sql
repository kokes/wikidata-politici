select
   v_ids.wikidata_id,
   org.id_osoba, jmeno, prijmeni, narozeni, zkratka, nazev_organu_cz,
   od, max(do) as do,
   'Senátní obvod č. ' || obvod as obvod, strana,
   lag(wikidata_id) over(partition by obvod order by od asc) preceded_by,
   lead(wikidata_id) over(partition by obvod order by od asc) succeeded_by
from v_poslanci_organy org
inner join poslanci_osoba_extra ex on ex.id_osoba = org.id_osoba
inner join v_ids on v_ids.psp_id = org.id_osoba
where nazev_organu_cz = 'Senát' -- and obvod = 5
group by org.id_osoba, od
order by od desc
limit 1000;
