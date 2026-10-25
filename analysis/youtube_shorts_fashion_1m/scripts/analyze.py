import json, re, statistics as st, csv, collections, unicodedata
rows=json.load(open('curated.json'))
rows.sort(key=lambda r:-r['views'])
CELEB=r"ronaldo|cr7|neymar|georgina|yamal|alien star|alian star|aaryan|aryan kelvin|aman sharma|mc stan|tamanna|alia bhatt|aliya|madhuri|sara |sarah|shraddha|rohit|sandler|lisa|aneet|mavie|kylie|zendaya|gigi|kendall|sreeleela|georgia style|tejasswi|rocky"
def cat(t,c):
    tl=t.lower()
    if re.search(r"price|cost|₹|cuánto|prices|billionaire|luxury outfit",tl) or re.search(CELEB,tl) and re.search(r"outfit|look|style|bag|watch|chappal",tl) and not re.search(r"runway|catwalk|show",tl):
        return "셀럽·운동선수 룩 (가격 공개/분석)"
    if re.search(r"runway|catwalk|zendaya|gigi|dior|kendall|fashion ?show|audition|slay|expensive walk|caught me off guard|convenient|kylie|wedding lehenga",tl):
        return "런웨이·레드카펫·모델 워킹"
    if re.search(r"transformation|rip it|new life|cut my|कटिंग|blouse|ब्लाउज",tl) and not re.search(r"outfit transformations",tl) or "dress too big" in tl or "same dress… instant" in tl:
        return "DIY·리폼·업사이클"
    if re.search(r"hack|tuck|how to|upgrade|cuter|fix|footwear",tl):
        return "스타일링 팁·핵"
    if re.search(r"shop|order|for rent|for sale|collection|link bio|артикул|boutique|hijab|dafo|reload|available|lehenga|gowns|frock|dupatta|mini dress|top x|ruffle|dress in",tl) or c and re.search(r"clothing|boutique|saree|collection|brand|leather|store",c.lower()):
        return "상품 판매·광고"
    return "OOTD·룩북·GRWM·코디 제안"
def script(t):
    s=collections.Counter()
    for ch in t:
        if ch.isalpha():
            n=unicodedata.name(ch,"")
            s["Devanagari" if "DEVANAGARI" in n else "Hangul" if "HANGUL" in n else "Cyrillic" if "CYRILLIC" in n else "Latin" if "LATIN" in n else "Other"]+=1
    return s.most_common(1)[0][0] if s else "Latin"
IND=r"₹|india|kurta|saree|lehenga|chikankari|dupatta|bollywood|aaryan|aryan kelvin|alien star|alian star|aman sharma|mc stan|tamanna|alia|madhuri|sara |shraddha|rohit|tejasswi|aneet|sreeleela|rocky|frock|sherwani|hindi|तेंदुलकर|आणि|कुर्ता|ब्लाउज|outfit india|aaj tak|reload casual|silk saree|mirax|payal|chaudhary|choudhary|rich style hub|richstylehub|fashionflicksindia|n-volt|n explanation"
out=[]
for i,r in enumerate(rows,1):
    t=r['title'].replace("\n"," "); tl=t.lower(); c=r['channel'] or ""
    r['rank']=i; r['category']=cat(t,c)
    r['script']=script(t)
    r['price_reveal']=bool(re.search(r"price|cost|₹|cuánto|prices",tl))
    r['vs_or_question']=bool(re.search(r"\bvs\b|\?|which|this or that|who ",tl))
    r['hashtags']=len(re.findall(r"#\w+",t))
    r['emoji']=sum(1 for ch in t if unicodedata.category(ch)=="So")
    r['title_len']=len(re.sub(r"#\S+","",t).strip())
    r['hindi_india']=bool(re.search(IND,tl+" "+c.lower()) or r['script']=="Devanagari")
    r['cta']=bool(re.search(r"link|order|subscribe|follow|comment|part 2|whatsapp|shop",tl))
    r['title']=t
OV={2:'상품 판매·광고',52:'OOTD·룩북·GRWM·코디 제안',94:'OOTD·룩북·GRWM·코디 제안',20:'OOTD·룩북·GRWM·코디 제안',78:'스타일링 팁·핵',93:'스타일링 팁·핵',74:'스타일링 팁·핵'}
for r in rows:
    if r['rank'] in OV: r['category']=OV[r['rank']]
json.dump(rows,open('final.json','w'),ensure_ascii=False,indent=1)
with open('data.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(["rank","views","channel","title","category","url","source_hashtag","script","price_reveal","vs_or_question","hashtags","emoji","title_len","india_context","cta"])
    for r in rows: w.writerow([r['rank'],r['views'],r['channel'],r['title'],r['category'],r['url'],r['source_hashtag'],r['script'],int(r['price_reveal']),int(r['vs_or_question']),r['hashtags'],r['emoji'],r['title_len'],int(r['hindi_india']),int(r['cta'])])
V=[r['views'] for r in rows]
print("n",len(rows),"sum",sum(V)/1e9,"median",st.median(V)/1e6,"mean",st.mean(V)/1e6,"min",min(V)/1e6,"max",max(V)/1e6)
print("count >=10M",sum(v>=1e7 for v in V),">=50M",sum(v>=5e7 for v in V),"<5M",sum(v<5e6 for v in V))
g=collections.defaultdict(list)
for r in rows: g[r['category']].append(r)
for k,v in sorted(g.items(),key=lambda kv:-len(kv[1])): print(k,len(v),"median",round(st.median(x['views'] for x in v)/1e6,1),"sum%",round(100*sum(x['views'] for x in v)/sum(V),1))
for key in ["price_reveal","vs_or_question","cta","hindi_india"]:
    a=[r['views'] for r in rows if r[key]]; b=[r['views'] for r in rows if not r[key]]
    print(key,len(a),round(st.median(a)/1e6,1) if a else None,"vs",len(b),round(st.median(b)/1e6,1))
print(collections.Counter(r['script'] for r in rows))
print("hashtags median",st.median(r['hashtags'] for r in rows),"zero",sum(r['hashtags']==0 for r in rows),"emoji>=1",sum(r['emoji']>0 for r in rows),"title_len median",st.median(r['title_len'] for r in rows))
print("src tags",collections.Counter(r['source_hashtag'] for r in rows).most_common(10))
ch=collections.Counter(r['channel'] for r in rows)
print("channels",len(ch),[(k,v) for k,v in ch.most_common(8) if v>1])
for r in rows: print(r['rank'],r['category'][:6],int(r['hindi_india']),r['title'][:50])
