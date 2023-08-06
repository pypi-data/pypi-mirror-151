from pybtex.database.input import bibtex
from . import translator
import copy

def export2bib(filename,bibdata_in,mathml=True,jnStyle='full',encoding='ASCII'):
    # copy the bibdata_in
    bibdata = copy.deepcopy(bibdata_in)
    #etyDict = {}
    for ent in bibdata_in.entries:
        ety = bibdata.entries[ent]
        # convert journal name to jnStyle (abbr or full)
        try:
            jn = ety.fields['journal'].strip().strip(r'{}[]')
            ety.fields['journal'] = translator.jnameTranslator(jn,jnStyle=jnStyle)
        except:
            pass
        
        if mathml:
            # process title, convert formula to latex code
            try:
                title = ety.fields['title'].strip()
                ety.fields['title'] = translator.mathml_processor(title)
            except:
                pass
        
        ent2 = translator.uni2ascii(ent)
        # convert tag
        if (ent2!=ent and encoding.lower()=='ascii'):
            bibdata.entries[ent2] = bibdata.entries[ent]
            bibdata.entries.pop(ent)
        if encoding.lower()=='ascii':
            # this part can be done with "encoding='ASCII'" in most cases, but would fail if 'Mn' char exists
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
    
    bibstr = bibdata.to_string(bib_format='bibtex',encoding=encoding)
    # undo the bashslash insertion
    #\#$\%^\&*()\_
    bibstr = bibstr.replace('\#','#')
    bibstr = bibstr.replace('\%','%')
    bibstr = bibstr.replace('\&','&')
    bibstr = bibstr.replace('\_','_')
    savestr(filename,bibstr,encoding=encoding)
    #bibdata.to_file(filename,bib_format='bibtex',encoding=encoding)
    print(f'saved as {filename}')

def savestr(filename,bibstr,encoding='ASCII'):
    with open(filename,'w+',encoding=encoding) as fout:
        fout.write(bibstr)

def importbib(filename):
    parser = bibtex.Parser()
    bibdata = parser.parse_file(filename)
    return bibdata