bl_info = {
	"name" : "CM3D2 BoneUtil",
	"author" : "trzr",
	"version" : (0, 3, 0),
	"blender" : (2, 76, 0),
	"location" : "AddonDesc",
	"description" : "Bone data utility for CM3D2",
	"warning" : "",
	"wiki_url" : "https://github.com/trzr/Blender-CM3D2-BoneUtil/wiki",
	"tracker_url": "https://github.com/trzr/Blender-CM3D2-BoneUtil/issues",
	"category" : "Tools"
}

# サブスクリプト群をインポート
if "bpy" in locals():
	import imp
	
	imp.reload(translations)
	imp.reload(common)
	imp.reload(bonedata_importer)
	imp.reload(bonetype_renamer)
	
	imp.reload(blendset_importer)
	imp.reload(addon_updater)
	imp.reload(vertex_group_tools)

	imp.reload(selection_tool_mesh)
	imp.reload(selection_tool_arm)
else:
	from . import translations
	from . import common
	from . import bonedata_importer
	from . import bonetype_renamer
	
	from . import blendset_importer
	from . import addon_updater
	from . import vertex_group_tools

	from . import selection_tool_mesh
	from . import selection_tool_arm

import bpy, os.path, bpy.utils.previews

# アドオン設定
class AddonPreferences(bpy.types.AddonPreferences):
	bl_idname = __name__
	
	bonetype_renamer = bpy.props.BoolProperty(name="butl.ChangeBoneTypeFeature", description="butl.ChangeBoneTypeFDesc", default=False )
	bsimp = bpy.props.BoolProperty(name="butl.shapekey.BsImporterFeature", description="butl.shapekey.BsImporterFDesc", default=True )
	
	vgfeature = bpy.props.BoolProperty(name="頂点グループ関連機能", description="頂点グループ関連の機能を追加します", default=False )
	backup_ext = bpy.props.StringProperty(name="butl.shapekey.Menu.BackupExt", description="butl.shapekey.Menu.BackupExtDesc", default='bak')
	menu_default_path = bpy.props.StringProperty(name="butl.shapekey.Menu.TargetDir", subtype='DIR_PATH', description="butl.shapekey.Menu.TargetDirDesc")
	menu_import_path  = bpy.props.StringProperty(name="butl.shapekey.Menu.DefaultPath.Import", subtype='FILE_PATH', description="butl.shapekey.Menu.DefaultPath.ImportDesc")
	menu_export_path  = bpy.props.StringProperty(name="butl.shapekey.Menu.DefaultPath.Export", subtype='FILE_PATH', description="butl.shapekey.Menu.DefaultPath.ExportDesc")
	
	update_history = addon_updater.VersionHistory()
	update_history.now_ver = [ v for v in bl_info['version'] ]
	version = '.'.join( [ str(v) for v in bl_info['version'] ] )

	def draw(self, context):
		layout = self.layout
		layout.label(text="butl.PushSaveButton", icon='QUESTION')
		box = layout.box()
		box.label(text="butl.EnableOption", icon='DOT')
		row = box.row()
		split = row.split(percentage=0.3, align=True)
		split.prop(self, 'bonetype_renamer', icon='NONE')
		split.prop(self, 'bsimp', icon='NONE')
		split.prop(self, 'vgfeature', icon='NONE')
		
		box = layout.box()
		box.prop(self, 'backup_ext', icon='FILE_BACKUP')
		box.label(text="butl.shapekey.Menu.File", icon='FILE_IMAGE')
		box.prop(self, 'menu_default_path', icon='FILESEL', text="butl.shapekey.Menu.InitFolder")
		
		row = layout.row()
		
		#row.label(self, 'version', icon='INFO')
		row.menu('INFO_MT_CM3D2_BoneUtil_history', icon='INFO')
		
		v = self.version
		if self.update_history.has_update():
			v += ' => ' + self.update_history.latest_version
		row.label(text=v)
		row.operator('script.trzr_update_cm3d2_boneutil', icon='FILE_REFRESH')

def register():
	bpy.utils.register_module(__name__)
	bpy.app.translations.register(__name__, translations.dic)
	
	bpy.types.DATA_PT_context_arm.append(bonedata_importer.menu_func_arm)
	bpy.types.OBJECT_PT_context_object.append(bonedata_importer.menu_func)
	
	# bpy.types.OBJECT_PT_context_object.append(bonetype_renamer.menu_func)
	bonetype_renamer.register()
	bpy.types.OBJECT_PT_context_object.append(bonetype_renamer.menu_func)
	bpy.types.DATA_PT_context_arm.append(bonetype_renamer.menu_func_arm)
	
	
	blendset_importer.register()
	bpy.types.DATA_PT_context_mesh.append(blendset_importer.menu_func)
	#bpy.types.DATA_PT_vertex_groups.append(vertex_group_tools.menu_func)
	bpy.types.MESH_MT_vertex_group_specials.append(vertex_group_tools.menu_func_specials)
	selection_tool_mesh.register()
	selection_tool_arm.register()
	
	system = bpy.context.user_preferences.system
	if not system.use_international_fonts:
		system.use_international_fonts = True
	if not system.use_translate_interface:
		system.use_translate_interface = True

def unregister():
	bpy.utils.unregister_module(__name__)
	
	bpy.types.DATA_PT_context_arm.remove(bonedata_importer.menu_func_arm)
	bpy.types.OBJECT_PT_context_object.remove(bonedata_importer.menu_func)
	# bpy.types.OBJECT_PT_context_object.remove(bonetype_renamer.menu_func)
	
	bpy.types.OBJECT_PT_context_object.remove(bonetype_renamer.menu_func)
	bpy.types.DATA_PT_context_arm.remove(bonetype_renamer.menu_func_arm)
	bonetype_renamer.unregister()
	
	
	blendset_importer.unregister()
	bpy.types.DATA_PT_context_mesh.remove(blendset_importer.menu_func)
	
	#bpy.types.DATA_PT_vertex_groups.remove(vertex_group_tools.menu_func)
	bpy.types.MESH_MT_vertex_group_specials.remove(vertex_group_tools.menu_func_specials)
	selection_tool_mesh.unregister()
	selection_tool_arm.unregister()
	
	bpy.app.translations.unregister(__name__)

if __name__ == "__main__":
	register()
