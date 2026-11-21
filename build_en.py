# 영문판 생성: 한국어 index.html을 번역 사전으로 바꿔 en/index.html을 만들고, en/contact.html을 따로 만든다.
# 실행 순서: python3 build_pages.py  →  python3 build_en.py
import re, os, html

MAIL = 'mjmg1325@naver.com'
s = open('index.html', encoding='utf8').read()

# ---------- 1. 구조 손질 ----------
# 프로젝트(국문 상세) 구역은 영문판에서 제외
a = s.index('<section id="work">'); b = s.index('<section id="gallery">')
s = s[:a] + s[b:]
# 리포트 띠의 지자체 이름 캡션 제거
s = re.sub(r'<figcaption>.*?</figcaption>', '', s)
# 방문자 수 표시는 국문판에서만
s = re.sub(r'<div class="in"><p class="vis".*?</p></div>\n', '', s, flags=re.S)

T = {
 # 머리·메뉴
 '<html lang="ko">': '<html lang="en">',
 '<title>비써치 BeSearch | 데이터 시각화 보고서 제작</title>': '<title>BeSearch | Data Visualization Reports</title>',
 'content="데이터 시각화 보고서 제작 전문 기업. 기존 양식 보고서(HWPX·PPT), 새로운 양식 보고서(HTML·PDF), 3D 대시보드를 제작합니다."': 'content="BeSearch turns your data into visual reports and dashboards: HWPX, PPT, HTML, PDF and 3D dashboards."',
 'content="비써치 BeSearch"': 'content="BeSearch"',
 'content="비써치 BeSearch | 데이터 시각화 보고서 제작 전문"': 'content="BeSearch | Data Visualization Reports"',
 'content="데이터를 쉽고 빠르게 시각화해드립니다. 기존 양식 보고서(HWPX·PPT), 새로운 양식 보고서(HTML·PDF), 3D 대시보드 제작."': 'content="We visualize your data, simply and fast. Reports in HWPX, PPT, HTML and PDF, and 3D dashboards."',
 'content="https://besearch.co.kr/"': 'content="https://besearch.co.kr/en/"',
 '<small>비써치</small>': '',
 '<a href="index.html#can">서비스 안내</a><a href="daily.html">데이터 동향</a><a href="examples.html">제작 사례</a><a href="pricing.html">금액 산출</a><a href="contact.html">문의·의뢰</a><a class="lang" href="en/index.html" hreflang="en" lang="en">EN</a>':
   '<a href="#can">What we do</a><a href="#process">Process</a><a href="../examples.html">Examples</a><a href="contact.html">Contact</a><a class="lang" href="../index.html" hreflang="ko" lang="ko">한국어</a>',
 # 첫 화면
 '데이터 시각화 보고서 제작 전문': 'Data visualization reports',
 '<h1><span>데이터를 <em>쉽고 빠르게</em></span> <span>시각화해드립니다</span></h1>': '<h1><span>We visualize your data,</span> <span><em>simply and fast</em></span></h1>',
 '<p class="lead1"><span>자료만 보내 주시면 됩니다. 통계자료, 조사 결과, 인터뷰 스크립트를 받아 보고서와 대시보드로 빠르게 만들어 드립니다.</span><br>비써치는 데이터 시각화 보고서 제작 전문 기업입니다.</p>':
   '<p class="lead1"><span>Just send us your material. We turn statistics, survey results and interview transcripts into reports and dashboards, quickly.</span><br>BeSearch is a Korean studio that specializes in data visualization reports.</p>',
 '기존 양식의 보고서': 'Reports in familiar formats',
 '기관에서 쓰는 한글, 파워포인트, 워드 양식 그대로 작성. 제안서 PPT도 제작': 'Written in the formats your organization already uses: Hangul (HWPX), PowerPoint and Word. Proposal decks too.',
 '새로운 양식의 보고서': 'Reports in new formats',
 '웹에서 바로 열리고 그래프가 움직이는 보고서, 인쇄와 배포용 PDF': 'Reports that open in a browser with interactive charts, plus PDF for print and distribution.',
 '대시보드 형태': 'Dashboards',
 '3D 적용': 'with 3D',
 '지역, 연도, 항목을 골라 보는 통계 대시보드. 입체 그래프와 움직임 적용': 'Statistical dashboards filtered by region, year and indicator, with 3D charts and motion.',
 '<b>227<small>개</small></b><span>전국 시군구별 리포트</span>': '<b>227</b><span>reports, one per Korean municipality</span>',
 '<b>1,000<small>여 개</small></b><span>기관별 리포트</span>': '<b>1,000<small>+</small></b><span>reports, one per institution</span>',
 '<strong>조사 대상이 많을수록 유리합니다.</strong> 같은 틀에 대상별 수치만 바꿔 시군구별, 기관별 리포트를 한 번에 생성하도록 설계되어 있습니다. 대상이 수백, 수천 곳이어도 리포트마다 수치와 문장이 자동으로 채워집니다.':
   '<strong>The more units you survey, the more we help.</strong> One template, filled with each unit\'s own figures and sentences, produces a separate report for every municipality or institution in a single run, whether there are hundreds or thousands.',
 '<b>대상별 리포트 자동 생성</b><span>같은 틀로 만든 시군구 229곳의 보고서 화면(교통문화지수 지자체 컨설팅 보고서)</span>': '<b>One report per unit, generated automatically</b><span>Report screens for 229 municipalities built from one template (Traffic Culture Index consulting report)</span>',
 # 대표 화면
 '입체(3D)·모션 대시보드 사례': '3D and motion dashboard samples',
 'aria-label="입체 막대 예시"': 'aria-label="3D bars"', 'aria-label="지도 예시"': 'aria-label="Map"', 'aria-label="히트맵 예시"': 'aria-label="Heatmap"',
 '다시 재생': 'Replay',
 '입체 막대 · 2026 구단별 홈경기 평균 관중': '3D bars · Average home attendance by club, 2026',
 '단위: 명 · KBO 정규시즌 720경기': 'Persons · 720 KBO regular-season games',
 '지도 · 시도별 2026 홈경기 총관중': 'Map · Total home attendance by region, 2026',
 '단위: 명 · 홈구단 연고지 기준, 큰 값부터 지도에 맞춰짐': 'Persons · by home club location; regions fall into place from the largest',
 '지도 경계: @svg-maps/south-korea (CC BY 4.0)': 'Map boundaries: @svg-maps/south-korea (CC BY 4.0)',
 '히트맵 · 구단별 연도별 경기당 평균 관중': 'Heatmap · Average attendance per game by club and year',
 '단위: 천 명 · 낮은 값부터 한 칸씩 열림': 'Thousand persons · cells open from the lowest value',
 '<span>총관중</span><b>1,277만</b>': '<span>Total attendance</span><b>12.77M</b>',
 '<span>경기당 평균</span>': '<span>Average per game</span>',
 '<span>홈 평균 1위</span><b>삼성</b>': '<span>Top home average</span><b>Samsung</b>',
 '>대시보드 사례</span>': '>Dashboard samples</span>',
 'aria-label="방한 외래객 대시보드"': 'aria-label="Inbound visitors"', 'aria-label="농산물 가격동향 대시보드"': 'aria-label="Produce prices"', 'aria-label="국정수행 평가 대시보드"': 'aria-label="Approval rating"',
 '<b>방한 외래객 조사 결과 탐색</b>43개 문항을 국가, 성별, 연령, 방한 목적별로 골라 2025년과 2024년 결과를 비교': '<b>Inbound visitor survey explorer</b>Compare 2025 and 2024 results for 43 questions by country, sex, age and purpose of visit',
 '<b>농산물 가격동향</b>KAMIS 일별 가격을 매일 수집해 평년 대비 수준, 장보기 지수, 품목별 추이를 표시': '<b>Daily produce prices</b>Collected every day from KAMIS: level against the normal year, a shopping index and trends by item',
 '<b>국정수행 평가 종합 추세</b>여러 조사기관의 여론조사 결과를 모아 긍정·부정 평가의 흐름을 한 그래프로 표시': '<b>Presidential approval trend</b>Polls from many pollsters combined into one chart of approval and disapproval',
 # 할 수 있는 일
 '<h2>서비스 안내</h2>': '<h2>What we do</h2>',
 '제공 자료와 산출물, 제작 사례': 'What we need from you, what you get, and real samples',
 '01 · 데이터 → 보고서': '01 · Data → report',
 '데이터만 있으면 필요한 양식의 보고서로 작성': 'Give us the data; get a report in the format you need',
 '엑셀, 통계표, 조사 결과표를 받아 분석하고 보고서로 정리합니다. 같은 내용을 여러 형식으로 함께 낼 수 있습니다.': 'We analyze spreadsheets, statistical tables and survey results and write them up as a report. The same content can be delivered in several formats.',
 '해산어류 양식 사료 실태 동향 · 바로가기': 'Marine fish farming and feed trends (Korean) · open',
 '성소수자 국내외 동향 · 바로가기': 'LGBTQ+ trends in Korea and abroad (Korean) · open',
 '06 · 스크립트 → 정성 보고서': '06 · Transcripts → qualitative report',
 '인터뷰 스크립트만 있으면 정성 보고서로 작성': 'Give us interview transcripts; get a qualitative report',
 'FGI·IDI 전사 스크립트를 받아 그룹별, 응답자별, 주제별로 요약 정리하고 보고서로 만듭니다.': 'We summarize focus group and in-depth interview transcripts by group, respondent and theme, and turn them into a report.',
 '<dt>제공 자료</dt><dd>전사 스크립트, 참석자 프로파일, 조사 가이드(질문지)</dd><dt>산출물</dt><dd>주제별 발언 정리표, 요약, 엑셀·워드·PPT 보고서</dd>': '<dt>You send</dt><dd>Transcripts, participant profiles, discussion guide</dd><dt>You get</dt><dd>Quotes sorted by theme, summaries, and a report in Excel, Word or PPT</dd>',
 '<span>정성조사 자동정리 화면</span>': '<span>Qualitative research organizer</span>',
 '02 · 통계·조사 결과 → 대시보드': '02 · Statistics and surveys → dashboard',
 '통계자료나 조사 결과로 기관별 대시보드 제작': 'Dashboards built from your statistics or survey results',
 '기관이 보유한 통계와 조사 결과를 지역, 연도, 항목별로 골라 보는 화면으로 만듭니다. 공개 데이터는 매일 자동으로 수집해 갱신합니다.': 'We turn an organization\'s statistics and survey results into screens that can be filtered by region, year and indicator. Public data can be collected and refreshed automatically every day.',
 '<dt>사례 1</dt><dd>교통문화지수 지자체 컨설팅 대시보드: 전국 229개 지자체 선택, 3년 추이, 유형화 결과</dd><dt>사례 2</dt><dd>임산물 생산지도: 품목 123종의 시군구별 생산량과 순위</dd>': '<dt>Sample 1</dt><dd>Traffic Culture Index consulting dashboard: 229 municipalities, three-year trends, typology</dd><dt>Sample 2</dt><dd>Forest products map: output and ranking by municipality for 123 items</dd>',
 '<span>교통문화지수 대시보드</span>': '<span>Traffic Culture Index dashboard</span>',
 '<span>임산물 생산지도</span>': '<span>Forest products map</span>',
 '03 · A4 문서·PDF 산출': '03 · A4 documents and PDF',
 '같은 자료로 A4 문서와 PDF까지 제작': 'The same data, also as an A4 document and PDF',
 '대시보드에 쓴 통계와 그래프를 A4 세로 문서로 다시 구성해 표지, 목차, 본문을 갖춘 PDF로 냅니다. 대시보드에서 대상이나 기간을 골라 PDF로 내려받게 하거나, 매월 정해진 날에 자동으로 발행할 수도 있습니다.': 'We rebuild the statistics and charts of a dashboard as an A4 portrait document with a cover, contents and body, and export it as PDF. A dashboard can also offer a PDF download for a chosen unit or period, or publish a PDF automatically every month.',
 '<dt>사례</dt><dd>평생학습 개인실태조사 A4 문서(세로, 72쪽)의 표지와 본문 2쪽</dd>': '<dt>Sample</dt><dd>Cover and two pages from a 72-page A4 document on the Lifelong Learning Survey</dd>',
 '<span>표지</span>': '<span>Cover</span>', '<span>본문 · 추이 그래프</span>': '<span>Body · trend chart</span>', '<span>본문 · 시도별 표</span>': '<span>Body · table by region</span>',
 '04 · 공고문·제안요청서 → 제안서 PPT': '04 · Tender notice and RFP → proposal deck',
 '공고문과 제안요청서를 주시면 제안서 PPT로 제작': 'Send the tender notice and RFP; get a proposal deck',
 '입찰 공고문과 제안요청서(RFP)의 요구 사항을 항목별로 정리해 목차를 잡고, 지정 템플릿이나 원하는 디자인에 맞춰 발표용 제안서를 만듭니다.': 'We list the requirements in the tender notice and RFP, build the outline around them, and produce a presentation deck in the required template or the design you want.',
 '<dt>제공 자료</dt><dd>공고문, 제안요청서(과업지시서), 발주처 템플릿 또는 원하는 디자인 예시</dd><dt>산출물</dt><dd>편집 가능한 PPT 제안서(표·도형·차트 수정 가능), 필요 시 PDF</dd>': '<dt>You send</dt><dd>Tender notice, RFP, the client\'s template or a design reference</dd><dt>You get</dt><dd>An editable PPT deck (tables, shapes and charts stay editable), and PDF if needed</dd>',
 '<b>요구 사항 정리</b><span>제안요청서의 평가 항목과 과업 내용을 대응표로 정리</span>': '<b>Map the requirements</b><span>Evaluation criteria and scope from the RFP in a compliance table</span>',
 '<b>목차·뼈대 구성</b><span>평가 항목 순서에 맞춘 목차와 장표별 핵심 문장</span>': '<b>Outline</b><span>Contents in the order of the criteria, with a key message per slide</span>',
 '<b>장표 제작</b><span>템플릿의 표지·간지·색을 그대로 살려 표, 도형, 차트로 작성</span>': '<b>Build the slides</b><span>Tables, shapes and charts that keep the template\'s cover, dividers and colors</span>',
 '<b>검토·수정</b><span>요구 사항 누락 여부를 대조하고 의견을 받아 수정</span>': '<b>Review and revise</b><span>Check that no requirement is missing and apply your comments</span>',
 '05 · 대상별 리포트 대량 생성': '05 · One report per unit, at scale',
 '전국 227개 시군구, 기관 1,000여 곳의 리포트도 한 번에 생성': 'Reports for all 227 municipalities, or 1,000+ institutions, in one run',
 '조사 대상이 많을 때 강합니다. 한 번 만든 틀에 대상별 수치를 넣어, 지역이나 기관마다 순위, 등급, 추이, 해석 문장이 다른 리포트를 자동으로 만듭니다. 화면에서 대상을 골라 보고 PDF로 내려받거나, 전체를 한꺼번에 인쇄할 수 있습니다.': 'This is where we are strongest. Each unit\'s figures go into one template, producing reports whose rankings, grades, trends and commentary differ by region or institution. Readers pick a unit on screen and download its PDF, or print all of them at once.',
 '<dt>사례 1</dt><dd>교통문화지수 지자체 컨설팅 보고서: 전국 229개 시군구별 리포트, 대상 선택 후 PDF 내려받기</dd><dt>사례 2</dt><dd>자치구 AI 통합보고서: 서울 25개 자치구별 보고서, 25개 구 전체 인쇄</dd><dt>확장</dt><dd>대상이 1,000곳을 넘는 기관별 리포트도 같은 방식으로 생성</dd>': '<dt>Sample 1</dt><dd>Traffic Culture Index consulting report: 229 municipal reports with PDF download per unit</dd><dt>Sample 2</dt><dd>District AI report: one report for each of Seoul\'s 25 districts, printable all at once</dd><dt>Scale</dt><dd>The same method works for more than 1,000 institutions</dd>',
 '<span>229개 시군구별 리포트</span>': '<span>229 municipal reports</span>', '<span>25개 자치구별 보고서</span>': '<span>25 district reports</span>',
 # 예시
 '<h2>제작 사례</h2>': '<h2>Chart samples from our dashboards</h2>',

 '<a href="examples.html">제작 사례 전체 보기</a>': '<a href="../examples.html">See all samples (Korean)</a>',
 '<b>평생학습 개인실태조사</b><span>집단 간 차이 점 그래프</span>': '<b>Lifelong Learning Survey</b><span>Dot plot of gaps between groups</span>',
 '<b>한국철도공사 서비스 품질평가</b><span>점수 추이 꺾은선</span>': '<b>Korail service quality evaluation</b><span>Score trend line</span>',
 '<b>국민여행조사</b><span>시도 간 여행 흐름 지도</span>': '<b>Korea National Travel Survey</b><span>Flow map between regions</span>',
 '<b>관광숙박 수급분석 데이터 조사</b><span>수급 사분면 산점도</span>': '<b>Tourist accommodation supply and demand</b><span>Quadrant scatter plot</span>',
 '<b>외래관광객조사</b><span>방한 시장 순위 변화선</span>': '<b>International Visitor Survey</b><span>Bump chart of market rankings</span>',
 '<b>연구산업 실태조사</b><span>인력 구성 도넛</span>': '<b>Research Industry Survey</b><span>Donut of workforce composition</span>',
 '<b>카지노 이용실태조사</b><span>단계별 누적 막대와 표</span>': '<b>Casino Use Survey</b><span>Stacked bars with a table</span>',
 '<b>공공심야약국 운영 현황</b><span>시간대별 다중 꺾은선</span>': '<b>Late-night public pharmacies</b><span>Multi-line chart by hour</span>',
 '<b>연구자 대상 연구산업 실태조사</b><span>요인별 영향 구간 그래프</span>': '<b>Research Industry Survey of researchers</b><span>Interval plot of factor effects</span>',
 # 절차
 '<h2>업무 절차</h2>': '<h2>Process</h2>',
 '문의부터 납품까지 다섯 단계로 진행합니다.': 'Five steps from inquiry to delivery.',
 '<b>문의와 자료 전달</b><span>필요한 결과물과 보유 자료를 알려주시면 검토 후 회신합니다.</span>': '<b>Inquiry and material</b><span>Tell us what you need and what you have; we review and reply.</span>',
 '<b>범위와 견적 확정</b><span>분량, 형식, 일정, 수정 횟수를 정하고 견적을 드립니다.</span>': '<b>Scope and quote</b><span>We agree on length, formats, schedule and rounds of revision, and send a quote.</span>',
 '<b>초안 제작</b><span>목차와 대표 화면을 먼저 보여드리고 방향을 맞춥니다.</span>': '<b>Draft</b><span>You see the outline and a sample screen first, so we agree on direction.</span>',
 '<b>검토와 수정</b><span>의견을 모아 주시면 정해진 횟수 안에서 반영합니다.</span>': '<b>Review and revision</b><span>Send your comments together; we apply them within the agreed rounds.</span>',
 '<b>납품</b><span>약속한 형식의 파일이나 화면 주소로 전달합니다.</span>': '<b>Delivery</b><span>Files in the agreed formats, or a link to the screen.</span>',
 # FAQ
 '<h2>자주 묻는 질문</h2>': '<h2>FAQ</h2>',
 '<summary>어떤 자료를 보내야 하나요?</summary><p>엑셀이나 통계표, 조사 결과표, 인터뷰 전사 스크립트처럼 가지고 계신 자료를 그대로 보내 주시면 됩니다. 제안서는 공고문과 제안요청서, 템플릿이 있으면 함께 보내 주세요. 정리가 덜 된 자료도 검토 후 작업 가능 여부를 알려드립니다.</p>': '<summary>What should I send?</summary><p>Send what you have as it is: spreadsheets, statistical tables, survey results or interview transcripts. For a proposal, include the tender notice, the RFP and a template if there is one. If the material is not yet tidy, we will review it and tell you whether we can work with it.</p>',
 '<summary>어떤 형식으로 받을 수 있나요?</summary><p>기존 양식(HWPX, PPT, DOCX)과 새로운 양식(HTML, PDF), 웹에서 여는 대시보드 가운데 필요한 형식으로 납품합니다. 같은 내용을 두 가지 이상 형식으로 함께 받을 수도 있습니다.</p>': '<summary>Which formats can I get?</summary><p>Familiar formats (HWPX, PPT, DOCX), new formats (HTML, PDF) and web dashboards. The same content can be delivered in two or more formats.</p>',
 '<summary>비용과 기간은 어떻게 정해지나요?</summary><p>분량, 형식, 내용 작성 포함 여부, 수정 횟수에 따라 달라집니다. 자료와 원하는 결과물을 알려주시면 범위를 정한 뒤 견적과 일정을 함께 안내합니다.</p>': '<summary>How are price and schedule decided?</summary><p>They depend on length, formats, whether we also write the content, and the rounds of revision. Tell us about your material and the output you want; once the scope is set we send a quote and a schedule.</p>',
 '<summary>수정은 몇 번까지 가능한가요?</summary><p>견적을 확정할 때 포함되는 수정 횟수를 함께 정합니다. 의견을 한 번에 모아 전달해 주시는 것을 1회로 봅니다.</p>': '<summary>How many revisions are included?</summary><p>The number of rounds is agreed with the quote. One round means one consolidated set of comments.</p>',
 '<summary>보낸 자료는 어떻게 관리되나요?</summary><p>받은 자료는 의뢰하신 작업에만 사용합니다. 공개되지 않은 자료와 결과물은 동의 없이 외부에 공개하거나 예시로 사용하지 않습니다. 자세한 내용은 <a href="privacy.html">개인정보처리방침</a>에서 확인할 수 있습니다.</p>': '<summary>How is my material handled?</summary><p>We use it only for the work you ordered. Unpublished material and deliverables are not disclosed or used as samples without your consent. See our <a href="../privacy.html">Privacy Policy (Korean)</a>.</p>',
 # 회사
 '<h2>회사 소개</h2>': '<h2>About</h2>',
 '비써치(BeSearch)는 데이터 시각화 보고서 제작 전문 기업입니다.': 'BeSearch is a Korean studio that specializes in data visualization reports.',
 '<dt>상호</dt><dd>비써치(BeSearch)</dd>': '<dt>Name</dt><dd>BeSearch</dd>',
 '<dt>사업자등록번호</dt>': '<dt>Business registration no.</dt>',
 '<dt>개업</dt><dd>2025년 11월</dd>': '<dt>Established</dt><dd>November 2025</dd>',
 '<dt>업종</dt><dd>시장조사 및 여론조사업, 기타 인문 및 사회과학 연구개발업, 전자상거래 소매업</dd>': '<dt>Business</dt><dd>Market research and public opinion polling; research in the humanities and social sciences; e-commerce</dd>',
 # 바닥글
 '<h5>서비스</h5><a href="index.html#can">서비스 안내</a><a href="index.html#process">업무 절차</a><a href="examples.html">제작 사례</a><a href="pricing.html">금액 산출표</a>': '<h5>Services</h5><a href="#can">What we do</a><a href="#process">Process</a><a href="../examples.html">Examples (Korean)</a>',
 '<h5>고객지원</h5><a href="daily.html">데이터 동향</a><a href="index.html#faq">자주 묻는 질문</a><a href="contact.html">문의·의뢰</a>': '<h5>More</h5><a href="../daily.html">Daily trends (Korean)</a><a href="#faq">FAQ</a><a href="contact.html">Contact</a>',
 '<h5>약관 및 정책</h5><a href="terms.html">이용약관</a><a href="privacy.html"><strong>개인정보처리방침</strong></a>': '<h5>Policies</h5><a href="../terms.html">Terms of Service (Korean)</a><a href="../privacy.html"><strong>Privacy Policy (Korean)</strong></a>',
 '상호 비써치(BeSearch) · 사업자등록번호 189-36-01510 · 업종 시장조사 및 여론조사업 외 · 문의 mjmg1325@naver.com': 'BeSearch · Business registration no. 189-36-01510 · Republic of Korea · mjmg1325@naver.com',
 '<a href="en/index.html" hreflang="en">English</a>': '<a href="../index.html" hreflang="ko">한국어</a>',
 '<a class="logo" href="index.html"><span>Be<b>Search</b></span></a>': '<a class="logo" href="index.html"><span>Be<b>Search</b></span></a>',
}
miss = []
for k in sorted(T, key=len, reverse=True):
    if k not in s:
        miss.append(k[:50])
    s = s.replace(k, T[k])

