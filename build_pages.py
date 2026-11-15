# index.html 수정 + examples.html, contact.html 생성 (build.py 실행 뒤에 실행)
import base64,os,re,html
TH='thumbs/'
MAIL='mjmg1325@naver.com'
t=open('template.html',encoding='utf8').read()
def rep(a,b,cnt=1):
    global t
    assert a in t, a[:50]
    t=t.replace(a,b,cnt)
NAV='<nav><a href="index.html#service">하는 일</a><a href="index.html#work">프로젝트</a><a href="examples.html">예시</a><a href="contact.html">문의</a></nav>'
rep('<nav><a href="#service">하는 일</a><a href="#work">프로젝트</a><a href="#company">회사 정보</a></nav>',NAV)
rep('<a class="logo" href="#top">','<a class="logo" href="index.html">')
rep('<p>비써치는 시장조사·여론조사와 사회과학 연구를 수행하고, 그 결과를 대시보드와 서비스로 제작합니다. 수집부터 검증, 게시까지 자동으로 돌아가는 구조로 운영합니다.</p>',
    '<p>비써치는 데이터와 인터뷰 자료를 받아 보고서와 통계 대시보드로 제작합니다. HTML, PPT, PDF, HWPX, DOCX 가운데 필요한 형식으로 납품합니다.</p>')
