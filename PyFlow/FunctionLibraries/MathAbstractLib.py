from ..Core.FunctionLibrary import *
from ..Core.AGraphCommon import *
import pyrr
class MathAbstractLib(FunctionLibraryBase):
    '''doc string for MathAbstractLib'''
    def __init__(self):
        super(MathAbstractLib, self).__init__()

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Basic', 'Keywords': ["="]})
    ## Is a equal b
    def isequal(a=(DataTypes.Any, 0,{"constraint":"1"}),
                b=(DataTypes.Any, 0,{"constraint":"1"})):
        '''
        Is a equal b
        '''
        return a == b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Basic', 'Keywords': [">"]})
    ## Is a > b
    def isGreater(a=(DataTypes.Any, 0,{"constraint":"1","supportedDataTypes":[DataTypes.Bool,DataTypes.Float,DataTypes.Int,
                                                                              DataTypes.Matrix33,DataTypes.Matrix44,DataTypes.Quaternion,
                                                                              DataTypes.FloatVector3,DataTypes.FloatVector4]}),
                  b=(DataTypes.Any, 0,{"constraint":"1","supportedDataTypes":[DataTypes.Bool,DataTypes.Float,DataTypes.Int,
                                                                              DataTypes.Matrix33,DataTypes.Matrix44,DataTypes.Quaternion,
                                                                              DataTypes.FloatVector3,DataTypes.FloatVector4]})):
        '''
        Is a > b
        '''
        return a > b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Basic', 'Keywords': [">"]})
    ## Is a >= b
    def isGreaterOrEqual(a=(DataTypes.Any, 0,{"constraint":"1","supportedDataTypes":[DataTypes.Bool,DataTypes.Float,DataTypes.Int,
                                                                              DataTypes.Matrix33,DataTypes.Matrix44,DataTypes.Quaternion,
                                                                              DataTypes.FloatVector3,DataTypes.FloatVector4]}),
                         b=(DataTypes.Any, 0,{"constraint":"1","supportedDataTypes":[DataTypes.Bool,DataTypes.Float,DataTypes.Int,
                                                                              DataTypes.Matrix33,DataTypes.Matrix44,DataTypes.Quaternion,
                                                                              DataTypes.FloatVector3,DataTypes.FloatVector4]})):
        '''
        Is a >= b
        '''
        return a >= b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Basic', 'Keywords': ["<"]})
    ## Is a < b
    def isLess(a=(DataTypes.Any, 0,{"constraint":"1","supportedDataTypes":[DataTypes.Bool,DataTypes.Float,DataTypes.Int,
                                                                              DataTypes.Matrix33,DataTypes.Matrix44,DataTypes.Quaternion,
                                                                              DataTypes.FloatVector3,DataTypes.FloatVector4]}),
               b=(DataTypes.Any, 0,{"constraint":"1","supportedDataTypes":[DataTypes.Bool,DataTypes.Float,DataTypes.Int,
                                                                              DataTypes.Matrix33,DataTypes.Matrix44,DataTypes.Quaternion,
                                                                              DataTypes.FloatVector3,DataTypes.FloatVector4]})):
        '''
        Is a < b
        '''
        return a < b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Basic', 'Keywords': ["<"]})
    ## Is a <= b
    def isLessOrEqual(a=(DataTypes.Any, 0,{"constraint":"1","supportedDataTypes":[DataTypes.Bool,DataTypes.Float,DataTypes.Int,
                                                                              DataTypes.Matrix33,DataTypes.Matrix44,DataTypes.Quaternion,
                                                                              DataTypes.FloatVector3,DataTypes.FloatVector4]}),
                         b=(DataTypes.Any, 0,{"constraint":"1","supportedDataTypes":[DataTypes.Bool,DataTypes.Float,DataTypes.Int,
                                                                              DataTypes.Matrix33,DataTypes.Matrix44,DataTypes.Quaternion,
                                                                              DataTypes.FloatVector3,DataTypes.FloatVector4]})):
        '''
        Is a <= b
        '''
        return a <= b

    @staticmethod
    @IMPLEMENT_NODE(returns=((DataTypes.Any, 0,{"constraint":"1"})), meta={'Category': 'Math|Basic', 'Keywords': ['+', 'append',"sum"]})
    ## Basic Sum 
    def add(a=(DataTypes.Any, 0,{"constraint":"1"}), b=(DataTypes.Any, 0,{"constraint":"1"})):
        '''
        Basic Sum 
        '''
        return a + b

    @staticmethod
    @IMPLEMENT_NODE(returns=((DataTypes.Any, 0,{"constraint":"1"})), meta={'Category': 'Math|Basic', 'Keywords': ['-']})
    ## Basic subtraction
    def subtract(a=(DataTypes.Any, 0,{"constraint":"1","supportedDataTypes":[DataTypes.Bool,DataTypes.Float,DataTypes.Int,
                                                                              DataTypes.Matrix33,DataTypes.Matrix44,DataTypes.Quaternion,
                                                                              DataTypes.FloatVector3,DataTypes.FloatVector4]}),
                         b=(DataTypes.Any, 0,{"constraint":"1","supportedDataTypes":[DataTypes.Bool,DataTypes.Float,DataTypes.Int,
                                                                              DataTypes.Matrix33,DataTypes.Matrix44,DataTypes.Quaternion,
                                                                              DataTypes.FloatVector3,DataTypes.FloatVector4]})):
        '''
        Basic subtraction
        '''
        return a - b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Any, 0.0,{"constraint":"1"}), meta={'Category': 'Math|Basic', 'Keywords': ['/',"divide"]})
    ## Basic division
    def divide(a=(DataTypes.Any, 0,{"constraint":"1","supportedDataTypes":[DataTypes.Bool,DataTypes.Float,DataTypes.Int,
                                                                              DataTypes.Matrix33,DataTypes.Matrix44,DataTypes.Quaternion,
                                                                              DataTypes.FloatVector3,DataTypes.FloatVector4]}),
                         b=(DataTypes.Any, 0,{"constraint":"1","supportedDataTypes":[DataTypes.Bool,DataTypes.Float,DataTypes.Int,
                                                                              DataTypes.Matrix33,DataTypes.Matrix44,DataTypes.Quaternion,
                                                                              DataTypes.FloatVector3,DataTypes.FloatVector4]}),
                         result=(DataTypes.Reference, (DataTypes.Bool, False))):
        '''
        Basic division
        '''
        try:
            d = a / b
            result(True)
            return d
        except:
            result(False)
            return -1

    @staticmethod
    @IMPLEMENT_NODE(returns=((DataTypes.Any, 0,{"constraint":"1"})), meta={'Category': 'Math|Basic', 'Keywords': ['*',"multiply"]})
    ## Basic multiplication
    def multiply(a=(DataTypes.Any, 0,{"constraint":"1","supportedDataTypes":[DataTypes.Bool,DataTypes.Float,DataTypes.Int,
                                                                              DataTypes.Matrix33,DataTypes.Matrix44,DataTypes.Quaternion,
                                                                              DataTypes.FloatVector3,DataTypes.FloatVector4]}),
             b=(DataTypes.Any, 0,{"constraint":"1","supportedDataTypes":[DataTypes.Bool,DataTypes.Float,DataTypes.Int,
                                                                              DataTypes.Matrix33,DataTypes.Matrix44,DataTypes.Quaternion,
                                                                              DataTypes.FloatVector3,DataTypes.FloatVector4]})):
        '''
        Basic multiplication
        '''
        return a * b
       

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Vector4', 'Keywords': ['vector', '|','dot','product']})
    def dotProduct(a=(DataTypes.Any, 0,{"constraint":"1","supportedDataTypes":[DataTypes.FloatVector4,DataTypes.FloatVector3,DataTypes.Quaternion]}),
              b=(DataTypes.Any, 0,{"constraint":"1","supportedDataTypes":[DataTypes.FloatVector4,DataTypes.FloatVector3,DataTypes.Quaternion]})):
        '''Dot product'''
        if type(a) == "Quaternion":
            return a.dot(b)
        return a | b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Int', 'Keywords': ["inrange","range"]})
    def inRange(Value=(DataTypes.Any, 0,{"constraint":"1","supportedDataTypes":[DataTypes.Bool,DataTypes.Float,DataTypes.Int,
                                                                              DataTypes.Matrix33,DataTypes.Matrix44,DataTypes.Quaternion,
                                                                              DataTypes.FloatVector3,DataTypes.FloatVector4]}),
                RangeMin=(DataTypes.Any, 0,{"constraint":"1","supportedDataTypes":[DataTypes.Bool,DataTypes.Float,DataTypes.Int,
                                                                              DataTypes.Matrix33,DataTypes.Matrix44,DataTypes.Quaternion,
                                                                              DataTypes.FloatVector3,DataTypes.FloatVector4]}),
                RangeMax=(DataTypes.Any, 0,{"constraint":"1","supportedDataTypes":[DataTypes.Bool,DataTypes.Float,DataTypes.Int,
                                                                              DataTypes.Matrix33,DataTypes.Matrix44,DataTypes.Quaternion,
                                                                              DataTypes.FloatVector3,DataTypes.FloatVector4]}),
                InclusiveMin=(DataTypes.Bool, False),
                InclusiveMax=(DataTypes.Bool, False)):
        '''
        Returns true if value is between Min and Max (V &gt;= Min && V &lt;= Max) If InclusiveMin is true, value needs to be equal or larger than Min, else it needs to be larger If InclusiveMax is true, value needs to be smaller or equal than Max, else it needs to be smaller
        '''
        return ((Value >= RangeMin) if InclusiveMin else (Value > RangeMin)) and ((Value <= RangeMax) if InclusiveMax else (Value < RangeMax))        