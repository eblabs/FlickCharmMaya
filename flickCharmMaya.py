# coding: utf-8

# import maya.cmds as cmds
# import maya.mel as mel
from functools import partial
import copy
import string
import colorsys
# import maya.api.OpenMaya as OpenMaya
import math
import os
#import json
# from itertools import groupby
import traceback
import re
from operator import itemgetter
# import maya.OpenMayaUI as mui
import getpass
# from PySide import QtGui
# import cPickle
import shutil
import sys
import datetime
# import time
import bisect
#import scandir
import flickCharm
reload(flickCharm)
from flickCharm import *

try:
    import simplejson as json
except ImportError:
    import json

SipLoaded = False
ShibokenLoaded = False
try:
    import sip
    for a in ['QDate', 'QDateTime' , 'QString', 'QTextStream', 'QTime', 'QUrl', 'QVariant']:
        try:
            sip.setapi(a, 2)
        except Exception, e:
            print e, 'SET API v2 FAIL'
    #
    SipLoaded = True
except:
    try:
        import shiboken
        ShibokenLoaded = True
    except:
        pass


PyQt4Loaded = False
PySideLoaded = False
try:
    from PyQt4 import QtGui, QtCore
    PyQt4Loaded = True
except:
    try:
        from PySide import QtGui, QtCore
        PySideLoaded = True
    except:
        pass
    
    
    
    
class Window(QtGui.QDialog):  # QtGui.QWidget QtGui.QMainWindow
    __OBJ_NAME__ = 'dev'
    __TITLE__ = 'dev'
    __instance__ = None
    currentSelection = False
    copySelectionBuffer = False

    def __init__(self, parent=None):
        # init
        mayaWindow = Maya.getMainWindow()
        if mayaWindow:
            parent = mayaWindow
        super(Window, self).__init__(parent)
        
        # finger scrolling effect
        self.charm = FlickCharm()
        
        print 'dev' #, __version__
        # set size
        self.resize(425, 500)
        
        # window setup
        self.setWindowTitle("scrolling dev")
        self.setVisible(True)  # without this, there are focus problems!!
        
        # set some variables
        self.infoPath = False
        self.infoVersion = False
        
        # set main layout
        self.mainLayout = VBoxLayout(self)
        self.setLayout(self.mainLayout)
        self.setupLayouts(self.mainLayout)

        # set focus
        self.setFocus()
        
        

    @classmethod
    def load(cls):
        # force a singleton pattern
        if cls.__instance__ is not None:
            cls.__instance__.close()

        # init UI
        cls.__instance__ = cls()

        # Show UI
        cls.__instance__.show()
        cls.__instance__.raise_()


    def setupLayouts(self, parent):
        
        # main list view
        mainWidget = QtGui.QWidget(self)
        mainWidgetLayout = VBoxLayout(self)
        mainWidget.setLayout(mainWidgetLayout)
        
        # listview
        self.customView = CustomQListView(parent=self)
        
        # flickcharm
        self.charm.activateOn(self.customView)
        
        # parenting
        mainWidgetLayout.addWidget(self.customView)
        parent.addWidget(mainWidget)
        
        # add some icons
        for i in range(0,20):
            print i
            item = QtGui.QStandardItem()
            icon = QtGui.QIcon()
            iconImage = QtGui.QPixmap(500 , 500)
            rgb = [.5,.5,.5]
            iconImage.fill(QtGui.QColor(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)))
            icon.addPixmap(iconImage)
            item.setIcon(icon)
            self.customView._model.appendRow(item)
            

class VBoxLayout(QtGui.QVBoxLayout): 
    
    def __init__(self, parent=False, *args, **kwargs):
        #
        super(VBoxLayout, self).__init__(*args, **kwargs)
        
        # set defaults
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        # self.layout().setContentsMargins(0, 0, 0, 0)

class CustomQListView(QtGui.QListView): 

    def __init__(self, parent, *args, **kwargs):
        #
        super(CustomQListView, self).__init__(parent, *args, **kwargs)
        
        # model
        self._model = QtGui.QStandardItemModel(self)
        self.setModel(self._model)
        
        # settings
        self.setViewMode(QtGui.QListView.IconMode)
        self.setIconSize(QtCore.QSize(100, 100))
        self.setMovement(QtGui.QListView.Static)     
        self.setResizeMode(QtGui.QListView.Adjust)

    def setSize(self, size, *args, **kwargs):
        self.setIconSize(QtCore.QSize(size, size))
    
    def clear(self):
        self._model.clear()

class Maya():
    mayaLoaded = False
    try:
        from maya import cmds
        from maya import mel
        import maya.OpenMayaUI as OpenMayaUI
        import maya.api.OpenMaya as OpenMaya
        mayaLoaded = True
    except Exception, e:
        print 568, e
        pass
    
    @classmethod
    def isMayaLoaded(cls):
        return cls.mayaLoaded   

    @classmethod
    def getMainWindow(cls):
        if not cls.isMayaLoaded():
            return False
        try:
            pointer = cls.OpenMayaUI.MQtUtil.mainWindow()
            return cls.wrapInstance(pointer)
        except:
            return False

    @classmethod
    def unwrapInstance(cls, pointer):
        if not cls.isMayaLoaded():
            return False
        try:
            try:
                return long(sip.unwrapinstance(pointer))
            except:
                return shiboken.getCppPointer(pointer)[0]
                # return long(shiboken.unwrapinstance(pointer))
        except:
            return False  

    @classmethod
    def wrapInstance(cls, pointer):
        if not cls.isMayaLoaded():
            return False
        try:
            try:
                return sip.wrapinstance(long(pointer), QtCore.QObject)
            except:
                return shiboken.wrapInstance(long(pointer), QtGui.QWidget)
        except:
            return False         

'''
import sys
path = '/u/flickCharmMaya'
if not path in sys.path:
    sys.path.append(path)
import flickCharmMaya
reload(flickCharmMaya)
flickCharmMaya.Window.load()
'''
