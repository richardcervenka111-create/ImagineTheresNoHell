import re,html,glob,json,sys,os
def tag(s,pat,flags=re.S|re.I): 
    m=re.search(pat,s,flags); return html.unescape(m.group(1).strip()) if m else None
files=sys.argv[1:] or sorted(glob.glob('*.html'))
for f in files:
    s=open(f,encoding='utf-8',errors='replace').read()
    if len(s)<20000: print(f"== {f}: {len(s)} B (short/blocked)"); continue
    print(f"\n== {f} ({len(s)//1024} KB)")
    print(" title:",tag(s,r'<title>(.*?)</title>'))
    print(" meta desc:",(tag(s,r'<meta name="description" content="(.*?)"') or '')[:200])
    print(" canonical:",tag(s,r'<link rel="canonical" href="(.*?)"'))
    hl=re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"',s); print(" hreflang:",hl[:6])
    print(" robots meta:",tag(s,r'<meta name="robots" content="(.*?)"'))
    h1=[re.sub('<[^>]+>','',x).strip() for x in re.findall(r'<h1[^>]*>(.*?)</h1>',s,re.S)]; print(" h1:",[html.unescape(x)[:80] for x in h1])
    h2=[html.unescape(re.sub('<[^>]+>','',x).strip())[:60] for x in re.findall(r'<h2[^>]*>(.*?)</h2>',s,re.S)]; print(" h2 (",len(h2),"):",h2[:12])
    ld=re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>',s,re.S)
    types=[]
    for x in ld:
        try:
            j=json.loads(x); j=j if isinstance(j,list) else [j]
            for o in j: types.append(o.get('@type'))
        except Exception as e: types.append('INVALID-JSON')
    print(" json-ld types:",types)
    scripts=re.findall(r'<script[^>]+src="([^"]+)"',s); doms={}
    for u in scripts:
        d=re.sub(r'^https?://','',u).split('/')[0] or 'inline-rel'; doms[d]=doms.get(d,0)+1
    print(" external scripts:",len(scripts),doms)
    inl=re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>',s,re.S); print(" inline scripts:",len(inl),"total",sum(len(x) for x in inl)//1024,"KB")
    st=re.findall(r'<style[^>]*>(.*?)</style>',s,re.S); print(" inline style blocks:",len(st),"total",sum(len(x) for x in st)//1024,"KB; stylesheets:",len(re.findall(r'<link[^>]+rel="stylesheet"',s)))
    imgs=re.findall(r'<img\b[^>]*>',s); noalt=[i for i in imgs if 'alt=' not in i]; emptyalt=[i for i in imgs if re.search(r'alt=""',i)]
    lazy=[i for i in imgs if 'loading="lazy"' in i]; eager=[i for i in imgs if 'loading="eager"' in i or 'fetchpriority="high"' in i]
    print(f" img: {len(imgs)} | no alt attr {len(noalt)} | empty alt {len(emptyalt)} | lazy {len(lazy)} | eager/high {len(eager)} | srcset {sum(1 for i in imgs if 'srcset' in i)} | width attr {sum(1 for i in imgs if 'width=' in i)}")
    fonts=re.findall(r'<link[^>]+(?:preload|preconnect)[^>]*>',s); print(" preload/preconnect:",len(fonts), [re.search(r'href="([^"]+)"',x).group(1)[:70] for x in fonts][:6])
    print(" font-face:",len(re.findall(r'@font-face',s)), "google fonts:", 'fonts.googleapis' in s, "| fonts.shopifycdn:", 'fonts.shopifycdn' in s)
    print(" viewport:",tag(s,r'<meta name="viewport" content="(.*?)"'))
    print(" og:image:",bool(re.search(r'property="og:image"',s)), "og:title:",tag(s,r'property="og:title" content="(.*?)"'))
    print(" lang:",tag(s,r'<html[^>]*lang="([^"]+)"'))
    # nav links
    nav=re.search(r'<nav[^>]*>(.*?)</nav>',s,re.S)
    if nav:
        links=re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>',nav.group(1),re.S)
        print(" nav links:",[(html.unescape(re.sub('<[^>]+>','',t)).strip()[:25],u) for u,t in links][:14])
    foot=re.search(r'<footer[^>]*>(.*?)</footer>',s,re.S)
    if foot:
        links=re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>',foot.group(1),re.S)
        print(" footer links:",[(html.unescape(re.sub('<[^>]+>','',t)).strip()[:25],u) for u,t in links][:20])
        print(" footer text sample:",html.unescape(re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',foot.group(1))))[:400])
    kw={'cookie':len(re.findall(r'cookie',s,re.I)),'consent':len(re.findall(r'consent',s,re.I)),'shopify-pay/shop pay':len(re.findall(r'shop[ -]?pay',s,re.I)),'judge.me/reviews':len(re.findall(r'judge\.me|loox|yotpo|reviews',s,re.I)),'gelato':len(re.findall(r'gelato',s,re.I)),'inbox/chat':len(re.findall(r'shopify-chat|inbox',s,re.I)),'gtag/ga4':len(re.findall(r'gtag|googletagmanager|G-[A-Z0-9]{6,}',s)),'meta pixel':len(re.findall(r'fbq\(|connect\.facebook',s)),'klaviyo':len(re.findall(r'klaviyo',s,re.I)),'sold out/ausverkauft':len(re.findall(r'ausverkauft|sold out',s,re.I)),'CHF':len(re.findall(r'CHF',s)),'versand':len(re.findall(r'versand',s,re.I)),'rückgabe':len(re.findall(r'rückgabe|retour',s,re.I)),'newsletter':len(re.findall(r'newsletter',s,re.I)),'instagram':len(re.findall(r'instagram',s,re.I)),'skip to content':len(re.findall(r'skip[- ]to|zum inhalt',s,re.I)),'aria-label':len(re.findall(r'aria-label',s)),'form':len(re.findall(r'<form',s)),'button':len(re.findall(r'<button',s)),'iframe':len(re.findall(r'<iframe',s)),'video':len(re.findall(r'<video',s)),'noindex':len(re.findall(r'noindex',s)),'web-pixels':len(re.findall(r'web-pixels|webPixelsManager',s)),'theme-check/schema':len(re.findall(r'Shopify\.theme',s))}
    print(" signals:",{k:v for k,v in kw.items() if v})
    m=re.search(r'Shopify\.theme\s*=\s*(\{.*?\});',s,re.S); print(" Shopify.theme:",m.group(1)[:200] if m else None)
    body=re.sub(r'<script.*?</script>|<style.*?</style>|<svg.*?</svg>','',s,flags=re.S); text=html.unescape(re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',body))); print(" visible text length:",len(text)); print(" text start:",text[:700])
