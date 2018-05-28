
import os

from collections import defaultdict
from lxml import etree

def validate(path):
    graph = defaultdict(lambda: [])
    def validateHelper(path, graph):
        if graph.has_key(path):
            return graph
        print "Scanning schema: {0}".format(path)
        with open(path, 'r') as f:
            doc = etree.parse(f)
        root  = doc.getroot()
        for elem in root.getiterator():
            if not hasattr(elem.tag, 'find'): continue
            i = elem.tag.find('}')
            if i >= 0:
                elem.tag = elem.tag[i + 1:]
        items =  [t.attrib['schemaLocation'] for t in root.getchildren() if t.tag == 'include' ]
        graph[path] = items
        map(lambda x: validateHelper(os.path.join(os.path.dirname(path), x), graph), items)
    validateHelper(path, graph)
    return graph



class RDFNavigatorSingleFileScanner(object):
    def __init__(self, *args, **kwargs):
        self.fileName = kwargs.get('fileName', None)
        self.references = {}

    def analyze(self, *args, **kwargs):
        print "Analyzing file : {0}".format(self.fileName)
        with open(self.fileName, 'r') as f:
            doc = etree.parse(f)
        root  = doc.getroot()
        for elem in root.getiterator():
            if not hasattr(elem.tag, 'find'): continue
            i = elem.tag.find('}')
            if i >= 0:
                elem.tag = elem.tag[i + 1:]
        return self.__analyzeTextLibraries(root=root)
        
    
    def __analyzeTextLibraries(self, *args, **kwargs):
        tagName = 'TextLibraries'
        root = kwargs.get('root', None)
        if root is None:
            return
        libs = root.find(tagName)
        refs = {}
        if libs is not None:
            for lib in filter(lambda x: type(x.tag) == str, libs.getchildren()):
                refs[lib.attrib['Name']] = dict([(x.attrib['ID'], x.sourceline) for x in lib.getchildren() if type(x.tag) == str and x.attrib.has_key('ID')])
        return refs
        
    def __alayzeReferences(self, *args, **kwargs):
        pass
        
def qDomModelExample(filePath):
    pass


def main():
    #print validate('c:\IOWA\RDFTools_anycpu\PH\PHManagerXMLSchema.xsd')
    #fileScanner = RDFNavigatorSingleFileScanner(fileName='c:\IOWA\RDFTools_anycpu\SystemData\Platform\PredefinedResources.xml')
    #fileScanner.analyze()
    qDomModelExample('c:\IOWA\RDFTools_anycpu\SystemData\Platform\PredefinedResources.xml)

if __name__ == '__main__':
    main()