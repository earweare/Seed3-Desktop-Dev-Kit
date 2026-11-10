"""Seed3 Desktop Rev4: millimetres, PCB lower-left origin, Z up.
Run from project root: python enclosure/build.py. cadquery 2.x, sexpdata.
Geometry provenance is emitted per component. Unknown MPNs are NOT certified.
"""
import cadquery as cq, sexpdata as sx, pathlib as P, math,json,csv,time
ROOT=P.Path(__file__).resolve().parent;OUT=ROOT/'deliverable';OUT.mkdir(exist_ok=True)
PCB=P.Path('seed3-hardware/pcb/Seed3-DevKit-Desktop/Seed3-DevKit-Desktop.kicad_pcb')
a=sx.loads(PCB.read_text())
def tag(x):return str(x[0]) if isinstance(x,list) and x else ''
def sub(x,t):return [y for y in x if tag(y)==t]
def one(x,t,d=None):return next(iter(sub(x,t)),d)
def prop(f):return {str(v[1]):str(v[2]) for v in sub(f,'property')}
F={prop(f).get('Reference'):f for f in sub(a,'footprint')}
def pos(r):
 v=one(F[r],'at')[1:];return (float(v[0])-50,155-float(v[1]),float(v[2]) if len(v)>2 else 0)
ZPCB=8;ZT=9.6
C={ 'pcb':(0.035,.055,.05), 'black':(.07,.075,.08),'metal':(.65,.68,.7),'gold':(.75,.54,.16),'yellow':(.85,.78,.10),'blue':(.08,.3,.55),'case':(.16,.18,.20),'lid':(.32,.36,.39),'amber':(.9,.42,.07)}
parts=[];rows=[]
def box(x0,y0,z0,x1,y1,z1):return cq.Solid.makeBox(x1-x0,y1-y0,z1-z0,cq.Vector(x0,y0,z0))
def cyl(x,y,z,r,h):return cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z))
def compound(xs):return cq.Compound.makeCompound(xs)
def add(name,s,col='black',status='',src=''):
 parts.append((name,s,C.get(col,col)));rows.append({'reference':name,'geometry':status,'source':src});return s

def rbox(x0,y0,z0,x1,y1,z1,r=2.5):
 return cq.Workplane('XY').box(x1-x0,y1-y0,z1-z0).edges('|Z').fillet(r).val().translate(((x0+x1)/2,(y0+y1)/2,(z0+z1)/2))
board=rbox(0,0,ZPCB,197,111,ZT,2.5)
for r in ['H1','H2','H3','H4']:
 x,y,_=pos(r);board=board.cut(cyl(x,y,7,1.75,4))
add('PCB_197x111x1_6',board,'pcb','Exact Edge.Cuts and thickness','KiCad Rev4')
for r in ['H1','H2','H3','H4']:
 x,y,_=pos(r);add(r+'_plating',cyl(x,y,ZT,3.5,.035).cut(cyl(x,y,ZT-.01,1.75,.1)),'gold','KiCad mounting pad')
# Standard KiCad component STEP models; all placements are from the PCB, not centroid CSV.
cache={}
def load(p):
 p=str(p)
 if p not in cache:cache[p]=cq.importers.importStep(p).val()
 return cache[p]
def place(s,r):
 x,y,ang=pos(r);return s.rotate((0,0,0),(0,0,1),ang).translate((x,y,ZT))
custom=set(['A1','RV1','J7','MICRO_SD7','J5','L2','U1']+[f'J{i}' for i in [1,2,3,4,8,10,11]]+[f'VR{i}' for i in range(1,9)]+[f'S{i}' for i in range(1,17)]+['SW17','SW18']+[r for r in F if r.startswith(('J_CV','J_GATE'))])
for r,f in F.items():
 if r in custom or r.startswith(('H','FD')):continue
 models=sub(f,'model')
 if not models:continue
 rel=str(models[0][1]).split('}/')[-1];p=ROOT/'models'/rel
 if not p.exists():continue
 s=place(load(p),r)
 col='yellow' if r.startswith('D') and r[1:].isdigit() and int(r[1:])<=16 else ('metal' if 'CP_Elec' in rel else 'black')
 add(r,s,col,'Standard KiCad STEP; nominal package envelope',rel)
print('standard parts',len(parts),flush=True)
# Exact manufacturer jack STEP. Original axes: X width, Y height, Z depth.
j=load(ROOT/'models/NMJ6HCD2.stp').rotate((0,0,0),(1,0,0),90).rotate((0,0,0),(0,0,1),180)
for r in ['J1','J2','J3','J4']:
 x,y,_=pos(r);add(r,j.translate((x+8.115,y+16.7,ZT)),'metal','Manufacturer STEP, aligned to drawing pin layout','Neutrik NMJ6HCD2')
