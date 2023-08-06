from urllib.parse import uses_relative
import urllib.request
from urllib.error import HTTPError,URLError
from pybtex.database import BibliographyData,Entry,Person
import json
import os
from . import ioxml
from . import iobib
from . import translator
import copy

def testfun(p1,p2):
    return translator.jnameTranslator(jname=p1,jnStyle=p2)

def journalEnroll(jname=None):
    (fullname, abbrname) = translator.EnrollUI(jname)
    if (fullname is not None) and (abbrname is not None):   
        translator.updateUsrList(fullname,abbrname)

def authors2person(authors):
    new_authors = []
    for author in authors:
        pers = Person()
        given_name = author.get('given')
        if given_name is not None:
            strs = given_name.split(' ')
            pers.first_names = [strs[0]]
            if len(strs)>1:
                pers.middle_names = strs[1:]
        last_name = author.get('family')
        if last_name is not None:
            pers.last_names = [last_name]
        new_authors.append(pers)
    return new_authors

def json2entry(jstr):
    fields = {}
    keymaps = dict(
        doi='DOI',
        journal='container-title',
        number='issue',
        pages='page',
        publisher='publisher',
        title='title',
        url='URL',
        volume='volume',
        city='city',
        edition='edition-number',
        issn = 'ISSN',
        journal_full = 'container-title',
        #journal_abbr = 'container-title-short'
        )
    for key,value in keymaps.items():
        data = jstr.get(value)
        if data is not None:
            data = str(data)
            data = data.strip().strip(r'{}[]')
            if data!='':
                fields[key] = data
    
    if fields.get('pages') is None:
        pages = jstr.get('article-number')
        if pages is not None:
            fields['pages'] = pages

    # get three type of years and select the earliest one
    years = []
    try:
        yr1 = str(jstr['published-print']['date-parts'][0][0])
        years.append(int(yr1))
    except:
        pass
    try:
        yr2 = str(jstr['created']['date-parts'][0][0])
        years.append(int(yr2))
    except:
        pass
    try:
        yr3 = str(jstr['published']['date-parts'][0][0])
        years.append(int(yr3))
    except:
        pass
    if len(years)>0:
        fields['year'] = str(min(years))
    
    type_ = jstr.get('type','journal-article')
    type_ = translator.jtypeTranslator(type_,itype='json',otype='bib')

    #get journal abbreviation
    try:
        fields['journal'] = fields['journal'].strip()
        if len(fields['journal']) > 0:
            fields['journal_abbr'] = translator.jnameTranslator(fields['journal'],'abbr')
        else:
            fields['journal_abbr'] = ''
    except:
        pass
    # set check flag
    fields['doichecked'] = 'True'

    # covert to Entry
    ety = Entry(type_,fields=fields)
    authors = jstr.get('author')
    if authors is not None:
        pers = authors2person(authors)
        ety.persons['author'] = pers
    editors = jstr.get('editor')
    if editors is not None:
        pers = authors2person(editors)
        ety.persons['editor'] = pers
    
    return ety

def etytag(ety):
    try:
        lastname = ety.persons['author'][0].last_names[0]
        # convert unicode charaters to ascii
        lastname = translator.uni2ascii(lastname)
    except:
        lastname = 'Anonymity'
    try:
        year = ety.fields['year']
    except:
        year = '1900'
    return lastname+year
    
    pass

def entries2bib(entries,tags=[]):
    etyDict = {}
    N1 = len(entries) - len(tags)
    tags = tags+ [None]*N1
    for ii, ety in enumerate(entries):
        if tags[ii] is None:
            try:
                #tag = ety.persons['author'][0].last_names[0]+ety.fields['year']
                tag = etytag(ety)
            except:
                tag = 'reftag'
        else:
            tag = tags[ii]
        # check if tag already exists in previous tags
        if tag in tags[0:ii]:
            ii=1
            while (tag+f'_{ii:d}') in tags[0:ii]:
                ii += 1
            tag = tag+f'_{ii:d}'
        # add ety to dict
        tags[ii] = tag
        etyDict[tag] = ety
    return BibliographyData(entries=etyDict)

# if not found online, use default
def defaultBibety(doi,userlib=None,reason='unkown reason'):
    if userlib is not None:
        try:
            for entag in userlib.entries:
                ety = userlib.entries[entag]
                if ety.fields['doi'] == doi:
                    print(f'{doi} was found in userlib!')
                    return ety
        except:
            pass
    
    jdict = dict(title='Doi lookup failed!',
                 DOI=doi,
                 author=[{'family':'Anom','given':'Anom'}]
                 )
    jstr = json.dumps(jdict)
    jobj = json.loads(jstr)
    print(f'Default bib data was used for {doi}')
    return json2entry(jobj)
    
def fetchadoi(doi,userlib=None,message=True):
    # look up doi on website
    BASE_URL = 'http://dx.doi.org/'
    url = BASE_URL + doi
    req = urllib.request.Request(url)
    req.add_header('Accept', 'application/vnd.citationstyles.csl+json')
    tout = 10
    while True:
        try:
            f = urllib.request.urlopen(req,timeout=tout)
            jstr = f.read().decode()
            jobj = json.loads(jstr)
            if message:
                print(f'{doi} was successfully looked up!')
            return json2entry(jobj)
        except HTTPError:
            return defaultBibety(doi,userlib=userlib,reason='HTTPError')
        except (TimeoutError,URLError):
            # time out
            if (tout>=30):
                return defaultBibety(doi,userlib=userlib, reason='TIMEOUT')
            else:
                tout = tout + 10
        except:
            return defaultBibety(doi,userlib=userlib)
     
