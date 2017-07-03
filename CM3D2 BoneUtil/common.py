# -*- coding: utf-8 -*-

import bpy  # type: ignore
import re
import struct
from typing import Any, Optional


addon_name = "CM3D2 BoneUtil"
pt_includeNum = re.compile('.*(0[1-9]|1[0-2]).*')


# このアドオンの設定値群を呼び出す
def prefs():  # type: () ->  bpy.types.AddonPreferences
	return bpy.context.user_preferences.addons[__name__.split('.')[0]].preferences


# データ名末尾の「.001」などを削除
def remove_serial_num(name):  # type: (str) -> str
	return re.sub(r'\.\d{3,}$', "", name)


def parse_bonetype(name):  # type: (str) -> Optional[str]
	if '_skirt_' in name:

		if pt_includeNum.match(remove_serial_num(name)):
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


def replace_bonename(name, source_type, target_type):  # type: (str, str, str)  -> str

	if source_type == 'soft' or source_type == 'hard':
		src_str = '_yure_' + source_type + '_'
		if target_type == 'soft':
			return name.replace(src_str, "_yure_soft_")
		if target_type == 'hard':
			return name.replace(src_str, "_yure_hard_")
		elif target_type == 'hair':
			return name.replace(src_str, "_yure_hair_")
		elif target_type == 'hair_h':
			return name.replace(src_str, "_yure_hair_h_")
		elif target_type == 'hair_h50':
			return name.replace(src_str, "_yure_hair_h50_")
		elif target_type == 'skirt':
			if pt_includeNum.match(name):
				return name.replace(src_str, "_yure_skirt_")
			else:
				return name.replace(src_str, "_01_yure_skirt_")
		elif target_type == 'skirt_h':
			if pt_includeNum.match(name):
				return name.replace(src_str, "_yure_skirt_h_")
			else:
				return name.replace(src_str, "_01_yure_skirt_h_")

	elif source_type == 'hair' or source_type == 'hair_h' or source_type == 'hair_h50':
		if source_type == 'hair_h':
			name = name.replace('_h_', "_")
		elif source_type == 'hair_h50':
			name = name.replace('_h50_', "_")

		src_str = '_yure_hair_'
		if target_type == 'soft' or target_type == 'hard' or target_type == 'hair' or target_type == 'hair_h' or target_type == 'hair_h50':
			replace_str = '_yure_' + target_type + '_'
			return re.sub(r'(_)?_yure_hair_(_)?', replace_str, name)
		elif target_type == 'skirt':
			if pt_includeNum.match(name):
				return re.sub(r'(_)?_yure_hair_(_)?', "_yure_skirt_", name)
			else:
				return re.sub(r'(_)?_yure_hair_(_)?', "_01_yure_skirt_", name)
		elif target_type == 'skirt_h':
			if pt_includeNum.match(name):
				return re.sub(r'(_)?_yure_hair_(_)?', "_yure_skirt_h_", name)
			else:
				return re.sub(r'(_)?_yure_hair_(_)?', "_01_yure_skirt_h_", name)

	elif source_type == 'skirt' or source_type == 'skirt_h':
		if source_type == 'skirt_h':
			name = name.replace('_h_', "_")
		name = re.sub(r'(_)?_skirt_(_)?', '_', name)

		replace_str = '_yure_' + target_type + '_'
		return re.sub(r'(_)?_yure_(_)?', replace_str, name)

	return name


###########################
# CM3D2Converterより引用
def read_str(file, total_b=""):  # type: (Any, str) -> str
	for i in range(9):
		b_str = format(struct.unpack('<B', file.read(1))[0], '08b')
		total_b = b_str[1:] + total_b
		if b_str[0] == '0':
			break
	return file.read(int(total_b, 2)).decode('utf-8', 'backslashreplace')
	# return file.read(int(total_b, 2)).decode('utf-8')


# CM3D2専用ファイル用の文字列書き込み
def write_str(file, raw_str):  # type: (Any, str) -> None
	b_str = format(len(raw_str.encode('utf-8')), 'b')
	for i in range(9):
		if 7 < len(b_str):
			file.write( struct.pack('<B', int("1" + b_str[-7:], 2)) )
			b_str = b_str[:-7]
		else:
			file.write( struct.pack('<B', int(b_str, 2)) )
			break
	file.write(raw_str.encode('utf-8'))


# bytearrayへの文字列追加
def append_str(barray, raw_str):  # type: (bytearray, str) -> None
	b_str = format(len(raw_str.encode('utf-8')), 'b')
	for i in range(9):
		if 7 < len(b_str):
			barray += bytearray( struct.pack('<B', int("1" + b_str[-7:], 2)) )
			b_str = b_str[:-7]
		else:
			barray += bytearray( struct.pack('<B', int(b_str, 2)) )
			break
	barray += raw_str.encode('utf-8')
