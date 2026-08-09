import bpy
import os
from . import modules
PyBtnBox = modules

icon_in_blender = bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.keys()

AreaData = [['3D Viewport','VIEW3D'],
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

node_type_icons = {'0':'FILE_SCRIPT','1':'TOPBAR','2':'FILE_TEXT'}

class Layout_Tools:
    @staticmethod
    def space(layout,space_scale):
        row = layout.row(align=True)
        col_space = row.column()
        col_space.label(text='',icon='BLANK1')
        col_space.scale_x = space_scale
        return row.column()
    @staticmethod
    def split_2_row(layout,factor=0.5):
        split = layout.split(factor=factor)
        col_1 = split.column()
        col_1.alignment='RIGHT'
        col_2 = split.column()
        col_2.alignment='LEFT'
        return col_1,col_2
    
    @staticmethod
    def get_icon(icon_id,default):
        icon_in_blender = bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.keys()
        output_icon =  icon_id if icon_id in icon_in_blender else default
        return output_icon

class NodeLayout:
    @staticmethod
    def edit_opsBtns(Editor,Layout,nodeName):
        #row_ops = Layout.menu_pie()
        row_ops = Layout.row(align=True)
        if not (nodeName == Editor.btn_get):
            row_ops.operator( "pybtnbox.editor_node_active"   ,text=''  ,icon= "RADIOBUT_OFF" ).Btn=nodeName
        else:
            row_ops.operator( "pybtnbox.editor_node_active_cancel" ,text=''  ,icon= "RADIOBUT_ON" ,depress=True  )
        
        #row_ops.operator( "pybtnbox.editor_btn_funclist_current" ,text='',icon= "THREE_DOTS"  ).btn_name  = nodeName
        
    @staticmethod
    def nodetree_panel_header(header,nodeName,nodeData):
        row = header.row(align = True)
        
        # Tip Button 
        nodeIcon = nodeData.get('icon','QUESTION')
        nodeLabel = nodeData['label']

        row.label(text=nodeLabel,icon='NONE' if nodeIcon=='BLANK1' else nodeIcon)
            
        if nodeIcon != 'NONE':
            tipBtn = row.operator("pybtnbox.button_description",text='',icon='STATUS_INFO' ,emboss=False)
            tipBtn.btnName = nodeName
            tipBtn.text =nodeData['text']
        return
    
    @staticmethod
    def nodetree_button(Menu,layout,nodeName,nodeData,is_editor=True):
        # Tip Button
        row = layout.row(align = True)
        nodeIcon = nodeData.get('icon','QUESTION')
        if nodeIcon !='NONE':
            btnIcon = nodeIcon if nodeIcon in icon_in_blender else 'ERROR'
            tipBtn = row.operator("pybtnbox.button_description",text='',icon=btnIcon ,emboss=True)
            tipBtn.btnName = nodeName
            tipBtn.text =nodeData['text']

        # Operator Button
        btnText = nodeData['label'] if nodeData['label']!='' else ' '
        pyPath = os.path.join(Menu.get_menu_path(Menu.name),f'{nodeName[2:]}.py')
        ops_function = "pybtnbox.editor_btn_operator_menu" if is_editor else "pybtnbox.button_execute"
        row.operator(ops_function ,text= btnText).file_path = pyPath


        return row
    
    @staticmethod
    def nodetree_textbox(layout,nodeData):
        data_label = nodeData.get('label','')
        data_icon = nodeData.get('icon','ERROR')
        data_text = nodeData.get('text','')
        header_icon = data_icon if data_icon in icon_in_blender else 'ERROR'

        # Main Layout
        row_edit = layout.row(align=True)
        draw_panel=row_edit.menu_pie()
        draw_operators=row_edit.menu_pie()

        def tip_blocks(box_layout,data_text='',use_separator=False):
            if use_separator:
                box_layout.separator(factor=0.2, type='LINE')
            if data_text=='' :
                return draw_operators
            # TextBox Content
            for line in data_text.split('\n'):
                text = f'    {line}'
                box_layout.label(text=text,icon='NONE')

        # Text Box Panel
        has_icon = header_icon != 'NONE'
        has_label = data_label != ''
        has_tip = data_text != ''
         
        if not (has_icon | has_label ): # 只使用分割線
            if not has_tip:
                draw_panel = draw_panel.column()
                draw_panel.label(text=' ')
                draw_panel.scale_y = 0.45
                draw_panel.separator(factor=1, type='LINE')
                return draw_operators
            else:
                draw_box = draw_panel.box()
                draw_box = draw_box.column(align=True)
                tip_blocks(draw_box,data_text=data_text,use_separator=False)
                return draw_operators
        
        #  Header Layout
        draw_box = draw_panel.box().column(align=True)
        draw_box.row()
        row_label = draw_box.row()
        row_label.alignment='CENTER'
        row_label.label(text=data_label,icon=header_icon)
        if has_tip:
            tip_blocks(draw_box,data_text=data_text,use_separator=True)
        return draw_operators


    
    @staticmethod
    def draw_nodetree(Editor,layout,Menu,is_editor=True):
        # build Picker
        #Menu = PyBtnBox.Menu.from_menu_name(menuName)
        MenuData  = Menu.data
        menuLevel = MenuData.get('level',None)
        menuNode = MenuData.get('node',None)
        if not menuLevel or not menuNode : 
            return
        def picker_node_tree(pnl_name,pnl_layout):
            for node in menuLevel.get(pnl_name,[]):
                nodeData = menuNode.get(node,None)
                if not nodeData:
                    continue
                if node.startswith('1'): # SubPanel
                    pnl_id = f'pyBtnBox_{Menu.name}_{node}'
                    header,body = pnl_layout.panel(idname=pnl_id,default_closed=False)
                    NodeLayout.nodetree_panel_header(header,node,nodeData)
                    if is_editor:
                        NodeLayout.edit_opsBtns(Editor,header,node)

                    if not body:
                        continue
                    bodyColumn = Layout_Tools.space(body,space_scale=0.8)
                    picker_node_tree(node,bodyColumn)
                    continue

                if node.startswith('0'): # Button
                    col = Layout_Tools.space(pnl_layout,space_scale=0.5)
                    ops_layout = NodeLayout.nodetree_button(Menu,col,node,nodeData,is_editor)
                    if is_editor:
                        NodeLayout.edit_opsBtns(Editor,ops_layout,node)

                    continue
                    
                if node.startswith('2'): # TextBox
                    col = Layout_Tools.space(pnl_layout,space_scale=0.5)
                    ops_layout = NodeLayout.nodetree_textbox(col,nodeData)
                    if is_editor:
                        NodeLayout.edit_opsBtns(Editor,ops_layout,node)

                    continue
        
        picker_node_tree('_',layout)
        return
# { MENU }
class MenuLayout:
    @staticmethod
    def draw_panel(self,context,Menu_ID):
        Editor = context.scene.pybtnbox_prop_editor
        # Root 
        Pref = context.preferences.addons[__package__].preferences
        rootPathState = Pref.root_path_state()
        if rootPathState != 'PATH_FINE':
            box = self.layout.box()
            Pref.draw_root_path(box,rootPathState)
            return

        # Menu Picker
        pybtnbox_prop = context.scene.pybtnbox_prop
        folderName = pybtnbox_prop.get(Menu_ID,'')
        Menu = PyBtnBox.Menu.from_menu_name(folderName)        
        if not Menu : 
            row_menu = self.layout.row(align=True)
            row_menu.prop(pybtnbox_prop,Menu_ID,text='',icon='NONE')
            self.layout.label(text = 'No Found This Menu In Folder',icon='QUESTION')
            return
        
        layout = self.layout
        MenuData  = Menu.data
        menuIcon = Layout_Tools.get_icon( MenuData['icon'],'NONE') #MenuData['icon'] if MenuData['icon'] in icon_in_blender else 'NONE'
        row_menu = layout.row(align=True)
        row_menu.prop(pybtnbox_prop,Menu_ID,text='',icon=menuIcon)
        layout.separator(factor=2.0,type='LINE')

        # build panels
        col_node_tree = layout.column(align=True)
        NodeLayout.draw_nodetree(Editor, col_node_tree, Menu, is_editor=False)
        return

class Editor_Menu_Layout:
    @staticmethod
    def draw(self, context):
        # Menu Picker
        Editor = context.scene.pybtnbox_prop_editor
        MenuName = Editor.menu

        layout = self.layout
        Pref = context.preferences.addons[__package__].preferences
        rootPathState = Pref.root_path_state()
        if rootPathState != 'PATH_FINE':
            box = layout.box()
            Pref.draw_root_path(box,rootPathState)
            return
        
        # Menu Picker
        menu = PyBtnBox.Menu.from_menu_name(Editor.menu)
        row = layout.row()
        if not menu or MenuName =='':
            row.prop(Editor,'menu',text='',icon='NONE')
            row.operator("pybtnbox.editor_menu_funclist_current",text='', icon = "THREE_DOTS")
            return
        menuData = menu.data
        Icon = icon if PyBtnBox.is_icon_in_blender(icon :=menuData['icon']) else 'NONE'
        row.prop(Editor,'menu',text='',icon=Icon)
        row.operator("pybtnbox.editor_menu_funclist_current",text='', icon = "THREE_DOTS")
        
        if not MenuName in PyBtnBox.Root.load().menu_list():
            box = layout.box()
            row = box.row()
            row.alignment='CENTER'
            row.label(text='Not found this menu in folder',icon='ERROR')
            return
        layout.separator(factor=2.0,type="LINE")

        
        # Setting Area
        box = layout.box()
        row = box.row()
        row.alignment='CENTER'
        Icon = Editor.menu_icon
        if Icon in icon_in_blender:
            row.label(text='',icon=Icon)
        else :
            row.alert = True
            row.label(text='icon error',icon='ERROR')
        
        row = box.row()
        row.prop(Editor, "menu_name",text='Name')
        row = box.row()
        row.prop(Editor, "menu_icon",text='Icon')

        # Set Used Areas
        row = box.row()
        areaBox = row.box()
        header,body = areaBox.panel('menu_area_panel',default_closed=True)
        header.alignment='CENTER'
        header.label(text='Searched In')
        if body:
            areaBox_col = body.column(align=True)
            for i in range(13):
                areaBox_col.prop(Editor,'menu_useAreas',index=i,
                                text=AreaData[i][0],
                                icon=AreaData[i][1])
        # Update Button
        row = box.row()
        row.alignment='CENTER'
        row.operator("pybtnbox.editor_menu_update",text='Update')

        box.separator(factor=0.05)


class Editor_Node_Layout:
    @staticmethod
    def editBox_title(layout,nodeName):
        nodeName = nodeName
        type_icon = node_type_icons.get(nodeName[0],'NONE')
        row_title = layout.row()
        row_title.label(text = nodeName, icon = type_icon)
        row_title.operator( "pybtnbox.editor_node_active_cancel" ,text=''  ,icon= "PANEL_CLOSE"  )

    @staticmethod
    def editBox_operators(layout,nodeName):
        row_label,row_btns=Layout_Tools.split_2_row(layout,factor=0.225)
        
        row_label.label(text='Order')
        row_orderWalk = row_btns.row()
        btn_walk_U =row_orderWalk.operator( "pybtnbox.editor_node_order_walk" ,text='',icon= "TRIA_UP"  )
        btn_walk_U.Walk= 'up'
        btn_walk_U.nodeName= nodeName
        btn_walk_D =row_orderWalk.operator( "pybtnbox.editor_node_order_walk" ,text='',icon= "TRIA_DOWN"  )
        btn_walk_D.Walk= 'down'
        btn_walk_D.nodeName= nodeName

        row_orderWalk.operator( "pybtnbox.editor_node_change_panel" ,text='Switch Panel',icon= "OUTLINER"  ).btn_name=nodeName

        # Delete Node
        row_label.label(text='Delete')
        if nodeName.startswith('0'):
            row_btns.operator( "pybtnbox.editor_btn_del" ,text='Remove',icon= "TRASH"  ).node_name  = nodeName
        else :
            row_btns.operator( "pybtnbox.editor_node_del" ,text='Remove',icon= "TRASH"  ).node_name  = nodeName


    @staticmethod
    def editBox_dataEditor(Editor,layout):
        active_btn = Editor.btn_get
        # == Node Edit ==
        column = layout.column()
        column.label(text='Data Editor')

        # Show Icon
        row = column.row()
        row.alignment='CENTER'
        icon = Layout_Tools.get_icon(Editor.btn_icon,None)
        if icon :
            row.label(icon=icon)
        else :
            row.alert=True
            row.label(text ='Error Icon',icon='ERROR')

        # Node Data
        if active_btn.startswith('0'):
            col_icon_1,col_icon_2 = Layout_Tools.split_2_row(column,factor=0.225)
            col_icon_1.label(text='Name')
            col_icon_2.prop(Editor, "btn_name",text='')
            #column.separator(factor=2.0,type='LINE')

        col_icon_1,col_icon_2 = Layout_Tools.split_2_row(column,factor=0.225)
        col_icon_1.label(text='Icon')
        col_icon_2.prop(Editor, "btn_icon",text='')

        col_label_1,col_label_2 = Layout_Tools.split_2_row(column,factor=0.225)
        col_label_1.label(text='Label')
        col_label_2.prop(Editor, "btn_label",text='')
        #column.prop(Editor, "btn_text",text='Text')

        col_tip_1,col_tip_2 = Layout_Tools.split_2_row(column,factor=0.225)
        col_tip_1.label(text='Tip')
        col_tip_2.textbox(Editor, "btn_text")

        rowR = layout.row()
        rowR.alignment='CENTER'
        rowR.enabled = Editor.btn_name != ''
        rowR.operator("pybtnbox.editor_node_update",text="Update")
        layout.separator(factor=0.1)
        column.separator(factor=1)
        return 
    
    @staticmethod
    def edit_box(Layout,Editor):    
        active_btn = Editor.btn_get

        box = Layout.box()
        column = box.column()
        
        # Title
        Editor_Node_Layout.editBox_title(column,active_btn)
        column.separator(factor=2.0,type='LINE')
        Editor_Node_Layout.editBox_operators(column,active_btn)
        column.separator(factor=2.0,type='LINE')

        # == Node Edit ==
        Editor_Node_Layout.editBox_dataEditor(Editor,box)
        return
    


    
    @staticmethod
    def draw(self,context):
        Editor = context.scene.pybtnbox_prop_editor
        if Editor.btn_get !="":
            Editor_Node_Layout.edit_box(self.layout,Editor)
            self.layout.separator(factor=1.0, type='LINE')

        layout = self.layout
        #layout.separator(factor=1.0,type='LINE')
        layout.label(text='Button Picker')
        col_btnPicker = layout.column(align=True)
        # Add Button
        row_addBtn = col_btnPicker.row()
        row_addBtn.alignment = 'RIGHT'
        row_addBtn.operator("pybtnbox.editor_node_funclist_add",text='Add', icon = "PLUS")

        # build Picker
        
        Menu = PyBtnBox.Menu.from_menu_name(Editor.menu)
        NodeLayout.draw_nodetree(Editor, col_btnPicker, Menu, is_editor=True)
        return
        