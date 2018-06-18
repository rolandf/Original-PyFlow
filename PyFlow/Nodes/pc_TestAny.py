from ..Core.AbstractGraph import *
from ..Core.Settings import *
from ..Core import Node

from Qt import QtWidgets

class pc_TestAny(Node):
    def __init__(self, name, graph):
        super(pc_TestAny, self).__init__(name, graph)
        self.A = self.addInputPin('A', DataTypes.Any,constraint=1)
        self.B = self.addInputPin('B', DataTypes.Any,constraint=1)
        self.A.dynamic = True
        self.C = self.addOutputPin("C",DataTypes.Any,constraint=1)

        pinAffects(self.A, self.C)
        pinAffects(self.B, self.C)

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
        #try:
        print self.A.getData()+self.B.getData()
            #self.C.setData(self.A.getData()+self.B.getData())
        #except Exception as e:
        #    print(e)
