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
import configparser

import gi

gi.require_version('IBus', '1.0')
from gi.repository import IBus

from brailleinput.engine import BrailleInputEngine
from brailleinput.engine import Keys

from IBusBraille import preferences
from IBusBraille import global_var
from IBusBraille import user_abbreviation_manager

from IBusBraille import localization
_ = localization._

# For 3 dot system
from threading import Timer

 
keysyms = IBus

user_conf_dir = os.environ['HOME']+"/.ibus-braille/"

abbreviations_file_path = user_conf_dir+"abbreviations.txt"


########################## Temporary fix ###################
espeak_available = 0
speechd_available = 0;
try:
	import speechd
	speechd_available = 1;
	client = speechd.Client("IBus-Braille")
except:
	try:
		from espeak import espeak
		espeak_available = 1;
	except:
		espeak_available = 0;

#def start_tts():
#	if(speechd_available):
#		client = speechd.Client("IBus-Braille")


def speak(text):
	if(speechd_available):
		client.cancel()
		client.speak(text);
		print("TTS : "+text)
	elif (espeak_available):
		espeak.cancel()
		espeak.synth(text)
	else:
		print("No tts api available!(python3-espeak/python3-speechd)");

def set_tts_language(language):
	print(language)
	if(speechd_available):
		try:
			client.set_language(language)
		except:
			client.set_language(language.split("-")[0])
	elif (espeak_available):
		espeak.set_voice(language)
	else:
		pass
		
def close_tts():
	if(speechd_available):
		print("Closing tts")
		client.close()


tts_dictionary = {"\n" : _("new_line"),
 " " : _("space"), "?" : _("questionmark"), 
 "," : _("comma"), "·" : _("multiplication dot"),"." : _("full stop"), "!" : _("exclamation"),
 "(" : _("opening bracket"), ")" : _("closing bracket"), 
 "\"" : _("double_quote"), "\'" : _("single_quote"), 
 "/" : _("slash"), "\\" : _("backslash"), ";" : _("semicolon"), "–" : _("Dash"),"…" : _("Ellipsis"),
 ":" : _("colon"), "{" : _("opening curly bracket"), "}" : _("closing curly bracket"),
"[" : _("opening square bracket"), "]" : _("closing square bracket"),
"⏢" : _("Trapezium"),
"☆" : _("White Star"),
"¶" : _("Paragraph mark"),
"￩" : _("Halfwidth leftwards arrow"),
"+-" : _("Plus followed by minus"),
"〃" : _("Ditto Mark"),
"ʹ" : _("Prime"),
"≮" : _("Note less than"),
"∠" : _("Acute angle"),
"▬" : _("Rectangle"),
"○" : _("Circle"),
"⊥" : _("is perpenticular to"),
"∥" : _("is parallel to"),
"✓" : _("Check mark"),
"″" : _("Ditto mark"),
"∶" : _("Ratio"),
"|" : _("Vertical"),
"―" : _("Horizondal"),
"<" : _("Less than"),
">" : _("Greater than"),
"⋝" : _("Bar over greater than"),
"⋜" : _("Bar over less than"),
"≦" : _("Is less than or equal to"),
"≧" : _("Is greater than or equal to"),
"≦" : _("Is equal to or less than"),
"≧" : _("Is equal to or greater than"),
"><" : _("Is greater than followed by less than"),
"<>" : _("Is less than followed by greater than"),
">=<" : _("Is greater than followed by equals sign followed by less than"),
"<=>" : _("Is less than followed by equals sign followed by greater than"),
"◺" : _("Right Triangle"),
"▱" : _("Parallellogram"),
"◠" : _("Arc upward"),
"◡" : _("Arc downward"),
"⬠" : _("Pentagon"),
"⬡" : _("Hexagon"),
"⩳" : _("Equall sign under single tilde"),
"≂" : _("Bar under single tilde"),
"∠" : _("Angle acute"),
"⦦" : _("Angle obtuse"),
"∟" : _("Right Angle"),
"△" : _("Acute triangle"),
"⊕" : _("Circle with interior plus sign"),
"⊗" : _("Circle with interior cross sign"),
"⊡" : _("Square with interior dot sign"),
"￫" : _("Right pointing short"),
"⇄" : _("Reverse arrows"),
"⇒" : _("Implication"),
"′" : _("Prime"),
"′" : _("Minute"),
"″" : _("Second"),
"❘" : _("such that"),
"❘" : _("Vertical Bar"),
"≯" : _("Is not greator than"),
"≮Is" : _("not less than"),
"∦" : _("Is not parallel to"),
"≟" : _("Question mark over equal sign"),
"ꞷ" : _("Small letter Omega"),
"∈" : _("is an element of (Membership)"),
"∍" : _("Contains the element"),
"⊂" : _("inclusion sign"),
"⊃" : _("reverse inclusion sign"),
"∩" : _("intersection set"),
"∪" : _("Union set"),
"∅" : _("Empty set"),
"{}" : _("Empty set"),
"⊆" : _("Bar under inclusion sign"),
"⊇" : _("Bar under reverse inclusion") }
		
####### End of Temporary fix #############


