import json, urllib.request, urllib.parse, time, sys
raw=[x for x in json.load(open('raw2.json')) if (x[1] or 0)>=1e6]
raw.sort(key=lambda x:-x[1])
base=[0,1,3,10,12,13,15,19,24,29,31,35,36,43,44,50,51,52,55,58,61,62,71,74,80,81,82,88,97,100,102,105,107,111,112,113,116,118,119,120,125,128,129,132,137,140,148,151,152,157,159,161,162,167,169,171,172,174,178,184,188,189,190,193,194,196,198,199,203,208,213,215,224,226]
extra=[73,99,109,130,163,204,211,227,228,23,230,235,239,240,255,257,262,268,275,284,288,306,320,243,253,289]
sel=list(dict.fromkeys(base+extra))
sel=sorted(sel,key=lambda i:-raw[i][1])
print(len(sel),file=sys.stderr)
sel=sel[:100]
rows=[]
for i in sel:
    x=raw[i]
    ch=None
    try:
        u="https://www.youtube.com/oembed?format=json&url="+urllib.parse.quote("https://www.youtube.com/shorts/"+x[0])
        with urllib.request.urlopen(u,timeout=20) as r: d=json.load(r)
        ch=d.get('author_name')
    except Exception as e: ch=None
    rows.append(dict(rank=0,id=x[0],views=x[1],title=x[3],channel=ch,source_hashtag=x[5],url="https://www.youtube.com/shorts/"+x[0]))
    time.sleep(0.4)
json.dump(rows,open('curated.json','w'),ensure_ascii=False,indent=1)
print(len(rows), sum(1 for r in rows if r['channel']))
