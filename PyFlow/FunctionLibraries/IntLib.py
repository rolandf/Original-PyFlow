from ..Core.FunctionLibrary import *
from ..Core.AGraphCommon import *
from numpy import sign


class IntLib(FunctionLibraryBase):
    '''doc string for IntLib'''
    def __init__(self):
        super(IntLib, self).__init__()

   

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Int', 'Keywords': []})
    def modulo(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''
        Modulo (A % B)
        '''
        return (a % b) if b != 0 else 0

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []})
    def bitwiseAnd(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''
        Bitwise AND (A & B)
        '''
        return a & b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []})
    def bitwiseNot(a=(DataTypes.Int, 0)):
        '''
        Bitwise NOT (~A)
        '''
        return ~a

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []})
    def bitwiseOr(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''
        Bitwise OR (A | B)
        '''
        return a | b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []})
    def bitwiseXor(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''
        Bitwise XOR (A ^ B)
        '''
        return a ^ b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []})
    def binaryLeftShift(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''
        Binary left shift a << b
        '''
        return a << b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []})
    def binaryRightShift(a=(DataTypes.Int, 0), b=(DataTypes.Int, 0)):
        '''
        Binary right shift a << b
        '''
        return a >> b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []})
    def testBit(intType=(DataTypes.Int, 0), offset=(DataTypes.Int, 0)):
        '''
        Returns a nonzero result, 2**offset, if the bit at 'offset' is one
        '''
        mask = 1 << offset
        return(intType & mask)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []})
    def setBit(intType=(DataTypes.Int, 0), offset=(DataTypes.Int, 0)):
        '''
        Returns an integer with the bit at 'offset' set to 1'
        '''
        mask = 1 << offset
        return(intType | mask)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []})
    def clearBit(intType=(DataTypes.Int, 0), offset=(DataTypes.Int, 0)):
        '''
        Returns an integer with the bit at 'offset' cleared.
        '''
        mask = ~(1 << offset)
        return(intType & mask)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Bits manipulation', 'Keywords': []})
    def toggleBit(intType=(DataTypes.Int, 0), offset=(DataTypes.Int, 0)):
        '''
        Returns an integer with the bit at 'offset' inverted, 0 -> 1 and 1 -> 0.
        '''
        mask = 1 << offset
        return(intType ^ mask)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Int', 'Keywords': []})
    def clampInt(Value=(DataTypes.Int, 0), Min=(DataTypes.Int, 0), Max=(DataTypes.Int, 0)):
        '''
        Returns Value clamped to be between A and B (inclusive)
        '''
        return clamp(Value, Min, Max)



    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Int', 'Keywords': []})
    def selectInt(A=(DataTypes.Int, 0), B=(DataTypes.Int, 0), PickA=(DataTypes.Bool, False)):
        '''
        If bPickA is true, A is returned, otherwise B is
        '''
        return A if PickA else B

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Math|Int', 'Keywords': []})
    def sign(a=(DataTypes.Int, 0)):
        '''
        Sign (integer, returns -1 if A &lt; 0, 0 if A is zero, and +1 if A &gt; 0)
        '''
        return sign(a)