rep('<a class="btn" href="#company">회사 정보</a>','<a class="btn" href="examples.html">예시 보기</a><a class="btn" href="contact.html">의뢰하기</a>')
s0=t.index('<p class="sub">사업자등록 업종 기준 세 가지 영역</p>'); s1=t.index('</div></section>',s0)
t=t[:s0]+'''<p class="sub">자료를 받아 결과물로 만드는 네 가지 작업</p>
  <div class="svc">
    <div><span class="no">01</span><h3>모든 형식의 보고서</h3><p>데이터를 받아 HTML, PPT, PDF, HWPX, DOCX 보고서로 작성</p></div>
    <div><span class="no">02</span><h3>정성 인터뷰 정리</h3><p>인터뷰 스크립트를 받아 요약 정리하고 보고서로 작성</p></div>
    <div><span class="no">03</span><h3>기관별 통계 대시보드</h3><p>기관이 보유한 통계와 조사 결과를 한 화면에서 조회하는 대시보드 제작</p></div>
    <div><span class="no">04</span><h3>입체(3D) 대시보드</h3><p>지도, 막대, 카드에 입체 표현과 움직임을 적용한 대시보드 제작</p></div>
  </div>
'''+t[s1:]
rep('.svc{display:grid;grid-template-columns:repeat(3,1fr)','.svc{display:grid;grid-template-columns:repeat(4,1fr)')
rep('.svc,.feat{grid-template-columns:1fr}','.svc,.feat{grid-template-columns:1fr}\n  .form .row{grid-template-columns:1fr}\n  .gal{grid-template-columns:1fr 1fr}')
rep('@media (max-width:820px){','@media (max-width:1000px){.svc{grid-template-columns:1fr 1fr}}\n@media (max-width:820px){')
rep('    <div class="links"><a href="https://baebong3.github.io/kbo-dashboard/">대시보드 열기</a></div>\n','')
a0=t.index('<div class="two">'); a1=t.index('</div></section>',a0)
t=t[:a0]+'''<article class="proj">
    <div class="proj-h"><h3>해산어류 양식 사료 실태 동향</h3><span class="tag">동향보고서</span></div>
    <p>어류양식동향조사(2025 잠정)와 해양수산부 고수온 피해 집계(2026년 9월 4일 잠정)를 바탕으로 생산, 사료 구조, 정책 수단, 고수온 피해를 정리한 보고서.</p>
    <div class="kpis">
      <div class="kpi"><span>양식 생산량</span><b>82,807톤</b><em>2025 잠정, +1.1%</em></div>
      <div class="kpi"><span>생산금액</span><b>1조 3,579억</b><em>2025 잠정, +12.1%</em></div>
      <div class="kpi"><span>배합사료 비중</span><b>16% 내외</b><em>추정치</em></div>
      <div class="kpi"><span>고수온 폐사</span><b>1,353만 마리</b><em>2026년 9월 4일 잠정</em></div>
    </div>
    <div class="links"><a href="reports/haesan-feed.html">보고서 열기</a></div>
  </article>
  <article class="proj">
    <div class="proj-h"><h3>교통문화지수 지자체 컨설팅 대시보드</h3><span class="tag">기관별 대시보드</span></div>
    <p>한국교통안전공단 「2025년 교통문화지수 실태조사」 결과를 지자체별 컨설팅 보고서로 구성한 대시보드. 시도와 시군구를 고르면 해당 지자체의 종합 지수, 등급, 그룹 내 순위, 최근 3년 추이, 유형화 결과, 교통사고 현황이 한 화면에 표시되고 PDF로 내려받을 수 있음.</p>
    <div class="kpis">
      <div class="kpi"><span>대상 지자체</span><b>229개</b><em>17개 시도 전체</em></div>
      <div class="kpi"><span>지자체 유형</span><b>5개</b><em>교통선도형 ~ 이동지원형</em></div>
      <div class="kpi"><span>평가 영역</span><b>3개</b><em>운전행태·보행행태·교통안전</em></div>
      <div class="kpi"><span>추이 기간</span><b>3년</b><em>2023~2025</em></div>
    </div>
    <img class="cap" loading="lazy" src="img/traffic-culture.jpg" alt="교통문화지수 지자체 컨설팅 대시보드 화면">
    <p class="note">원자료는 공개 대상이 아니어서 결과물 화면으로 게재함.</p>
  </article>
  <div class="links"><a href="examples.html">예시 전체 보기</a></div>
'''+t[a1:]
c0=t.index('<section id="company">'); c1=t.index('</main>')
t=t[:c0]+'''<section id="company"><div class="in">
  <h2>회사 정보</h2>
  <p class="sub">2025년 11월 개업</p>
  <dl class="info">
    <dt>상호</dt><dd>비써치(BeSearch)</dd>
    <dt>업종</dt><dd>시장조사 및 여론조사업, 전자상거래 소매업, 기타 인문 및 사회과학 연구개발업</dd>
    <dt>문의</dt><dd><a href="contact.html">조사·분석 의뢰하기</a></dd>
  </dl>
</div></section>
'''+t[c1:]
f0=t.index('<footer>'); f1=t.index('</footer>')
FOOT='<footer><div class="in">비써치(BeSearch) · <a href="contact.html">문의</a><br>© 2026 BeSearch</div>'
t=t[:f0]+FOOT+t[f1:]
rep('#tip{position:fixed','''.gal{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.gc{background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden;text-decoration:none;display:block}
.gc img{display:block;width:100%;aspect-ratio:8/5;object-fit:cover;object-position:top;border-bottom:1px solid var(--line);background:#fff}
.gc div{padding:11px 14px 13px}
.gc b{display:block;font-size:14.5px;line-height:1.4}
.gc span{font-size:12.5px;color:var(--muted)}
a.gc:hover{border-color:var(--acc)}
.filt{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:20px}
.filt button{font:inherit;font-size:14px;font-weight:600;padding:7px 14px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--ink2);cursor:pointer}
.filt button.on{background:var(--acc);border-color:var(--acc);color:var(--bg)}
.cap{display:block;width:100%;border:1px solid var(--line);border-radius:12px;margin-top:6px}
.gh{font-size:18px;font-weight:800;margin:30px 0 12px}
.form{max-width:640px;display:grid;gap:14px}
.form .row{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.form label{display:grid;gap:6px;font-size:14px;font-weight:600}
.form input,.form select,.form textarea{font:inherit;font-size:15px;padding:11px 12px;border:1px solid var(--line);border-radius:10px;background:var(--card);color:var(--ink);width:100%}
.form textarea{min-height:160px;resize:vertical}
.form input:focus,.form select:focus,.form textarea:focus{outline:2px solid var(--acc);outline-offset:1px}
.form button{font:inherit;font-size:15px;font-weight:700;padding:13px 20px;border-radius:10px;border:0;background:var(--acc);color:var(--bg);cursor:pointer;justify-self:start}
.mailbox{display:flex;align-items:center;gap:10px;flex-wrap:wrap;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;max-width:640px;margin-bottom:26px}
.mailbox b{font-size:17px}
.mailbox button{font:inherit;font-size:13px;font-weight:700;padding:6px 12px;border-radius:8px;border:1px solid var(--line);background:transparent;color:var(--ink2);cursor:pointer}
.page{padding:48px 0 64px}
#tip{position:fixed''')
open('template.html.out','w',encoding='utf8').write(t)
exec(open('build.py',encoding='utf8').read())

