from lxml import etree as ET
from pybtex.database import Entry,Person
from . import translator

def pretty_xml(element,indent='\t',newline='\n',level=0):
    if len(element):
        if (element.text is None) or element.text.isspace():
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent*(level+1) + element.text.strip() + newline + indent*(level+1)
    
    temp = list(element)
    for subelement in temp:
        if temp.index(subelement) < (len(temp)-1):
            subelement.tail = newline + indent*(level+1)
        else:
            subelement.tail = newline + indent*level
        pretty_xml(subelement,indent,newline,level=level+1)

def XML_NewNode(tag,name=None,text=None,Attr={}):
    # generate new node with tag name (tag)
    NewNode = ET.Element(tag)
    # add attributes
    if name is not None:
        NewNode.set('Name',name)
    if text is not None:
        NewNode.text=f'{text}'
    for key in Attr:
        NewNode.set('%s'%key,'%s'%(Attr[key]))
    return NewNode

def XML_LocalName(tag):
    # tag may have namespace as : '{namespace}tag'
    # grid of namespace by splitting with '}'
    return tag.split('}')[-1]

def XML_Initialize(filename,rootTag='Sources',rootAttrs={},pretty=True):
    rootAttrs['xmlns']=r'http://schemas.openxmlformats.org/officeDocument/2006/bibliography'
    # Generate XML
    root = ET.Element(rootTag)
    for key in rootAttrs:
        AttrStr = rootAttrs[key]
        root.set(f'{key:s}',f'{AttrStr:s}')

    tree = ET.ElementTree(root)
    # format xml
    if(pretty):
        pretty_xml(root)
    # save xml
    tree.write(filename, encoding='utf-8', xml_declaration=True)

def XML_ReadChildNodeText(parentNode,nodeTag,default=None):
    node = parentNode.xpath(nodeTag)
    if(len(node)<1):
        return default
    else:
        result = node[0].text.strip()
        return result
    
def XML_ReadChildrenAsDict(parentNode,excludes=[]):
    children = parentNode.xpath('*')
    if(len(children)==0):
        return None
    result = {}
    for node in children:
        key = node.tag
        key = XML_LocalName(key)
        if key in excludes:
            continue
        try:
            value = node.text.strip()
            result[key]=value
        except:
            pass
    return result

def XML_FieldsNode(fields,jnStyle='full'):
    nodes =[]
    # title needs special care
    try:
        title = fields.pop('Title')
        title = formatTitle(title)
        if (title!='') and title is not None:
            nodes.append(XML_NewNode('Title',text=title))
    except:
        pass
    # journal name needs special care
    try:
        jn = fields.pop('JournalName')
        jn = jn.strip().strip(r'{}')
        if jn is not None:
            jn = translator.jnameTranslator(jn,jnStyle=jnStyle)
            nodes.append(XML_NewNode('JournalName',text=jn))
    except:
        pass
    #other fields
    for key, value in fields.items():
        if (value!='') and (value is not None):
            value = value.strip().strip('{}')
            nodes.append(XML_NewNode(key,text=value.strip()))
    return nodes

def XML_PersonNode(person):
    ndPerson = XML_NewNode('Person')
    if (person.last_names!='') and (person.last_names is not None):
        ndPerson.append(XML_NewNode('Last',text=catnames(person.last_names)))
    if (person.first_names!='') and (person.first_names is not None):
        ndPerson.append(XML_NewNode('First',text=catnames(person.first_names)))
    if (person.middle_names!='') and (person.middle_names is not None):
        ndPerson.append(XML_NewNode('Middle',text=catnames(person.middle_names)))
    return ndPerson

def XML_AuthorNode(authors):
    nodes = []
    for key, value in authors.items():
        if len(value)==0:
            continue
        ndAuthor = ET.Element(key.capitalize())
        ndNameList = ET.Element('NameList')
        for person in value:
            ndNameList.append(XML_PersonNode(person))
        ndAuthor.append(ndNameList)
        nodes.append(ndAuthor)
    
    if len(nodes)>0:
        res = ET.Element('Author')
        for node in nodes:
            res.append(node)
    else:
        res = None
    return res

