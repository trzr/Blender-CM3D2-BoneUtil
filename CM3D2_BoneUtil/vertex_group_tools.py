# -*- coding: utf-8 -*-

import bpy
import bmesh
import mathutils
import math
import os
import re
import sys
from . import common
from . import compatibility as compat
from typing import List, Any, Match, Set


def menu_func_specials(self, context: bpy.types.Context) -> None:
    if not common.prefs().feature_vgroups:
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
    self.layout.operator(BUTL_OT_Bone2VertexGroup.bl_idname, icon='BONE_DATA')


@compat.BlRegister()
class BUTL_OT_Bone2VertexGroup(bpy.types.Operator):
    """ボーン情報を元に頂点グループを作成するオペレータ"""

    bl_idname = 'object.trzr_bone_ot_vertex_group'
    bl_label = "butl.vgroups.ImportLabel"
    bl_description = "butl.vgroups.ImportDesc"
    bl_options = {'REGISTER', 'UNDO'}

    skip_nub = bpy.props.BoolProperty(name="butl.vgroups.SkipNub", default=True, description="butl.vgroups.SkipNubDesc")
    skip_shapekeys = bpy.props.BoolProperty(name="butl.vgroups.SkipShapeKeyName", default=True, description="butl.vgroups.SkipShapeKeyNameDesc")

    src_data = bpy.props.EnumProperty(
        name="Source",
        items=[
            ('Selected', 'butl.EnumSelected', "butl.EnumDescSelected", 'NONE', 0),
            ('All', 'butl.EnumAll', "butl.EnumDescDescendant", 'NONE', 1),
            ('LocalBoneData', 'LocalBoneData', "butl.EnumDescLocalBoneData", 'NONE', 2),
        ],
        default='All')

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
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

    def invoke(self, context: bpy.types.Context, event: Any) -> set:
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context: bpy.types.Context):  # type: () -> None
        row = self.layout.row()
        row.label(text="butl.DataSource:", icon='BONE_DATA')
        row = self.layout.row()
        row.prop(self, 'src_data', icon='BONE_DATA', expand=True)
        row = self.layout.row()
        row.label(text="butl.FilterConfig:", icon='FILTER')
        row = self.layout.row()
        row.prop(self, 'skip_nub', icon='GROUP_BONE')
        row = self.layout.row()
        row.prop(self, 'skip_shapekeys', icon='SHAPEKEY_DATA')
        # TODO armatureのBaseBoneかmeshのBaseBoneかを選択？

    def execute(self, context: bpy.types.Context) -> set:
        ob = context.active_object
        arm = ob.parent

        props = None
        bb_name = ob.get('BaseBone')
        if bb_name:
            props = ob
        else:
            bb_name = arm.data.get('BaseBone')
            if bb_name:
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
            self.report(type={'INFO'}, message="butl.vgroups.NotFoundSourceBone")
            return {'CANCELLED'}

        ignores = None
        if self.skip_shapekeys:
            shape_keys = ob.data.shape_keys
            if shape_keys:
                ignores = set()
                for key in shape_keys.key_blocks.keys():
                    ignores.add(key.lower())

        created = 0
        for bone_name in target_bonenames:
            if '_IK_' in bone_name:
                continue
            if bone_name == bb_name or bone_name in ob.vertex_groups:
                continue

            bone_name_l = bone_name.lower()
            if self.skip_nub and bone_name_l.endswith('nub'):
                continue
            if ignores and bone_name_l in ignores:
                continue

            ob.vertex_groups.new(bone_name)
            created += 1

        if created > 0:
            msg = bpy.app.translations.pgettext('butl.vgroups.VertexGroupCreated') % created
        else:
            msg = bpy.app.translations.pgettext('butl.vgroups.VertexGroupAlreadyExist')

        self.report(type={'INFO'}, message=msg)
        return {'FINISHED'}
