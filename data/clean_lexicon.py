import pandas as pd
data=pd.read_csv('lexicon.tsv',sep='\t',names=['word','ipa']).drop_duplicates()
d={}
for index, row in data.iterrows():
 d.update({row['word']:row['ipa']})
listd=list(d.keys())
listd.sort()
t=""
for i in listd:
 t+=i+'\t'+d[i]+'\n'
with open('lexicon.tsv','w',encoding='utf-8') as f:
 f.write(t)