s = re.sub(r'<p class="sub">대시보드마다 대표 그래프를 하나씩 골랐습니다\.[^<]*</p>', '<p class="sub">One representative chart from each dashboard. The screens themselves are in Korean.</p>', s)
# ---------- 2. 그래프 안의 이름·단위 ----------
TEAM = {'삼성': 'Samsung', '두산': 'Doosan', '롯데': 'Lotte', '한화': 'Hanwha', '키움': 'Kiwoom'}
REGION = {'서울': 'Seoul', '대구': 'Daegu', '부산': 'Busan', '광주': 'Gwangju', '인천': 'Incheon', '대전': 'Daejeon', '경기': 'Gyeonggi', '경남': 'Gyeongnam'}
s = re.sub(r'data-tip="([^"]*?) 홈경기 평균 ([\d,]+)명"', lambda m: f'data-tip="{TEAM.get(m.group(1), m.group(1))} home average {m.group(2)}"', s)
s = re.sub(r'data-tip="([^"]*?) 홈경기 총관중 ([\d,]+)명"', lambda m: f'data-tip="{REGION.get(m.group(1), m.group(1))} total home attendance {m.group(2)}"', s)
s = re.sub(r'data-tip="([^"]*?) (\d{4})년 평균 ([\d,]+)명"', lambda m: f'data-tip="{TEAM.get(m.group(1), m.group(1))} {m.group(2)} average {m.group(3)}"', s)
s = re.sub(r'<em>(\d+)만</em>', lambda m: f'<em>{int(m.group(1))/100:.2f}M</em>', s)
s = s.replace('<span>LG·두산·키움</span>', '<span>LG · Doosan · Kiwoom</span>')
for k, v in {**TEAM, **REGION}.items():
    s = re.sub(r'>' + k + r'<', '>' + v + '<', s)
