import json, re, csv, statistics as st, collections, unicodedata
rows=json.load(open('curated_kr.json')); rows.sort(key=lambda r:-r['views'])
A="꿀팁·입는 법"; B="코디 제안(상황·체형·아이템)"; C="모델·런웨이·워킹"; D="연예인·명품·아이템 이야기"; E="수선·리폼·DIY"; F="일상·상황극·스토리"; G="쇼핑·구매 연결"
CAT={1:B,2:F,3:C,4:F,5:E,6:A,7:C,8:E,9:B,10:F,11:B,12:A,13:B,14:E,15:C,16:A,17:C,18:B,19:B,20:F,21:D,22:B,23:B,24:F,25:G,26:B,27:F,28:G,29:F,30:B,31:A,32:F,33:C,34:B,35:G,36:F,37:D,38:D,39:F,40:B,41:D,42:F,43:F,44:F,45:F,46:B,47:B,48:F,49:B,50:D,51:D,52:C,53:A,54:A,55:B,56:B,57:B,58:B,59:B,60:C,61:E,62:B,63:B,64:F,65:A,66:D,67:A,68:D,69:B,70:C,71:B,72:A,73:F,74:B,75:A,76:G,77:B,78:E,79:B,80:A,81:F,82:B,83:B,84:E,85:D,86:D,87:D}
hg=re.compile(r'[가-힣]')
BRAND={"비르 VIR","고유 GOYU","톨앤무드","릿씨 reetc","SSROOM","언스테이블 스튜디오 (UNSTABLE_STUDIO)"}
for i,r in enumerate(rows,1):
    t=r['title'].replace("\n"," "); r['title']=t; r['rank']=i; r['category']=CAT[i]
    r['channel']=(r['channel'] or '').strip()
    r['title_ko']=bool(hg.search(t))
    r['hashtags']=len(re.findall(r"#\S+",t))
    r['title_len']=len(re.sub(r"#\S+","",t).strip())
    r['emoji']=sum(1 for ch in t if unicodedata.category(ch)=="So")
    r['howto']=bool(re.search(r"방법|하는 ?법|매는법|꿀팁|넣입|법$|하세요|마세요",t))
    r['question']=bool(re.search(r"\?|vs|투표|1위|어때|맞냐|인가요|일까",t))
    r['pov_relate']=bool(re.search(r"POV|공감|특$|특 |ㅋㅋ|ㄷㄷ",t))
    r['brand_channel']=r['channel'] in BRAND
    r['series_vibecraft']=r['channel']=="VibeCraft"
with open('data_kr.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(["rank","views","channel","title","category","url","source_hashtag","title_has_korean","hashtags","title_len","emoji","howto_phrase","question_or_vote","pov_or_relate","brand_channel"])
    for r in rows: w.writerow([r['rank'],r['views'],r['channel'],r['title'],r['category'],r['url'],r['source_hashtag'],int(r['title_ko']),r['hashtags'],r['title_len'],r['emoji'],int(r['howto']),int(r['question']),int(r['pov_relate']),int(r['brand_channel'])])
json.dump(rows,open('final_kr.json','w'),ensure_ascii=False,indent=1)
V=[r['views'] for r in rows]
print("n",len(rows),"sum",sum(V)/1e8,"억 median",st.median(V)/1e6,"mean",st.mean(V)/1e6,"p25/75",[q/1e6 for q in st.quantiles(V,n=4)],"max",max(V)/1e6,"min",min(V)/1e6)
print(">=10M",sum(v>=1e7 for v in V),">=5M",sum(v>=5e6 for v in V),"<2M",sum(v<2e6 for v in V),"top10 share",round(sum(V[:10])/sum(V),3))
g=collections.defaultdict(list)
for r in rows: g[r['category']].append(r)
for k,v in sorted(g.items(),key=lambda kv:-len(kv[1])): print(k,len(v),"median",round(st.median(x['views'] for x in v)/1e6,2),"sum%",round(100*sum(x['views'] for x in v)/sum(V),1))
for key in ["title_ko","howto","question","pov_relate","brand_channel","series_vibecraft"]:
    a=[r['views'] for r in rows if r[key]]; b=[r['views'] for r in rows if not r[key]]
    print(key,len(a),round(st.median(a)/1e6,2) if a else None,"vs",len(b),round(st.median(b)/1e6,2) if b else None)
print("hashtags median",st.median(r['hashtags'] for r in rows),"zero",sum(r['hashtags']==0 for r in rows),"emoji>=1",sum(r['emoji']>0 for r in rows),"len median",st.median(r['title_len'] for r in rows))
ch=collections.Counter(r['channel'] for r in rows); print("channels",len(ch),ch.most_common(8))
print("#shorts",sum('#shorts' in r['title'].lower() for r in rows))
nv=[r for r in rows if not r['series_vibecraft']]
print("excl VibeCraft n",len(nv),"median",st.median(r['views'] for r in nv)/1e6)
# tag stats
tc=collections.Counter(t for r in rows for t in re.findall(r"#(\S+)",r['title']))
print(tc.most_common(12))
print("top 8 channel share by views",[(c,round(sum(r['views'] for r in rows if r['channel']==c)/1e6,1)) for c,_ in ch.most_common(5)])
print("src hashtag",collections.Counter(r['source_hashtag'] for r in rows).most_common(8))
