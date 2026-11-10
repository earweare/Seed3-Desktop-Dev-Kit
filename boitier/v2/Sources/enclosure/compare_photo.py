import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
from PIL import Image
import pathlib,sexpdata as s
exec(pathlib.Path('enclosure/extract.py').read_text().split('out=[]')[0])
fig,ax=plt.subplots(figsize=(16,10.4),facecolor='#171b20')
im=Image.open('upload/image(20261109-225526).png');ax.imshow(im)
# Calibration on the four hole centers visually picked from the supplied image.
# 187 mm ->1827 pixels, 101 mm ->987 pixels; no inferred Z dimensions.
sx_=1827/187;sy_=987/101
for f in sub(a,'footprint'):
 r=props(f).get('Reference','');p=one(f,'at');
 if not p:continue
 if not(r.startswith(('VR','SW','J_CV','J_GATE','H')) or (r.startswith('S') and r[1:].isdigit()) or r=='RV1'):continue
 x=103+(float(p[1])-55)*sx_;y=194+(float(p[2])-49)*sy_
 color='#4bf2b0' if r.startswith('H') else '#ffab40'
 ax.plot(x,y,'+',ms=11,mew=1.5,color=color)
 ax.text(x+7,y-13,r,color=color,fontsize=8,bbox={'facecolor':'black','alpha':.65,'pad':1,'edgecolor':'none'})
ax.set_xlim(0,2048);ax.set_ylim(1337,0);ax.axis('off')
fig.text(.05,.96,'PHOTO FOURNIE + CENTRES EXTRAITS DU KICAD',color='white',fontsize=18,weight='bold')
fig.text(.05,.027,'Recalage sur H1–H4 · contrôle XY uniquement · les hauteurs ne sont pas déduites de la photo',color='#b8c4ce',fontsize=12)
fig.subplots_adjust(left=.02,right=.98,top=.92,bottom=.06)
fig.savefig('enclosure/deliverable/Comparaison_photo_KiCad.png',dpi=130,facecolor=fig.get_facecolor());plt.close(fig)