# DIN envelope reconstructed from Switchcraft drawing; no hidden contact spring detail.
for r in ['J8','J10','J11']:
 x,y,_=pos(r)
 b=box(x-5,y-10,ZT,x+12,y+10,ZT+21)
 bore=cq.Solid.makeCylinder(7.8,4,cq.Vector(x+9,y,ZT+10),cq.Vector(1,0,0));b=b.cut(bore)
 add(r,b,'black','Drawing-based exterior, connector contacts simplified','Switchcraft 57PC5F drawing')
 for k in range(5):
  an=math.radians(30+30*k);py=y+4*math.cos(an);pz=ZT+10+4*math.sin(an)
  add(r+'_contact'+str(k),cq.Solid.makeCylinder(.65,2,cq.Vector(x+9.1,py,pz),cq.Vector(1,0,0)),'metal','Visual contact representation')
# Pots: inferred R0904N KQ-type from photo (round knurled shaft, white pointer).
# Exact suffix remains unknown; manufacturer family drawing constrains the body.
for i in range(1,9):
 r=f'VR{i}';x,y,_=pos(r)
 add(r,box(x-4.65,y-5.9,ZT,x+4.65,y+5.4,ZT+6.8),'blue','Inferred Song Huei R0904N family; body height 6.8 mm','R0904N drawing R09N-003; actual MPN unconfirmed')
 cover=box(x-4.65,y-5.9,ZT+6.8,x+4.65,y+5.4,ZT+7.6)
 for dx,dy in [(-3.6,4.2),(3.6,-4.7)]:cover=cover.cut(cyl(x+dx,y+dy,ZT+6.7,.65,1))
 add(r+'_cover',cover,'metal','0.8 mm nominal cover, visual body details','R0904N family drawing and photo')
 sh=cyl(x,y,ZT+7.6,3,17.4)
 for k in range(40):
  an=math.radians(k*9);sh=sh.cut(cyl(x+3*math.cos(an),y+3*math.sin(an),ZT+18,.10,7.1))
 add(r+'_shaft',sh,'black','Round knurled KQ shaft D6; total L25 inferred from calibrated oblique photo, not measured','Photo white pointer + R0904N shaft variants')
 add(r+'_pointer',box(x-.25,y-2.65,ZT+24.99,x+.25,y-.8,ZT+25.01),(.9,.88,.78),'Visual white pointer observed in photo')
# Tact switches, manufacturer drawing height 7.50 mm; caps not present on bare board.
for i in range(1,17):
 r=f'S{i}';x,y,_=pos(r)
 add(r,box(x-3,y-3,ZT,x+3,y+3,ZT+3.6),'black','Drawing-based envelope','E-Switch TL1105SPF250Q drawing')
 add(r+'_cover',box(x-2.9,y-2.9,ZT+3.6,x+2.9,y+2.9,ZT+3.9),'metal','Drawing-based cover envelope')
 add(r+'_actuator',cyl(x,y,ZT+3.6,1.75,1.1).fuse(box(x-1.4,y-1.4,ZT+4.7,x+1.4,y+1.4,ZT+7.5)),'yellow','Actuator height 7.5 mm; square head 2.8 mm','E-Switch drawing')
# CV/GATE unspecified MPN. XY footprint exact, nominal PJ301-style vertical stack.
for r in F:
 if not r.startswith(('J_CV','J_GATE')):continue
 x,y,_=pos(r)
 add(r,box(x-4.5,y-4.5,ZT,x+4.5,y+6,ZT+10),'black','XY footprint exact; body height 10 mm ASSUMPTION','No manufacturer MPN in BOM')
 b=cyl(x,y,ZT+10,3,5).cut(cyl(x,y,ZT+9.9,1.8,6))
 add(r+'_bushing',b,'metal','Inferred PJ301M-12/WQP518MA family: barrel D6 x5; oblique-photo estimated total height about15mm, MPN unconfirmed')
for r in ['SW17','SW18']:
 x,y,_=pos(r)
 add(r,box(x-2.54,y-4.065,ZT,x+2.54,y+4.065,ZT+8.64),(.55,.035,.035),'Inferred Dailywell 2M SPDT family: 5.08 x8.13 x8.64 mm','Manufacturer 2M drawing; matching pin pitch, MPN unconfirmed')
 add(r+'_cover',box(x-2.54,y-4.065,ZT+7.84,x+2.54,y+4.065,ZT+8.64),'metal','Metal cover over red housing observed in photo')
 bush=cyl(x,y,ZT+8.64,3,5.59)
 lever=cyl(x,y,ZT+14.23,1.27,8.13).fuse(cq.Solid.makeSphere(1.27,cq.Vector(x,y,ZT+22.36)))
 if r=='SW17':lever=lever.rotate((x,y,ZT+14.23),(x+1,y,ZT+14.23),15)
 add(r+'_lever',bush.fuse(lever),'metal','B1 bushing 5.59 mm; T1 lever 9.4 mm nominal','Dailywell 2M family drawing; inferred variant')
