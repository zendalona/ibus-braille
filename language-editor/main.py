#!/usr/bin/env python

import os
import shutil
import configparser
from gi.repository import Gtk
home_dir = os.environ['HOME']
data_dir = "/usr/share/ibus-sharada-braille/braille"


class page(Gtk.ScrolledWindow):
	def __init__(self,name,language,key_dict):
		self.key_dict = key_dict
		self.language = language
		Gtk.ScrolledWindow.__init__(self)
		self.filename = name
		
		self.liststore = Gtk.ListStore(str, str)
		self.treeview = Gtk.TreeView()
		self.treeview.set_model(self.liststore)
		
		
		self.pressed_keys = ""
		cell = Gtk.CellRendererText(editable=True)
		cell.connect('edited', self.key_combination_changed, 0)
		
		cell.connect("editing-started",self.editingKey,0)		
		
		col = Gtk.TreeViewColumn("key-combination",cell,text = 0)
		self.treeview.append_column(col)

		cell = Gtk.CellRendererText(editable=True)
		cell.connect('edited', self.value_changed, 1)
		col = Gtk.TreeViewColumn("Value",cell,text = 1)
		self.treeview.append_column(col)
		
		self.import_from_file(data_dir+"/"+self.language+"/"+name)
	
	def editingKey(self, cell, editable, path, treeModel):
		editable.connect('key-press-event', self.kbKeyPressed)
		editable.connect('key-release-event', self.kbKeyReleased)
		
	def kbKeyPressed(self, editable, event):
		hardware_keycode = int(event.hardware_keycode)-8
		value = ""
		try:
			value = self.key_dict[hardware_keycode]
		except:
			value = ""
		self.pressed_keys = self.pressed_keys + value

	def kbKeyReleased(self, editable, event):
		if (self.pressed_keys != ""):
			orderd = ""
			for item in ["1","2","3","4","5","6","7"]:
				if item in self.pressed_keys:
					orderd = orderd + item
			editable.set_text(orderd)
			self.pressed_keys = ""
		
		
			

	def import_from_file(self,filename):
		try:
			text = open(filename).read()
		except:
			file = open(filename,'w')
			file.close()
			text = ""
		skip_all = 0
		replace_all = 0
		for line in text.split("\n"):
			if(len(line.split(" "))>1):
				if (not self.key_combination_exist(line.split(" ")[0])):
					self.liststore.append(line.split(" "))
				else:
					if (not skip_all and not replace_all):
						dialog =  Gtk.Dialog("Warning!",None,1,("Skip",Gtk.ResponseType.NO,"Skip-All",Gtk.ResponseType.NONE,"Replace",Gtk.ResponseType.YES,"Replace-All",Gtk.ResponseType.APPLY))
						label = Gtk.Label("key-combination already exist :  "+line)
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
								if row[0] == line.split(" ")[0]:
									self.liststore.insert_before(row.iter,line.split(" "))
									self.liststore.remove(row.iter)
									break
						else:
							pass
						dialog.destroy()

					if(replace_all):
						for row in self.liststore:
							if row[0] == line.split(" ")[0]:
								self.liststore.insert_before(row.iter,line.split(" "))
								self.liststore.remove(row.iter)
								break
					self.saved = False
		self.treeview.show()
		self.add(self.treeview)

	def key_combination_exist(self,value):
		flag = 0
		for item in self.liststore:
			abb,exp = item
			if (abb == value):
				flag = 1
				break
		return flag


	def key_combination_changed(self, w, changed_raw, new_value, column):
		if(not self.key_combination_exist(new_value)):
			self.liststore[changed_raw][column] = new_value
			self.saved = False
		else:
			dialog_exist =  Gtk.Dialog("Warning!",None,1,("Close",Gtk.ResponseType.YES))
			label = Gtk.Label("Key-Combination already exists!")
			box = dialog_exist.get_content_area();
			box.add(label)
			dialog_exist.show_all()
			response = dialog_exist.run()
			dialog_exist.destroy()
			

	def value_changed(self, w, row, new_value, column):
		self.liststore[row][column] = new_value		
		

