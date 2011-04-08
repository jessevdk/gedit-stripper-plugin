# -*- coding: utf-8 -*-

#  phpcompletion.py - PHP completion using the completion framework
#
#  Copyright (C) 2009 - Jesse van den Kieboom
#  Copyright (C) 2009 - Ignacio Casal Quinteiro
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330,
#  Boston, MA 02111-1307, USA.

from documenthelper import DocumentHelper
from gi.repository import Gedit, GObject

class WindowHelper(GObject.Object, Gedit.WindowActivatable):
    window = GObject.property(type=Gedit.Window)

    DOCUMENT_DATA_KEY = "StripperPluginDocumentData"

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        for view in self.window.get_views():
            self.add_document_helper(view)

        self._tab_added_id = self.window.connect('tab-added', self.on_tab_added)
        self._tab_removed_id = self.window.connect('tab-removed', self.on_tab_removed)

    def do_deactivate(self):
        # Remove the provider from all the views
        for view in self.window.get_views():
            self.remove_document_helper(view)

        self.window.disconnect(self._tab_added_id)
        self.window.disconnect(self._tab_removed_id)

        self.window = None

    def add_document_helper(self, view):
        data = view.get_data(self.DOCUMENT_DATA_KEY)

        if not data:
            view.set_data(self.DOCUMENT_DATA_KEY, DocumentHelper(view))

    def remove_document_helper(self, view):
        data = view.get_data(self.DOCUMENT_DATA_KEY)

        if data:
            data.deactivate()
            view.set_data(self.DOCUMENT_DATA_KEY, None)

    def on_tab_added(self, window, tab):
        # Add provider to the new view
        self.add_document_helper(tab.get_view())

    def on_tab_removed(self, window, tab):
        # Remove provider from the view
        self.remove_document_helper(tab.get_view())

# ex:ts=4:et:
