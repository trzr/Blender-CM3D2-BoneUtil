# -*- coding: utf-8 -*-

import bpy
import re
import struct
from . import compatibility as compat
from . import translations
from typing import Any, Optional

# pt_includeNum = re.compile('.*([01[1-9]|2[0-4]).*')


def get_preferences(context):  # type: (bpy.types.Context) -> bpy.types.Preferences
    if compat.IS_LEGACY:  # if hasattr(context, 'user_preferences'):
        return context.user_preferences

    return context.preferences


class PrefsHolder:
    prefs = None


# このアドオンの設定値群を呼び出す
def prefs():  # -> BUTL_AddonPreferences:
    if PrefsHolder.prefs is None:
        PrefsHolder.prefs = get_preferences(bpy.context).addons[__package__].preferences

    return PrefsHolder.prefs


class TransManager:
    registered = False

    @classmethod
    def trans_text(cls, key):
        if not cls.registered:
            cls.register()

        return bpy.app.translations.pgettext(key)

    @classmethod
    def register(cls):
        bpy.app.translations.unregister(__package__)
        bpy.app.translations.register(__package__, translations.get_dic())
        cls.registered = True

    @classmethod
    def unregister(cls):
        if cls.registered:
            bpy.app.translations.unregister(__package__)
            cls.registered = False


def trans_text(key):
    return TransManager.trans_text(key)


# データ名末尾の「.001」などを削除
def remove_serial_num(name: str) -> str:
    return re.sub(r'\.\d{3,}$', '', name)


def parse_bonetype(name: str) -> Optional[str]:
    if '_skirt_' in name:

        if '_h_' in name:
            return 'skirt_h'
        else:
            return 'skirt'
    elif '_yure_hair_' in name:
        if '_h_' in name:
            return 'hair_h'
        elif '_h50_' in name:
            return 'hair_h50'
        else:
            return 'hair'
    elif '_yure_soft_' in name:
        return 'soft'
    elif '_yure_hard_' in name:
        return 'hard'
    return None


def replace_bonename(name: str, source_type: str, target_type: str) -> str:

    if source_type == 'soft' or source_type == 'hard':
        src_str = '_yure_' + source_type + '_'
        if target_type == 'soft':
            return name.replace(src_str, '_yure_soft_')
        if target_type == 'hard':
            return name.replace(src_str, '_yure_hard_')
        elif target_type == 'hair':
            return name.replace(src_str, '_yure_hair_')
        elif target_type == 'hair_h':
            return name.replace(src_str, '_yure_hair_h_')
        elif target_type == 'hair_h50':
            return name.replace(src_str, '_yure_hair_h50_')
        elif target_type == 'skirt':
            return name.replace(src_str, '_yure_skirt_')
        elif target_type == 'skirt_h':
            return name.replace(src_str, '_yure_skirt_h_')

    elif source_type == 'hair' or source_type == 'hair_h' or source_type == 'hair_h50':
        if source_type == 'hair_h':
            name = name.replace('_h_', '_')
        elif source_type == 'hair_h50':
            name = name.replace('_h50_', '_')

        src_str = '_yure_hair_'
        if target_type == 'soft' or target_type == 'hard' or target_type == 'hair' or target_type == 'hair_h' or target_type == 'hair_h50':
            replace_str = '_yure_' + target_type + '_'
            return re.sub(r'(_)?_yure_hair_(_)?', replace_str, name)
        elif target_type == 'skirt':
            return re.sub(r'(_)?_yure_hair_(_)?', '_yure_skirt_', name)
        elif target_type == 'skirt_h':
            return re.sub(r'(_)?_yure_hair_(_)?', '_yure_skirt_h_', name)

    elif source_type == 'skirt' or source_type == 'skirt_h':
        if source_type == 'skirt_h':
            name = name.replace('_h_', '_')
        name = re.sub(r'(_)?_skirt_(_)?', '_', name)

        replace_str = '_yure_' + target_type + '_'
        return re.sub(r'(_)?_yure_(_)?', replace_str, name)

    return name


###########################
# CM3D2Converterを参考に
def read_str(file, total_b: str='') -> str:
    for i in range(9):
        b_str = format(struct.unpack('<B', file.read(1))[0], '08b')
        total_b = b_str[1:] + total_b
        if b_str[0] == '0':
            break

    return file.read(int(total_b, 2)).decode('utf-8', 'backslashreplace')
    # return file.read(int(total_b, 2)).decode('utf-8')


# CM3D2専用ファイル用の文字列書き込み
def write_str(file, raw_str: str) -> None:
    b_str = format(len(raw_str.encode('utf-8')), 'b')
    for i in range(9):
        if 7 < len(b_str):
            file.write(struct.pack('<B', int('1' + b_str[-7:], 2)))
            b_str = b_str[:-7]
        else:
            file.write(struct.pack('<B', int(b_str, 2)))
            break

    file.write(raw_str.encode('utf-8'))


# bytearrayへの文字列追加
def append_str(barray: bytearray, raw_str: str) -> None:
    b_str = format(len(raw_str.encode('utf-8')), 'b')
    for i in range(9):
        if 7 < len(b_str):
            barray += bytearray(struct.pack('<B', int('1' + b_str[-7:], 2)))
            b_str = b_str[:-7]
        else:
            barray += bytearray(struct.pack('<B', int(b_str, 2)))
            break
    barray += raw_str.encode('utf-8')

