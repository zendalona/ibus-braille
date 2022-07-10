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
import gettext
_ = gettext.gettext

app_name = "IBus-Braille"

locale_dir =  '/usr/share/locale'

version = "2.0"

#Where the data is located
data_dir = "/usr/share/ibus-braille/";

user_conf_dir = os.environ['HOME']+"/.ibus-braille/"

user_preferences_file_path = user_conf_dir+'user-preferences.cfg'

abbreviations_file_path = user_conf_dir+"abbreviations.json"
