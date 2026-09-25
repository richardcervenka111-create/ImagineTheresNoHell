# Prompt pre lokálny chat na Macu – RC prints, 25. 9. 2026

Ahoj. Pracuj hneď, bez otázok a bez prestávok, okrem miest, kde nižšie výslovne píšem „SPÝTAJ SA“. Píš po slovensky, stručne, čitateľne na telefóne, bez žargónu. Čo zmeriaš, označ ZMERANÉ (s príkazom a časom v bernskom čase), čo posúdiš, POSÚDENÉ. Nič si nevymýšľaj – chýbajúci údaj je lepší než nesprávny.

## Kontext (čo je hotové z cloudu, dnes 25. 9. 2026)
- Obchod: RC prints, https://shop.rcprints.ch (Shopify, plán Basic, CHF, trh len Švajčiarsko, jazyky de + en, téma „rcprints-theme-v90“ na báze Dawn).
- Repozitár GitHub: richardcervenka111-create/ImagineTheresNoHell, vetva `claude/shopify-photos-alt-text-kx79n8` (jediná vetva, PR neexistuje). Najprv: `git fetch origin && git checkout claude/shopify-photos-alt-text-kx79n8 && git pull`.
- V repozitári nájdeš:
  - `KOMPLIKACIE-2026-09-25.md` – denník z cloudu, záznamy #937 až #942 (pokračovanie denníka na Macu, ktorý končí #936). Časy sú v bernskom čase.
  - `audit/audit-shopify-web-rcprints-2026-09-25.html` – kompletný audit obchodu (26 nálezov F01–F26, skóre 65/100, top 10, plán 30/60/90). Web rcprints.ch v ňom NIE JE auditovaný, lebo cloud ho nemohol otvoriť.
  - `audit/shots/*.png` + `audit/shots/metrics.jsonl` – snímky a metriky (Playwright), `audit/analyze.py`, `audit/shot.js`.
  - `skripty/2026-09-25/` – kontrola tričiek (`kontrola-tricka.py`), zoznamy ID, `over-zivy-obchod.sh` (kontrola živého obchodu s pauzami proti HTTP 429).
- Hotové a overené v Shopify (ZMERANÉ v cloude): 28 tričiek × 36 fotiek, alt DE + EN, obrázky variant, poradie variant zjednotené podľa „Katze — T-Shirt“ (opravené Die Leiter, Über Bern, Espressokanne, Die Kuppeln); 20 plátien 20 × 20 × 2 fotky s alt DE + EN. Nič nebolo zmazané.
- Pravidlá bez výnimky: nič nemazať (fotky len odpájať cez fileUpdate referencesToRemove), nepísať do živej témy Shopify kódom (Theme editor a nastavenia sú OK), nepýtať heslá, neposielať e-maily ani formuláre, nič nezverejňovať v Gelate. Shopify GraphQL: najprv schéma, potom validácia, až potom vykonanie.
- Denník: každú chybu a jej riešenie zapíš hneď. Pokračuj od **#943** v súbore `KOMPLIKACIE-2026-09-25.md` (po pripojení podľa bloku A ďalej píš do zlúčeného denníka na Macu).

## Blok A – veci, ktoré ide urobiť len na Macu (urob ako prvé)
1. Nájdi denník `KOMPLIKACIE-2026-09-11.md` na Macu (`mdfind -name KOMPLIKACIE-2026-09-11.md` alebo `find ~ -name "KOMPLIKACIE-2026-09-11.md" 2>/dev/null`). Over, že posledný záznam je #936. Pripoj obsah `KOMPLIKACIE-2026-09-25.md` z repozitára na jeho koniec (bez duplicitnej hlavičky), zachovaj čísla #937–#942. Do repozitára ulož kópiu zlúčeného denníka. ZMERANÉ: `grep -c "^## #" <súbor>` pred a po.
2. Spusti skript `05_Fotky-eshop-2026-09-14/stiahni-fotky-2026-09-24.command` (nájdi ho rovnako cez `mdfind`/`find`). Pred spustením si ho prečítaj a povedz jednou vetou, čo robí a kam ukladá. Po dobehnutí over počty: 1008 fotiek tričiek + 40 fotiek plátien = 1048 (`find <cieľ> -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.webp" \) | wc -l`). Rozdiel zapíš do denníka aj s príčinou (napr. HTTP 429 – v takom prípade pridaj pauzu a spusti znova len pre chýbajúce).
3. Otvor v Chrome (alebo cez Claude v Chrome, ak je k dispozícii) tieto stránky a vizuálne over, že sa zobrazujú nové fotky, alt texty (Inspect → img alt) a poradie variant Herren → Damen:
   - https://shop.rcprints.ch/products/tshirt-waves
   - https://shop.rcprints.ch/products/tshirt-f-rooftops
   - https://shop.rcprints.ch/products/tshirt-f-gramo
   - https://shop.rcprints.ch/products/tshirt-shrimp
   - https://shop.rcprints.ch/products/katze-leinwanddruck-20-20-cm
   - https://shop.rcprints.ch/en/products/tshirt-waves
   Zapíš, čo si videl (POSÚDENÉ) a urob snímky obrazovky do `audit/shots/mac/`.

