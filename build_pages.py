# examples.html, contact.html 생성 + index.html 생성(build.py)
import base64,os,re,html
TH='thumbs/'
MAIL='mjmg1325@naver.com'
FORM_URL='https://docs.google.com/forms/d/e/1FAIpQLSd7X7seoX8WcJfFqxXcLSFgly9ysC7RdNHq7Gqt484Vh3gnIQ/viewform'
t=open('template.html',encoding='utf8').read()
exec(open('build.py',encoding='utf8').read())

# ---------- 공통 머리/꼬리 ----------
HEAD=t[:t.index('<main id="top">')]; TAIL=t[t.index('<footer>'):]
def page(title,body):
    h=HEAD.replace('<title>비써치 BeSearch | 데이터 시각화 보고서 제작</title>',f'<title>{title} | 비써치 BeSearch</title>')
    return h+'<main>'+body+'</main>\n\n'+TAIL

# ---------- 예시 모음 ----------
D,R,I,T='통계 대시보드','보고서·브리프','뉴스 동향·자동 수집','조사 도구·지도'
G='https://baebong3.github.io/'
EX=[ # (썸네일, 제목, 분류, 링크)
('a_AxwtS8vR3UDjcVv1LxLvcj','한국철도공사 서비스 품질 현황 대시보드',D,''),
('r_kbo2','KBO 관중 분석 콘솔 2016~2026',D,''),
('r_kbo1','KBO 관중 분석 콘솔 2025~2026',D,''),
('r_kbo3','KBO 포스트시즌 관중 분석',D,''),
('u_traffic','교통문화지수 지자체 컨설팅 대시보드',D,''),
('r_fruit','농산물 가격동향 일일 리포트',D,G+'fruitbasket/'),
('r_fruitbasket2','농산물 장바구니 지수',D,G+'fruitbasket/basket.html'),
('a_GWDtKaT8ct8iyNheWrExJC','2025 외래관광객조사 결과 탐색 대시보드',D,''),
('a_FZdLk6sk2TXah7ehK5M7xe','국민여행조사 데이터 대시보드',D,''),
('a_S3PMk1DyCqyG64MSCZyyWm','연구산업 실태조사 대시보드',D,''),
('a_R9kpc3pdhMvBD5T4fTcj8a','연구산업 실태조사 결과 대시보드(예시)',D,''),
('a_V3EaZwxGjiUucxhzZ5Wozs','숙박 통계 종합 대시보드',D,''),
('a_XK1xNbKN6bNjaVo6hy6Rmb','관광숙박 수급 대시보드',D,''),
('a_RYbegj69RkPmyYQTDzD4Uq','방한 의료관광 통계 대시보드',D,''),
('a_CqmVCyFsvYbxJu9KmJxc9B','의료관광 통계마스터 현황',D,''),
('a_Husc7r3XTX5AgnXKdab4dG','방한 시장 순위 변화',D,''),
('a_2wo9xhYeDnZwhSGf2qdmx1','국가산단 산업동향 현황판',D,''),
('a_YSNsnuApQ25zAXJLwkt3T2','해양산업 생태계 현황판',D,''),
('a_8ApuvcZc2F3mcM9UBsXfyd','공공심야약국 운영 현황판',D,''),
('a_4G3xrL2CcwPQKRRe43ekuw','담뱃갑 건강경고 기수별 통계',D,''),
('a_EsYAP17KKdsKXduXCMm9Mj','체육인 실태조사 대시보드',D,''),
('a_YSdeTqzidSWoz7NRrZQGCv','카지노 이용실태조사 결과 대시보드',D,''),
('a_UAPidK1YDQdEhJqKtdxT59','2026/27년도 카지노 이용실태조사 결과 대시보드',D,''),
('a_QhGupdBwRgas3urbX1mZSD','전국학교스포츠클럽 축전 통계',D,''),
('a_DZQepgNkbYgW6yLNwQqoJp','여론조사 종합 추세',D,''),
('a_8g47xXrrixmMAvPnBwJ3Jc','AI 생태계 기업 관측',D,''),
('a_RRnFXztgjxX9c5dwjpKFMa','서울 자치구 AI 통합보고서',D,''),
('u_aqua','해산어류 양식 사료 실태 동향',R,'reports/haesan-feed.html'),
('u_lgbtq','성소수자 국내외 동향',R,'reports/lgbtq-trend.html'),
('a_XqK6piu3XjDP5boytCogfz','KBO 팬 이코노미 순환 구조 보고서',R,''),
('r_kborep','KBO 월간 관중 리포트',R,''),
('r_bizrep','소상공인 정책 여론 브리프',R,''),
('a_42euZ698iwt7f2TDctChqj','AHP 가중치 계산법',R,''),
('r_medtour','의료관광·웰니스 뉴스 동향',I,''),
('r_mice','MICE 산업 뉴스 동향',I,''),
('r_youth2','청년정책 뉴스 동향',I,''),
('r_youth','청년정책 분석·평가 콘솔',I,''),
('r_biz','소상공인 정책 동향',I,''),
('r_forest','임산물 수급 동향',I,''),
('r_fruitrecipe','농산물 가격 기반 오늘의 알뜰 요리',I,G+'fruitbasket/recipes.html'),
('r_forestmap','임산물 생산지도',T,''),
('a_VauRA9WZB8gC1EZ5aUw5Sq','국민여행조사 시도 간 여행 흐름 지도',T,''),
('r_qual','정성조사 자동정리',T,''),
('a_R3sEAVcxkoJwmYMfrcLTQz','연구자 연구산업 실태조사 조사 설계와 설문 화면',T,''),
('a_2QGXksJBKS2jA3FQkd2wzY','전수조사 응답 시스템 시연',T,''),
('a_6MwJdL3BnXhRyx3ofqKRXh','산단 현장 대조 입력',T,''),
('a_2LRDrjb5PwkFLtmJjHa7qW','K-MICE 베뉴파인더 개선 시안',T,''),
('a_E48GEnGCgdicvuHkcrc7KE','K-MICE 베뉴파인더 검증',T,''),
]
cards={c:[] for c in (D,R,I,T)}
for th,title,cat,link in EX:
    b64=base64.b64encode(open(TH+th+'.jpg','rb').read()).decode()
    inner=f'<img loading="lazy" alt="{html.escape(title)} 화면" src="data:image/jpeg;base64,{b64}"><div><b>{html.escape(title)}</b><span>{cat}{" · 열기" if link else ""}</span></div>'
    cards[cat].append(f'<a class="gc" href="{link}">{inner}</a>' if link else f'<div class="gc">{inner}</div>')
