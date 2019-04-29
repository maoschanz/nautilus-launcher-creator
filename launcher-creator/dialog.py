#!/usr/bin/env python3

# "Nautilus Launcher Creator" 0.x
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
		self.launcher_type = launcher_type
		self.launcher_path = ''
		self.execpath = execpath
		self.name = ''
		self.description = ''
		self.icon_string = ''
		self.categories = []
		self.keywords = []

		builder = Gtk.Builder.new_from_file(os.path.join(BASE_PATH, 'dialog.ui'))
		self.dialog = builder.get_object('dialog')
		switcher = Gtk.StackSwitcher(stack=builder.get_object('main_stack'))
		self.dialog.get_titlebar().set_show_close_button(False)
		self.dialog.get_titlebar().set_custom_title(switcher)
		
		self.name_entry = builder.get_object('name_entry')
		self.description_entry = builder.get_object('description_entry')

		self.type_btn_app = builder.get_object('type_btn1')
		self.type_btn_link = builder.get_object('type_btn2')

		self.target_entry = builder.get_object('target_entry')
		self.target_entry.set_text(self.execpath)
		self.target_entry.set_size_request(400, 10)

		self.path_entry = builder.get_object('path_entry')
		path_btn = builder.get_object('path_btn')
		path_btn.connect('clicked', self.open_path_chooser)
		
		basename = self.execpath.split('/')[-1]
		if self.launcher_type == 'Application':
			self.type_btn_app.set_active(True)
			filename = APPS_DIRECTORY + GLib.str_to_ascii(basename).replace(' ', '') + ".desktop"
		elif self.launcher_type == 'Link':
			self.type_btn_link.set_active(True)
			filename = HOME_DIRECTORY + GLib.str_to_ascii(basename).replace(' ', '') + ".desktop"
		self.path_entry.set_text(filename)

		self.icon_image = builder.get_object('icon_image')
		builder.get_object('icon_btn_theme').connect('clicked', self.on_icon_from_theme)
		builder.get_object('icon_btn_custom').connect('clicked', self.on_icon_custom)

#		self.name_entry.connect('notify::text', self.check_1st_page_completion)
#		self.path_entry.connect('notify::text', self.check_1st_page_completion)
#		self.fn_entry.connect('notify::text', self.check_1st_page_completion)

		keywords_list = EditableList()
		kw_frame = builder.get_object('keywords_frame')
		kw_frame.add(keywords_list.get_widget())

		categories_list = EditableList()
		categories_frame = builder.get_object('categories_frame')
		categories_frame.add(categories_list.get_widget())

		types_list = EditableList()
		types_frame = builder.get_object('types_frame')
		types_frame.add(types_list.get_widget())
		
		
		

	def run(self, *args):
		self.dialog.show_all()
		res = self.dialog.run()
		if res == 1:
			self.on_create()
		else:
			self.on_cancel()
		self.destroy()

	def on_create(self, *args): # TODO