# Thumbwheel RK10J12R nominal dual SMD; diameter from footprint and ALPS drawing.
x,y,_=pos('RV1')
add('RV1_body',box(x-8,y-5.2,ZT,x+3,y+5.2,ZT+3.8),'metal','ALPS family drawing; exact suffix not in BOM','RK10J12R')
wheel=cyl(x,y,ZT+3.8,7,.9)
for k in range(48):
 an=math.radians(k*7.5);wheel=wheel.cut(cyl(x+7*math.cos(an),y+7*math.sin(an),ZT+3.7,.23,1.2))
add('RV1_wheel',wheel,'black','14 mm wheel; 4.7 mm total nominal','ALPS RK10J12R drawing')
# Low-profile headphone connector envelope (6 x 14.5, 5 mm height); barrel projects forward.
x,y,_=pos('J5')
hp=box(x-3,y-6,ZT,x+3,y+8.5,ZT+5)
hp=hp.fuse(cq.Solid.makeCylinder(2.5,2.5,cq.Vector(x,y-6,ZT+2.5),cq.Vector(0,-1,0)))
hp=hp.cut(cq.Solid.makeCylinder(1.8,5,cq.Vector(x,y-9,ZT+2.5),cq.Vector(0,1,0)))
add('J5',hp,'black','XY footprint; height 5 mm nominal package','CUI SJ-3523-SMT footprint')
# USB and microSD native local STEP files supplied by PCB designer.
for r,path in [('J7','libs/USB4110GFA.step'),('MICRO_SD7','libs/TF-01A/TF-01A.step')]:
 s=load(PCB.parent/path)
 s=s.rotate((0,0,0),(1,0,0),90)
 if r=='MICRO_SD7':s=s.translate((-1,-3.6,-.1))
 add(r,place(s,r),'metal','STEP supplied with hardware project',path)
# Small packages lacking standard STEP.
x,y,_=pos('L2');add('L2',box(x-3,y-3,ZT,x+3,y+3,ZT+4.5),'black','6 x 6 x 4.5 nominal package','TDK VLS6045')
x,y,_=pos('U1');add('U1',box(x-1.5,y-1.5,ZT,x+1.5,y+1.5,ZT+1.1),'black','3 x 3 nominal body','HVSSOP8')
# Actual Seed3 STEP, NOT the legacy Daisy Seed model named by old footprint.
print('loading official Seed3',flush=True)
seed=load(ROOT/'models/Seed3-models/ES_Daisy_Seed3_Rev5.step')
seed=seed.rotate((0,0,0),(0,0,1),-90).translate((1.366,46.354,ZT+11.5))
add('A1_Seed3_official',seed,'black','Official Seed3 Rev5 STEP; socket stack11.5mm inferred from oblique photo (estimated11.67mm)','Daisy Seed3-models.zip')
for yy in [29.705,44.945]:
 add('A1_socket_'+str(yy),box(1.525,yy-1.27,ZT,52.325,yy+1.27,ZT+8.5),'black','Socket stack inferred; module removable','2 x 20 pin 2.54 mm')
print('all board parts',len(parts),flush=True)
# Named STEP assembly and reusable BREP caches.
assembly=cq.Assembly(name='Seed3_Desktop_Rev4_reconstruction')
for name,s,col in parts:assembly.add(s,name=name,color=cq.Color(*col))
assembly.save(str(OUT/'Carte_Seed3_peuplee.step'))
compound([s for _,s,_ in parts]).exportBrep(str(ROOT/'board.brep'))
# Component STLs for deterministic Blender rendering (no generative imaging).
meshdir=ROOT/'meshes';meshdir.mkdir(exist_ok=True)
manifest=[]
for name,s,col in parts:
 s.exportBrep(str(meshdir/(name+'.brep')))
 path=meshdir/(name+'.stl');cq.exporters.export(s,str(path),tolerance=.10,angularTolerance=.25)
 manifest.append({'name':name,'file':str(path),'color':col})
(ROOT/'render_manifest.json').write_text(json.dumps(manifest))
with (OUT/'Provenance_composants.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['reference','geometry','source']);w.writeheader();w.writerows(rows)
# Exact XY table includes every footprint and all mounting centers.
with (OUT/'Implantation_KiCad_mm.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['reference','x_from_left_mm','y_from_front_mm','rotation_deg','footprint'])
 for r in sorted(F):w.writerow([r,*pos(r),F[r][1]])
print('BOARD SAVED',flush=True)
