# -*- coding: utf-8 -*-

import bpy
import mathutils
import math
import os
import sys
from . import common
from . import compatibility as compat
from typing import Dict, Set, List, Tuple, Optional, Any


def menu_func(self, context: bpy.types.Context) -> None:
    if not common.prefs().feature_bonetype:
        return

    ob = context.active_object
    if not ob or ob.type != 'MESH' or ob.parent is None or ob.parent.type != 'ARMATURE':
        return
    if len(ob.parent.data.bones) == 0:
        return

    menu_func_common(self, context)


def menu_func_arm(self, context: bpy.types.Context) -> None:
    if not common.prefs().feature_bonetype:
        return

    ob = context.active_object
    if not ob or ob.type != 'ARMATURE' or len(ob.data.bones) == 0:
        return

    menu_func_common(self, context)


def menu_func_common(self, context: bpy.types.Context) -> None:
    layout = self.layout

    ybl = context.scene.trzr_butl_bone_props

    row = layout.row()
    col = row.column()
    split = compat.layout_split(col, factor=0.60, align=True)
    split.label(text="butl.ChangeBoneType", icon='BONE_DATA')
    split.operator(BUTL_OT_BoneListUpdater.bl_idname, icon='FILE_REFRESH', text="")

    ui_list = context.scene.trzr_butl_bone_list
    if len(ui_list.yure_bones) == 0:
        return

    if ybl.display_ybl:
        split.prop(ybl, 'display_ybl', text='', icon='TRIA_DOWN')  # icon='DOWNARROW_HLT')
    else:
        split.prop(ybl, 'display_ybl', text='', icon='TRIA_LEFT')  # icon='RIGHTARROW')

    # ListView
    if ybl.display_ybl:
        box = col.column(align=True).box().column()
        row = box.row(align=True)
        col = row.column(align=True)

        col.template_list('BUTL_UL_YureBoneList', '', ui_list, 'yure_bones', ui_list, 'item_idx', rows=2)
        col = row.column(align=True)
        col.operator(BUTL_OT_BoneListSelecter.bl_idname, icon=compat.icon('ADD'), text='')
        col.operator(BUTL_OT_BoneListDeselecter.bl_idname, icon=compat.icon('REMOVE'), text='')

        row = box.row()
        col = row.column(align=True)
        col.prop(ui_list, 'target_type', icon='BONE_DATA')

        # TODO filter
        # if len(ui_list.yure_bones):
        #     row = layout.row()
        #     row.prop(ui_list.yure_bones[ui_list.item_idx], "name")
        #     row = layout.row()
        #     row.prop(ui_list.yure_bones[ui_list.item_idx], "selected")
        row = box.row()
        label = bpy.app.translations.pgettext('butl.ChangeBoneType')
        row.operator(BUTL_OT_BoneTypeChanger.bl_idname, text=label)


