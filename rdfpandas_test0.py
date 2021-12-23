# import sys
# import requests
# import json
# import pickle
# import re
# import pandas as pd
# from bs4 import BeautifulSoup as bs
# from rdflib import Graph, URIRef, Literal
# import networkx as nx
# import matplotlib.pyplot as plt
# from tqdm import tqdm
# from rdflib import Graph, URIRef, Literal, Namespace, term
# import urllib.request

# # A dictionary to store the data we'll retrieve.
# entity_list = []

# url = 'https://dbpedia.org/data/1967.rdf'

#################
# def fetchxml(x):
#     file = urllib.request.urlopen(x)
#     data = file.read()
#     file.close()
#     return data
#     #soup = bs(data, 'xml.parser')
#     #fetched = list(soup.rdf)  # Display and check the title of URL
#     #return print(soup)
# fetchxml(url)

#################
import rdfpandas
from rdfpandas.graph import to_dataframe
import pandas as pd
import rdflib

g = rdflib.Graph()
g.parse('https://dbpedia.org/data/1967.rdf', format = 'xml')
df = to_dataframe(g)
df.to_csv('testrdf.csv', index = True, index_label = "@id")

#################
from rdflib import Graph, URIRef, Literal, Namespace, term
# from rdflib.term import term
# Define Namespaces
from rdflib.namespace import DCTERMS, RDF, RDFS

# # create a Graph
# g = Graph()
# g.parse("https://dbpedia.org/data/1967.rdf")
# # Loop through each triple in the graph (subj, pred, obj)
# for subj, pred, obj in g:
#     # Check if there is at least one triple in the Graph
#     if (subj, pred, obj) not in g:
#        raise Exception("It better be!")
#
#
# # Print the number of "triples" in the Graph
# print(f"Graph g has {len(g)} statements.")
# # Prints: Graph g has 86 statements.
#
# # Print out the entire Graph in the RDF Turtle format
# print(g.serialize(format="turtle"))

#################
# x = g.parse("https://dbpedia.org/data/1967.rdf")
# # Create an RDF URI node to use as the subject for multiple triples
# subject1 = URIRef(x)
# # Add triples using store's add() method.
# g.add((subject1, RDFS.label, Literal(placename, lang="en")))
# g.add((subject1, RDF.type, URIRef(crm.E53_Place)))
# g.add((subject1, crm.P59_has_section, URIRef(subject2)))
# print(g)
#
# new_data2 = g.serialize(format="turtle").decode("utf-8")
# print(new_data2)

#####################
# import xml.etree.ElementTree as ET
# mytree = ET.parse('https://dbpedia.org/data/1967.rdf')
# myroot = mytree.getroot()
# print(myroot)