s = s.replace(".toLocaleString('ko-KR')+'명 · '+el.dataset.c+' '+el.dataset.y", ".toLocaleString('en-US')+' · '+({'삼성':'Samsung','두산':'Doosan','롯데':'Lotte','한화':'Hanwha','키움':'Kiwoom'}[el.dataset.c]||el.dataset.c)+' '+el.dataset.y")
s = re.sub(r'aria-label="[^"]*[가-힣][^"]*"', 'aria-label="chart"', s)
s = re.sub(r'alt="[^"]*[가-힣][^"]*"', 'alt="Sample screen (Korean)"', s)
s = s.replace('.rc figcaption{', '.rc figcaption{display:none;')
s = s.replace('</style>', '.hero h1{font-size:clamp(30px,6.7vw,74px)}.hero p.lead1 span{white-space:normal}@media (max-width:820px){nav a[href="#process"]{display:none}.hero h1 span{white-space:normal;width:auto}}\n</style>', 1)

# ---------- 3. 경로 ----------
s = re.sub(r'(src|href)="(img/|thumbs/|reports/)', r'\1="../\2', s)
s = s.replace('href="index.html#', 'href="#')

# 남은 한글 점검(스크립트·한국어 전환 링크 제외)
body = re.sub(r'<script.*?</script>', '', s[s.index('<body>'):], flags=re.S).replace('>한국어<', '><')
left = sorted(set(x.strip() for x in re.findall(r'>([^<>]*[가-힣][^<>]*)<', body)))
os.makedirs('en', exist_ok=True)
open('en/index.html', 'w', encoding='utf8').write(s)
print('en/index.html', len(s) // 1024, 'KB', '| not found in source:', len(miss), miss[:8], '| leftover Korean:', len(left), left[:12])

# ---------- 4. 영문 문의 페이지 ----------
head = s[:s.index('<main')]
tail = s[s.index('<footer>'):]
head = head.replace('<title>BeSearch | Data Visualization Reports</title>', '<title>Contact | BeSearch</title>')
body = f'''<main><div class="in page">
  <h2>Contact</h2>
  <p class="sub">Tell us about your data and the output you need. Fill in the form and press the button to open your mail app with the message ready, or write to us directly.</p>
  <div class="mailbox"><span>Email</span><b id="addr">{MAIL}</b><button type="button" id="copy">Copy address</button></div>
  <form class="form" id="f">
    <div class="row">
      <label>Name<input name="name" required autocomplete="name"></label>
      <label>Organization<input name="org" autocomplete="organization"></label>
    </div>
    <div class="row">
      <label>Reply to<input name="reply" required placeholder="Email or phone"></label>
      <label>Type of request<select name="type">
        <option>Report from data</option><option>Qualitative report from transcripts</option><option>Statistical dashboard</option><option>3D / motion dashboard</option><option>Proposal deck (PPT)</option><option>One report per unit, at scale</option><option>Other</option></select></label>
    </div>
    <label>Preferred schedule<input name="due" placeholder="e.g. by mid-December"></label>
    <label>Details<textarea name="msg" required placeholder="What material you have, the formats you need, and the approximate length"></textarea></label>
    <button type="submit">Open mail app</button>
    <p class="note" style="margin:0">If nothing opens, please email us at the address above. You can attach files in the email. We reply in English or Korean.</p>
  </form>
</div></main>
<script>
(function(){{var M='{MAIL}',f=document.getElementById('f');
f.addEventListener('submit',function(e){{e.preventDefault();var d=new FormData(f);
var s='[Request] '+d.get('type')+' - '+d.get('name')+(d.get('org')?' ('+d.get('org')+')':'');
var b='Name: '+d.get('name')+'\\nOrganization: '+(d.get('org')||'-')+'\\nReply to: '+d.get('reply')+'\\nType: '+d.get('type')+'\\nSchedule: '+(d.get('due')||'-')+'\\n\\nDetails\\n'+d.get('msg');
location.href='mailto:'+M+'?subject='+encodeURIComponent(s)+'&body='+encodeURIComponent(b);}});
document.getElementById('copy').addEventListener('click',function(){{var b=this;
(navigator.clipboard?navigator.clipboard.writeText(M):Promise.reject()).then(function(){{b.textContent='Copied'}},function(){{
var r=document.createRange();r.selectNode(document.getElementById('addr'));var s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent='Selected'}});}});
}})();
</script>
'''
open('en/contact.html', 'w', encoding='utf8').write(head + body + tail)
print('en/contact.html ok')
