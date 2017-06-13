import bpy
from . import common

class CM3D2BoneUtilUpdater(bpy.types.Operator):
	bl_idname = 'script.trzr_update_cm3d2_boneutil'
	bl_label       = 'Update'
	bl_description = bpy.app.translations.pgettext('butl.updater.Desc')
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, context):
		hist = common.prefs().update_history
		if len(hist.updates) > 0:
			if hist.has_update():
				return True
		
		return False
	
	def execute(self, context):
		import os, sys, urllib, zipfile, subprocess, urllib.request
		from urllib.error import URLError, HTTPError
		
		hist = common.prefs().update_history
		version = hist.titles[0]
		
		zip_path = os.path.join(bpy.app.tempdir, "Blender-CM3D2-BoneUtil-master.zip")
		addon_path = os.path.dirname(__file__)
		
		url = hist.links[0][1]
		response = urllib.request.urlopen(url)
		zip_file = open(zip_path, "wb")
		zip_file.write(response.read())
		zip_file.close()
		
		zip_file = zipfile.ZipFile(zip_path, "r")
		for path in zip_file.namelist():
			if not os.path.basename(path):
				continue
			sub_dir = os.path.split( os.path.split(path)[0] )[1]
			if sub_dir == "CM3D2 BoneUtil":
				file = open(os.path.join(addon_path, os.path.basename(path)), 'wb')
				file.write(zip_file.read(path))
				file.close()
		zip_file.close()

		hist.now_ver = hist.latest_ver
		ver = '.'.join([ str(v) for v in hist.now_ver ])
		common.prefs().version = ver
		self.report(type={'INFO'}, message=bpy.app.translations.pgettext('butl.updater.Finished') % ver)
		try:
			bpy.ops.wm.addon_disable(module=__name__)
			bpy.ops.wm.addon_enable(module=__name__)
		except:
			pass
		# TODO reload scripts
		return {'FINISHED'}

class VersionHistory:
	updated_time = None
	vers = []
	titles = []
	updates = []
	links = []
	#last_ver_date = None
	now_ver = []
	latest_ver = []
	latest_version = ''
	
	def update(self, now):
		import json, datetime, urllib, urllib.request
		url = 'https://api.github.com/repos/trzr/Blender-CM3D2-BoneUtil/releases'
		res = urllib.request.urlopen(url)
		json_data = json.loads(res.read().decode('utf-8'))

		vers = []
		titles = []
		updates = []
		links = []

		for rel in json_data:
			if rel['prerelease']: continue
			ver = rel['tag_name']
			assets = rel['assets']
			body = rel['body'].split("\n", 1)[0].strip()
			if len(body) >= 64: body = body[0:63]
			title = ver + " " + body
			
			if len(assets) > 0 and 'browser_download_url' in assets[0]:
				dl_link = assets[0]['browser_download_url']
			else:
				dl_link = rel['zipball_url']
			link = (rel['html_url'], dl_link)
			update = rel['created_at']
			if len(update) < 19: continue
			
			updates.append( datetime.datetime.strptime(update[0:19], '%Y-%m-%dT%H:%M:%S') )
			vers.append(ver)
			titles.append(title)
			links.append(link)
		
		self.titles = titles
		self.vers   = vers
		self.updates = updates
		self.links = links
		self.updated_time = now
		if len(self.vers) > 0:
			self.latest_version = self.vers[0]
			try:
				self.latest_ver = [ int(v) for v in self.latest_version.split('.') ]
			except:
				pass
		
		if len(self.now_ver) == 0:
			ver = common.prefs().version
			self.now_ver = [ int(v) for v in ver.split('.') ]
	
	def has_update(self):
		if len(self.now_ver) == len(self.latest_ver):
			for now, latest in zip(self.now_ver, self.latest_ver):
				if now == latest: continue
				elif now < latest: return True
				else: return False
		return False

# 更新履歴メニュー
class INFO_MT_CM3D2_BoneUtil_history(bpy.types.Menu):
	bl_idname = 'INFO_MT_CM3D2_BoneUtil_history'
	bl_label = bpy.app.translations.pgettext('butl.updater.History')
	
	def draw(self, context):
		import datetime
		diff_seconds = 1000

		hist = common.prefs().update_history
		now = datetime.datetime.now()
		if hist.updated_time:
			diff_seconds = (now - hist.updated_time).seconds
		if diff_seconds > 600:
			try:
				hist.update(now)
			except TypeError:
				self.layout.label(text=bpy.app.translations.pgettext('butl.updater.History'), icon='ERROR')
				return

		utcnow = datetime.datetime.utcnow()
		count = 0
		for title, update, link in zip(hist.titles, hist.updates, hist.links):
			diff_seconds = utcnow - update
			icon = 'SORTTIME'
			if 7 < diff_seconds.days:
				icon = 'NLA'
			elif 3 < diff_seconds.days:
				icon = 'COLLAPSEMENU'
			elif 1 <= diff_seconds.days:
				icon = 'TIME'
			elif diff_seconds.days == 0 and 60 * 60 < diff_seconds.seconds:
				icon = 'RECOVER_LAST'
			elif diff_seconds.seconds <= 60 * 60:
				icon = 'PREVIEW_RANGE'
			
			if diff_seconds.days:
				date_str = bpy.app.translations.pgettext('butl.updater.HistoryDays') % diff_seconds.days
			elif 60 * 60 <= diff_seconds.seconds:
				date_str = bpy.app.translations.pgettext('butl.updater.HistoryHours') % int(diff_seconds.seconds / (60 * 60))
			elif 60 <= diff_seconds.seconds:
				date_str = bpy.app.translations.pgettext('butl.updater.HistoryMins') % int(diff_seconds.seconds / 60)
			else:
				date_str = bpy.app.translations.pgettext('butl.updater.HistorySecs') % diff_seconds.seconds
			
			text = "(" + date_str + ") " + title
			self.layout.operator('wm.url_open', text=text, icon=icon).url = link[0]
			count += 1

		self.layout.label(text=bpy.app.translations.pgettext('butl.updater.HistoryUpdated:') + hist.updated_time.strftime('%Y-%m-%d %H:%M:%S'))
