import os, sys, bpy, math, mathutils
from . import common
# メニュー等に項目追加
def menu_func(self, context):
	ob = context.active_object
	if not ob or ob.type != 'MESH': return
	if ob.data.shape_keys is None: return
	
	box = self.layout.box()
	box.label(text="shapekey.BatchOperation", icon='HAND')
	
	# row = box.split(percentage=0.005)
	# row.label(text='') # indent
	
	col = box.column()
	#row = col.split(percentage=0.5)
	sub_row1 = col.row(align=True)
	sub_row1.label(text='shapekey.BlendsetOpeation')
	label = bpy.app.translations.pgettext('shapekey.CopySet')
	sub_row1.operator('shapekey.copy_blendsets', icon='COPYDOWN', text=label)
	label = bpy.app.translations.pgettext('shapekey.PasteSet')
	sub_row1.operator('shapekey.paste_blendsets', icon='PASTEDOWN', text=label)
	label = bpy.app.translations.pgettext('shapekey.ClearSet')
	sub_row1.operator('shapekey.clear_blendsets', icon='X', text=label)
	
	has_target = False
	ob = context.active_object
	if ob and ob.type == 'MESH':
		for prop_key in ob.data.keys():
			if prop_key.startswith('blendset:'):
				has_target = True
				break
	
	#if has_target:
	bsl = context.window_manager.blendset_list
	refresh_list(self, context, bsl, ob.data)
	
	split = col.split(percentage=0.15, align=True)
	if bsl.display_list:
		split.prop(bsl, "display_list", text="", icon='TRIA_DOWN')
	else:
		split.prop(bsl, "display_list", text="", icon='TRIA_RIGHT')
	
	sub_row = split.row()
	bs_count = len(bsl.blendset_items)
	sub_row.label(text="shapekey.BlendsetList", icon='SHAPEKEY_DATA')
	subsub_row = sub_row.row()
	subsub_row.alignment = 'RIGHT'
	subsub_row.label(text=str(bs_count), icon='CHECKBOX_HLT')
	
	if bsl.display_list:
		row = col.row(align=True)
		col1 = row.column(align=True)
		col1.template_list("BlendsetList", "", bsl, "blendset_items", bsl, "item_idx", rows=2)
		
		if bsl.item_idx != bsl.prev_idx:
			if bsl.item_idx >= 0 and bsl.item_idx < bs_count:
				bsl.target_name = bsl.blendset_items[bsl.item_idx].name
			else:
				bsl.target_name = ""
			bsl.prev_idx = bsl.item_idx
		
		row1 = col.row(align=True)
		split1 = row1.split(percentage=0.6, align=True)
		split1.prop(bsl, "target_name", text="")
		label = bpy.app.translations.pgettext('shapekey.Reflect')
		split1.operator('shapekey.reflect_blendset', icon='MOVE_DOWN_VEC', text=label)
		label = bpy.app.translations.pgettext('shapekey.Regist')
		split1.operator('shapekey.regist_blendset', icon='MOVE_UP_VEC', text=label)
		
		subsplit = split1.split(percentage=0.5, align=True)
		subsplit.operator('shapekey.add_blendset', icon='ZOOMIN', text='')
		subsplit.operator('shapekey.del_blendset', icon='ZOOMOUT', text='')
	
	# bottom
	col = col.column()
	row = col.row(align=True)
	row.label(text='shapekey.ShapeKeyVal')
	label = bpy.app.translations.pgettext('shapekey.CopyValue')
	row.operator('shapekey.copy_blendset', icon='COPYDOWN', text=label)
	label = bpy.app.translations.pgettext('shapekey.PasteValue')
	row.operator('shapekey.paste_blendset', icon='PASTEDOWN', text=label)
	

def refresh_list(self, context, bs_list, target_props):
	bs_list.blendset_items.clear()
	for propkey in target_props.keys():
		if propkey.startswith('blendset:'):
			item = bs_list.blendset_items.add()
			item.name = propkey[9:]

