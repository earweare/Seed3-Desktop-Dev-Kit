import cadquery as cq, pathlib as P,json,csv,math,trimesh
ROOT=P.Path(__file__).resolve().parent;OUT=ROOT/'deliverable'
def box(x0,y0,z0,x1,y1,z1):return cq.Solid.makeBox(x1-x0,y1-y0,z1-z0,cq.Vector(x0,y0,z0))
def cyl(x,y,z,r,h):return cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z))
def rbox(x0,y0,z0,x1,y1,z1,r):return cq.Workplane('XY').box(x1-x0,y1-y0,z1-z0).edges('|Z').fillet(r).val().translate(((x0+x1)/2,(y0+y1)/2,(z0+z1)/2))
coords={r['reference']:(float(r['x_from_left_mm']),float(r['y_from_front_mm'])) for r in csv.DictReader(open(OUT/'Implantation_KiCad_mm.csv'))}
ZT=9.6;LOW=24.0;HIGH=34.0;T=2.4;SPLIT=10.0
# 209 x 123 mm. Flat PCB, no fictitious sloped panel or relocated connector.
base=rbox(-6,-6,0,203,117,SPLIT,4)
base=base.cut(rbox(-1,-1,T,198,112,11,2.5))
for r in ['H1','H2','H3','H4']:
 x,y=coords[r];base=base.fuse(cyl(x,y,T,3.5,8-T));base=base.cut(cyl(x,y,1.2,1.3,7))
# Raised rear protection, with recessed CV field; raised MIDI side and Seed service area.
highzones=[(-6,71.5,75,117),(128,71.5,203,117),(75,105,128,117),(177,30,203,117)]
outer=rbox(-6,-6,SPLIT,203,117,LOW,4)
for x0,y0,x1,y1 in highzones:outer=outer.fuse(box(x0,y0,LOW-.1,x1,y1,HIGH))
# Ergonomic scallop around VR1: 45 degree conical relief, R7 at Z24 and R12.5 at Z29.5.
# Matching inner cone maintains a 2.4 mm normal wall thickness.
px,py=coords['VR1']
def relief(z0,z1,offset=0):
 return cq.Solid.makeCone(z0-17+offset,z1-17+offset,z1-z0,cq.Vector(px,py,z0))
SEED_HIGH=29.5
seed_outer=box(-6,23,LOW-.1,56,53,SEED_HIGH).cut(relief(LOW-.1,SEED_HIGH+.1))
outer=outer.fuse(seed_outer)
# Keep same external round corners through raised portions.
outer=outer.intersect(rbox(-6,-6,SPLIT,203,117,HIGH,4))
lid=outer.cut(rbox(-1,-1,SPLIT-.1,198,112,LOW-T,2.5))
# Interior raised cavities. These volumes overlap to avoid redundant internal walls.
for b in [( -1,74,72.6,112),(130.4,74,198,112),(72.6,107.4,130.4,112),(179.4,32.4,198,112)]:
 lid=lid.cut(box(*b[:2],LOW-T-.1,*b[2:],HIGH-T))
seed_inner=box(-1,25.4,LOW-T-.1,53.6,50.6,SEED_HIGH-T).cut(relief(LOW-T-.1,SEED_HIGH-T+.1,T*math.sqrt(2)))
lid=lid.cut(seed_inner)
# Outer-corner screw bosses independent of PCB mounting.
mounts=[(-2.5,-2.5,LOW),(199.5,-2.5,LOW),(-2.5,113.5,HIGH),(199.5,113.5,HIGH)]
for x,y,h in mounts:
 base=base.fuse(cyl(x,y,0,3.5,SPLIT)).cut(cyl(x,y,1.2,1.3,SPLIT))
 lid=lid.fuse(cyl(x,y,SPLIT,3.5,h-SPLIT)).cut(cyl(x,y,SPLIT-.1,1.7,h-SPLIT+.2)).cut(cyl(x,y,h-2,3.1,2.1))
# Connector openings shared between halves; generous rectangular service windows avoid
# imposing unknown barrel heights / panel nuts on board-mounted connectors.
cuts=[]
for r in ['J1','J2','J3','J4']:
 x,y=coords[r];cx=x+8.115
 cuts.append(box(cx-10.1,106.8,ZT-.5,cx+10.1,119,ZT+17.5))
for r in ['J8','J10','J11']:
 x,y=coords[r];cuts.append(box(195.5,y-10.8,ZT-.5,205,y+10.8,ZT+22))
# USB main, Seed service USB, microSD: separate openings, enough plug-body access.
cuts += [box(-8,62.5,ZT-.8,1,77.5,ZT+6),box(-8,30.5,ZT+5,2,44,ZT+18),box(-8,9.3,ZT-1,2,27.3,ZT+4)]
# Headphones at actual FRONT edge; volume wheel accessible from top/right at its real position.
x,y=coords['J5'];cuts.append(box(x-5.5,-8,ZT-.6,x+5.5,2,ZT+7))
x,y=coords['RV1'];cuts.append(box(x-10,y-10,ZT+2,205,y+10,HIGH+1))
for cut in cuts:base=base.cut(cut);lid=lid.cut(cut)
# Control apertures based exclusively on footprint centers.
for i in range(1,9):
 x,y=coords[f'VR{i}'];lid=lid.cut(cyl(x,y,ZT+9,4.25,30))
for r in ['SW17','SW18']:
 x,y=coords[r];lid=lid.cut(cyl(x,y,ZT+7,5.25,30))
for r in coords:
 if r.startswith(('J_CV','J_GATE')):
  x,y=coords[r];lid=lid.cut(cyl(x,y,ZT+9,4.25,30))