@compat.BlRegister(use_bl_attr=False)
class YureBoneItem(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty()
    selected = bpy.props.BoolProperty()
    desc = bpy.app.translations.pgettext('Hardness')
    bone_types = [
        ('soft',     'yure_soft',     desc + ":(0.05, 0.5)", '', 0),
        ('hard',     'yure_hard',     desc + ":(0.1, 1)", '', 1),
        ('skirt',    'yure_skirt',    desc + ":(0.5, 0.9)", '', 2),
        ('skirt_h',  'yure_skirt_h',  desc + ":(0.95, 99999)", '', 3),
        ('hair',     'yure_hair',     desc + ":(0.05, 0.3)", '', 4),
        ('hair_h50', 'yure_hair_h50', desc + ":(0.1, 1)", '', 5),
        ('hair_h',   'yure_hair_h',   desc + ":(0.5, 3)", '', 6),
    ]
    bone_type = bpy.props.EnumProperty(name='BoneType', items=bone_types, default='soft')


@compat.BlRegister(use_bl_attr=False)
class ItemGroup(bpy.types.PropertyGroup):
    yure_bones = bpy.props.CollectionProperty(type=YureBoneItem, name='yure_bones')
    item_idx = bpy.props.IntProperty()

    target_type = bpy.props.EnumProperty(name='BoneType', items=YureBoneItem.bone_types, default='soft')


@compat.BlRegister(use_bl_attr=False)
class YureBoneProps(bpy.types.PropertyGroup):
    display_ybl = bpy.props.BoolProperty(
        name="butl.BonesList",
        description="Display Yure Bone List",
        default=False)


@compat.BlRegister(use_bl_attr=False)
class BUTL_UL_YureBoneList(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = compat.layout_split(layout, factor=0.05)
        split.prop(item, "selected", text="", icon='NONE')
        split = compat.layout_split(split, factor=0.80)
        split.label(text=item.name, translate=False, icon='BONE_DATA' )
        split.label(text=item.bone_type, translate=False, icon='NONE')


@compat.BlRegister()
class BUTL_OT_BoneListSelectItem(bpy.types.Operator):
    bl_idname = "trzr.butl_ot_bonelist_select_item"
    bl_label  = "Select Item"

    opr_type = bpy.props.StringProperty(default='')

    def execute(self, context: bpy.types.Context) -> set:

        ui_list = context.scene.trzr_butl_bone_list
        if self.opr_type == 'SELECT_ALL':
            for bone in ui_list.yure_bones:
                bone.selected = True
        elif self.opr_type == 'DESELECT_ALL':
            for bone in ui_list.yure_bones:
                bone.selected = False
        return {'FINISHED'}


# # custom list
# class ULItems(bpy.types.UIList):
#     bl_idname = 'BUTL_UL_custom_list'

#     def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
#         row = layout.row()
#         col2 = row.column(align=True)
#         col2.prop(item, "selected", text="", icon='NONE')

#         col1 = row.column(align=True)
#         col1.prop(item, "name", text="", emboss=False, translate=False, icon_value=icon)  # icon='NONE')

# @compat.make_annotations
# class CheckItem(bpy.types.PropertyGroup):
#     name = bpy.props.StringProperty()
#     replaced_name = bpy.props.StringProperty()


# class CheckList(bpy.types.UIList):
#     def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
#         split = compat.layout_split(layout, factor=0.5)
#         split.label(text=item.name, translate=False, icon='NONE' )
#         split.label(text=item.replaced_name, translate=False, icon='NONE')


# ========== Operator =====================================

@compat.BlRegister()
class BUTL_OT_BoneListSelecter(bpy.types.Operator):
    bl_idname = "trzr.butl_ot_yurebonelist_select_all"
    bl_label = "Select All"

    def execute(self, context:bpy.types.Context) -> set:
        for bone in context.scene.trzr_butl_bone_list.yure_bones:
            bone.selected = True
        return {'FINISHED'}


@compat.BlRegister()
class BUTL_OT_BoneListDeselecter(bpy.types.Operator): 
    bl_idname = "trzr.butl_ot_yurebonelist_deselect_all"
    bl_label = "Deselect All"

    def execute(self, context: bpy.types.Context) -> set:
        for bone in context.scene.trzr_butl_bone_list.yure_bones:
            bone.selected = False
        return {'FINISHED'}

@compat.BlRegister()
class BUTL_OT_BoneListUpdater(bpy.types.Operator):
    bl_idname = "trzr.butl_ot_refresh_bone_list"
    bl_label = "Refresh bone list"

    # @classmethod
    # def poll(cls, context: bpy.types.Context) -> bool:
    #     ob = context.active_object
    #     if ob is None:
    #         return False

    #     if ob.type == 'MESH':
    #         if ob.parent is None or ob.parent.type != 'ARMATURE':
    #             return False
    #         if len(ob.parent.data.bones) == 0:
    #             return False
    #     elif ob.type == 'ARMATURE':
    #         if len(ob.data.bones) == 0:
    #             return False
    #     else:
    #         return False

    #     return True

    def execute(self, context: bpy.types.Context) -> set:
        BUTL_OT_BoneListUpdater.refresh_bonelist(context)

        return {'FINISHED'}

    @classmethod
    def refresh_bonelist(cls, context: bpy.types.Context) -> None:
        ob = context.active_object
        
        if ob.type == 'MESH': # ob.parent and ob.parent.type == 'ARMATURE': # 呼び出し前に確認されている前提とする
            target_bones = ob.parent.data.bones
            target_props = context.active_object.items()
        elif ob.type == 'ARMATURE':
            target_bones = ob.data.bones
            target_props = context.active_object.data.items()

        ui_list = context.scene.trzr_butl_bone_list

        cls.refresh_list(ui_list, target_bones, target_props)

    @classmethod
    def refresh_list(cls, ui_list: ItemGroup, target_bones: dict, target_props: list) -> None:
        # 前回の選択状態を保持
        selected_dic = {}
        for bone in ui_list.yure_bones:
            selected_dic[bone.name] = bone.selected

        ui_list.yure_bones.clear()
        if len(target_bones) > 0:
            bone_names = cls.parse_bone_names(target_props)

            for bone in target_bones:
                if '_yure_' not in bone.name:
                    continue

                bone_type = common.parse_bonetype(bone.name)
                if bone_type is not None and bone.name in bone_names:
                    item = ui_list.yure_bones.add()
                    item.name = bone.name
                    item.bone_type = bone_type

                    item.selected = selected_dic[bone.name] if (bone.name in selected_dic) else False


    @classmethod
    def parse_bone_names(cls, target_props: list) -> set:
        bone_names = set()

        for item in target_props:
            prop_name, prop_val = item[0], item[1]
            if prop_name.startswith('BoneData:'):
                bd = prop_val.split(',', 1)
                bone_names.add(bd[0])
        return bone_names


@compat.BlRegister()
class BUTL_OT_BoneTypeChanger(bpy.types.Operator):
    bl_idname = "trzr.butl_ot_change_bonetype"
    bl_label = "change bone type"
    bl_options = {'REGISTER', 'UNDO'}

    count_lbd_replace = 0
    count_bd_replace = 0
    count_bdp_replace = 0

    def create_rename_list(self, context: bpy.types.Context) -> List[Tuple[str, str]]:
        ui_list = context.scene.trzr_butl_bone_list
        target_type = ui_list.target_type

        rename_list = []
        for bone in ui_list.yure_bones:
            if bone.selected and target_type != bone.bone_type:
                replaced = common.replace_bonename(bone.name, bone.bone_type, target_type)
                rename_list.append( (bone.name, replaced) )
        return rename_list

    def execute(self, context:bpy.types.Context) -> set:
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
        
        # 完了後にリストを更新
        BUTL_OT_BoneListUpdater.refresh_bonelist(context)
        return {'FINISHED'}

    def replace_props(self, context: bpy.types.Context, rename_list: List[Tuple[str, str]]) -> None:
        # max_idx = 0
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

