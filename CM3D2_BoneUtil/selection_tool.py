# -*- coding: utf-8 -*-

import bpy
import bmesh
import mathutils

from . import compatibility as compat
from typing import Dict, Set, List, Tuple, Optional, Any, Callable


@compat.BlRegister(use_bl_attr=False)
class LocalProps(bpy.types.PropertyGroup):
    opr = bpy.props.EnumProperty(
        name='selutl.Inclusion',
        items=[
            ('p', '+', "", '', 0),
            ('m', '-', "", '', 1)
        ], default='p')

    axis = bpy.props.EnumProperty(
        name='Axis',
        items=[
            ('x', 'x', "", '', 0),
            ('y', 'y', "", '', 1),
            ('z', 'z', "", '', 2)
        ], default='x')

    base = bpy.props.FloatProperty(name='selutl.BasePointB', default=0.0, step=0.1, precision=5)
    margin = bpy.props.FloatProperty(name='selutl.Margin', default=0.0001, min=0, soft_min=0, step=0.01, precision=5)

    key = bpy.props.StringProperty(name="selutl.Key", default='')
    ignore_case = bpy.props.BoolProperty(name="selutl.Ignorecase", default=True)


def update_select(edit_me, changed_vertices):  # type: (Any, List) -> None
    # selected = [v.index for v in edit_me.verts if v.select]
    selected = []
    for v in edit_me.verts:
        if v.select:
            selected.append(v.index)

    # ensure_lookup_table()は、いったん操作後にドロップダウンから再操作に対応するため
    edit_me.faces.ensure_lookup_table()
    edit_me.edges.ensure_lookup_table()
    edit_me.verts.ensure_lookup_table()

    # 以下のedge, facesの選択状態を変更すると関連する頂点も非選択になる
    # このため、現時点の選択状態を保持し、再度反映させる
    for v in changed_vertices:
        for f in v.link_faces:
            edit_me.faces[f.index].select = False
        for e in v.link_edges:
            edit_me.edges[e.index].select = False

    # backup
    for idx in selected:
        edit_me.verts[idx].select = True


@compat.BlRegister()
class BUTL_OT_ArmSelectNameOprator(bpy.types.Operator):
    bl_idname = 'armature.trzr_select_name'
    bl_label = "Select bones"
    bl_description = bpy.app.translations.pgettext('selutl.SelBoneByNameDesc')
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        ob = context.active_object
        if ob and ob.type == 'ARMATURE':  # and (context.mode == 'POSE' or context.mode == 'EDIT_ARMATURE'))
            return len(context.scene.trzr_select_props.key) > 0
        return False

    def execute(self, context: bpy.types.Context) -> set:
        ob = context.active_object
        arm = ob.data

        bones = arm.edit_bones
        sel_props = context.scene.trzr_select_props
        is_select = (sel_props.opr == 'p')
        key = sel_props.key
        ignore_case = sel_props.ignore_case

        for b in bones:
            if ignore_case:
                if key.lower() in b.name.lower():
                    b.select, b.select_head, b.select_tail = is_select, is_select, is_select
            elif key in b.name:
                b.select, b.select_head, b.select_tail = is_select, is_select, is_select

        self.report(type={'INFO'}, message="selutl.UpdateSelectedBones")
        return {'FINISHED'}


