# Politici na wikidatech

Stává se mi často, že potřebuji zjistit nějaké reálie ohledně české politiky. Kdo byl kdy předsedou čeho, jak starý byl kdo při zvolení, kolik jsme měli ministrů něčeho atd. Data k těmto skutkům jsou relativně volně dostupná, většinou ale jen jako psaný text, často na Wikipedii.

Existuje však sesterský projekt Wikipedie s názvem [Wikidata](https://wikidata.org/), který má za cíl zhmotnit wikipedické informace jako strukturovaná data - jako opravdový dataset, kde víme, že Nicholas Cage je herec, člověk, muž, že se narodil tehdy a tehdy a hrál v těchto konkrétních filmech. Když pak zadál do vyhledávače Wikidat, že chci všechny herce 50+, kteří se narodili v Kalifornii, dostanu všechny relevantní herce včetně Nicholase Cage.

Podobnou ambici mám i pro prostor české politiky. Chci mít strukturovaná data o tom, kdo byl kdy poslancem, případně kdo koho nahradil v průběhu volebního období. Kdo byl kdy senátorem za jaký obvod, kdo kdy vedl sněmovnu nebo senát. Umřel někdo někdy ve vysoké ústavní funkci? Atd. atd.

Cílem tohoto repa je tedy následující:

- Sbírat skripty, které pomohou s přípravou dat pro nahrání do Wikidat
  - V tuto chvíli mám kód pro stahování dat z Poslanecké sněmovny (obsahuje i data za Senát a spoustu dalšího) a z Wikidat, to vše uloží to SQLite databáze pro maximální přenositelnost. Jediná závislost tu je Python 3 (bez externích balíčků).
- Napsat testy takovým způsobem, že budeme moci stáhnout data z externího zdroje a porovnat je s Wikidaty a poukázat na nesrovnalosti.
  - Cíl je takový, že jednorázově dohrajeme historická data a pak dílčí změny už budou probíhat ručně, jak se budou dít.
- Poukazovat na nesrovnalosti či chybějící data, které budeme muset doplnit ručně, protože k nim nejsou dobré zdroje (např. [místo]předsednictva stran nebo členství stran).
- Poukazovat na nejasnosti ohledně datových modelů Wikidat - jak správně zapsat určitou funkci? Jak zlepšit kvalitu nějakých dat, aby byla podle pravidel? To se pak konzultuje s Wikipedisty na jiných platformách.
- Blíže skloubit Wikidata s Wikipedií, aby data vyplněná na Wikidatech byla automaticky propsaná v textu Wikipedie, abychom krom systematické databáze měli i bližší propojení s populární databází, a tím pádem méně nutných úprav na obou stranách.

Všechny dosud známé problémy sledujeme v [issues](https://github.com/kokes/wikidata-politici/issues), jistě se jich ještě spousta objeví.

Přispívat do Wikidat systematicky a správně není jednoduché, oceníme ale i dílčí úpravy, metodologické rady či poukázání na chyby. Zde je pár odkazů na nástroje, které používáme:

- [Every politician](https://www.wikidata.org/wiki/Wikidata:WikiProject_every_politician) - WikiProjekt, který trackuje průběh vyplnění politických dat na Wikidatech
- [Open Refine](https://www.wikidata.org/wiki/Wikidata:Tools/OpenRefine) - nástroj pro velmi rychlé čištění dat, kde se dají i snadno propojit údaje se záznamy z Wikidat
- [QuickStatements](https://tools.wmflabs.org/quickstatements/) - rychlé úpravy wikidat, většinou na úrovni přidat/odebrat statement, hůř se zde pracuje s různými detaily, člověk trochu musí vědět, co dělá
- [TABernacle](https://tools.wmflabs.org/tabernacle/) - tabulární prohlížečka a editor wikidat
