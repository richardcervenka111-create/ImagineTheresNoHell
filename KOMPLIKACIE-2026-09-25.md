# Komplikácie a riešenia – 25. 9. 2026 (kontrola fotiek, alt textov a variant v Shopify)

Pokračovanie denníka KOMPLIKACIE-2026-09-11.md z Macu (posledné číslo #936). Časy sú v bernskom čase (CEST, UTC+2).
Označenie: ZMERANÉ = overené príkazom/dotazom, POSÚDENÉ = môj úsudok bez merania.

## #937 – Živý obchod shop.rcprints.ch sa z cloudu nedá otvoriť (13:03)
- Čo: WebFetch aj curl na shop.rcprints.ch a cdn.shopify.com vracajú „blocked by the network egress proxy“ (HTTP 403 z proxy). Sieťová politika prostredia Claude Code doménu nepovoľuje.
- Riešenie: vizuálnu kontrolu nahradila kontrola cez Admin API (produkt má `onlineStoreUrl`, stav ACTIVE, fotky READY, alt DE aj EN). Skutočné zobrazenie na webe treba overiť z telefónu alebo Macu – **čaká na Mac / telefón**.
- ZMERANÉ 13:07 (dotaz `products(query:"handle:...")`): Wellen, Die Kuppeln, Grammophone, Garnele (tričká) aj plátno Katze sú ACTIVE, majú `onlineStoreUrl` na shop.rcprints.ch a titulnú fotku s novým alt textom – teda v obchode sú zverejnené s novými fotkami.
- Dodatok 13:13–13:15: pri druhom pokuse (`curl -sS https://shop.rcprints.ch/products/...`) obchod odpovedal HTTP 200 (WebFetch ostal blokovaný). ZMERANÉ zo stiahnutého HTML: Wellen, Die Kuppeln, Grammophone, Garnele majú v galérii 36 fotiek s novými DE alt textami (prvá „T-Shirt aus Bio-Baumwolle … Weiss, Herrenschnitt“), selektor zobrazuje Herren, Damen; Weiss … Marineblau; S, M, L, XL, XXL, XS. Plátno Katze: 2 fotky, Vorderansicht prvá, Seitenansicht druhá. Anglická stránka /en/products/tshirt-waves má EN alt texty („Organic cotton T-shirt with the linocut “Waves” – white, men’s cut“) a EN hodnoty možností (Men, Women, White …).
- Pozor: Shopify pri rýchlych požiadavkách vracia HTTP 429 (limit požiadaviek); pomohla pauza 8–20 s medzi stránkami.
- Oprava 13:36–13:38: skript `skripty/2026-09-25/over-zivy-obchod.sh` sťahuje stránky s pauzou 6 s a pri HTTP 429 počká 20 s a skúsi znova (max 4×). ZMERANÉ behom skriptu: 6 stránok, všetky HTTP 200 bez jediného 429; tričká 36 fotiek (+1 obrázok súvisiaceho produktu = 37 unikátnych alt), plátno Katze 2 fotky (+1), možnosti v poradí Herren, Damen; Weiss … Marineblau; S, M, L, XL, XXL, XS; EN stránka Men, Women, White … Navy.
- Ak má kontrola z cloudu fungovať nabudúce: v nastaveniach prostredia (Network access) pridať shop.rcprints.ch a cdn.shopify.com medzi povolené domény.

## #938 – Poradie variant: postihnuté 4 tričká, nie 3 (13:01)
- Čo: ZMERANÉ (dotaz `products(query:"product_type:T-Shirt AND status:active")` + skript `skripty/2026-09-25/kontrola-tricka.py`): dámske varianty pred pánskymi mali Die Leiter, Über Bern, Espressokanne **a navyše Die Kuppeln** (tshirt-f-rooftops). Zároveň mali iné poradie hodnôt možností (Schnitt: Damen, Herren; Farbe: dámske farby prvé; Grösse: XS prvé).
- Riešenie (13:04–13:06): `productOptionsReorder` (poradie hodnôt Schnitt/Farbe/Grösse podľa Katze) a potom `productVariantsBulkReorder` (presné pozície 1–60 podľa Katze) pre všetky 4 produkty. Nič sa nemazalo, ID variant ostali.
- Overenie: ZMERANÉ opakovaným dotazom 13:06 – všetkých 28 tričiek má teraz rovnaké poradie ako Katze, skript hlási 0 chýb.

## #939 – Katze ako vzor má nezvyčajné poradie veľkostí (POSÚDENÉ, 13:04)
- Čo: pri Katze (a 24 ďalších tričkách) je poradie hodnôt Grösse „S, M, L, XL, XXL, XS“ (XS na konci), ale dámske varianty idú „XS, S, M, L, XL“. Nie je to chyba zobrazenia, len nekonzistentné poradie hodnoty XS v selektore veľkosti.
- Riešenie: nechal som podľa zadania „zjednoť podľa Katze“ – všetkých 28 tričiek je teraz rovnakých. Ak chceš XS na začiatku, je to jeden `productOptionsReorder` na každé tričko (28 volaní) – **nerobil som, čaká na rozhodnutie**.

## #940 – Plátien 20 × 20 je 20, nie 16 (ZMERANÉ, 13:01)
- Čo: aktívnych produktov typu „Leinwand“ je 20 (14 motívov + 6 Schneekugel). V zadaní bolo 16.
- Riešenie: skontroloval som všetkých 20 – každé má 2 fotky, prvá „Vorderansicht“, druhá „Seitenansicht“, alt DE aj EN, EN nie je zastaraný. Bez zásahu.

## #941 – Veľké odpovede API sa nezmestia do výstupu nástroja (13:00)
- Čo: dotazy na schému (`Mutation`, `QueryRoot`) a na 7–10 produktov s 36 fotkami majú 60–370 kB, nástroj ich ukladá do súboru.
- Riešenie: uložené JSON som spracoval skriptom (jq/python), nie ručne. Skript a zoznamy ID sú v `skripty/2026-09-25/`.

## Súhrn kontroly (ZMERANÉ, 13:00–13:07)
| Čo | Výsledok |
|---|---|
| Tričká (28 aktívnych, typ T-Shirt) | každé 36 fotiek, poradie 12 farieb × (predná, golier, model) presne podľa Katze |
| Alt DE na tričkách | 1008 fotiek, všetky podľa vzoru, žiadna prázdna |
| Alt EN (translations, locale en) | 1008 registrovaných, 0 zastaraných (`outdated: false`) |
| Obrázky variant | 1680 variant (28 × 60), každá má prednú fotku svojej farby a strihu |
| Poradie variant | po oprave 28/28 zhodných s Katze |
| Plátna 20 × 20 (20 aktívnych) | 2 fotky, spredu prvá, alt DE + EN, 0 zastaraných |
| Ostatné aktívne produkty (tašky, fľaše, becher, postery, originály, reprodukcie, hoodie, gutschein) | každá fotka má alt DE + EN, 0 zastaraných |
| Jazyky obchodu | de (primárny, publikovaný), en (publikovaný) |

## Čaká na Mac (nerobené)
- Stiahnutie 1048 fotiek skriptom `05_Fotky-eshop-2026-09-14/stiahni-fotky-2026-09-24.command` a overenie počtov (1008 + 40).
- Kontrola živého obchodu v skutočnom prehliadači (rozloženie, načítanie obrázkov) – HTML a alt texty som overil z cloudu o 13:15 (#937), vizuálne vykreslenie nie.
- Pripojenie tohto denníka k KOMPLIKACIE-2026-09-11.md.

## #942 – Audit obchodu a webu: marketingový web rcprints.ch nedostupný (15:40–16:20)
- Čo: pri audite (zadanie „principal digital commerce auditor“) proxy prostredia blokovala rcprints.ch a www.rcprints.ch (403 CONNECT). DNS domény ukazuje na Cloudflare, web teda existuje. Shopify obchod bol dostupný cez curl a Chromium (Playwright), Google Fonts blokované.
- Riešenie: obchod auditovaný kompletne (60 stránok HTML, 26 vykreslení mobil/desktop, 187 produktov cez Admin API, 4 skúšobné košíky). Web označený ako „neauditované“, skóre webu nevyplnené. Report: `audit/audit-shopify-web-rcprints-2026-09-25.html`, snímky v `audit/shots/`.
- Čaká: povoliť domény rcprints.ch, www.rcprints.ch, fonts.googleapis.com v Network access prostredia a spustiť doaudit webu (cca 45 min).
- Kritické nálezy zapísané v reporte: F01 poukaz „Gedruckte Karte“ → 404 (produkt v Draft), F02 TWINT sľúbený, v ikonách chýba, F04 dve sadzby dopravy pri pohľadniciach (ZMERANÉ cez /cart/shipping_rates.json).
