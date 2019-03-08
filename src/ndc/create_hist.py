import json

with open('data/ndc.json', 'r') as f:
    data = json.load(f)

with open('data/subjects.json', 'r') as f:
    subjects = json.load(f)

arr = data["children"]

for lev1 in arr:

    for lev2 in lev1["children"]:

        for lev3 in lev2["children"]:

            for lev4 in lev3["children"]:
                id = lev4["id"]
                id = id.split("/")[-1].replace("ndc", "")
                id = id.upper()

                if id in subjects:
                    lev4["value"] = subjects[id]

with open('../../docs/tools/lod/hist.json', 'w') as outfile:
    json.dump(data, outfile, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
