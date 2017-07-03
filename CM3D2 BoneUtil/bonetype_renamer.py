# -*- coding: utf-8 -*-

import bpy  # type: ignore
import math
import mathutils  # type: ignore
import os
import sys
from . import common
from typing import Dict, Set, List, Tuple, Optional, Any


def menu_func(self, context):  # type: (Any, bpy.types.Context) -> None
	if not common.prefs().bonetype_renamer:
		return
	ob = context.active_object
	if not ob or ob.type != 'MESH' or ob.parent is None or ob.parent.type != 'ARMATURE':
		return
	if len(ob.parent.data.bones) == 0:
		return

	ui_list = context.window_manager.my_bone_list
	refresh_bonelist(self, context, ui_list, ob.parent.data.bones)
	if len(ui_list.yure_bones) == 0:
		return

	menu_func_common(self, context, ui_list)


def menu_func_arm(self, context):  # type: (Any, bpy.types.Context) -> None
	if not common.prefs().bonetype_renamer:
		return

	ob = context.active_object
	if not ob or ob.type != 'ARMATURE' or len(ob.data.bones) == 0:
		return

	ui_list = context.window_manager.my_bone_list
	refresh_bonelist(self, context, ui_list, ob.data.bones)
	if len(ui_list.yure_bones) == 0:
		return

	menu_func_common(self, context, ui_list)


def menu_func_common(self, context, ui_list):  # type: (Any, bpy.types.Context, Any) -> None
	layout = self.layout
	ybl = context.window_manager.yure_bone_list

	row = layout.row()
	col = row.column()
	split = col.split(percentage=0.85, align=True)
	split.label(text="butl.ChangeBoneType", icon='BONE_DATA')
	if ybl.display_ybl:
		split.prop(ybl, "display_ybl", text="", icon='TRIA_DOWN')  # icon='DOWNARROW_HLT')
	else:
		split.prop(ybl, "display_ybl", text="", icon='TRIA_LEFT')  # icon='RIGHTARROW')

	# ListView
	if ybl.display_ybl:
		box = col.column(align=True).box().column()
		row = box.row(align=True)
		col = row.column(align=True)
		# ui_list = context.window_manager.my_bone_list
		col.template_list("YureBoneList", "", ui_list, "yure_bones", ui_list, "item_idx", rows=2)
		col = row.column(align=True)
		col.operator(BoneListSelectOperator.bl_idname, icon='ZOOMIN', text="")
		col.operator(BoneListDeselectOperator.bl_idname, icon='ZOOMOUT', text="")

		row = box.row()
		col = row.column(align=True)
		col.prop(ui_list, 'target_type', icon='BONE_DATA')

		# TODO filter
		# if len(ui_list.yure_bones):
		# 	row = layout.row()
		# 	row.prop(ui_list.yure_bones[ui_list.item_idx], "name")
		# 	row = layout.row()
		# 	row.prop(ui_list.yure_bones[ui_list.item_idx], "selected")
		row = box.row()
		label = bpy.app.translations.pgettext('butl.ChangeBoneType')
		row.operator(BoneTypeChangeOperator.bl_idname, text=label)


def refresh_bonelist(self, context, ui_list, target_bones):  # type: (Any, bpy.types.Context, Any, Dict) -> None
	# 前回の選択状態を保持
	selected_dic = {}
	for bone in ui_list.yure_bones:
		selected_dic[bone.name] = bone.selected

	bone_names = None  # type: Optional[Set[str]]
	ui_list.yure_bones.clear()
	for bone in target_bones:
		if '_yure_' in bone.name:

			if bone_names is None:
				bone_names = parse_bone_names(self, context)

			bone_type = common.parse_bonetype(bone.name)
			if bone_type is not None and bone.name in bone_names:
				item = ui_list.yure_bones.add()
				item.name = bone.name
				item.bone_type = bone_type

				item.selected = selected_dic[bone.name] if (bone.name in selected_dic) else False


def parse_bone_names(self, context):  # type: (Any, bpy.types.Context) -> Set[str]
	bone_names = set()  # type: Set[str]
	if context.active_object.type == 'MESH':
		target_props = context.active_object
	else:  # ARMATURE
		target_props = context.active_object.data

	for item in target_props.items():
		prop_name, prop_val = item[0], item[1]
		if prop_name.startswith('BoneData:'):
			bd = prop_val.split(',', 1)
			bone_names.add(bd[0])
	return bone_names


class YureBoneItem(bpy.types.PropertyGroup):  # type: ignore
	name = bpy.props.StringProperty()
	selected = bpy.props.BoolProperty()
	desc = bpy.app.translations.pgettext('Hardness')
	bone_types = [
		('soft', 'yure_soft', desc + ":(0.05, 0.5)", '', 0),
		('hard', 'yure_hard', desc + ":(0.1, 1)", '', 1),
		('skirt', 'yure_skirt', desc + ":(0.5, 0.9)", '', 2),
		('skirt_h', 'yure_skirt_h', desc + ":(0.95, 99999)", '', 3),
		('hair', 'yure_hair', desc + ":(0.05, 0.3)", '', 4),
		('hair_h50', 'yure_hair_h50', desc + ":(0.1, 1)", '', 5),
		('hair_h', 'yure_hair_h', desc + ":(0.5, 3)", '', 6),
	]
	bone_type = bpy.props.EnumProperty(name="BoneType", items=bone_types, default='soft')


class ItemGroup(bpy.types.PropertyGroup):  # type: ignore
	yure_bones = bpy.props.CollectionProperty(type=YureBoneItem)
	item_idx   = bpy.props.IntProperty()

	target_type = bpy.props.EnumProperty(name="BoneType", items=YureBoneItem.bone_types, default='soft')


