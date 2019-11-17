# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 23:55:25 2019

@author: Mario
"""

def readjosn_myself(fileName=""):
    import json
    if fileName!='':
        strList = fileName.split(".")
        if strList[len(strList)-1].lower() == "json":
            with open(fileName,mode='r',encoding="utf-8") as file:
                return json.loads(file.read())
