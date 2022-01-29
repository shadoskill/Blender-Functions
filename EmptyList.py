bl_info = {
    "name": "[EmptyList]",
    "author": "Shadoskill",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "",
    "description": "",
    "warning": "",
    "doc_url": "",
    "category": "",
}

import bpy
import math

class EmptyList(bpy.types.Panel):
    bl_label = "[EmptyList]"
    bl_idname = "OBJECT_PT_EmptyList"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "[EmptyList]"

    def draw(self, context):
        layout = self.layout
        column = layout.column()
        
        column.operator("el.uv")
        column.operator("el.clothes")

class RenameUV(bpy.types.Operator):
    bl_label = "Rename Selected Objects UV"
    bl_idname = "el.uv"
    uvName = bpy.props.StringProperty(name="UV Map Name:", default="UVMap")
    
    def execute(self, context):
        for obj in bpy.context.selected_objects :
            for uvmap in  obj.data.uv_layers :
                uvmap.name = self.uvName
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
class NewClothing(bpy.types.Operator):
    bl_label = "New Clothes Base for Selected"
    bl_idname = "el.clothes"
    
    def execute(self, context):
        selectedObject = bpy.context.active_object
        
        bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.ops.transform.translate(value=(0, -0.5, 1.15))
        bpy.ops.transform.resize(value=(0.05, 0.05, 0.05))
        bpy.ops.transform.rotate(value=-math.radians(90), orient_axis='X')
        bpy.ops.object.editmode_toggle()
        
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        bpy.context.object.modifiers["Solidify"].thickness = 0.02

        bpy.ops.object.modifier_add(type='SUBSURF')

        bpy.ops.object.modifier_add(type='SHRINKWRAP')
        bpy.context.object.modifiers["Shrinkwrap"].offset = 0.002
        
        if selectedObject is not None:
            bpy.context.object.modifiers["Shrinkwrap"].target = bpy.data.objects[selectedObject.name]

        return {'FINISHED'}
    
def register():
    bpy.utils.register_class(EmptyList)
    bpy.utils.register_class(RenameUV)
    bpy.utils.register_class(NewClothing)


def unregister():
    bpy.utils.unregister_class(EmptyList)
    bpy.utils.unregister_class(RenameUV)
    bpy.utils.unregister_class(NewClothing)

if __name__ == "__main__":
    register()