def XML_AuthorNodeParser(etyNode,who='Author'):
    authors = []
    #rpath = f'Author\\{who}\\NameList\Person'
    rpath = '*[local-name() = \'Author\']'
    rpath = rpath + '/'+ f'*[local-name() = \'{who}\']'
    rpath = rpath + '/' + f'*[local-name() = \'NameList\']'
    rpath = rpath + '/' + f'*[local-name() = \'Person\']'
    cNodes = etyNode.xpath(rpath)
    if len(cNodes) == 0:
        return authors
    else:
        for pNode in cNodes:
            temp = Person()
            pers = XML_ReadChildrenAsDict(pNode)
            last_name = pers.get('Last')
            if last_name is not None:
                temp.last_names = last_name.strip().split(' ')
            first_name = pers.get('First')
            if last_name is not None:
                temp.first_names = first_name.strip().split(' ')
            middle_name = pers.get('Middle')
            if middle_name is not None:
                temp.middle_names = middle_name.strip().split(' ')
            
            authors.append(temp)
        return authors

def catnames(names):
    ns = ''
    for name in names:
        ns = ns +' ' + name
    ns = ns.strip()
    ns = ns.strip('{}')
    return ns.strip()

def getType(entry):
    bibtype = entry.type
    bibtype = bibtype.strip().strip(r'{}[]')
    types = dict(
        article='JournalArticle',
        book='Book',
        incollection='BookSection',
        inproceedings='ConferenceProceedings',
        misc='InternetSite')

    if bibtype in types.keys():
        return types[bibtype]
    else:
        return bibtype

def formatTitle(title):
    if title.lower().strip() in ['{no title}','no title']:
        title = ''
    title = title.strip(r'{}')
    return title

def getFields(entry,field):
    try:
        data = entry.fields[field]
        return data.strip()
    except:
        return None

def export2xml(filename,bibdata,jnStyle='full'):
    XML_Initialize(filename)
    root = ET.parse(filename).getroot()
    tree = ET.ElementTree(root)

    for ent in bibdata.entries:
        ety = bibdata.entries[ent]
        ndSource = XML_NewNode('Source')

        # Source type
        ndSource.append(XML_NewNode('SourceType',text=getType(ety)))

        # Tag
        ndSource.append(XML_NewNode('Tag',text=ent))

        # author
        ndSource.append(XML_AuthorNode(ety.persons))

        # fields
        fields = translator.fieldsTranslator(ety.fields,dst='xml')
        fdsNodes = XML_FieldsNode(fields,jnStyle=jnStyle)
        for node in fdsNodes:
            ndSource.append(node)

        root.append(ndSource)

    pretty_xml(root,indent='  ')
    # save xml
    tree.write(filename, encoding='utf-8', xml_declaration=True)

def importxml(filename):
    entries = []
    tags = []
    root = ET.parse(filename).getroot()
    path_str = '*[local-name() = \'Source\']'
    entNodes = root.xpath(path_str)
    if len(entNodes) > 0:
        for entNode in entNodes:
            data = XML_ReadChildrenAsDict(entNode,excludes=['Author'])
            # type
            try:
                type_ = data.pop('SourceType')
            except:
                type_ = "article"
            # tag
            try:
                tag = data.pop('Tag')
            except:
                 tag = None
            tags.append(tag)
            fields = translator.fieldsTranslator(data,dst='bib')
            ety = Entry(type_,fields=fields)
            # authors
            authors = XML_AuthorNodeParser(entNode,who='Author')
            editors = XML_AuthorNodeParser(entNode,who='Editor')
            ety.persons['author'] = authors
            ety.persons['editor'] = editors
            entries.append(ety)
    # combine all entries as a BibliographyData object
    return (entries,tags)


