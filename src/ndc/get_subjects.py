from SPARQLWrapper import SPARQLWrapper
import urllib.request, json

with urllib.request.urlopen(
        "https://api.github.com/search/code?q=in:file+extension:xml+path:data/complete/tei_lib_lv3+repo:TEI-EAJ/aozora_tei") as url:
    data = json.loads(url.read().decode())

map = {}

for item in data["items"]:
    name = item["name"]
    id = name.split("_")[0]

    print(name)

    sparql = SPARQLWrapper(endpoint='https://dydra.com/ut-digital-archives/aozora/sparql', returnFormat='json')
    sparql.setQuery("""
        SELECT DISTINCT ?subject WHERE {
        ?s <http://purl.org/dc/elements/1.1/subject> ?subject .
        ?s <http://purl.org/net/aozora/titleID> ?o . 
        filter (?o = '""" + id + """'^^xsd:int) . 
        } 
    """)

    results = sparql.query().convert()

    for obj in results["results"]["bindings"]:

        subjects = obj["subject"]["value"].split(" ")
        for subject in subjects:

            if subject == "NDC":
                continue

            if subject not in map:
                map[subject] = 0

            map[subject] = map[subject] + 1

            if "K" in subject:

                subject = subject.replace("K", "")

                if subject not in map:
                    map[subject] = 0

                map[subject] = map[subject] + 1

fw = open("data/subjects.json", 'w')
json.dump(map, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
