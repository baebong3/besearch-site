# besearch.co.kr 첫 화면 생성기 - KBO 수치는 kbo-dashboard/kbo_games.json(2026-11-14 갱신)에서 집계한 값
import html
YEARS=[(2016,11583),(2017,11668),(2018,11214),(2019,10119),(2021,2234),(2022,8439),(2023,11250),(2024,15122),(2025,17101),(2026,17737)]
TEAMS=[('삼성',23521),('LG',22222),('두산',21233),('롯데',19161),('KIA',17800),('SSG',17627),('한화',16207),('kt',14408),('키움',12820),('NC',12369)]
DOW=[('화',15691),('수',16140),('목',16781),('금',18254),('토',19994),('일',19420)]
f=lambda n:format(n,',')

def year_chart():
    W,H,L,B,T=640,280,46,30,26
    R=8; bw=(W-L-R)/len(YEARS); mx=20000; out=[]
    for gv in (5000,10000,15000,20000):
        y=T+(H-T-B)*(1-gv/mx)
        out.append(f'<line class="grid" x1="{L}" x2="{W-R}" y1="{y:.1f}" y2="{y:.1f}"/><text class="tick" x="{L-6}" y="{y+4:.1f}" text-anchor="end">{f(gv)}</text>')
    for i,(yr,v) in enumerate(YEARS):
        h=(H-T-B)*v/mx; x=L+i*bw+bw*0.22; w=bw*0.56; y=H-B-h
        cls='bar hi' if yr==2026 else ('bar lo' if yr==2021 else 'bar')
        out.append(f'<g class="mk" tabindex="0" data-tip="{yr}년 경기당 평균 {f(v)}명"><rect class="hit" x="{L+i*bw:.1f}" y="{T}" width="{bw:.1f}" height="{H-T-B}"/>'
                   f'<path class="{cls}" d="M{x:.1f},{H-B} V{y+4:.1f} Q{x:.1f},{y:.1f} {x+4:.1f},{y:.1f} H{x+w-4:.1f} Q{x+w:.1f},{y:.1f} {x+w:.1f},{y+4:.1f} V{H-B} Z"/>'
                   f'<title>{yr}년 경기당 평균 {f(v)}명</title></g>')
        if yr in (2016,2021,2024,2026):
            out.append(f'<text class="val" x="{x+w/2:.1f}" y="{y-7:.1f}" text-anchor="middle">{f(v)}</text>')
        out.append(f'<text class="xl" x="{x+w/2:.1f}" y="{H-9}" text-anchor="middle">{str(yr)[2:]}</text>')
    out.append(f'<line class="axis" x1="{L}" x2="{W-R}" y1="{H-B}" y2="{H-B}"/>')
    return f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="연도별 경기당 평균 관중 막대그래프">{"".join(out)}</svg>'

def team_rows():
    mx=TEAMS[0][1]; r=[]
    for t,v in TEAMS:
        r.append(f'<li class="mk" tabindex="0" data-tip="{t} 홈경기 평균 {f(v)}명"><span class="tn">{t}</span><span class="tb"><i style="width:{v/mx*100:.1f}%"></i></span><span class="tv">{f(v)}</span></li>')
    return ''.join(r)

def table():
    a=''.join(f'<tr><td>{y}</td><td>{f(v)}</td></tr>' for y,v in YEARS)
    b=''.join(f'<tr><td>{t}</td><td>{f(v)}</td></tr>' for t,v in TEAMS)
    return (f'<div class="tw"><table><caption>연도별 경기당 평균 관중(명)</caption><thead><tr><th>연도</th><th>평균</th></tr></thead><tbody>{a}</tbody></table>'
            f'<table><caption>2026 구단별 홈경기 평균 관중(명)</caption><thead><tr><th>구단</th><th>평균</th></tr></thead><tbody>{b}</tbody></table></div>')

page=open('template.html.out',encoding='utf8').read()
page=page.replace('{{YEAR_CHART}}',year_chart()).replace('{{TEAM_ROWS}}',team_rows()).replace('{{TABLE}}',table())
open('index.html','w',encoding='utf8').write(page)
print(len(page))