class ibus_sharada_braille_le():
	def __init__ (self,file_list=None):
		self.guibuilder = Gtk.Builder()
		self.guibuilder.add_from_file("/usr/share/ibus-sharada-braille-language-editor/ui.glade")
		self.window = self.guibuilder.get_object("window1")
		self.guibuilder.connect_signals(self);
		
		self.notebook = self.guibuilder.get_object("notebook")
		self.black_list = []
		
		self.key_dict = {}
		self.config = configparser.ConfigParser()
		if (self.config.read("{}/isb.cfg".format(home_dir)) == []):
			self.key_dict = { 33:"1",32:"2",31:"3",36:"4",37:"5",38:"6",34:"7"}
		else:
			self.key_dict[int(self.config.get('cfg',"dot-1"))] = "1"
			self.key_dict[int(self.config.get('cfg',"dot-2"))] = "2"
			self.key_dict[int(self.config.get('cfg',"dot-3"))] = "3"
			self.key_dict[int(self.config.get('cfg',"dot-4"))] = "4"
			self.key_dict[int(self.config.get('cfg',"dot-5"))] = "5"
			self.key_dict[int(self.config.get('cfg',"dot-6"))] = "6"
			self.key_dict[int(self.config.get('cfg',"capitol_switch_key"))] = "7"				

		self.lang_liststore = Gtk.ListStore(str)
		for line in open("{}/languages.txt".format(data_dir)):
			self.lang_liststore.append([line[:-1]])
		self.combobox_language = self.guibuilder.get_object("combobox_language")
		self.combobox_language.set_model(self.lang_liststore)
		renderer_text = Gtk.CellRendererText()
		self.combobox_language.pack_start(renderer_text, True)
		self.combobox_language.add_attribute(renderer_text, "text", 0)			
		
		self.saved = True
			
		self.combobox_language.set_active(0)
		self.notebook.show();
		self.window.show()

	def remove_selected_language(self,widget,data=None):
		iter = self.combobox_language.get_active_iter()
		item = self.lang_liststore.get_value(iter,0)
		shutil.rmtree(data_dir+"/"+item.split("-")[0])
		self.lang_liststore.remove(iter)
		file = open("{}/languages.txt".format(data_dir),"w")
		for raw in self.lang_liststore:
			file.write(raw[0]+"\n")
		file.close()
		self.combobox_language.set_active(0)

	
	def add_new_language(self,widget,data=None):
		dialog =  Gtk.Dialog("New entry",self.window,1,("Add",Gtk.ResponseType.YES,"Cancel",Gtk.ResponseType.NO))
		label = Gtk.Label("Please enter the language name \n with espeak voice varient (eg english-en)")
		box = dialog.get_content_area();
		box.add(label)
		
		entry = Gtk.Entry()
		label.set_mnemonic_widget(entry)
		box.add(entry)

		
		dialog.show_all()
		response = dialog.run()
		if response == Gtk.ResponseType.YES:
			new_value = entry.get_text()
			exist = 0
			pos = 0			
			for row in self.lang_liststore:
				if row[0] == new_value:
					exist = 1
					break;
				pos = pos + 1
			if(exist):
				dialog_exist =  Gtk.Dialog("Warning!",self.window,1,("Close",Gtk.ResponseType.YES))
				label = Gtk.Label("Language already exists!")
				box = dialog_exist.get_content_area();
				box.add(label)
				dialog_exist.show_all()
				response = dialog_exist.run()
				dialog_exist.destroy()
			else:
				os.mkdir(data_dir+"/"+new_value.split("-")[0])
				file = open("{}/languages.txt".format(data_dir),"a")
				file.write(new_value)
				self.lang_liststore.append([new_value])
				self.combobox_language.set_active(pos)
			dialog.destroy()
		
				
	
	def language_changed(self,combo,data=None):
		if(not self.saved):
			dialog =  Gtk.Dialog("Warning!",self.window,1,("Save",Gtk.ResponseType.YES,"Change",Gtk.ResponseType.NO))
			label = Gtk.Label("Do you want to change language without saving ?")
			box = dialog.get_content_area();
			box.add(label)
			dialog.show_all()
			response = dialog.run()
			if response == Gtk.ResponseType.YES:
				#self.save(self)
				self.saved = True
			dialog.destroy()
			
		tree_iter = combo.get_active_iter()
		if (tree_iter == None):
			return
		model = combo.get_model()
		self.language = model.get_value(tree_iter,0).split("-")[0]
		
		for i in range(0,len(self.black_list)):
			self.notebook.remove_page(-1)
		
		self.black_list = ['help.txt','abbreviations.txt','abbreviations_default.txt']
		for item in ['beginning.txt','middle.txt','punctuations.txt']+os.listdir("/usr/share/ibus-sharada-braille/braille/"+self.language+"/"):
			if item not in self.black_list:
				label = Gtk.Label(item)
				print(item)
				sw = page(item,self.language,self.key_dict)
				sw.show()
				self.notebook.append_page(sw,label);
				self.black_list.append(item)
	
	def add_map(self,widget,data=None):
		dialog =  Gtk.Dialog("New entry",self.window,1,("Add",Gtk.ResponseType.YES,"Cancel",Gtk.ResponseType.NO))
		label = Gtk.Label("Please enter the map name ")
		box = dialog.get_content_area();
		box.add(label)
		
		entry = Gtk.Entry()
		label.set_mnemonic_widget(entry)
		box.add(entry)

		dialog.show_all()
		response = dialog.run()
		if response == Gtk.ResponseType.YES:
			map_name = entry.get_text()
			map_name = map_name + ".txt"
			if map_name not in self.black_list:
				label = Gtk.Label(map_name)
				sw = page(map_name,self.language,self.key_dict)
				sw.show()
				self.notebook.append_page(sw,label);
				self.black_list.append(map_name)
		dialog.destroy()
	
	def remove_map(self,widget,data=None):
		pagenum = self.notebook.get_current_page()
		if pagenum > 2:
			object = self.notebook.get_nth_page(pagenum)
			os.remove("{}/{}/{}".format(data_dir,self.language,object.filename))
			self.notebook.remove_page(pagenum)


	def add(self,widget,data=None):
		dialog =  Gtk.Dialog("New entry",self.window,1,("Add",Gtk.ResponseType.YES,"Cancel",Gtk.ResponseType.NO))
		label = Gtk.Label("Fill entrys with appropriate data \n")
		box = dialog.get_content_area();
		box.add(label)
		table = Gtk.Table(2, 2, True)
		box.add(table)
		
		label_abbreviation = Gtk.Label("Key-Combination")
		entry_abbreviation = Gtk.Entry()
		label_abbreviation.set_mnemonic_widget(entry_abbreviation)
		label_expansion = Gtk.Label("Value")
		entry_expansion = Gtk.Entry()
		label_expansion.set_mnemonic_widget(entry_expansion)
		
		self.pressed_keys = ""
		def kbKeyPressed(editable, event):
			hardware_keycode = int(event.hardware_keycode)-8
			value = ""
			try:
				value = self.key_dict[hardware_keycode]
			except:
				value = ""
			self.pressed_keys = self.pressed_keys + value

		def kbKeyReleased(editable, event):
			if (self.pressed_keys != ""):
				orderd = ""
				for item in ["1","2","3","4","5","6","7"]:
					if item in self.pressed_keys:
						orderd = orderd + item
				editable.set_text(orderd)
				self.pressed_keys = ""
				
		entry_abbreviation.connect('key-press-event',kbKeyPressed )
		entry_key_combination.connect('key-release-event',kbKeyReleased )
		
		table.attach(label_key_combination,0,1,0,1)
		table.attach(entry_key_combination,1, 2, 0, 1)
		table.attach(label_expansion, 0,1,1,2)
		table.attach(entry_expansion, 1,2,1,2)
		
		pagenum = self.notebook.get_current_page()
		object = self.notebook.get_nth_page(pagenum)

		
		dialog.show_all()
		response = dialog.run()
		if response == Gtk.ResponseType.YES:
			new_value = entry_key_combination.get_text()
			if (not object.key_combination_exist(new_value)):
				object.liststore.append([entry_key_combination.get_text(),entry_expansion.get_text()])
				self.saved = False
			else:
				dialog_exist =  Gtk.Dialog("Warning!",self.window,1,("Skip",Gtk.ResponseType.NO,"Replace",Gtk.ResponseType.YES))
				label = Gtk.Label("Expansion for this Key-Combination already exists!")
				box = dialog_exist.get_content_area();
				box.add(label)
				dialog_exist.show_all()
				response = dialog_exist.run()
				if response == Gtk.ResponseType.YES:
					self.saved = False
					for row in object.liststore:
						if row[0] == new_value:
							object.liststore.insert_before(row.iter,[entry_key_combination.get_text(),entry_expansion.get_text()])
							object.liststore.remove(row.iter)
							break
				dialog_exist.destroy()
		dialog.destroy()

	def clear_all(self,widget,data=None):
		dialog =  Gtk.Dialog("Warning!",self.window,1,("No",Gtk.ResponseType.NO,"Yes",Gtk.ResponseType.YES))
		label = Gtk.Label("Clear all entries ?!")
		box = dialog.get_content_area();
		box.add(label)
		dialog.show_all()
		response = dialog.run()
		if response == Gtk.ResponseType.YES:
			pagenum = self.notebook.get_current_page()
			object = self.notebook.get_nth_page(pagenum)
			object.liststore.clear()
		dialog.destroy()

	def remove(self,widget,data=None):
		pagenum = self.notebook.get_current_page()
		object = self.notebook.get_nth_page(pagenum)
		selection = object.treeview.get_selection()
		(model, pathlist) = selection.get_selected_rows()
		self.saved = False
		for path in pathlist:
			tree_iter = model.get_iter(path)
			value = model.get_value(tree_iter,0)
			model.remove(tree_iter)


	def import_from_file(self,filename):
		pagenum = self.notebook.get_current_page()
		object = self.notebook.get_nth_page(pagenum)
		object.import_from_file(filename)
		
		
					
				
	def import_(self,widget,data=None):
		open_file = Gtk.FileChooserDialog("Select the file to open",None,Gtk.FileChooserAction.OPEN,buttons=(Gtk.STOCK_OPEN,Gtk.ResponseType.OK))
		open_file.set_current_folder("%s"%(os.environ['HOME']))
		response = open_file.run()
		if response == Gtk.ResponseType.OK:
			self.import_from_file(open_file.get_filename())
		open_file.destroy()

	
	def save_to_file(self,filename):
		pagenum = self.notebook.get_current_page()
		object = self.notebook.get_nth_page(pagenum)
		file = open(filename,"w")
		for item in object.liststore:
			abb,exp = item
			file.write("{} {}\n".format(abb,exp))
		file.close()
	
	def export(self,widget,data=None):
		save_file = Gtk.FileChooserDialog("Export list ",None,Gtk.FileChooserAction.SAVE,buttons=(Gtk.STOCK_SAVE,Gtk.ResponseType.OK))
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
		pagenum = self.notebook.get_current_page()
		object = self.notebook.get_nth_page(pagenum)		
		self.save_to_file("{}/{}/{}".format(data_dir,self.language,object.filename))

	def save_all(self,widget,data=None):
		for pagenum in range(0,self.notebook.get_n_pages()):
			object = self.notebook.get_nth_page(pagenum)
			file = open("{}/{}/{}".format(data_dir,self.language,object.filename),"w")
			for item in object.liststore:
				key,val = item
				file.write("{} {}\n".format(key,val))
			file.close()
		
		

	def quit(self,widget,data=None):
		Gtk.main_quit()
		
ibus_sharada_braille_le()
Gtk.main()



		
	