class paste_blendsets(bpy.types.Operator):
	bl_idname = 'shapekey.paste_blendsets'
	bl_label       = bpy.app.translations.pgettext('shapekey.PasteBlendsets')
	bl_description = bpy.app.translations.pgettext('shapekey.PasteBlendsets.Desc')
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, context):
		ob = context.active_object
		if ob and ob.type == 'MESH':
			clipboard = context.window_manager.clipboard
			if 'blendset' in clipboard:
				return True
		return False
	
	def execute(self, context):
		ob = context.active_object
		props = ob.data
		# clear
		for prop_key in props.keys():
			if prop_key.startswith('blendset:'):
				del props[prop_key]
		
		set_item_count, idx = 0, 0
		lines = context.window_manager.clipboard.split('\n')
		line_len = len(lines)
		on_blendset = False
		kv_list = []
		bs_name = ''
		while idx+1 < line_len:
			key = lines[idx].strip()
			if key == 'blendset':
				on_blendset = True
				bs_name = lines[idx+1].strip()
				idx += 2
				continue
			
			if on_blendset:
				if key == '':
					on_blendset = False
					if len(kv_list) > 0:
						text = ''
						for kv in kv_list:
							text += kv[0] + " " + kv[1] + ","
						props['blendset:' + bs_name] = text
						set_item_count += 1
						kv_list.clear()
					idx += 1
				else:
					val = lines[idx+1].strip()
					try:
						float(val)
						kv_list.append( (key, val) )
					except:
						msg = bpy.app.translations.pgettext('shapekey.ParseFailed')
						self.report(type={'WARNING'}, message=msg % val)
						continue
					idx += 2
			else:
				idx += 1
		
		# 
		if len(kv_list) > 0:
			text = ''
			for kv in kv_list:
				text += kv[0] + " " + kv[1] + ","
			props['blendset:' + bs_name] = text
			set_item_count += 1
			kv_list.clear()
		msg = bpy.app.translations.pgettext('shapekey.PasteBlendsets.Finished')
		self.report(type={'INFO'}, message=msg % set_item_count)
		return {'FINISHED'}

class copy_blendsets(bpy.types.Operator):
	bl_idname = 'shapekey.copy_blendsets'
	bl_label       = bpy.app.translations.pgettext('shapekey.CopyBlendsets')
	bl_description = bpy.app.translations.pgettext('shapekey.CopyBlendsets.Desc')
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, context):
		ob = context.active_object
		if ob and ob.type == 'MESH':
			for prop_key in ob.data.keys():
				if prop_key.startswith('blendset:'):
					return True
		return False
	
	def execute(self, context):
		output_text = ""
		
		ob = context.active_object
		for propkey, propval in ob.data.items():
			if propkey.startswith('blendset:'):
				output_text += "blendset\n"
				output_text += "\t" + propkey[9:] + "\n"
				
				for val in propval.split(','):
					if len(val) > 2:
						entry = val.split(' ')
						output_text += "\t" + entry[0] + "\n"
						output_text += "\t" + entry[1] + "\n"
				output_text += "\n"
		
		context.window_manager.clipboard = output_text
		msg = bpy.app.translations.pgettext('shapekey.CopyBlendsets.Finished')
		self.report(type={'INFO'}, message=msg)
		return {'FINISHED'}

class clear_blendsets(bpy.types.Operator):
	bl_idname = 'shapekey.clear_blendsets'
	bl_label       = bpy.app.translations.pgettext('shapekey.ClearBlendsets')
	bl_description = bpy.app.translations.pgettext('shapekey.ClearBlendsets.Desc')
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, context):
		ob = context.active_object
		if ob and ob.type == 'MESH':
			for prop_key in ob.data.keys():
				if prop_key.startswith('blendset:'):
					return True
		return False
	
	def execute(self, context):
		ob = context.active_object
		props = ob.data
		
		for prop_key in props.keys():
			if prop_key.startswith('blendset:'):
				del props[prop_key]
		
		msg = bpy.app.translations.pgettext('shapekey.CopyBlendsets.Finished')
		self.report(type={'INFO'}, message=msg)
		return {'FINISHED'}

