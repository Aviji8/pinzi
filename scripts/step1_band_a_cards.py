"""Step 1: TOCFL Band A (Pre-A1, A1, A2) word list -> 61 cards of 20 words (build/cards.json)."""
import csv,json,re,sys,collections
from paths import TOCFL, BUILD
D=str(TOCFL)+'/'
rows=[x for x in csv.DictReader(open(D+'tocfl-cedict.csv')) if x['ID'][:2] in ('L0','L1','L2')]
def forms(t): return [f for f in t.split('/') if f]
cat={}
for x in csv.DictReader(open(D+'tocfl-20180419.csv')):
    for f in forms(x['Traditional']): cat.setdefault(f,x['Category'])
terse={}
for fn in ['top-20111208.csv','top-20100915.csv']:
    for x in csv.DictReader(open(D+fn)):
        for f in forms(x['Traditional']): terse.setdefault(f,x.get('Meaning',''))
def clean(m):
    m=m.split('<br>')[0]
    m=re.sub(r'^\S+ \[[^\]]*\]\s*','',m)
    m=re.sub(r'^\[[^\]]*\]\s*','',m)
    parts=[p.strip() for p in re.split(r'[/;]',m) if p.strip() and not p.strip().startswith('CL:') and 'variant of' not in p and 'surname' not in p.lower()]
    return '; '.join(parts[:3])
out=[]
for x in rows:
    t=x['Traditional']; f=forms(t)
    c=next((cat[k] for k in f+[re.sub(r'[()兒]','',k) for k in f] if k in cat),'其他')
    g=next((terse[k] for k in f if terse.get(k)),'') or clean(x['Meaning'])
    out.append(dict(id=x['ID'],lv={'L0':'Pre-A1','L1':'A1','L2':'A2'}[x['ID'][:2]],t=t,p=x['Pinyin'],pos=x['POS'],en=g,cat=c))
# group into 20-word cards: by level, then theme, then official ID
order={'Pre-A1':0,'A1':1,'A2':2}
for x in out: x['cat']=x['cat'] or '常用詞'
out.sort(key=lambda x:(order[x['lv']],x['cat']=='常用詞',x['cat'],x['id']))
cards=[out[i:i+20] for i in range(0,1220,20)]; cards[-1]+=out[1220:]
json.dump(cards,open(BUILD/'cards.json','w',encoding='utf-8'),ensure_ascii=False)
print('Band A words:',len(out),'cards:',len(cards))
