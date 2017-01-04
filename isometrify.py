#Quick readme:
#
# This project was based on Spritify and also uses ImageMagick
#
# This is fairly well tested in windows and for basic animation setups
#
# Step 1. Install addon
# Step 2. create an object that parents your lighting and camera objects
# Step 3. create, rig, and animate whatever
# Step 4. in the isometrify panel on the render tab, connect your world object and your armature
# Step 5. Click "Generate Isometric Renders"


bl_info = {
    "name": "Isometrify",
    "author": "Jacob Stewart",
    "version": (0, 0, 1),
    "blender": (2, 66, 0),
    "location": "Render > Isometrify",
    "description": "Captures a render as multiple isometric frames",
    "warning": "Requires ImageMagick and Spritify",
    "category": "Render"}

import bpy, math

class IsometrifyOperator(bpy.types.Operator):
    bl_idname="render.isometrify"
    bl_label = "Generate Isometric Renders"

    def execute(self, context):
        scene = context.scene

        scene.objects.active = scene.objects[scene.armature]#select the armature because it contains the actions

        for a in bpy.context.screen.areas:
            if a.type == 'DOPESHEET_EDITOR':
                x = a.spaces.active
#                z = bpy.data.actions.get('CubeAction')
#                x.action = z

        for action in bpy.data.actions:
            name = action.name
            scene.frame_start = action.frame_range[0] + scene.SettleFrames
            scene.frame_end = action.frame_range[1]
            scene.frame_step = 10

            numFrames = (scene.frame_end - scene.frame_start)/scene.frame_step
            scene.spritesheet.tiles = 8#numFrames+1
            #            scene.spritesheet.is_rows = False

            z = bpy.data.actions.get(name)
            x.action = z#Set the dopesheet to the correct action

            self.report({'ERROR'}, name+str(action.frame_range[1]))

            scene.objects[scene.worldCamera].rotation_euler.z = 0
            scene.render.filepath = "//temp\\0"+name
            bpy.ops.render.render(animation = True)
            scene.spritesheet.filepath = "//temp\\ss0_"+name+".png"
            bpy.ops.render.spritify()

            scene.objects[scene.worldCamera].rotation_euler.z = 3*math.pi/2
            scene.render.filepath = "//temp\\1"+name
            bpy.ops.render.render(animation = True)
            scene.spritesheet.filepath = "//temp\\ss1_"+name+".png"
            bpy.ops.render.spritify()

            scene.objects[scene.worldCamera].rotation_euler.z = math.pi
            scene.render.filepath = "//temp\\2"+name
            bpy.ops.render.render(animation = True)
            scene.spritesheet.filepath = "//temp\\ss2_"+name+".png"
            bpy.ops.render.spritify()

            scene.objects[scene.worldCamera].rotation_euler.z = math.pi/2
            scene.render.filepath = "//temp\\3"+name
            bpy.ops.render.render(animation = True)
            scene.spritesheet.filepath = "//temp\\ss3_"+name+".png"
            bpy.ops.render.spritify()

        return {'FINISHED'}

class OBJECT_PT_Isometrify(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Isometrify"
    bl_idname = "OBJECT_PT_Isometrifys"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.operator("render.isometrify", text="Generate Isometric Renders")
        layout.prop_search(scene, "worldCamera", scene, "objects")
        layout.prop_search(scene, "armature", scene, "objects")
        layout.prop(scene, "SettleFrames")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.worldCamera = bpy.props.StringProperty()
    bpy.types.Scene.armature = bpy.props.StringProperty()
    bpy.types.Scene.SettleFrames = bpy.props.IntProperty(name="Settle Frames", min = 0, max = 1000, default = 0)


def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.worldCamera
    del bpy.types.Scene.armature
    del bpy.types.Scene.SettleFrames


if __name__ == "__main__":
    register()
