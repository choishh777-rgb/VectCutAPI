import json, urllib.request, urllib.parse, time
a=json.load(open('kr_cand.json')); b=json.load(open('kr_cand2.json'))
pa=[1,2,5,10,13,16,19,20,21,22,23,25,26,30,32,33,34,35,37,38,42,43,44,45,49,52,54,62,63,64,65,67,68,69,74,75,76,77,78,80,83,84,86,87,88,89,91,94,95,97,98,99,101,104,105,106,107,109,110,111,114,115,116,117,119,120,121,123,125,126,129,130,131,132]
pb=[8,15,22,26,31,37,43,51,52,55,63,67,70]
sel=[a[i] for i in pa]+[b[i] for i in pb]
sel=list({x[0]:x for x in sel}.values())
sel.sort(key=lambda x:-x[1])
rows=[]
for x in sel:
    ch=None
    try:
        u="https://www.youtube.com/oembed?format=json&url="+urllib.parse.quote("https://www.youtube.com/shorts/"+x[0])
        with urllib.request.urlopen(u,timeout=20) as r: ch=json.load(r).get('author_name')
    except Exception: pass
    rows.append(dict(id=x[0],views=x[1],title=x[3],channel=ch,source_hashtag=x[5],url="https://www.youtube.com/shorts/"+x[0]))
    time.sleep(0.4)
json.dump(rows,open('curated_kr.json','w'),ensure_ascii=False,indent=1)
print(len(rows),sum(1 for r in rows if r['channel']))
for i,r in enumerate(rows,1): print(i,round(r['views']/1e6,1),r['channel'],'|',r['title'][:55].replace('\n',' '))
