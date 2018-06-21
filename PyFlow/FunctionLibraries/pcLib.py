from ..Core.FunctionLibrary import *
from ..Core.AGraphCommon import *
import os

from Qt.QtWidgets import QFileDialog
import sys 
sys.path.append(r"C:\Users\pedro\OneDrive\pcTools_v5\pcSequenceExplorer\modules")
from pcSeq import get_sequences

class pcLib(FunctionLibraryBase):
    '''
    Default library builting stuff, variable types and conversions
    '''
    def __init__(self):
        super(pcLib, self).__init__()

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Array, 0), meta={'Category': 'pcTools|FileSystem', 'Keywords': ["get","sequences"]})
    ## make integer
    def getSequences(path=(DataTypes.String, "")):
        '''make integer'''      
        return get_sequences(path)[0]
    
 