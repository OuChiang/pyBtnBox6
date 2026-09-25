import bpy
from bpy_extras.io_utils import ImportHelper,ExportHelper
import os
import shutil

from . import modules
from . import panel_modules

PyBtnBox = modules
Panel = panel_modules.Layout_Tools


# Button Execute
class PYBTNBOX_OT_Btn_Execute(bpy.types.Operator):
    """Execute Python File"""
    bl_idname = "pybtnbox.button_execute"
    bl_label = "Button"
    file_path : bpy.props.StringProperty(default="")
    @classmethod
    def description(cls,context, properties):
        import os
        return f'Run {os.path.basename(properties.file_path)}\nExecute Python Script'
    
    def execute(self, context):
        btnPath = self.file_path
        if not os.path.isfile(btnPath):
            message = "File Not Found"
            self.report({'ERROR'}, message)
            return {'CANCELLED'}
        

        bpy.utils.execfile(filepath = btnPath)
        message = 'Button Executed'
        self.report({'OPERATOR'}, message)
        return {'FINISHED'}

# Button Description
class PYBTNBOX_OT_Btn_Description(bpy.types.Operator):
    """Show Description"""
    bl_idname = "pybtnbox.button_description"
    bl_label = 'Info'
    bl_description = 'Button Info'
    btnName: bpy.props.StringProperty(default="")
    text: bpy.props.StringProperty(default="")
    
    def execute(self, context):
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self)

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.scale_y=0.75
        for t in self.text.split('\n'):
            row = col.row()
            row.label(text=t)




#  == Editor ==

# [ Editor.Menu Editor ]
# < list > Menu Operators 
class PYBTNBOX_OT_Editor_Menu_Function_List_Current(bpy.types.Operator):
    """Current Menu's Operator list"""
    bl_idname = "pybtnbox.editor_menu_funclist_current"
    bl_label = "Menu Factions"  

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self)
    
    def draw(self, context):
        layout = self.layout
        layout.label(text='Current Menu')
        layout.operator("pybtnbox.editor_menu_new" ,text='New Empty Menu',icon= 'NEWFOLDER' )
        layout.operator("pybtnbox.editor_menu_open_folder" ,text='Open Menus Folder',icon= 'FILEBROWSER' )
        layout.operator("pybtnbox.editor_menu_del",text="Remove Menu",icon='TRASH')
        layout.operator("pybtnbox.load_settings_from_pybtnbox5_json",text="Load pyBtnBox5 Settings",icon='SETTINGS')

class PYBTNBOX_OT_Editor_Menu_New(bpy.types.Operator):
    """Create A New Empty Menu"""
    bl_idname = "pybtnbox.editor_menu_new"
    bl_label = "Add New Menu"

    def execute(self, context):
        Editor = context.scene.pybtnbox_prop_editor
        root = PyBtnBox.Root.load()
        NameBase = 'newMenu'
        nameNumber = 0
        menuName = NameBase + str(nameNumber)
        newMenuPath = os.path.join(root.path , menuName)
        while os.path.exists(newMenuPath):
            nameNumber += 1
            menuName = NameBase + str(nameNumber)       
            newMenuPath = os.path.join(root.path , menuName)
        try : 
            os.makedirs(newMenuPath)
        except:
            self.report({'ERROR'},'Error When Folder Create')
            return {'CANCELLED'}
        
        create_state = PyBtnBox.Menu.data_new(menuName)
        if not create_state in ['DATA_CREATED','DATA_ALREADY_EXISTED']:
            self.report({'ERROR'},create_state)
            return {'CANCELLED'}

        Editor.menu = menuName
        self.report({'INFO'},create_state)
        return {'FINISHED'}

class PYBTNBOX_OT_Editor_Menu_Open_Folder(bpy.types.Operator):
    """Open Current Menu Folder"""
    bl_idname = "pybtnbox.editor_menu_open_folder"
    bl_label = "Open Menu Folder"
    def execute(self, context):
        root = PyBtnBox.Root.load()
        os.startfile( root.path )
        return {'FINISHED'}

