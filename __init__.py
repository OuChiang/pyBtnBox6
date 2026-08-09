import bpy
import os
import importlib

# Preferences
class PyBtnBox_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__
    
    root_path : bpy.props.StringProperty(
        name="Example File Path",
        default= '',
        subtype='DIR_PATH',
    )

    Menus_show : bpy.props.BoolVectorProperty(
        name="Panel Use",
        size=14,
        default=(True,True,True,True,True,True,True,
                 True,True,True,True,True,True,True)
        )
    def root_path_state(self):
        rootPath = self.root_path
        if rootPath=='':
            return 'PATH_EMPTY'
        if not os.path.exists(rootPath):
            return 'FOLDER_NOT_FOUND'
        dir_base_name = os.path.basename(os.path.dirname(rootPath))
        if not dir_base_name.startswith('pybtnbox_menus'):
            return 'FOLDER_NAME_WRONG'
        return 'PATH_FINE'
    def draw_root_path(self,layout,pathState):
        layout.prop(self, "root_path",text='Root Folder Path')
        col = layout.column(align=True)
        row_pathState = col.row()
        if pathState == 'PATH_EMPTY':
            row_pathState.alert = True
            row_pathState.label(text='Root Path Is Empty', icon='ERROR')
            info_txt_1 = 'For data security reasons'
            info_txt_2 = 'the root folder must be named start with \"pybtnbox_menus\"'
            col.label(text=info_txt_1, icon='INFO')
            col.label(text=info_txt_2, icon='BLANK1')

        if pathState == 'FOLDER_NAME_WRONG':
            row_pathState.alert = True
            row_pathState.label(text='Folder Name Is Wrong', icon='ERROR')
            info_txt_1 = 'For data security reasons'
            info_txt_2 = 'the root folder must be named start with \"pybtnbox_menus\"'
            col.label(text=info_txt_1, icon='INFO')
            col.label(text=info_txt_2, icon='BLANK1')

        if pathState == 'FOLDER_NOT_FOUND':
            row_pathState.alert = True
            row_pathState.label(text='The Folder Is Not Found', icon='ERROR')
            col.label(text='The folder not found', icon='INFO')

        if pathState == 'PATH_FINE':
            row_pathState.alert = False
            row_pathState.label(text='Root Path Is Fine', icon='CHECKMARK')
            col.label(text='You can edit Menus/Buttons in :', icon='INFO')
            col.label(text='Text_Editor > Sidebar > pyBtnBox Edit', icon='BLANK1')

    def draw(self, context):
        layout = self.layout

        # Root Path 
        pathState = self.root_path_state()
        self.draw_root_path(layout,pathState)
        # Show Area
        Area_data = [
            ['3D Viewport','VIEW3D'],
            ['Image Editor','IMAGE'],
            ['UV Editor','UV'],
            ['Compositor','NODE_COMPOSITING'],
            ['Texture Node Editor','NODE_TEXTURE'],
            ['Geometry Node Editor','GEOMETRY_NODES'],
            ['Shader Editor','SHADING_RENDERED'],
            ['Video Sequencer','SEQUENCE'],
            ['Dope Sheet','ACTION'],
            ['Graph Editor','GRAPH'],
            ['Drivers','DRIVER'],
            ['Nonlinear Animation','NLA'],
            ['Text Editor','TEXT'],
            #['Timeline','TIME']
        ]
        useAreas = layout.panel('use_area',default_closed =True)
        useAreas[0].label(text='Area')
        if useAreas[1]:
            col_areas =useAreas[1].column(align=True)
            for i,velues in enumerate(Area_data):
                col_areas.prop(self,'Menus_show',index=i,text=velues[0],icon=velues[1])



class_list = [
    'properties',
    'operators',
    'panels',
]
def register():
    bpy.utils.register_class(PyBtnBox_Preferences)
    for cls in class_list:
        param = importlib.import_module(f'.{cls}',package=__name__)
        param.register()


def unregister():
    class_list.reverse()
    for cls in class_list:
        param = importlib.import_module(f'.{cls}',package=__name__)
        param.unregister()
    bpy.utils.unregister_class(PyBtnBox_Preferences)