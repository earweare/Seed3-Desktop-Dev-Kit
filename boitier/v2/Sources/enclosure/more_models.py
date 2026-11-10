import urllib.request, pathlib, zipfile, concurrent.futures
p=pathlib.Path('enclosure/models');p.mkdir(exist_ok=True)
urls={
'Seed3-models.zip':'https://daisy.nyc3.cdn.digitaloceanspaces.com/products/seed3/Seed3-models.zip',
'DaisyKiCad-main.zip':'https://daisy.nyc3.cdn.digitaloceanspaces.com/libraries/DaisyKiCad-main.zip',
}
def get(kv):
 n,u=kv
 try:
  b=urllib.request.urlopen(u,timeout=45).read();(p/n).write_bytes(b)
  if n.endswith('.zip'):zipfile.ZipFile(p/n).extractall(p/n[:-4])
  return n,len(b)
 except Exception as e:return n,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for r in ex.map(get,urls.items()):print(r,flush=True)
