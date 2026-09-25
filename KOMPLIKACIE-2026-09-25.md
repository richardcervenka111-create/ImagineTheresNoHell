# Komplikácie a riešenia – 25. 9. 2026 (kontrola fotiek, alt textov a variant v Shopify)

Pokračovanie denníka KOMPLIKACIE-2026-09-11.md z Macu (posledné číslo #936). Časy sú UTC (Bern = UTC+2).
Označenie: ZMERANÉ = overené príkazom/dotazom, POSÚDENÉ = môj úsudok bez merania.

## #937 – Živý obchod shop.rcprints.ch sa z cloudu nedá otvoriť (11:03 UTC)
- Čo: WebFetch aj curl na shop.rcprints.ch a cdn.shopify.com vracajú „blocked by the network egress proxy“ (HTTP 403 z proxy). Sieťová politika prostredia Claude Code doménu nepovoľuje.
- Riešenie: vizuálnu kontrolu nahradila kontrola cez Admin API (produkt má `onlineStoreUrl`, stav ACTIVE, fotky READY, alt DE aj EN). Skutočné zobrazenie na webe treba overiť z telefónu alebo Macu – **čaká na Mac / telefón**.
- ZMERANÉ 11:07 UTC (dotaz `products(query:"handle:...")`): Wellen, Die Kuppeln, Grammophone, Garnele (tričká) aj plátno Katze sú ACTIVE, majú `onlineStoreUrl` na shop.rcprints.ch a titulnú fotku s novým alt textom – teda v obchode sú zverejnené s novými fotkami.
- Ak má kontrola z cloudu fungovať nabudúce: v nastaveniach prostredia (Network access) pridať shop.rcprints.ch a cdn.shopify.com medzi povolené domény.

## #938 – Poradie variant: postihnuté 4 tričká, nie 3 (11:01 UTC)
- Čo: ZMERANÉ (dotaz `products(query:"product_type:T-Shirt AND status:active")` + skript `skripty/2026-09-25/kontrola-tricka.py`): dámske varianty pred pánskymi mali Die Leiter, Über Bern, Espressokanne **a navyše Die Kuppeln** (tshirt-f-rooftops). Zároveň mali iné poradie hodnôt možností (Schnitt: Damen, Herren; Farbe: dámske farby prvé; Grösse: XS prvé).
- Riešenie (11:04–11:06 UTC): `productOptionsReorder` (poradie hodnôt Schnitt/Farbe/Grösse podľa Katze) a potom `productVariantsBulkReorder` (presné pozície 1–60 podľa Katze) pre všetky 4 produkty. Nič sa nemazalo, ID variant ostali.
- Overenie: ZMERANÉ opakovaným dotazom 11:06 UTC – všetkých 28 tričiek má teraz rovnaké poradie ako Katze, skript hlási 0 chýb.

## #939 – Katze ako vzor má nezvyčajné poradie veľkostí (POSÚDENÉ, 11:04 UTC)
- Čo: pri Katze (a 24 ďalších tričkách) je poradie hodnôt Grösse „S, M, L, XL, XXL, XS“ (XS na konci), ale dámske varianty idú „XS, S, M, L, XL“. Nie je to chyba zobrazenia, len nekonzistentné poradie hodnoty XS v selektore veľkosti.
- Riešenie: nechal som podľa zadania „zjednoť podľa Katze“ – všetkých 28 tričiek je teraz rovnakých. Ak chceš XS na začiatku, je to jeden `productOptionsReorder` na každé tričko (28 volaní) – **nerobil som, čaká na rozhodnutie**.

## #940 – Plátien 20 × 20 je 20, nie 16 (ZMERANÉ, 11:01 UTC)
- Čo: aktívnych produktov typu „Leinwand“ je 20 (14 motívov + 6 Schneekugel). V zadaní bolo 16.
- Riešenie: skontroloval som všetkých 20 – každé má 2 fotky, prvá „Vorderansicht“, druhá „Seitenansicht“, alt DE aj EN, EN nie je zastaraný. Bez zásahu.

## #941 – Veľké odpovede API sa nezmestia do výstupu nástroja (11:00 UTC)
- Čo: dotazy na schému (`Mutation`, `QueryRoot`) a na 7–10 produktov s 36 fotkami majú 60–370 kB, nástroj ich ukladá do súboru.
- Riešenie: uložené JSON som spracoval skriptom (jq/python), nie ručne. Skript a zoznamy ID sú v `skripty/2026-09-25/`.

## Súhrn kontroly (ZMERANÉ, 11:00–11:07 UTC)
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
- Vizuálna kontrola živého obchodu (Wellen, Die Kuppeln, Grammophone, Garnele, plátno Katze) v prehliadači – z cloudu zablokované (#937).
- Pripojenie tohto denníka k KOMPLIKACIE-2026-09-11.md.