@compat.BlRegister()
class BUTL_OT_ArmSelectOperator(bpy.types.Operator):
    bl_idname = 'armature.trzr_butl_select_arm'
    bl_label = "Select bones"
    bl_description = bpy.app.translations.pgettext('selutl.SelBoneDesc')
    bl_options = {'REGISTER', 'UNDO'}

    target = bpy.props.EnumProperty(
        name="target",
        items=[
            ('gt', '>',  "", '', 0),
            ('ge', '>=', "", '', 1),
            ('lt', '<',  "", '', 2),
            ('le', '<=', "", '', 3),
            ('eq', '==', "", '', 4)
        ])

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        ob = context.active_object
        return ob and ob.type == 'ARMATURE'  # and (context.mode == 'POSE' or context.mode == 'EDIT_ARMATURE')

    def execute(self, context: bpy.types.Context) -> set:
        ob = context.active_object
        arm = ob.data

        sel_props = context.scene.trzr_select_props

        is_select = (sel_props.opr == 'p')
        base = sel_props.base
        margin = sel_props.margin

        if sel_props.axis == 'x':
            get_val = lambda b: b.head.x
        elif sel_props.axis == 'y':
            get_val = lambda b: b.head.y
        else:
            get_val = lambda b: b.head.z

        def loop(bone_list, func):  # type: ignore
            for b in bone_list:
                if func(b):
                    b.select, b.select_head, b.select_tail = is_select, is_select, is_select

        bones = arm.edit_bones
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


@compat.BlRegister()
class BUTL_OT_MeshSelectOperator(bpy.types.Operator):
    bl_idname = 'mesh.trzr_butl_select_mesh'
    bl_label = 'SelectUtil'
    bl_description = bpy.app.translations.pgettext('selutl.SelPointDesc')
    bl_options = {'REGISTER', 'UNDO'}

    # bb_name       = bpy.props.StringProperty(name="BaseBoneName")
    target = bpy.props.EnumProperty(
        name="target",
        items=[
            ('gt', '>',  "", '', 0),
            ('ge', '>=', "", '', 1),
            ('lt', '<',  "", '', 2),
            ('le', '<=', "", '', 3),
            ('eq', '==', "", '', 4)
        ])

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        ob = context.active_object
        return ob and ob.type == 'MESH' and context.mode == 'EDIT_MESH'

    def _get_item(self, v_neighbors, v):
        item = v_neighbors[v.index]
        if item is None:
            item = []
            v_neighbors[v.index] = item
        return item

    def execute(self, context: bpy.types.Context) -> set:
        ob = context.active_object
        me = ob.data
        edit_me = bmesh.from_edit_mesh(me)
        sel_props = context.scene.trzr_select_props

        is_select = (sel_props.opr == 'p')
        base = sel_props.base
        margin = sel_props.margin

        if sel_props.axis == 'x':
            get_val = lambda co: co.x
        elif sel_props.axis == 'y':
            get_val = lambda co: co.y
        else:
            get_val = lambda co: co.z

        changed_vertex = []  # type: List[Any]

        def loop(me_list, func):  # type: (Any, Callable) -> None
            for v in me_list.verts:
                if func(v):
                    v.select = is_select
                    if not is_select:
                        changed_vertex.append(v)

        if self.target == 'gt':
            loop(edit_me, lambda v: get_val(v.co) > base + margin)  # type: ignore
        elif self.target == 'ge':
            loop(edit_me, lambda v: get_val(v.co) >= base - margin)  # type: ignore
        elif self.target == 'eq':
            loop(edit_me, lambda v: base - margin <= get_val(v.co) <= base + margin)  # type: ignore
        elif self.target == 'le':
            loop(edit_me, lambda v: get_val(v.co) <= base + margin)  # type: ignore
        elif self.target == 'lt':
            loop(edit_me, lambda v: get_val(v.co) < base - margin)  # type: ignore

        # edge
        if is_select:
            for e in edit_me.edges:
                if e.verts[0].select and e.verts[1].select:
                    e.select = True
            # Face
            for f in edit_me.faces:
                if all(v.select for v in f.verts):
                    f.select = True

        else:
            update_select(edit_me, changed_vertex)

        # common.update_active()
        bmesh.update_edit_mesh(me)
        self.report(type={'INFO'}, message="selutl.UpdateSelected")
        return {'FINISHED'}


def negative_x(co: mathutils.Vector):
    co.x = -co.x

def negative_y(co: mathutils.Vector):
    co.y = -co.y

def negative_z(co: mathutils.Vector):
    co.z = -co.z


