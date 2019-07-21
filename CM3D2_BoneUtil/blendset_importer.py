# -*- coding: utf-8 -*-

import bpy
import os
import struct
import tempfile
from . import common
from . import compatibility as compat
from typing import List, Tuple, Dict, Optional, Iterator, Any


def menu_func(self, context: bpy.types.Context) -> None:
    ob = context.active_object
    if not ob or ob.type != 'MESH' or ob.data.shape_keys is None:
        return
    if not common.prefs().feature_importer:
        return

    bsl = context.scene.trzr_butl_blendsets
    box = self.layout.box()
    col = box.column()
    split = compat.layout_split(col, factor=0.14, align=True)
    if bsl.display_box:
        split.prop(bsl, 'display_box', text='', icon='TRIA_DOWN')
    else:
        split.prop(bsl, 'display_box', text='', icon='TRIA_RIGHT')
    split = compat.layout_split(split, factor=0.837, align=True)
    split.label(text="butl.shapekey.BatchOperation", icon='HAND')
    split.operator(BUTL_OT_BlendsetsUpdater.bl_idname, text='', icon='FILE_REFRESH')

    if not bsl.display_box:
        return

    col = box.column()
    sub_row1 = col.row(align=True)
    sub_row1.label(text='butl.shapekey.menuif')
    label = bpy.app.translations.pgettext('Import')
    sub_row1.operator(BUTL_OT_CM3D2MenuImporter.bl_idname, icon='IMPORT', text=label)
    label = bpy.app.translations.pgettext('Export')
    sub_row1.operator(BUTL_OT_CM3D2MenuExporter.bl_idname, icon='EXPORT', text=label)

    sub_row1 = col.row(align=True)
    sub_row1.label(text='butl.shapekey.BlendsetOpeation')
    label = bpy.app.translations.pgettext('butl.shapekey.CopySet')
    sub_row1.operator(BUTL_OT_BlendsetsCopier.bl_idname, icon='COPYDOWN', text=label)
    label = bpy.app.translations.pgettext('butl.shapekey.PasteSet')
    sub_row1.operator(BUTL_OT_BlendsetsPaster.bl_idname, icon='PASTEDOWN', text=label)
    label = bpy.app.translations.pgettext('butl.shapekey.ClearSet')
    sub_row1.operator(BUTL_OT_BlendsetsClearer.bl_idname, icon='X', text=label)

    # has_target = False
    # for prop_key in ob.data.keys():
    #     if prop_key.startswith('blendset:'):
    #         has_target = True
    #         break
    # if has_target:
    # refresh_list(context, bsl, ob.data)

    split = compat.layout_split(col, factor=0.1, align=True)
    if bsl.display_list:
        split.prop(bsl, "display_list", text="", icon='TRIA_DOWN')
    else:
        split.prop(bsl, "display_list", text="", icon='TRIA_RIGHT')

    sub_row = split.row()
    bs_count = len(bsl.blendset_items)
    sub_row.label(text="butl.shapekey.BlendsetList", icon='SHAPEKEY_DATA')
    subsub_row = sub_row.row()
    subsub_row.alignment = 'RIGHT'
    subsub_row.label(text=str(bs_count), icon='CHECKBOX_HLT')

    if bsl.display_list:
        row = col.row(align=True)
        col1 = row.column(align=True)
        col1.template_list("BUTL_UL_BlendsetList", "", bsl, "blendset_items", bsl, "item_idx", rows=2)

        if bsl.item_idx != bsl.prev_idx:
            if 0 <= bsl.item_idx < bs_count:
                bsl.target_name = bsl.blendset_items[bsl.item_idx].name
            else:
                bsl.target_name = ""
            bsl.prev_idx = bsl.item_idx

        row1 = col.row(align=True)
        split1 = compat.layout_split(row1, factor=0.6, align=True)
        split1.prop(bsl, "target_name", text="")
        label = bpy.app.translations.pgettext('butl.shapekey.Reflect')
        split1.operator(BUTL_OT_BlendsetReflector.bl_idname, icon='TRIA_DOWN', text=label)
        label = bpy.app.translations.pgettext('butl.shapekey.Regist')
        split1.operator(BUTL_OT_BlendsetRegister.bl_idname, icon='TRIA_UP', text=label)

        subsplit = compat.layout_split(split1, factor=0.5, align=True)
        subsplit.operator(BUTL_OT_BlendsetAdder.bl_idname, icon=compat.icon('ADD'), text='')
        subsplit.operator(BUTL_OT_BlendsetDeleter.bl_idname, icon=compat.icon('REMOVE'), text='')

    # bottom
    col = col.column()
    row = col.row(align=True)
    row.label(text='butl.shapekey.ShapeKeyVal')
    label = bpy.app.translations.pgettext('butl.shapekey.CopyValue')
    row.operator(BUTL_OT_BlendsetCopier.bl_idname, icon='COPYDOWN', text=label)
    label = bpy.app.translations.pgettext('butl.shapekey.PasteValue')
    row.operator(BUTL_OT_BlendsetPaster.bl_idname, icon='PASTEDOWN', text=label)