class reflect_blendset(bpy.types.Operator):
	bl_idname = 'shapekey.reflect_blendset'
	bl_label       = bpy.app.translations.pgettext('shapekey.ReflectBlendset')
	bl_description = bpy.app.translations.pgettext('shapekey.ReflectBlendset.Desc')
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, context):
		ob = context.active_object
		if ob and ob.type == 'MESH':
			bsl = context.window_manager.blendset_list
			if bsl.target_name in bsl.blendset_items:
				return True
		return False
	
	def execute(self, context):
		bsl = context.window_manager.blendset_list
		target_name = bsl.target_name
		
		ob = context.active_object
		bs_text = ob.data['blendset:' + target_name]
		
		me = ob.data
		key_blocks = me.shape_keys.key_blocks
		# reset
		for key_block in key_blocks.values():
			key_block.value = 0.0
		
		for val in bs_text.split(','):
			if len(val) > 2:
				entry = val.split(' ')
				try:
					key = entry[0].lower()
					numval = float(entry[1])
					if key in key_blocks:
						key_blocks[key].value = numval/100
					else:
						msg = bpy.app.translations.pgettext('shapekey.KeyNotFound')
						self.report(type={'WARNING'}, message=msg % key)
				except:
					continue
		
		msg = bpy.app.translations.pgettext('shapekey.ReflectBlendset.Finished')
		self.report(type={'INFO'}, message=msg % target_name)
		return {'FINISHED'}

class regist_blendset(bpy.types.Operator):
	bl_idname = 'shapekey.regist_blendset'
	bl_label       = bpy.app.translations.pgettext('shapekey.RegistBlendset')
	bl_description = bpy.app.translations.pgettext('shapekey.RegistBlendset.Desc')
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, context):
		ob = context.active_object
		if ob and ob.type == 'MESH':
			bsl = context.window_manager.blendset_list
			if bsl.target_name in bsl.blendset_items:
				return True
		return False
	
	def execute(self, context):
		bsl = context.window_manager.blendset_list
		target_name = bsl.target_name
		
		ob = context.active_object
		key_blocks = ob.data.shape_keys.key_blocks
		
		output_text = ""
		for key, key_block in key_blocks.items():
			key_val = float(key_block.value*100)
			if key_val > 0:
				output_text += key + " {0:g},".format(key_val)
		ob.data['blendset:' + target_name] = output_text
		
		msg = bpy.app.translations.pgettext('shapekey.RegistBlendset.Finished')
		self.report(type={'INFO'}, message=msg % target_name)
		return {'FINISHED'}

class add_blendset(bpy.types.Operator):
	bl_idname = 'shapekey.add_blendset'
	bl_label       = bpy.app.translations.pgettext('shapekey.AddBlendset')
	bl_description = bpy.app.translations.pgettext('shapekey.AddBlendset.Desc')
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		ob = context.active_object
		if ob and ob.type == 'MESH':
			bsl = context.window_manager.blendset_list
			if len(bsl.target_name) > 0 and not bsl.target_name in bsl.blendset_items:
				return True
		return False
	
	def execute(self, context):
		bsl = context.window_manager.blendset_list
		target_name = bsl.target_name
		
		ob = context.active_object
		key_blocks = ob.data.shape_keys.key_blocks
		
		output_text = ""
		for key, key_block in key_blocks.items():
			key_val = float(key_block.value*100)
			if key_val > 0:
				output_text += key + " {0:g},".format(key_val)
		ob.data['blendset:' + target_name] = output_text
		
		msg = bpy.app.translations.pgettext('shapekey.AddBlendset.Finished')
		self.report(type={'INFO'}, message=msg % target_name)
		return {'FINISHED'}

