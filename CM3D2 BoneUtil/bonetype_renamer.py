import os, sys, bpy, math, mathutils
from . import common

def refresh_bonelist(self, context, ui_list, target_bones):
	# 前回の選択状態を保持
	selected_dic = {}
	for bone in ui_list.yure_bones:
		selected_dic[bone.name] = bone.selected

	ui_list.yure_bones.clear()
	for bone in target_bones:
		if '_yure_' in bone.name:
			item = ui_list.yure_bones.add()
			item.name = bone.name

			item.selected = selected_dic[bone.name] if (bone.name in selected_dic) else False

			item.bone_type = common.parse_bonetype(bone.name)
			if item.bone_type == None:
				ui_list.yure_bones.remove(item)
				#del item

class YureBoneItem(bpy.types.PropertyGroup):
	name = bpy.props.StringProperty()
	selected = bpy.props.BoolProperty()
	desc = bpy.app.translations.pgettext('Hardness')
	bone_types = [
		('soft',     'yure_soft',     desc+":(0.05, 0.5)", '', 0),
		('hard',     'yure_hard',     desc+":(0.1, 1)", '', 1),
		('skirt',    'yure_skirt',    desc+":(0.5, 0.9)", '', 2),
		('skirt_h',  'yure_skirt_h',  desc+":(0.95, 99999)", '', 3),
		('hair',     'yure_hair',     desc+":(0.05, 0.3)", '', 4),
		('hair_h50', 'yure_hair_h50', desc+":(0.1, 1)", '', 5),
		('hair_h',   'yure_hair_h',   desc+":(0.5, 3)", '', 6),
	]
	bone_type = bpy.props.EnumProperty(name="BoneType", items=bone_types, default='soft')

class ItemGroup(bpy.types.PropertyGroup):
	yure_bones = bpy.props.CollectionProperty(type=YureBoneItem)
	item_idx   = bpy.props.IntProperty()

	target_type = bpy.props.EnumProperty(name="BoneType", items=YureBoneItem.bone_types, default='soft')

class BoneListSelectItemOperator(bpy.types.Operator):
	bl_idname = "custom.bonelist_select_item"
	bl_label  = "Select Item"

	opr_type = bpy.props.StringProperty(default='')

	def execute(self, context):
		ui_list = context.window_manager.my_bone_list
		if self.opr_type == 'SELECT_ALL':
			for bone in ui_list.yure_bones:
				bone.selected = True
		elif self.opr_type == 'DESELECT_ALL':
			for bone in ui_list.yure_bones:
				bone.selected = False
		return {'FINISHED'}

