# -*- coding: utf-8 -*-
"""
Created on Mon May 14 13:34:03 2018

@author: z003umpb
"""
from rdfnavigatorchildren  import RDFNavigatorChildrenTypes,\
                                  RDFNavigatorXmlChild,\
                                  RDFNavigatorSchemaChild,\
                                  RDFNavigatorTemplateChild


class RDFNavigatorChildrenFactory(object):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
    
    def createObject(self, childType):
        child = None
        if childType in [RDFNavigatorChildrenTypes.RDF, RDFNavigatorChildrenTypes.XML]:
            child = RDFNavigatorXmlChild(self.parent)
            child.output_message.connect(self.parent.output_message)
        elif childType == RDFNavigatorChildrenTypes.SCHEMA:
            child = RDFNavigatorSchemaChild(self.parent)
        elif childType == RDFNavigatorChildrenTypes.TEMPLATE:
            child = RDFNavigatorTemplateChild(self.parent)
            child.crossRefRequested.connect(self.parent.showReference)
            child.crossRefValueRequested.connect(self.parent.showReferenceValue)
            child.bookmark_added.connect(self.parent.bookmarskWidget.addBookmark)
            child.bookmark_deleted.connect(self.parent.bookmarskWidget.removeBookmark)
        return child