## Blok B – doaudit marketingového webu rcprints.ch (z Macu nie je blokovaný)
1. Prejdi https://www.rcprints.ch rovnakým postupom ako obchod: robots.txt, sitemap.xml, všetky stránky v menu a pätičke, 404, formuláre, odkazy do obchodu (hľadaj `shop.rcprints.ch` a UTM parametre), jazyky, cookie lišta, rýchlosť (Playwright: LCP, CLS, počet požiadaviek, prenos na mobile 390 px a desktope 1440 px – použi `audit/shot.js`, spusti `npx playwright install chromium`, ak treba).
2. Over, čím je web postavený (hlavička `server`, generátor v HTML, zmienka o Lovable) a či dizajn (logo, písmo Lora/Assistant, bordová farba) sedí s obchodom.
3. Vyplň v `audit/audit-shopify-web-rcprints-2026-09-25.html`:
   - sekciu 6 „Marketingový web“ (nahraď text „neauditované“ reálnymi nálezmi, oblasti A–X ako pri obchode, skrátene),
   - skóre webu v hlavičke (rovnaké váhy: jasnosť 15, dôvera 15, nájditeľnosť 15, obsah 15, mobil 10, rýchlosť 10, kontakt/konverzia 10, právne 5, súlad 5),
   - kombinované skóre,
   - nové nálezy ako karty F27+ do sekcie 8 a do matice priorít, ak patria do „TERAZ“,
   - prílohu dôkazov (tabuľka stránok webu).
   Nemeň existujúce nálezy F01–F26, ak ich nové fakty nevyvracajú; ak áno, oprav ich a zapíš do denníka.
4. Ulož ako novú verziu súboru (verzia 2 v hlavičke), commitni a pushni.

## Blok C – opravy v Shopify podľa auditu (Top 10), len bezpečné bez rozhodnutia
Urob rovno (sú vratné, nič sa nemaže):
- F09: Online Store → Navigation → Main menu: „Alle Werke“ → /collections/alle-werke, „Kleinformate“ → /collections/kleinformate. Vytvor kolekcie „Originale A3/A4“ (podmienka tag = original) a „Postkarten“ (tag = karten) so SEO titulkom a popisom a prelinkuj „A3/A4-Formate“ a „Postkarten“ na ne. Ak menu ide meniť cez Admin API (`menuUpdate`), použi schéma → validácia → vykonanie.
- F10: kolekcie „Werkstatt“, „Home page“ (frontpage) a „Postkarten-Motive“ vypnúť z kanála Online Store (nie mazať). Pred vypnutím „Postkarten-Motive“ over na https://shop.rcprints.ch/products/postkarten-nach-wahl, či výber motívov funguje aj potom; ak nie, vráť späť a zapíš.
- F21: Theme editor → Footer: odstrániť „Powered by Shopify“ (Theme content → Footer → „Powered by“ → prázdny reťazec), ponechať jeden jazykový prepínač.
- F16: Theme editor → 404 template: pridať vyhľadávacie pole a 4 kolekcie (Alle Werke, Kleinformate, Leinwände & Drucke, Geschenke aus Bern). Do Navigation → URL redirects pridať presmerovania starých archivovaných handles typu `/products/print-cat` → `/products/original-cat` (zoznam archivovaných produktov si vytiahni cez Admin API `products(query:"status:archived")`, mapuj podľa motívu; kde mapovanie nie je jednoznačné, presmeruj na /collections/alle-werke).
- F03: Theme editor → sekcia Pop-up („rc_popup“): ak má nastavenia, nastav oneskorenie 25 s, len domov a kolekcie, nie košík/produkt/404. Ak nastavenia nemá, NEMEŇ kód témy; zapíš, že to vyžaduje vývojára, a priprav presný návrh zmeny (JS: WAIT 6000 → 25000, podmienka na `template.name`).
- F11: Theme editor → Cart drawer: ak existuje nastavenie „free shipping bar/threshold“, nastav 75 CHF. Na PDP pridať blok textu pod cenu: „Versand CHF 12 · ab CHF 75 gratis · nur Postkarten CHF 5“ (a EN preklad cez Translate & Adapt).

SPÝTAJ SA pred vykonaním (jedna správa s tromi otázkami, potom čakaj):
- F01: Zverejniť produkt „Geschenkkarte gedruckt (per Post)“ (dnes Draft), alebo odstrániť voľbu „Gedruckte Karte per Post“ zo stránky poukazu?
- F02: Je TWINT zapnutý v Settings → Payments → Shopify Payments? (Ty to musíš pozrieť, ja tam prístup nemám.) Ak nie a nechceš ho zapnúť, mám vymazať „TWINT“ z hero textu a meta description?
- F04: Pri košíku len s pohľadnicami sa ponúkajú dve sadzby (CHF 5 a CHF 12). Riešiť podmienkou hmotnosti na „Versand Schweiz“, alebo pohľadnice do vlastného profilu dopravy? Po zmene otestuj tri košíky cez `/cart/shipping_rates.json` (postup je v denníku #942 a v audite).

Po každej zmene v Shopify: over výsledok dotazom (ZMERANÉ), zapíš do denníka číslo, čas, príkaz a výsledok.

## Blok D – na konci
Napíš mi: čo si zmeral, čo si opravil, čo ostáva, a chyby s časom (čísla záznamov). Commitni a pushni všetko na vetvu `claude/shopify-photos-alt-text-kx79n8` (commit správy po slovensky, jedna vec na commit). Ak vetva medzitým dostala nové commity, najprv `git pull --rebase`.
