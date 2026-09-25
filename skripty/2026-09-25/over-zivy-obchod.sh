#!/usr/bin/env bash
# Overí produktové stránky na shop.rcprints.ch: stiahne HTML s pauzou medzi požiadavkami,
# pri HTTP 429 (limit požiadaviek Shopify) počká a skúsi znova. Vypíše počet alt textov
# a poradie hodnôt možností. Použitie: ./over-zivy-obchod.sh [handle ...]
set -u
PAUSE=${PAUSE:-6}        # sekundy medzi požiadavkami
RETRY_WAIT=${RETRY_WAIT:-20}
OUT=${OUT:-./live}
mkdir -p "$OUT"
HANDLES=("$@")
[ ${#HANDLES[@]} -eq 0 ] && HANDLES=(tshirt-waves tshirt-f-rooftops tshirt-f-gramo tshirt-shrimp katze-leinwanddruck-20-20-cm en/tshirt-waves)
for h in "${HANDLES[@]}"; do
  case "$h" in en/*) url="https://shop.rcprints.ch/en/products/${h#en/}"; f="$OUT/en-${h#en/}.html";; *) url="https://shop.rcprints.ch/products/$h"; f="$OUT/$h.html";; esac
  for try in 1 2 3 4; do
    code=$(curl -sS -L --max-time 30 -A "Mozilla/5.0 (kontrola RC prints)" -o "$f" -w "%{http_code}" "$url")
    if [ "$code" = "429" ]; then echo "$(date -u +%H:%M:%S) $h HTTP 429, čakám ${RETRY_WAIT}s (pokus $try)"; sleep "$RETRY_WAIT"; continue; fi
    break
  done
  read -r n opts < <(python3 - "$f" <<'PY'
import re,html,sys
s=open(sys.argv[1],encoding='utf-8',errors='replace').read()
alts=[html.unescape(a) for a in re.findall(r'<img[^>]+alt="([^"]*)"',s)]
keys=['Linolschnitt','Nackenetikett','Model trägt','linocut','neck label','Model wearing']
u=list(dict.fromkeys(a for a in alts if any(k in a for k in keys)))
vals=[html.unescape(v) for v in re.findall(r'<input[^>]*type="radio"[^>]*value="([^"]+)"',s)]
print(len(u), ",".join(vals))
PY
)
  echo "$(date -u +%H:%M:%S) $h HTTP $code | unikátnych produktových alt: $n | možnosti: $opts"
  sleep "$PAUSE"
done
