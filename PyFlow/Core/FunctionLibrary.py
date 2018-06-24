"""@file FunctionLibrary.py

This file contains decorator for implementing node from function.

The main idea is to describe argument types and default values.

Using this information it becomes possible to create pins according to arguments types.
"""
from inspect import getargspec
from AGraphCommon import *
from Settings import Colors
empty = {}


## Turns function into a node
# @param[in] func decorated function
# @param[in] returns it can be tuple with [data type identifier](@ref PyFlow.Core.AGraphCommon.DataTypes) + default value, or None
# @param[in] meta dictionary with category path, keywords and any additional info
# @param[in] nodeType determines wheter it is a Pure node or Callable. If Callable - input and output execution pins will be created
# @sa [NodeTypes](@ref PyFlow.Core.AGraphCommon.NodeTypes) FunctionLibraries
def IMPLEMENT_NODE(func=None, returns=empty, meta={'Category': 'Default', 'Keywords': []}, nodeType=NodeTypes.Pure,color=Colors.NodeBackgrounds):
    def wrapper(func):
        func.__annotations__ = getattr(func, '__annotations__', {})
        func.__annotations__['nodeType'] = nodeType
        func.__annotations__['color'] = color
        if not meta == empty:
            func.__annotations__['meta'] = meta

        if not returns == empty:
            func.__annotations__['return'] = returns

        defaults = func.__defaults__
        if defaults:
            spec = getargspec(func)

            nanno = len(defaults)
            for (i, name) in enumerate(spec.args[-nanno:]):
                if len(defaults[i]) < 1 or defaults[i][0] is empty:
                    continue
                if defaults[i][0] == DataTypes.Reference:
                    func.__annotations__[name] = defaults[i][1]
                else:
                    #print defaults[i][0]
                    if defaults[i][0] == DataTypes.Any:
                        func.__annotations__[name] = [defaults[i]]
                    else:
                        func.__annotations__[name] = defaults[i][0]

            # defaults = tuple((d[1] for d in func.__defaults__ if len(d) > 1))
            customDefaults = []
            for d in func.__defaults__:
                if len(d) > 1:
                    if isinstance(d[1], tuple):
                        customDefaults.append(d[1][1])
                    else:
                        customDefaults.append(d[1])
            # func.__defaults__ = defaults or None
            func.__defaults__ = tuple(customDefaults) or None
        return func

    if returns == empty:
        return wrapper(func)
    return wrapper


## Base class for all function libraries
# some common utilities can be moved here in future
class FunctionLibraryBase(object):
    def __init__(self):
        super(FunctionLibraryBase, self).__init__()
        self.__foos = inspect.getmembers(self, inspect.isfunction)

    def getFunctions(self):
        return self.__foos
