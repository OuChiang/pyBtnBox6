import bpy
import os
from . import modules
PyBtnBox = modules
from . import panel_modules
Panel = panel_modules


## Main Layout Root Panel
class PYBTNBOX_PT_Main(bpy.types.Panel):
    bl_label = "pyBtnBox"
    bl_region_type = 'UI'
    bl_category = "pyBtnBox"
    icons = None
    area = 'veiw_3d'

    def draw_header(self, context):
        self.layout.label(text = "", icon = "SCRIPT")
    def draw(self, context):
        pass

# [General]
# VIEW_3D
class PYBTNBOX_PT_Main_View( PYBTNBOX_PT_Main ):
    bl_idname = "PYBTNBOX_PT_Main_View"
    bl_space_type = 'VIEW_3D'
    @classmethod
    def poll(cls, context):
        return context.preferences.addons[__package__].preferences.Menus_show[0] 
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_0")
# IMAGE
class PYBTNBOX_PT_Main_Image( PYBTNBOX_PT_Main ):
    bl_idname = "PYBTNBOX_PT_Main_Image"
    bl_space_type = 'IMAGE_EDITOR'
    @classmethod
    def poll(cls, context):
        nodePanel = context.area.ui_type == "IMAGE_EDITOR"
        menusShow = context.preferences.addons[__package__].preferences.Menus_show[1] 
        return nodePanel and menusShow 
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_1")
# UV
class PYBTNBOX_PT_Main_Image_UV( PYBTNBOX_PT_Main ):
    bl_idname = "PYBTNBOX_PT_Main_Image_UV"
    bl_space_type = 'IMAGE_EDITOR'
    @classmethod
    def poll(cls, context):
        nodePanel = context.area.ui_type == "UV"
        menusShow = context.preferences.addons[__package__].preferences.Menus_show[2] 
        return nodePanel and menusShow 
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_2")
# NODE Compositor
class PYBTNBOX_PT_Main_Node_Compositor(PYBTNBOX_PT_Main):
    bl_idname = "PYBTNBOX_PT_Main_Node_Compositor"
    bl_space_type = 'NODE_EDITOR'
    @classmethod
    def poll(cls, context):
        nodePanel = context.area.ui_type == "CompositorNodeTree"
        menusShow = context.preferences.addons[__package__].preferences.Menus_show[3] 
        return nodePanel and menusShow
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_3")
# NODE Texture
class PYBTNBOX_PT_Main_Node_Tex(PYBTNBOX_PT_Main):
    bl_idname = "PYBTNBOX_PT_Main_Node_Tex"
    bl_space_type = 'NODE_EDITOR'
    @classmethod
    def poll(cls, context):
        nodePanel = context.area.ui_type == "TextureNodeTree"
        menusShow = context.preferences.addons[__package__].preferences.Menus_show[4] 
        return nodePanel and menusShow 
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_4")
# NODE Geometry
class PYBTNBOX_PT_Main_Node_Geo(PYBTNBOX_PT_Main):
    bl_idname = "PYBTNBOX_PT_Main_Node_Geo"
    bl_space_type = 'NODE_EDITOR'
    @classmethod
    def poll(cls, context):
        nodePanel = context.area.ui_type == "GeometryNodeTree"
        menusShow = context.preferences.addons[__package__].preferences.Menus_show[5] 
        return nodePanel and menusShow
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_5")

# NODE Shader
class PYBTNBOX_PT_Main_Node_Shader(PYBTNBOX_PT_Main):
    bl_idname = "PYBTNBOX_PT_Main_Node_Shader"
    bl_space_type = 'NODE_EDITOR'
    @classmethod
    def poll(cls, context):
        nodePanel = context.area.ui_type == "ShaderNodeTree"
        menusShow = context.preferences.addons[__package__].preferences.Menus_show[6] 
        return nodePanel and menusShow
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_6")