class BoneListSelectItemOperator(bpy.types.Operator):  # type: ignore
	bl_idname = "custom.trzr_bonelist_select_item"
	bl_label  = "Select Item"

	opr_type = bpy.props.StringProperty(default='')

	def execute(self, context):  # type: (bpy.types.Context) -> Set
		ui_list = context.window_manager.my_bone_list
		if self.opr_type == 'SELECT_ALL':
			for bone in ui_list.yure_bones:
				bone.selected = True
		elif self.opr_type == 'DESELECT_ALL':
			for bone in ui_list.yure_bones:
				bone.selected = False
		return {'FINISHED'}


# custom list
class ULItems(bpy.types.UIList):  # type: ignore
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):  # type: ignore
		row = layout.row()
		col2 = row.column(align=True)
		col2.prop(item, "selected", text="", icon='NONE')

		col1 = row.column(align=True)
		col1.prop(item, "name", text="", emboss=False, translate=False, icon_value=icon)  # icon='NONE')


class BoneListSelectOperator(bpy.types.Operator):  # type: ignore
	bl_idname = "custom.trzr_yurebonelist_select_all"
	bl_label = "Select All"

	def execute(self, context):  # type: (bpy.types.Context) -> Set
		for bone in context.window_manager.my_bone_list.yure_bones:
			bone.selected = True
		return {'FINISHED'}


class BoneListDeselectOperator(bpy.types.Operator):  # type: ignore
	bl_idname = "custom.trzr_yurebonelist_deselect_all"
	bl_label = "Deselect All"

	def execute(self, context):  # type: (bpy.types.Context) -> Set
		for bone in context.window_manager.my_bone_list.yure_bones:
			bone.selected = False
		return {'FINISHED'}


class CheckItem(bpy.types.PropertyGroup):  # type: ignore
	name = bpy.props.StringProperty()
	replaced_name = bpy.props.StringProperty()


class CheckList(bpy.types.UIList):  # type: ignore
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):  # type: ignore
		split = layout.split(0.5)
		split.label(text=item.name, translate=False, icon='NONE' )
		split.label(text=item.replaced_name, translate=False, icon='NONE')


class BoneTypeChangeOperator(bpy.types.Operator):  # type: ignore
	bl_idname = "custom.trzr_change_bonetype"
	bl_label = "change bone type"
	bl_options = {'REGISTER', 'UNDO'}

	count_lbd_replace = 0
	count_bd_replace = 0
	count_bdp_replace = 0

	def create_rename_list(self, context):  # type: (bpy.types.Context) -> List[Tuple[str, str]]
		ui_list = context.window_manager.my_bone_list
		target_type = ui_list.target_type

		rename_list = []
		for bone in ui_list.yure_bones:
			if bone.selected and target_type != bone.bone_type:
				replaced = common.replace_bonename(bone.name, bone.bone_type, target_type)
				rename_list.append( (bone.name, replaced) )
		return rename_list

	def execute(self, context):  # type: (bpy.types.Context) -> Set
		rename_list = self.create_rename_list(context)

		ob = context.active_object
		if ob.type == 'MESH':
			target_bones = context.active_object.parent.data.bones
		else:  # ARMATURE
			target_bones = context.active_object.data.bones

		# 重複チェック
		for rename_item in rename_list:
			if rename_item[1] in target_bones:
				msg = 'bone rename failed. already exist:%s' % rename_item[1]
				self.report(type={'ERROR'}, message=msg)
				return {'CANCELLED'}

		for rename_item in rename_list:
			try:
				target_bones[rename_item[0]].name = rename_item[1]
			except:
				pass
		self.replace_props(context, rename_list)

		# 処理件数を出力する。BoneData数, LocalBoneData数
		msg = bpy.app.translations.pgettext('butl.ChangeBoneTypeCompleted')
		logmsg = ". Count BoneData:%d(parent:%d),LocalBoneData:%d)" % (
			self.count_bd_replace, self.count_bdp_replace, self.count_lbd_replace)
		self.report(type={'INFO'}, message=msg + logmsg)
		ui_list = context.window_manager.my_bone_list
		return {'FINISHED'}

	def replace_props(self, context, rename_list):  # type: (bpy.types.Context, List[Tuple[str, str]]) -> None
		max_idx = 0
		lbd_dic = {}
		bd_dic  = {}
		bdp_dic = {}  # type: Dict[str, List[str]]

		if context.active_object.type == 'MESH':
			target_props = context.active_object
		else:  # ARMATURE
			target_props = context.active_object.data

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
			bone_name, replace_name = rename_item[0], rename_item[1]
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


class YureBoneList(bpy.types.UIList):  # type: ignore
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):  # type: ignore
		split = layout.split(0.05)
		split.prop(item, "selected", text="", icon='NONE')
		split = split.split(0.80)
		split.label(text=item.name, translate=False, icon='BONE_DATA' )
		split.label(text=item.bone_type, translate=False, icon='NONE')


class YureBoneProps(bpy.types.PropertyGroup):  # type: ignore
	display_ybl = bpy.props.BoolProperty(
		name="butl.BonesList",
		description="Display Yure Bone List",
		default=False)


# -------------------------------------------------------------------
# register
# -------------------------------------------------------------------
def register():  # type: () -> None
	bpy.types.WindowManager.my_bone_list = bpy.props.PointerProperty(type=ItemGroup)
	bpy.types.WindowManager.yure_bone_list = bpy.props.PointerProperty(type=YureBoneProps)


def unregister():  # type: () -> None
	del bpy.types.WindowManager.my_bone_list
	del bpy.types.WindowManager.yure_bone_list
