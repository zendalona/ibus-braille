ibus-sharada-braille
====================

<b>Braille input method for ibus </b>


ibus-sharada-braille is an ibus input engine based on six key approach of braille. We express our gratitude to Swathanthra Malayalam Computing(SMC) for mentoring this project. We consider the acceptance of this project by Svathanthra Malayalam Computing and Google as a new flowering of the effort of louis braille. By default it uses letters f, d, s, j, k, and l in the keyboard to represent 1, 2, 3, 4, 5 and 6 of the braille dots respectively. One can use different combinations of braille to produce text. For example key 'f' will produce 'a', 'f' and 'd' will produce 'b' and 'f' and 'j' will produce 'c' and like. The combination of keys should be released together fafter pressing them.

	
<b>Languages : - </b> This version comes with  seven languages English, Malayalam, Hindi, Kannada, Tamil, French, and Spanish.
English is the default language, and one can switch to other languages by pressing language switch key (Pause Break). one can go back to previus language using the same key. One can select the required languages by checking them in general page of ibus-sharada-braille-preferences. Also default language can be change by using the combo box that appears in the same page.


<b> Contractions : -</b> All the grade 2 and grade 3 contractions in English and Malayalam is available in ibus-sharada-braille. 
In order to activate contractions one should uncheck the simple mode. To produce contraction, press the combination of
letters after pressing the contraction key, Dot 5, 5-6, 4-5-6, 4, 3, 3-6, 6, 3, 1-5-6 are the contraction signs.
For example, press 'f' and 'd' together after pressing 'j' will produce word "better" and like. Along with these contractions,
we have provided some contractions in the simple mode itself. For this purpose we have used the combinations which
are not used for alphabets.

<b> Numerals : -</b> One can select numeral as language. Nemeth code approach is accepted here. In this mode, 
d, s, k, l representing 2, 3, 5, 6 of the braille dots are used for numbers that is d for 1 and d, 
s together for 2 etc. Other letters are written as in braille mode.f, k, l combination is used to produce 
underscore an this combination can be used  to produce line in any text. Numeral mode is used for handling 
mathematics.

<b>Punctuations : -</b> To produce any punctuation one should press semicolon in the ordinary keyboard and then press necessary combinations.


<b>Abbreviations : -</b> letter 'a' is the abbreviation key and one should press 'a'  after typing the abbreviation. For example pressing 'a' 
after typing 'ab' will expand the word 'ab' to 'about' This facility will increase the speed of producing text.

<b>Abbreviation-Editor : -</b> It is a unique feature of isb which enable a user to create whatever abbreviation he/she requires. 
In order to edit the abbreviation one has to open ibus-sharada-braille-abbreviation-editor then select the language of which abbreviation to be edited. 
For adding a new abbreviation one has to click add button which will prompt a dialog with two entrys abbreviation and expantion, user has to fill apropriate data and click add button. One can remove an abbreviation by clicking on remove button. One has to press save button to make it effective. Abbreviations thus saved can be shared with others using the export button which will prompt a save dialog.
restore button will delete all newly added abbreviations and restore the list to the default position.
For english we have already provided all the grade 3 abbreviations in the package. 




<b> Beginning list and middle list : -</b> One can switch between middle list and beginning list using map-switching key(left ALT). 
This will help the user to write any letter anywhere. for example  one can write a vowel in hindi inside a word. 
To write a full vowel instead of a sign, one should press left alt and then type the combination needed for the vowel.

<b> Simple-Mode : -</b> ibus sharada braille is installed as the simple mode unchecked. This is will be complicated for a beginner. To avoid these complications a newbie can disable abbreviations and contractions by checking simple mode from general page of ibus-sharada-braille-preferences.

<b> Text Manipulation : -</b> capitol/chill key('g') is used to produce capital letter in English and chillu in malayalam. 
pressing this key before typing the braille combination to make a letter capital and pressing this key after typing 
the braille combination to make a letter chillu in malayalam. If this capitol key is pressed before using a contracted 
word, whole letters will be in capital. Letter deletion key('h') will delete the last letter typed and pressing letter deletion key and capitol/chill key together will delete the last word. 
Caps lock : One can enable and disable caps lock by pressing capitol/chill key two tyme continuesly. 