def fetchdois(dois,userlib=None):
    # dois: list of doi
    if isinstance(dois,str):
        dois = [dois]

    entries = []
    for ii, doi in enumerate(dois):
        # get rid of duplicate dois
        if doi in dois[0:ii]:
            continue
        ety = fetchadoi(doi,userlib=userlib)
        entries.append(ety)
    
    # add tags for each ref
    bibdata = entries2bib(entries)
    return bibdata

def checkbib(bibdata,checkdoi=0,message=True):
    checkdoi = int(checkdoi)
    # if do not check
    if checkdoi==0:
        return bibdata

    ii = 0
    for ent in bibdata.entries:
        ii = ii + 1

        ety = bibdata.entries[ent]
        
        try:
            doichecked = ety.fields['doichecked'].strip().strip(r'{}[]')
        except:
            doichecked = 'false'
        
        # if already checked
        if (checkdoi==1) and (doichecked.lower()=='true'):
            if message:
                print(f'{ii}:   {doi} skipped!')
            continue
        
        # if already checked but need re-check or not checked
        try:
            doi = ety.fields['doi'].strip().strip(r'{}[]')
        except:
            if message:
                print(f'{ii}:   {doi} not found!')
            # if no doi found
            continue
        
        ety2 = fetchadoi(doi,message=False)
        if ety2.fields['title']=='Doi lookup failed!':
            if message:
                print(f'{ii}:   {doi} failed!')
            continue
        else:
            if message:
                print(f'{ii}:   {doi} succeed!')
            # type
            newtype = ety2.type
            if newtype!='':
                ety.type = newtype
            # fields
            for key, value in ety2.fields.items():
                ety.fields[key]= value
            # person
            ety.persons = ety2.persons
    return bibdata

def export(filename,bibdata,mathml=True,jnStyle='full',encoding='ASCII'):
    exts = ['.bib','.xml']
    extension = os.path.splitext(filename)[1]
    if extension.lower() not in exts:
        extension = exts[0]
        filename = filename+extension
    
    if extension == '.bib':
        iobib.export2bib(filename,bibdata,mathml=mathml,jnStyle=jnStyle,encoding=encoding)
    
    if extension == '.xml':
        ioxml.export2xml(filename,bibdata,jnStyle=jnStyle)

def doi2db(dois,outfile):
    bibdata = fetchdois(dois)
    export(outfile,bibdata)

def loadbib(filename,checkdoi=0):
    checkdoi = int(checkdoi)
    bibdata = iobib.importbib(filename)
    if checkdoi>0:
        bibdata = checkbib(bibdata,checkdoi=checkdoi)
    return bibdata

def loadxml(filename,checkdoi=0):
    entries,tags = ioxml.importxml(filename)
    bibdata = entries2bib(entries,tags=tags)
    if checkdoi>0:
        bibdata = checkbib(bibdata,checkdoi)
    return bibdata

def loadois(filename,userlib=None):
    dois = []
    with open(filename, "r") as infile:
        while True:
            line = infile.readline()
            if not line:
                break
            else:
                doi = line.strip()
                doi = line.strip(',.;"').strip()
                if len(doi)>8:
                    dois.append(doi)
    if userlib is not None:
        userlib = loaddb(userlib,checkdoi=0)
    bibdata = fetchdois(dois,userlib=userlib)
    return bibdata

def loaddb(filename,format=None,checkdoi=0):
    if format is None:
        extension = os.path.splitext(filename)[1]
        if extension=='.bib':
            return loadbib(filename,checkdoi=checkdoi)
        elif extension=='.xml':
            return loadxml(filename,checkdoi=checkdoi)
        else:
            return None
    elif format == 'bib':
         return loadbib(filename,checkdoi=checkdoi)
    elif format == 'xml':
         return loadbib(filename,checkdoi=checkdoi)
    else:
        return None

def bib2db(infile,outfile,checkdoi=0):
    bibdata = iobib.importbib(infile)
    if checkdoi>0:
        bibdata = checkbib(bibdata,checkdoi=checkdoi)
    export(outfile,bibdata)

def xml2db(infile,outfile,checkdoi=0):
    bibdata = ioxml.importxml(infile)
    if checkdoi>0:
        bibdata = checkbib(bibdata)
    export(outfile,bibdata)

def texbib(bibdata_in):
    bibdata = copy.deepcopy(bibdata_in)
    for ent in bibdata.entries:
        ety = bibdata.entries[ent]
        # process title, convert formula to latex code
        try:
            title = ety.fields['title'].strip().strip(r'{}[]')
            ety.fields['title'] = translator.mathml_processor(title)
        except:
            pass
        if False:
            # process author name, convert unicode char to latex code
            try:
                for per in ety.persons['author']:
                    per.first_names = [translator.uni2tex(ii) for ii in per.first_names]
                    per.middle_names = [translator.uni2tex(ii) for ii in per.middle_names] 
                    per.last_names = [translator.uni2tex(ii) for ii in per.last_names]
            except:
                pass
            # process editor name, convert unicode char to latex code
            try:
                for per in ety.persons['editor']:
                    per.first_names = [translator.uni2tex(ii) for ii in per.first_names]
                    per.middle_names = [translator.uni2tex(ii) for ii in per.middle_names] 
                    per.last_names = [translator.uni2tex(ii) for ii in per.last_names]
            except:
                pass
    return bibdata