import bpy, os, re

addon_name = "CM3D2 BoneUtil"

# データ名末尾の「.001」などを削除
def remove_serial_num(name):
	return re.sub(r'\.\d{3,}$', "", name)