class PYBTNBOX_OT_Editor_Menu_Del(bpy.types.Operator):
    """Delete Current Menu"""
    bl_idname = "pybtnbox.editor_menu_del"
    bl_label = "Remove Menu"
    @classmethod
    def poll(cls, context):
        root = PyBtnBox.Root.load()
        Editor = context.scene.pybtnbox_prop_editor
        return Editor.menu in root.menu_list()

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def execute(self, context):
        root = PyBtnBox.Root.load()
        Editor = context.scene.pybtnbox_prop_editor
        menuName =Editor.menu
        menuPath = root.menu_path(menuName)
        
        try:
            shutil.rmtree(menuPath)
            self.report({'INFO',},f'{menuName} is already deleted')

        except PermissionError:
            self.report({'ERROR',},f'PermissionError: [WinError 5] Access is denied : {menuPath}')

        Editor.menu = ''
        return {'FINISHED'}
    
    def draw(self, context):
        Editor = context.scene.pybtnbox_prop_editor

        MenuName = Editor.menu
        layout = self.layout

        row = layout.row()
        row.alert = True
        row.label(text ='Delete Cannot Be Undo,Are You Sure?',icon = 'ERROR')

        row = layout.row()
        row.label(text=MenuName, icon="TRASH")


# Load pyBtnBox5 Json Layout
class PYBTNBOX_OT_load_settings_from_pybtnbox5_json(bpy.types.Operator):
    """Load Settings From pyBtnBox5 json"""
    bl_idname = "pybtnbox.load_settings_from_pybtnbox5_json"
    bl_label = "Load Old Settings"

    @classmethod
    def poll(cls, context):
        root = PyBtnBox.Root.load()
        Editor = context.scene.pybtnbox_prop_editor
        MenuName = Editor.menu
        menuPath = root.menu_path(MenuName)
        jsonPath = os.path.join(menuPath,'_menuData.json')
        return os.path.isfile(jsonPath)
    
    def execute(self, context):
        root = PyBtnBox.Root.load()
        Editor = context.scene.pybtnbox_prop_editor
        MenuName = Editor.menu
        menuPath = root.menu_path(MenuName)
        old_jsonPath = os.path.join(menuPath,'_menuData.json')
        import json
        with open( old_jsonPath, 'r') as f: 
            old_menuData = json.load(f)
        old_menuAttrs = old_menuData.get('__menuAttributes__',None)
        if not old_menuAttrs:
            return {'CANCELLED'}
        
        def get_old_nodeData():
            output_node = {}
            output_level = {'_':[]}
            temp_level_list = ['_'] 
            for nodeName,nodeData in old_menuData.items():
                if nodeName == "__menuAttributes__":
                    continue
                nodePanel = temp_level_list[-1]
                new_data ={
                    "icon": nodeData.get("icon","NONE"),
                    "label": nodeData.get("text",""),
                    "text": nodeData.get("tip",""),
                    "panel":nodePanel
                }

                node_typeID = nodeData.get('type',None)

                if node_typeID==0:# TEXT
                    new_name = f'2.{nodeName}'
                    output_level[nodePanel].append(new_name)

                elif node_typeID==1:# PANEL 
                    new_name = f'1.{nodeName}'
                    output_level[nodePanel].append(new_name)
                    output_level[new_name]=[]
                    temp_level_list.append(new_name)
                    
                elif node_typeID==2:# Return 
                    new_name = f'x.{nodeName}'
                    if temp_level_list[-1]!='_':
                        temp_level_list.pop()
                    continue
                else: # BUTTON
                    new_name = f'0.{nodeName}'
                    output_level[nodePanel].append(new_name)
                output_node[new_name] = new_data

            return output_node,output_level
        new_node,new_level = get_old_nodeData()


        new_menuData ={
            "ver": "pyBtnBox6",
            "icon": old_menuAttrs.get("icon","NONE"),
            "area": old_menuAttrs.get("area",[True for _ in range(14)]),
            "level" :new_level,
            "node":new_node
        }

        menu = PyBtnBox.Menu.from_menu_name(MenuName)
        menu.data = new_menuData
        menu.data_update()
        return {'FINISHED'}



