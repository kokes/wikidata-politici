DROP VIEW IF EXISTS v_ids;
CREATE VIEW v_ids AS
SELECT
	distinct
	substr(item, instr(item, '/Q') + 1) AS wikidata_id,
	Czech_parliament_ID AS psp_id
FROM
	wikidata_prehled