# custom list
class ULItems(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		row = layout.row()
		col2 = row.column(align=True)
		col2.prop(item, "selected", text="", icon='NONE')

		col1 = row.column(align=True)
		col1.prop(item, "name", text="", emboss=False, translate=False, icon_value=icon) #icon='NONE')

class BoneListSelectOperator(bpy.types.Operator):
	bl_idname = "custom.yurebonelist_select_all"
	bl_label = "Select All"

	def execute(self, context):
		for bone in context.window_manager.my_bone_list.yure_bones:
			bone.selected = True
		return {'FINISHED'}

class BoneListDeselectOperator(bpy.types.Operator):
	bl_idname = "custom.yurebonelist_deselect_all"
	bl_label = "Deselect All"

	def execute(self, context):
		for bone in context.window_manager.my_bone_list.yure_bones:
			bone.selected = False
		return {'FINISHED'}

class CheckItem(bpy.types.PropertyGroup):
	name = bpy.props.StringProperty()
	replaced_name = bpy.props.StringProperty()

class CheckList(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		split = layout.split(0.5)
		split.label(text=item.name, translate=False, icon='NONE' )
		split.label(text=item.replaced_name, translate=False, icon='NONE')

class ChangeBoneTypeOperator(bpy.types.Operator):
	bl_idname = "custom.change_bonetype"
	bl_label = "change bone type"
	bl_options = {'REGISTER', 'UNDO'}

	count_lbd_replace = 0
	count_bd_replace = 0
	count_bdp_replace = 0

	def create_rename_list(self, context):
		ui_list = context.window_manager.my_bone_list
		target_type = ui_list.target_type

		rename_list = []
		for bone in ui_list.yure_bones:
			if bone.selected and target_type != bone.bone_type:
				replaced = common.replace_bonename(bone.name, bone.bone_type, target_type)
				rename_list.append( (bone.name, replaced) )
		return rename_list

	def execute(self, context):
		rename_list = self.create_rename_list(context)

		target_bones = context.active_object.parent.data.bones
		# 重複チェック
		for rename_item in rename_list:
			if rename_item[1] in target_bones:
				msg = 'bone rename failed. already exist:%s' % rename_item[1]
				self.report(type={'ERROR'}, message=msg)
				return {'CANCEL'}

		for rename_item in rename_list:
			try:
				target_bones[rename_item[0]].name = rename_item[1]
			except: pass
		self.replace_props(context, rename_list)

		# 処理件数を出力する。BoneData数, LocalBoneData数
		logmsg = "Count BoneData:%d(parent:%d),LocalBoneData:%d)" % (
			self.count_bd_replace, self.count_bdp_replace, self.count_lbd_replace)
		self.report(type={'INFO'}, message="ChangeBoneTypeCompleted." + logmsg)
		ui_list = context.window_manager.my_bone_list
		return {'FINISHED'}

	def replace_props(self, context, rename_list):
		target_props = context.active_object
		max_idx = 0
		lbd_dic = {}
		bd_dic  = {}
		bdp_dic = {}

		# parse props
		for item in target_props.items():
			prop_name, prop_val = item[0], item[1]
			if prop_name.startswith('LocalBoneData:'):
				lbd = prop_val.split(',')
				lbd_dic[lbd[0]] = (prop_name, lbd[1])

			elif prop_name.startswith('BoneData:'):
				bd = prop_val.split(',')
				bd_dic[bd[0]] = prop_name
				parent_name = bd[2]
				if parent_name != 'None':
					if parent_name not in bdp_dic:
						bdp_dic[parent_name] = [prop_name]
					else:
						bdp_dic[parent_name].append(prop_name)

		# replace_props
		for rename_item in rename_list:
			bone_name = rename_item[0]
			replace_name = rename_item[1]
			if bone_name in lbd_dic:
				lbd_item = lbd_dic[bone_name]
				target_props[lbd_item[0]] = "{0},{1}".format(replace_name, lbd_item[1])
				self.count_lbd_replace += 1

			if bone_name in bdp_dic:
				prop_names = bdp_dic[bone_name]
				for prop_name in prop_names:
					prop_val = target_props[prop_name]
					items = prop_val.split(',')
					target_props[prop_name] = "{0},{1},{2},{3},{4}".format(
						items[0], items[1], replace_name, items[3], items[4])
					self.count_bdp_replace += 1

			if bone_name in bd_dic:
				prop_name = bd_dic[bone_name]
				prop_val = target_props[prop_name]
				items = prop_val.split(',')
				target_props[prop_name] = "{0},{1},{2},{3},{4}".format(
					replace_name, items[1], items[2], items[3], items[4])
				self.count_bd_replace += 1

class YureBoneList(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		split = layout.split(0.05)
		split.prop(item, "selected", text="", icon='NONE')
		split = split.split(0.80)
		split.label(text=item.name, translate=False, icon='BONE_DATA' )
		split.label(text=item.bone_type, translate=False, icon='NONE')

class UIListTestPanel(bpy.types.Panel):
	bl_label = "Bone List"
	bl_idname = "PROPERTIES_ui_list_test"
	bl_space_type = "PROPERTIES"
	bl_context="object"
	bl_region_type = "WINDOW"

	@classmethod
	def poll(self, context):
		if not common.prefs().bonetype_renamer: return False

		ob = context.active_object
		if not ob or ob.type != 'MESH': return False

		if ob.parent is None or ob.parent.type != 'ARMATURE': return False
		if len(ob.parent.data.bones) == 0: return False

		ui_list = context.window_manager.my_bone_list
		refresh_bonelist(self, context, ui_list, ob.parent.data.bones)
		if len(ui_list.yure_bones) == 0: return False
		return True

	def draw(self, context):
		layout = self.layout
		ui_list = context.window_manager.my_bone_list

		row = layout.row()
		col = row.column()
		col.template_list("YureBoneList", "", ui_list, "yure_bones", ui_list, "item_idx", rows=2)

		col = row.column(align=True)
		col.operator("custom.yurebonelist_select_all", icon='ZOOMIN', text="")
		col.operator("custom.yurebonelist_deselect_all", icon='ZOOMOUT', text="")

		row = layout.row()
		col = row.column(align=True)
		col.prop(ui_list, 'target_type', icon='BONE_DATA')
		# TODO filter
		#if len(ui_list.yure_bones):
		#	row = layout.row()
		#	row.prop(ui_list.yure_bones[ui_list.item_idx], "name")
		# 	row = layout.row()
		# 	row.prop(ui_list.yure_bones[ui_list.item_idx], "selected")
		row = layout.row()
		label = bpy.app.translations.pgettext('ChangeBoneType')
		row.operator("custom.change_bonetype", text=label)
# -------------------------------------------------------------------
# register
# -------------------------------------------------------------------
def register():
	bpy.types.WindowManager.my_bone_list = bpy.props.PointerProperty(type=ItemGroup)

def unregister():
	del bpy.types.WindowManager.my_bone_list