@compat.BlRegister(use_bl_attr=False)
class BlendsetItem(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty()
    selected = bpy.props.BoolProperty()


@compat.BlRegister(use_bl_attr=False)
class BUTL_UL_BlendsetList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=item.name, translate=False, icon='NONE')


@compat.BlRegister(use_bl_attr=False)
class Blendsets(bpy.types.PropertyGroup):
    blendset_items = bpy.props.CollectionProperty(type=BlendsetItem)
    item_idx = bpy.props.IntProperty()
    prev_idx = bpy.props.IntProperty()
    target_name = bpy.props.StringProperty()
    display_list = bpy.props.BoolProperty(
        name="Blendset List",
        description="Display Blendset List",
        default=False)

    display_box = bpy.props.BoolProperty(
        name="display_box",
        description="",
        default=False)

# ========== Operator =====================================


@compat.BlRegister()
class BUTL_OT_BlendsetsUpdater(bpy.types.Operator):
    bl_idname = 'shapekey.trzr_update_blendsets'
    bl_label = "Refresh blendset list"

    def execute(self, context: bpy.types.Context) -> set:
        BUTL_OT_BlendsetsUpdater.refresh_list(context)
        return {'FINISHED'}

    @classmethod
    def refresh_list(cls, context: bpy.types.Context) -> None:
        bs_list = context.scene.trzr_butl_blendsets
        target_props = context.active_object.data

        bs_list.blendset_items.clear()
        for propkey in target_props.keys():
            if propkey.startswith('blendset:'):
                item = bs_list.blendset_items.add()
                item.name = propkey[9:]


@compat.BlRegister()
class BUTL_OT_BlendsetsPaster(bpy.types.Operator):
    bl_idname = 'shapekey.trzr_paste_blendsets'
    bl_label = bpy.app.translations.pgettext('butl.shapekey.PasteBlendsets')
    bl_description = bpy.app.translations.pgettext('butl.shapekey.PasteBlendsets.Desc')
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        ob = context.active_object
        if ob and ob.type == 'MESH':
            clipboard = context.window_manager.clipboard
            if 'blendset' in clipboard:
                return True
        return False

    def execute(self, context: bpy.types.Context) -> set:
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
        kv_list = []  # type: List[Tuple[str, str]]
        bs_name = ''
        while idx + 1 < line_len:
            key = lines[idx].strip()
            if key == 'blendset':
                on_blendset = True
                bs_name = lines[idx + 1].strip()
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
                    val = lines[idx + 1].strip()
                    try:
                        float(val)
                        kv_list.append((key, val))
                    except:
                        msg = bpy.app.translations.pgettext('butl.shapekey.ParseFailed')
                        self.report(type={'WARNING'}, message=msg % val)
                        continue
                    idx += 2
            else:
                idx += 1

        if len(kv_list) > 0:
            text = ''
            for kv in kv_list:
                text += kv[0] + " " + kv[1] + ","
            props['blendset:' + bs_name] = text
            set_item_count += 1
            kv_list.clear()
        msg = bpy.app.translations.pgettext('butl.shapekey.PasteBlendsets.Finished')
        self.report(type={'INFO'}, message=msg % set_item_count)

        BUTL_OT_BlendsetsUpdater.refresh_list(context)
        return {'FINISHED'}


@compat.BlRegister()
class BUTL_OT_BlendsetsCopier(bpy.types.Operator):
    bl_idname = 'shapekey.trzr_copy_blendsets'
    bl_label = bpy.app.translations.pgettext('butl.shapekey.CopyBlendsets')
    bl_description = bpy.app.translations.pgettext('butl.shapekey.CopyBlendsets.Desc')
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        ob = context.active_object
        if ob and ob.type == 'MESH':
            for prop_key in ob.data.keys():
                if prop_key.startswith('blendset:'):
                    return True
        return False

    def execute(self, context: bpy.types.Context) -> set:
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
        msg = bpy.app.translations.pgettext('butl.shapekey.CopyBlendsets.Finished')
        self.report(type={'INFO'}, message=msg)
        return {'FINISHED'}