# --menu edit--
# Menu Update
class PYBTNBOX_OT_Editor_Menu_Update(bpy.types.Operator):
    """Save Current Menu's Settings"""
    bl_idname = "pybtnbox.editor_menu_update"
    bl_label = "Rename Menu"
    @classmethod
    def poll(cls, context):
        Editor = context.scene.pybtnbox_prop_editor
        return Editor.menu_name
    def execute(self, context):
        Editor = context.scene.pybtnbox_prop_editor
        root = PyBtnBox.Root.load()
        OldName = Editor.menu
        NewName = Editor.menu_name
        # Save Menu Settings
        Menu = PyBtnBox.Menu.from_menu_name(OldName)
        Menu.data['icon'] = Editor.menu_icon
        Menu.data['area'] = list(Editor.menu_useAreas)
        # output json
        import json
        jsonPath = PyBtnBox.Menu.get_data_path(OldName)
        with open( jsonPath , 'w+') as f:
            json_data = json.dumps(Menu.data, indent=4)
            f.write(json_data)

        OldNamePath = os.path.join(root.path , OldName)
        NewNamePath = os.path.join(root.path , NewName)
        
        os.rename(OldNamePath,NewNamePath)

        Editor.menu = NewName
        
        self.report({'OPERATOR',},f'Menu Saved : {NewName}')
        return {'FINISHED'}
    

# [ Editor.Node Picker ]

# < 新增節點選單 >
# <list operators> Node Add
class PYBTNBOX_OT_Editor_Node_Function_List_Add(bpy.types.Operator):
    """Add Node Operators List"""
    bl_idname = "pybtnbox.editor_node_funclist_add"
    bl_label = "Create Button"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self)
    
    def draw(self, context):
        layout = self.layout
        layout.label(text='Add Button Node')
        layout.operator("pybtnbox.add_btn_empty",text='Empty Button',icon='FILE_NEW')
        layout.operator("pybtnbox.add_btn_from_current_text",text='From Current Text',icon='TEXT')

        layout.separator(factor=1.0, type='LINE')
        layout.label(text='Add Layout Node')
        layout.operator("pybtnbox.add_new_node",text='New Panel',icon='TOPBAR').node_type = 'PANEL'
        layout.operator("pybtnbox.add_new_node",text='New TextBox',icon='WORDWRAP_ON').node_type = 'TEXTBOX'
        
        
class PYBTNBOX_OT_Editor_Btn_New(bpy.types.Operator):
    """Add A New Button"""
    bl_idname = "pybtnbox.add_btn_empty"
    bl_label = "Add New Btn"

    def execute(self, context):
        # 導入方法
        Editor = context.scene.pybtnbox_prop_editor
        root = PyBtnBox.Root.load()
        MenuPath = root.menu_path(Editor.menu)
        Menu = PyBtnBox.Menu.from_menu_name(Editor.menu)

        # 創建新按鍵
        num = 0
        btnName = f'newBtn_{num}.py'
        newPath = os.path.join(MenuPath , btnName)
        while os.path.exists(newPath):
            num+=1
            btnName = f'newBtn_{num}.py'
            newPath = os.path.join(MenuPath , btnName)
        with open( newPath , 'w+') as f:
            f.write('')

        # 設定按鍵預設
        btnData = {
            'icon' : 'SCRIPTPLUGINS',
            'label' : f'newBtn_{num}' ,
            'text': '',
            'panel': '_'
            }
        Menu.data["node"][f"0.newBtn_{num}"] = btnData

        Menu.data_update()
        return {'FINISHED'}
    
class PYBTNBOX_OT_Editor_Btn_AddFromCurrentText(bpy.types.Operator):
    """Add New Button From Current Text"""
    bl_idname = "pybtnbox.add_btn_from_current_text"
    bl_label = "Add From current Text"

    @classmethod
    def poll(cls, context):
        Editor = context.scene.pybtnbox_prop_editor
        currentText = context.space_data.text
        return currentText and Editor.menu_name
    
    def execute(self, context):
        Editor = context.scene.pybtnbox_prop_editor
        Menu = PyBtnBox.Menu.from_menu_name(Editor.menu)
        MenuPath = PyBtnBox.Menu.get_menu_path(Editor.menu)
        # 若沒有Text，則取消
        currentText = context.space_data.text
        if not currentText:
            return {'CANCELLED'}
        
        # --獲取新名稱
        base_name  = currentText.name
        if base_name.endswith('.py'):
            base_name  = base_name[:-3]

        # 若已有該py檔案，則替換成新名字
        num = 0
        newLabel = base_name
        newPath = os.path.join(MenuPath , f'{base_name}.py')
        while os.path.exists(newPath):
            num+=1
            newLabel = f'{base_name}_{num}'
            newPath = os.path.join(MenuPath , f'{base_name}_{num}.py')

        # 另存檔案
        btnData = {
            'icon' : 'SCRIPTPLUGINS',
            'label' : newLabel ,
            'text': '',
            'panel': '_'
            }
        Menu.data["node"][f"0.{newLabel}"] = btnData
        bpy.ops.text.save_as(filepath=newPath)
        Menu.data_update()
        return {'FINISHED'}

