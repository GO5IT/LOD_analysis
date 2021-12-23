import pickle
import rdfpandas
from rdfpandas.graph import to_dataframe
import pandas as pd
import rdflib

g = rdflib.Graph()
g.parse('https://api.europeana.eu/entity/agent/base/60305?wskey=apidemo', format = 'json-ld')
#g.parse(r"https://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=DESCRIBE%20%3Chttp%3A%2F%2Fdbpedia.org%2Fresource%2F1968%3E&format=application%2Fjson-ld", format = 'json-ld')
#g.parse('http://id.worldcat.org/fast/1037825.rdf.xml', format = 'xml')

df = to_dataframe(g)
df.to_csv('rdfpandas_test2.csv', index = True, index_label = "@id")