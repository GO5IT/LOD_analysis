from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import RDF, FOAF, SKOS
# Create a Graph
g = Graph()
g.parse("http://babelnet.org/rdf/data/s00008556n?output=xml")
# Loop through each triple in the graph (subj, pred, obj)
for subj, pred, obj in g:
    # Check if there is at least one triple in the Graph
    if (subj, pred, obj) not in g:
       raise Exception("It better be!")

# Print the number of "triples" in the Graph
print(f"Graph g has {len(g)} statements.")

# Print out the entire Graph in the RDF Turtle format
print(g.serialize(format="turtle"))

# for subj, pred, obj in g.triples((None,  SKOS.exactMatch, None)):
#     print(f"{subj} is a {obj}")

for subj, pred, obj in g.triples((None,  FOAF.primaryTopic, None)):
    print(f"{subj} is a {obj}")
