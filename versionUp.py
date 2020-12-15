#!/usr/bin/env python2.7

"""
Works with Maya 2018
Will incrementally save current file while maintaining the number padding.
Only works if current file has a name with numbers at the end.
Created Oct 2020

__author__: James Chan
"""

import maya.cmds as cmds


def versionUp():
    # grab scene name and filetype
    scene_name = cmds.file(q=True, sn=True, shn=True)[:-3]
    scene_type = cmds.file(q=True, sn=True, shn=True)[-3:]
    number_string = ''

    if scene_name is None:
        print "File currently not named!"
        return

    # loop backwards through scene_name to put digits into number_string
    i = len(scene_name)-1
    while i >= 0 and scene_name[i].isdigit():
        number_string += scene_name[i]
        i -= 1

    if number_string == '':
        number_string = '000'

    # grab words of the filename and reverse number string
    word_string = scene_name[0:i+1]
    number_string_reverse = number_string[::-1]

    # convert number string to int, add 1, re-convert to padded string
    number_int = int(number_string_reverse)+1
    number_string_final = str(number_int)
    padding = len(number_string)
    padded_number = number_string_final.zfill(padding)

    # concatenate elements into final string and save
    final_save_name = word_string + padded_number + scene_type
    cmds.file(rename=final_save_name)
    cmds.file(save=True)

versionUp()    
