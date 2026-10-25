import subprocess, json, sys, time, concurrent.futures as cf, urllib.parse
tags = """가디건 코트 슬랙스 후드티 맨투맨 셔츠코디 반바지 비니 모자코디 목걸이 선글라스 향수 신발 부츠 구두 스니커즈 나이키 아디다스 뉴발란스 자라 유니클로 HM 다이소 쿠팡 쇼핑 득템 세일 중고 당근 중고옷 빈티지샵 구제옷 패션꿀팁 옷잘입는법 옷 잘입는 법 코디공식 체형 마른체형 통통코디 빅사이즈 어깨넓은 키큰남자 학생코디 중학생코디 고등학생코디 직장인코디 면접룩 결혼식 신부 드레스 웨딩드레스 한복 교복 졸업사진 커플룩 시밀러룩 가족룩 아기옷 아기패션 강아지옷 임산부패션 시니어패션 중년패션 할머니패션 아줌마패션 오빠코디 여친룩 첫데이트 소개팅 여행룩 휴양지룩 해외여행 공항룩 페스티벌룩 클럽룩 헬스룩 운동복 요가복 레깅스 수영복 비키니 속옷 양말 머플러 장갑 우산 시계 반지 귀걸이 헤어액세서리 안경 가발""".split()
queries = """옷 잘입는 법 쇼츠
코디 공식 쇼츠
체형 보완 코디 쇼츠
옷 수선 쇼츠
패션 유튜버 쇼츠
공항 패션 아이돌 쇼츠
웨딩드레스 쇼츠
하객룩 쇼츠
다이소 패션 쇼츠
코디 추천 남자 20대 쇼츠""".split("\n")
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
json.dump(list(res.values()),open("raw_kr2.json","w"),ensure_ascii=False)
print(len(res), sum(1 for v in res.values() if (v[1] or 0)>=1e6))
