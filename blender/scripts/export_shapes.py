import os
import bpy
import mathutils

def clean_transforms(link):
    link.parent = None
    link.location = mathutils.Vector((0., 0., 0.))
    link.rotation_euler = mathutils.Euler((0., 0., 0.), "XYZ")

if __name__ == "__main__":
    base_path = r"C:\Users\hgtll\Projects\hexapod-ros2\blender"
    links_names = ["link0"] + ["link%d%d" % (i, j) for i in range(1, 3) for j in range(1, 5)]
    
    bpy.ops.object.select_all(action='DESELECT')
    
    for link_name in links_names:
        link = bpy.data.objects[link_name]
        clean_transforms(link)
        link.select_set(True)
        bpy.ops.wm.collada_export(
            filepath=os.path.join(base_path, link_name + "---.dae"), selected=True
        )
        link.select_set(False)