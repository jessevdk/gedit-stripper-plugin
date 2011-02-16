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

import gtk

class DocumentHelper:
    def __init__(self, view):
        self._view = view
        self._buffer = view.get_buffer()
        self._completion = view.get_completion()
        self._no_text = True

        self._view_signals = [
            self._view.connect('notify::buffer', self.on_notify_buffer),
            self._view.connect('event-after', self.on_key_press_event)
        ]
        
        self._completion_signals = [
            self._completion.connect('activate-proposal', self.on_activate_proposal)
        ]

        self._connect_buffer()

    def _connect_buffer(self):
        self._buffer_signals = [
        ]

    def _disconnect(self, obj, signals):
        if obj:
            for sid in signals:
                obj.disconnect(sid)

        return []

    def _disconnect_buffer(self):
        self._buffer_signals = self._disconnect(self._buffer, self._buffer_signals)
        self._buffer_signals = []

    def _disconnect_view(self):
        self._disconnect(self._view, self._view_signals)
        self._view_signals = []

    def _disconnect_completion(self):
        self._disconnect(self._completion, self._completion_signals)
        self._completion_signals = []

    def deactivate(self):
        self._disconnect_buffer()
        self._disconnect_completion()
        self._disconnect_view()

        self._buffer = None
        self._view = None
        self._completion = None

    def on_notify_buffer(self, view, gspec):
        self._disconnect_buffer()

        self._buffer = view.get_buffer()
        self._connect_buffer()

    def on_key_press_event(self, view, event):
        if event.type != gtk.gdk.KEY_PRESS:
            return

        if not self._no_text:
            self._no_text = True
            return

        state = event.state
        key = event.keyval

        if (key == gtk.keysyms.Return or key == gtk.keysyms.KP_Enter) and not (state & gtk.gdk.SHIFT_MASK):
            piter = self._buffer.get_iter_at_mark(self._buffer.get_insert())

            if not piter.backward_line():
                return

            end = piter.copy()
            end.forward_to_line_end()

            extraindent = 0

            while not end.starts_line():
                if not end.backward_char():
                    break

                if end.get_char() == ')':
                    break

                if end.get_char() == '(':
                    start = end.copy()
                    start.set_line_offset(0)

                    extraindent = len(start.get_text(end).lstrip()) + 1

            end = piter.copy()
            stripit = True

            while not end.ends_line():
                if not end.get_char().isspace():
                    stripit = False
                    break

                if not end.forward_char():
                    stripit = False
                    break

            if stripit:
                self._buffer.delete(piter, end)

            if extraindent > 0:
                piter = self._buffer.get_iter_at_mark(self._buffer.get_insert())
                self._buffer.insert(piter, ' ' * extraindent)

    def on_activate_proposal(self, completion):
        self._no_text = False

# ex:ts=4:et:
