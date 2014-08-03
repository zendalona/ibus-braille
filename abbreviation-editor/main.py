#!/usr/bin/env python

import os
from gi.repository import Gtk
home_dir = os.environ['HOME']
data_dir = "/usr/share/ibus-sharada-braille/braille"


class ibus_sharada_braille_ae():
	def __init__ (self,file_list=None):
		self.guibuilder = Gtk.Builder()
		self.guibuilder.add_from_file("/usr/share/ibus-sharada-braille-abbreviation-editor/ui.glade")
		self.window = self.guibuilder.get_object("window1")
		self.guibuilder.connect_signals(self);
		
		
		self.liststore = Gtk.ListStore(str, str)
		self.treeview = self.guibuilder.get_object("treeview")
		self.treeview.set_model(self.liststore)
		
		
		cell = Gtk.CellRendererText(editable=True)
		cell.connect('edited', self.abbreviation_changed, 0)
		col = Gtk.TreeViewColumn("Abbreviation",cell,text = 0)
		self.treeview.append_column(col)

		cell = Gtk.CellRendererText(editable=True)
		cell.connect('edited', self.expansion_changed, 1)
		col = Gtk.TreeViewColumn("Expansion",cell,text = 1)
		self.treeview.append_column(col)
			
		
		
		lang_liststore = Gtk.ListStore(str)
		for line in open("{}/languages.txt".format(data_dir)):
			lang_liststore.append([line[:-1]])
		self.combobox_language = self.guibuilder.get_object("combobox_language")
		self.combobox_language.set_model(lang_liststore)
		renderer_text = Gtk.CellRendererText()
		self.combobox_language.pack_start(renderer_text, True)
		self.combobox_language.add_attribute(renderer_text, "text", 0)			
		
		self.saved = True
			
		self.combobox_language.set_active(0)
		self.window.show()
				
		
	def abbreviation_changed(self, w, changed_raw, new_value, column):
		if(not self.abbreviation_exist(new_value)):
			self.liststore[changed_raw][column] = new_value
			self.saved = False
		else:
			dialog_exist =  Gtk.Dialog("Warning!",self.window,1,("Close",Gtk.ResponseType.YES))
			label = Gtk.Label("Expantion for this abbreviation alredy exists!")
			box = dialog_exist.get_content_area();
			box.add(label)
			dialog_exist.show_all()
			response = dialog_exist.run()
			dialog_exist.destroy()
			

	def expansion_changed(self, w, row, new_value, column):
		self.liststore[row][column] = new_value
	
	def language_changed(self,combo,data=None):
		if(not self.saved):
			dialog =  Gtk.Dialog("Warning!",self.window,1,("Save",Gtk.ResponseType.YES,"Change",Gtk.ResponseType.NO))
			label = Gtk.Label("Do you want to change language without saving ?")
			box = dialog.get_content_area();
			box.add(label)
			dialog.show_all()
			response = dialog.run()
			if response == Gtk.ResponseType.YES:
				self.save(self)
				self.saved = True
			dialog.destroy()
		self.liststore.clear()
		tree_iter = combo.get_active_iter()
		model = combo.get_model()
		self.language = model.get_value(tree_iter,0).split("-")[0]
		self.import_from_file("{}/{}/abbreviations.txt".format(data_dir,self.language))
		
	def quit(self,widget,data=None):
		Gtk.main_quit()
		
	def add(self,widget,data=None):
		dialog =  Gtk.Dialog("New entry",self.window,1,("Add",Gtk.ResponseType.YES,"Cancel",Gtk.ResponseType.NO))
		label = Gtk.Label("Fill entrys with appropriate data \n")
		box = dialog.get_content_area();
		box.add(label)
		table = Gtk.Table(2, 2, True)
		box.add(table)
		
		label_abbreviation = Gtk.Label("Abbreviation")
		entry_abbreviation = Gtk.Entry()
		label_abbreviation.set_mnemonic_widget(entry_abbreviation)
		label_expansion = Gtk.Label("Expansion")
		entry_expansion = Gtk.Entry()
		label_expansion.set_mnemonic_widget(entry_expansion)
		
		table.attach(label_abbreviation,0,1,0,1)
		table.attach(entry_abbreviation,1, 2, 0, 1)
		table.attach(label_expansion, 0,1,1,2)
		table.attach(entry_expansion, 1,2,1,2)
		
		dialog.show_all()
		response = dialog.run()
		if response == Gtk.ResponseType.YES:
			new_value = entry_abbreviation.get_text()
			if (not self.abbreviation_exist(new_value)):
				self.liststore.append([entry_abbreviation.get_text(),entry_expansion.get_text()])
				self.saved = False
			else:
				dialog_exist =  Gtk.Dialog("Warning!",self.window,1,("Skip",Gtk.ResponseType.NO,"Replace",Gtk.ResponseType.YES))
				label = Gtk.Label("Expantion for this abbreviation alredy exists!")
				box = dialog_exist.get_content_area();
				box.add(label)
				dialog_exist.show_all()
				response = dialog_exist.run()
				if response == Gtk.ResponseType.YES:
					self.saved = False
					for row in self.liststore:
						if row[0] == new_value:
							self.liststore.insert_before(row.iter,[entry_abbreviation.get_text(),entry_expansion.get_text()])
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
		dialog =  Gtk.Dialog("Warning!",self.window,1,("No",Gtk.ResponseType.NO,"Yes",Gtk.ResponseType.YES))
		label = Gtk.Label("Clear all entries ?!")
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
		text = open(filename).read()
		skip_all = 0
		replace_all = 0
		for line in text.split("\n"):
			if(len(line.split("  "))>1):
				if (not self.abbreviation_exist(line.split("  ")[0])):
					self.liststore.append(line.split("  "))
				else:
					if (not skip_all and not replace_all):
						dialog =  Gtk.Dialog("Warning!",self.window,1,("Skip",Gtk.ResponseType.NO,"Skip-All",Gtk.ResponseType.NONE,"Replace",Gtk.ResponseType.YES,"Replace-All",Gtk.ResponseType.APPLY))
						label = Gtk.Label("Abbreviation alrady exist :  "+line)
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
								if row[0] == line.split("  ")[0]:
									self.liststore.insert_before(row.iter,line.split("  "))
									self.liststore.remove(row.iter)
									break
						else:
							pass
						dialog.destroy()

					if(replace_all):
						for row in self.liststore:
							if row[0] == line.split("  ")[0]:
								self.liststore.insert_before(row.iter,line.split("  "))
								self.liststore.remove(row.iter)
								break
					self.saved = False
					
				
	def import_(self,widget,data=None):
		open_file = Gtk.FileChooserDialog("Select the file to open",None,Gtk.FileChooserAction.OPEN,buttons=(Gtk.STOCK_OPEN,Gtk.ResponseType.OK))
		open_file.set_current_folder("%s"%(os.environ['HOME']))
		response = open_file.run()
		if response == Gtk.ResponseType.OK:
			self.import_from_file(open_file.get_filename())
		open_file.destroy()
	
	def restore(self,widget,data=None):
		dialog =  Gtk.Dialog("Warning!",self.window,1,("No",Gtk.ResponseType.NO,"Yes",Gtk.ResponseType.YES))
		label = Gtk.Label("Restore default ?!")
		box = dialog.get_content_area();
		box.add(label)
		dialog.show_all()
		response = dialog.run()
		self.saved = False
		if response == Gtk.ResponseType.YES:
			self.liststore.clear()
			dialog.destroy()
			self.import_from_file("{}/{}/abbreviations_default.txt".format(data_dir,self.language))
		else:
			dialog.destroy()

	
	def save_to_file(self,filename):
		file = open(filename,"w")
		for item in self.liststore:
			abb,exp = item
			file.write("{}  {}\n".format(abb,exp))
		file.close()
	
	def export(self,widget,data=None):
		save_file = Gtk.FileChooserDialog("Export abbreviation list ",None,Gtk.FileChooserAction.SAVE,buttons=(Gtk.STOCK_SAVE,Gtk.ResponseType.OK))
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
			

	def save(self,widget,data=None):
		self.save_to_file("{}/{}/abbreviations.txt".format(data_dir,self.language))		
		

		
ibus_sharada_braille_ae()
Gtk.main()
