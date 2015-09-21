# vim:set et ts=4:
#
# ibus-sharada-braille - The braille ibus engine
#
# Copyright (c) 2014-2015 Nalin.x.GNU <nalin.x.linux@gmail.com>
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

# if not 1, append datestamp to the version number.
m4_define([package_name], [ibus-braille])
m4_define([ibus_released], [0])
m4_define([ibus_major_version], [1])
m4_define([ibus_minor_version], [2])
m4_define([ibus_micro_version], [99])
m4_define(ibus_maybe_datestamp,
    m4_esyscmd([if test x]ibus_released[ != x1; then date +.%Y%m%d | tr -d '\n\r'; fi]))

m4_define([ibus_version],
    ibus_major_version.ibus_minor_version.ibus_micro_version[]ibus_maybe_datestamp)

AC_INIT([package_name], [ibus_version], [http://code.google.com/p/ibus/issues/entry], [package_name])
AM_INIT_AUTOMAKE([1.10])
AC_GNU_SOURCE

AC_CONFIG_HEADERS([config.h])
AC_CONFIG_MACRO_DIR([m4])
m4_ifdef([AM_SILENT_RULES],[AM_SILENT_RULES([yes])])

# define PACKAGE_VERSION_* variables
#AS_VERSION
#AS_NANO
AM_SANITY_CHECK
AM_MAINTAINER_MODE
AM_DISABLE_STATIC
AC_PROG_CC
AM_PROG_CC_C_O
AC_PROG_CXX
AC_ISC_POSIX
AC_HEADER_STDC
AM_PROG_LIBTOOL


# Define python version
AC_ARG_WITH(python,
    AS_HELP_STRING([--with-python[=PATH]],
        [Select python2 or python3]),
    [PYTHON=$with_python], []
)


#check python
AM_PATH_PYTHON([2.5])

# OUTPUT files
AC_CONFIG_FILES(
Makefile
engine/Makefile
engine/ibus-braille
engine/braille.xml.in
icons/Makefile
m4/Makefile
braille/Makefile
braille/english/Makefile
braille/french/Makefile
braille/hindi/Makefile
braille/kannada/Makefile
braille/malayalam/Makefile
braille/numerical/Makefile
braille/spanish/Makefile
braille/tamil/Makefile
preferences/Makefile
preferences/ibus-braille-preferences
abbreviation-editor/Makefile
abbreviation-editor/ibus-braille-abbreviation-editor
language-editor/Makefile
language-editor/ibus-braille-language-editor

)

AC_OUTPUT
