#Testing rdflib
from rdflib import Graph, URIRef, Literal, Namespace, term
# from rdflib.term import term
# Define Namespaces
from rdflib.namespace import DCTERMS, RDF, RDFS

# #Reading Turtle file
# with open('./rdf_test2.ttl', 'rb') as f:
#     rdf_triple_data = f.read()
# # print(rdf_triple_data)
#
# # Create a Graph
# g = rdflib.Graph()
# g.parse(data=rdf_triple_data, format='turtle')
# new_data = g.serialize(format='xml')
# print(new_data)


# The following section is to generate turtle from scratch with CIDOC-CRM
gw = Namespace("https://www.geschichtewiki.wien.gv.at/")
crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
gw.blut  = term.URIRef(u'https://www.geschichtewiki.wien.gv.at/Blutgasse')
placename = 'Blutgasse'
at_address = 'Wien, Örsterreich'

# create a Graph
g = Graph()
# Create an RDF URI node to use as the subject for multiple triples
subject1 = URIRef(gw.blut)
subject2 = URIRef(gw.blut +'/5')
subject3 = URIRef(gw + 'Wenzel_M%C3%BCller#_37916d5d63d408742f912e2082a7160f')
subject4 = URIRef(gw + 'Blutgasse_5#_a954cc8dcee6fd1e5b3dad231b03cf11')
subject5 = URIRef(gw.blut +'/5/Appellation')

# Add triples using store's add() method.
g.add((subject1, RDFS.label, Literal(placename, lang="en")))
g.add((subject1, RDF.type, URIRef(crm.E53_Place)))
g.add((subject1, crm.P59_has_section, URIRef(subject2)))

g.add((subject2, RDFS.label, Literal(placename + ' 5', lang="de")))
g.add((subject2, DCTERMS.relation, URIRef(gw + 'Johann_H%C3%A4ringshauser#_6d5b60630b98c52534bed761f65b0980')))
g.add((subject2, DCTERMS.relation, URIRef(gw + 'Wenzel_M%C3%BCller#_37916d5d63d408742f912e2082a7160f')))
g.add((subject2, DCTERMS.relation, URIRef(gw + 'Blutgasse_5#_a954cc8dcee6fd1e5b3dad231b03cf11')))
g.add((subject2, RDF.type, URIRef(crm.E53_Place)))
g.add((subject2, crm.P1_is_identified_by, URIRef(subject5)))
g.add((subject2, crm.P168_place_is_defined_by, Literal('<location><lat>48.207579199236</lat><lng>16.374236317069</lng></location>')))

g.add((subject5, RDFS.label, Literal(placename + ' 5, '+ at_address, lang="de")))
g.add((subject5, RDF.type, URIRef(crm.E41_Appellation)))

g.add((subject3, RDF.type, Literal('Personen', lang="de")))

g.add((subject4, RDF.type, Literal('Bauwerke', lang="de")))

print(g)
# Iterate over triples in store and print them out.
# print("--- printing raw triples ---")
# for s, p, o in g:
#     print((s, p, o))

# g.parse(data=rdf_triple_data, format='turtle')
new_data2 = g.serialize(format="turtle").decode("utf-8")
print(new_data2)