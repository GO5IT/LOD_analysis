# Specify date and calculate the age of a person from DBpedia URI
# SPARQLWrapper returns SPARQL query results in JSON format 

from SPARQLWrapper import SPARQLWrapper, JSON, XML
from datetime import datetime
from dateutil.relativedelta import relativedelta

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
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
query_content = """
    SELECT *
       WHERE { dbpedia:Charles_Darwin rdfs:label ?name; dbo:birthDate ?b_date; dbo:deathDate ?d_date 
       FILTER(lang(?name)='en')
       }
"""
# Age calculation is set inside SPARQL (but so far no target year can be posted together)
# """
#     SELECT *
#        WHERE { dbr:Charles_Darwin rdfs:label ?name; dbo:birthDate ?b_date; dbo:deathDate ?d_date
#          BIND(?d_date - ?b_date AS ?ageInDays)
#          BIND(?ageInDays / 365 AS ?ageInYears)
#          BIND(FLOOR(?ageInYears) AS ?age)
# }

targetdate = "1822-01-11"
query = prefix + query_content
sparql.setQuery(query)

# Define outcomes 1 (in JSON)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result)
    person_name = result["name"]["value"]
    birthdate = result["b_date"]["value"]
    deathdate = result["d_date"]["value"]
    birthdate_convert = datetime.strptime(birthdate, "%Y-%m-%d")
    deathdate_convert = datetime.strptime(deathdate, "%Y-%m-%d")
    targetdate_convert = datetime.strptime(targetdate, "%Y-%m-%d")

    if targetdate_convert < deathdate_convert:
        # Calculate years and months from birth date
        age_y = relativedelta(targetdate_convert, birthdate_convert).years
        age_m = relativedelta(targetdate_convert, birthdate_convert).months
        if targetdate_convert >= birthdate_convert:
            print("On "+ targetdate + " " + person_name + " was " + str(age_y) + " years and " + str(age_m) + " months old")
        else:
            # Convert positive value to negative
            age_y = abs(age_y)
            age_m = abs(age_m)
            print(targetdate + " is " + str(age_y) + " years and " + str(age_m) + " months before " + person_name + " was born")
    else:
        # Calculate years and months from death date
        age_y = relativedelta(targetdate_convert, deathdate_convert).years
        age_m = relativedelta(targetdate_convert, deathdate_convert).months
        print(targetdate + " is " + str(age_y) + " years and " + str(age_m) + " months after " + person_name + " was dead")
    #print(result["label"]["value"])

print('---------------------------')

# Display all SPARQL results
#for result in results["results"]["bindings"]:
#    print(result)
#    #print('%s: %s' % (result["label"]["xml:lang"], result["label"]["value"]))


# Define outcomes 2 (in XML)
# sparql.setReturnFormat(XML)
# results = sparql.query().convert()
# print(results.toxml())
