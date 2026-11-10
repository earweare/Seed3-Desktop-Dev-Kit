from pathlib import Path
exec(Path('enclosure/extract.py').read_text().split('out=[]')[0])
import urllib.request,concurrent.futures
models=set()
for f in sub(a,'footprint'):
 for m in sub(f,'model'):
  if '3DMODEL_DIR}' in m[1]:models.add(m[1].split('}/')[1])
def get(m):
 p=Path('enclosure/models')/m;p.parent.mkdir(parents=True,exist_ok=True)
 u='https://raw.githubusercontent.com/KiCad/kicad-packages3D/master/'+m
 try:
  r=urllib.request.urlopen(u,timeout=30).read()
  p.write_bytes(r)
  return m,200,len(r)
 except Exception as e:return m,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 for r in ex.map(get,sorted(models)):print(r,flush=True)
