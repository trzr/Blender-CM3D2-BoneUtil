bl_info = {
	"name" : "CM3D2 BoneUtil",
	"author" : "trzr",
	"version" : (0, 0, 1),
	"blender" : (2, 76, 0),
	"location" : "",
	"description" : "カスタムメイド3D2のボーン関連の補助機能を提供します",
	"warning" : "",
	"wiki_url" : "https://github.com/trzr/Blender-CM3D2-BoneUtil",
	"tracker_url": "https://github.com/trzr/Blender-CM3D2-BoneUtil/issues",
	"category" : "Tools"
}

# サブスクリプト群をインポート
if "bpy" in locals():
	import imp

	imp.reload(common)
	imp.reload(bonedata_importer)
	#imp.reload(bone_renamer)
else:
	from . import common
	from . import bonedata_importer
	#from . import bone_renamer

import bpy, os.path, bpy.utils.previews

# アドオン設定
class AddonPreferences(bpy.types.AddonPreferences):
	bl_idname = __name__
#	auto_update = bpy.props.BoolProperty(name="更新", description="自動更新：GihHubから最新版を取得", default=False )
#
#	def draw(self, context):
#		self.layout.label(text="ここの設定は「ユーザー設定の保存」ボタンを押すまで保存されていません", icon='QUESTION')


def register():
	bpy.utils.register_module(__name__)

	bpy.types.DATA_PT_context_arm.append(bonedata_importer.menu_func_arm)
	bpy.types.OBJECT_PT_context_object.append(bonedata_importer.menu_func)

	#bpy.types.OBJECT_PT_context_object.append(bone_renamer.menu_func)

	system = bpy.context.user_preferences.system
	if not system.use_international_fonts:
		system.use_international_fonts = True
	if not system.use_translate_interface:
		system.use_translate_interface = True
	try:
		import locale
		if system.language == 'DEFAULT' and locale.getdefaultlocale()[0] != 'ja_JP':
			system.language = 'en_US'
	except: pass

	try:
		import locale
		if locale.getdefaultlocale()[0] != 'ja_JP':
			unregister()
	except: pass

def unregister():
	bpy.utils.unregister_module(__name__)

	bpy.types.DATA_PT_context_arm.remove(bonedata_importer.menu_func_arm)
	bpy.types.OBJECT_PT_context_object.remove(bonedata_importer.menu_func)
	#bpy.types.OBJECT_PT_context_object.remove(bone_renamer.menu_func)

	bpy.app.translations.unregister(__name__)

if __name__ == "__main__":
	register()
