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
        if True:
            out.append(f'<text class="val" x="{x+w/2:.1f}" y="{y-7:.1f}" text-anchor="middle">{f(v)}</text>')
        out.append(f'<text class="xl" x="{x+w/2:.1f}" y="{H-9}" text-anchor="middle">{str(yr)[2:]}</text>')
    out.append(f'<line class="axis" x1="{L}" x2="{W-R}" y1="{H-B}" y2="{H-B}"/>')
    return f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="연도별 경기당 평균 관중 막대그래프">{"".join(out)}</svg>'

def team_rows():
    mx=TEAMS[0][1]; r=[]
    for t,v in TEAMS:
        r.append(f'<li class="mk" tabindex="0" data-tip="{t} 홈경기 평균 {f(v)}명"><span class="tn">{t}</span><span class="tb"><i style="width:{v/mx*100:.1f}%"></i></span><span class="tv">{f(v)}</span></li>')
    return ''.join(r)


def iso_chart(t=1.0):
    c,ox,oy,H=34,62,196,168; mx=TEAMS[0][1]
    def P(x,y,z): return f"{ox+(x-y)*c*0.866:.1f},{oy+(x+y)*c*0.5-z:.1f}"
    o=[f'<polygon class="fl" points="{P(-.7,-.7,0)} {P(15.1,-.7,0)} {P(15.1,1.7,0)} {P(-.7,1.7,0)}"/>']; lab=[]
    for i,(tm,v) in enumerate(TEAMS):
        x0,x1,y0,y1,h=i*1.5,i*1.5+.9,0,.9,v/mx*H*t
        top,lf,rt=('#F2B89A','#D9703F','#A9502A') if i==0 else ('#7FC4BD','#2F7F79','#17504C')
        o.append(f'<g class="mk" tabindex="0" data-tip="{tm} 홈경기 평균 {f(v)}명">'
                 f'<polygon fill="{lf}" points="{P(x0,y1,0)} {P(x1,y1,0)} {P(x1,y1,h)} {P(x0,y1,h)}"/>'
                 f'<polygon fill="{rt}" points="{P(x1,y0,0)} {P(x1,y1,0)} {P(x1,y1,h)} {P(x1,y0,h)}"/>'
                 f'<polygon fill="{top}" points="{P(x0,y0,h)} {P(x1,y0,h)} {P(x1,y1,h)} {P(x0,y1,h)}"/></g>')
        vx,vy=P(x0+.45,.45,h).split(','); nx,ny=P(x0+.45,2.1,0).split(',')
        lab.append(f'<text class="vl" text-anchor="middle" x="{vx}" y="{float(vy)-12:.1f}">{f(round(v*t))}</text><text class="nm" text-anchor="middle" x="{nx}" y="{float(ny)+4:.1f}">{tm}</text>')
    return f'<svg id="isoS" viewBox="0 0 560 500" role="img" aria-label="2026 구단별 홈경기 평균 관중 입체 막대그래프">{"".join(o)}{"".join(lab)}</svg>'

import json as _json
HEAT={'삼성':[9367,11912,18452,23101,23521],'LG':[12919,16939,19144,21725,22222],'두산':[8953,13282,18335,19595,21233],'롯데':[8773,12216,17364,20653,19161],'KIA':[8394,10099,17250,15207,17800],'SSG':[13633,14633,16109,17549,17627],'한화':[4975,7764,11327,16875,16207],'kt':[7393,9553,11887,13301,14408],'키움':[4858,8220,11073,12312,12820],'NC':[5125,7854,10261,10621,12369]}
REG=[('seoul','서울','LG·두산·키움',4065612),('daegu','대구','삼성',1717050),('busan','부산','롯데',1360401),('gwangju','광주','KIA',1299388),('incheon','인천','SSG',1251538),('daejeon','대전','한화',1150694),('gyeonggi','경기','kt',1022972),('south-gyeongsang','경남','NC',902905)]
def _mix(a,b,t):
    a=[int(a[i:i+2],16) for i in (1,3,5)]; b=[int(b[i:i+2],16) for i in (1,3,5)]
    return '#%02X%02X%02X'%tuple(round(a[i]+(b[i]-a[i])*t) for i in range(3))