class EngineBraille(IBus.Engine, BrailleInputEngine):
	__gtype_name__ = 'EngineSharadaBraille'
	
	def __init__(self):
		super(EngineBraille, self).__init__()
		
		self.__is_invalidate = False
		self.__preedit_string = ""
		self.__lookup_table = IBus.LookupTable.new(10, 0, True, True)
		self.__prop_list = IBus.PropList()
		self.__prop_list.append(IBus.Property(key="test", icon="ibus-local"))
		
		
		# Setting braille input engine
		BrailleInputEngine.__init__(self)
				
		self.set_get_text_before_cursor_callback(self.get_text_before_cursor)
		self.set_delete_text_before_cursor_callback(self.delete_text_before_cursor)
		self.set_insert_text_at_cursor_callback(self.insert_text_at_cursor)
		
		# Creating user configuration directory
		os.makedirs(global_var.user_conf_dir, exist_ok=True)
		
		# User Preferences
		self.pref = preferences.Preferences()
		list_of_available_built_in_languages = self.get_available_built_in_languages()
		list_of_available_liblouis_languages = self.get_available_liblouis_languages()
		self.pref.set_built_in_language_list(list_of_available_built_in_languages)
		self.pref.set_liblouis_language_list(list_of_available_liblouis_languages)
		self.pref.set_on_apply_preferences_callback(self.apply_preferences)
		self.pref.load_preferences_from_file(global_var.user_preferences_file_path)
		
		# User Abbreviations
		self.uam = user_abbreviation_manager.UserAbbreviationManager()
		self.uam.set_on_apply_abbreviations_callback(self.apply_abbreviations)
		self.uam.import_from_file(global_var.abbreviations_file_path)
		self.set_abbreviations(self.uam.get_abbreviations())
	
	
		self.set_notify_language_callback(self.set_notify_language)
		self.set_notify_callback(self.notify)
		
		self.apply_preferences()


	def apply_preferences(self):
		self.set_auto_capitalize_sentence(self.pref.auto_capitalize_sentence)
		self.set_auto_capitalize_line(self.pref.auto_capitalize_line)
		self.set_simple_mode(self.pref.simple_mode)
		self.set_auto_new_line(self.pref.auto_new_line)
		#self.set_speech(self.pref.speech)
		self.set_line_limit(self.pref.line_limit)
		
		self.set_checked_languages_built_in(self.pref.checked_languages_built_in)
		self.set_checked_languages_liblouis(self.pref.checked_languages_liblouis)
		
		self.set_keycode_map(self.pref.get_keycode_map())

		self.set_conventional_braille(self.pref.conventional_braille)
		self.set_one_hand_mode(self.pref.one_hand_mode)
		self.set_one_hand_conversion_delay(self.pref.one_hand_conversion_delay)
		
		self.load_default_language()

		# Saving to file
		self.pref.save_preferences_to_file(global_var.user_preferences_file_path)

	def apply_abbreviations(self):
		abbreviations = self.uam.get_abbreviations()
		self.set_abbreviations(abbreviations)

		# Saving to file
		self.uam.save_to_file(global_var.abbreviations_file_path)


	def notify(self, message, verbose=False):
		#frame = self.label.get_parent()
		#atk_ob = frame.get_accessible()
		#self.label.set_text(message)
		#atk_ob.notify_state_change(Atk.StateType.SHOWING,True);
		if not(verbose):
			speak(message)
		else:
			speak(self.convert_marks_in_text_to_words(message))

	def convert_marks_in_text_to_words(self, text):
		is_uppercase = text.upper() == text;
		result = "";
		for charecter in list(text):
			if (charecter in tts_dictionary):
				if(is_uppercase):
					result = result = result + (", "+tts_dictionary[charecter].upper()+", ");
				else:
					result = result = result + (", "+tts_dictionary[charecter]+", ");
			else:
				result = result + charecter;
		return result;


	def set_notify_language(self,language):
		set_tts_language(language)


	def do_enable (self):
		# Tell the input-context that the engine will utilize
		# surrounding-text:
		self.get_surrounding_text()
		self.do_focus_in(self)

	def do_disable (self):
		pass
	
	def do_focus_out(arg):
		pass

	def do_focus_in(self, arg2=None):
		self.reset()

		
	def do_process_key_event(self, keyval, keycode, state):
		is_press = ((state & IBus.ModifierType.RELEASE_MASK) == 0)
		
		no_control = ((state & IBus.ModifierType.CONTROL_MASK) == 0)
		no_alt = ((state & IBus.ModifierType.META_MASK) == 0)
		no_shift = ((state & IBus.ModifierType.SHIFT_MASK) == 0)
		no_super = ((state & IBus.ModifierType.SUPER_MASK) == 0)
		
		if(is_press and (state & IBus.ModifierType.SUPER_MASK) and (state & IBus.ModifierType.SHIFT_MASK)):
			print("Super mask")
			if(keycode == 25):
				os.system("ibus-braille-preferences &")
			elif(keycode == 30):
				os.system("ibus-braille-user-abbreviation-editor &")
			return True
			
				
		#no_extra_mask = (no_control & no_alt & no_shift & no_super)
		no_extra_mask = (no_control & no_alt & no_super)
		if (not no_extra_mask):
			return False;

		if not is_press:
			#Key Release
			return self.key_released(keycode) # needs hardware_keycode = keycode
		else:
			#Key press
			return self.key_pressed(keycode)



	def load_abbrivation(self):
		self.abbreviations = {}
		try:
			for line in open(abbreviations_file_path,mode='r'):
				self.abbreviations[line.split("  ")[0]] = line.split("  ")[1][:-1]
		except FileNotFoundError:
			pass

	def get_text_before_cursor(self, count):
		surrounding_text = self.get_surrounding_text()
		text = surrounding_text[0].get_text()
		cursor_pos = surrounding_text[1]
		string_up_to_cursor = text[:cursor_pos];
		return string_up_to_cursor
		
	def delete_text_before_cursor(self, count):
		self.delete_surrounding_text(-(count),count);


	def insert_text_at_cursor(self, text):
		self.commit_text(IBus.Text.new_from_string(text))