secs=''.join(f'<div class="gs" data-c="{c}"><h3 class="gh">{c} <span style="font-weight:500;color:var(--muted);font-size:14px">{len(v)}건</span></h3><div class="gal">{"".join(v)}</div></div>' for c,v in cards.items())
btn='<button class="on" data-f="">전체 '+str(len(EX))+'</button>'+''.join(f'<button data-f="{c}">{c}</button>' for c in cards)
body=f'''<div class="in page">
  <h2>예시</h2>
  <p class="sub">HTML 화면으로 구현한 대시보드, 보고서, 뉴스 동향, 조사 도구 {len(EX)}건의 첫 화면. "열기"가 표시된 항목만 실제 화면으로 연결되고, 나머지는 캡처 화면으로 게재함.</p>
  <div class="filt">{btn}</div>
  {secs}
</div>
<script>document.querySelectorAll('.filt button').forEach(function(b){{b.addEventListener('click',function(){{
document.querySelectorAll('.filt button').forEach(function(x){{x.classList.toggle('on',x===b)}});
document.querySelectorAll('.gs').forEach(function(s){{s.style.display=(!b.dataset.f||s.dataset.c===b.dataset.f)?'':'none'}});}});}});</script>'''
open('examples.html','w',encoding='utf8').write(page('예시',body))
# 첫 화면 예시 띠
PICK=['a_AxwtS8vR3UDjcVv1LxLvcj','r_forest','r_mice','r_forestmap','a_YSNsnuApQ25zAXJLwkt3T2','a_VauRA9WZB8gC1EZ5aUw5Sq','a_2wo9xhYeDnZwhSGf2qdmx1','u_traffic','a_GWDtKaT8ct8iyNheWrExJC','a_FZdLk6sk2TXah7ehK5M7xe','a_DZQepgNkbYgW6yLNwQqoJp','a_Husc7r3XTX5AgnXKdab4dG']
by={e[0]:e for e in EX}; hg=''
for k in PICK:
    th,title,cat,link=by[k]
    hg+=f'<div class="gc"><img alt="{html.escape(title)} 화면" src="thumbs/{th}.jpg"><div><b>{html.escape(title)}</b><span>{cat}</span></div></div>'
