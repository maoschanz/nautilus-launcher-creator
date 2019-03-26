# -*- coding: utf-8 -*-
# "Nautilus Launcher Creator" 0.5
# Copyright (C) 2018 Romain F. T.
#
# "Nautilus Launcher Creator" is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# "Nautilus Launcher Creator" is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with "Create .desktop file"; if not, see http://www.gnu.org/licenses
# for more information.

import os, gi, gettext, urllib
gi.require_version('Nautilus', '3.0')
from gi.repository import Nautilus, Gtk, GObject, Gio, GLib

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
LOCALE_PATH = os.path.join(BASE_PATH, 'locale')
try:
	import gettext
	gettext.bindtextdomain('launcher-creator', LOCALE_PATH)
	_ = lambda s: gettext.dgettext('launcher-creator', s)
except:
	_ = lambda s: s

from .dialog import LauncherCreatorWindow

class CreateLauncherMenu(GObject.GObject, Nautilus.MenuProvider):
	"""Create Launcher Menu"""
	def __init__(self):
		pass
	
	def get_file_items(self, window, items):
		"""Nautilus invoke this function in its startup > Then, create menu entry"""
		# Checks
		if not self._check_generate_menu(items):
			return
		# Return menu
		return self._generate_menu(items)
	
	def get_background_items(self, window, item):
		pass
	
	def _check_generate_menu(self, items):
		"""Show the menu?"""
		# No items selected
		if not len(items):
			return False
		
		for item in items:
			if item.is_directory():
				self.type = 'Link'
			elif GLib.file_test(item.get_name(), GLib.FileTest.IS_EXECUTABLE):
				self.type = 'Application'
			else:
				self.type = 'Link'
				
		for item in items: # XXX how useful ?
			if item.is_gone():
				continue
			self.execpath = urllib.unquote(item.get_uri()[7:])
		
		# All OK > Generate menu
		return True
	
	def _generate_menu(self, items):
		"""Generate menu"""
		top_menuitem = Nautilus.MenuItem(name='CreateALauncher', label=_("Create a launcher"), sensitive=True)
		top_menuitem.connect('activate', self.open_dialog)
		return top_menuitem,
	
	def open_dialog(self, btn):
		win = LauncherCreatorWindow(self.type, self.execpath)
		win.run()


