import subprocess, json, sys, concurrent.futures as cf, urllib.parse
tags = """ootd outfit fashion style grwm outfitideas outfitinspo streetstyle fashiontrends lookbook thrift thriftflip haul tryonhaul sneakers dress jeans mensfashion womensfashion fashiontips stylingtips fashionhacks diyclothes outfitoftheday dailyoutfit y2k oldmoney koreanfashion 코디 데일리룩 패션 runway fashionweek fashionmodel fashiondesigner sewing upcycle closet shoes streetwear vintage summeroutfit winteroutfit fallfashion modestfashion plussize fashionshow outfitcheck getreadywithme styletips capsulewardrobe minimalfashion fashionstyle fashionblogger outfittransition fashionvideo 패션쇼츠 룩북 겨울코디 여름코디 mensstyle womensstyle fashionista trendyoutfits fashionreels clothinghaul outfitswap""".split()
def run(t):
    u="https://www.youtube.com/hashtag/%s/shorts"%urllib.parse.quote(t)
    try:
        p=subprocess.run(["yt-dlp","--flat-playlist","--playlist-end","250","-J",u],capture_output=True,text=True,timeout=500)
        d=json.loads(p.stdout)
        return t,[(e['id'],e.get('view_count'),e.get('duration'),e.get('title'),e.get('channel') or e.get('uploader')) for e in d['entries']]
    except Exception as ex:
        return t,[]
res={}
with cf.ThreadPoolExecutor(8) as ex:
    for t,r in ex.map(run,tags):
        n=sum(1 for x in r if (x[1] or 0)>=1e6)
        print(t,len(r),n,file=sys.stderr,flush=True)
        for x in r: res.setdefault(x[0],x+(t,))
json.dump(list(res.values()),open("raw2.json","w"),ensure_ascii=False)
print(len(res), sum(1 for v in res.values() if (v[1] or 0)>=1e6))
