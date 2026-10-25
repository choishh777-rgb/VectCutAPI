import subprocess, json, sys, time, concurrent.futures as cf, urllib.parse
tags = """코디 데일리룩 패션 룩북 겨울코디 여름코디 가을코디 봄코디 남자코디 여자코디 남친룩 데이트룩 오오티디 패션쇼츠 스타일링 코디추천 하울 쇼핑하울 신상 무신사 지그재그 에이블리 옷장 옷정리 빈티지 구제 명품 샤넬 루이비통 하객룩 출근룩 데일리코디 대학생코디 소개팅룩 키작녀코디 체형별코디 청바지 원피스 운동화 가방 한국패션 kfashion 코디팁 패션꿀팁 셀럽패션 공항패션 아이돌패션 연예인패션 스트릿패션 옷스타일링 꾸안꾸 미니멀룩 캐주얼룩 트렌치코트 패딩 니트 자켓 청바지코디 스커트 옷가게 동대문 옷사기 패션유튜버 패션브랜드 모델 워킹 런웨이 변신 리폼 옷리폼""".split()
queries = """코디 쇼츠
데일리룩 쇼츠
남자 코디 쇼츠
여자 코디 쇼츠
옷 추천 쇼츠
패션 꿀팁 쇼츠
룩북 쇼츠
하울 쇼츠
옷 리폼 쇼츠
체형별 코디 쇼츠
키작녀 코디 쇼츠
소개팅룩 쇼츠
공항패션 쇼츠
명품 하울 쇼츠
옷 정리 쇼츠""".split("\n")
def yt(u,n):
    p=subprocess.run(["yt-dlp","--flat-playlist","--playlist-end",str(n),"-J",u],capture_output=True,text=True,timeout=400)
    d=json.loads(p.stdout)
    return [(e['id'],e.get('view_count'),e.get('duration'),e.get('title'),e.get('channel') or e.get('uploader')) for e in d['entries']]
def run(job):
    kind,k=job
    try:
        time.sleep(1.0)
        if kind=="tag": r=yt("https://www.youtube.com/hashtag/%s/shorts"%urllib.parse.quote(k),250)
        else: r=yt("ytsearch80:"+k,80)
        return job,r
    except Exception as ex:
        return job,[]
jobs=[("tag",t) for t in tags]+[("q",q) for q in queries]
res={}
with cf.ThreadPoolExecutor(4) as ex:
    for job,r in ex.map(run,jobs):
        n=sum(1 for x in r if (x[1] or 0)>=1e6)
        print(job,len(r),n,file=sys.stderr,flush=True)
        for x in r: res.setdefault(x[0],x+(job[1],))
json.dump(list(res.values()),open("raw_kr.json","w"),ensure_ascii=False)
print(len(res), sum(1 for v in res.values() if (v[1] or 0)>=1e6))
