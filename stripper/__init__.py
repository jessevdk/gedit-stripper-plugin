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

import gedit
from windowhelper import WindowHelper

class StripperPlugin(gedit.Plugin):
    WINDOW_DATA_KEY = "StripperPluginWindowData"

    def __init__(self):
        gedit.Plugin.__init__(self)

    def activate(self, window):
        helper = WindowHelper(self, window)
        window.set_data(self.WINDOW_DATA_KEY, helper)

    def deactivate(self, window):
        window.get_data(self.WINDOW_DATA_KEY).deactivate()
        window.set_data(self.WINDOW_DATA_KEY, None)

    def update_ui(self, window):
        window.get_data(self.WINDOW_DATA_KEY).update_ui()

# ex:ts=4:et:
