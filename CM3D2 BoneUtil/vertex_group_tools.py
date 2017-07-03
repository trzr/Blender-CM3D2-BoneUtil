# -*- coding: utf-8 -*-

import bpy  # type: ignore
import bmesh  # type: ignore
import math
import mathutils  # type: ignore
import os
import re
import sys
from . import common
from typing import List, Any, Match


def menu_func_specials(self, context):  # type: (Any, bpy.types.Context) -> None
	if not common.prefs().vgfeature:
		return
	ob = context.active_object
	if ob is None or ob.type != 'MESH':
		return
	if ob.parent and ob.parent.type == 'ARMATURE':
		if len(ob.parent.data.bones) == 0 and 'BaseBone' not in ob.parent.data:
			return
	else:
		if 'BaseBone' not in ob:
			return

	self.layout.separator()
	self.layout.operator(Bone2VertexGroup.bl_idname, icon='BONE_DATA')


class Bone2VertexGroup(bpy.types.Operator):  # type: ignore
	bl_idname = 'object.trzr_bone_to_vertex_group'
	bl_label = "ボーン情報から取り込み"
	bl_description = "ボーン情報から頂点グループを作成します"
	bl_options = {'REGISTER', 'UNDO'}

	skip_nub       = bpy.props.BoolProperty(name="nubボーン スキップ", default=True, description="末端ボーンをスキップ")
	skip_shapekeys = bpy.props.BoolProperty(name="シェイプキーと同名をスキップ", default=True, description="シェイプキーと同名のボーンをスキップ")

	src_data = bpy.props.EnumProperty(
		name="Source",
		items=[
			('Selected', '選択ボーン', "選択されたボーンのみ", 'NONE', 0),
			('All', '全ボーン', "blender上のボーン", 'NONE', 1),
			('LocalBoneData', 'LocalBoneData', "property上のLocalBoneData", 'NONE', 2),
		],
		default='All')

	@classmethod
	def poll(cls, context):  # type: (bpy.types.Context) -> bool
		ob = context.active_object
		if ob:
			if 'BaseBone' in ob:
				return True
			elif ob.parent:
				if 'BaseBone' in ob.parent.data:
					return True
				elif ob.parent.type == 'ARMATURE':
					if len(ob.parent.data.bones) > 0:
						return True
		return False

	def invoke(self, context, event):  # type: (bpy.types.Context, Any) -> Set
		return context.window_manager.invoke_props_dialog(self)

	def draw(self, context):  # type: (bpy.types.Context) -> None
		row = self.layout.row()
		row.label(text="データソース:", icon='BONE_DATA')
		row = self.layout.row()
		row.prop(self, 'src_data', icon='BONE_DATA', expand=True)
		row = self.layout.row()
		row.label(text="スキップ設定:", icon='FILTER')
		row = self.layout.row()
		row.prop(self, 'skip_nub', icon='GROUP_BONE')
		row = self.layout.row()
		row.prop(self, 'skip_shapekeys', icon='SHAPEKEY_DATA')
		# TODO armatureのBaseBoneかmeshのBaseBoneかを選択？

	def execute(self, context):  # type: (bpy.types.Context) -> Set
		ob = context.active_object
		arm = ob.parent

		bb_name = ''
		props = None
		if 'BaseBone' in ob:
			bb_name = ob['BaseBone']
			props = ob
		elif 'BaseBone' in arm.data:
			bb_name = arm.data['BaseBone']
			props = arm.data

		# collect bonenames
		target_bonenames = []
		if self.src_data == 'Selected':
			for bone in arm.data.bones:
				if bone.select:
					target_bonenames.append(bone.name)
		elif self.src_data == 'All':
			for bone in arm.data.bones:
				target_bonenames.append(bone.name)
		elif props is not None:
			for item in props.items():
				if item[0].startswith('LocalBoneData:'):
					prop_val = item[1]
					key = prop_val[:prop_val.index(',')]
					target_bonenames.append(key)

		if len(target_bonenames) == 0:
			self.report(type={'INFO'}, message="抽出元のボーン情報がありません。中断します")
			return {'CANCELLED'}

		ignores = None
		if self.skip_shapekeys:
			shape_keys = ob.data.shape_keys
			if shape_keys:
				ignores = set()
				for key in shape_keys.key_blocks.keys():
					ignores.add( key.lower() )

		created = 0
		for bone_name in target_bonenames:
			if '_IK_' in bone_name:
				continue
			if bone_name == bb_name or bone_name in ob.vertex_groups:
				continue

			bone_nameL = bone_name.lower()
			if self.skip_nub and bone_nameL.endswith('nub'):
				continue
			if ignores and bone_nameL in ignores:
				continue

			ob.vertex_groups.new(bone_name)
			created += 1

		if created > 0:
			msg = "ボーンから頂点グループを作成しました. created=%d" % created
		else:
			msg = "頂点グループはすべて作成済みです"

		self.report(type={'INFO'}, message=msg)
		return {'FINISHED'}