# Captive free plungers: no press-fit on tiny square switch actuators.
plungers=[]
for i in range(1,17):
 x,y=coords[f'S{i}'];lid=lid.cut(cyl(x,y,ZT+7,3.3,30))
 # 7.5 mm switch top at17.1; flange .3 mm below lid underside at21.6.
 p=cyl(x,y,ZT+7.5,1.7,3.0).fuse(cyl(x,y,20.1,4.2,1.2)).fuse(cyl(x,y,21.3,3,4.2))
 plungers.append(p)
 # LED direct-view aperture, suitable for optional transparent 3mm lightpipe.
 xl,yl=coords[f'D{i}'];lid=lid.cut(cyl(xl,yl,ZT,1.7,30))
# Vent slots above module, leave boot/reset reachable by removing lid.
for xx in [15,21,27,33,39,45]:lid=lid.cut(box(xx,32,SEED_HIGH-T-.1,xx+2.4,43,SEED_HIGH+.1))
# Clean and mesh validity; export printing coordinates independent of assembled location.
base=base.clean();lid=lid.clean()
print('solids',len(base.Solids()),len(lid.Solids()),'valid',base.isValid(),lid.isValid(),flush=True)
assert len(base.Solids())==1 and base.isValid()
assert len(lid.Solids())==1 and lid.isValid()
caseasm=cq.Assembly(name='Boitier_Seed3_prototype_v2')
caseasm.add(base,name='Socle',color=cq.Color(.16,.18,.20));caseasm.add(lid,name='Capot',color=cq.Color(.32,.36,.39))
for i,p in enumerate(plungers):caseasm.add(p,name=f'Poussoir_{i+1:02d}',color=cq.Color(.82,.80,.66))
caseasm.save(str(OUT/'Boitier_Seed3.step'))
# Print orientation: base flat; lid on its top is stepped, use supports as documented.
printparts={'Socle':base,'Capot':lid.translate((0,0,-SPLIT)),'Poussoir_x16':plungers[0].translate((-coords['S1'][0],-coords['S1'][1],-(ZT+7.5)))}
report={}
for name,s in printparts.items():
 p=OUT/(name+'.stl');cq.exporters.export(s,str(p),tolerance=.04,angularTolerance=.15)
 m=trimesh.load(p,force='mesh');report[name]={'watertight':bool(m.is_watertight),'winding_consistent':bool(m.is_winding_consistent),'parts':len(m.split()),'dimensions_mm':m.extents.tolist(),'volume_mm3':float(m.volume)}
 assert m.is_watertight and m.is_winding_consistent
# Board reference mesh is NOT a printable functional PCB.
board=cq.Shape.importBrep(str(ROOT/'board.brep'))
cq.exporters.export(board,str(OUT/'Carte_Seed3_reference.stl'),tolerance=.1,angularTolerance=.25)
# Complete assembly keeps 3D parts accessible, including separately named electronics.
full=cq.Assembly(name='Seed3_Boitier_et_Carte')
full.add(base,name='Socle',color=cq.Color(.16,.18,.20));full.add(lid,name='Capot',color=cq.Color(.32,.36,.39))
manifest=json.loads((ROOT/'render_manifest.json').read_text())
for m in manifest:
 p=P.Path(m['file']).with_suffix('.brep');s=cq.Shape.importBrep(str(p));full.add(s,name=m['name'],color=cq.Color(*m['color']))
for i,p in enumerate(plungers):full.add(p,name=f'Poussoir_{i+1:02d}',color=cq.Color(.82,.80,.66))
full.save(str(OUT/'Assemblage_Seed3_complet.step'))
# Collision test exact BREP, excluding intentional board rests and actuator contact.
coll=[]
for m in manifest:
 p=P.Path(m['file']).with_suffix('.brep');s=cq.Shape.importBrep(str(p))
 for n,case in [('Capot',lid),('Socle',base)]:
  bb=s.BoundingBox();cb=case.BoundingBox()
  # Skip parts entirely below lid: most small SMD components.
  if n=='Capot' and bb.zmax<10.001:continue
  if n=='Socle' and bb.zmin>10:continue
  q=case.intersect(s);v=q.Volume()
  if v>.001:coll.append({'part':m['name'],'case':n,'intersection_mm3':v})
print('COLLISIONS',coll,flush=True)
report['collisions']=coll
seed=cq.Shape.importBrep(str(ROOT/'meshes/A1_Seed3_official.brep'))
report['ergonomie_v2']={'capot_seed_z_mm':SEED_HIGH,'capot_seed_abaissement_mm':HIGH-SEED_HIGH,'rayon_degagement_a_z24_mm':7,'rayon_degagement_a_z29_5_mm':12.5,'paroi_normale_mm':T,'jeu_minimal_seed_capot_mm':lid.distance(seed),'jeu_radial_axe_coque_a_z24_mm':4,'jeu_radial_axe_coque_a_z29_5_mm':9.5}
print('ERGONOMICS',report['ergonomie_v2'],flush=True)
(OUT/'Verification_geometrie.json').write_text(json.dumps(report,indent=2))
# Assembled render meshes separate from printing orientation.
for n,s,col in [('Socle',base,[.16,.18,.20]),('Capot',lid,[.32,.36,.39])]+[(f'Poussoir_{i+1:02}',p,[.82,.8,.66]) for i,p in enumerate(plungers)]:
 path=ROOT/'meshes'/(n+'.stl');cq.exporters.export(s,str(path),tolerance=.08,angularTolerance=.25);manifest.append({'name':n,'file':str(path),'color':col})
(ROOT/'assembly_manifest.json').write_text(json.dumps(manifest))
print('CASE SAVED',flush=True)
