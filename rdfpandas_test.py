from rdfpandas.graph import to_dataframe
import pandas as pd
import rdflib

g = rdflib.Graph()
# Insert a HTTP URL or a file in the same folder
#g.parse('http://babelnet.org/rdf/data/s00008556n?output=xml', format = 'xml')
#g.parse('tgn_1000070.rdf', format = 'xml')
#g.parse('http://vocab.getty.edu/tgn/1000070', format = 'xml')
#g.parse('http://entity.europeana.eu/entity/agent/base/60305?wskey=apidemo', format = 'xml')
#g.parse('https://yago-knowledge.org/resource/29th_century', format = 'ttl')
g.parse('http://lod.openlinksw.com/sparql?query=define%20sql%3Adescribe-mode%20%22CBD%22%20%20DESCRIBE%20%3Chttp%3A%2F%2Fdbpedia.org%2Fresource%2FCategory%3A1967%3E&output=application%2Frdf%2Bxml', format = 'xml')

print(g)

# df = to_dataframe(g)
# print(df)
# #Select a row
# new = df.loc['tgn:1000070']
# #new = df.loc['bn:s00008556n']
# #Transpose for better visibility for one long row
# trans = new.T
# #print(trans)
# trans.to_csv('rdfpandas_test_getty_tgn_web.csv', index = True, index_label = "@id")