#		self.launcher_path_entry.set_text(self.launcher_path)
#		text = '[Desktop Entry]\nName=' + self.name
#		text += '\nType=' + self.launcher_type
#		if self.launcher_type == 'Application':
#			text += '\nExec=' + self.execpath
#		else:
#			text += '\nURL=file://' + urllib.pathname2url(self.execpath)
#		if self.description != '':
#			text += '\nComment=' + self.description
#		if self.icon_string != '':
#			text += '\nIcon=' + self.icon_string
#		if self.categories != []:
#			text += '\nCategories=' + ';'.join(self.categories) + ';'
#		if self.keywords != []:
#			text += '\nKeywords=' + ';'.join(self.keywords) + ';'
#		self.textview.get_buffer().set_text(text)
		pass

	def on_cancel(self, *args):
		pass

	def destroy(self, *args):
		self.dialog.destroy()

	def open_path_chooser(self, *args):
		file_chooser = Gtk.FileChooserDialog(_("Launcher path"), self.dialog,
			Gtk.FileChooserAction.SAVE,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
		response = file_chooser.run()
		if response == Gtk.ResponseType.OK:
			self.path_entry.set_text(file_chooser.get_filename())
		file_chooser.destroy()

	def on_icon_from_theme(self, btn):
		settings = Gtk.Settings.get_default()
		theme_name = settings.get_property('gtk-icon-theme-name')
		SYSTEM_PATH = '/usr/share/icons'
		USER_PATH = os.path.join(os.getenv('HOME'), '.local/share/icons')
		user_path = os.path.join(SYSTEM_PATH, theme_name)
		system_path = os.path.join(USER_PATH, theme_name)
		
		if os.path.exists(user_path):
			path = user_path
		elif os.path.exists(system_path):
			path = system_path
		else:
			return
		
		# Building a FileChooserDialog for pictures
		file_chooser = Gtk.FileChooserDialog(_("Select an icon"), self.dialog,
			Gtk.FileChooserAction.OPEN,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		onlyPictures = Gtk.FileFilter()
		onlyPictures.set_name(_("Pictures"))
		onlyPictures.add_mime_type('image/*')
		file_chooser.set_filter(onlyPictures)
		file_chooser.set_current_folder(path)
		response = file_chooser.run()
		
		# It gets the chosen file's path
		if response == Gtk.ResponseType.OK:
			self.icon_string = ''.join(file_chooser.get_filename().split('/')[-1:]).replace('.svg', '')
			self.icon_string = ''.join(self.icon_string.split('/')[-1:]).replace('.png', '')
			self.icon_image.set_from_icon_name(self.icon_string, Gtk.IconSize.DIALOG)
		file_chooser.destroy()

	def on_icon_custom(self, *args):
		# Building a FileChooserDialog for pictures
		file_chooser = Gtk.FileChooserDialog(_("Select an icon"), self.dialog,
			Gtk.FileChooserAction.OPEN,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		onlyPictures = Gtk.FileFilter()
		onlyPictures.set_name(_("Pictures"))
		onlyPictures.add_mime_type('image/*')
		file_chooser.set_filter(onlyPictures)
		response = file_chooser.run()
		
		# It gets the chosen file's path
		if response == Gtk.ResponseType.OK:
			self.icon_string = file_chooser.get_filename()
			pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale( \
			                          file_chooser.get_filename(), 48, 48, True)
			self.icon_image.set_from_pixbuf(pixbuf)
		file_chooser.destroy()


class EditableList():
	def __init__(self):
		builder4 = Gtk.Builder.new_from_file(os.path.join(BASE_PATH, 'listwidget.ui'))
		self.widget = builder4.get_object('list-widget')
		self.list_box = builder4.get_object('list_box')
		self.entry = builder4.get_object('add_entry')
		builder4.get_object('add_btn').connect('clicked', self.add_row)
		
	
	def get_widget(self):
		return self.widget
	
	def add_row(self, *args):
		text = self.entry.get_text()
		if text == '':
			return
		new_row = DeletableRow(text)
		self.list_box.prepend(new_row)
		self.list_box.show_all()
		self.entry.set_text('')
	
	def get_string(self):
		for row in self.list_box.get_children():
			print(row)

class DeletableRow(Gtk.Box):
	__gtype_name__ = 'DeletableRow'
	
	def __init__(self, row_label):
		super(DeletableRow, self).__init__()
#		super().__init__() # For some reason, python3 isn't the interpreter here
		
		new_label = Gtk.Label(label=row_label)
		del_btn = Gtk.Button.new_from_icon_name('edit-delete-symbolic', Gtk.IconSize.BUTTON)
		del_btn.set_relief(Gtk.ReliefStyle.NONE)
		del_btn.connect('clicked', self.destroy2)
		self.pack_start(new_label, False, False, 0)
		self.pack_end(del_btn, False, False, 0)
		
	def destroy2(self, *args):
		self.get_parent().destroy()
		
		



