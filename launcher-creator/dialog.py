# -*- coding: utf-8 -*-
# "Nautilus Launcher Creator" 0.5
# Copyright (C) 2018 Romain F. T.

import os
import gi
import urllib

gi.require_version('Nautilus', '3.0')
from gi.repository import Gtk, GObject, Gio, GLib, GdkPixbuf

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
LOCALE_PATH = os.path.join(BASE_PATH, 'locale')
try:
	import gettext
	gettext.bindtextdomain('launcher-creator', LOCALE_PATH)
	_ = lambda s: gettext.dgettext('launcher-creator', s)
except:
	_ = lambda s: s	

APPS_DIRECTORY = os.path.join(os.getenv('HOME'), '.local/share/applications/')
HOME_DIRECTORY = os.path.join(os.getenv('HOME'), '')

class LauncherCreatorWindow():
	def __init__(self, launcher_type, execpath):
		builder = Gtk.Builder.new_from_file(os.path.join(BASE_PATH, 'dialog.ui'))
		self.dialog = builder.get_object('dialog')
		switcher = Gtk.StackSwitcher(stack=builder.get_object('main_stack'))
		self.dialog.get_titlebar().set_show_close_button(False)
		self.dialog.get_titlebar().set_custom_title(switcher)

	def run(self, *args):
		self.dialog.show_all()
		res = self.dialog.run()
		if res == 1:
			self.on_create()
		else:
			self.on_cancel()
		self.destroy()

	def on_create(self, *args):
		pass

	def on_cancel(self, *args):
		pass

	def destroy(self, *args):
		self.dialog.destroy()



