import bpy

class IOPS(bpy.types.Operator):
    bl_idname = "iops.main"
    bl_label = "IOPS"
    bl_options = {"REGISTER","UNDO"}

    modes_3d = {0:"VERT", 1:"EDGE", 2:"FACE"}
    modes_uv = {0:"VERTEX", 1:"EDGE", 2:"FACE", 3:"ISLAND"}
    modes_gpen = {0:"EDIT_GPENCIL", 1:"PAINT_GPENCIL", 2:"SCULPT_GPENCIL"}
    modes_curve = {0:"EDIT_CURVE"}
    supported_types = ["MESH", "CURVE", "GPENCIL", "EMPTY"]

    current_mode_3d = ""
    current_mode_uv = ""
    current_mode_gpen = ""
    current_mode_curve = ""
       
    @classmethod
    def poll(cls, context):                  
        return context.object is not None
      
    def execute(self, context):
        #Object <-> Mesh
        scene = bpy.context.scene
        if bpy.context.active_object.type == "MESH": 
            current_mode_3d = "VERT" if scene.tool_settings.mesh_select_mode[0] else ""
            current_mode_3d = "EDGE" if scene.tool_settings.mesh_select_mode[1] else ""
            current_mode_3d = "FACE" if scene.tool_settings.mesh_select_mode[2] else ""
            
            if (bpy.context.area.type == "VIEW_3D" or 
               (bpy.context.area.type == "IMAGE_EDITOR" and 
                bpy.context.tool_settings.use_uv_select_sync == True)):
                # Same modes for active sync in UV 
                # Go to Edit Mode       
                if bpy.context.mode == "OBJECT": 
                    bpy.ops.object.mode_set(mode="EDIT")            
                    bpy.ops.mesh.select_mode(type=self.current_mode_3d)
                    IOPS.current_mode_3d = self.current_mode_3d
                    return{"FINISHED"}
                    
                # Switch selection modes
                # If activated same selection mode again switch to Object Mode   
                if bpy.context.mode == "EDIT_MESH" and self.current_mode_3d != IOPS.current_mode_3d:                
                    bpy.ops.mesh.select_mode(type=self.current_mode_3d)
                    IOPS.current_mode_3d = self.current_mode_3d
                    return{"FINISHED"}
                else:
                    bpy.ops.object.mode_set(mode="OBJECT")
                    return{"FINISHED"}   

            # UV <-> Mesh 
            if bpy.context.area.type == "IMAGE_EDITOR": 
                # Go to Edit Mode and Select All
                if bpy.context.mode == "OBJECT":
                    bpy.ops.object.mode_set(mode="EDIT")
                    bpy.ops.mesh.select_all(action="SELECT")
                    bpy.context.tool_settings.uv_select_mode = self.current_mode_uv
                    IOPS.current_mode_uv = self.current_mode_uv
                    return{"FINISHED"}

                elif self.current_mode_uv != IOPS.current_mode_uv:
                        bpy.context.tool_settings.uv_select_mode = self.current_mode_uv
                        IOPS.current_mode_uv = self.current_mode_uv
                        return{"FINISHED"}
                else:
                        bpy.ops.object.mode_set(mode="OBJECT")
                        return{"FINISHED"} 

        # Object <-> Curve    
        if bpy.context.active_object.type == "CURVE":  
            current_mode_curve = "EDIT" if bpy.context.mode != "EDIT_CURVE" else "OBJECT" 
            bpy.ops.object.mode_set(mode=current_mode_curve)                             
            return{"FINISHED"}

        # Object <-> GPencil  
        if bpy.context.active_object.type == "GPENCIL":
            current_mode_gpen = "EDIT_GPENCIL" if bpy.context.mode != "EDIT_GPENCIL" else "OBJECT" 
            bpy.ops.object.mode_set(mode=current_mode_gpen)
            return{"FINISHED"} 

        #Unsupported Types      
        if bpy.context.active_object.type not in IOPS.supported_types:
            print(bpy.context.active_object.type,"not supported yet!")
            return{"FINISHED"} 
        return{"FINISHED"}