import json
with open("phonology.json","r",encoding="utf-8-sig") as f:
    data = json.load(f)
list_phonemes=[]
for i in data["phones"]:
    list_phonemes.append(i[0])
list_phonemes.sort(key=len,reverse=True)
print(list_phonemes)
