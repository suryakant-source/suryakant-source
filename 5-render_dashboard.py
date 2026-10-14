from PIL import Image, ImageDraw, ImageFont
import urllib.request,json,datetime,pathlib,math,html,random,re,os
from bs4 import BeautifulSoup
O='suryakant-source';root=pathlib.Path('assets-v3');root.mkdir(exist_ok=True)
def fetch(u):
 headers={'User-Agent':'profile-public-data'}
 if u.startswith('https://api.github.com/') and os.environ.get('GH_TOKEN'):headers['Authorization']='Bearer '+os.environ['GH_TOKEN']
 return urllib.request.urlopen(urllib.request.Request(u,headers=headers),timeout=30).read()
u=json.loads(fetch(f'https://api.github.com/users/{O}'));repos=json.loads(fetch(f'https://api.github.com/users/{O}/repos?per_page=100'));repos=[r for r in repos if not r['private']]
g=BeautifulSoup(fetch(f'https://github.com/users/{O}/contributions'),'html.parser');summary=' '.join(g.select_one('h2').get_text(' ',strip=True).split());days=sorted([{'date':x['data-date'],'level':int(x.get('data-level','0'))} for x in g.select('td.ContributionCalendar-day')],key=lambda x:x['date'])
assert days
num=int(re.search(r'[\d,]+',summary).group().replace(',',''));stars=sum(r['stargazers_count'] for r in repos)
archive=json.loads(fetch(f'https://api.github.com/repos/{O}/dsa-solutions/git/trees/main?recursive=1'))['tree']
practice={site:sum(x['path'].startswith(site+'/') and x['path'].endswith('.py') for x in archive) for site in ['leetcode','codeforces']}
state={'practice':practice,'design':6,'repos':u['public_repos'],'followers':u['followers'],'contributions':num,'days':days,'stars':stars,'languages':[[r['name'],r['language']] for r in repos]}
st=pathlib.Path('4-public-dashboard-data.json')
if st.exists() and json.loads(st.read_text())==state: print('Public data unchanged');raise SystemExit()
W=1000;mint='#88dec3';cyan='#57c0ca';font='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf';bold=font.replace('.ttf','-Bold.ttf')
def f(n,b=False):return ImageFont.truetype(bold if b else font,n)
def svg(name,h,content,light=False):
 bg,fg,mut,panel=('#eff8f4','#123f37','#4d7169','#e0f0e9') if light else ('#081817','#e0f6ee','#8cac9f','#102a27')
 s=f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{h}" viewBox="0 0 1000 {h}"><rect width="1000" height="{h}" rx="22" fill="{bg}"/><rect x="14" y="14" width="972" height="{h-28}" rx="17" fill="none" stroke="{mut}" opacity=".4"/><g font-family="monospace" fill="{fg}">{content.replace("$FG",fg).replace("$MUT",mut).replace("$PANEL",panel)}</g></svg>'
 if light:s=s.replace('#88dec3','#20745e').replace('#57c0ca','#287d85')
 (root/f'{name}-{"light" if light else "dark"}.svg').write_text(s)
