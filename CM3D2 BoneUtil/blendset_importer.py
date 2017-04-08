import os, sys, bpy, math, mathutils, struct, tempfile
from . import common

def menu_func(self, context):
	ob = context.active_object
	if not ob or ob.type != 'MESH': return
	if ob.data.shape_keys is None: return

	if not common.prefs().bsimp: return
	
	bsl = context.window_manager.blendset_list
	box = self.layout.box()
	col = box.column()
	split = col.split(percentage=0.14, align=True)
	if bsl.display_box:
		split.prop(bsl, 'display_box', text="", icon='TRIA_DOWN')
	else:
		split.prop(bsl, 'display_box', text="", icon='TRIA_RIGHT')
	split.label(text="shapekey.BatchOperation", icon='HAND')
	
	if not bsl.display_box: return
	
	col = box.column()
	sub_row1 = col.row(align=True)
	sub_row1.label(text='shapekey.menuif')
	label = bpy.app.translations.pgettext('Import')
	sub_row1.operator('shapekey.import_cm3d2_menu', icon='IMPORT', text=label)
	label = bpy.app.translations.pgettext('Export')
	sub_row1.operator('shapekey.export_cm3d2_menu', icon='EXPORT', text=label)
	
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
	refresh_list(self, context, bsl, ob.data)
	
	split = col.split(percentage=0.1, align=True)
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
						if len(entry) >= 2:
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
		
		msg = bpy.app.translations.pgettext('shapekey.ClearBlendsets.Finished')
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
		if ob is None: return False
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
		msg = bpy.app.translations.pgettext('shapekey.CopyBlendsets.Finished')
		self.report(type={'INFO'}, message=msg)
		return {'FINISHED'}
		
class import_cm3d2_menu(bpy.types.Operator):
	bl_idname = 'shapekey.import_cm3d2_menu'
	bl_label = 'import menu file'#bpy.app.translations.pgettext('shapekey.ImportMenufile')
	bl_description = bpy.app.translations.pgettext('shapekey.Menu.ImportfileDesc')
	bl_options = {'REGISTER', 'UNDO'}
	
	filepath = bpy.props.StringProperty(subtype='FILE_PATH')
	filename_ext = ".menu"
	filter_glob = bpy.props.StringProperty(default="*.menu", options={'HIDDEN'})
	
	@classmethod
	def poll(self, context):
		ob = context.active_object
		if ob and ob.type == 'MESH':
			return True
		return False
	
	def invoke(self, context, event):
		if common.prefs().menu_import_path:
			self.filepath = common.prefs().menu_import_path
		else:
			self.filepath = common.prefs().menu_default_path
		
		context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}
		
	def execute(self, context):
		common.prefs().menu_import_path = self.filepath
		
		ob = context.active_object
		props = ob.data
		
		try:
			file = open(self.filepath, 'rb')
		except:
			msg = bpy.app.translations.pgettext('shapekey.CannotOpenFile') % self.filepath
			self.report(type={'ERROR'}, message=msg)
			return {'CANCELLED'}
		
		if common.read_str(file) != 'CM3D2_MENU':
			msg = bpy.app.translations.pgettext('shapekey.Menu.InvalidFile') % self.filepath
			self.report(type={'ERROR'}, message=msg)
			return {'CANCELLED'}
		
		for prop_key in props.keys():
			if prop_key.startswith('blendset:'):
				del props[prop_key]
			# elif prop_key.startswith('cm3d2menu:'):
			# 	del props[prop_key]
		
		set_item_count = 0
		try:
			menu_ver = struct.unpack('<i', file.read(4))[0]
			menu_path = common.read_str(file)
			menu_name = common.read_str(file)
			menu_cate = common.read_str(file)
			menu_desc = common.read_str(file)
			# props['cm3d2menu:ver'] = mate_ver
			# props['cm3d2menu:path'] = mate_path
			# props['cm3d2menu:name'] = mate_name
			# props['cm3d2menu:cate'] = mate_cate
			# props['cm3d2menu:desc'] = mate_desc
			
			num = struct.unpack('<i', file.read(4))[0]
			vals = []
			length = struct.unpack('<B', file.read(1))[0]
			# include_blendset = False
			# idx = 0
			while (length > 0):
				vals.clear()
				key = common.read_str(file)
				
				for i in range(length-1):
					vals.append( common.read_str(file) )
				
				if key == 'blendset':
					if length >= 2:
						bs_name = vals[0]
						text = ""
						for i in range(1, length-2, 2):
							text += vals[i] + " " + vals[i+1] + ","
						
						props['blendset:' + bs_name] = text
						set_item_count += 1
						
						# if not include_blendset:
						# 	props['cm3d2menu:bspos'] + idx
						# 	include_blendset = True
				
				# else:
				# 	text = key + '\t'
				# 	for i in range(0, length-1):
				# 		text += vals[i] + "\t"
				# 	props['cm3d2menu:' + idx] = text
				# 	idx += 1
				chunk = file.read(1)
				if len(chunk) == 0: break
				length = struct.unpack('<B', chunk)[0]
				
			props['menu_path'] = self.filepath
		except:
			msg = bpy.app.translations.pgettext('shapekey.Menu.FailedToParsefile')
			self.report(type={'ERROR'}, message=msg)
			return {'CANCELLED'}
		finally:
			file.close()
			
		msg = bpy.app.translations.pgettext('shapekey.Menu.BlendsetsImport.Finished')
		self.report(type={'INFO'}, message=msg % set_item_count)
		return {'FINISHED'}

