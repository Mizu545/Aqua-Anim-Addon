bl_info = {
    "name": "Spring Bone Function",
    "blender": (4, 4, 0),
    "category": "Rigging",
}

import bpy 

class SpringBoneProperties(bpy.types.PropertyGroup):
    stiffness: bpy.props.FloatProperty(name="Stiffness", default=0.5, min=0.0, max=1.0)
    damping: bpy.props.FloatProperty(name="Damping", default=0.5, min=0.0, max=1.0)

class AddSpringBonesOperator(bpy.types.Operator):
    bl_idname = "rigging.add_spring_bones"
    bl_label = "Add Spring Bones"
    bl_options = {'REGISTER', 'UNDO'}

    bone_name: bpy.props.StringProperty(name="Bone Name", default="Bone")

    def execute(self, context):
        armature = context.object
        if armature and armature.type == 'ARMATURE':
            bpy.ops.object.mode_set(mode='EDIT')
            bone = armature.data.edit_bones.get(self.bone_name)
            if bone:
                # Create a new bone for the spring effect
                spring_bone = armature.data.edit_bones.new(self.bone_name + "_spring")
                spring_bone.head = bone.head
                spring_bone.tail = bone.tail
                spring_bone.parent = bone

                # Switch to pose mode to add constraints
                bpy.ops.object.mode_set(mode='POSE')
                pose_bone = armature.pose.bones[spring_bone.name]
                
                #Copy Transforms constraint
                copy_transforms = pose_bone.constraints.new('COPY_TRANSFORMS')
                copy_transforms.target = armature
                copy_transforms.subtarget = bone.name
                
                #Damped Track constraint
                damped_track = pose_bone.constraints.new('DAMPED_TRACK')
                damped_track.target = armature
                damped_track.subtarget = bone.name
                damped_track.influence = bpy.context.scene.spring_bone_properties.stiffness
                
                # Limit Distance constraint
                limit_distance = pose_bone.constraints.new('LIMIT_DISTANCE')
                limit_distance.target = armature
                limit_distance.subtarget = bone.name
                limit_distance.limit_mode = 'FIXED'
                limit_distance.distance = (bone.tail - bone.head).length
                limit_distance.influence = bpy.context.scene.spring_bone_properties.damping
                
                bpy.ops.object.mode_set(mode='EDIT')
            else:
                self.report({'WARNING'}, "Bone not found")
        else:
             self.report({'WARNING'}, "Select an Armature")
        return {'FINISHED'}

class SpringBonePanel(bpy.types.Panel):
    bl_label = "Spring Bone Settings"
    bl_idname = "OBJECT_PT_spring_bone_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Spring Bone"

    def draw(self, context):
         layout = self.layout
         scene = context.scene
         layout.prop(scene.spring_bone_properties, "stiffness")
         layout.prop(scene.spring_bone_properties, "damping")
         layout.operator(AddSpringBonesOperator.bl_idname, text="Add Spring Bones")

def register():
     bpy.utils.register_class(SpringBoneProperties)
     bpy.types.Scene.spring_bone_properties = bpy.props.PointerProperty(type=SpringBoneProperties)
     bpy.utils.register_class(AddSpringBonesOperator)
     bpy.utils.register_class(SpringBonePanel)

def unregister():
    bpy.utils.unregister_class(SpringBoneProperties)
    del bpy.types.Scene.spring_bone_properties
    bpy.utils.unregister_class(AddSpringBonesOperator)
    bpy.utils.unregister_class(SpringBonePanel)

if __name__ == "__main__":
    register()