# SEQUENCE_EDITOR
class PYBTNBOX_PT_Main_Video(PYBTNBOX_PT_Main):
    bl_idname = "PYBTNBOX_PT_Main_Video"
    bl_space_type = 'SEQUENCE_EDITOR'
    @classmethod
    def poll(cls, context):
        return context.preferences.addons[__package__].preferences.Menus_show[7] 
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_7")
# [Animation]
# DOPESHEET_EDITOR
class PYBTNBOX_PT_Main_Dope( PYBTNBOX_PT_Main ):
    bl_idname = "PYBTNBOX_PT_Main_Dope"
    bl_space_type = 'DOPESHEET_EDITOR'
    @classmethod
    def poll(cls, context):
        nodePanel = context.area.ui_type == "DOPESHEET"
        menusShow = context.preferences.addons[__package__].preferences.Menus_show[8] 
        return nodePanel and menusShow
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_8")
# [Animation]
# GRAPH_EDITOR
class PYBTNBOX_PT_Main_Graph_Fcurves( PYBTNBOX_PT_Main ):
    bl_idname = "PYBTNBOX_PT_Main_Graph_Fcurves"
    bl_space_type = 'GRAPH_EDITOR'
    @classmethod
    def poll(cls, context):
        nodePanel = context.area.ui_type == "FCURVES"
        menusShow = context.preferences.addons[__package__].preferences.Menus_show[9] 
        return nodePanel and menusShow
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_9")
# GRAPH_EDITOR
class PYBTNBOX_PT_Main_Graph_Drivers( PYBTNBOX_PT_Main ):
    bl_idname = "PYBTNBOX_PT_Main_Graph_Drivers"
    bl_space_type = 'GRAPH_EDITOR'
    @classmethod
    def poll(cls, context):
        nodePanel = context.area.ui_type == "DRIVERS"
        menusShow = context.preferences.addons[__package__].preferences.Menus_show[10] 
        return nodePanel and menusShow
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_10")
# NLA_EDITOR
class PYBTNBOX_PT_Main_NLA( PYBTNBOX_PT_Main ):
    bl_idname = "PYBTNBOX_PT_Main_NLA"
    bl_space_type = 'NLA_EDITOR'
    @classmethod
    def poll(cls, context):
        return context.preferences.addons[__package__].preferences.Menus_show[11] 
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_11")
# [Scripting]
# TEXT_EDITOR
class PYBTNBOX_PT_Main_Script( PYBTNBOX_PT_Main ):
    bl_idname = "PYBTNBOX_PT_Main_Script"
    bl_space_type = 'TEXT_EDITOR'
    @classmethod
    def poll(cls, context):
        return context.preferences.addons[__package__].preferences.Menus_show[12] 
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_12")
'''
# DOPESHEET_EDITOR
class PYBTNBOX_PT_Main_Dope_Timelime( PYBTNBOX_PT_Main ):
    bl_idname = "PYBTNBOX_PT_Main_Dope_Timelime"
    bl_space_type = 'DOPESHEET_EDITOR'
    @classmethod
    def poll(cls, context):
        nodePanel = context.area.ui_type == "TIMELINE"
        menusShow = context.preferences.addons[__package__].preferences.Menus_show[9] 
        return nodePanel and menusShow
    def draw(self, context):
        Panel.MenuLayout.draw_panel(self,context,"Menu_area_13")
'''


#==================
#==  Edit Panel  ==
#==================

# Menu Select
class PYBTNBOX_PT_Editor_Menu(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = "pyBtnBox Edit"
    bl_label = ''
    bl_idname = "PYBTNBOX_PT_Editor_Menu"
    bl_options = {'HEADER_LAYOUT_EXPAND'}

    def draw_header(self, context):
        layout = self.layout
        layout.label(text='Menu Edit',icon='TOOL_SETTINGS')
        return
        

    def draw(self, context):
        Panel.Editor_Menu_Layout.draw(self, context)
        return
        

class PYBTNBOX_PT_Editor_Node(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = "pyBtnBox Edit"
    bl_label = "Node Edit"
    bl_idname = "PYBTNBOX_PT_Editor_Node"
    bl_order = 1
    bl_options = {'HEADER_LAYOUT_EXPAND','DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        # Menu Picker
        Editor = context.scene.pybtnbox_prop_editor
        Menu = PyBtnBox.Menu.from_menu_name(Editor.menu)
        if not Menu : 
            return False
        
        Menus = PyBtnBox.Root.load().menu_list()
        return Menu.name in Menus
    
    def draw(self, context):
        Panel.Editor_Node_Layout.draw(self,context)
        return
        
class_list = [
    # [ Main Panels ]
    PYBTNBOX_PT_Main_View,
    PYBTNBOX_PT_Main_Image,
    PYBTNBOX_PT_Main_Image_UV,
    PYBTNBOX_PT_Main_Node_Compositor,
    PYBTNBOX_PT_Main_Node_Tex,
    PYBTNBOX_PT_Main_Node_Geo,
    PYBTNBOX_PT_Main_Node_Shader,
    PYBTNBOX_PT_Main_Video,
    PYBTNBOX_PT_Main_Dope,
    PYBTNBOX_PT_Main_Graph_Fcurves,
    PYBTNBOX_PT_Main_Graph_Drivers,
    PYBTNBOX_PT_Main_NLA,
    PYBTNBOX_PT_Main_Script,
    #PYBTNBOX_PT_Main_Dope_Timelime,

    # [ Edit Panel ]
    PYBTNBOX_PT_Editor_Menu,
    PYBTNBOX_PT_Editor_Node
]
def register():
    for cls in class_list:
        bpy.utils.register_class(cls)


def unregister():
    class_list.reverse()
    for cls in class_list:
        bpy.utils.unregister_class(cls)