from ..Core.AbstractGraph import *
from ..Core.Settings import *
from ..Core import Node

from enum import IntEnum


class FILEFORMAT(IntEnum):
    mp4 = 0
    avi = 1
    mov = 2
    mkv = 3
class CODECS(IntEnum):
    h264 = 0
    h265 = 1
    Apple_Prores = 2
    mpeg4 = 3
    mpeg2 = 3
class CODECS_MPG(IntEnum):
    h264 = 0
    mpeg4 = 1
    mpeg2 = 2   
class QTPRESETS(IntEnum):
    ultrafast = 0
    superfast = 1
    veryfast = 2 
    faster = 3
    fast = 4
    medium = 5
    slow = 6
    slower = 7
    veryslow  = 8
class QTTUNES(IntEnum):
    none = 0
    film = 1
    animation = 2 
    grain = 3
    stillimage = 4
    psnr = 5
    ssim = 6
    fastdecode = 7
    zerolatency  = 8
class QTPROFILES(IntEnum):
    none = 0
    baseline = 1
    main = 2 
    high = 3
    high10 = 4
    high422 = 5
    high444 = 6
class PRORESPRESETSnames(IntEnum):
    yuv422p10le = 0
    yuva444p10le = 1
class PRORESPROFILES(IntEnum):
    Proxy = 0
    LT = 1
    SQ = 2
    HQ = 3

from Qt import QtWidgets

import sys 
sys.path.append(r"C:\Users\pedro\OneDrive\pcTools_v5\pcSequenceExplorer\modules")
from ui import converter
import subprocess as sp
class pc_ConvertToVideo(Node):
    def __init__(self, name, graph):
        super(pc_ConvertToVideo, self).__init__(name, graph)
        self.doit = self.addInputPin('DoIt', DataTypes.Exec,self.compute)
        self.seqs = self.addInputPin('seq', DataTypes.Array)
        self.ind = self.addInputPin("ind",DataTypes.Int)
        
        self.rate = self.addInputPin("rate",DataTypes.Float,defaultValue=25.0)
        self.format = self.addInputPin("format",DataTypes.Enum,userStructClass=FILEFORMAT,defaultValue=2)

        self.format.dataBeenSet.connect(self.test)
        self.codec = self.addInputPin("codec",DataTypes.Enum,userStructClass=CODECS)

        self.preset = self.addInputPin("preset",DataTypes.Enum,userStructClass=QTPRESETS,defaultValue=5)
        self.tune = self.addInputPin("tune",DataTypes.Enum,userStructClass=QTTUNES)
        self.profile = self.addInputPin("profile",DataTypes.Enum,userStructClass=QTPROFILES)
        
        self.quality = self.addInputPin("quality",DataTypes.Int,defaultValue=70)

        self.finished = self.addOutputPin("finish",DataTypes.Exec)
        self.resPath = self.addOutputPin("path",DataTypes.String)

        self.currFormat = FILEFORMAT(self.format.getData()).name
        print self.currFormat
        #pinAffects(self.inp0, self.out0)
    def test(self):
        currFormat =  self.format.getData().name
        if currFormat != self.currFormat:
            if str(currFormat) in ['mp4','avi']:
                self.codec.setUserStruct(CODECS_MPG)
                self.currFormat = currFormat
                print "mp4"

            elif str(currFormat) in ['mkv','mov']:
                self.codec.setUserStruct(CODECS)
                
                print "mov"
            self.currFormat = currFormat  
            clearLayout(self.propertyView().parent().formLayout) 
            self.onUpdatePropertyView(self.propertyView().parent().formLayout)
                      
        #self.updateOn

    @staticmethod
    def pinTypeHints():
        '''
            used by nodebox to suggest supported pins
            when drop wire from pin into empty space
        '''
        return {'inputs': [DataTypes.String], 'outputs': []}

    @staticmethod
    def category():
        '''
            used by nodebox to place in tree
            to make nested one - use '|' like this ( 'CatName|SubCatName' )
        '''
        return 'pcTools'

    @staticmethod
    def keywords():
        '''
            used by nodebox filter while typing
        '''
        return []

    @staticmethod
    def description():
        '''
            used by property view and node box widgets
        '''
        return 'default description'

    def compute(self):
        '''
            1) get data from inputs
            2) do stuff
            3) put data to outputs
            4) call output execs
        '''

        
        try:
            Dialog = QtWidgets.QDialog()
            ui = converter()
            ui.setupUi(Dialog)
            ui.BASIC_OPTIONS_FRAME.setEditText (str(self.rate.getData()))
            ui.QT_FILE_FORMAT.setEditText (str(self.format.getData()))
            args = ui.arguments(self.seqs.getData()[self.ind.getData()]) 
            args2 = [args[0]]
            for i in args[1]:
                args2.append(i)
            #print args[-1]
            a = sp.Popen(args2)
            a.wait()
            self.resPath.setData(args2[-1])
            self.finished.call()
            #str_data = self.inp0.getData()
            #self.out0.setData(str_data.upper())
        except Exception as e:
            print(e)
