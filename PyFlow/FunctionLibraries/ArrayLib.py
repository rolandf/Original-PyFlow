from ..Core.FunctionLibrary import *
from ..Core.AGraphCommon import *
import pyrr


class ArrayLib(FunctionLibraryBase):
    '''doc string for ArrayLib'''
    def __init__(self):
        super(ArrayLib, self).__init__()

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.String, ''), meta={'Category': 'Array', 'Keywords': []})
    def arrayToString(arr=(DataTypes.Array, [])):
        return str(arr)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'Array', 'Keywords': []})
    def arrayLen(arr=(DataTypes.Array, [])):
        return len(arr)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Any, ''), meta={'Category': 'Array', 'Keywords': []})
    def selectInArray(arr=(DataTypes.Array, []), Index=(DataTypes.Int, 0), Result=(DataTypes.Reference, (DataTypes.Bool, False))):
        try:
            element = arr[Index]
            Result(True)
            return element
        except:
            Result(False)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, False), meta={'Category': 'Array', 'Keywords': []})
    def findInArray(List=(DataTypes.Array, []), Value=(DataTypes.Any, 0),Result=(DataTypes.Reference, (DataTypes.Bool, False))):
        find = Value in List
        if find:
            Result(True)
            return List.index(Value)
        else:
            Result(False)
            return -1


    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Array', 'Keywords': []})
    def Any(List=(DataTypes.Array, [])):
        return any(List)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, False), meta={'Category': 'Array', 'Keywords': []})
    def All(List=(DataTypes.Array, [])):
        return all(List)

