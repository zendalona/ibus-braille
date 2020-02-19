# vim:set et sts=4 sw=4:
#
# ibus-sharada-braille - The Braille Input Bus project
#
# Copyright (c) 2014-2015 Nalin.x.Linux <Nalin.x.Linux@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.



# for python2
from __future__ import print_function

import os
import configparser
from gi.repository import GLib
from gi.repository import IBus
from gi.repository import Pango

#Liblouis
import louis

# For 3 dot system
from threading import Timer

 
keysyms = IBus

#Where the data is located
data_dir = "/usr/share/ibus-braille";

home_dir = os.environ['HOME']


########################## Temporary fix ###################
espeak_available = 0
speechd_available = 0;
try:
	import speechd
	speechd_available = 1;
	client = speechd.Client()
except:
	try:
		from espeak import espeak
		espeak_available = 1;
	except:
		espeak_available = 0;


def speak(text):
	if(speechd_available):
		client.cancel()
		client.speak(text);
	elif (espeak_available):
		espeak.cancel()
		espeak.synth(text)
	else:
		print("No tts api available!(python3-espeak/python3-speechd)");

def set_language(language):
	print(language)
	if(speechd_available):
		client.set_language(language)
	elif (espeak_available):
		espeak.set_voice(language)
	else:
		pass
####### End of Temporary fix #############


