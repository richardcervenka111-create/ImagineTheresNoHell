import json,glob,re,sys
media={}; variants={}; titles={}
for f in sorted(glob.glob('raw/tm*.json')):
    for p in json.load(open(f))['data']['products']['nodes']:
        media[p['handle']]=p['media']['nodes']; titles[p['handle']]=p['title']
for f in sorted(glob.glob('raw/tv*.json')):
    for p in json.load(open(f))['data']['products']['nodes']:
        variants[p['handle']]=p
print("products media:",len(media),"variants:",len(variants))
H=["Weiss","Aschgrau","Gold","Sand","Apfelgrün","Aqua","Rot","Royalblau"]
D=["Weiss","Hellgelb","Flieder","Marineblau"]
colors=[(c,"Herrenschnitt","Herren") for c in H]+[(c,"Damenschnitt","Damen") for c in D]
EN={"Weiss":"white","Aschgrau":"ash grey","Gold":"gold","Sand":"sand","Apfelgrün":"apple green","Aqua":"aqua","Rot":"red","Royalblau":"royal blue","Hellgelb":"light yellow","Flieder":"lilac","Marineblau":"navy blue"}
ENcut={"Herrenschnitt":"men’s cut","Damenschnitt":"women’s cut"}
issues=[]
for h,ms in media.items():
    X=titles[h].split(" — T-Shirt")[0].replace(" — "," ")
    if len(ms)!=36: issues.append((h,"media count",len(ms)))
    # derive EN name from first EN alt
    en0=ms[0]['translations'][0]['value'] if ms[0].get('translations') else ''
    m=re.search(r'“(.+?)”',en0); XE=m.group(1) if m else None
    i=0
    for (c,cut,cutv) in colors:
        exp=[f"T-Shirt aus Bio-Baumwolle mit Linolschnitt «{X}» – {c}, {cut}",
             f"Kragen mit Nackenetikett in Shirtfarbe – T-Shirt «{X}», {c}, {cut}",
             f"Model trägt T-Shirt «{X}», {c}, {cut} – Vorderansicht"]
        expEN=[f"Organic cotton T-shirt with the linocut “{XE}” – {EN[c]}, {ENcut[cut]}",
               f"Collar with neck label in the shirt colour – T-shirt “{XE}”, {EN[c]}, {ENcut[cut]}",
               f"Model wearing T-shirt “{XE}”, {EN[c]}, {ENcut[cut]} – front view"]
        for k in range(3):
            if i>=len(ms): break
            n=ms[i]
            if n['alt']!=exp[k]: issues.append((h,i+1,"DE alt",n['alt'],"expected",exp[k]))
            tr=n.get('translations') or []
            if not tr: issues.append((h,i+1,"EN missing"))
            else:
                if tr[0]['outdated']: issues.append((h,i+1,"EN outdated"))
                if tr[0]['value']!=expEN[k]: issues.append((h,i+1,"EN alt",tr[0]['value'],"expected",expEN[k]))
            i+=1
    # variants
    p=variants.get(h)
    if not p: issues.append((h,"no variant data")); continue
    vs=p['variants']['nodes']
    if len(vs)!=60: issues.append((h,"variant count",len(vs)))
    front={}
    for idx,n in enumerate(ms):
        if idx%3==0: front[(colors[idx//3][2],colors[idx//3][0])]=n['id']
    order=[v['title'].split(' / ')[0] for v in vs]
    if order!=['Herren']*40+['Damen']*20: issues.append((h,"variant order",order[0],order[-1],"HerrenFirstIdx",order.index('Herren') if 'Herren' in order else None))
    opts=[(o['name'],o['values']) for o in p['options']]
    if opts!=[('Schnitt',['Herren','Damen']),('Farbe',H+['Hellgelb','Flieder','Marineblau']),('Grösse',['S','M','L','XL','XXL','XS'])]: issues.append((h,"options",opts))
    for v in vs:
        cut,c,sz=v['title'].split(' / ')
        mid=[m['id'] for m in v['media']['nodes']]
        if not mid: issues.append((h,"variant no image",v['title']))
        elif mid[0]!=front.get((cut,c)): issues.append((h,"variant wrong image",v['title'],mid[0],front.get((cut,c))))
for x in issues: print(x)
print("issues:",len(issues))
