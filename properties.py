import bpy
import os

from . import modules
PyBtnBox = modules

def menu_search_filter(self,context,edit_text,menu_id):
    output_list = []
    root = PyBtnBox.Root.load()
    for menuName in root.menu_list():
        menu = PyBtnBox.Menu.from_menu_name(menuName)
        areas = menu.data.get('area',[True for _ in range(13)])
        if areas[menu_id]:
            output_list.append(menuName)
    return output_list
def menu_update_use_id(self,context,menu_id):
    #print(menu_id)
    menu_id = f"Menu_area_{menu_id}"
    def menu_update(self,context):
        folder_name = getattr(self,menu_id,'')
        if folder_name not in PyBtnBox.Root.load().menu_list():
            return None
        
        menu = PyBtnBox.Menu.from_menu_name(folder_name)
        menu.data_update()
        return None
    return menu_update(self,context)

# Properties
class PYBTNBOX_Prop(bpy.types.PropertyGroup):
    def add_menu_enum(menu_id):
        return  bpy.props.StringProperty(
            name=f"Menu_{menu_id}" ,
            description="Select Menu",
            search = lambda self,context,edit_text:menu_search_filter(self,context,edit_text,menu_id),
            update = lambda self,context:menu_update_use_id(self,context,menu_id),
            search_options ={'SUGGESTION'}
            )
    Menu_area_0 : add_menu_enum(0)
    Menu_area_1 : add_menu_enum(1)
    Menu_area_2 : add_menu_enum(2)
    Menu_area_3 : add_menu_enum(3)
    Menu_area_4 : add_menu_enum(4)
    Menu_area_5 : add_menu_enum(5)
    Menu_area_6 : add_menu_enum(6)
    Menu_area_7 : add_menu_enum(7)    
    Menu_area_8 : add_menu_enum(8)
    Menu_area_9 : add_menu_enum(9)
    Menu_area_10 : add_menu_enum(10)
    Menu_area_11 : add_menu_enum(11)
    Menu_area_12 : add_menu_enum(12)
    #Menu_area_13 : add_menu_enum(13)


def menu_update(self,context):
    folder_name = self.menu
    if folder_name not in PyBtnBox.Root.load().menu_list():
        return None
    
    menu = PyBtnBox.Menu.from_menu_name(folder_name)
    menuData = menu.data_update()
    self.menu_name = menu.name
    self.menu_icon = menuData['icon']
    for i in range(14):
        self.menu_useAreas[i] = menuData['area'][i]
    
    # Update Btn Edit
    self.btn_get=''
    return None

def menu_search(self, context, edit_text):
    return PyBtnBox.Root.load().menu_list()


# PyBtnBox Editor Props
class PYBTNBOX_Prop_Editor(bpy.types.PropertyGroup):

    menu : bpy.props.StringProperty(
        name="Menu",
        description='Select Edit Menu',
        update = menu_update,
        search = menu_search,
        search_options ={'SUGGESTION'}
        )
    
    menu_name: bpy.props.StringProperty(name="Menu Rename",
                                        description="Reset Menu Name",
                                        default='')
    menu_icon: bpy.props.StringProperty(name="Menu Icon",
                                        description="Reset Menu Icon",
                                        default='')
    menu_useAreas_option : bpy.props.BoolProperty(name="Areas Use",
                                                  description="Show Menu Reset Areas",
                                                  default=False)
    menu_useAreas : bpy.props.BoolVectorProperty(
        name="Areas Use",
        description="Reset Menu Used Areas",
        size=14
        )

    # Button Edit Props
    btn_get: bpy.props.StringProperty(name="Btn Name",
                                      description="Show Button In Edit Options",
                                      default="")
    btn_name: bpy.props.StringProperty(name="Btn Rename",
                                       description="Reset The python file Name",
                                       default="")
    btn_label: bpy.props.StringProperty(name="Btn Label",
                                       description="Reset The Button Label Text", 
                                       default="")
    btn_icon: bpy.props.StringProperty(name="Btn Icon", 
                                       description="Reset The Button Icon", 
                                       default="")
    btn_text: bpy.props.StringProperty(name="Btn Text", 
                                       description="Reset The Button Tip", 
                                       default="")
    btn_use_tip : bpy.props.BoolProperty(name="Btn Use Tip Text", 
                                         default=True)
    btn_set_panel : bpy.props.StringProperty(name="Btn Set Panel", 
                                       description="Set The Button To Panel", 
                                       default="")
class_list = []
def register():
    bpy.utils.register_class(PYBTNBOX_Prop)
    bpy.utils.register_class(PYBTNBOX_Prop_Editor)
    bpy.types.Scene.pybtnbox_prop = bpy.props.PointerProperty(type=PYBTNBOX_Prop)
    bpy.types.Scene.pybtnbox_prop_editor = bpy.props.PointerProperty(type=PYBTNBOX_Prop_Editor)
    
    for cls in class_list:
        cls.register()


def unregister():

    class_list.reverse()
    for cls in class_list:
        cls.unregister()
    del bpy.types.Scene.pybtnbox_prop
    del bpy.types.Scene.pybtnbox_prop_editor
    bpy.utils.unregister_class(PYBTNBOX_Prop)
    bpy.utils.unregister_class(PYBTNBOX_Prop_Editor)