# vim:set et sts=4 sw=4:
#
# ibus-sharada-braille - The Braille Input Bus project
#
# Copyright (c) 20014-2015 Nalin.x.Linux <Nalin.x.Linux@gmail.com>
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

import gobject
import pango
import os
import ibus
from ibus import keysyms
from ibus import modifier
from espeak import espeak

#Where the data is located
data_dir = "/usr/share/ibus-sharada-braille";

class Engine(ibus.EngineBase):
    def __init__(self, bus, object_path):
        super(Engine, self).__init__(bus, object_path)
        self.pressed_keys = u""
        
        #Key code map #{30:"a",31:"s",32:"d",33:"f",34:"g",35:"h",36:"j",37:"k",38:"l",39:";"}
        
        self.keycode_map = {33:"1",32:"2",31:"3",36:"4",37:"5",38:"6",30:"7",34:"8",35:"9",39:"0"}
        
        #Braille Iter's
        self.braille_letter_map_pos = 0;
        
        #capital switch
        self.capital_switch = 0;

        self.__is_invalidate = False
        self.__preedit_string = u""
        self.__lookup_table = ibus.LookupTable()
        self.__prop_list = ibus.PropList()
        self.__prop_list.append(ibus.Property(u"test", icon = u"ibus-locale"))		

        #Load the first language by default
        self.load_map("malayalam ml")
    
    def do_enable (self):
        # Tell the input-context that the engine will utilize
        # surrounding-text:
        self.get_surrounding_text()
        self.do_focus_in()        
        
    def process_key_event(self, keyval, keycode, state):
		is_press = ((state & modifier.RELEASE_MASK) == 0)
		
		#Key Release
		if not is_press:
			ordered_pressed_keys = self.order_pressed_keys(self.pressed_keys);
			self.pressed_keys = "";
			
			#Move map position to contraction if any
			if ordered_pressed_keys in self.contractions_dict.keys():
				self.braille_letter_map_pos = self.contractions_dict[ordered_pressed_keys];
			
			#Toggle Punctuation
			elif ordered_pressed_keys == "0":
				self.braille_letter_map_pos = 2;
			
			#Expand Abbreviation
			elif ordered_pressed_keys == "7":
				#self.pressed_keys = "";
				surrounding_text = self.get_surrounding_text()
				text = surrounding_text[0].get_text()#.decode('UTF-8')
				cursor_pos = surrounding_text[1]
				string_up_to_cursor = text[:cursor_pos];
				last_word = string_up_to_cursor.split()[-1]
				
								
				#Substitute abbreviation if exist and letter bofore the cursor is not space
				if (last_word in self.abbreviations.keys() and string_up_to_cursor[-1] != " "):
					self.delete_surrounding_text(-(len(last_word)),len(last_word));
					for key,value in self.abbreviations.iteritems():
						if key == last_word:
							self.__commit_string(value)
					#Fixme Why this heck is not working :( ??
					#self.__commit_string(self.abbreviations[last_word.decode('UTF-8')].decode('UTF-8'))

			#Delete Last word
			elif (ordered_pressed_keys == "89"):
				surrounding_text = self.get_surrounding_text()
				text = surrounding_text[0].get_text().decode('UTF-8')
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
				
				#If end is not space, delete length of last word	
				else:
					count = len(string_up_to_cursor.split()[-1])
					self.delete_surrounding_text(-(count),count);	


			#Delete Last letter
			elif (ordered_pressed_keys == "9"):
				self.delete_surrounding_text(-1,1);	

			#Toggle capital switch
			elif (ordered_pressed_keys == "8" and self.language == "english"):
				self.capital_switch = 1;					
				
			else:
				value = self.map[ordered_pressed_keys][self.braille_letter_map_pos]
				if (self.capital_switch == 1):
					value = value.upper()
					self.capital_switch = 0;
				self.__commit_string(value);
				self.braille_letter_map_pos = 1;
			return False


		#Key press
		else:
			#self.__commit_string(keycode)
			self.get_surrounding_text()
			if keycode in self.keycode_map.keys():
				#Store the letters
				self.pressed_keys  += self.keycode_map[keycode];
				return True
			else:
				if keyval == keysyms.space:
					self.braille_letter_map_pos = 0;
				else:
					if (keycode == 119):
						if self.language == "malayalam":
							self.load_map("english en")
						else:
							self.load_map("malayalam ml")	
				return False
		
    def load_map(self,language_with_code):
		self.language = language_with_code.split()[0]
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
				if "~" not in text_file:
					submap_number += 1;
					self.append_sub_map(text_file,submap_number);
					self.contractions_dict[text_file[:-4]] = submap_number-1;
		  
		#Load abbreviations if exist
		self.load_abbrivation();
		


	
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
		for key in ["1","2","3","4","5","6","7","8","9","0"]:
			if key in pressed_keys:
				ordered += key;
		return ordered;    

    def __commit_string(self, text):
        self.commit_text(ibus.Text(text))
