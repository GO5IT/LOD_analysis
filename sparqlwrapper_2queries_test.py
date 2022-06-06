from SPARQLWrapper import SPARQLWrapper, JSON, XML
from datetime import datetime
from dateutil.relativedelta import relativedelta

#endpoint = 'http://dbpedia.org/sparql'
endpoint = 'http://localhost:7200/sparql'

sparql = SPARQLWrapper(endpoint)

# Define Prefix for SPARQL query
prefix = """
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX schema: <http://schema.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX dbpedia: <http://dbpedia.org/resource/>
    PREFIX dbo: <http://dbpedia.org/resource/>
    PREFIX dbp: <http://dbpedia.org/property/>
    PREFIX dbc: <http://dbpedia.org/resource/Category:>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbt: <http://dbpedia.org/resource/Template:>
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX dbyago: <http://dbpedia.org/class/yago/>
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX dul: <http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX gnd: <http://d-nb.info/gnd/>
    PREFIX gold: <http://purl.org/linguistics/gold/>
    PREFIX prov: <http://www.w3.org/ns/prov#>
    PREFIX umbelrc: <http://umbel.org/umbel/rc/>
    PREFIX viaf: <http://viaf.org/viaf/>
"""
# Sample SPARQL queries
# query_content = """
#     SELECT * WHERE {
#         ?s ?p ?o
#     }
#     LIMIT 100
# """
# query_content = """
# SELECT *
# WHERE {
# ?person rdfs:label ?name; dbo:birthDate ?b_date; owl:sameAs ?URI
#
# }
# LIMIT 3
# """

# #3 entities in VALUES
# query_content = """
# SELECT * {
#    VALUES ?person { dbpedia:Tomoyasu_Hotei dbpedia:Kyosuke_Himuro dbpedia:Boøwy}
#    ?person owl:sameAs ?URI
# }
# #LIMIT 3
# """

# #3 entities with URI (Somehow this does not work Bad Gateway 502)
# query_content = """
# SELECT * {
#     ?person owl:sameAs ?URI;
#             foaf:name ?name .
#     VALUES (?person ?URI )
#     { (dbpedia:Tomoyasu_Hotei <http://yago-knowledge.org/resource/Tomoyasu_Hotei>)
#       (dbpedia:Kyosuke_Himuro UNDEF)
#       (dbpedia:Boøwy UNDEF)
#     }
# }
# """

# # 3 entities with URI (SELECT and VALUES are separated)
# query_content = """
# SELECT * {
#     ?person owl:sameAs ?URI;
#             foaf:name ?name .
# }
# VALUES
#     (?person ?URI )
#     { (dbpedia:Tomoyasu_Hotei <http://yago-knowledge.org/resource/Tomoyasu_Hotei>)
#       (dbpedia:Kyosuke_Himuro UNDEF)
#       (dbpedia:Boøwy UNDEF)
#     }
# """

query_content = """
    SELECT * WHERE {
        ?s ?p ?o
    }
    LIMIT 100
"""

query = prefix + query_content
sparql.setQuery(query)

# Define outcomes 1 (in JSON)
# sparql.setReturnFormat(JSON)
# results = sparql.query().convert()
#
# for result in results["results"]["bindings"]:
#     print(result)
#     #print('%s: %s' % (result["label"]["xml:lang"], result["label"]["value"]))


# Define outcomes 2 (in XML)
sparql.setReturnFormat(XML)
results = sparql.query().convert()
print(results.toxml())
