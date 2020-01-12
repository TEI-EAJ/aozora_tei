from bs4 import BeautifulSoup
import json
import sys

args = sys.argv

path = args[1]

filename = path.split("/")[-1].split(".")[0]

# ファイルの読み込み
f1 = open('data/'+filename+'.xml','r')
soup1 = BeautifulSoup(f1, 'html.parser')
f1.close()

listPerson = soup1.find("listperson")

persons = listPerson.find_all("person")

sexes = {}

for person in persons:
    sex = 0
    sex_ = person.get("sex")
    if sex_ != None:
        try:
            sex = int(sex_)
        except:
            sex = 0
    sexes["#"+person.get("xml:id")] = sex

def getSex(id):
    if id in sexes:
        return sexes[id]
    else:
        return 0

for tag in soup1.find_all("span", {"type" : "rb"}):
    # タグとその内容の削除
    tag.decompose()

for tag in soup1.find_all("span", {"type" : "rp"}):
    # タグとその内容の削除
    tag.decompose()

sps = soup1.find_all("sp")

arr = []

for sp in sps:

    who = sp.get("who")

    ps = sp.find_all("p")

    for p in ps:

        text = p.text

        obj = {
            "text" : text,
            "sex" : getSex(who)
        }

        arr.append(obj)

fw = open("data/"+filename+".json", 'w')
json.dump(arr, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))