class PYBTNBOX_OT_Editor_Node_New(bpy.types.Operator):
    """Add A New UI Node"""
    bl_idname = "pybtnbox.add_new_node"
    bl_label = "Add New Layout"
    node_type : bpy.props.StringProperty(default="PANEL")
    def execute(self, context):
        node_type_num = {"PANEL":'1',"TEXTBOX":'2'}
        typeNum = node_type_num.get(self.node_type,'1')
        # 導入方法
        Editor = context.scene.pybtnbox_prop_editor
        Menu = PyBtnBox.Menu.from_menu_name(Editor.menu)
        
        # 創建新按鍵
        num = 0
        nodeName = f'{typeNum}.{num}'
        while Menu.data['node'].get(nodeName,None):
            num+=1
            nodeName = f'{typeNum}.{num}'
            
        # 設定按鍵預設
        nodeData = {
            'icon' : 'NONE',
            'label' : self.node_type ,
            'text': '',
            'panel': '_'
            }
        Menu.data["node"][nodeName] = nodeData

        Menu.data_update()
        return {'FINISHED'}
    
# Active
class PYBTNBOX_OT_Editor_Node_Active(bpy.types.Operator):
    """Edit This Button"""
    bl_idname = "pybtnbox.editor_node_active"
    bl_label = "Editor Get Btn"
    Btn : bpy.props.StringProperty(default="")

    def execute(self, context):
        Editor = context.scene.pybtnbox_prop_editor
        Menu = PyBtnBox.Menu.from_menu_name(Editor.menu)
        #Data = Menu.json
        Data = Menu.data
        BtnData = Data['node'].get(self.Btn,None)
        if not BtnData:
            print(f'no found button {self.Btn}')
            return {'FINISHED'}
        
        #BtnIsUI = BtnData.get("is_ui",False)
        BtnType = BtnData.get("type",0)
        BtnLabel = BtnData.get("label",'')
        BtnIcon = BtnData.get("icon",'NONE')
        BtnText  = BtnData.get("text",'')
        btnEd = context.scene.pybtnbox_prop_editor
        btnEd.btn_get  =self.Btn
        btnEd.btn_name =self.Btn[2:]
        btnEd.btn_label =BtnLabel
        btnEd.btn_icon =BtnIcon
        btnEd.btn_text  =BtnText
        #btnEd.btn_is_ui = BtnIsUI
        btnEd.btn_type =str(BtnType)
        btnEd.menu_del_bool = False
        btnEd.btn_del_bool = False
        return {'FINISHED'}

class PYBTNBOX_OT_Editor_Node_Active_Cancel(bpy.types.Operator):
    """Cancel Button Edit"""
    bl_idname = "pybtnbox.editor_node_active_cancel"
    bl_label = "Button Editor Cancel"
    def execute(self, context):
        context.scene.pybtnbox_prop_editor.btn_get=''
        return {'FINISHED'}


# <list> editor button
class PYBTNBOX_OT_Editor_Btn_Operator_Menu(bpy.types.Operator):
    """Function list for current button"""
    bl_idname = "pybtnbox.editor_btn_operator_menu"
    bl_label = "Button Functions"
    
    file_path : bpy.props.StringProperty(default="")
    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self,width=150)
    def draw(self, context):
        layout = self.layout
        layout.scale_x = 0.5
        layout.operator( 'text.open' ,text='Load To Text Editor',icon= "APPEND_BLEND"  ).filepath  = self.file_path #self.pyPath

             
# [Editor.Node Edit]
# Panel Walk
class PYBTNBOX_OT_Editor_Node_OrderWalk(bpy.types.Operator):
    """Node Walk Up or Down Index in Panel"""
    bl_idname = "pybtnbox.editor_node_order_walk"
    bl_label = "Button Walk"
    Walk : bpy.props.StringProperty(default="up")
    nodeName : bpy.props.StringProperty(default="")
    def execute(self, context):
        Editor = context.scene.pybtnbox_prop_editor
        MenuName = Editor.menu
        Menu = PyBtnBox.Menu.from_menu_name(MenuName)
        menuData = Menu.data
        nodeData = menuData['node'].get(self.nodeName)
        
        if not nodeData:
            return {'CANCELLED'}
        nodePanel = nodeData.get('panel')
        if not nodeData:
            return {'CANCELLED'}
        
        levels = menuData['level']
        btnList = levels.get(nodePanel,[])

        Index=0
        for i in range(len(btnList)):
            if btnList[i] == self.nodeName:
                Index=i
        if 0 <= Index < len(btnList):
            if   self.Walk =='up':
                btnList.pop(Index)
                btnList.insert( Index-1 , self.nodeName )
            if self.Walk =='down':
                btnList.pop(Index)
                btnList.insert( Index+1 , self.nodeName )
        
        Menu.data_update()
        return {'FINISHED'}
    
