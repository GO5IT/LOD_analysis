import pickle
import rdfpandas
from rdfpandas.graph import to_dataframe
import pandas as pd
import rdflib

# rdfpandas converts rdf (from URL) into dataframe
g = rdflib.Graph()
# Note on Rdfpandas
# Full HTTP entity URI may not work, so shortened URI should be used in Getty and Wikidata (e.g. wd:Q2648 and not http://www.wikidata.org/entity/Q2648)
# wd:Q2648, dbr:1968, bn:s02830721n,
# JSON-LD is not supported in rdfpandas
g.parse('https://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=DESCRIBE%20%3Chttp%3A%2F%2Fdbpedia.org%2Fresource%2F1968%3E&format=application%2Fjson-ld', format = 'json-ld')
# Wikidata Q2648.rdf and format=xml will return an error: rdf:nodeID value is not a valid NCName:
# Solution is to use Q2648.ttl and format=ttl
# Working URI examples:
#g.parse('https://www.wikidata.org/wiki/Special:EntityData/Q2648.ttl', format = 'ttl')
#g.parse('https://dbpedia.org/data/1968.ttl', format = 'ttl')

#g.parse('http://data.europeana.eu/entity/agent/base/60305', format = 'json-ld')
#g.parse('https://api.europeana.eu/entity/agent/base/60305?wskey=apidemo', format = 'json-ld')


df = to_dataframe(g)
#Select a row
#new = df.loc['http://experimental.worldcat.org/fast/29048']
#new = df.loc['https://dbpedia.org/resource/1968']
#new = df.loc['https://dbpedia.org/resource/1968']
# create 'entity' column as index of dataframe
#new['entity'] = new.index
#print(new.head)

# #Saving as CSV file
df_csv = df.to_csv('rdfpandas_test_euro_jsonld.csv', index = True, index_label = "@id")
# #Saving as Pickle file
# with open('test.pkl', 'wb') as f:
#     pickle.dump(df, f)
# #Reading Pickle file
# with open('test.pkl', 'rb') as f:
#     df = pickle.load(f)
# df['entity'] = df.index
# print(df.head)

# Search exact match text in "entity" column in dataframe
# x = df[df['entity'] == "http://id.worldcat.org/fast/1037825.rdf.xml"]
# print(x)
# # #Saving as CSV file
# df_csv = x.to_csv('test_match.csv', index = True, index_label = "@id")
