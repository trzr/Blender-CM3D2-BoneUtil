# -*- coding: utf-8 -*-

import bpy
import re
import struct
from typing import Any, Optional


# LEGAY: version less than 2.80
IS_LEGACY = not hasattr(bpy.app, 'version') or bpy.app.version < (2, 80)


class BlRegister:
    idnames = set()
    classes = []

    def __init__(self, *args, **kwargs):
        self.make_annotation = kwargs.get('make_annotation', True)
        self.use_bl_attr = kwargs.get('use_bl_attr', True)

    def __call__(self, cls):

        if hasattr(cls, 'bl_idname'):
            bl_idname = cls.bl_idname
        else:
            if self.use_bl_attr:
                bl_idname = "{}{}{}{}".format(cls.bl_space_type, cls.bl_region_type, cls.bl_context, cls.bl_label)
            else:
                bl_idname = cls.__qualname__

        BlRegister.add(bl_idname, cls)
        if self.make_annotation:
            cls = make_annotations(cls)
        return cls

    @classmethod
    def add(cls: type, bl_idname: str, op_class: type) -> None:
        if bl_idname in cls.idnames:
            raise RuntimeError("Duplicate bl_idname: %s" % bl_idname)

        cls.idnames.add(bl_idname)
        cls.classes.append(op_class)

    @classmethod
    def register(cls):
        for cls1 in cls.classes:
            bpy.utils.register_class(cls1)

    @classmethod
    def unregister(cls):
        for cls1 in reversed(cls.classes):
            bpy.utils.unregister_class(cls1)

    @classmethod
    def cleanup(cls):
        cls.classes.clear()
        cls.idnames.clear()


def make_annotations(cls):
    if IS_LEGACY:
        return cls

    cls_props = {}
    for k, v in cls.__dict__.items():
        if isinstance(v, tuple):
            cls_props[k] = v

    annos = cls.__dict__.get('__annotations__')  # type: dict[str, type]
    if annos is None:
        annos = {}
        setattr(cls, '__annotations__', annos)

    for k, v in cls_props.items():
        annos[k] = v
        delattr(cls, k)
    return cls


def layout_split(layout, factor=0.0, align=False):
    if IS_LEGACY:
        return layout.split(percentage=factor, align=align)

    return layout.split(factor=factor, align=align)

def get_active():
    if IS_LEGACY:
        return bpy.context.scene.objects.active
    else:
        return bpy.context.view_layer.objects.active

def set_active(obj):
    if IS_LEGACY:
        bpy.context.scene.objects.active = obj
    else:
        bpy.context.view_layer.objects.active = obj

def get_select(obj: bpy.types.Object) -> bool:
    if IS_LEGACY:
        return obj.select

    return obj.select_get()

def set_select(obj: bpy.types.Object, select: bool) -> None:
    if IS_LEGACY:
        obj.select = select
    else:
        obj.select_set(select)

def is_select(*args) -> bool:
    """すべてが選択状態であるかを判定する."""
    if IS_LEGACY:
        return all(arg.select for arg in args)

    return all(arg.select_get() for arg in args)
        # for arg in args:
        #     if not arg.select_get():
        #         return False
        # return True

def get_hide(obj: bpy.types.Object) -> bool:
    if IS_LEGACY:
        return obj.hide

    return obj.hide_viewport

def set_hide(obj: bpy.types.Object, hide: bool):
    if IS_LEGACY:
        obj.hide = hide

    else:
        obj.hide_viewport = hide

def mul(x, y):
    if IS_LEGACY:
        return x * y

    return x @ y

def mul3(x, y, z):
    if IS_LEGACY:
        return x * y * z

    return x @ y @ z

legacy_icons = {}
legacy_icons['ADD'] = 'ZOOMIN'
legacy_icons['REMOVE'] = 'ZOOMOUT'
legacy_icons['ARROW_LEFTRIGHT'] = 'MAN_SCALE'
legacy_icons['FILE_FOLDER'] = 'FILESEL'
legacy_icons['FILE_NEW'] = 'NEW'

def icon(key):
    if IS_LEGACY:
        # 対応アイコンがdictにない場合はNONEとする
        icon_name = legacy_icons.get(key)
        if icon_name is None:
            icon_name = 'NONE'
        return icon_name
    else:
        return key

def region_type():
    if IS_LEGACY:
        return 'TOOLS'
    return 'UI'

