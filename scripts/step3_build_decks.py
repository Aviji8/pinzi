"""Step 3: all TOCFL levels + HSK 3.0 levels -> public/data/*.json, and stroke-order files -> public/strokes/*.json."""
import csv,json,re,os,math,collections
from paths import TOCFL, HSK, STROKES_SRC, PUBLIC, BUILD
T=str(TOCFL)+'/'; H=str(HSK)+'/'
HW=str(STROKES_SRC)+'/'
OUT=str(PUBLIC)+'/'
def clean(m):
    m=m.split('<br>')[0]
    m=re.sub(r'^\S+ \[[^\]]*\]\s*','',m); m=re.sub(r'^\[[^\]]*\]\s*','',m)
    parts=[p.strip() for p in re.split(r'[/;]',m) if p.strip() and not p.strip().startswith('CL:') and 'variant of' not in p and 'surname' not in p.lower()]
    return '; '.join(parts[:3])
def forms(t):
    out=[]
    for f in t.split('/'):
        if '(' in f: out+=[re.sub(r'[()]','',f),re.sub(r'\(.*?\)','',f)]
        elif f: out.append(f)
    return sorted(dict.fromkeys(out),key=len,reverse=True)
terse={}
for fn in ['top-20111208.csv','top-20100915.csv']:
    for x in csv.DictReader(open(T+fn)):
        for f in x['Traditional'].split('/'): terse.setdefault((f,x['Pinyin']),x.get('Meaning',''))
cat={}
for x in csv.DictReader(open(T+'tocfl-20180419.csv')):
    for f in x['Traditional'].split('/'): cat.setdefault(f,x['Category'])
decks={}
# TOCFL band A with stories
band=json.load(open(BUILD/'deck.json',encoding='utf-8'))
for c in band:
    for w in c['words']: w.pop('cat',None)
decks['tocfl-a']=band
LVN={'L3':'B1','L4':'B2','L5':'C1–C2'}
rows=list(csv.DictReader(open(T+'tocfl-cedict.csv')))
for L,name in LVN.items():
    ws=[]
    for x in rows:
        if x['ID'][:2]!=L: continue
        t=x['Traditional'];f=t.split('/')
        g=next((terse[(k,x['Pinyin'])] for k in f if terse.get((k,x['Pinyin']))),'') or clean(x['Meaning'])
        ws.append(dict(t=t,p=x['Pinyin'],en=g,lv=name,pos=x['POS'],f=forms(t),c=cat.get(f[0]) or 'zz'))
    ws.sort(key=lambda w:w['c'])
    for w in ws: w.pop('c')
    decks['tocfl-'+L]=[dict(n=i//20+1,words=ws[i:i+20]) for i in range(0,len(ws),20)]
for lv in range(1,8):
    d=json.load(open(H+f'{lv}.json')); ws=[]
    for x in sorted(d,key=lambda x:x.get('frequency',99999)):
        fm=x['forms'][0]
        en='; '.join(m for m in fm['meanings'][:2])[:80]
        ws.append(dict(s=x['simplified'],t=fm['traditional'],p=fm['transcriptions']['pinyin'],en=en,lv='HSK '+(str(lv) if lv<7 else '7–9'),pos='/'.join(x.get('pos',[])[:2])))
    decks[f'hsk-{lv}']=[dict(n=i//20+1,words=ws[i:i+20]) for i in range(0,len(ws),20)]
# strokes: per deck per group of 10 cards
G=20
have=set(n[:-5] for n in os.listdir(HW) if n.endswith('.json'))
miss=collections.Counter(); total=0; files=0; biggest=0
for k,cards in decks.items():
    json.dump(cards,open(OUT+f'data/{k}.json','w'),ensure_ascii=False,separators=(',',':'))
    for g in range(math.ceil(len(cards)/G)):
        chars=set()
        for c in cards[g*G:g*G+G]:
            for w in c['words']:
                for fld in (('s',) if 's' in w else ('t',)):
                    for ch in w.get(fld,''):
                        if '一'<=ch<='鿿' or '㐀'<=ch<='䶿': chars.add(ch)
        sh={}
        for ch in chars:
            if ch in have:
                j=json.load(open(HW+ch+'.json')); sh[ch]={'strokes':j['strokes'],'medians':j['medians']}
            else: miss[ch]+=1
        s=json.dumps(sh,ensure_ascii=False,separators=(',',':'))
        open(OUT+f'strokes/{k}-{g}.json','w').write(s); files+=1; total+=len(s); biggest=max(biggest,len(s))
print({k:(len(v),sum(len(c['words']) for c in v)) for k,v in decks.items()})
print('stroke files',files,'MB',round(total/1e6,1),'biggest KB',biggest//1000,'missing chars',len(miss),''.join(list(miss)[:60]))
