from ..Core.FunctionLibrary import *
from ..Core.AGraphCommon import *

import sys
import os
import ast

from shotgun_api3 import Shotgun

ca_certs = os.path.join(r"C:\Users\pedro\OneDrive\pcTools_v5\pcSequenceExplorer\modules", 'shotgun_api3','lib','httplib2', 'cacerts.txt')
sg_script_name = "PC_Tools"
sg_script_key = "351db1c30bedafb4a04b9de6fb7ab5fe429b92266438b442bddce9065108c282"


registerDatatype("Sg")
registerDatatype("SgFilter")

class sgFilters():
    def __init__(self,project=None,
                        code=None,
                        id=None,
                        name=None,
                        sg_sequence=None,
                        task_template=None,
                        image="None",
                        entity=None,
                        sg_operator=None,
                        sg_hours=None,
                        sg_task=None,
                        sg_date=None,
                        entity_type=None,
                        layout_project=None,
                        link=None):
        self.project = project
        self.code = code
        self.id = id
        self.name = name
        self.sg_sequence = sg_sequence
        self.task_template = task_template
        self.image = image
        self.entity = entity
        self.sg_operator = sg_operator
        self.sg_hours = sg_hours
        self.sg_task= sg_task
        self.sg_date=sg_date
        self.entity_type = entity_type
        self.layout_project = layout_project
        self.link=link
    def __getSearchFilters__(self):
        filters =[]
        for name, obj in inspect.getmembers(self):
            if not "__" in name and name != 'image':
                if str(obj) != "None" and str(obj) != "" :
                    if isinstance(obj,str):
                        if obj[0]== "{" and obj[-1] == "}":
                            obj = ast.literal_eval(obj)
                    filters.append([name, 'is', obj])
        return filters
    def __getCreateFilters__(self):
        filters ={}
        for name, obj in inspect.getmembers(self):
            if not "__" in name:
                if name != 'image' and str(obj) != "None" and str(obj) != '':
                    if isinstance(obj,str):
                        if obj[0]== "{" and obj[-1] == "}":
                            obj = ast.literal_eval(obj)                      
                        filters[name]=obj
                if name == 'image' and str(obj) != 'None' and str(obj) != '':                 
                    filters[name]=obj                   
        return filters


