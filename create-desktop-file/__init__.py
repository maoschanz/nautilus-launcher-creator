# -*- coding: utf-8 -*-
# --- 0.1
# Copyright (C) 2012-2015 Marcos Alvarez Costales https://launchpad.net/~costales
#
# --- is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# --- is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with ---; if not, see http://www.gnu.org/licenses
# for more information.

import os
#import gi
import gettext
import urllib
#gi.require_version('Nautilus', '3.14')
from gi.repository import Nautilus, Gtk, GObject, Gio, GLib

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
LOCALE_PATH = os.path.join(BASE_PATH, 'locale')

try:
	import gettext
	gettext.bindtextdomain('create-desktop-file', LOCALE_PATH)
	_ = lambda s: gettext.dgettext('create-desktop-file', s)
except:
	_ = lambda s: s

APPS_DIRECTORY = os.path.join(os.getenv('HOME'), '.local/share/applications/')

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
    
    def _check_generate_menu(self, items):
        """Show the menu?"""
        # No items selected
        if not len(items):
            return False
        
        for item in items:
            # GNOME can only handle files
            if item.get_uri_scheme() != 'file':
                return False
            # Not folders
            if item.is_directory():
                return False
            # Only executable for now
            if not item.is_executable():
                return False
                
        for item in items:
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
        
        headerbar = Gtk.HeaderBar()
        headerbar.set_title(_("Create a launcher"))
        headerbar.set_show_close_button(True)
        self.cancelButton = Gtk.Button(_("Previous"))
        headerbar.pack_start(self.cancelButton)
        self.nextButton = Gtk.Button(_("Next"))
        self.createButton = Gtk.Button(_("Create"))
        self.createButton.get_style_context().add_class('suggested-action')
        headerbar.pack_end(self.nextButton)
        headerbar.pack_end(self.createButton)
        
        self.cancelButton.connect('clicked', self.on_previous)
        self.nextButton.connect('clicked', self.on_next)
        self.createButton.connect('clicked', self.on_create)
        
        self.win  = Gtk.Window()
        self.win .set_default_size(250, 30)
        self.win .set_border_width(10)
        self.win .set_position(Gtk.WindowPosition.CENTER)
        self.win .set_titlebar(headerbar)
        self.win .set_resizable(True)
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.first_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.second_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        self.name_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        self.description_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        self.categories_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        
        name_label = Gtk.Label(_("Name"))
        description_label = Gtk.Label(_("Description"))
        categories_label = Gtk.Label(_("Categories"))
        self.icon_preview = Gtk.Image()
        self.icon1_button = Gtk.Button(_("Select an icon from your current theme"))
        self.icon2_button = Gtk.Button(_("Select a custom picture as icon"))
        
        self.icon1_button.connect('clicked', self.on_icon_from_theme)
        self.icon2_button.connect('clicked', self.on_icon_custom)
        
        self.name_entry = Gtk.Entry()
        self.description_entry = Gtk.Entry()
        self.categories_entry = Gtk.Entry()
        
        self.name_box.pack_start(name_label, expand=False, fill=False, padding=0)
        self.description_box.pack_start(description_label, expand=False, fill=False, padding=0)
        self.categories_box.pack_start(categories_label, expand=False, fill=False, padding=0)
        
        self.name_box.pack_end(self.name_entry, expand=False, fill=False, padding=0)
        self.description_box.pack_end(self.description_entry, expand=False, fill=False, padding=0)
        self.categories_box.pack_end(self.categories_entry, expand=False, fill=False, padding=0)
        
        self.first_box.add(self.name_box)
        self.first_box.add(self.description_box)
        self.first_box.add(self.categories_box)
        self.second_box.add(self.icon_preview)
        self.second_box.add(self.icon1_button)
        self.second_box.add(self.icon2_button)
        
        main_box.add(self.first_box)
        main_box.add(self.second_box)
        
        self.win .connect('delete-event', self._close_win)
        self.win .show_all()
        
        self.win .add(main_box)
        
        main_box.show_all()
        self.second_box.props.visible = False
        self.createButton.props.visible = False
        self.cancelButton.props.visible = False
        
        Gtk.main()
    
    def on_next(self, btn):
        self.name = self.name_entry.get_text()
        self.description = self.description_entry.get_text()
        self.categories = self.categories_entry.get_text()
        self.icon_string = ''
        
        self.createButton.props.visible = True
        self.cancelButton.props.visible = True
        self.second_box.show_all()
        
        self.nextButton.props.visible = False
        self.first_box.props.visible = False
    
    def on_previous(self, btn):
        
        self.createButton.props.visible = False
        self.cancelButton.props.visible = False
        self.second_box.props.visible = False
        
        self.nextButton.props.visible = True
        self.first_box.show_all()
        
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
        file_chooser = Gtk.FileChooserDialog(_("Select an icon"), self.win,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        onlyPictures = Gtk.FileFilter()
        onlyPictures.set_name("Icons")
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
        file_chooser = Gtk.FileChooserDialog(_("Select a picture"), self.win,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        onlyPictures = Gtk.FileFilter()
        onlyPictures.set_name("Pictures")
        onlyPictures.add_mime_type('image/*')
        file_chooser.set_filter(onlyPictures)
        response = file_chooser.run()
        
        # It gets the chosen file's path
        if response == Gtk.ResponseType.OK:
            self.icon_string = file_chooser.get_filename()
            self.icon_preview.set_from_file(self.icon)
        file_chooser.destroy()
    
    def on_create(self, btn):
        filename = APPS_DIRECTORY + GLib.str_to_ascii(self.name).replace(' ', '') + ".desktop"
        Gio.File.new_for_path(filename)
        newfile = open(filename, 'w')
        newfile.write("#!/usr/bin/env xdg-open\n" +
            "[Desktop Entry]" + "\n" +
            "Name=" + self.name + "\n" +
            "Comment=" + self.description + "\n" +
            "Type=Application" + "\n" +
            "Exec=\"" + self.execpath + "\"\n" +
            "Categories=" + self.categories + "\n" +
            "Icon=" + self.icon_string
        )
        newfile.close()
        self.win.close()
        
    def _close_win(self, null1, null2):
        Gtk.main_quit()



