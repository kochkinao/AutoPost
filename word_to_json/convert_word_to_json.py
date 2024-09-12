import docx
import json


doc = docx.Document("1-22.docx")
result = [p.text for p in doc.paragraphs]
spisok = []

for i in result:
    try:
        if i == "":
            spisok.append("/n")
        elif type(int(i)) == int:
            spisok.append(int(i))
    except:
        spisok.append(i)

itog = []
a = ""

for i in range(0, len(spisok)):
    if type(spisok[i]) != int:
        a += str(spisok[i])
    else:
        itog.append(a)
        a = ""
del itog[0]

with open("template.json", "r") as outfile:
    messages = json.load(outfile)

for i in range(0, len(itog)):
    try:
        messages["message"][i]["text"] = itog[i]
    except:
        messages["message"].append({"id": i, "text": itog[i]})


with open("../text.json", "w") as outfile:
    json.dump(messages, outfile, ensure_ascii=False, indent=2)