class PYBTNBOX_OT_Editor_Node_ChangePanel_SelectTarget(bpy.types.Operator):
    """Select Change Panel Target"""
    bl_idname = "pybtnbox.editor_node_change_panel_target"
    bl_label = "Button Set Panel"
    pnl_name : bpy.props.StringProperty(default="")
    def execute(self, context):
        Editor = context.scene.pybtnbox_prop_editor
        Editor.btn_set_panel = self.pnl_name
        if Editor.btn_set_panel == '':
            return {'CANCELLED'}

        return {'FINISHED'}

class PYBTNBOX_OT_Editor_Node_ChangePanel(bpy.types.Operator):
    """Button Picker"""
    bl_idname = "pybtnbox.editor_node_change_panel"
    bl_label = "Outliner Move"
    #pnl_name : bpy.props.StringProperty(default="_")
    btn_name : bpy.props.StringProperty(default="")

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def execute(self, context):
        Editor = context.scene.pybtnbox_prop_editor
        Menu = PyBtnBox.Menu.from_menu_name(Editor.menu)
        Menu.update_data_panel(Editor.get('btn_set_panel',''),self.btn_name)
        Editor.btn_set_panel = ''
        return {'FINISHED'}
    
    def cancel(self, context):
        Editor = context.scene.pybtnbox_prop_editor
        #self.report({'INFO'},self.btn_name)
        Editor.btn_set_panel = ''
        return None

    def draw(self,context):
        layout = self.layout
        nodeName = self.btn_name
        type_icons = {'0':'FILE_SCRIPT','1':'OUTLINER','2':'FILE_TEXT'}
        type_icon = type_icons.get(nodeName[0],'NONE')
        row_node_label = layout.row()
        row_node_label.alignment='CENTER'
        row_node_label.label(text = nodeName[2:], icon = type_icon)

        # build panels
        Editor = context.scene.pybtnbox_prop_editor
        Menu = PyBtnBox.Menu.from_menu_name(Editor.menu)
        levels = Menu.data.get('level',None)
        nodes = Menu.data.get('node',None)
        if not (levels and nodes) :
            return

        # Show Set To Panel Name 
        picker_pnl = layout.column(align=True)
        row = picker_pnl.row(align=True)
        pie_label = row.menu_pie()
        pie_label.label(text = 'Set To Panel')

        pie_pnl_name = row.menu_pie()
        set_pnl = getattr(Editor,'btn_set_panel')
        pnl_data = nodes.get(set_pnl,None)
        pnl_name = pnl_data['label'] if pnl_data else set_pnl
        pie_pnl_name.label(text = pnl_name)
        
        # Build Panel Tree
        
        parent_trees = Menu.get_parent_trees()
        tabs = { key:len(value) for key,value in parent_trees.items() if key.startswith('1') }


        node_data = nodes.get(self.btn_name,None)
        if not node_data : 
            return
        node_panel = node_data['panel']


        panel_children = Menu.get_children_tree(self.btn_name)
        is_panel = self.btn_name.startswith('1')
        
        # Panel List 
        def frist_row(layout):
            row= layout.row(align=True)
            if node_panel != '_':
                btn_depress = Editor.btn_set_panel == '_' 
                btn_set_pnl =row.operator( "pybtnbox.editor_node_change_panel_target"   ,text='_'  ,icon= "FILE_FOLDER_LARGE" ,depress=btn_depress)
                btn_set_pnl.pnl_name = '_'
            else:
                row.enabled = False
                row.label( text='_'  ,icon= "FILE_FOLDER_LARGE")


        def row_disable(Layout,node):
            nodeData = nodes.get(node,None)
            if not nodeData : 
                return
            row= Layout.row(align=True)
            row.enabled = False
            row_pick = Panel.space(row,space_scale=tabs[node]*2 )
            label = nodeData['label'] if nodeData['label']!='' else ' '
            row_pick.label(text=label, icon= "FILE_FOLDER_LARGE")

        def row_enable(Layout,node):
            nodeData = nodes.get(node,None)
            if not nodeData : 
                return
            row= Layout.row(align=True)
            row.enabled = not node in ( self.btn_name, node_panel)
            btn_depress = Editor.btn_set_panel == node
            row_pick = Panel.space(row,space_scale=tabs[node]*2 )
            label = nodeData['label'] if nodeData['label']!='' else ' '
            btn_set_pnl =row_pick.operator( "pybtnbox.editor_node_change_panel_target", text=label, icon= "FILE_FOLDER_LARGE", depress=btn_depress)
            btn_set_pnl.pnl_name = node

        if is_panel:
            condition_panel_enable =lambda node :(node in ( self.btn_name, node_panel)) or (node in panel_children)
        else:
            condition_panel_enable =lambda node :node == node_panel
        def build_panel_row(pnl_name):
            for node in levels.get(pnl_name,[]):
                if not node.startswith('1') : 
                    continue
                if condition_panel_enable(node): 
                    row_disable(picker_pnl,node)
                    build_panel_row(node)
                else:
                    row_enable(picker_pnl,node)
                    build_panel_row(node)
        frist_row(picker_pnl)
        build_panel_row('_')

        return

