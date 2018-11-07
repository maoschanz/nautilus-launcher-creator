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
		self.ass = Gtk.Assistant.new()
		self.ass.set_position(Gtk.WindowPosition.CENTER)
		self.ass.connect('apply', self.on_apply)
		
		self.launcher_type = launcher_type
		self.launcher_path = ''
		self.execpath = execpath
		self.name = ''
		self.description = ''
		self.icon_string = ''
		self.categories = []
		self.keywords = []
		
		self.intro_page = self.build_intro_page()
		self.ass.append_page(self.intro_page)
		self.ass.set_page_title(self.intro_page, _("Launcher"))
		self.ass.set_page_type(self.intro_page, Gtk.AssistantPageType.CONFIRM)
		
		self.options_page = self.build_options_page()
		self.ass.append_page(self.options_page)
		self.ass.set_page_title(self.options_page, _("Options"))
		self.ass.set_page_complete(self.options_page, True)
		self.ass.set_page_type(self.options_page, Gtk.AssistantPageType.CONFIRM)
		
		self.icon_page = self.build_icon_page()
		self.ass.append_page(self.icon_page)
		self.ass.set_page_title(self.icon_page, _("Icon"))
		self.ass.set_page_complete(self.icon_page, True)
		self.ass.set_page_type(self.icon_page, Gtk.AssistantPageType.CONFIRM)
		
		self.summary_page = self.build_summary_page()
		self.ass.append_page(self.summary_page)
		self.ass.set_page_title(self.summary_page, _("Summary"))
		self.ass.set_page_complete(self.summary_page, True)
		self.ass.set_page_type(self.summary_page, Gtk.AssistantPageType.CONFIRM)
		
		self.ass.connect('close', self.destroy_ass)
		self.ass.connect('cancel', self.destroy_ass)
		
	def build_intro_page(self):
		
		page_grid = Gtk.Grid(column_spacing=20, row_spacing=20, margin=20, column_homogeneous=False)
		
		name_label = Gtk.Label(_("Name"))
		self.name_entry = Gtk.Entry()
		
		type_label = Gtk.Label(_("Type"))
		
		self.app_btn = Gtk.RadioButton(_("Application"), draw_indicator=False)
		self.link_btn = Gtk.RadioButton(_("Link"), group=self.app_btn, draw_indicator=False)
		type_btn_box = Gtk.Box(homogeneous=True)
		type_btn_box.add(self.app_btn)
		type_btn_box.add(self.link_btn)
		type_btn_box.get_style_context().add_class('linked')
		type_btn_box.set_size_request(400, 10)
		
		path_label = Gtk.Label(_("Target path"))
		self.path_entry = Gtk.Entry()
		self.path_entry.set_text(self.execpath)
		
		fn_label = Gtk.Label(_("Launcher path"))
		self.fn_entry = Gtk.Entry()
		fn_btn = Gtk.Button.new_from_icon_name('document-open-symbolic', Gtk.IconSize.BUTTON)
		fn_btn.set_tooltip_text(_("Browse"))
		fn_btn.connect('clicked', self.open_path_chooser)
		fn_box = Gtk.Box()
		fn_box.pack_start(self.fn_entry, expand=True, fill=True, padding=0)
		fn_box.add(fn_btn)
		fn_box.get_style_context().add_class('linked')
		
		basename = self.execpath.split('/')[-1]
		if self.launcher_type == 'Application':
			self.app_btn.set_active(True)
			filename = APPS_DIRECTORY + GLib.str_to_ascii(basename).replace(' ', '') + ".desktop"
		elif self.launcher_type == 'Link':
			self.link_btn.set_active(True)
			filename = HOME_DIRECTORY + GLib.str_to_ascii(basename).replace(' ', '') + ".desktop"
		self.fn_entry.set_text(filename)
		
		page_grid.attach(name_label, 0, -1, 1, 1)
		page_grid.attach(self.name_entry, 1, -1, 1, 1)
		page_grid.attach(type_label, 0, 0, 1, 1)
		page_grid.attach(type_btn_box, 1, 0, 1, 1)
		page_grid.attach(path_label, 0, 1, 1, 1)
		page_grid.attach(self.path_entry, 1, 1, 1, 1)
		page_grid.attach(fn_label, 0, 2, 1, 1)
		page_grid.attach(fn_box, 1, 2, 1, 1)
		
		self.name_entry.connect('notify::text', self.check_1st_page_completion)
		self.path_entry.connect('notify::text', self.check_1st_page_completion)
		self.fn_entry.connect('notify::text', self.check_1st_page_completion)
		
		return page_grid
		
	def build_options_page(self):
		page_grid = Gtk.Grid(column_spacing=20, row_spacing=20, margin=20, row_homogeneous=False, column_homogeneous=False)
		
		description_label = Gtk.Label(_("Description"))
		categories_label = Gtk.LinkButton('https://standards.freedesktop.org/menu-spec/latest/apa.html')
		categories_label.set_label(_("Categories"))
		keywords_label = Gtk.Label(_("Keywords"))
		
		self.description_entry = Gtk.Entry()
		self.categories_entry = Gtk.Entry() # TODO
		self.keywords_entry = Gtk.Entry() # TODO
		
		self.categories_box = Gtk.Box()
		self.keywords_box = Gtk.Box()
		self.categories_box.get_style_context().add_class('linked')
		self.keywords_box.get_style_context().add_class('linked')
		
		self.categories_box.set_tooltip_text(_("Applications can be organized in categories in the system menus."))
		self.keywords_box.set_tooltip_text(_("Applications can be found from a keyword with the system search."))
		
		categories_btn = Gtk.Button.new_from_icon_name('list-add-symbolic', Gtk.IconSize.BUTTON)
		keywords_btn = Gtk.Button.new_from_icon_name('list-add-symbolic', Gtk.IconSize.BUTTON)
		categories_btn.connect('clicked', self.add_category)
		keywords_btn.connect('clicked', self.add_keyword)
		
		self.categories_box.add(self.categories_entry)
		self.categories_box.add(categories_btn)
		self.keywords_box.add(self.keywords_entry)
		self.keywords_box.add(keywords_btn)
		
		self.categories_list = Gtk.ListBox()
		self.keywords_list = Gtk.ListBox()
		self.keywords_list.set_size_request(100, 10)
		
		destroy_categories_btn = Gtk.Button(_("Reset"))
		destroy_keywords_btn = Gtk.Button(_("Reset"))
		destroy_categories_btn.connect('clicked', self.destroy_c_list)
		destroy_keywords_btn.connect('clicked', self.destroy_k_list)
		
		page_grid.attach(description_label, 0, 1, 1, 1)
		page_grid.attach(self.description_entry, 1, 1, 3, 1)
		
		page_grid.attach(categories_label, 0, 2, 1, 1)
		page_grid.attach(self.categories_box, 1, 2, 1, 1)
		page_grid.attach(self.categories_list, 2, 2, 1, 2)
		page_grid.attach(destroy_categories_btn, 3, 2, 1, 1)
		page_grid.attach(keywords_label, 0, 4, 1, 1)
		page_grid.attach(self.keywords_box, 1, 4, 1, 1)
		page_grid.attach(self.keywords_list, 2, 4, 1, 2)
		page_grid.attach(destroy_keywords_btn, 3, 4, 1, 1)
		
		return page_grid
		
	def build_icon_page(self):
		page_grid = Gtk.Grid(column_spacing=20, row_spacing=20, margin=20, column_homogeneous=False)
		
		self.icon_preview = Gtk.Image()
		self.icon_preview.set_size_request(60, 60)
		frame = Gtk.Frame()
		frame.add(self.icon_preview)
		
		icon1_button = Gtk.Button(_("Select an icon from your current theme"))
		icon2_button = Gtk.Button(_("Select a custom picture as icon"))
		
		icon1_button.connect('clicked', self.on_icon_from_theme)
		icon2_button.connect('clicked', self.on_icon_custom)
		
		page_grid.attach(frame, 0, 0, 1, 2)
		page_grid.attach(icon1_button, 1, 0, 1, 1)
		page_grid.attach(icon2_button, 1, 1, 1, 1)
		
		return page_grid
		
	def build_summary_page(self):
		page_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, margin=10, spacing=10)
		self.launcher_path_entry = Gtk.Entry()
		self.textview = Gtk.TextView(expand=True)
		self.textview.set_accepts_tab(True)
		page_box.add(self.launcher_path_entry)
		page_box.add(self.textview)
		
		return page_box
		
	def destroy_ass(self, ass):
		ass.destroy()
		
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
		file_chooser = Gtk.FileChooserDialog(_("Select an icon"), self.ass,
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
			self.icon_preview.set_from_icon_name(self.icon_string, Gtk.IconSize.DIALOG)
		file_chooser.destroy()
		
	def on_icon_custom(self, btn):
		# Building a FileChooserDialog for pictures
		file_chooser = Gtk.FileChooserDialog(_("Select an icon"), self.ass,
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
			pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(file_chooser.get_filename(), 48, 48, True)
			self.icon_preview.set_from_pixbuf(pixbuf)
		file_chooser.destroy()
		
	def open_path_chooser(self, b):
		file_chooser = Gtk.FileChooserDialog(_("Launcher path"), self.ass,
			Gtk.FileChooserAction.SAVE,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
		response = file_chooser.run()
		if response == Gtk.ResponseType.OK:
			self.fn_entry.set_text(file_chooser.get_filename())
		file_chooser.destroy()
		
	def add_category(self, b):
		if self.categories_entry.get_text() == '':
			return
		self.categories.append(self.categories_entry.get_text())
		self.build_c_list()
		self.categories_entry.set_text('')
		
	def add_keyword(self, b):
		if self.keywords_entry.get_text() == '':
			return
		self.keywords.append(self.keywords_entry.get_text())
		self.build_k_list()
		self.keywords_entry.set_text('')
		
	def destroy_c_list(self, b):
		while self.categories_list.get_row_at_index(0) is not None:
			self.categories_list.get_row_at_index(0).destroy()
		self.categories = []
			
	def destroy_k_list(self, b):
		while self.keywords_list.get_row_at_index(0) is not None:
			self.keywords_list.get_row_at_index(0).destroy()
		self.keywords = []
	
	def build_c_list(self):
		while self.categories_list.get_row_at_index(0) is not None:
			self.categories_list.get_row_at_index(0).destroy()
		for cat in self.categories:
			print(cat)
			row = Gtk.ListBoxRow()
			row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
			row_box.pack_start(Gtk.Label(cat), expand=False, fill=False, padding=0)
			row.add(row_box)
			self.categories_list.prepend(row)
		self.categories_list.show_all()
	
	def build_k_list(self):
		while self.keywords_list.get_row_at_index(0) is not None:
			self.keywords_list.get_row_at_index(0).destroy()
		for cat in self.keywords:
			print(cat)
			row = Gtk.ListBoxRow()
			row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
			row_box.pack_start(Gtk.Label(cat), expand=False, fill=False, padding=0)
			row.add(row_box)
			self.keywords_list.prepend(row)
		self.keywords_list.show_all()
		
	def check_1st_page_completion(self, e, t):
		if self.name_entry.get_text() == '':
			self.ass.set_page_complete(self.intro_page, False)
		elif self.path_entry.get_text() == '':
			self.ass.set_page_complete(self.intro_page, False)
		elif self.fn_entry.get_text() == '':
			self.ass.set_page_complete(self.intro_page, False)
		else:
			self.ass.set_page_complete(self.intro_page, True)

	def on_apply(self, ass):
		if self.ass.get_current_page() == 0:
			self.name = self.name_entry.get_text()
			if self.app_btn.get_active():
				self.launcher_type = 'Application'
				self.categories_box.set_sensitive(True)
				self.keywords_box.set_sensitive(True)
			elif self.link_btn.get_active():
				self.launcher_type = 'Link'
				self.categories_box.set_sensitive(False)
				self.keywords_box.set_sensitive(False)
				self.categories = []
				self.keywords = []
			self.execpath = self.path_entry.get_text()
			self.launcher_path = self.fn_entry.get_text()
			
		elif self.ass.get_current_page() == 1:
			self.description = self.description_entry.get_text()
		
		elif self.ass.get_current_page() == 2:
			self.launcher_path_entry.set_text(self.launcher_path)
			text = '[Desktop Entry]\nName=' + self.name
			text += '\nType=' + self.launcher_type
			if self.launcher_type == 'Application':
				text += '\nExec=' + self.execpath
			else:
				text += '\nURL=file://' + urllib.pathname2url(self.execpath)
			if self.description != '':
				text += '\nComment=' + self.description
			if self.icon_string != '':
				text += '\nIcon=' + self.icon_string
			if self.categories != []:
				text += '\nCategories=' + ';'.join(self.categories) + ';'
			if self.keywords != []:
				text += '\nKeywords=' + ';'.join(self.keywords) + ';'
			self.textview.get_buffer().set_text(text)
		
		elif self.ass.get_current_page() == 3:
			self.launcher_path = self.launcher_path_entry.get_text()
			text = self.textview.get_buffer().get_text( self.textview.get_buffer().get_start_iter(), \
				self.textview.get_buffer().get_end_iter(), False)
			Gio.File.new_for_path(self.launcher_path)
			newfile = open(self.launcher_path, 'w')
			newfile.write(text)
			newfile.close()
			self.ass.close()
		
#----------------------------------------
