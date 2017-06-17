import os, sys, bpy, math, mathutils
import bmesh
from . import common

def update_select(edit_me, changed_vertices):
	selected = []
	for v in edit_me.verts:
		if v.select: selected.append(v.index)
	
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

class MESH_OP_select(bpy.types.Operator):
	bl_idname = 'mesh.trzr_select'
	bl_label = "SelectUtil"
	bl_description = bpy.app.translations.pgettext('selutl.SelPointDesc')
	bl_options = {'REGISTER', 'UNDO'}
	#bb_name       = bpy.props.StringProperty(name="BaseBoneName")
	target = bpy.props.EnumProperty(name="target", # range
		items = [
			('gt', '>',  "", '', 0),
			('ge', '>=', "", '', 1),
			('lt', '<',  "", '', 2),
			('le', '<=', "", '', 3),
			('eq', '==', "", '', 4)
		]
	)

	@classmethod
	def poll(cls, context):
		ob = context.active_object
		return (ob and ob.type == 'MESH' and context.mode == 'EDIT_MESH')
	
	def get_item(self, v_neighbors, v):
		item = v_neighbors[v.index]
		if item is None:
			item = []
			v_neighbors[v.index] = item
		return item
	
	def execute(self, context):
		ob = context.active_object
		me = ob.data
		edit_me = bmesh.from_edit_mesh(me)
		
		scn = context.scene
		is_select = (scn.TrzrSelUtilOpr == 'p')
		base = scn.TrzrSelUtilBase
		margin = scn.TrzrSelUtilMargin
		
		if scn.TrzrSelUtilAxis == 'x':
			get_val = lambda co: co.x
		elif scn.TrzrSelUtilAxis == 'y':
			get_val = lambda co: co.y
		else:
			get_val = lambda co: co.z
		
		changed_vertex = []
		def loop(edit_me, func): # type: (Any, Any)
			for v in edit_me.verts:
				if func(v):
					v.select = is_select
					if not is_select: changed_vertex.append(v)
		
		if self.target == 'gt':
			loop(edit_me, lambda v : get_val(v.co) > base + margin)
		elif self.target == 'ge':
			loop(edit_me, lambda v : get_val(v.co) >= base - margin)
		elif self.target == 'eq':
			loop(edit_me, lambda v : base - margin <= get_val(v.co) <= base + margin)
		elif self.target == 'le':
			loop(edit_me, lambda v : get_val(v.co) <= base + margin)
		elif self.target == 'lt':
			loop(edit_me, lambda v : get_val(v.co) < base - margin)
		
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
		
		bpy.context.scene.objects.active = bpy.context.scene.objects.active
		#bmesh.update_edit_mesh(me, True)
		self.report(type={'INFO'}, message="selutl.UpdateSelected")
		return {'FINISHED'}
		

class MESH_OP_select_symmetry(bpy.types.Operator):
	bl_idname = 'mesh.trzr_select_symmetry'
	bl_label = "SelectUtil"
	bl_description = bpy.app.translations.pgettext('selutl.SelSymmetricPointDesc')
	bl_options = {'REGISTER', 'UNDO'}
	#bb_name       = bpy.props.StringProperty(name="BaseBoneName")
	target = bpy.props.EnumProperty(name="target", # range
		items = [
			('gt', '>',  "", '', 0),
			('ge', '>=', "", '', 1),
			('lt', '<',  "", '', 2),
			('le', '<=', "", '', 3),
			('eq', '==', "", '', 4)
		]
	)

	@classmethod
	def poll(cls, context):
		ob = context.active_object
		return (ob and ob.type == 'MESH' and context.mode == 'EDIT_MESH')
	
	def get_item(self, v_neighbors, v):
		item = v_neighbors[v.index]
		if item is None:
			item = []
			v_neighbors[v.index] = item
		return item
		
	def execute(self, context):
		ob = context.active_object
		me = ob.data
		edit_me = bmesh.from_edit_mesh(me)
		
		scn = context.scene
		is_select = (scn.TrzrSelUtilOpr == 'p')
		base = scn.TrzrSelUtilBase
		margin = scn.TrzrSelUtilMargin

		lt = lambda val: val < 0
		gt = lambda val: val > 0
		def negative_x(co):	co.x = -co.x
		def negative_y(co):	co.y = -co.y
		def negative_z(co):	co.z = -co.z
		
		if scn.TrzrSelUtilAxis == 'x':
			get_val = lambda co: co.x
			negative_co = negative_x
		elif scn.TrzrSelUtilAxis == 'y':
			get_val = lambda co: co.y
			negative_co = negative_y
		else:
			get_val = lambda co: co.z
			negative_co = negative_z
		
		changed_vertices = []
		
		selected = []
		target = []
		if self.target == 'lt':
			infunc  = lt
			outfunc = gt
		elif self.target == 'gt':
			infunc  = gt
			outfunc = lt
		
		for v in edit_me.verts:
			val = get_val(me.vertices[v.index].co)
			if infunc(val):
				target.append(v.index)
			elif v.select and outfunc(val):
				selected.append(v.index)
		
		kd = mathutils.kdtree.KDTree(len(target))
		for vindex in target:
			kd.insert(me.vertices[vindex].co, vindex)
			# TODO active shapeに合わせた選択
			# else:
			# 	target_vert = target_shape_key.data[vindex]
			# 	kd.insert(target_vert.co, vindex)
		kd.balance()
		
		for vindex in selected:
			co = me.vertices[vindex].co.copy()
			negative_co(co)
			
			near_co, near_index, near_dist = kd.find(co)
			if near_dist <= margin:
				v = edit_me.verts[near_index]
				v.select = is_select
				if not is_select: changed_vertices.append(v)
		
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
		
		bpy.context.scene.objects.active = bpy.context.scene.objects.active
		#bmesh.update_edit_mesh(me, True)
		self.report(type={'INFO'}, message="selutl.UpdateSelected")
		return {'FINISHED'}