<b> Key-remapping : -</b> One can change the all keys by using ket/shortcut page of ibus-sharada-braille-preferences. users having non qwerty keyboard can use this to setup six appropriate keys on there keyboard. Here user can also change the key for language switching,map switching and capitol/chill as well. By default the following keys are given for different functionalities.
f, d, s, j, k, l for dots 1, 2, 3, 4, 5, 6 of the braille dots.  semicolon as punctuation key, 'g' as capital/chilli, 'h' for deletion of last letter, left alt map switching key,
'a' as abbreviation expansion key. User can tab to listen to the key assigned to the function and simply press the needed key to change it.After making the changes press apply button to effect the changes. Here also one can use restore button to come back to the default settings.

<b>ibus-sharada-braille language editor : -</b> The language editor enable the user to add a new language, remove the existing language, add a new map 
of contractions, remove the map of contractions, and manipulate the characters and contractions of existing languages.
One can also share the languages, maps, and contractions he has created, with others using the export and import facility. 


one cant start the process of editing by selecting the languge to be edited from combobox. This is the list of existing languages and one can press add-language button for creating new language. After pressing this button, one should enter the name of the language with its espeak variant name putting a hyphen between them.
Now one can work upon the language by selecting it from the list. Using remove-language button one can remove any language.

<b>Editing Map : -</b> A map is an arrangement for producing a character or list or a contraction list. 
A map is a key combination which does not produce any character but enable the user to produce the list of characters and contractions. 
After pressing the add-map button it will ask for the entry. One can press the braille combination using and press the add button. If one has pressed j and l the editor will show 4 6 and in the 
process map for 4, 6 will appear in the editor and one can add any contractions in the 4, 6 list.


<b>Editing Beginning list : -</b> This page list out all the characters that should appear after pressing the space. for 
example it contains all the vowels and other alphabets of  indian languages, and all the alphabets and 
contractions given in the braille six key combinations in english. Let us now see how one can change 
or remove a character.Just tab and then a list will appear which contains the number combinations are 
given. Again tab and add new row button will appear.After pressing the button, editor will ask for the 
braille combination and enter it using six key combinations as done in map creation.Again tab and you 
will get the column for adding the value.Then again tab and press add button.If one needs further entry 
add row button will appear again.

<b>Editing middle list : -</b> In the map page and curser is at beginning, use right arrow to select the middle list. middle list contains 
all the characters that should appear when a character  is already in position. It contains all the 
signs attached to the vowels and other alphabets in indian languages andall the alphabets and middle 
contractions like cc dd etc. 

<b>Editing Punctuation list : -</b> press right arrow and one can go to punctuation list  and here one can see the list 
of combinations for punctuations which will appear after pressing the punctution key(semicolon) in the ordinary key 
board.

please note that one can't remove beggning,middle and pucntation lists because they are essential for the working of a language
Using the right arrow one can manipulate other maps such as 4 6, 5, 4 5 6, etc in english. Again one 
can remove any unwanted row as well. one can clear all the entries using clear-all button, After the operations one should save/save-all and quit the editor to bring the changes in 
to effect.


<b>Accessibility : -</b> ibus-shrada-braille is fully orca supported and one can use the orca preferences for changing voices, punctuation levels 
to be pronounced, key echo  by character etc. In order to activate orca preferences one should 
press insert+space together. After the installation of the program,  
we recommend you to open the orca preferences and check the echo by character and uncheck the 
key echo in the key echo page to get a better speech support. To get speech support for Kannada and Tamil one should change 
the language to that language using the orca preferences


Copyright (c) 2014-2015 ISB Development Team 

    All rights reserved . Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met: 

    Redistributions of source code must retain the below copyright notice, 

    this list of conditions and the following disclaimer. 

    Redistributions in binary form must reproduce the below copyright notice, 

    this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution. 

    Neither the name of the nor the Lios team names of its 

    contributors may be used to endorse or promote products derived from this software without specific prior written permission. 

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE." 

FREE SOFTWARE FREE SOCIETY
