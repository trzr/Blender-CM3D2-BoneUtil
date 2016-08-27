bl_info = {
	"name" : "CM3D2 BoneUtil",
	"author" : "trzr",
	"version" : (0, 2, 0),
	"blender" : (2, 76, 0),
	"location" : "AddonDesc",
	"description" : "",
	"warning" : "",
	"wiki_url" : "https://github.com/trzr/Blender-CM3D2-BoneUtil",
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
else:
	from . import translations
	from . import common
	from . import bonedata_importer
	from . import bonetype_renamer
	
	from . import blendset_importer

import bpy, os.path, bpy.utils.previews

# アドオン設定
class AddonPreferences(bpy.types.AddonPreferences):
	bl_idname = __name__
	
	bonetype_renamer = bpy.props.BoolProperty(name="ChangeBoneTypeFeature", description="ChangeBoneTypeFDesc", default=False )
	#bone2mesh = bpy.props.BoolProperty(name="GenMeshFromBoneFeature", description="GenMeshFromBoneFDesc", default=False )
	
	def draw(self, context):
		layout = self.layout
		layout.label(text="PushSaveButton", icon='QUESTION')
		box = layout.box()
		box.label(text="EnableOption", icon='DOT')
		row = box.row()
		row.prop(self, 'bonetype_renamer', icon='NONE')
		row.prop(self, 'bone2mesh', icon='NONE')


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
