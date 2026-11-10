import bpy,json,math,sys,pathlib
from mathutils import Vector
ROOT=pathlib.Path(__file__).resolve().parent
mode=sys.argv[-1]
file=ROOT/('render_manifest.json' if mode=='board' else 'assembly_manifest.json')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in json.loads(file.read_text()):
 bpy.ops.wm.stl_import(filepath=m['file']);o=bpy.context.object;o.name=m['name']
 mat=bpy.data.materials.new(o.name);mat.diffuse_color=(*m['color'],1);mat.use_nodes=True
 bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*m['color'],1);bs.inputs['Roughness'].default_value=.38
 bs.inputs['Metallic'].default_value=.55 if min(m['color'])>.5 and max(m['color'])<.8 else .08
 o.data.materials.append(mat)
 if mode=='exploded':
  if m['name']=='Capot':o.location.z+=45
  elif m['name'].startswith('Poussoir_'):o.location.z+=35
  elif m['name']!='Socle':o.location.z+=16
# Table
bpy.ops.mesh.primitive_plane_add(size=2000,location=(98,55,-.15));plane=bpy.context.object
mat=bpy.data.materials.new('ground');mat.diffuse_color=(.16,.18,.21,1);plane.data.materials.append(mat)
world=bpy.context.scene.world;world.color=(.4,.4,.4)
for loc,power,size in [((30,-40,250),1500000,180),((220,150,210),1100000,130),((-100,60,140),750000,120)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((98,55,10))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(250,-240,270));cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=260 if mode!='exploded' else 290
cam.rotation_euler=(Vector((98,55,20 if mode!='exploded' else 35))-cam.location).to_track_quat('-Z','Y').to_euler()
if mode=='detail':
 cam.location=(110,-25,115);cam.data.ortho_scale=67
 cam.rotation_euler=(Vector((64,49,25))-cam.location).to_track_quat('-Z','Y').to_euler()
sc=bpy.context.scene;sc.camera=cam;sc.render.engine='CYCLES';sc.cycles.samples=64;sc.cycles.use_denoising=False
sc.render.resolution_x=1600;sc.render.resolution_y=1100;sc.render.resolution_percentage=100
sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-1.0;sc.render.image_settings.file_format='PNG';sc.render.filepath=str(ROOT/'deliverable'/f'Vue_3D_{mode}.png')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/f'{mode}.blend'))
bpy.ops.render.render(write_still=True)
if mode=='board':
 cam.location=(98.5,55.5,350);cam.rotation_euler=(0,0,0);cam.data.ortho_scale=218
 sc.render.resolution_x=1800;sc.render.resolution_y=1100;sc.render.filepath=str(ROOT/'deliverable'/'Vue_carte_dessus.png');bpy.ops.render.render(write_still=True)
