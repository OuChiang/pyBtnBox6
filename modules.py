import bpy
import os
import json
preferences = bpy.context.preferences.addons[__package__].preferences
AreaData = [['3D Viewport','VIEW3D'],
            ['Image Editor','IMAGE'],
            ['UV Editor','UV'],
            ['Compositor','NODE_COMPOSITING'],
            ['Texture Node Editor','NODE_TEXTURE'],
            ['Geometry Node Editor','GEOMETRY_NODES'],
            ['Shader Editor','SHADING_RENDERED'],
            ['Video Sequencer','SEQUENCE'],
            ['Dope Sheet','ACTION'],
            ['Timeline','TIME'],
            ['Graph Editor','GRAPH'],
            ['Drivers','DRIVER'],
            ['Nonlinear Animation','NLA'],
            ['Text Editor','TEXT']]
def is_icon_in_blender(iconName):
    items = bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.keys()
    
    return iconName in items

def get_script_folder_root():
    addon_prefs = bpy.context.preferences.addons[__package__].preferences
    if not addon_prefs:
        return ''
    
    rootPath = getattr(addon_prefs,'root_path')
    dir_base_name = os.path.basename(os.path.dirname(rootPath))
    if not dir_base_name.startswith('pybtnbox_menus'):
        return ''
    if not os.path.exists(rootPath):
        return ''
    return rootPath

class Root:
    def __init__(self,path,state):
        self.path = path
        self.state = state
    @classmethod
    def load(cls):
        preferences = bpy.context.preferences.addons[__package__].preferences
        rootPath = getattr(preferences,'root_path')
        rootPathState = preferences.root_path_state()
        return cls(rootPath,rootPathState)

    
    def menu_list(self):
        if self.state != 'PATH_FINE':
            return []
        rootPath = self.path
        return [d for d in os.listdir( rootPath ) if os.path.isdir( os.path.join(rootPath,d))]
    
    def menu_path(self,menu_name):
        if self.state != 'PATH_FINE':
            return ''
        menuPath = os.path.join(self.path,menu_name)
        if not os.path.isdir(menuPath):
            return ''
        return menuPath
    def menu_data_path(self,menu_name):
        menuPath = self.menu_path(menu_name)
        dataPath = os.path.join(menuPath,'.menuData.json')
        if not os.path.exists(dataPath):
            return ''
        return dataPath

default_menuData = {
    'ver' : 'pyBtnBox6',
    'icon' : 'NONE',
    'area' : [True for i in range(14)] ,
    'level': {'_':[]},
    'node': {}
    }

default_nodeData = {
    'icon' : 'NONE',
    'label' : '' ,
    'text': '',
    'panel': '_'
    }