# ---------- 공통 머리/꼬리 ----------
HEAD=t[:t.index('<main id="top">')]; TAIL=t[t.index('<footer>'):]
def page(title,body):
    h=HEAD.replace('<title>비써치 BeSearch | 조사·데이터 분석</title>',f'<title>{title} | 비써치 BeSearch</title>')
    return h+'<main>'+body+'</main>\n\n'+TAIL

# ---------- 예시 모음 ----------
D,R,I,T='통계 대시보드','보고서·브리프','이슈 레이더·자동 수집','조사 도구·지도'
G='https://baebong3.github.io/'
EX=[ # (썸네일, 제목, 분류, 링크)
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
('a_AxwtS8vR3UDjcVv1LxLvcj','한국철도공사 서비스 품질 현황 대시보드',D,''),
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
('a_JLwU9Twz91ZZkA4B2h3q4d','관광두레 사업 현황',D,''),
('a_UhdwGzhC7FaKqAJLc4YazR','넷플릭스 반응 랭킹',D,''),
('a_8g47xXrrixmMAvPnBwJ3Jc','AI 생태계 기업 관측',D,''),
('a_RRnFXztgjxX9c5dwjpKFMa','서울 자치구 AI 통합보고서',D,''),
('u_aqua','해산어류 양식 사료 실태 동향',R,'reports/haesan-feed.html'),
('u_lgbtq','성소수자 국내외 동향',R,'reports/lgbtq-trend.html'),
('a_XqK6piu3XjDP5boytCogfz','KBO 팬 이코노미 순환 구조 보고서',R,''),
('r_kborep','KBO 월간 관중 리포트',R,''),
('r_bizrep','소상공인 정책 여론 브리프',R,''),
('a_VfDTXgces6zQzpBAkX3ZuC','관광두레 조사설계 기획안',R,''),
('a_42euZ698iwt7f2TDctChqj','AHP 가중치 계산법',R,''),
('r_medtour','의료관광·웰니스 이슈 레이더',I,''),
('r_mice','MICE 이슈 레이더',I,''),
('r_youth2','청년정책 이슈 레이더',I,''),
('r_youth','청년정책 분석·평가 콘솔',I,''),
('r_biz','소상공인 정책 레이더',I,''),
('r_forest','임산물 수급 레이더',I,''),
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
  <p class="sub">HTML 화면으로 구현한 대시보드, 보고서, 이슈 레이더, 조사 도구 {len(EX)}건의 첫 화면. "열기"가 표시된 항목만 실제 화면으로 연결되고, 나머지는 캡처 화면으로 게재함.</p>
  <div class="filt">{btn}</div>
  {secs}
</div>
<script>document.querySelectorAll('.filt button').forEach(function(b){{b.addEventListener('click',function(){{
document.querySelectorAll('.filt button').forEach(function(x){{x.classList.toggle('on',x===b)}});
document.querySelectorAll('.gs').forEach(function(s){{s.style.display=(!b.dataset.f||s.dataset.c===b.dataset.f)?'':'none'}});}});}});</script>'''
open('examples.html','w',encoding='utf8').write(page('예시',body))

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
open('contact.html','w',encoding='utf8').write(page('문의',body))
print('pages ok',os.path.getsize('examples.html')//1024,'KB',len(EX))
