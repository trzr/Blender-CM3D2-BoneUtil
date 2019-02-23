__author__ = "trzr"
__status__ = "dev"
__version__ = "0.4.0"
__date__ = "23 Feb 2019"  # ctrl+shift+I

bl_info = {
    "name": "CM3D2 BoneUtil",
    "author": "trzr",
    "version": (0, 4, 0),
    "blender": (2, 80, 0),
    "location": 'Properties > Object Data (Mesh), etc...',
    "description": "Bone data utility for CM3D2/COM3D2",
    "warning": "",
    "wiki_url": "https://github.com/trzr/Blender-CM3D2-BoneUtil/wiki",
    "tracker_url": "https://github.com/trzr/Blender-CM3D2-BoneUtil/issues",
    "category": "Object"
}


# サブスクリプト群をインポート
if 'bpy' not in locals():
    from . import translations

    from . import common
    from . import compatibility

    from . import addon_updater
    from . import bonedata_importer
    from . import bonetype_renamer

    from . import blendset_importer
    from . import vertex_group_tools

    from . import selection_tool
else:
    import importlib

    importlib.reload(translations)
    importlib.reload(common)
    importlib.reload(compatibility)

    importlib.reload(addon_updater)
    importlib.reload(bonedata_importer)
    importlib.reload(bonetype_renamer)
    # # importlib.reload(bone_edit)

    importlib.reload(blendset_importer)
    importlib.reload(vertex_group_tools)
    # # importlib.reload(shape_key_tools)
    # # importlib.reload(attachpoint_tools)

    importlib.reload(selection_tool)

import bpy

# アドオン設定
@compatibility.BlRegister()
class BUTL_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    feature_bonetype = bpy.props.BoolProperty(name="butl.feature.ChangeBoneType", description="butl.feature.ChangeBoneTypeDesc", default=False)
    feature_importer = bpy.props.BoolProperty(name="butl.feature.BsImporter", description="butl.feature.BsImporterDesc", default=True)
    feature_vgroups = bpy.props.BoolProperty(name="butl.feature.Vertexgroups", description="butl.feature.VertexgroupsDesc", default=False)

    backup_ext = bpy.props.StringProperty(name="butl.shapekey.Menu.BackupExt",
                                          description="butl.shapekey.Menu.BackupExtDesc", default='bak')
    menu_default_path = bpy.props.StringProperty(name="butl.shapekey.Menu.TargetDir", subtype='DIR_PATH',
                                                 description="butl.shapekey.Menu.TargetDirDesc")
    menu_import_path = bpy.props.StringProperty(name="butl.shapekey.Menu.DefaultPath.Import", subtype='FILE_PATH',
                                                description="butl.shapekey.Menu.DefaultPath.ImportDesc")
    menu_export_path = bpy.props.StringProperty(name="butl.shapekey.Menu.DefaultPath.Export", subtype='FILE_PATH',
                                                description="butl.shapekey.Menu.DefaultPath.ExportDesc")

    update_history = addon_updater.VersionHistory(bl_info['version'])
    version = '.'.join([str(v) for v in bl_info['version']])

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        layout.label(text="butl.PushSaveButton", icon='QUESTION')
        box = layout.box()
        box.label(text="butl.EnableOption", icon='DOT')
        row = box.row()
        split = compatibility.layout_split(row, factor=0.3, align=True)
        split.prop(self, 'feature_bonetype', icon='NONE')
        split.prop(self, 'feature_importer', icon='NONE')
        split.prop(self, 'feature_vgroups', icon='NONE')

        box = layout.box()
        box.prop(self, 'backup_ext', icon='FILE_BACKUP')
        box.label(text="butl.shapekey.Menu.File", icon='FILE_IMAGE')
        box.prop(self, 'menu_default_path', icon=compatibility.icon('FILEBROWSER'), text="butl.shapekey.Menu.InitFolder")


        row = layout.row()
        # row.label(self, 'version', icon='INFO')
        row.menu(addon_updater.BUTL_MT_History.bl_idname, icon='INFO')

        v = BUTL_AddonPreferences.version
        if BUTL_AddonPreferences.update_history.has_update():
            v += ' => ' + BUTL_AddonPreferences.update_history.latest_version
        row.label(text=v)
        row.operator(addon_updater.BUTL_OT_Updater.bl_idname, icon='FILE_REFRESH')


def register():
    common.TransManager.register()
    compatibility.BlRegister.register()

    # append menu
    bpy.types.DATA_PT_context_arm.append(bonedata_importer.menu_func_arm)
    bpy.types.DATA_PT_context_arm.append(bonetype_renamer.menu_func_arm)
    bpy.types.DATA_PT_context_mesh.append(blendset_importer.menu_func)

    bpy.types.OBJECT_PT_context_object.append(bonedata_importer.menu_func)
    bpy.types.OBJECT_PT_context_object.append(bonetype_renamer.menu_func)

    bpy.types.MESH_MT_vertex_group_specials.append(vertex_group_tools.menu_func_specials)

    # initialize properties
    bpy.types.Scene.trzr_select_props = bpy.props.PointerProperty(type=selection_tool.LocalProps)
    bpy.types.Scene.trzr_butl_bone_list = bpy.props.PointerProperty(type=bonetype_renamer.ItemGroup)
    bpy.types.Scene.trzr_butl_bone_props = bpy.props.PointerProperty(type=bonetype_renamer.YureBoneProps)
    bpy.types.Scene.trzr_butl_blendsets = bpy.props.PointerProperty(type=blendset_importer.Blendsets)


def unregister():
    # delete properties
    del bpy.types.Scene.trzr_butl_blendsets
    del bpy.types.Scene.trzr_butl_bone_props
    del bpy.types.Scene.trzr_butl_bone_list
    del bpy.types.Scene.trzr_select_props

    # remove menu
    bpy.types.MESH_MT_vertex_group_specials.remove(vertex_group_tools.menu_func_specials)

    bpy.types.OBJECT_PT_context_object.remove(bonedata_importer.menu_func)
    bpy.types.OBJECT_PT_context_object.remove(bonetype_renamer.menu_func)

    bpy.types.DATA_PT_context_mesh.remove(blendset_importer.menu_func)
    bpy.types.DATA_PT_context_arm.remove(bonedata_importer.menu_func_arm)
    bpy.types.DATA_PT_context_arm.remove(bonetype_renamer.menu_func_arm)

    # unregister classes
    compatibility.BlRegister.unregister()
    common.TransManager.unregister()


if __name__ == '__main__':
    register()