# Delete
class PYBTNBOX_OT_Editor_Btn_Del(bpy.types.Operator):
    """Delete This Button"""
    bl_idname = "pybtnbox.editor_btn_del"
    bl_label = "Remove Btn"
    node_name : bpy.props.StringProperty(default="")

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def execute(self, context):
        Editor = context.scene.pybtnbox_prop_editor
        Editor.btn_get=''
        menuName = Editor.menu
        Menu = PyBtnBox.Menu.from_menu_name(menuName) 
        menuPath = PyBtnBox.Menu.get_menu_path(menuName)
        fileName = self.node_name[2:]
        btnPath = os.path.join(menuPath,f'{fileName}.py')
        try:
            os.remove(btnPath)
        except FileNotFoundError:
            self.report({'ERROR'},f'File path is not exist : {btnPath}')
        Menu.data_update()
        self.report({'INFO'},f'{fileName} Removed')
        
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.alignment='CENTER'
        row.label(text ='Are You Sure To Delete The Button?',icon="TRASH")

class PYBTNBOX_OT_Editor_Node_Del(bpy.types.Operator):
    """Delete This Node"""
    bl_idname = "pybtnbox.editor_node_del"
    bl_label = "Remove Btn"
    node_name : bpy.props.StringProperty(default="")

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def execute(self, context):
        nodeName = self.node_name
        Editor = context.scene.pybtnbox_prop_editor
        Editor.btn_get=''
        menuName = Editor.menu
        Menu = PyBtnBox.Menu.from_menu_name(menuName) 

        nodes = Menu.data['node']
        if not nodes.get(nodeName):
            return {'CANCELLED'}
        nodePanel = nodes[nodeName]['panel']

        if nodeName.startswith('2') :
            del Menu.data['node'][nodeName]
            Menu.data['level'][nodePanel].remove(nodeName)
            
            Menu.data_update()
            self.report({'INFO'},f'TextBox Removed')
            return {'FINISHED'}

        if nodeName.startswith('1') :
            nodePanel = nodes[nodeName].get('panel','_')

            newNodes = {}
            for ndName,ndData in nodes.items():
                if ndName == self.node_name:
                    continue
                if ndData['panel'] == nodeName:
                    ndData['panel'] = nodePanel
                newNodes[ndName] = ndData
            Menu.data['node'] = newNodes

            levels = Menu.data['level']
            nodeKids = levels.get(nodeName,None)
            oldLevel =levels.get(nodePanel,None)
            

            newLevel = []
            for node in oldLevel:
                if node != nodeName:
                    newLevel.append(node)
                else:
                    for nodeKid in nodeKids:
                        newLevel.append(nodeKid)
            levels[nodePanel] = newLevel
            del levels[nodeName]
            Menu.data['level'] = levels
            print(Menu.data)

            Menu.data_update()
            self.report({'INFO'},f'Panel Removed')
            
            return {'FINISHED'}
    
        return {'CANCELLED'}
    
    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.alignment='CENTER'
        row.label(text ='Are You Sure To Delete The Button?',icon="TRASH")