class del_blendset(bpy.types.Operator):
	bl_idname = 'shapekey.del_blendset'
	bl_label       = bpy.app.translations.pgettext('shapekey.DelBlendset')
	bl_description = bpy.app.translations.pgettext('shapekey.DelBlendset.Desc')
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, context):
		ob = context.active_object
		if ob and ob.type == 'MESH':
			bsl = context.window_manager.blendset_list
			if len(bsl.target_name) > 0 and bsl.target_name in bsl.blendset_items:
				return True
		return False
	
	def execute(self, context):
		bsl = context.window_manager.blendset_list
		target_name = bsl.target_name
		
		ob = context.active_object
		
		del ob.data['blendset:' + target_name]
		
		msg = bpy.app.translations.pgettext('shapekey.DelBlendset.Finished')
		self.report(type={'INFO'}, message=msg % target_name)
		return {'FINISHED'}

class paste_blendset(bpy.types.Operator):
	bl_idname = 'shapekey.paste_blendset'
	bl_label       = bpy.app.translations.pgettext('shapekey.PasteBlendset')
	bl_description = bpy.app.translations.pgettext('shapekey.PasteBlendset.Desc')
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, context):
		data = context.window_manager.clipboard
		if 'blendset' in data:
			return False
		lines = data.split('\n')
		if len(lines) < 2:
			return False
		
		return True
	
	def execute(self, context):
		data = context.window_manager.clipboard
		lines = data.split('\n')
		
		ob = context.active_object
		key_blocks = ob.data.shape_keys.key_blocks
		# reset
		for key_block in key_blocks.values():
			key_block.value = 0.0
		
		for line in lines:
			val = line.strip()
			if not val:
				key = None
				continue
			
			try:
				numval = float(val)
				key = key.lower()
				if key in key_blocks:
					key_blocks[key].value = numval/100
				else:
					msg = bpy.app.translations.pgettext('shapekey.KeyNotFound')
					self.report(type={'WARNING'}, message=msg % key)
			except:
				key = val
				continue
		msg = bpy.app.translations.pgettext('shapekey.PasteBlendset.Finished')
		self.report(type={'INFO'}, message=msg)
		return {'FINISHED'}

class copy_blendset(bpy.types.Operator):
	bl_idname = 'shapekey.copy_blendset'
	bl_label       = bpy.app.translations.pgettext('shapekey.CopyBlendsets')
	bl_description = bpy.app.translations.pgettext('shapekey.CopyBlendsets.Desc')
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, context):
		ob = context.active_object
		shape_keys = ob.data.shape_keys
		
		if shape_keys and len(shape_keys.key_blocks.items()) < 1:
			return False
		return True
	
	def execute(self, context):
		ob = context.active_object
		key_blocks = ob.data.shape_keys.key_blocks
		output_text = ""
		
		for key, key_block in key_blocks.items():
			key_val = float(key_block.value*100)
			if key_val > 0:
				output_text += "\t" + key + "\n\t{0:g}\n".format(key_val)
		
		context.window_manager.clipboard = output_text
		msg = bpy.app.translations.pgettext('shapekey.PasteBlendset.Finished')
		self.report(type={'INFO'}, message=msg)
		return {'FINISHED'}
	
class BlendsetItem(bpy.types.PropertyGroup):
	name = bpy.props.StringProperty()
	selected = bpy.props.BoolProperty()

class BlendsetList(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		layout.label(text=item.name, translate=False, icon='NONE' )

class Blendsets(bpy.types.PropertyGroup):
	blendset_items = bpy.props.CollectionProperty(type=BlendsetItem)
	item_idx       = bpy.props.IntProperty()
	prev_idx       = bpy.props.IntProperty()
	target_name    = bpy.props.StringProperty()
	display_list   = bpy.props.BoolProperty(name = "Blendset List",
		description = "Display Blendset List",
		default = False)

# -------------------------------------------------------------------
# register
# -------------------------------------------------------------------
def register():
	bpy.types.WindowManager.blendset_list = bpy.props.PointerProperty(type=Blendsets)

def unregister():
	del bpy.types.WindowManager.blendset_list