@compat.BlRegister()
class BUTL_OT_BlendsetsClearer(bpy.types.Operator):
    bl_idname = 'shapekey.trzr_clear_blendsets'
    bl_label = bpy.app.translations.pgettext('butl.shapekey.ClearBlendsets')
    bl_description = bpy.app.translations.pgettext('butl.shapekey.ClearBlendsets.Desc')
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        ob = context.active_object
        if ob and ob.type == 'MESH':
            for prop_key in ob.data.keys():
                if prop_key.startswith('blendset:'):
                    return True
        return False

    def execute(self, context: bpy.types.Context) -> set:
        ob = context.active_object
        props = ob.data

        for prop_key in props.keys():
            if prop_key.startswith('blendset:'):
                del props[prop_key]

        msg = bpy.app.translations.pgettext('butl.shapekey.ClearBlendsets.Finished')
        self.report(type={'INFO'}, message=msg)

        bs_list = context.scene.trzr_butl_blendsets
        bs_list.blendset_items.clear()
        return {'FINISHED'}


@compat.BlRegister()
class BUTL_OT_BlendsetReflector(bpy.types.Operator):
    bl_idname = 'shapekey.trzr_reflect_blendset'
    bl_label = bpy.app.translations.pgettext('butl.shapekey.ReflectBlendset')
    bl_description = bpy.app.translations.pgettext('butl.shapekey.ReflectBlendset.Desc')
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        ob = context.active_object
        if ob and ob.type == 'MESH':
            bsl = context.scene.trzr_butl_blendsets
            if bsl.target_name in bsl.blendset_items:
                return True
        return False

    def execute(self, context: bpy.types.Context) -> set:
        bsl = context.scene.trzr_butl_blendsets
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
                    key = entry[0]
                    numval = float(entry[1])
                    if key in key_blocks:
                        key_blocks[key].value = numval / 100
                    else:
                        key_l = key.lower()
                        if key != key_l and key_l in key_blocks:
                            key_blocks[key_l].value = numval / 100
                        else:
                            msg = bpy.app.translations.pgettext('butl.shapekey.KeyNotFound')
                            self.report(type={'WARNING'}, message=msg % key)
                except:
                    continue

        msg = bpy.app.translations.pgettext('butl.shapekey.ReflectBlendset.Finished')
        self.report(type={'INFO'}, message=msg % target_name)
        return {'FINISHED'}


@compat.BlRegister()
class BUTL_OT_BlendsetRegister(bpy.types.Operator):
    bl_idname = 'shapekey.trzr_regist_blendset'
    bl_label = bpy.app.translations.pgettext('butl.shapekey.RegistBlendset')
    bl_description = bpy.app.translations.pgettext('butl.shapekey.RegistBlendset.Desc')
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        ob = context.active_object
        if ob and ob.type == 'MESH':
            bsl = context.scene.trzr_butl_blendsets
            if bsl.target_name in bsl.blendset_items:
                return True
        return False

    def execute(self, context: bpy.types.Context) -> set:
        bsl = context.scene.trzr_butl_blendsets
        target_name = bsl.target_name

        ob = context.active_object
        key_blocks = ob.data.shape_keys.key_blocks

        output_text = ""
        for key, key_block in key_blocks.items():
            key_val = float(key_block.value * 100)
            if key_val > 0:
                output_text += key + " {0:g},".format(key_val)
        ob.data['blendset:' + target_name] = output_text

        msg = bpy.app.translations.pgettext('butl.shapekey.RegistBlendset.Finished')
        self.report(type={'INFO'}, message=msg % target_name)

        BUTL_OT_BlendsetsUpdater.refresh_list(context)
        return {'FINISHED'}


