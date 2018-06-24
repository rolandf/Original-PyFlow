from ..Core.FunctionLibrary import *
from ..Core.AGraphCommon import *
import pyrr


class Vector3(FunctionLibraryBase):
    '''doc string for Vector3'''
    def __init__(self):
        super(Vector3, self).__init__()

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.FloatVector3, pyrr.Vector3()), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Vector3', 'Keywords': ['vector3']})
    def v3Create():
        '''Zero Vector3.'''
        v = pyrr.Vector3()
        return v

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.FloatVector3, pyrr.Vector3()), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Vector3', 'Keywords': ['vector3']})
    def v3UnitLenX():
        '''Unit length x vector3.'''
        return pyrr.Vector3(pyrr.vector3.create_unit_length_x())

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.FloatVector3, pyrr.Vector3()), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Vector3', 'Keywords': ['vector3']})
    def v3UnitLenY():
        '''Unit length y vector3.'''
        return pyrr.Vector3(pyrr.vector3.create_unit_length_y())

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.FloatVector3, pyrr.Vector3()), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Vector3', 'Keywords': ['vector3']})
    def v3UnitLenZ():
        '''Unit length z vector3.'''
        return pyrr.Vector3(pyrr.vector3.create_unit_length_z())

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.FloatVector3, pyrr.Vector3()), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Vector3', 'Keywords': ['vector3', 'vector4']})
    def v3FromVector4(v4=(DataTypes.FloatVector4, pyrr.Vector4()), W=(DataTypes.Reference, (DataTypes.Float, 0.0))):
        '''Returns a vector3 and the W component.'''
        arrV3, _w = pyrr.vector3.create_from_vector4(v4)
        W(_w)
        return pyrr.Vector3(arrV3)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.FloatVector3, True), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Vector3', 'Keywords': ['lerp']})
    def v3Lerp(a=(DataTypes.FloatVector3, pyrr.Vector3()), b=(DataTypes.FloatVector3, pyrr.Vector3()), alpha=(DataTypes.Float, 0.0)):
        '''Vector3 lerp'''
        return pyrr.Vector3(pyrr.vector.interpolate(a, b, clamp(alpha, 0.0, 1.0)))

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.FloatVector3, pyrr.Vector3()), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Vector3', 'Keywords': ['vector3']})
    def v3Create(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0), c=(DataTypes.Float, 0.0)):
        '''creates Vector3 from given components'''
        return pyrr.Vector3([a, b, c])


    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.FloatVector3, pyrr.Vector3()), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Vector3', 'Keywords': ['vector3', '^']})
    def v3Cross(a=(DataTypes.FloatVector3, pyrr.Vector3()), b=(DataTypes.FloatVector3, pyrr.Vector3())):
        '''cross product of two vectors'''
        return a ^ b

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.FloatVector3, pyrr.Vector3()), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Vector3', 'Keywords': ['vector3', '*']})
    def v3RotateByM33(v=(DataTypes.FloatVector3, pyrr.Vector3()), m=(DataTypes.Matrix33, pyrr.Matrix33())):
        '''rotates a vector3 by a matrix33'''
        return m * v

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.FloatVector3, pyrr.Vector3()), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Vector3', 'Keywords': ['vector3', '*']})
    def v3RotateByQuat(v=(DataTypes.FloatVector3, pyrr.Vector3()), q=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''rotates a vector3 by a quaternion'''
        return q * v

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Vector3', 'Keywords': ['vector3']})
    def v3Len(v=(DataTypes.FloatVector3, pyrr.Vector3())):
        '''Returns the length of a vector.'''
        return pyrr.vector.length(v)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Vector3', 'Keywords': ['vector3']})
    def v3SquaredLen(v=(DataTypes.FloatVector3, pyrr.Vector3())):
        '''Calculates the squared length of a vector.\nUseful when trying to avoid the performance penalty of a square root operation.'''
        return pyrr.vector.squared_length(v)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.FloatVector3, pyrr.Vector3()), meta={'Category': 'Math|Vector3', 'Keywords': ['vector3']})
    def v3Normalize(v=(DataTypes.FloatVector3, pyrr.Vector3()), result=(DataTypes.Reference, (DataTypes.Bool, False))):
        '''Normalizes a single vector to unit length.\nIf zero-length - returns original one.'''
        try:
            res = pyrr.Vector3(pyrr.vector.normalize(v))
            result(True)
            return res
        except:
            result(False)
            return v

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Vector3', 'Keywords': ['vector3']})
    def v3SetLen(v=(DataTypes.FloatVector3, pyrr.Vector3()), length=(DataTypes.Float, 0.0)):
        '''Resizes a vector to "length".'''
        return pyrr.Vector3(pyrr.vector.set_length(v, length))

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.FloatVector3, pyrr.Vector3()), meta={'Category': 'Math|Vector3', 'Keywords': ['vector3']})
    def v3GenerateNormals(v1=(DataTypes.FloatVector3, pyrr.Vector3()), v2=(DataTypes.FloatVector3, pyrr.Vector3()), v3=(DataTypes.FloatVector3, pyrr.Vector3()), norm=(DataTypes.Bool, True)):
        '''Generates a normal vector for 3 vertices.\nThe result is a normalized vector.\nIt is assumed the ordering is counter-clockwise starting at v1, v2 then v3.'''
        return pyrr.Vector3(pyrr.vector3.generate_normals(v1, v2, v3, norm))

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Vector3', 'Keywords': ['vector3']})
    def v3X(v=(DataTypes.FloatVector3, pyrr.Vector3())):
        '''Returns x component of the vector3.'''
        return v.x

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Vector3', 'Keywords': ['vector3']})
    def v3Y(v=(DataTypes.FloatVector3, pyrr.Vector3())):
        '''Returns y component of the vector3.'''
        return v.y

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Vector3', 'Keywords': ['vector3']})
    def v3Z(v=(DataTypes.FloatVector3, pyrr.Vector3())):
        '''Returns z component of the vector3.'''
        return v.z
