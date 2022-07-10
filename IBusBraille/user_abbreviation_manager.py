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

from IBusBraille.textview import BrailleInputTextView
from IBusBraille import global_var

from IBusBraille import localization
_ = localization._

import json


class UserAbbreviationManager():
	def __init__ (self,file_list=None):
		self.guibuilder = Gtk.Builder()
		self.guibuilder.add_from_file(global_var.data_dir + "user_abbreviation_manager.glade")
		self.window = self.guibuilder.get_object("window")
		self.guibuilder.connect_signals(self);
		
		
		self.liststore = Gtk.ListStore(str, str)
		self.treeview = self.guibuilder.get_object("treeview")
		self.treeview.set_model(self.liststore)
		
		cell = Gtk.CellRendererText(editable=False)
		col = Gtk.TreeViewColumn(_("Abbreviation"),cell,text = 0)
		self.treeview.append_column(col)

		cell = Gtk.CellRendererText(editable=False)
		col = Gtk.TreeViewColumn(_("Expansion"),cell,text = 1)
		self.treeview.append_column(col)	

	def on_window_delete_event(self,widget, data=None):
		self.window.hide()
		self.apply_abbreviations()
		return True
	
	def set_braille_view_copy_object(self,obj):
		self.copy_object = obj;
		
	def get_abbreviations(self):
		return {abb : exp for abb, exp in self.liststore}

	def set_on_apply_abbreviations_callback(self, function):
		self.apply_abbreviations = function
		
	def add(self,widget,data=None):
		dialog =  Gtk.Dialog(_("New entry"),self.window,1,(_("Add"),Gtk.ResponseType.YES,_("Cancel"),Gtk.ResponseType.NO))
		label = Gtk.Label(_("Fill entrys with appropriate data \n"))
		box = dialog.get_content_area();
		box.add(label)
		table = Gtk.Table(3, 4, True)
		box.add(table)
		
		entry_abbreviation = Gtk.TextView()
		###entry_abbreviation = BrailleInputTextView()
		### entry_abbreviation.set_variables_from_object(self.copy_object)
		entry_abbreviation.set_accepts_tab(False)
		###entry_abbreviation.set_single_line_mode(True)
		label_abbreviation = Gtk.Label(_("Abbreviation"))
		label_abbreviation.set_mnemonic_widget(entry_abbreviation)

		seperator = Gtk.HSeparator()
		seperator.set_vexpand(True)

		
		###def on_expansion_focused(widget,data):
		###	entry_expansion.set_variables_from_object(entry_abbreviation)

		
		entry_expansion = Gtk.TextView()
		###entry_expansion = BrailleInputTextView()
		###entry_expansion.set_variables_from_object(self.copy_object)
		entry_expansion.set_accepts_tab(False)
		entry_expansion.set_vexpand(True)
		label_expansion = Gtk.Label(_("Expansion"))
		label_expansion.set_mnemonic_widget(entry_expansion)
		label_expansion.set_hexpand(False)

		###entry_expansion.connect("focus-in-event", on_expansion_focused)
		
		table.attach(label_abbreviation,0,1,0,1)
		table.attach(entry_abbreviation,1, 4, 0, 1)
		table.attach(seperator, 0, 4, 1,2)
		table.attach(label_expansion, 0,1,2,3)
		table.attach(entry_expansion, 1,4,2,3)
		
		dialog.show_all()
		response = dialog.run()
		if response == Gtk.ResponseType.YES:

			entry_buffer = entry_abbreviation.get_buffer()
			start,end = entry_buffer.get_bounds()
			new_abbreviation = entry_buffer.get_text(start, end, False)

			expansion_buffer = entry_expansion.get_buffer()
			start,end = expansion_buffer.get_bounds()
			new_expansion = expansion_buffer.get_text(start, end, False)

			if (not self.abbreviation_exist(new_abbreviation)):
				self.liststore.append([new_abbreviation,new_expansion])
				self.saved = False
			else:
				dialog_exist =  Gtk.Dialog(_("Warning!"),self.window,1,(_("Skip"),Gtk.ResponseType.NO,_("Replace"),Gtk.ResponseType.YES))
				label = Gtk.Label(_("Expansion for this abbreviation already exists!"))
				box = dialog_exist.get_content_area();
				box.add(label)
				dialog_exist.show_all()
				response = dialog_exist.run()
				if response == Gtk.ResponseType.YES:
					self.saved = False
					for row in self.liststore:
						if row[0] == new_abbreviation:
							self.liststore.insert_before(row.iter,[new_abbreviation,new_expansion])
							self.liststore.remove(row.iter)
							break
				dialog_exist.destroy()
		dialog.destroy()	

	def abbreviation_exist(self,value):
		flag = 0
		for item in self.liststore:
			abb,exp = item
			if (abb == value):
				flag = 1
				break
		return flag
		
		
	def clear_all(self,widget,data=None):
		dialog =  Gtk.Dialog(_("Warning!"),self.window,1,(_("No"),Gtk.ResponseType.NO,_("Yes"),Gtk.ResponseType.YES))
		label = Gtk.Label(_("Clear all entries ?"))
		box = dialog.get_content_area();
		box.add(label)
		dialog.show_all()
		response = dialog.run()
		if response == Gtk.ResponseType.YES:
			self.liststore.clear()
		dialog.destroy()			

	def remove(self,widget,data=None):
		selection = self.treeview.get_selection()
		(model, pathlist) = selection.get_selected_rows()
		self.saved = False
		for path in pathlist:
			tree_iter = model.get_iter(path)
			value = model.get_value(tree_iter,0)
			model.remove(tree_iter)
	
	def import_from_file(self,filename):
		self.saved = True
		try:
			with open(filename) as f:
				new_abbreviations = json.load(f)
		except:
			return
		skip_all = 0
		replace_all = 0		
		
		for abb, exp in new_abbreviations.items():
			if (not self.abbreviation_exist(abb)):
				self.liststore.append([abb, exp])
			else:
				if (not skip_all and not replace_all):
					dialog =  Gtk.Dialog(_("Warning!"),None,1,(_("Skip"),Gtk.ResponseType.NO,
					_("Skip-All"),Gtk.ResponseType.NONE,_("Replace"),Gtk.ResponseType.YES,
					_("Replace-All"),Gtk.ResponseType.APPLY))
					label = Gtk.Label(_("Abbreviation ")+abb+_(" already exist with expansion ")+exp)
					box = dialog.get_content_area();
					box.add(label)
					dialog.show_all()
					response = dialog.run()
					if(response == Gtk.ResponseType.NONE):
						skip_all = 1
					elif (response == Gtk.ResponseType.APPLY):
						replace_all = 1
					elif (response == Gtk.ResponseType.YES):
						for row in self.liststore:
							if row[0] == abb:
								self.liststore.insert_before(row.iter,[abb, exp])
								self.liststore.remove(row.iter)
								break
					else:
						pass
					dialog.destroy()

				if(replace_all):
					for row in self.liststore:
						if row[0] == abb:
							self.liststore.insert_before(row.iter,[abb, exp])
							self.liststore.remove(row.iter)
							break
				self.saved = False
				
	def import_(self,widget,data=None):
		open_file = Gtk.FileChooserDialog(_("Select the file to open"),None,Gtk.FileChooserAction.OPEN,buttons=(_("Open"),Gtk.ResponseType.OK))
		open_file.set_current_folder("%s"%(os.environ['HOME']))
		response = open_file.run()
		if response == Gtk.ResponseType.OK:
			self.import_from_file(open_file.get_filename())
		open_file.destroy()
	
	def save_to_file(self,filename):
		#file = open(filename,"w")
		for item in self.liststore:
			abb,exp = item
		#	file.write("{}  {}\n".format(abb,exp))
		#file.close()
		
		abb_dict = {abb: exp for abb, exp in self.liststore}
		with open(filename, 'w') as f:
			json.dump(abb_dict, f)
	
	def export(self,widget,data=None):
		save_file = Gtk.FileChooserDialog(_("Export abbreviation list "),None,Gtk.FileChooserAction.SAVE,buttons=(_("Save"),Gtk.ResponseType.OK))
		save_file.set_current_folder("{}".format(os.environ['HOME']))
		save_file.set_do_overwrite_confirmation(True);
		filter = Gtk.FileFilter()
		filter.add_pattern("*.txt")
		filter.add_pattern("*.text")
		save_file.add_filter(filter)
		response = save_file.run()
		if response == Gtk.ResponseType.OK:
			self.save_to_file(save_file.get_filename())
		save_file.destroy()

	def show(self):
		self.window.show()
