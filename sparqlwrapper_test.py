from SPARQLWrapper import SPARQLWrapper, JSON, XML

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
# Define Prefix for SPARQL query
prefix = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dbo: <http://dbpedia.org/resource/>
"""
# Sample SPARQL queries
# query_content = """
#     SELECT * WHERE {
#         ?s ?p ?o
#     }
#     LIMIT 100
# """
query_content = """
    SELECT ?label
       WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
"""

query = prefix + query_content
sparql.setQuery(query)

# Define outcomes 1 (in JSON)
# sparql.setReturnFormat(JSON)
# results = sparql.query().convert()
#
# for result in results["results"]["bindings"]:
#     print(result["label"]["value"])
#
# print('---------------------------')
#
# for result in results["results"]["bindings"]:
#     print('%s: %s' % (result["label"]["xml:lang"], result["label"]["value"]))
#

# Define outcomes 2 (in XML)
sparql.setReturnFormat(XML)
results = sparql.query().convert()
print(results.toxml())
