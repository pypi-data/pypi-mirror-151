import numpy as np
import logging
import json
import os
import tkinter as tk
from lxml import etree
import unicodedata
from importlib_resources import files, as_file
from accbib import data

accents = {
    0x0300: '`', 0x0301: "'", 0x0302: '^', 0x0308: '"',
    0x030B: 'H', 0x0303: '~', 0x0327: 'c', 0x0328: 'k',
    0x0304: '=', 0x0331: 'b', 0x0307: '.', 0x0323: 'd',
    0x030A: 'r', 0x0306: 'u', 0x030C: 'v',
}

def EnrollUI(journame=None):
    if (journame is None) or len(journame.strip())==0:
        msg = "Please input the following infomation of the journal:"
    else:
        msg = f"Please input the following infomation of \"{journame.strip()}\":"
    #Create a Toplevel window
    winUI= tk.Tk()
    #winUI.geometry("750x250")
    winUI.title("Journal Enrollment")

    lblInfo = tk.Label(winUI,text=msg,anchor='w')
    lblInfo.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky='w')
    #lblInfo.pack(side=tk.TOP,padx=10,pady=10,fill=tk.BOTH, expand=True)
    #Create Widgets for full name input
    lblFullname = tk.Label(winUI,text="Journal Full name:")
    lblFullname.grid(row=1, column=0,sticky='w')
    fullEntry= tk.Entry(winUI,width=60)
    fullEntry.grid(row=1, column=1,columnspan=2, padx=10, pady=5,sticky='we')

    #Create Widgets for abbr name input
    lblAbbrname = tk.Label(winUI,text="Journal Abbreviation:")
    lblAbbrname.grid(row=2, column=0,sticky='w')
    abbrEntry= tk.Entry(winUI,width=60)
    abbrEntry.grid(row=2, column=1,columnspan=2, padx=10, pady=5,sticky='we')

    #Create a Button to print something in the Entry widget
    btnCancel = tk.Button(winUI,text= "Cancel",width=20,command=lambda: winUI.destroy())
    btnCancel.grid(row=3,column=1, padx=10, pady=5,sticky='e')
    btnOK= tk.Button(winUI, text="Ok", width=20,command=lambda: winUI.quit())
    btnOK.grid(row=3,column=2, padx=10, pady=5,sticky='e')
    # show window
    winUI.attributes('-topmost',True)
    winUI.mainloop()
    try:
        fullname = fullEntry.get().strip()
        abbrname = abbrEntry.get().strip()
        if len(fullname)==0:
            fullname = None
        if len(abbrname)==0:
            abbrname = None
    except:
        fullname = None
        abbrname = None
    try:
        winUI.destroy()
    except:
        pass

    return (fullname,abbrname)

def listLookup(jname,listFile,jnStyle='abbr'):
    jname2 = jname.lower()
    try:
        jourlist = json.load(open(listFile,encoding='utf-8'))
        for key,value in jourlist.items():
            if (key.lower()==jname2) or (value.lower()==jname2):
                if jnStyle.lower()=='abbr':
                    return value
                else:
                    return key
    except:
        return None
    
    return None

def updateUsrList(key,value):
    sourcefile = files(data).joinpath('JourList_user.json')
    if os.path.exists(sourcefile):
        jourlist = json.load(open(sourcefile,encoding='utf-8'))
    else:
        jourlist = {}

    jourlist[key] = value
    with open(sourcefile, 'w', encoding='utf-8') as f:
        json.dump(jourlist, f, ensure_ascii=False, indent=4)
    
def jnameTranslator(jname,jnStyle='abbr'):
    # lookup in user list
    sourcefile = files(data).joinpath('JourList_user.json')
    jname_out = listLookup(jname,sourcefile,jnStyle=jnStyle)
    if jname_out is not None:
        return jname_out

    # lookup in pre-defined list
    sourcefile = files(data).joinpath('JourList.json')
    jname_out = listLookup(jname,sourcefile,jnStyle=jnStyle)
    if jname_out is not None:
        return jname_out
    
    # ask user to provide the info
    (fullname, abbrname) = EnrollUI(jname)
    if (fullname is not None) and (abbrname is not None):
        updateUsrList(fullname,abbrname)
        if jnStyle.lower()=='abbr':
            return abbrname
        else:
            return fullname

    # all failed
    print(f'The {jnStyle} name of {jname} is not found!')
    return jname

