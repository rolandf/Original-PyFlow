from ..Core.FunctionLibrary import *
from ..Core.AGraphCommon import *
import os


class DefaultLib(FunctionLibraryBase):
    '''
    Default library builting stuff, variable types and conversions
    '''
    def __init__(self):
        super(DefaultLib, self).__init__()

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Bool', 'Keywords': []},color=Colors.Bool.lighter(50))
    ## make boolean
    def makeBool(b=(DataTypes.Bool, False)):
        return b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'GenericTypes', 'Keywords': ["Int","Integer"]},color=Colors.Int.lighter(50))
    ## make integer
    def makeInt(i=(DataTypes.Int, 0)):
        '''make integer'''
        return i

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'GenericTypes', 'Keywords': ["Float"]},color=Colors.Float.lighter(50))
    ## make floating point number
    def makeFloat(f=(DataTypes.Float, 0.0)):
        '''make floating point number'''
        return f

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.String, ''), meta={'Category': 'GenericTypes', 'Keywords': ["String"]},color=Colors.String.lighter(50))
    ## make string
    def makeString(s=(DataTypes.String, '')):
        '''make string'''
        return s

    # Conversions
    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Conversion', 'Keywords': ["Bool"]},color=Colors.Bool.lighter(50))
    def toBool(i=(DataTypes.Any, 0,{"supportedDataTypes":[DataTypes.Bool,DataTypes.Float,DataTypes.Int]})):
        return bool(i)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Conversion', 'Keywords': []},color=Colors.Int.lighter(50))
    def toInt(i=(DataTypes.Any, 0,{"supportedDataTypes":[DataTypes.Bool,DataTypes.Float,DataTypes.Int]})):
        return int(f)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, False), meta={'Category': 'Conversion', 'Keywords': []},color=Colors.Float.lighter(50))
    def toFloat(i=(DataTypes.Any, 0,{"supportedDataTypes":[DataTypes.Bool,DataTypes.Float,DataTypes.Int]})):
        return float(i)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.String, ''), meta={'Category': 'Conversion', 'Keywords': []},color=Colors.String.lighter(50))
    def toString(i=(DataTypes.Any, 0)):
        return str(i)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Any, 0,{"constraint":"1"}), meta={'Category': 'Conversion', 'Keywords': []},color=Colors.Yellow.lighter(50))
    def passtrhough(input=(DataTypes.Any, 0,{"constraint":"1"})):
        return input  

    ###########

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Utils', 'Keywords': []},color=Colors.NodeNameRect)
    ## Returns the CPU time or real time since the start of the process or since the first call of clock()
    def clock():
        '''Returns the CPU time or real time since the start of the process or since the first call of clock().'''
        return time.clock()

    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={'Category': 'DefaultLib', 'Keywords': ['print']},color=Colors.NodeNameRect)
    ## Python's 'print' function wrapper
    def pyprint(entity=(DataTypes.Any, None)):
        '''
        printing a string
        '''
        print(str(entity))

    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={'Category': 'DefaultLib', 'Keywords': []},color=Colors.NodeNameRect)
    ## cls cmd call Clears Output Log.
    def cls():
        '''cls cmd call Clears Output Log.'''
        os.system('cls')        