class VIEW3D_PT_tools_selectutil(bpy.types.Panel):
	bl_space_type  = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = 'Tools'
	bl_context  = "mesh_edit"
	bl_label = "SelectUtil"

	def draw(self, context):
		scn = context.scene
		
		layout = self.layout
		
		#row = layout.row(align=True)
		col = layout.column()
		split = col.split(0.5)
		row = split.row()
		row.label(text="selutl.Inclusion")
		row.prop(scn, 'TrzrSelUtilOpr', icon='ZOOMIN', expand=True)
		split.prop(scn, 'TrzrSelUtilAxis', icon='EMPTY_DATA')
		
		row = layout.row()
		
		split = row.split(0.18, align=True)
		split.label('Select')
		split.operator(MESH_OP_select.bl_idname, icon='NONE', text='< B' ).target='lt'
		split.operator(MESH_OP_select.bl_idname, icon='NONE', text='<= B').target='le'
		split.operator(MESH_OP_select.bl_idname, icon='NONE', text='== B').target='eq'
		split.operator(MESH_OP_select.bl_idname, icon='NONE', text='B <=').target='ge'
		split.operator(MESH_OP_select.bl_idname, icon='NONE', text='B <' ).target='gt'
		
		row = layout.row()
		split = row.split(0.18, align=True)
		split.label(' ')
		label=bpy.app.translations.pgettext('selutl.SymmetryLTB')
		split.operator(MESH_OP_select_symmetry.bl_idname, icon='NONE', text=label).target='lt'
		label=bpy.app.translations.pgettext('selutl.SymmetryGTB')
		split.operator(MESH_OP_select_symmetry.bl_idname, icon='NONE', text=label).target='gt'
		
		row = layout.row()
		split = row.split(0.75)
		split.prop(scn, 'TrzrSelUtilBase', icon='NONE')
		split.operator(MESH_OP_select_set_base.bl_idname, text='0')
		row = layout.row()
		split = row.split(0.75)
		split.prop(scn, 'TrzrSelUtilMargin', icon='NONE')
#		split.operator('mesh.select_util_set_margin', text='0').value=0
		split.operator(MESH_OP_select_set_margin.bl_idname, text='0.0001').value=0.0001
		
class MESH_OP_select_set_base(bpy.types.Operator):
	bl_idname = 'mesh.trzr_select_base_clear'
	bl_label = "clear base"
	bl_description = bpy.app.translations.pgettext('selutl.ClearBaseDesc')

	@classmethod
	def poll(cls, context):
		ob = context.active_object
		return (ob and ob.type == 'MESH' and context.mode == 'EDIT_MESH')

	def execute(self, context):
		
		ob = context.active_object
		scn = context.scene
		scn.TrzrSelUtilBase = 0.0
		return {'FINISHED'}

class MESH_OP_select_set_margin(bpy.types.Operator):
	bl_idname = 'mesh.trzr_select_set_margin'
	bl_label = "set default margin"
	bl_description = bpy.app.translations.pgettext('selutl.SetDefaultMarginDesc')
	
	value = bpy.props.FloatProperty(name="selutl.Margin", default=0.0001, min=0, soft_min=0, step=1, precision=5)
	
	@classmethod
	def poll(cls, context):
		ob = context.active_object
		return (ob and ob.type == 'MESH' and context.mode == 'EDIT_MESH')
	
	def execute(self, context):
		ob = context.active_object
		scn = context.scene
		scn.TrzrSelUtilMargin = self.value
		return {'FINISHED'}
	
def register():
	bpy.types.Scene.TrzrSelUtilOpr = bpy.props.EnumProperty(name='selutl.Inclusion',
		items = [
			('p', '+',  "", '', 0),
			('m', '-', "", '', 1)
		], default='p')
	
	bpy.types.Scene.TrzrSelUtilAxis = bpy.props.EnumProperty(name='Axis',
		items = [
			('x', 'x', "", '', 0),
			('y', 'y', "", '', 1),
			('z', 'z', "", '', 2)
		], default='x')
	
	bpy.types.Scene.TrzrSelUtilBase   = bpy.props.FloatProperty(name='selutl.BasePointB', default=0.0, step=0.1, precision=5)
	bpy.types.Scene.TrzrSelUtilMargin = bpy.props.FloatProperty(name='selutl.Margin', default=0.0001, min=0, soft_min=0, step=0.01, precision=5)
	
def unregister():
	del bpy.types.Scene.TrzrSelUtilOpr
	del bpy.types.Scene.TrzrSelUtilAxis
	del bpy.types.Scene.TrzrSelUtilBase
	del bpy.types.Scene.TrzrSelUtilMargin