def jtypeTranslator(jtype, itype='bib',otype='xml'):
    typetbl = np.array([['article','JournalArticle','journal-article'],
                        ['book','Book','book'],
                        ['inproceedings','ConferenceProceedings','proceedings-article']
                      ])

    if itype == 'xml':
        indi = 1
    elif itype == 'json':
        indi = 2
    else:
    # take as 'bib'
        indi = 0

    if otype == 'xml':
        indo = 1
    elif otype == 'json':
        indo = 2
    else:
    # take as 'bib'
        indo = 0
    # if input type equals to output type
    if itype == otype:
        return jtype
    
    ind = np.where(np.char.lower(typetbl[:,indi])==jtype.lower())
    try:
        ind = ind[0][0]
        res = typetbl[ind][indo]
        return res
    except:
        return jtype
    
def fieldsTranslator(fields,dst='bib'):
    xmlfields = ['URL','Issue', 'JournalName','City',   'DOI']
    bibfields = ['url','number','journal',    'address','doi']
    if dst.lower()=='bib':
        lut = xmlfields
        out = bibfields
        convertor = str.lower
    elif dst.lower()=='xml':
        lut = bibfields
        out=xmlfields
        convertor = str.capitalize
    else:
        logging.warn(f'undefined dst paramters: {dst}')
        return fields
    
    outfields = {}
    for key,value in fields.items():
        try:
            ind = lut.index(key)
            key2 = out[ind]
        except:
            key2 = convertor(key)
        outfields[key2] = value
    
    return outfields

def mathml2tex(equation):
    """ MathML to LaTeX conversion with XSLT from Vasil Yaroshevich """
    xslt_file = files(data).joinpath('xsl_yarosh/mmltex.xsl')
    xslt_file = str(xslt_file)
    dom = etree.fromstring(equation)
    xslt = etree.parse(xslt_file)
    transform = etree.XSLT(xslt)
    newdom = transform(dom)
    newdom = str(newdom)
    return newdom

def mathml_processor(mathstr):
    Ind0 = mathstr.find('<mml')
    while(Ind0!=-1):
        Ind1 = mathstr.find('math>')
        if Ind1 == -1:
            break;
        temp = mathstr[Ind0:Ind1+5]
        try:
            tex = mathml2tex(temp)
        except:
            tex = temp
        mathstr = mathstr[0:Ind0] + ' '+ tex + ' ' + mathstr[Ind1+5:]
        Ind0 = mathstr.find('<mml')
    
    mathstr = mathstr.replace('\n','')
    return mathstr

def uni2tex(text):
    out = ""
    txt = tuple(text)
    i = 0
    while i < len(txt):
        char = text[i]
        code = ord(char)

        # combining marks
        if unicodedata.category(char) in ("Mn", "Mc") and code in accents:
            out += "\\%s{%s}" %(accents[code], txt[i+1])
            i += 1
        # precomposed characters
        elif unicodedata.decomposition(char):
            base, acc = unicodedata.decomposition(char).split()
            acc = int(acc, 16)
            base = int(base, 16)
            if acc in accents:
                out += "\\%s{%s}" %(accents[acc], chr(base))
            else:
                out += char
        else:
            out += char

        i += 1

    return out

def uni2ascii(text):
    out = ""
    txt = tuple(text)
    i = 0
    while i < len(txt):
        char = text[i]
        code = ord(char)
        # combining marks
        if unicodedata.category(char) in ("Mn", "Mc") and code in accents:
            out += "%s" %(txt[i+1])
            i += 1
        # precomposed characters
        elif unicodedata.decomposition(char):
            base, acc = unicodedata.decomposition(char).split()
            #acc = int(acc, 16)
            base = int(base, 16)
            out += "%s" %(chr(base))
        else:
            out += char
        i += 1
    return out