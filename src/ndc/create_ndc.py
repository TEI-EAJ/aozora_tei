from SPARQLWrapper import SPARQLWrapper
from rdflib import URIRef, BNode, Literal
from rdflib import Graph

sparql = SPARQLWrapper(endpoint='https://dydra.com/ut-digital-archives/aozora/sparql', returnFormat='json')
sparql.setQuery("""
    SELECT DISTINCT ?s ?subject WHERE {
    ?s <http://purl.org/dc/elements/1.1/subject> ?subject .
    }
""")
results = sparql.query().convert()

g = Graph()

for obj in results["results"]["bindings"]:

    uri = obj["s"]["value"]
    subject = obj["subject"]["value"]
    ss = subject.split(" ")
    for i in range(1, len(ss)):
        s = ss[i]
        g.add((URIRef(uri), URIRef("http://purl.org/dc/terms/type"), Literal(s)))

g.serialize(format='pretty-xml', destination="ndcs.rdf")
