import sexpdata as s,json,pathlib
p=pathlib.Path('seed3-hardware/pcb/Seed3-DevKit-Desktop/Seed3-DevKit-Desktop.kicad_pcb');a=s.loads(p.read_text())
def tag(x):return str(x[0]) if isinstance(x,list) and x else ''
def sub(x,t):return [y for y in x if tag(y)==t]
def one(x,t,d=None):return next(iter(sub(x,t)),d)
def props(f):return {v[1]:v[2] for v in sub(f,'property')}
out=[]
for f in sub(a,'footprint'):
 pr=props(f);r=pr.get('Reference','');v=pr.get('Value','')
 if r.startswith(('J','VR','SW','S','H')) or r=='U1':
  g={'ref':r,'value':v,'footprint':f[1],'at':one(f,'at')[1:],'models':sub(f,'model'),'graphics':[z for z in f if tag(z) in ['fp_line','fp_rect','fp_circle','fp_arc']],'pads':sub(f,'pad')};out.append(g)
  print(r,v,f[1],g['at'],'models:',g['models'])
print('EDGES')
for x in a:
 if tag(x).startswith('gr_') and one(x,'layer')==[s.Symbol('layer'),'Edge.Cuts']:print(x)
pathlib.Path('enclosure/pcb-extract.json').write_text(json.dumps(out,indent=2,default=str))
