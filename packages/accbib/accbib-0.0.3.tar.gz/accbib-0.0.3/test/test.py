import accbib as ab

dois = ['10.1103/physrevlett.98.243001']
bibdata = ab.fetchdois(dois)

ab.export('test.bib',bibdata,mathml=True,encoding='ASCII')