def heat_chart():
    L,T,cw,ch=46,24,90,31; ys=[2022,2023,2024,2025,2026]
    vals=[v for r in HEAT.values() for v in r]; lo,hi=min(vals),max(vals); o=[]
    for j,y in enumerate(ys): o.append(f'<text class="hx" text-anchor="middle" x="{L+j*cw+cw/2}" y="15">{y}</text>')
    for i,(tm,row) in enumerate(HEAT.items()):
        y0=T+i*ch; o.append(f'<text class="hy" x="0" y="{y0+ch/2+4}">{tm}</text>')
        for j,v in enumerate(row):
            t=(v-lo)/(hi-lo); x0=L+j*cw
            o.append(f'<rect class="h0" x="{x0+1}" y="{y0+1}" width="{cw-2}" height="{ch-2}" rx="3"/>'
                     f'<g class="pc mk" tabindex="0" data-v="{v}" data-c="{tm}" data-y="{ys[j]}" data-tip="{tm} {ys[j]}년 평균 {f(v)}명"><rect x="{x0+1}" y="{y0+1}" width="{cw-2}" height="{ch-2}" rx="3" fill="{_mix('#DCEBE8','#17504C',t)}"/>'
                     f'<text class="hv" text-anchor="middle" x="{x0+cw/2}" y="{y0+ch/2+4}" fill="{'#fff' if t>0.45 else '#15191E'}">{v/1000:.1f}</text></g>')
    return f'<svg id="heatS" viewBox="0 0 {L+5*cw} {T+10*ch}" role="img" aria-label="구단별 연도별 경기당 평균 관중 히트맵">{"".join(o)}</svg>'
def map_chart():
    m=_json.load(open('skmap.json')); val={r[0]:r for r in REG}; lo,hi=REG[-1][3],REG[1][3]; o=[]
    for l in m['locations']:
        if l['id'] in val:
            v=val[l['id']][3]; t=min(1,(v-lo)/(hi-lo)); nm=val[l['id']][1]
            o.append(f'<path class="rg mk" tabindex="0" data-id="{l["id"]}" data-v="{v}" data-tip="{nm} 홈경기 총관중 {f(v)}명" fill="{_mix('#BFE0DB','#17504C',t)}" d="{l["path"]}"/>')
        else:
            o.append(f'<path class="rg nv" d="{l["path"]}"/>')
    o.sort(key=lambda s:'nv' not in s)
    rows=''.join(f'<li data-id="{i}"><i>{k+1}</i><b>{n}</b><span>{tm}</span><em>{v/10000:,.0f}만</em></li>' for k,(i,n,tm,v) in enumerate(REG))
    return f'<div class="mapw"><svg id="mapS" viewBox="{m["viewBox"]}" role="img" aria-label="시도별 2026 홈경기 총관중 지도">{"".join(o)}</svg><ol class="mapl" id="mapL">{rows}</ol></div>'

def marquee():
    rs=_json.load(open('regions.json',encoding='utf8')); o=[]
    for n,sd,mt in rs:
        o.append(f'<figure class="rc"><img loading="lazy" decoding="async" width="210" height="279" src="img/rep/{n}.jpg" alt=""><figcaption><small>{sd}</small>{mt}</figcaption></figure>')
    return f'<div class="mq" aria-hidden="true"><div class="mqt" id="mqt">{"".join(o)}</div></div>',len(rs)

def table():
    a=''.join(f'<tr><td>{y}</td><td>{f(v)}</td></tr>' for y,v in YEARS)
    b=''.join(f'<tr><td>{t}</td><td>{f(v)}</td></tr>' for t,v in TEAMS)
    return (f'<div class="tw"><table><caption>연도별 경기당 평균 관중(명)</caption><thead><tr><th>연도</th><th>평균</th></tr></thead><tbody>{a}</tbody></table>'
            f'<table><caption>2026 구단별 홈경기 평균 관중(명)</caption><thead><tr><th>구단</th><th>평균</th></tr></thead><tbody>{b}</tbody></table></div>')

page=open('template.html',encoding='utf8').read()
_mq,_mqn=marquee()
page=page.replace('{{MARQUEE}}',_mq).replace('{{MQ_N}}',str(_mqn)).replace('{{ISO_CHART}}',iso_chart()).replace('{{HEAT_CHART}}',heat_chart()).replace('{{MAP_CHART}}',map_chart()).replace('{{YEAR_CHART}}',year_chart()).replace('{{TEAM_ROWS}}',team_rows()).replace('{{TABLE}}',table())
open('index.html','w',encoding='utf8').write(page)
print(len(page))