ix=open('index.html',encoding='utf8').read().replace('{{HOME_GAL}}',hg).replace('{{EX_N}}',str(len(EX)))
open('index.html','w',encoding='utf8').write(ix)

# ---------- 문의 ----------
body=f'''<div class="in page">
  <h2>문의</h2>
  <p class="sub">조사, 보고서 작성, 대시보드 제작 의뢰를 메일로 받습니다. 아래 양식을 채우고 보내기를 누르면 메일 작성 화면이 열립니다.</p>
  <div class="mailbox"><span>받는 주소</span><b id="addr">{MAIL}</b><button type="button" id="copy">주소 복사</button></div>
  <form class="form" id="f">
    <div class="row">
      <label>이름<input name="name" required autocomplete="name"></label>
      <label>소속<input name="org" autocomplete="organization"></label>
    </div>
    <div class="row">
      <label>회신 연락처<input name="reply" required placeholder="메일 또는 전화번호"></label>
      <label>의뢰 유형<select name="type">
        <option>조사 설계·실사</option><option>보고서 작성(HTML·PPT·PDF·HWPX·DOCX)</option><option>정성 인터뷰 정리</option><option>통계 대시보드 제작</option><option>입체(3D) 대시보드</option><option>기타</option></select></label>
    </div>
    <label>희망 일정<input name="due" placeholder="예: 12월 둘째 주까지"></label>
    <label>의뢰 내용<textarea name="msg" required placeholder="보유 자료, 필요한 결과물 형식, 분량 등을 적어 주세요"></textarea></label>
    <button type="submit">메일 작성 화면 열기</button>
    <p class="note" id="fb" style="margin:0">메일 앱이 열리지 않으면 위 주소로 직접 보내 주세요. 첨부 자료는 메일에서 추가할 수 있습니다.</p>
  </form>
</div>
<script>
(function(){{var M='{MAIL}',f=document.getElementById('f');
f.addEventListener('submit',function(e){{e.preventDefault();var d=new FormData(f);
var s='[의뢰] '+d.get('type')+' - '+d.get('name')+(d.get('org')?' ('+d.get('org')+')':'');
var b='이름: '+d.get('name')+'\\n소속: '+(d.get('org')||'-')+'\\n회신 연락처: '+d.get('reply')+'\\n의뢰 유형: '+d.get('type')+'\\n희망 일정: '+(d.get('due')||'-')+'\\n\\n의뢰 내용\\n'+d.get('msg');
location.href='mailto:'+M+'?subject='+encodeURIComponent(s)+'&body='+encodeURIComponent(b);}});
document.getElementById('copy').addEventListener('click',function(){{var b=this;
(navigator.clipboard?navigator.clipboard.writeText(M):Promise.reject()).then(function(){{b.textContent='복사됨'}},function(){{
var r=document.createRange();r.selectNode(document.getElementById('addr'));var s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent='선택됨'}});}});
}})();
</script>'''
# 구글 폼 주소를 FORM_URL에 넣으면 문의 페이지가 폼 연결형으로 바뀜 (예: https://docs.google.com/forms/d/e/.../viewform)
if FORM_URL:
    emb=FORM_URL+('&' if '?' in FORM_URL else '?')+'embedded=true'
    body=f'''<div class="in page">
  <h2>문의</h2>
  <p class="sub">조사, 보고서 작성, 대시보드 제작 의뢰를 아래 양식으로 받습니다. 제출하면 담당자에게 바로 전달됩니다.</p>
  <div class="links" style="margin:0 0 18px"><a href="{FORM_URL}" target="_blank" rel="noopener">새 창에서 양식 열기</a></div>
  <iframe src="{emb}" title="의뢰 양식" style="width:100%;max-width:760px;height:1400px;border:1px solid var(--line);border-radius:12px;background:#fff" loading="lazy">양식을 불러오는 중입니다.</iframe>
  <p class="note">양식이 보이지 않으면 {MAIL} 로 메일을 보내 주세요.</p>
</div>'''
open('contact.html','w',encoding='utf8').write(page('문의',body))
print('pages ok',os.path.getsize('examples.html')//1024,'KB',len(EX))

# ---------- 매일 서비스 ----------
open('daily.html','w',encoding='utf8').write(page('일일 동향 자료',open('daily_body.html',encoding='utf8').read()))
print('daily ok')