class export_cm3d2_menu(bpy.types.Operator):
	bl_idname = 'shapekey.export_cm3d2_menu'
	bl_label = "export to menu"
	bl_description = bpy.app.translations.pgettext('shapekey.Menu.ExportfileDesc')
	
	filepath = bpy.props.StringProperty(subtype='FILE_PATH')
	filename_ext = ".menu"
	filter_glob = bpy.props.StringProperty(default="*.menu", options={'HIDDEN'})
	
	is_backup = bpy.props.BoolProperty(name="shapekey.Menu.Backup", default=True, description="shapekey.Menu.BackupDesc")
	savefile  = bpy.props.StringProperty(name="shapekey.Menu.SaveFilename", default='', description="shapekey.Menu.SaveFilenameDesc")
	
	@classmethod
	def poll(self, context):
		ob = context.active_object
		if ob and ob.type == 'MESH':
			return True
		return False
	
	def invoke(self, context, event):
		ob = context.active_object
		props = ob.data
		self.filepath = ''
		if 'menu_path' in props:
			filepath = props['menu_path']
			if os.path.exists(filepath):
				self.filepath = filepath

		if self.filepath is None:
			if common.prefs().menu_export_path:
				self.filepath = common.prefs().menu_export_path
			else:
				self.filepath = common.prefs().menu_default_path
		
		context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}
	
	def draw(self, context):
		self.layout.prop(self, 'is_backup', icon='FILE_BACKUP')
		self.layout.prop(self, 'savefile', icon='NEW')
		self.layout.label(text="shapekey.Menu.Overwrite")#, icon='LAMP')
	
	def execute(self, context):
		common.prefs().menu_export_path = self.filepath

		filename = os.path.basename(self.filepath)
		outdir = os.path.dirname(self.filepath)
		
		ob = context.active_object
		try:
			infile = open(self.filepath, 'rb')
		except:
			msg = bpy.app.translations.pgettext('shapekey.CannotOpenFile') % self.filepath
			self.report(type={'ERROR'}, message=msg)
			return {'CANCELLED'}
		
		if common.read_str(infile) != 'CM3D2_MENU':
			msg = bpy.app.translations.pgettext('shapekey.Menu.InvalidFile') % self.filepath
			self.report(type={'ERROR'}, message=msg)
			return {'CANCELLED'}
		
		props = ob.data
		try:
			with tempfile.NamedTemporaryFile(mode='w+b', suffix='temp', prefix=filename, dir=outdir, delete=False) as outfile:
				tempfilepath = outfile.name
				menu_ver = struct.unpack('<i', infile.read(4))[0]
				menu_path = common.read_str(infile)
				menu_name = common.read_str(infile)
				menu_cate = common.read_str(infile)
				menu_desc = common.read_str(infile)

				common.write_str(outfile, 'CM3D2_MENU')
				outfile.write(struct.pack('<i', menu_ver))
				common.write_str(outfile, menu_path)
				common.write_str(outfile, menu_name)
				common.write_str(outfile, menu_cate)
				common.write_str(outfile, menu_desc)
				
				ba = bytearray()
				num = struct.unpack('<i', infile.read(4))[0]
				
				length = struct.unpack('<B', infile.read(1))[0]
				exported_blendset = False
				while (length > 0):
					
					key = common.read_str(infile)
					if key == 'blendset':
						for i in range(length-1):
							val = common.read_str(infile)

						if not exported_blendset:
							exported_blendset = True
							# export blendset
							self.export_blendset(ba, props.items())
							# read and discard
					else:
						#ba += struct.pack('<b', length)
						ba.append(length)
						common.append_str(ba, key)
						for i in range(length-1):
							val = common.read_str(infile)
							common.append_str(ba, val)
					
					chunk = infile.read(1)
					if len(chunk) == 0: break
					length = struct.unpack('<B', chunk)[0]
				
				if not exported_blendset:
					self.export_blendset(ba, props.items())

				ba.append(0) # EOFとして長さ0を挿入
				num = len(ba)
				outfile.write(struct.pack('<i', num))
				outfile.write(ba)
				
				props['menu_path'] = self.filepath
		except:
			msg = bpy.app.translations.pgettext('shapekey.Menu.FailedToParsefile.Export') % self.filepath
			self.report(type={'ERROR'}, message=msg)
			if tempfilepath:
				os.remove(tempfilepath)
			raise
			#return {'CANCELLED'}
		finally:
			if infile:	infile.close()
		
		# バックアップチェック
		if self.savefile:
			filename = self.savefile
			if not filename.endswith('.menu'):
				filename += '.menu'
			outfilepath = os.path.join(outdir, filename)
		else:
			outfilepath = self.filepath
		
		if self.is_backup and os.path.exists(outfilepath):
			bk_ext = common.prefs().backup_ext
			if bk_ext:
				bkfile = outfilepath + '.' + bk_ext
				if os.path.exists(bkfile):
					os.remove(bkfile)
				os.rename(outfilepath, bkfile)
		if os.path.exists(outfilepath):
			os.remove(outfilepath)
		os.rename(tempfilepath, outfilepath)
		
		msg = bpy.app.translations.pgettext('shapekey.Menu.BlendsetsExport.Finished') % self.filepath
		self.report(type={'INFO'}, message=msg)
		return {'FINISHED'}
	
	def export_blendset(self, ba, props):
		for propkey, propval in props:
			if propkey.startswith('blendset:'):
				pvalItems = propval.split(',')
				itemLength = len(pvalItems)*2 # 末尾にカンマがあるため+2は不要
				
				ba.append(itemLength) # bytearray( struct.pack('<i', itemLength) )
				common.append_str(ba, 'blendset')
				common.append_str(ba, propkey[9:])
				
				for val in pvalItems:
					if len(val) <= 2: continue
					entry = val.split(' ')
					if len(entry) >= 2:
						common.append_str(ba, entry[0])
						common.append_str(ba, entry[1])
	
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
	
	display_box   = bpy.props.BoolProperty(name = "display_box",
		description = "",
		default = False)

# -------------------------------------------------------------------
# register
# -------------------------------------------------------------------
def register():
	bpy.types.WindowManager.blendset_list = bpy.props.PointerProperty(type=Blendsets)

def unregister():
	del bpy.types.WindowManager.blendset_list
