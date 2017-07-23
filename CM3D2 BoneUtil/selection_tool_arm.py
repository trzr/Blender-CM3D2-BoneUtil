# -*- coding: utf-8 -*-

import bpy  # type: ignore
from typing import Dict, Set, List, Tuple, Optional, Any, Callable


class ArmSelectNameOprator(bpy.types.Operator):  # type: ignore
    bl_idname = 'armature.trzr_select_name'
    bl_label = "Select bones"
    bl_description = bpy.app.translations.pgettext('selutl.SelBoneByNameDesc')
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):  # type: (bpy.types.Context) -> bool
        ob = context.active_object
        if ob and ob.type == 'ARMATURE':  # and (context.mode == 'POSE' or context.mode == 'EDIT_ARMATURE'))
            return len(context.scene.TrzrSelUtilKey) > 0
        return False

    def execute(self, context):  # type: (bpy.types.Context) -> Set
        ob = context.active_object
        arm = ob.data

        bones = arm.edit_bones
        scn = context.scene
        is_select = (scn.TrzrSelUtilOpr == 'p')
        key = scn.TrzrSelUtilKey
        ignorecase = scn.TrzrSelUtilIgnoreCase

        for b in bones:
            if ignorecase:
                if key.lower() in b.name.lower():
                    b.select, b.select_head, b.select_tail = is_select, is_select, is_select
            elif key in b.name:
                b.select, b.select_head, b.select_tail = is_select, is_select, is_select

        self.report(type={'INFO'}, message="selutl.UpdateSelectedBones")
        return {'FINISHED'}


class ArmSelectOperator(bpy.types.Operator):  # type: ignore
    bl_idname = 'armature.trzr_select'
    bl_label = "Select bones"
    bl_description = bpy.app.translations.pgettext('selutl.SelBoneDesc')
    bl_options = {'REGISTER', 'UNDO'}

    target = bpy.props.EnumProperty(
        name="target",
        items=[
            ('gt', '>', "", '', 0),
            ('ge', '>=', "", '', 1),
            ('lt', '<', "", '', 2),
            ('le', '<=', "", '', 3),
            ('eq', '==', "", '', 4)
        ])

    @classmethod
    def poll(cls, context):  # type: (bpy.types.Context) -> bool
        ob = context.active_object
        return ob and ob.type == 'ARMATURE'  # and (context.mode == 'POSE' or context.mode == 'EDIT_ARMATURE')

    def execute(self, context):  # type: (bpy.types.Context) -> Set
        ob = context.active_object
        arm = ob.data

        scn = context.scene
        is_select = (scn.TrzrSelUtilOpr == 'p')
        base = scn.TrzrSelUtilBase
        margin = scn.TrzrSelUtilMargin

        if scn.TrzrSelUtilAxis == 'x':
            get_val = lambda b: b.head.x
        elif scn.TrzrSelUtilAxis == 'y':
            get_val = lambda b: b.head.y
        else:
            get_val = lambda b: b.head.z

        bones = arm.edit_bones

        def loop(bone_list, func):  # type: ignore
            for b in bone_list:
                if func(b):
                    b.select, b.select_head, b.select_tail = is_select, is_select, is_select

        if self.target == 'gt':
            loop(bones, lambda b: get_val(b) > base + margin)  # type: ignore
        elif self.target == 'ge':
            loop(bones, lambda b: get_val(b) >= base - margin)  # type: ignore
        elif self.target == 'eq':
            loop(bones, lambda b: base - margin <= get_val(b) <= base + margin )  # type: ignore
        elif self.target == 'le':
            loop(bones, lambda b: get_val(b) <= base + margin )  # type: ignore
        elif self.target == 'lt':
            loop(bones, lambda b: get_val(b) < base - margin )  # type: ignore

        self.report(type={'INFO'}, message="selutl.UpdateSelectedBones")
        return {'FINISHED'}


