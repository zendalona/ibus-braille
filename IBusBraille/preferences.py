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

import sys
import configparser

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

from IBusBraille import global_var

from IBusBraille import localization
_ = localization._

from brailleinput.engine import Keys


class Preferences():
	
	default_keycode_map = {Keys.Dot1 : 33, Keys.Dot2 : 32, Keys.Dot3 : 31,
		Keys.Dot4 : 36, Keys.Dot5 : 37, Keys.Dot6 : 38, Keys.Dot7 : 44,
		Keys.Dot8 : 52, Keys.ToggleBrailleMode : 88, Keys.Abbreviation : 30, Keys.Capital : 34,
		Keys.LetterDeletion : 35, Keys.Punctuation : 39, Keys.BegMidSwitch : 23,
		Keys.OneHandSkip : 20, Keys.Space : 57, Keys.NewLine : 28, Keys.NewLine2 : 49,
		Keys.LangSwitch : 13, Keys.BuiltInSel : 54, Keys.L1 : 2, Keys.L2 : 3,
		Keys.L3 : 4, Keys.L4 : 5, Keys.L5 : 6, Keys.L6 : 7, Keys.L7 : 8, Keys.L8 : 9,
		Keys.L9 : 10, Keys.L10 : 11, Keys.L11 : 12, Keys.L12 : 13}

	
	def __init__(self):
		self.set_default_preferences();
		
	def get_keycode_map(self):
		return {v: k for k, v in self.keycode_map.items()}


	def set_default_preferences(self):
		self.checked_languages_built_in = ["english","hindi", "kannada", "malayalam", "spanish", "tamil", "numerical", "arabic", "english-grade-2", "sanskrit", "braille-patterns", "french",]
		self.checked_languages_liblouis = ["English-US-Grade-1", "English-US-Grade-2", "Malayalam-Grade-1", "Malayalam-Grade-2", "Hindi-Grade-1", 
		"Spanish", "Portuguese-Grade-1", "Arabic-Grade-1", "Nemeth-Code-for-Mathematics", "Russian-Grade-1", "English-US-Grade-3", "Malayalam-Grade-3" ]
		
		self.keycode_map = self.default_keycode_map.copy();

		self.default_liblouis_mode = True;
		self.auto_capitalize_sentence =  True
		self.auto_capitalize_line =  False
		self.simple_mode =  False
		self.speech =  True
		self.conventional_braille = False;
		self.one_hand_mode = False
		self.one_hand_conversion_delay = 500
		self.line_limit =  100
		self.auto_new_line = 1;


	
	def load_preferences_from_file(self, filename):
		try:
			cp = configparser.ConfigParser()
			print(filename)
			cp.read(filename)
			self.checked_languages_built_in = cp.get('language',"checked-languages-built-in").split(",")
			self.checked_languages_liblouis = cp.get('language',"checked-languages-liblouis").split(",")
			self.default_liblouis_mode = int(cp.get('language',"default-liblouis-mode"))

			for item in Keys:
				self.keycode_map[item] = int(cp.get('key-bindings',str(item)))
			
			self.auto_capitalize_sentence = int(cp.get('auto-capitalizing',"auto-capitalize-sentence"))
			self.auto_capitalize_line = int(cp.get('auto-capitalizing',"auto-capitalize-line"))

			self.simple_mode = int(cp.get('built-in',"simple-mode"))
			self.conventional_braille = int(cp.get('built-in',"conventional-braille"))

			self.line_limit = int(cp.get('line-limiting','line-limit'))
			self.auto_new_line = int(cp.get('line-limiting','auto-new-line'))
			
			self.speech = int(cp.get('voice-announcement',"speech"))

			self.one_hand_mode = int(cp.get('one-hand-typing',"one-hand-mode"))
			self.one_hand_conversion_delay = int(cp.get('one-hand-typing',"one-hand-conversion-delay"));
			
		except:
			print("Configuration reading error : ", sys.exc_info()[0])
			self.set_default_preferences()

	def save_preferences_to_file(self, filename):
		
		cp = configparser.ConfigParser()
		cp.add_section('language')
		cp.add_section('built-in')
		cp.add_section('auto-capitalizing')
		cp.add_section('line-limiting')
		cp.add_section('voice-announcement')
		cp.add_section('one-hand-typing')
		cp.add_section('key-bindings')

		cp.set('language',"checked-languages-built-in",",".join(self.checked_languages_built_in))
		cp.set('language',"checked-languages-liblouis",",".join(self.checked_languages_liblouis))
		cp.set('language',"default-liblouis-mode",str(int(self.default_liblouis_mode)))

		for key in self.keycode_map.keys():
			cp.set('key-bindings',str(key),str(self.keycode_map[key]))

		cp.set('auto-capitalizing',"auto-capitalize-sentence",str(int(self.auto_capitalize_sentence)))
		cp.set('auto-capitalizing',"auto-capitalize-line",str(int(self.auto_capitalize_line)))

		cp.set('built-in',"simple-mode",str(int(self.simple_mode)))
		cp.set('built-in',"conventional-braille",str(int(self.conventional_braille)))

		cp.set('line-limiting',"line-limit",str(int(self.line_limit)))
		cp.set('line-limiting',"auto-new-line",str(int(self.auto_new_line)))

		cp.set('voice-announcement',"speech",str(int(self.speech)))

		cp.set('one-hand-typing',"one-hand-mode",str(int(self.one_hand_mode)))
		cp.set('one-hand-typing',"one-hand-conversion-delay",str(int(self.one_hand_conversion_delay)))

		with open(filename , 'w') as configfile:
			cp.write(configfile)
			
	def set_built_in_language_list(self, list_):
		self.list_of_available_built_in_languages = list_

	def set_liblouis_language_list(self, list_):
		self.list_of_available_liblouis_languages = list_
		
			
	def open_preferences_dialog(self):
		self.guibuilder = Gtk.Builder()
		self.guibuilder.add_from_file(global_var.data_dir+"preferences.glade")
		self.window = self.guibuilder.get_object("window")


		# Setting Liblouis language comboboxes
		self.box_liblouis = self.guibuilder.get_object("box_liblouis")

		liststore_liblouis_languages = Gtk.ListStore(str)
		for item in self.list_of_available_liblouis_languages:
			liststore_liblouis_languages.append([item]);
		
		self.list_of_liblouis_language_comboboxes = []
		for i in range (0, 12) :		
			# Setting combobox 
			combo = Gtk.ComboBox.new_with_model(liststore_liblouis_languages)
			renderer_text = Gtk.CellRendererText()
			combo.pack_start(renderer_text, True)
			combo.add_attribute(renderer_text, "text", 0)
			
			cur_lang = self.checked_languages_liblouis[i]
			cur_lang_index =  self.list_of_available_liblouis_languages.index(cur_lang)
			combo.set_active(cur_lang_index)
			combo.show()
			
			# Setting label
			label = Gtk.Label(_("Table ")+str(i+1))
			label.set_mnemonic_widget(combo)
			label.show()
			
			# Packing label and combobox
			box = Gtk.HBox()
			box.pack_start(label,True,True,10);
			box.pack_start(combo,True,True,10);
			box.show()
			
			self.box_liblouis.pack_start(box,False,False,10)
			
			self.list_of_liblouis_language_comboboxes.append(combo)


		# Setting Built-in language comboboxes
		self.box_built_in = self.guibuilder.get_object("box_built_in")

		liststore_built_in_languages = Gtk.ListStore(str)
		for item in self.list_of_available_built_in_languages:
			liststore_built_in_languages.append([item]);
		
		self.list_of_built_in_language_comboboxes = []
		for i in range (0, 12) :		
			# Setting combobox 
			combo = Gtk.ComboBox.new_with_model(liststore_built_in_languages)
			renderer_text = Gtk.CellRendererText()
			combo.pack_start(renderer_text, True)
			combo.add_attribute(renderer_text, "text", 0)
			
			cur_lang = self.checked_languages_built_in[i]
			cur_lang_index =  self.list_of_available_built_in_languages.index(cur_lang)
			combo.set_active(cur_lang_index)
			combo.show()
			
			# Setting label
			label = Gtk.Label(_("Language "+str(i+1)))
			label.set_mnemonic_widget(combo)
			label.show()
			
			# Packing label and combobox
			box = Gtk.HBox()
			box.pack_start(label,True,True,20);
			box.pack_start(combo,True,True,20);
			box.show()			
			
			self.box_built_in.pack_start(box,False,False,10);
			
			self.list_of_built_in_language_comboboxes.append(combo)
		

		# Set key/shortcuts in UI
		self.keycode_map_new = self.keycode_map.copy()
		for item in Keys:
			widget = self.guibuilder.get_object(str(item).replace("Keys.",""))
			hardware_keycode = self.keycode_map_new[item]
			
			keymap = Gdk.Keymap.get_default()
			entries_for_keycode = keymap.get_entries_for_keycode(hardware_keycode + 8)
			entries = entries_for_keycode[-1]
			text = Gdk.keyval_name(entries[0])
			
			widget.set_text(text)
		
		
		#Set auto capitalize sentence checkbox
		self.checkbutton_auto_capitalize_sentence = self.guibuilder.get_object("checkbutton_auto_capitalize_sentence")
		self.checkbutton_auto_capitalize_sentence.set_active(self.auto_capitalize_sentence)

		#Set auto capitalize line checkbox
		self.checkbutton_auto_capitalize_line = self.guibuilder.get_object("checkbutton_auto_capitalize_line")
		self.checkbutton_auto_capitalize_line.set_active(self.auto_capitalize_line)

		#Set Simple mode checkbox
		self.checkbutton_simple_mode = self.guibuilder.get_object("checkbutton_simple_mode")
		self.checkbutton_simple_mode.set_active(self.simple_mode)

		#Set conventional-braille checkbox
		self.checkbutton_conventional_braille = self.guibuilder.get_object("checkbutton_conventional_braille")
		self.checkbutton_conventional_braille.set_active(self.conventional_braille)

		#Set default TableType combobox
		self.combobox_table_type = self.guibuilder.get_object("combobox_table_type")
		self.combobox_table_type.set_active(self.default_liblouis_mode)

		
		#Set auto new line checkbox
		self.checkbutton_auto_new_line = self.guibuilder.get_object("checkbutton_auto_new_line")
		self.checkbutton_auto_new_line.set_active(self.auto_new_line)

		#Set Speech checkbox
		self.checkbutton_speech = self.guibuilder.get_object("checkbutton_speech")
		self.checkbutton_speech.set_active(self.speech)

		#Set auto new line checkbox
		self.spinbutton_line_limit = self.guibuilder.get_object("spinbutton_line_limit")
		self.spinbutton_line_limit.set_value(self.line_limit)


		#Set one-hand-mode checkbox
		self.checkbutton_one_hand_mode = self.guibuilder.get_object("checkbutton_one_hand_mode")
		self.checkbutton_one_hand_mode.set_active(self.one_hand_mode)

		#Set one-hand-mode conversion delay
		self.scale_one_hand_conversion_delay = self.guibuilder.get_object("scale_one_hand_conversion_delay")
		self.scale_one_hand_conversion_delay.set_value(self.one_hand_conversion_delay)			
		
		self.guibuilder.connect_signals(self)
		self.window.show()



	def on_key_press(self,widget,event):
		hardware_keycode = int(event.hardware_keycode)
		hardware_keycode_ibus = hardware_keycode - 8 
		print(hardware_keycode_ibus)
		# Avoid essential keys like Esc, Tab, Shift, R-Shift, Left, Right, Up, Down 
		if (hardware_keycode not in [9,23,50,62,113,114,111,116]):
			widget_name = Gtk.Buildable.get_name(widget)	
			key_in_widget = Keys.__dict__[widget_name]
			if self.keycode_map_new[key_in_widget] != hardware_keycode_ibus:
				if hardware_keycode_ibus in self.keycode_map_new.values():
					widget.set_text("None")
					self.keycode_map_new[key_in_widget] = None;
				else:
					self.keycode_map_new[key_in_widget] = hardware_keycode_ibus
					keymap = Gdk.Keymap.get_default()
					entries_for_keycode = keymap.get_entries_for_keycode(hardware_keycode)
					entries = entries_for_keycode[-1]
					text = Gdk.keyval_name(entries[0])
					widget.set_text(text)

	def set_on_apply_preferences_callback(self, function):
		self.apply_preferences = function
	
	def on_preferences_dialog_apply(self, widget):
		# Copy new key bindings if there is no unassigned keybinding
		if (None in self.keycode_map_new.values()):
			dialog = Gtk.MessageDialog( flags=0, message_type=Gtk.MessageType.INFO,
			buttons=Gtk.ButtonsType.OK, text=_("Unassigned keybinding found"))
			dialog.format_secondary_text(_("Find and fix unassigned keybindings before applying"))
			dialog.run()
			dialog.destroy()
			return
		else:
			self.keycode_map = self.keycode_map_new.copy()

		self.checked_languages_liblouis = []
		for combo in self.list_of_liblouis_language_comboboxes:
			index = combo.get_active()
			self.checked_languages_liblouis.append(self.list_of_available_liblouis_languages[index])
		print(self.checked_languages_liblouis)

		self.checked_languages_built_in = []
		for combo in self.list_of_built_in_language_comboboxes:
			index = combo.get_active()
			self.checked_languages_built_in.append(self.list_of_available_built_in_languages[index])
		print(self.checked_languages_built_in)
		
		# Copy new values
		self.auto_capitalize_sentence = self.checkbutton_auto_capitalize_sentence.get_active()
		self.auto_capitalize_line = self.checkbutton_auto_capitalize_line.get_active()
		self.simple_mode = self.checkbutton_simple_mode.get_active()
		self.conventional_braille = self.checkbutton_conventional_braille.get_active()
		self.default_liblouis_mode = self.combobox_table_type.get_active()
		
		self.one_hand_mode = self.checkbutton_one_hand_mode.get_active()
		self.one_hand_conversion_delay = self.scale_one_hand_conversion_delay.get_value()

		self.auto_new_line = self.checkbutton_auto_new_line.get_active()
		self.line_limit = self.spinbutton_line_limit.get_value_as_int()

		self.speech = self.checkbutton_speech.get_active()
		
		# Closing preferences window
		self.window.destroy()
		
		# Calling function to apply preferences on existing views
		self.apply_preferences()


	def on_preferences_dialog_restore(self, widget):
		self.set_default_preferences()
		self.apply_preferences()
		self.window.destroy()

	def on_preferences_dialog_close(self, widget):
		self.window.destroy()