class EngineSharadaBraille(IBus.Engine):
	__gtype_name__ = 'EngineSharadaBraille'
	
	def __init__(self):
		super(EngineSharadaBraille, self).__init__()
		self.pressed_keys = u""
		
		self.liblouis_language_table_conversion_dict = {}
		for line in open(data_dir+"/braille/liblouis_language_list.txt").readlines():
			language, tablename = line[:-1].split(" ");
			self.liblouis_language_table_conversion_dict[language] = tablename;

		Config = configparser.ConfigParser()
		try:
			Config.read("{}/isb.cfg".format(home_dir))
			self.checked_languages = Config.get('cfg',"checked_languages").split(",")
			self.checked_languages_liblouis = Config.get('cfg',"checked_languages_liblouis").split(",")
			self.simple_mode = int(Config.get('cfg',"simple-mode"))
			self.keycode_map = {}
			for key,value in {"dot-1":"1","dot-2":"2","dot-3":"3","dot-4":"4","dot-5":"5",
			"dot-6":"6","dot-7":"7","dot-8":"8","punctuation_key":"0","capitol_switch_key":"c",
			"letter_deletion_key":"9","abbreviation_key":"a","one_hand_skip_key":"o"}.items():
				self.keycode_map[int(Config.get('cfg',key))] = value
			self.key_to_switch_between_languages = int(Config.get('cfg',"switch_between_languages"))
			self.list_switch_key = int(Config.get('cfg',"list_switch_key"))
			self.language_iter = int(Config.get('cfg',"default-language"))
			self.language_iter_liblouis = int(Config.get('cfg',"default-language-liblouis"))
			self.conventional_braille = int(Config.get('cfg',"conventional-braille"))
			self.liblouis_mode = int(Config.get('cfg',"liblouis-mode"))
			self.one_hand_mode = int(Config.get('cfg',"one-hand-mode"))
			self.one_hand_conversion_delay = int(Config.get('cfg',"one-hand-conversion-delay"))*1/1000;
		except:
			self.checked_languages = ["english-en","hindi-hi"]
			self.checked_languages_liblouis = ["English-US-Grade-1", "English-US-Grade-2"]
			self.simple_mode =  0
			self.keycode_map = {33:"1",32:"2",31:"3",36:"4",37:"5",38:"6",44:"7",52:"8",30:"a",34:"c",35:"9",39:"0"}
			self.key_to_switch_between_languages = 119
			self.list_switch_key = 56
			self.language_iter = 0
			self.language_iter_liblouis = 0
			self.conventional_braille = False;
			self.one_hand_mode = False
			self.one_hand_conversion_delay = 0.5
			self.liblouis_mode = True;

		self.language_liblouis = self.liblouis_language_table_conversion_dict[self.checked_languages_liblouis[self.language_iter_liblouis]]


		self.conventional_braille_dot_4 = False;
		self.conventional_braille_dot_4_pass = False;
		self.conventional_braille_dot_3 = False;

		#Three dot braille
		self.three_dot_pos = 1;

		#Braille Iter's
		self.braille_letter_map_pos = 0;
		
		#capital switch
		self.capital_switch = 0;
		self.capital = 0
		
		self.__is_invalidate = False
		self.__preedit_string = ""
		self.__lookup_table = IBus.LookupTable.new(10, 0, True, True)
		self.__prop_list = IBus.PropList()
		self.__prop_list.append(IBus.Property(key="test", icon="ibus-local"))
		
		#Load the first language by default
		if (self.liblouis_mode):
			language_name = self.checked_languages_liblouis[self.language_iter_liblouis];
			self.language_liblouis = self.liblouis_language_table_conversion_dict[language_name]
			speak("{} Loaded!".format(language_name));
		else:
			self.load_built_in_table(self.checked_languages[self.language_iter])


		# Used with liblouis based engine
		self.last_appeared_word_length = 0;
		self.louis_typing_word_combinations = "";


	def do_enable (self):
		# Tell the input-context that the engine will utilize
		# surrounding-text:
		self.get_surrounding_text()
		self.do_focus_in(self)        
	
	def do_process_key_event(self, keyval, keycode, state):
		is_press = ((state & IBus.ModifierType.RELEASE_MASK) == 0)
		
		no_control = ((state & IBus.ModifierType.CONTROL_MASK) == 0)
		no_alt = ((state & IBus.ModifierType.META_MASK) == 0)
		no_shift = ((state & IBus.ModifierType.SHIFT_MASK) == 0)
		no_super = ((state & IBus.ModifierType.SUPER_MASK) == 0)
				
		no_extra_mask = (no_control & no_alt & no_shift & no_super)
		if (not no_extra_mask):
			return False;

		#if (not is_control and not is_alt and not is_shift and not is_super):
		#	return False;
		
		#Key Release
		if not is_press:
			ordered_pressed_keys = self.order_pressed_keys(self.pressed_keys);
			
			if (ordered_pressed_keys == "3" and self.conventional_braille):
				self.conventional_braille_dot_3 = True;
				self.old_braille_letter_map_pos = self.braille_letter_map_pos

			#Move map position to contraction if any
			if (self.liblouis_mode == False):
				if (ordered_pressed_keys in self.contractions_dict.keys()
				and self.one_hand_mode == False):
					self.braille_letter_map_pos = self.contractions_dict[ordered_pressed_keys];
			
			#Toggle Punctuation
			elif ordered_pressed_keys == "0":
				self.braille_letter_map_pos = 2;
			
			#Expand Abbreviation
			elif (ordered_pressed_keys == "a" and self.simple_mode == 0):
				#self.pressed_keys = "";
				surrounding_text = self.get_surrounding_text()
				text = surrounding_text[0].get_text()
				cursor_pos = surrounding_text[1]
				string_up_to_cursor = text[:cursor_pos];
				last_word = string_up_to_cursor.split()[-1]
				
								
				#Substitute abbreviation if exist and letter bofore the cursor is not space
				if (last_word in self.abbreviations.keys() and string_up_to_cursor[-1] != " "):
					self.delete_surrounding_text(-(len(last_word)),len(last_word));
					for key,value in self.abbreviations.items():
						if key == last_word:
							self.__commit_string(value)
					#Fixme Why this heck is not working :( ??
					#self.__commit_string(self.abbreviations[last_word.decode('UTF-8')].decode('UTF-8'))

			#Delete Last word
			elif (ordered_pressed_keys == "c9"):
				surrounding_text = self.get_surrounding_text()
				text = surrounding_text[0].get_text()
				cursor_pos = surrounding_text[1]
				string_up_to_cursor = text[:cursor_pos];
				
				#If end is space, then count backword till a space found  			
				if (string_up_to_cursor[-1] == " "):
					count = 0
					char_found = 0;
					
					for item in string_up_to_cursor[::-1]:
						if (item != " "):
							char_found = 1;
						if (item == " " and char_found == 1):
							break;
						count += 1
					self.delete_surrounding_text(-(count),count);
					speak(string_up_to_cursor[-(count):]+"Deleted")	
				
				#If end is not space, delete length of last word	
				else:
					count = len(string_up_to_cursor.split()[-1])
					self.delete_surrounding_text(-(count),count);
					speak(string_up_to_cursor.split()[-1]+"Deleted")	


			#Delete Last letter
			elif (ordered_pressed_keys == "9"):
				surrounding_text = self.get_surrounding_text()
				text = surrounding_text[0].get_text()
				speak(text[-1:]+"Deleted")
				self.delete_surrounding_text(-1,1);	

			#Toggle capital switch
			elif (ordered_pressed_keys == "c" and self.language == "english"):
				if (self.capital_switch == 1):
					if (self.capital == False):
						self.capital = True
						speak("Caps Lock On!")
					else:
						self.capital = False
						speak("Caps Lock Off!")
						self.capital_switch = 0;
				self.capital_switch = 1;

			elif( self.conventional_braille == True and
				ordered_pressed_keys == "4" and self.liblouis_mode == False):
					self.conventional_braille_dot_4 = True;
				
			else:
				if (len(ordered_pressed_keys) > 0):
					if (self.liblouis_mode):
						sum = 0
						for i in ordered_pressed_keys:
							sum = sum + pow(2,int(i)-1);
						pressed_dots = 0x2800 + sum

						# Adding last typed combination to list
						self.louis_typing_word_combinations = self.louis_typing_word_combinations + chr(pressed_dots)

						# Deleting last appeared word
						self.delete_surrounding_text(-(self.last_appeared_word_length),self.last_appeared_word_length);

						# Translating typing combinations
						word = louis.backTranslate(['unicode.dis',self.language_liblouis],self.louis_typing_word_combinations,None,0)
						result = word[0];

						# Storing length of result for deleting on
						self.last_appeared_word_length = len(result);

						# Commiting resut
						self.__commit_string(result);

					else:
						if (self.one_hand_mode):
							if (self.three_dot_pos == 1 and self.pressed_keys != ""):
								if (self.pressed_keys == "o"):
									self.pressed_keys = "";
								self.three_dot_pos = 2;
								t = Timer(self.one_hand_conversion_delay, self.three_dot_do_commit)
								t.start()
							return False

						try:
							value = self.map[ordered_pressed_keys][self.braille_letter_map_pos]
						except:
							value = "";
						if (self.capital_switch == 1 or self.capital == 1):
							value = value.upper()
							self.capital_switch = 0;
						self.__commit_string(value);
						self.conventional_braille_dot_4_pass = False;
						self.conventional_braille_dot_3 = False;
						if (self.conventional_braille == 1 and self.conventional_braille_dot_4):
							self.conventional_braille_dot_4 = False;
							self.__commit_string(self.map["4"][self.braille_letter_map_pos]);
							self.conventional_braille_dot_4_pass = True;
						self.braille_letter_map_pos = 1;
			self.pressed_keys = "";
			return False


		#Key press
		else:
			self.get_surrounding_text()
			if keycode in self.keycode_map.keys():
				#Store the letters
				if (self.one_hand_mode):
					if (self.three_dot_pos == 1):
						self.pressed_keys  += self.keycode_map[keycode];
					else:
						self.pressed_keys  += str(int(self.keycode_map[keycode])+3);
				else:
					self.pressed_keys  += self.keycode_map[keycode];
				return True
			else:

				self.last_appeared_word_length = 0;
				self.louis_typing_word_combinations = "";

				if (keyval == keysyms.space):
					self.braille_letter_map_pos = 0;
					if(not self.liblouis_mode):
						if (self.conventional_braille == True ):
							if(self.conventional_braille_dot_3):
								self.__commit_string(self.map["3"][self.old_braille_letter_map_pos]);
								self.conventional_braille_dot_3 = False;
							if(self.conventional_braille_dot_4):
								self.conventional_braille_dot_4 = False;
								self.__commit_string(self.map["4"][self.braille_letter_map_pos]);
							elif (self.conventional_braille_dot_4_pass == True):
								self.conventional_braille_dot_4_pass = False
								self.__commit_string(self.map["8"][self.braille_letter_map_pos]);
								return True
				else:
					if (keycode == self.key_to_switch_between_languages):
						if(self.liblouis_mode):
							self.language_iter_liblouis=(self.language_iter_liblouis+1)%len(self.checked_languages_liblouis);
							language_name = self.checked_languages_liblouis[self.language_iter_liblouis];
							self.language_liblouis = self.liblouis_language_table_conversion_dict[language_name]
							speak("{} Loaded!".format(language_name));
						else:
							self.language_iter=(self.language_iter+1)%len(self.checked_languages);
							self.load_built_in_table(self.checked_languages[self.language_iter])
					
					if (keycode == self.list_switch_key):
						self.braille_letter_map_pos = (self.braille_letter_map_pos+1)%2

				return False
	
	def load_built_in_table(self,language_with_code):
		self.language = language_with_code.split("-")[0]
		set_language(language_with_code.split("-")[1])
		print ("loading Map for language : %s" %self.language)
		self.map = {}
		submap_number = 1;
		self.append_sub_map("beginning.txt",submap_number);
		submap_number = 2;
		self.append_sub_map("middle.txt",submap_number);
		submap_number = 3;
		self.append_sub_map("punctuations.txt",submap_number);
		
		#Contraction dict 
		self.contractions_dict = {};
		
		#load each contractions to map
		for text_file in os.listdir("%s/braille/%s/"%(data_dir,self.language)):
			if text_file not in ["beginning.txt","middle.txt","abbreviations.txt","abbreviations_default.txt","punctuations.txt","help.txt"]:
				if (self.simple_mode == 0 and "~" not in text_file):
					submap_number += 1;
					self.append_sub_map(text_file,submap_number);
					self.contractions_dict[text_file[:-4]] = submap_number-1;
		  
		#Load abbreviations if exist
		self.load_abbrivation();
		speak("{} Loaded!".format(self.language));
		


	def append_sub_map(self,filename,submap_number):
		print("Loading sub map file for : %s with sn : %d " % (filename,submap_number))	
		for line in open("%s/braille/%s/%s"%(data_dir,self.language,filename),"r"):
			if (line.split(" ")[0]) in self.map.keys():
				self.map[line.split(" ")[0]].append(line.split(" ")[1][:-1])
				if len(self.map[line.split(" ")[0]]) != submap_number:
					print("Repeated on : ",line.split(" ")[0])
			else:
				list=[];
				for i in range (1,submap_number):
					list.append(" ");
				list.append(line.split(" ")[1][:-1]);
				self.map[line.split(" ")[0]] = list;
		
		for key in self.map.keys():
			if len(self.map[key]) < submap_number:
				self.map[key].append(" ");

	def load_abbrivation(self):
		self.abbreviations = {}
		try:
			for line in open("%s/braille/%s/abbreviations.txt"%(data_dir,self.language),mode='r'):
				self.abbreviations[line.split("  ")[0]] = line.split("  ")[1][:-1]
		except FileNotFoundError:
			pass

	def order_pressed_keys(self,pressed_keys):
		ordered = ""
		#["g","f","d","s","h","j","k","l","a",";"]
		for key in ["1","2","3","4","5","6","7","8","a","c","9","0","o"]:
			if key in pressed_keys:
				ordered += key;
		return ordered;    

	def __commit_string(self, text):
		self.commit_text(IBus.Text.new_from_string(text))
		if (len(text) > 1 or self.liblouis_mode):
			speak(text)

	def three_dot_do_commit(self):
		print("Commiting and Reverting")
		self.three_dot_pos = 1;
		ordered_pressed_keys = self.order_pressed_keys(self.pressed_keys);
		self.pressed_keys = ""
		try:
			value = self.map[ordered_pressed_keys][self.braille_letter_map_pos]
			self.__commit_string(value);
			self.braille_letter_map_pos = 1
		except:
			pass