# Button Update
class PYBTNBOX_OT_Editor_Node_Update(bpy.types.Operator):
    """Save Edited Button Settings"""
    bl_idname = "pybtnbox.editor_node_update"
    bl_label = "Editor Reset Btn"

    def execute(self, context):
        Editor = context.scene.pybtnbox_prop_editor
        oldName = Editor.btn_get
        typeNum = oldName[0]
        newName = f'{typeNum}.{Editor.btn_name}'
        # Old Data
        Menu  = PyBtnBox.Menu.from_menu_name(Editor.menu)
        oldData = Menu.data["node"].get(oldName,None)
        if not oldData:
            return {'CANCELLED'}
        nodePanel = oldData.get('panel','_')

        # 修改節點
        nodes = Menu.data["node"]
        del nodes[oldName]
        # [面板] : 更改各節點面板屬性
        if oldName.startswith('1') :
            for nd_name,nd_data in nodes.items():
                if nd_data["panel"] == oldName:
                    nodes[nd_name]["panel"] = newName
        nodes[newName] = { 
            "icon"  : Editor.get('btn_icon','NONE'),
            "label" : Editor.get('btn_label',''),
            "text"  : Editor.get('btn_text',''),
            "panel" : nodePanel 
            }
        Menu.data["node"] = nodes

        # 修改階層
        ## 修改其父面板階層
        levels = Menu.data["level"]
        newPanelLevel = []
        for nd in levels[nodePanel]:
            if nd != oldName :
                newPanelLevel.append(nd)
            else :
                newPanelLevel.append(newName)
        levels[nodePanel] = newPanelLevel

        # [ 面板 ] : 更新該節點階層
        if oldName.startswith('1') :
            oldLevel = levels.get(oldName)
            del levels[oldName]
            levels[newName] = oldLevel

        Menu.data["level"] = levels

        # 更新python檔案
        if oldName.startswith('0') :
            menuPath = PyBtnBox.Menu.get_menu_path(Editor.menu)
            if oldName != newName: 
                oldPyPath = os.path.join( menuPath, f'{oldName[2:]}.py')
                newPyPath = os.path.join( menuPath, f'{newName[2:]}.py')
                os.rename(oldPyPath,newPyPath)
        print(Menu.data)
        # 完成
        Menu.data_update()
        Editor.btn_get = ''
        self.report({'OPERATOR',},f'Button Saved : {Editor.btn_name}')
        return {'FINISHED'}



    
""""""""" Register """""""""
class_list=[
    # [System]
    PYBTNBOX_OT_load_settings_from_pybtnbox5_json,
    # [Main]
    PYBTNBOX_OT_Btn_Execute,
    PYBTNBOX_OT_Btn_Description,
    
    # [Editor]
    # [Editor.Menu Edit]
    # <list> menu operators
    PYBTNBOX_OT_Editor_Menu_Function_List_Current,
    PYBTNBOX_OT_Editor_Menu_New,
    PYBTNBOX_OT_Editor_Menu_Open_Folder,
    PYBTNBOX_OT_Editor_Menu_Del,
    # update
    PYBTNBOX_OT_Editor_Menu_Update,

    # [Editor.Node Picker]
    # <list> node add 
    PYBTNBOX_OT_Editor_Node_Function_List_Add,
    PYBTNBOX_OT_Editor_Btn_New,
    PYBTNBOX_OT_Editor_Btn_AddFromCurrentText,
    PYBTNBOX_OT_Editor_Node_New,
    # active
    PYBTNBOX_OT_Editor_Node_Active,
    PYBTNBOX_OT_Editor_Node_Active_Cancel,
    # <list> editor button
    PYBTNBOX_OT_Editor_Btn_Operator_Menu,

    # [Editor.Node Edit]
    # panel walk
    PYBTNBOX_OT_Editor_Node_OrderWalk,
    PYBTNBOX_OT_Editor_Node_ChangePanel_SelectTarget,
    PYBTNBOX_OT_Editor_Node_ChangePanel,
    # del
    PYBTNBOX_OT_Editor_Btn_Del,
    PYBTNBOX_OT_Editor_Node_Del,
    # update
    PYBTNBOX_OT_Editor_Node_Update,

    ]    

def register():
    for cls in class_list:
        bpy.utils.register_class(cls)



def unregister():
    for cls in class_list:
        bpy.utils.unregister_class(cls)