class Menu:
    def __init__(self,name,data):
        self.name = name
        self.data = data

    @classmethod
    def from_menu_name(cls,menuName):
        if Menu.get_menu_path(menuName)=='':
            return None
        # Menu存在，但Json檔案不存在
        dataPath = Menu.get_data_path(menuName)
        if not dataPath:
            Menu.data_new(menuName)
            return cls(menuName,default_menuData)
        if not os.path.exists(dataPath):
            return cls(menuName,default_menuData)

        # 獲取Json資料，若缺少Key則使用預設值
        with open( dataPath, 'r') as f: 
            menuData = json.load(f)
        define_data = {}
        for key,value in default_menuData.items():
            define_data[key] = menuData[key] if menuData.get(key,None) else value

        return cls(menuName,define_data)
    
    @staticmethod
    def data_new(menuName):
        # Menu不存在
        if Menu.get_menu_path(menuName) == '':
            return 'NO_FOUND_MENU'
        
        jsonPath = Menu.get_data_path(menuName)
        if not jsonPath or not os.path.exists(jsonPath):
            json_data = json.dumps(default_menuData, indent=4)
            with open( jsonPath, 'w+') as f:
                f.write(json_data)
            return 'DATA_CREATED'
        return 'DATA_ALREADY_EXISTED'

    def update_data_panel(self,panel_name,btn_name):
        menuData = self.data
        nodes = menuData.get('node',None)
        levels = menuData.get('level',None)
        if not (nodes and levels):
            print(f'no found : nodes or levels')
            return False
        
        # Set Data
        btn_data = nodes.get(btn_name,None)
        if not btn_data:
            print(f'no found : {btn_data}')
            return False
        old_panel = btn_data.get('panel','_')
        btn_data['panel'] = panel_name

        # Set Level
        old_level_kids = levels.get(old_panel,[])
        if panel_name in old_level_kids:
            old_level_kids.remove(btn_name)
        new_level_kids = levels.get(panel_name,[])
        if not panel_name in new_level_kids:
            new_level_kids.append(btn_name)

        #self.data = menuData

        # Ouput Json
        jsonPath = self.get_data_path(self.name)
        json_data = json.dumps(self.data, indent=4)
        with open( jsonPath, 'w+') as f:
            f.write(json_data)
        self.data_update()
        
        #print(f'{btn_name} : level changed to {panel_name}')
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1) 
        #bpy.context.view_layer.update()
        return 
    '''
    @staticmethod
    def data_get(menuName):
        menuPath =Menu.path(menuName)
        if menuPath=='':
            return
        jsonPath = os.path.join(menuPath,'.menuData.json')
        with open( jsonPath, 'r') as f: 
            data = json.load(f)
        return data
    '''
    def data_update(self):
        menuPath = Menu.get_menu_path(self.name)
        if menuPath =='': # 沒有找到Json檔案
            print(f'menu {self.name} no update : cuase data path not found ')
            return
        
        # 獲取舊資料內各{節點}與{層級}
        old_data = self.data
        old_nodes = old_data.get('node', {} )

        # 檢查與重建{節點}
        def rebuild_node():
            # 從舊節點中獲取{面板}與{文字}資料
            new_node = {k:v for k,v in old_nodes.items() if k[0] in ['1','2']}

            # 依Menu內檔案，從舊資料中取得{按鈕}，沒有使用預設
            pyFiles = self.get_pyFiles(self.name,mode='base')
            for pyFile in pyFiles:
                btn_key = f'0.{pyFile}'
                btn_data = old_nodes.get(btn_key,None)
                if btn_data:
                    new_node[btn_key] = { k:btn_data.get(k,v) for k,v in default_nodeData.items() }
                else :
                    new_node[btn_key] = default_nodeData

            return new_node
    
        # 重構{層級}
        def rebuild_level(new_node):
            old_level = old_data.get('level', {'_':[]} )
            newNodeList = new_node.keys()

            # 獲取舊資料
            temp_level = {k:old_level.get(k,[]) for k in newNodeList if k.startswith('1')}
            temp_level['_'] = old_level.get('_',[])

            # 從各階層中移除多於節點
            for pnl_name,pnl_kids in temp_level.items():
                temp_kids = []
                for node in pnl_kids:
                    if not node in newNodeList:
                        continue
                    if node in temp_kids:
                        continue
                    node_panel = new_node[node].get('panel')
                    if node_panel == pnl_name:
                        temp_kids.append(node)
                        continue
                temp_level[pnl_name] = temp_kids

            # 將節點新增進{層級面板}中
            for node_name,node_data in new_node.items():
                node_parent = node_data.get('panel','_')
                level = temp_level.get(node_parent)
                if not level:
                    node_data['panel'] = '_'
                    level = []
                if not node_name in level:
                    temp_level['_'].append(node_name)

            return new_node,temp_level


        # 創建新節點資料
        new_node = rebuild_node()
        #X 創建新階層資料 <-- 從舊節點資料導入階層
        #X new_level,new_node = update_level_node_relationship(new_node)
        # 重構{階層}資料
        new_node,new_level = rebuild_level(new_node)

        # 導出新資料
        new_data = {} 
        new_data['ver'] = old_data.get('ver','pyBtnBox6')
        new_data['icon'] = old_data.get('icon','FILE_FOLDER')
        new_data['area'] = old_data.get('area',[True for i in range(14)])
        new_data['level'] = new_level
        new_data['node'] = new_node
        
        dataPath = self.get_data_path(self.name)
        json_data = json.dumps(new_data, indent=4)
        with open( dataPath , 'w+') as f:
            f.write(json_data)
        
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1) 
        return new_data
    
    @staticmethod
    def get_menu_path(menuName):
        root = Root.load()
        if root.state != 'PATH_FINE':
            return ''
        menuPath = os.path.join(root.path,menuName)
        if not os.path.isdir(menuPath):
            return ''
        return menuPath
    
    @staticmethod
    def get_data_path(menuName):
        menuPath = Menu.get_menu_path(menuName)
        if menuPath=='':
            return ''
        dataPath = os.path.join(menuPath,'.menuData.json')
        return dataPath
    
    @staticmethod
    def get_pyFiles(menuName,mode):
        menuPath = Menu.get_menu_path(menuName)
        if menuPath=='':
            return []
        
        output_list = []
        for file in os.listdir( menuPath ):
            if not file.endswith('.py'):
                continue
            if mode == 'name':
                output_list.append(file)
            if mode == 'base':
                output_list.append(file[:-3])
            if mode == 'path':
                output_list.append(os.path.join( menuPath,file ))
        return output_list
    

    def get_parent_trees(self):
        levels = self.data['level']
        nodes = self.data['node']

        # Build Panel Tree
        def get_parent_tree(search_node):

            parent_tree = []
            def append_parent(node_name):
                nodeData = nodes[node_name]
                nodePanel = nodeData.get('panel','_')
                if nodePanel !='_':
                    parent_tree.append(nodePanel)
                    append_parent(nodePanel)
                return
            append_parent(search_node)
            return parent_tree

        
        parent_trees = {key:get_parent_tree(key) for key in levels.keys() if key!='_' }
        return parent_trees


    def get_children_tree(self,pnl_name):
        levels = self.data['level']
        if not levels.get(pnl_name):
            return []
        
        children_tree=[]
        def append_tree(pnl_name):
            for child in levels.get(pnl_name,[]):
                if not child.startswith('1'):
                    continue
                children_tree.append(child)
                append_tree(child)
        append_tree(pnl_name)
        return children_tree