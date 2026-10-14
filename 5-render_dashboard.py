from PIL import Image,ImageDraw,ImageFont,ImageFilter
import json,math,datetime
import urllib.request, pathlib, collections, os
from bs4 import BeautifulSoup
owner=os.environ.get('GITHUB_REPOSITORY_OWNER','suryakant-source')
def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'public-profile-dashboard'}),timeout=30).read()
user=json.loads(fetch(f'https://api.github.com/users/{owner}'))
repos=json.loads(fetch(f'https://api.github.com/users/{owner}/repos?per_page=100'))
repos=[r for r in repos if not r.get('private')]
counts=collections.Counter(r.get('language') or 'Unset' for r in repos)
html=BeautifulSoup(fetch(f'https://github.com/users/{owner}/contributions'),'html.parser')
graph={'summary':' '.join(html.select_one('h2').get_text(' ',strip=True).split()),'days':[{'date':x.get('data-date'),'level':int(x.get('data-level','0'))} for x in html.select('td.ContributionCalendar-day')]}
if not graph['days']:raise RuntimeError('No contribution data')
state={'public_repos':user['public_repos'],'followers':user['followers'],'following':user['following'],'languages':dict(counts),'graph':graph,'avatar':user['avatar_url']}
statepath=pathlib.Path('4-public-dashboard-data.json')
if statepath.exists() and json.loads(statepath.read_text())==state:
    print('Public data unchanged; no new images.');raise SystemExit(0)
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%d %b %Y')
pathlib.Path('avatar.png').write_bytes(fetch(user['avatar_url']))
pathlib.Path('graph.json').write_text(json.dumps(graph))
W=900;bg='#090f14';panel='#0e201f';mint='#8de0c0';cyan='#62bfc8';ink='#e6f3ef';sub='#88a49d'
font='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf';bold='/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
def f(n,b=False):return ImageFont.truetype(bold if b else font,n)
def card(h,title,label):
 im=Image.new('RGB',(W,h),bg);d=ImageDraw.Draw(im)
 d.rounded_rectangle((8,8,W-9,h-9),radius=22,fill=panel,outline='#456f62',width=2)
 d.rounded_rectangle((20,20,W-21,h-21),radius=14,fill='#0b171a',outline='#25473f')
 for i,c in enumerate(['#ed8d84','#d7c280','#83cfb0']):d.ellipse((38+18*i,34,45+18*i,41),fill=c)
 d.text((115,29),label,font=f(12),fill=sub);d.text((38,63),title,font=f(25,True),fill=ink)
 return im
av=Image.open('avatar.png').convert('L').resize((42,28));chars=' .:-=+*#%@';frames=[]
for k in range(28):
 im=card(430,'Profile scan','SURYAKANT-SOURCE  /  IDENTITY PANEL');d=ImageDraw.Draw(im)
 d.rounded_rectangle((37,110,410,398),radius=12,outline='#456f62',fill='#0b1c1d')
 for y in range(28):
  line=''.join(chars[av.getpixel((x,y))*9//256] for x in range(42))
  d.text((48,118+y*9.5),line,font=f(12),fill='#75b398')
 sy=119+k*9.5;d.rectangle((42,sy,405,sy+5),fill='#aceed5')
 d.text((449,118),'SURYAKANT',font=f(34,True),fill=mint);d.text((449,160),'SAHOO',font=f(34,True),fill=ink)
 rows=[('ROLE','Web developer'),('STACK','React / Next.js / TypeScript'),('WORKFLOW','AI-assisted development'),('FOCUS','Interfaces + personal demos'),('OPEN TO','Remote roles / freelance'),('PUBLIC REPOS',str(user['public_repos'])),('FOLLOWERS',str(user['followers']))]
 for j,(a,b) in enumerate(rows):
  yy=218+j*23;d.text((449,yy),a,font=f(11),fill=sub);d.text((567,yy),b,font=f(12),fill=ink)
 frames.append(im)
frames[0].save('1-scan.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True);frames[14].save('/tmp/dashboard-scan-preview.png')
g=json.load(open('graph.json'));days=sorted(g['days'],key=lambda x:x['date']);start=datetime.date.fromisoformat(days[0]['date']);frames=[]
for k in range(38):
 im=card(315,'The year, so far','PUBLIC GITHUB ACTIVITY  /  FLIGHT PATH');d=ImageDraw.Draw(im)
 d.text((38,100),g['summary'],font=f(14),fill=sub)
 colors=['#162e2c','#285549','#43876b','#69b991','#a0e6c2']
 for x in days:
  delta=(datetime.date.fromisoformat(x['date'])-start).days;cx=42+(delta//7)*15;cy=140+(delta%7)*15
  d.rounded_rectangle((cx,cy,cx+10,cy+10),radius=2,fill=colors[x['level']])
 px=48+k*21;py=252+int(8*math.sin(k/5));d.line((max(38,px-65),py,px,py),fill=cyan,width=1)
 d.polygon([(px+15,py),(px-4,py-7),(px-1,py-2),(px-13,py-2),(px-13,py+2),(px-1,py+2),(px-4,py+7)],fill='#eefaf6')
 d.text((38,278),f'Real contribution cells. Jet is decorative. Snapshot: {stamp}.',font=f(11),fill=sub)
 frames.append(im)
frames[0].save('2-flight.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True);frames[15].save('/tmp/dashboard-flight-preview.png')
im=card(340,'Profile signal','PUBLIC REPOSITORIES  /  VERIFIED SNAPSHOT');d=ImageDraw.Draw(im)
for j,(a,b) in enumerate([('PUBLIC REPOS',str(user['public_repos'])),('FOLLOWERS',str(user['followers'])),('FOLLOWING','1')]):
 d.text((45,130+j*58),b,font=f(30,True),fill=mint);d.text((110,139+j*58),a,font=f(13),fill=sub)
langs=[(a,counts.get(a,0)) for a in ['TypeScript','Java','C']];langs.append(('Other / unset',len(repos)-sum(x[1] for x in langs)));colors=[mint,cyan,'#c5c999','#385950'];a=-90
for (label,count),c in zip(langs,colors):
 d.arc((424,116,592,284),start=a,end=a+360*count/len(repos)-3,fill=c,width=20);a+=360*count/len(repos)
for j,((label,count),c) in enumerate(zip(langs,colors)):
 d.rectangle((633,137+j*35,641,145+j*35),fill=c);d.text((650,133+j*35),f'{label}: {count}/{len(repos)}',font=f(13),fill=ink)
d.text((38,301),f'Primary language by public repo count, not proficiency. Updated {stamp}.',font=f(11),fill=sub)
im.save('3-signal.png');im.save('/tmp/dashboard-signal-preview.png')
print('preview assets generated')

statepath.write_text(json.dumps(state,indent=2))
pathlib.Path('avatar.png').unlink(missing_ok=True)
pathlib.Path('graph.json').unlink(missing_ok=True)