def text(x,y,t,size=20,col='$FG',weight='normal'):return f'<text x="{x}" y="{y}" font-size="{size}" fill="{col}" font-weight="{weight}">{html.escape(t)}</text>'
for light in (False,True):
 c='<defs><radialGradient id="glow"><stop stop-color="#3bb995" stop-opacity=".4"/><stop offset="1" stop-color="#3bb995" stop-opacity="0"/></radialGradient></defs><ellipse cx="750" cy="140" rx="240" ry="170" fill="url(#glow)"/>'
 c+=text(55,63,'FIELD NOTES / SURYAKANT-SOURCE',15,'$MUT')+text(55,137,'Ideas into interfaces.',40,mint,'bold')+text(55,179,'One useful build at a time.',25)+text(55,251,'WEB  /  AUTOMATION  /  AGENTIC AI  /  RAG',15,'$MUT')
 # Original isometric workspace scene
 for i,(x,y,h) in enumerate([(680,188,100),(755,185,125),(840,190,75)]):
  c+=f'<path d="M{x},{y} l45,-25 l45,25 v{h} l-45,25 l-45,-25 Z" fill="$PANEL" stroke="{cyan}"/><path d="M{x},{y} l45,25 l45,-25 M{x+45},{y+25} v{h}" fill="none" stroke="{mint}" opacity=".7"/>'
 c+='<path d="M610 305 Q770 345 935 300" fill="none" stroke="#88dec3" stroke-dasharray="5 8"/>'
 svg('hero',365,c,light)
 c=text(40,53,'IN THE CURRENT CUT',15,'$MUT')
 for j,(a,b) in enumerate([('01 / WEB','React + Next.js interfaces'),('02 / AI','Automation, agentic AI and RAG'),('03 / PRACTICE','Python DSA + Java programming')]):
  x=42+j*322;c+=f'<rect x="{x}" y="83" width="300" height="125" rx="12" fill="$PANEL"/>'+text(x+17,119,a,18,mint,'bold')+text(x+17,154,b,13)+text(x+17,185,'Personal projects / learning',12,'$MUT')
 svg('highlights',240,c,light)
 c=text(42,53,'PRODUCTION PALETTE',15,'$MUT')
 for j,t in enumerate(['React','Next.js','TypeScript','AI automation','Agentic AI','RAG','Python','Java']):
  x=42+(j%4)*238;y=85+(j//4)*84;c+=f'<rect x="{x}" y="{y}" width="220" height="63" rx="10" fill="$PANEL" stroke="#477e70"/>'+text(x+15,y+39,t,18)
 c+=text(42,279,'Tools used in projects and practice, not a proficiency rating.',14,'$MUT');svg('stack',310,c,light)
 c=text(42,53,'FEATURED REEL / PERSONAL WORK',15,'$MUT')
 for j,(a,b) in enumerate([('promptforge-ai','Prompt UI prototype'),('dsa-solutions','AI-assisted Python practice'),('JAVA-Programming','Java practice archive'),('C-programming','C programming archive')]):
  x=42+(j%2)*476;y=83+(j//2)*105;c+=f'<rect x="{x}" y="{y}" width="454" height="86" rx="12" fill="$PANEL"/>'+text(x+18,y+32,a,20,mint,'bold')+text(x+18,y+61,b,15,'$MUT')
 svg('projects',315,c,light)
 c=text(42,49,'PUBLIC SIGNAL / ROLLING YEAR',15,'$MUT')+text(42,101,f'{u["public_repos"]} repos   /   {num} contributions   /   {u["followers"]} follower   /   {stars} stars',23)
 c+=text(42,139,'Public-only snapshot. Private activity is excluded.',14,'$MUT');svg('stats',168,c,light)
from collections import Counter
counts=Counter(r.get('language') or 'Unset' for r in repos)
for light in (False,True):
 c=text(42,49,'LANGUAGE SIGNAL / PUBLIC REPOSITORY COUNT',15,'$MUT')
 total=len(repos)
 for j,(name,count) in enumerate(counts.most_common()):
  x=42+(j%2)*478;y=90+(j//2)*51
  c+=text(x,y,f'{name}  {count}/{total}',16)+f'<rect x="{x+200}" y="{y-13}" width="210" height="12" rx="6" fill="$PANEL"/><rect x="{x+200}" y="{y-13}" width="{210*count/total}" height="12" rx="6" fill="#88dec3"/>'
 c+=text(42,307,'Primary language per repo. Not coding time or proficiency.',14,'$MUT');svg('languages',338,c,light)
 c=text(42,49,'PRACTICE LOG / REAL SOURCE ARCHIVE',15,'$MUT')+text(42,113,f"{practice['leetcode']} LeetCode files  /  {practice['codeforces']} Codeforces files",27)
 c+=text(42,164,'Python / AI-assisted practice / original source uploads',16)+text(42,205,'Archive counts only. Not total judge solves, contest rating or unaided skill.',13,'$MUT');svg('practice',238,c,light)
# Animated ASCII name drawn as actual sampled glyph pixels
mask=Image.new('L',(1000,125));md=ImageDraw.Draw(mask);md.text((48,8),'SURYAKANT SAHOO',font=f(100,True),fill=255)
frames=[]
for k in range(20):
 im=Image.new('RGB',(1000,145),'#081817');d=ImageDraw.Draw(im)
 for y in range(10,120,8):
  for x in range(40,950,7):
   if mask.getpixel((x,y))>100:d.text((x,y),'+' if (x//7+y//8)%3 else ':',font=f(10),fill=mint if abs(x-k*50)<90 else '#467f6f')
 frames.append(im)
frames[0].save(root/'wordmark.gif',save_all=True,append_images=frames[1:],duration=[1600]+[100]*19,loop=0,optimize=True)
# Two original animations using the exact public contribution day levels
colors=['#173c35','#2b6653','#419175','#6bb99b','#9aebca'];start=datetime.date.fromisoformat(days[0]['date']);cells=[]
for day in days:
 delta=(datetime.date.fromisoformat(day['date'])-start).days;cells.append((40+(delta//7)*17,85+(delta%7)*22,day['level'],day['date']))
active=[i for i,c in enumerate(cells) if c[2]];targets=active[::max(1,len(active)//12)][:12]
def board(title,h=335):
 im=Image.new('RGB',(1000,h),'#081817');d=ImageDraw.Draw(im);d.rounded_rectangle((8,8,991,h-9),20,outline='#386b5c',width=2);d.text((40,30),title,font=f(21,True),fill=mint);return im,d
frames=[]
for k in range(96):
 im,d=board('ORBIT / CONTRIBUTION TARGETS',365);idx=min(k//8,len(targets)-1);phase=k%8;target=targets[idx];tx,ty,lv,dt=cells[target];destroyed=set(targets[:idx])
 for i,(x,y,l,dd) in enumerate(cells):
  if i not in destroyed and not (i==target and phase>5):d.rounded_rectangle((x,y,x+11,y+13),3,fill=colors[l])
 px=tx+5;py=285;d.polygon([(px,py-17),(px-13,py+12),(px,py+6),(px+13,py+12)],fill=mint);d.polygon([(px-5,py+13),(px,py+22+(k%3)*3),(px+5,py+13)],fill=cyan)
 if phase<6:
  by=py-25-(py-ty-30)*phase/5;d.line((px,by+12,px,by),fill='#effff6',width=3)
 else:
  r=9+(phase-6)*6
  for a in range(8):
   an=a*math.pi/4;d.line((px+math.cos(an)*r*.5,ty+6+math.sin(an)*r*.5,px+math.cos(an)*r,ty+6+math.sin(an)*r),fill=cyan,width=2)
 d.text((40,328),f'ANIMATED DEMO  /  Target day: {dt}  /  Not playable in README',font=f(14),fill='#8cac9f');frames.append(im)
frames[0].save(root/'shooter.gif',save_all=True,append_images=frames[1:],duration=[1800]+[90]*95,loop=0,optimize=True)
frames[46].save('/tmp/shooter-preview.png')
def pic(n,alt):return f'<picture><source media="(prefers-color-scheme: light)" srcset="assets-v3/{n}-light.svg"><img src="assets-v3/{n}-dark.svg" width="100%" alt="{alt}"></picture>'
def div():return '\n<p align="center">─────── ◇ ───────</p>\n'
links='<a href="https://suryakant-sahoo-portfolio.netlify.app/">Portfolio</a> · <a href="https://suryakant16-portfolio.netlify.app/">AI demos</a> · <a href="https://www.linkedin.com/in/suryakant-sahoo19/">LinkedIn</a> · <a href="mailto:xbsuryakant@gmail.com">Email</a>'
s='<div align="center">\n<p><sub>FIELD NOTES / SURYAKANT SAHOO</sub></p>\n'+pic('hero','Original mint city-of-ideas scene')+'\n<img src="assets-v3/wordmark.gif" width="100%" alt="Suryakant Sahoo animated ASCII name">\n<p><strong>Web + AI developer</strong> · Bhubaneswar, India</p>\n<p>Small steps. Honest work. Useful things.</p>\n<p>'+links+'</p>\n</div>\n'+div()
s+=f'<table width="100%"><tr><td width="58%" valign="top"><h2>The point of view</h2><blockquote>Small steps. Honest work. Useful things.</blockquote><p>I build web interfaces, AI automations, agentic AI and RAG projects. I use AI coding tools and keep learning through practice.</p><p>Open to remote roles and freelance projects.</p></td><td width="42%" valign="top"><code>PROFILE</code><p>ROLE · Web + AI developer<br>BASED · Bhubaneswar, India<br>FOCUS · Automation / Agentic AI / RAG</p><p>{u["public_repos"]} public repos<br>{num} public contributions<br>{u["followers"]} follower</p></td></tr></table>\n'+div()
s+='<h2>In the current cut</h2>\n'+pic('highlights','Web, AI and programming practice highlights')+div()+'<h2>Production palette</h2>\n'+pic('stack','Project and practice tools')+div()+'<h2>Language signal</h2>\n'+pic('languages','Public primary-language repository breakdown')+'<h2>Practice log</h2>\n'+pic('practice','Real archived LeetCode and Codeforces source counts')+'<p><a href="https://github.com/suryakant-source/dsa-solutions">Browse the source archive</a></p>'+div()+'<h2>Featured reel</h2>\n'+pic('projects','Four personal repository cards')+'\n<table width="100%"><tr>'
for name,desc in [('promptforge-ai','Next.js prompt UI prototype. Preset demo, not live generation.'),('dsa-solutions','AI-assisted LeetCode and Codeforces Python archive.'),('JAVA-Programming','Java programming practice.'),('C-programming','C programming practice.')]:
 r=next(r for r in repos if r['name']==name);s+=f'<td width="25%" valign="top"><strong><a href="{r["html_url"]}">{name}</a></strong><p>{desc}</p><sub>{r["language"] or "Practice"}</sub></td>'
s+='</tr></table>\n<p><sub>Personal demos and practice, not paid client-work claims.</sub></p>\n'+div()+pic('stats','Public repository, contribution, follower and star snapshot')+div()+'<h2>Play the next move</h2>\n<img src="assets-v3/shooter.gif" width="100%" alt="Original auto-playing space shooter targeting public contribution cells">\n<p><sub>Original auto-playing animated demo, not an interactive game. Targets use real public contribution day levels. The animation does not change GitHub activity.</sub></p>\n'+div()+'<div align="center"><sub>THE NEXT SCENE</sub><h2>Keep the story moving</h2><p>Have an idea for a useful website or automation? Get in touch.</p><p>'+links+'</p><p><sub>Original self-hosted profile assets. Public snapshots refresh daily only when data changes.</sub></p></div>\n'
mapping={'hero-dark.svg':'1-hero-dark.svg','hero-light.svg':'2-hero-light.svg','highlights-dark.svg':'3-highlights-dark.svg','highlights-light.svg':'4-highlights-light.svg','projects-dark.svg':'5-projects-dark.svg','projects-light.svg':'6-projects-light.svg','shooter.gif':'15-shooter-start.gif','stack-dark.svg':'8-stack-dark.svg','stack-light.svg':'9-stack-light.svg','stats-dark.svg':'10-stats-dark.svg','stats-light.svg':'11-stats-light.svg','wordmark.gif':'14-wordmark-start.gif'}
for a,b in mapping.items():
 s=s.replace('assets-v3/'+a,'assets-v3/'+b);(root/a).rename(root/b)
for stale in ['12-trail.gif','7-shooter.gif','13-wordmark.gif']: (root/stale).unlink(missing_ok=True)
pathlib.Path('README.md').write_text(s);st.write_text(json.dumps(state,indent=2));print('Generated original scene, wordmark, cards, trail and shooter')
