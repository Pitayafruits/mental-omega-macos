from pathlib import Path
import struct,math,shutil,re
from PIL import Image,ImageDraw,ImageFont
import argparse
parser=argparse.ArgumentParser(description='Translate common Mental Omega launcher controls and generate Chinese sprite fonts.')
parser.add_argument('game_dir',type=Path)
args=parser.parse_args()
game=args.game_dir.resolve();res=game/'Resources'

pairs={'Campaign':'战役','Skirmish':'遭遇战','Multiplayer':'多人游戏','LAN':'局域网','Load Game':'读取存档','Options':'设置','Map Editor':'地图编辑器','Statistics':'战绩统计','Quit Game':'退出游戏','Credits':'资金','MODE:':'模式：','Random Map':'随机地图','SUBFACTION':'阵营','LOC':'位置','Cancel':'取消','SETTINGS':'设置','Unit Count':'初始单位','Tech Level':'科技等级','Game Speed':'游戏速度','Ore Growth':'矿石生长','Tech Defense':'科技防御','Superweapons':'超级武器','Short Game':'快速游戏','MCV Repacks':'基地可重新部署','Stolen Tech Units':'渗透科技单位','No Naval Combat':'禁止海军','Mental AI Boost':'强化电脑','Immune Oil Derricks':'油井无敌','No Spawn Previews':'隐藏出生点预览','Build Off Ally Bases':'可在盟友基地旁建造','Ally Change Ingame':'允许中途更换盟友','Crates Appear':'随机工具箱','No Garrisons':'禁止驻军','Limited MCV':'限制基地车','Permanent Radar':'永久雷达','ConYard Start':'建筑基地开局','Global Soundtrack':'原版音乐','Extra Saved Game Fixes':'存档兼容修复','Soundtrack':'游戏音乐'}
chars=set(chr(i) for i in range(32,256))
for p in res.glob('*.ini'):
 lines=[]
 for line in p.read_text(encoding='utf-8-sig').splitlines():
  m=re.match(r';?Text=(.*)',line)
  if m and m[1] in pairs:line='Text='+pairs[m[1]]
  if line.startswith('Items=6 Fastest,'):line='Items=6 最快,5 较快,4 快,3 中等,2 慢,1 较慢,0 最慢'
  lines.append(line);chars.update(c for c in line if '\u4e00'<=c<='\u9fff' or c in '：，（）')
 p.write_text('\n'.join(lines)+'\n',encoding='utf-8-sig')
# The original main-menu button images contain English text.
for name in ['campaign','skirmish','cncnet','lan','loadmission','options','mapeditor','statistics','exitgame','credits']:
 for suffix,asset in [('', '133pxbtn.png'),('_c','133pxbtn_c.png')]:
  target=res/'MainMenu'/f'{name}{suffix}.png'
  if target.exists():shutil.copy2(res/asset,target)
p=res/'MainMenu.ini'
s=p.read_text(encoding='utf-8-sig')
s=re.sub(r'(?ms)(\[btnCredits\]\n.*?^Text=)[^\n]*',r'\g<1>制作名单',s)
p.write_text(s,encoding='utf-8-sig')
chars.update('制作名单')
chars=sorted(chars);n=len(chars)
def vi(v):
 b=bytearray()
 while v>127:b.append((v&127)|128);v>>=7
 return bytes(b)+bytes([v])
def st(s):b=s.encode();return vi(len(b))+b
def I(*v):return struct.pack('<'+'i'*len(v),*v)
def F(*v):return struct.pack('<'+'f'*len(v),*v)
readers=['SpriteFontReader','Texture2DReader','ListReader`1[[Microsoft.Xna.Framework.Rectangle, MonoGame.Framework]]','ListReader`1[[System.Char, mscorlib]]','ListReader`1[[Microsoft.Xna.Framework.Vector3, MonoGame.Framework]]']
readers+=['RectangleReader','CharReader','Vector3Reader']
for index,size in enumerate([14,13,14,18,12,14]):
 font=ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc',size)
 cell=size+5;cols=32;width=cols*cell;height=math.ceil(n/cols)*cell
 image=Image.new('RGBA',(width,height));draw=ImageDraw.Draw(image);glyphs=[];crops=[];kern=[]
 for j,c in enumerate(chars):
  x=j%cols*cell;y=j//cols*cell;advance=max(1,int(math.ceil(font.getlength(c))))
  draw.text((x,y),c,font=font,fill=(255,255,255,255),anchor='lt')
  glyphs.append((x,y,cell-1,cell-1));crops.append((0,0,cell-1,cell-1));kern.append((0.,float(advance),0.))
 raw=bytearray(image.tobytes())
 for j in range(0,len(raw),4):raw[j:j+3]=bytes([raw[j+3]])*3
 body=vi(len(readers))+b''.join(st('Microsoft.Xna.Framework.Content.'+s+', MonoGame.Framework')+I(0) for s in readers)+vi(0)
 body+=vi(1)+vi(2)+I(0,width,height,1,len(raw))+raw
 for entries in [glyphs,crops]:body+=vi(3)+I(n)+b''.join(I(*v) for v in entries)
 body+=vi(4)+I(n)+''.join(chars).encode('utf-8')+I(size+4)+F(0.)
 body+=vi(5)+I(n)+b''.join(F(*v) for v in kern)+b'\x01?'
 data=b'XNBw\x05\x00'+I(10+len(body))+body
 (res/f'SpriteFont{index}.xnb').write_bytes(data)
print('Installed official game translation and localized common lobby controls; Chinese-capable fonts:',n,'glyphs')