class ArmSelectPanel(bpy.types.Panel):  # type: ignore
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Tools'
    bl_context = "armature_edit"  # "posemode"
    bl_label = "SelectUtil"

    @classmethod
    def poll(cls, context):  # type: (bpy.types.Context) -> bool
        ob = context.active_object
        return ob and ob.type == 'ARMATURE' and (context.mode == 'POSE' or context.mode == 'EDIT_ARMATURE')

    def draw(self, context):  # type: (bpy.types.Context) -> None
        scn = context.scene

        layout = self.layout

        # row = layout.row(align=True)
        col = layout.column()
        split = col.split(0.5)
        row = split.row()
        row.label(text="selutl.Inclusion")
        row.prop(scn, 'TrzrSelUtilOpr', icon='ZOOMIN', expand=True)
        split.prop(scn, 'TrzrSelUtilAxis', icon='EMPTY_DATA')

        row = layout.row()

        split = row.split(0.18, align=True)
        split.label('Select')
        split.operator(ArmSelectOperator.bl_idname, icon='NONE', text='< B').target = 'lt'
        split.operator(ArmSelectOperator.bl_idname, icon='NONE', text='<= B').target = 'le'
        split.operator(ArmSelectOperator.bl_idname, icon='NONE', text='== B').target = 'eq'
        split.operator(ArmSelectOperator.bl_idname, icon='NONE', text='B <=').target = 'ge'
        split.operator(ArmSelectOperator.bl_idname, icon='NONE', text='B <').target = 'gt'

        row = layout.row()
        split = row.split(0.75)
        split.prop(scn, 'TrzrSelUtilBase', icon='NONE')
        split.alignment = 'RIGHT'
        split.operator(ArmSelectBaseClearer.bl_idname, text='0')
        row = layout.row()
        split = row.split(0.75)
        split.prop(scn, 'TrzrSelUtilMargin', icon='NONE')
        # split.operator('armature.select_util_set_margin', text='0').value=0
        split.operator(ArmSelectMarginSetter.bl_idname, text='0.0001').value = 0.0001

        row = layout.row()
        split = row.split(0.75)
        split.prop(scn, 'TrzrSelUtilKey', icon='NONE')
        split.operator(ArmSelectNameOprator.bl_idname, icon='NONE', text='Select')
        row = layout.row()
        row.alignment = 'RIGHT'
        row.prop(scn, 'TrzrSelUtilIgnoreCase', icon='NONE')
        # clear button
        # split.operator('armature.select_util_set_base', text='0')


class ArmSelectBaseClearer(bpy.types.Operator):  # type: ignore
    bl_idname = 'armature.trzr_select_base_clear'
    bl_label = "clear base"
    bl_description = bpy.app.translations.pgettext('selutl.ClearBaseDesc')

    # @classmethod
    # def poll(cls, context):  # type: (bpy.types.Context) -> bool
    #     ob = context.active_object
    #     return (ob and ob.type == 'ARMATURE' and (context.mode == 'POSE' or context.mode == 'EDIT_ARMATURE'))

    def execute(self, context):  # type: (bpy.types.Context) -> Set
        scn = context.scene
        scn.TrzrSelUtilBase = 0.0
        return {'FINISHED'}


class ArmSelectMarginSetter(bpy.types.Operator):  # type: ignore
    bl_idname = 'armature.trzr_select_set_margin'
    bl_label = "set default margin"
    bl_description = bpy.app.translations.pgettext('selutl.SetDefaultMarginDesc')

    value = bpy.props.FloatProperty(name="selutl.Margin", default=0.0001, min=0, soft_min=0, step=1, precision=5)

    # @classmethod
    # def poll(cls, context):  # type: (bpy.types.Context) -> bool
    #     ob = context.active_object
    #     return (ob and ob.type == 'ARMATURE' and (context.mode == 'POSE' or context.mode == 'EDIT_ARMATURE'))

    def execute(self, context):  # type: (bpy.types.Context) -> Set
        scn = context.scene
        scn.TrzrSelUtilMargin = self.value
        return {'FINISHED'}


def register():  # type: () -> None
    bpy.types.Scene.TrzrSelUtilKey = bpy.props.StringProperty(name="selutl.Key", default='')
    bpy.types.Scene.TrzrSelUtilIgnoreCase = bpy.props.BoolProperty(name="selutl.Ignorecase", default=True)


def unregister():  # type: () -> None
    del bpy.types.Scene.TrzrSelUtilKey
