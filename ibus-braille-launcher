#!/bin/bash

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
#    Entire project rewritten by Zendalona (2022-2023)
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

# Checking Ibus daemon is running. 
# If not, start the daemon
SERVICE="ibus-daemon"
if pgrep -x "$SERVICE" >/dev/null
then
    echo "$SERVICE is running"
else
    echo "$SERVICE stopped"
    ibus-daemon --daemonize
fi

# Waiting for daemon to start
sleep 1

# Checking current Ibus engine. 
# Switching if not IBus-Braille,

engine=`ibus engine`
if [ "$engine" != "IBus-Braille" ];
then
    echo "Switching to IBus-Braille"
    ibus engine IBus-Braille
else
    echo "Already in IBus-Braille"
fi    
