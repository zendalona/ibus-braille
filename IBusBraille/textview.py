###########################################################################
#    IBus-Braille - Braille input engine for IBus
#
#    Copyright (C) 2014-2015 Nalin Sathyan <nalin.x.linux@gmail.com>
#    Copyright (C) 2016-2017 Anwar N <anwar3746@gmail.com>
#    Copyright (C) 2022-2023 Nalin Sathyan <nalin.x.linux@gmail.com>
#    
#    This project was developed twice under Google Summer of Code program 
#    GSoC 2014 and 2016 under the guidance of Samuel Thibault.
#
#    Entire project is rewritten by Nalin Sathyan and powered by Zendalona
#    wwww.zendalona.com
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################


import os

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango

from brailleinput.engine import BrailleInputEngine

class BrailleInputTextView(Gtk.TextView, BrailleInputEngine):
	def __init__(self):
		Gtk.TextView.__init__(self)
		BrailleInputEngine.__init__(self)
				
		self.set_get_text_before_cursor_callback(self.get_text_before_cursor)
		self.set_delete_text_before_cursor_callback(self.delete_text_before_cursor)
		self.set_insert_text_at_cursor_callback(self.insert_text_at_cursor)
	
		self.connect('key-press-event', self.key_press_handler)
		self.connect('key-release-event', self.key_release_handler)

	def get_text_before_cursor(self, count):
		textbuffer = self.get_buffer();
		start = textbuffer.get_iter_at_mark(textbuffer.get_insert());
		end = start.copy()
		start.backward_chars(count)
		text = textbuffer.get_text(start,end,False)
		return text
		
	def delete_text_before_cursor(self, count):
		textbuffer = self.get_buffer();
		start = textbuffer.get_iter_at_mark(textbuffer.get_insert());
		end = start.copy()
		start.backward_chars(count)
		textbuffer.delete(start, end)

	def insert_text_at_cursor(self, text):
		textbuffer = self.get_buffer();
		textbuffer.insert_at_cursor(text);
		if(text == "\n"):
			insert_mark = textbuffer.get_insert()
			self.scroll_to_mark(insert_mark,0.0,False,0.0,0.0)
		
	def key_press_handler(self,widget,event):
		return self.key_pressed(event.hardware_keycode)

	def key_release_handler(self,widget,event):
		return self.key_released(event.hardware_keycode)

	def get_text(self):
		textbuffer = self.get_buffer();
		start,end = textbuffer.get_bounds()
		text = textbuffer.get_text(start,end,False)
		return text

	def get_modified(self):
		textbuffer = self.get_buffer();
		textbuffer.get_modified()

	def set_text(self, text):
		textbuffer = self.get_buffer();
		textbuffer.set_text(text)
		self.reset()