@compat.BlRegister()
class BUTL_OT_BlendsetAdder(bpy.types.Operator):
    bl_idname = 'shapekey.trzr_add_blendset'
    bl_label = bpy.app.translations.pgettext('butl.shapekey.AddBlendset')
    bl_description = bpy.app.translations.pgettext('butl.shapekey.AddBlendset.Desc')
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        ob = context.active_object
        if ob and ob.type == 'MESH':
            bsl = context.scene.trzr_butl_blendsets
            if len(bsl.target_name) > 0 and bsl.target_name not in bsl.blendset_items:
                return True
        return False

    def execute(self, context: bpy.types.Context) -> set:
        bsl = context.scene.trzr_butl_blendsets
        target_name = bsl.target_name

        ob = context.active_object
        key_blocks = ob.data.shape_keys.key_blocks

        output_text = ""
        for key, key_block in key_blocks.items():
            key_val = float(key_block.value * 100)
            if key_val > 0:
                output_text += key + " {0:g},".format(key_val)
        ob.data['blendset:' + target_name] = output_text

        msg = bpy.app.translations.pgettext('butl.shapekey.AddBlendset.Finished')
        self.report(type={'INFO'}, message=msg % target_name)

        BUTL_OT_BlendsetsUpdater.refresh_list(context)
        return {'FINISHED'}


@compat.BlRegister()
class BUTL_OT_BlendsetDeleter(bpy.types.Operator):
    bl_idname = 'shapekey.trzr_del_blendset'
    bl_label = bpy.app.translations.pgettext('butl.shapekey.DelBlendset')
    bl_description = bpy.app.translations.pgettext('butl.shapekey.DelBlendset.Desc')
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        ob = context.active_object
        if ob and ob.type == 'MESH':
            bsl = context.scene.trzr_butl_blendsets
            if len(bsl.target_name) > 0 and bsl.target_name in bsl.blendset_items:
                return True
        return False

    def execute(self, context: bpy.types.Context) -> set:
        bsl = context.scene.trzr_butl_blendsets
        target_name = bsl.target_name

        ob = context.active_object
        del ob.data['blendset:' + target_name]

        msg = bpy.app.translations.pgettext('butl.shapekey.DelBlendset.Finished') % target_name
        self.report(type={'INFO'}, message=msg)

        BUTL_OT_BlendsetsUpdater.refresh_list(context)
        return {'FINISHED'}


@compat.BlRegister()
class BUTL_OT_BlendsetPaster(bpy.types.Operator):
    bl_idname = 'shapekey.trzr_paste_blendset'
    bl_label = bpy.app.translations.pgettext('butl.shapekey.PasteBlendset')
    bl_description = bpy.app.translations.pgettext('butl.shapekey.PasteBlendset.Desc')
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        data = context.window_manager.clipboard
        if 'blendset' in data:
            return False
        lines = data.split('\n')
        if len(lines) < 2:
            return False

        return True

    def execute(self, context: bpy.types.Context) -> set:
        data = context.window_manager.clipboard
        lines = data.split('\n')

        ob = context.active_object
        key_blocks = ob.data.shape_keys.key_blocks
        # reset
        for key_block in key_blocks.values():
            key_block.value = 0.0

        key = None  # type: Optional[str]
        for line in lines:
            val = line.strip()
            if val is None:
                continue

            if key is None:
                key = val
                continue

            try:
                numval = float(val)
                if key in key_blocks:
                    key_blocks[key].value = numval / 100
                else:
                    key_l = key.lower()
                    if key != key_l and key_l in key_blocks:
                        key_blocks[key_l].value = numval / 100
                    else:
                        msg = bpy.app.translations.pgettext('butl.shapekey.KeyNotFound')
                        self.report(type={'WARNING'}, message=msg % key)
                key = None
            except:
                pass

        msg = bpy.app.translations.pgettext('butl.shapekey.PasteBlendset.Finished')
        self.report(type={'INFO'}, message=msg)
        return {'FINISHED'}


@compat.BlRegister()
class BUTL_OT_BlendsetCopier(bpy.types.Operator):
    bl_idname = 'shapekey.trzr_copy_blendset'
    bl_label = bpy.app.translations.pgettext('butl.shapekey.CopyBlendsets')
    bl_description = bpy.app.translations.pgettext('butl.shapekey.CopyBlendsets.Desc')
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        ob = context.active_object
        if ob is None:
            return False
        shape_keys = ob.data.shape_keys

        if shape_keys and len(shape_keys.key_blocks.items()) < 1:
            return False
        return True

    def execute(self, context: bpy.types.Context) -> set:
        ob = context.active_object
        key_blocks = ob.data.shape_keys.key_blocks
        output_text = ""

        for key, key_block in key_blocks.items():
            key_val = float(key_block.value * 100)
            if key_val > 0:
                output_text += "\t" + key + "\n\t{0:g}\n".format(key_val)

        context.window_manager.clipboard = output_text
        msg = bpy.app.translations.pgettext('butl.shapekey.CopyBlendsets.Finished')
        self.report(type={'INFO'}, message=msg)
        return {'FINISHED'}


@compat.BlRegister()
class BUTL_OT_CM3D2MenuImporter(bpy.types.Operator):
    bl_idname = 'shapekey.trzr_import_cm3d2_menu'
    bl_label = 'import menu file'
    bl_description = bpy.app.translations.pgettext('butl.shapekey.Menu.ImportfileDesc')
    bl_options = {'REGISTER', 'UNDO'}

    filepath = bpy.props.StringProperty(subtype='FILE_PATH')
    filename_ext = '.menu'
    filter_glob = bpy.props.StringProperty(default='*.menu', options={'HIDDEN'})

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        ob = context.active_object
        if ob and ob.type == 'MESH':
            return True
        return False

    def invoke(self, context, event):  # type: (bpy.types.Context, Any) -> set
        prefs = common.prefs()
        if prefs.menu_import_path:
            self.filepath = prefs.menu_import_path
        else:
            self.filepath = prefs.menu_default_path

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context: bpy.types.Context) -> set:
        common.prefs().menu_import_path = self.filepath

        ob = context.active_object
        props = ob.data

        try:
            file = open(self.filepath, 'rb')
        except:
            msg = bpy.app.translations.pgettext('butl.shapekey.CannotOpenFile') % self.filepath
            self.report(type={'ERROR'}, message=msg)
            return {'CANCELLED'}

        if common.read_str(file) != 'CM3D2_MENU':
            msg = bpy.app.translations.pgettext('butl.shapekey.Menu.InvalidFile') % self.filepath
            self.report(type={'ERROR'}, message=msg)
            return {'CANCELLED'}

        for prop_key in props.keys():
            if prop_key.startswith('blendset:'):
                del props[prop_key]
            # elif prop_key.startswith('cm3d2menu:'):
            #     del props[prop_key]

        set_item_count = 0
        try:
            # menu_ver =
            struct.unpack('<i', file.read(4))[0]
            # menu_path =
            common.read_str(file)
            # menu_name =
            common.read_str(file)
            # menu_cate =
            common.read_str(file)
            # menu_desc
            common.read_str(file)
            # props['cm3d2menu:ver'] = mate_ver
            # props['cm3d2menu:path'] = mate_path
            # props['cm3d2menu:name'] = mate_name
            # props['cm3d2menu:cate'] = mate_cate
            # props['cm3d2menu:desc'] = mate_desc

            # num
            struct.unpack('<i', file.read(4))[0]
            vals = []  # type: List[str]
            length = struct.unpack('<B', file.read(1))[0]
            # include_blendset = False
            # idx = 0
            while length > 0:
                vals.clear()
                key = common.read_str(file)

                for i in range(length - 1):
                    vals.append(common.read_str(file))

                if key == 'blendset':
                    if length >= 2:
                        bs_name = vals[0]
                        text = ""
                        for i in range(1, length - 2, 2):
                            text += vals[i] + " " + vals[i + 1] + ","

                        props['blendset:' + bs_name] = text
                        set_item_count += 1

                        # if not include_blendset:
                        #     props['cm3d2menu:bspos'] + idx
                        #     include_blendset = True

                # else:
                #     text = key + '\t'
                #     for i in range(0, length-1):
                #         text += vals[i] + "\t"
                #     props['cm3d2menu:' + idx] = text
                #     idx += 1
                chunk = file.read(1)
                if len(chunk) == 0:
                    break
                length = struct.unpack('<B', chunk)[0]

            props['menu_path'] = self.filepath
        except:
            msg = bpy.app.translations.pgettext('butl.shapekey.Menu.FailedToParsefile')
            self.report(type={'ERROR'}, message=msg)
            return {'CANCELLED'}
        finally:
            file.close()

        msg = bpy.app.translations.pgettext('butl.shapekey.Menu.BlendsetsImport.Finished')
        self.report(type={'INFO'}, message=msg % set_item_count)

        BUTL_OT_BlendsetsUpdater.refresh_list(context)
        return {'FINISHED'}