class ShotGunLib(FunctionLibraryBase):
    '''
    Default library builting stuff, variable types and conversions
    '''
    def __init__(self):
        super(ShotGunLib, self).__init__()

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Sg, None), meta={'Category': 'Shotgun', 'Keywords': ["Shotgun","Connect"]})
    ## Shotgun Connect
    def sgConnect(script_name=(DataTypes.String, sg_script_name),script_key=(DataTypes.String, sg_script_key)):
        '''make integer'''    
        try:
            sg = Shotgun("https://entropystudio.shotgunstudio.com",script_name,script_key,ca_certs=ca_certs)
            sg.find("Project",[],[])
            return(sg)
        except:
            print "error"
            return(DataTypes.Sg, None)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.SgFilter, sgFilters()), meta={'Category': 'Shotgun|Filters', 'Keywords': ["Shotgun","Filter"]})
    ## Shotgun Connect
    def sgFilter(
                project=(DataTypes.String,""),
                code=(DataTypes.String,""),
                sg_id=(DataTypes.String,""),
                name1=(DataTypes.String,""),
                sg_sequence=(DataTypes.String,""),
                task_template=(DataTypes.String,""),
                image=(DataTypes.String,""),
                entity=(DataTypes.String,""),
                sg_operator=(DataTypes.String,""),
                sg_hours=(DataTypes.Float,0),
                sg_task=(DataTypes.String,""),
                sg_date=(DataTypes.String,""),
                entity_type=(DataTypes.String,""),
                layout_project=(DataTypes.String,""),
                link=(DataTypes.String,"")
                ):
        '''make sg Filter'''    
        try:
            sg = sgFilters(project=project,code=code,id=sg_id,name=name1,sg_sequence=sg_sequence,task_template=task_template,image=image,entity=entity,sg_operator=sg_operator,sg_hours=sg_hours,sg_task=sg_task,sg_date=sg_date,entity_type=entity_type,layout_project=layout_project,link=link)
            return(sg)
        except:
            print "error"
            return(DataTypes.SgFilter, None)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.SgFilter, sgFilters()), meta={'Category': 'Shotgun|Filters', 'Keywords': ["Shotgun","Filter","Shot"]})
    ## Shotgun Shot Filter
    def sgShotFilter(
                project=(DataTypes.String,""),
                code=(DataTypes.String,""),
                sg_id=(DataTypes.String,""),
                sg_sequence=(DataTypes.String,""),
                entity=(DataTypes.String,""),
                link=(DataTypes.String,""),
                image=(DataTypes.String,"")
                ):
        '''make sg Filter'''    
        try:
            sg = sgFilters(project=project,code=code,id=sg_id,sg_sequence=sg_sequence,entity=entity,link=link,image=image)
            return(sg)
        except:
            print "error"
            return(DataTypes.SgFilter, None)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.SgFilter, sgFilters()), meta={'Category': 'Shotgun|Filters', 'Keywords': ["Shotgun","Filter","Project"]})
    ## Shotgun Project Filter
    def sgProjectFilter(
                sg_id=(DataTypes.String,""),
                name1=(DataTypes.String,""),
                task_template=(DataTypes.String,""),
                layout_project=(DataTypes.String,""),
                ):
        '''make sg Filter'''    
        try:
            sg = sgFilters(id=sg_id,name=name1,task_template=task_template,layout_project=layout_project)
            return(sg)
        except:
            print "error"
            return(DataTypes.SgFilter, None)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.SgFilter, sgFilters()), meta={'Category': 'Shotgun|Filters', 'Keywords': ["Shotgun","Filter","Taks"]})
    ## Shotgun Task Filter
    def sgTaskFilter(
                project=(DataTypes.String,""),
                code=(DataTypes.String,""),
                sg_id=(DataTypes.String,""),
                entity=(DataTypes.String,""),
                sg_operator=(DataTypes.String,""),
                sg_hours=(DataTypes.Float,0),
                sg_task=(DataTypes.String,""),
                sg_date=(DataTypes.String,""),
                ):
        '''make sg Filter'''    
        #try:
        sg = sgFilters(project=project,code=code,id=sg_id,entity=entity,sg_operator=sg_operator,sg_hours=sg_hours,sg_task=sg_task,sg_date=sg_date)
        return(sg)
        #except:
        #    print "error"
        #    return(DataTypes.SgFilter, sgFilters())

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.String, "None"), meta={'Category': 'Shotgun', 'Keywords': ["Shotgun","Create","Find"]})
    ## Shotgun Find Or Create Entity
    def sgFindOrCreate( sg=(DataTypes.Sg, None),
                        entity_type=(DataTypes.String, "Shot"),
                        sgfilter=(DataTypes.SgFilter, sgFilters()),
                        create=(DataTypes.Bool, False),
                        fields=(DataTypes.Array, ["id","code"]),
                        new=(DataTypes.Reference, (DataTypes.Bool, False))):
        filters = sgfilter.__getSearchFilters__()
        try:
            sgItem = sg.find_one(entity_type,filters,fields)
        except:
            sgItem = None
        new2 = False
        if sgItem == None and create:
            filters = sgfilter.__getCreateFilters__()
            sgItem = sg.create(entity_type,filters)
            new2 = True
        new(new2)
        return sgItem

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.String, "None"), meta={'Category': 'Shotgun', 'Keywords': ["Shotgun","Update"]})
    ## Shotgun Update
    def sgUpdate(sg=(DataTypes.Sg, None),entity_type=(DataTypes.String, "Shot"),sg_id=(DataTypes.String,""),sgfilter=(DataTypes.SgFilter, sgFilters())):
        return sg.update(entity_type,sg_id,sgfilter.__getCreateFilters__())

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.String, "None"), meta={'Category': 'Shotgun', 'Keywords': ["Shotgun","Update"]})
    ## Shotgun Update
    def sgUpload(sg=(DataTypes.Sg, None),entity=(DataTypes.String, "Shot"),path=(DataTypes.String, ""),field_name=(DataTypes.String, 'sg_uploaded_movie'),display_name=(DataTypes.String, '')):
        if field_name == "":
            field_name = None
        if display_name == "":
            display_name = None  
        entity = ast.literal_eval(entity)   
        entity_type = entity["type"]
        sg_id = entity['id']
        return sg.upload(entity_type,sg_id,path,field_name,display_name)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Array,[]), meta={'Category': 'Shotgun', 'Keywords': ["Shotgun","Find"]})
    ## Shotgun Find Filtered
    def sgFindFiltered(sg=(DataTypes.Sg, None),entity_type=(DataTypes.String, "Shot"),sgfilter=(DataTypes.SgFilter, sgFilters()),fields=(DataTypes.Array, ["id","code"])):
        return sg.find(entity_type,sgfilter.__getSearchFilters__(),fields)

    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={'Category': 'Shotgun', 'Keywords': ["Shotgun","Connect"]})
    ## Shotgun Print
    def printSg(sg=(DataTypes.Sg, None)):
        '''make integer'''    
        print sg


