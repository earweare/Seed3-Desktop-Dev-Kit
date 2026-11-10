import numpy as np
from PIL import Image
from scipy.ndimage import label,center_of_mass
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation
import csv,json,pathlib
im=np.asarray(Image.open('upload/image(20261109-232317).png').convert('RGB')).astype(float)
r,g,b=im[:,:,0],im[:,:,1],im[:,:,2]
mask=(r>140)&(g>140)&(b<g*.70)&(g>r*.83)&(g<r*1.18)
l,n=label(mask);cnt=np.bincount(l.ravel());valid=np.where((cnt>60)&(cnt<1600))[0]
pts=[]
for v in valid:
 y,x=center_of_mass(mask,l,int(v))
 if 450<x<1350 and 900<y<1460:pts.append((round(x,2),round(y,2),int(cnt[v])))
print(pts)
cent=[]
for v in valid:
 yy,xx=np.where(l==v)
 if not (450<xx.mean()<1350 and 900<yy.mean()<1460):continue
 bright=(r[yy,xx]+g[yy,xx])
 sel=bright>=np.quantile(bright,.6)
 cent.append([xx[sel].mean(),yy[sel].mean()])
# two diagonals separated by y-.67*x; sort each by x.
cent=np.array(cent);keys=cent[:,1]-.67*cent[:,0]
row1=cent[keys<560];row2=cent[keys>=560]
row1=row1[np.argsort(row1[:,0])];row2=row2[np.argsort(row2[:,0])]
print('rows',len(row1),len(row2))
co={r['reference']:np.array([float(r['x_from_left_mm']),float(r['y_from_front_mm'])]) for r in csv.DictReader(open('enclosure/deliverable/Implantation_KiCad_mm.csv'))}
world=[];obs=[];names=[]
for i,p in enumerate(np.vstack([row1,row2])):
 name=f'S{i+1}';world.append([*co[name],7.5]);obs.append(p);names.append(name)
for name,p in [('H1',[716,396]),('H2',[205,841]),('H4',[1366,1635])]:world.append([*co[name],0]);obs.append(p);names.append(name)
world=np.array(world);obs=np.array(obs)
origin=np.array([98.5,55.5,0])
R=np.array([[.8,.6,0],[.42,-.56,-.714],[-.428,.571,-.7]])
u,s,v=np.linalg.svd(R);R=u@v
p0=np.r_[Rotation.from_matrix(R).as_rotvec(),0,0,400,np.log(3000)]
def project(p,w):
 q=(w-origin)@Rotation.from_rotvec(p[:3]).as_matrix().T+p[3:6]
 return np.exp(p[6])*q[:,:2]/q[:,2:3]+[1024,1024]
def residual(p):return (project(p,world)-obs).ravel()
fit=least_squares(residual,p0,loss='soft_l1',f_scale=3,max_nfev=3000)
p=fit.x;err=np.linalg.norm(project(p,world)-obs,axis=1)
print('fit',fit.cost,'f',np.exp(p[6]),'rms',np.sqrt(np.mean(err**2)))
print(list(zip(names,np.round(err,2))))
# Manually picked top shaft centres from oblique photograph, approx 2 px uncertainty.
pots=np.array([[762,685],[857,742],[951,803],[1048,864],[1147,925],[1246,990],[1347,1052],[1449,1116]],float)
heights=[]
for i,o in enumerate(pots):
 xy=co[f'VR{i+1}'];res=least_squares(lambda z:(project(p,np.array([[*xy,z[0]]]))[0]-o),[20])
 heights.append(float(res.x[0]));print('VR',i+1,round(res.x[0],2),'px err',np.linalg.norm(res.fun))
# Validation observations for independent known-high capacitor top centres.
report={'method':'Perspective camera fit: 16 switch top faces at nominal 7.5mm plus 3 PCB mounting holes at z0; manual top-shaft centers','image':'image(20261109-232317).png','camera_focal_px':float(np.exp(p[6])),'calibration_rms_px':float(np.sqrt(np.mean(err**2))),'pot_heights_mm':heights,'pot_median_mm':float(np.median(heights)),'limitations':'One oblique photograph; unknown lens distortion; switch top extraction approximate; not certified metrology.'}
pathlib.Path('enclosure/deliverable/Estimation_photo_oblique.json').write_text(json.dumps(report,indent=2))
# Annotated evidence image, scientific overlay only.
import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(10,10));ax.imshow(im.astype('uint8'));ax.plot(obs[:,0],obs[:,1],'+',color='cyan',ms=6)
for i,o in enumerate(pots):ax.plot(*o,'+',color='orange',ms=8);ax.text(o[0]+7,o[1]-8,f'{heights[i]:.1f} mm',color='black',fontsize=8,bbox=dict(facecolor='white',alpha=.85,edgecolor='none'))
ax.set_xlim(130,1930);ax.set_ylim(1700,330);ax.axis('off');fig.suptitle('Estimation des hauteurs par recalage sur la vue oblique',fontsize=13);fig.savefig('enclosure/deliverable/Comparaison_photo_oblique.png',dpi=150,bbox_inches='tight');plt.close(fig)
for label,xy,h in [('seed front left',[1.366,28.354],10.101),('seed front right',[52.516,28.354],10.101),('seed back left',[1.366,46.354],10.101),('seed back right',[52.516,46.354],10.101)]:print(label,project(p,np.array([[*xy,h]]))[0])
for r,o in [('J_CV_OUT_1',[1100,634]),('J_CV_OUT_2',[1024,703]),('J_CV_IN_1',[1285,745]),('J_CV_IN_2',[1212,818]),('J_GATE_IN1',[1351,783]),('J_GATE_IN2',[1278,858])]:
 xy=co[r];res=least_squares(lambda z:project(p,np.array([[*xy,z[0]]]))[0]-o,[14.5]);print(r,res.x[0],np.linalg.norm(res.fun))
seed_xy=np.array([[1.366,28.354],[52.516,28.354],[1.366,46.354],[52.516,46.354]])
seed_obs=np.array([[299,654],[591,843],[391,576],[680,763]])
res=least_squares(lambda z:(project(p,np.column_stack([seed_xy,np.full(4,z[0])]))-seed_obs).ravel(),[12])
print('Seed top height',res.x[0], 'PCB bottom height',res.x[0]-1.601,'rms',np.sqrt(np.mean(res.fun**2)))
report['seed_pcb_top_above_main_pcb_mm']=float(res.x[0]);report['seed_pcb_bottom_above_main_pcb_mm']=float(res.x[0]-1.601);report['seed_corner_fit_rms_px']=float(np.sqrt(np.mean(res.fun**2)))
pathlib.Path('enclosure/deliverable/Estimation_photo_oblique.json').write_text(json.dumps(report,indent=2))
