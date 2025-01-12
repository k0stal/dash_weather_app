Projekt se skládá ze dvou částí.  

První je jupyter notebook, který obsahuje zpracování dat meteorologických stanic. Dále se zabývá tvorbu modelů, na základě GFS dat a dat naměřených na meteorologických stanicích. Všechny modely jsou nakonec porovnány navzájem i s referenčním GFS modelem. Na konci obsahuje přípravu sample dat pro demonstraci vizualizační aplikace.

Druhou částí je webová aplikace v Dashi. Aplikaci předáme csv soubor pozic meteorologickcý stanice ve formátu **('lon', 'lat')** a troj rozměrnou np matici ve formátu **(čas, stanice, valičina)**. Oba dva soubory jsou uloženy ve složece */app/model/data*. Aplikace nám data zobrazí pomocí grafu kontur a grafů jednotlivých veličn v závislosti an čase. Pro extrapolaci informačí dat jsou k dispozici tři modely: kNN regresor, Suppor Vector regressor a GradientBoostingRegressor. Můžeme si zvolit zobrazit data libovolné veličiny, pro konkrétní stanici i čas. Architektura aplikace odpovídá MVC. 

Webová aplikace se z CLI spouští příkazem `python3 app.py`, což spustí lokální server, na který se můžeme připojit v prohlížeči. Testování lze spustiv příkazem `pytest`. Aplikaci lze konfigurovat v souboru **config.yaml**. Musíme zde uvést, které veličny datová matice obsahuje, časový korok předpovědi a její rozsah. V neposlední řadě můžeme zvolit barvy a barevné schémata grafů a parametry extrapolačních modelů.

Soubor **requirements.txt** obsahuje nutné moduly pouze pro spuštění webové aplikace.