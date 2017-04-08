bl_info = {
	"name" : "CM3D2 BoneUtil",
	"author" : "trzr",
	"version" : (0, 2, 12),
	"blender" : (2, 76, 0),
	"location" : "AddonDesc",
	"description" : "",
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
else:
	from . import translations
	from . import common
	from . import bonedata_importer
	from . import bonetype_renamer
	
	from . import blendset_importer
	from . import addon_updater

import bpy, os.path, bpy.utils.previews

# アドオン設定
class AddonPreferences(bpy.types.AddonPreferences):
	bl_idname = __name__
	
	bonetype_renamer = bpy.props.BoolProperty(name="ChangeBoneTypeFeature", description="ChangeBoneTypeFDesc", default=False )
	bsimp = bpy.props.BoolProperty(name="shapekey.BsImporterFeature", description="shapekey.BsImporterFDesc", default=True )
	
	backup_ext = bpy.props.StringProperty(name="バックアップの拡張子 (空欄で無効)", description="エクスポート時にバックアップをこの拡張子で作成します、空欄でバックアップを無効", default='bak')
	menu_default_path = bpy.props.StringProperty(name="menuファイル配置ディレクトリ", subtype='DIR_PATH', description="設定すれば、menuを扱う時は必ずここからファイル選択を始めます")
	menu_import_path  = bpy.props.StringProperty(name="menuインポート時のデフォルトパス", subtype='FILE_PATH', description="menuインポート時に最初はここが表示されます、インポート毎に保存されます")
	menu_export_path  = bpy.props.StringProperty(name="menuエクスポート時のデフォルトパス", subtype='FILE_PATH', description="menuエクスポート時に最初はここが表示されます、エクスポート毎に保存されます")
	
	update_history = addon_updater.VersionHistory()
	update_history.now_ver = [ v for v in bl_info['version'] ]
	version = '.'.join( [ str(v) for v in bl_info['version'] ] )

	def draw(self, context):
		layout = self.layout
		layout.label(text="PushSaveButton", icon='QUESTION')
		box = layout.box()
		box.label(text="EnableOption", icon='DOT')
		row = box.row()
		split = row.split(percentage=0.3, align=True)
		split.prop(self, 'bonetype_renamer', icon='NONE')
		split.prop(self, 'bsimp', icon='NONE')
		
		box = layout.box()
		box.prop(self, 'backup_ext', icon='FILE_BACKUP')
		box.label(text="menuファイル", icon='FILE_IMAGE')
		box.prop(self, 'menu_default_path', icon='FILESEL', text="menuファイル選択時の初期フォルダ")
		
		row = layout.row()
		
		#row.label(self, 'version', icon='INFO')
		row.menu('INFO_MT_CM3D2_BoneUtil_history', icon='INFO')
		
		v = self.version
		if self.update_history.has_update(): 
			v += ' => ' + self.update_history.latest_version
		row.label(text=v)
		row.operator('script.update_cm3d2_boneutil', icon='FILE_REFRESH')
	
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
	
	bpy.app.translations.unregister(__name__)
if __name__ == "__main__":
	register()