@compat.BlRegister()
class BUTL_OT_CM3D2MenuExporter(bpy.types.Operator):
    bl_idname = 'shapekey.trzr_export_cm3d2_menu'
    bl_label = "export to menu"
    bl_description = bpy.app.translations.pgettext('butl.shapekey.Menu.ExportfileDesc')

    filepath = bpy.props.StringProperty(subtype='FILE_PATH')
    filter_glob = bpy.props.StringProperty(default="*.menu", options={'HIDDEN'})
    filename_ext = ".menu"

    is_backup = bpy.props.BoolProperty(name="butl.shapekey.Menu.Backup", default=True, description="butl.shapekey.Menu.BackupDesc")
    savefile = bpy.props.StringProperty(name="butl.shapekey.Menu.SaveFilename", default='', description="butl.shapekey.Menu.SaveFilenameDesc")

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        ob = context.active_object
        if ob and ob.type == 'MESH':
            return True
        return False

    def invoke(self, context, event):  # type: (bpy.types.Context, Any) -> set
        ob = context.active_object
        props = ob.data
        self.filepath = ''
        filepath = props.get('menu_path')
        if filepath and os.path.exists(filepath):
            self.filepath = filepath

        if self.filepath is None:
            prefs = common.prefs()
            if prefs.menu_export_path:
                self.filepath = prefs.menu_export_path
            else:
                self.filepath = prefs.menu_default_path

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context: bpy.types.Context) -> None:
        self.layout.prop(self, 'is_backup', icon='FILE_BACKUP')
        self.layout.prop(self, 'savefile', icon=compat.icon('FILE_NEW'))
        self.layout.label(text="butl.shapekey.Menu.Overwrite")  # , icon='LAMP')

    def execute(self, context: bpy.types.Context) -> set:
        common.prefs().menu_export_path = self.filepath

        filename = os.path.basename(self.filepath)
        outdir = os.path.dirname(self.filepath)

        ob = context.active_object
        try:
            infile = open(self.filepath, 'rb')
        except:
            msg = bpy.app.translations.pgettext('butl.shapekey.CannotOpenFile') % self.filepath
            self.report(type={'ERROR'}, message=msg)
            return {'CANCELLED'}

        if common.read_str(infile) != 'CM3D2_MENU':
            msg = bpy.app.translations.pgettext('butl.shapekey.Menu.InvalidFile') % self.filepath
            self.report(type={'ERROR'}, message=msg)
            return {'CANCELLED'}

        props = ob.data
        try:
            temp_filepath = None  # type: Optional[str]
            with tempfile.NamedTemporaryFile(mode='w+b', suffix='temp', prefix=filename, dir=outdir, delete=False) as outfile:
                temp_filepath = outfile.name
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
                while length > 0:
                    key = common.read_str(infile)
                    if key == 'blendset':
                        for i in range(length - 1):
                            common.read_str(infile)  # read skip

                        if not exported_blendset:
                            exported_blendset = True
                            # export blendset
                            self._export_blendset(ba, props.items())
                            # read and discard
                    else:
                        ba.append(length)
                        common.append_str(ba, key)
                        for i in range(length - 1):
                            val = common.read_str(infile)
                            common.append_str(ba, val)

                    chunk = infile.read(1)
                    if len(chunk) == 0:
                        break
                    length = struct.unpack('<B', chunk)[0]

                if not exported_blendset:
                    self._export_blendset(ba, props.items())

                ba.append(0)  # insert 0 for EOF
                num = len(ba)
                outfile.write(struct.pack('<i', num))
                outfile.write(ba)

                props['menu_path'] = self.filepath
        except:
            msg = bpy.app.translations.pgettext('butl.shapekey.Menu.FailedToParsefile.Export') % self.filepath
            self.report(type={'ERROR'}, message=msg)
            if temp_filepath:
                os.remove(temp_filepath)
            raise
            # return {'CANCELLED'}
        finally:
            if infile:
                infile.close()

        # check backup filename
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
        os.rename(temp_filepath, outfilepath)

        msg = bpy.app.translations.pgettext('butl.shapekey.Menu.BlendsetsExport.Finished') % outfilepath
        self.report(type={'INFO'}, message=msg)
        return {'FINISHED'}

    def _export_blendset(self, ba, props):  # type: (bytearray, Iterator[Tuple[str, str]]) -> None
        for propkey, propval in props:
            if propkey.startswith('blendset:'):
                pval_items = propval.split(',')
                item_length = len(pval_items) * 2  # no +2 (comma end)

                ba.append(item_length)  # bytearray( struct.pack('<i', item_length) )
                common.append_str(ba, 'blendset')
                common.append_str(ba, propkey[9:])

                for val in pval_items:
                    if len(val) <= 2:
                        continue
                    entry = val.split(' ')
                    if len(entry) >= 2:
                        common.append_str(ba, entry[0])
                        common.append_str(ba, entry[1])
