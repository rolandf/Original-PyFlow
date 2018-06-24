from ..Core.FunctionLibrary import *
from ..Core.AGraphCommon import *


class BoolLib(FunctionLibraryBase):
    '''doc string for BoolLib'''
    def __init__(self):
        super(BoolLib, self).__init__()


    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Bool', 'Keywords': []})
    def boolAnd(a=(DataTypes.Bool, False), b=(DataTypes.Bool, False)):
        '''
        Returns the logical AND of two values (A AND B)
        '''
        return a and b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Bool', 'Keywords': []})
    def boolNot(a=(DataTypes.Bool, False)):
        '''
        Returns the logical complement of the Boolean value (NOT A)
        '''
        return not a

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Bool', 'Keywords': []})
    def boolNand(a=(DataTypes.Bool, False), b=(DataTypes.Bool, False)):
        '''
        Returns the logical NAND of two values (A AND B)
        '''
        return not (a and b)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Bool', 'Keywords': []})
    def boolNor(a=(DataTypes.Bool, False), b=(DataTypes.Bool, False)):
        '''
        Returns the logical Not OR of two values (A NOR B)
        '''
        return not (a or b)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Bool', 'Keywords': []})
    def boolOr(a=(DataTypes.Bool, False), b=(DataTypes.Bool, False)):
        '''
        Returns the logical OR of two values (A OR B)
        '''
        return a or b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Bool', 'Keywords': []})
    def boolXor(a=(DataTypes.Bool, False), b=(DataTypes.Bool, False)):
        '''
        Returns the logical eXclusive OR of two values (A XOR B)
        '''
        return a ^ b