@compat.BlRegister()
class BUTL_OT_MeshSelectSymOperator(bpy.types.Operator):
    bl_idname = 'mesh.trzr_butl_ot_select_symmetry'
    bl_label = "Select"
    bl_description = bpy.app.translations.pgettext('selutl.SelSymmetricPointDesc')
    bl_options = {'REGISTER', 'UNDO'}
    target = bpy.props.EnumProperty(
        name="target",
        items=[
            ('gt', '>', "", '', 0),
            ('lt', '<', "", '', 1),
        ])

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        ob = context.active_object
        return ob and ob.type == 'MESH' and context.mode == 'EDIT_MESH'

    def _get_item(self, v_neighbors, v):
        item = v_neighbors[v.index]
        if item is None:
            item = []
            v_neighbors[v.index] = item
        return item

    def execute(self, context: bpy.types.Context) -> set:
        ob = context.active_object
        me = ob.data
        edit_me = bmesh.from_edit_mesh(me)
        sel_props = context.scene.trzr_select_props

        is_select = (sel_props.opr == 'p')
        # base = sel_props.base
        margin = sel_props.margin

        lt = lambda val: val < 0  # type: Callable[[int], bool]
        gt = lambda val: val > 0  # type: Callable[[int], bool]

        get_val = None  # type: Optional[Callable[[Any], float]]
        negative_co = None  # type: Optional[Callable[[mathutils.Vector], None]]
        if sel_props.axis == 'x':
            get_val = lambda co: co.x
            negative_co = negative_x
        elif sel_props.axis == 'y':
            get_val = lambda co: co.y
            negative_co = negative_y
        else:
            get_val = lambda co: co.z
            negative_co = negative_z

        changed_vertices = []

        selected = []
        target_verts = []
        if self.target == 'lt':
            infunc = lt
            outfunc = gt
        elif self.target == 'gt':
            infunc = gt
            outfunc = lt

        for v in edit_me.verts:
            val = get_val(me.vertices[v.index].co)
            if infunc(val):
                target_verts.append(v.index)
            elif v.select and outfunc(val):
                selected.append(v.index)

        kd = mathutils.kdtree.KDTree(len(target_verts))
        for vindex in target_verts:
            kd.insert(me.vertices[vindex].co, vindex)
            # TODO active shapeに合わせた選択
            # else:
            #     target_vert = target_shape_key.data[vindex]
            #     kd.insert(target_vert.co, vindex)
        kd.balance()

        for vindex in selected:
            co = me.vertices[vindex].co.copy()
            negative_co(co)  # type: ignore

            near_co, near_index, near_dist = kd.find(co)
            if near_dist <= margin:
                v = edit_me.verts[near_index]
                v.select = is_select
                if not is_select:
                    changed_vertices.append(v)

        # edge
        if is_select:
            for e in edit_me.edges:
                if e.verts[0].select and e.verts[1].select:
                    e.select = True
            # Face
            for f in edit_me.faces:
                if all(v.select for v in f.verts):
                    f.select = True
        else:
            update_select(edit_me, changed_vertices)

        # common.update_active()
        bmesh.update_edit_mesh(me)
        self.report(type={'INFO'}, message="selutl.UpdateSelected")
        return {'FINISHED'}


@compat.BlRegister()
class BUTL_OT_SelectBaseClearer(bpy.types.Operator):
    bl_idname = 'trzr.butl_ot_select_base_clear'
    bl_label = 'clear base'
    bl_description = bpy.app.translations.pgettext('selutl.ClearBaseDesc')

    def execute(self, context:bpy.types.Context) -> set:
        context.scene.trzr_select_props.base = 0.0
        return {'FINISHED'}


@compat.BlRegister()
class BUTL_OT_SelectMarginSetter(bpy.types.Operator):
    bl_idname = 'trzr.butl_ot_select_set_margin'
    bl_label = "set default margin"
    bl_description = bpy.app.translations.pgettext('selutl.SetDefaultMarginDesc')

    value = bpy.props.FloatProperty(name="selutl.Margin", default=0.0001, min=0, soft_min=0, step=1, precision=5)

    def execute(self, context: bpy.types.Context) -> set:
        context.scene.trzr_select_props.margin = self.value
        return {'FINISHED'}


class BaseSelectPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = compat.region_type()
    bl_category = 'Select'
    bl_label = "Select"

    opr_idname = None
    clearer_idname = BUTL_OT_SelectBaseClearer.bl_idname
    setter_idname = BUTL_OT_SelectMarginSetter.bl_idname

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        sel_props = context.scene.trzr_select_props

        # row = layout.row(align=True)
        col = layout.column()
        split = compat.layout_split(col, factor=0.5)
        row = split.row()
        row.label(text='selutl.Inclusion')

        row.prop(sel_props, 'opr', expand=True)
        split.prop(sel_props, 'axis', icon='EMPTY_DATA')

        row = layout.row()
        split = compat.layout_split(row, factor=0.18, align=True)
        split.label(text='Select')
        split.operator(self.opr_idname, icon='NONE', text='< B').target = 'lt'
        split.operator(self.opr_idname, icon='NONE', text='≦ B').target = 'le'
        split.operator(self.opr_idname, icon='NONE', text='= B').target = 'eq'
        split.operator(self.opr_idname, icon='NONE', text='B ≦').target = 'ge'
        split.operator(self.opr_idname, icon='NONE', text='B <').target = 'gt'

        self.draw_symmetry(layout, sel_props)

        row = layout.row()
        split = compat.layout_split(row, factor=0.75)
        split.prop(sel_props, 'base', icon='NONE')
        split.alignment = 'RIGHT'
        split.operator(self.clearer_idname, text='0')

        row = layout.row()
        split = compat.layout_split(row, factor=0.75)
        split.prop(sel_props, 'margin', icon='NONE')
        # split.operator('armature.select_util_set_margin', text='0').value=0
        split.operator(self.setter_idname, text='0.0001').value = 0.0001

        self.draw_filter(layout, sel_props)

    def draw_symmetry(self, layout: bpy.types.UILayout, sel_props: LocalProps) -> None:
        pass

    def draw_filter(self, layout: bpy.types.UILayout, sel_props: LocalProps) -> None:
        pass


@compat.BlRegister()
class BUTL_PT_ArmSelectPanel(BaseSelectPanel):
    bl_context = "armature_edit"  # "posemode"

    opr_idname = BUTL_OT_ArmSelectOperator.bl_idname

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        ob = context.active_object
        return ob and ob.type == 'ARMATURE' and (context.mode == 'POSE' or context.mode == 'EDIT_ARMATURE')

    def draw_filter(self, layout: bpy.types.UILayout, sel_props: LocalProps) -> None:
        row = layout.row()
        split = compat.layout_split(row, factor=0.75)
        split.prop(sel_props, 'key', icon='NONE')
        split.operator(BUTL_OT_ArmSelectNameOprator.bl_idname, icon='NONE', text='Select')

        row = layout.row()
        row.alignment = 'RIGHT'
        row.prop(sel_props, 'ignore_case', icon='NONE')


@compat.BlRegister()
class BUTL_PT_MeshSelectPanel(BaseSelectPanel):
    bl_context = "mesh_edit"

    opr_idname = BUTL_OT_MeshSelectOperator.bl_idname

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        ob = context.active_object
        return ob and ob.type == 'MESH' and context.mode == 'EDIT_MESH'

    def draw_symmetry(self, layout: bpy.types.UILayout, sel_props: LocalProps) -> None:
        row = layout.row()
        split = compat.layout_split(row, factor=0.18, align=True)
        split.label(text=' ')
        label = bpy.app.translations.pgettext('selutl.SymmetryLTB')
        split.operator(BUTL_OT_MeshSelectSymOperator.bl_idname, icon='NONE', text=label).target = 'lt'
        label = bpy.app.translations.pgettext('selutl.SymmetryGTB')
        split.operator(BUTL_OT_MeshSelectSymOperator.bl_idname, icon='NONE', text=label).target = 'gt'


