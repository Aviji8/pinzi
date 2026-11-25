"""Step 2: attach the hand-written stories (content/essays.txt), generate pinyin, fix multi-reading words -> build/deck.json."""
import json,re,jieba,logging
jieba.setLogLevel(logging.ERROR)
from pypinyin import pinyin,Style
from common import *
from paths import BUILD
cards=json.load(open(BUILD/'cards.json',encoding='utf-8'));E=load_essays()
# check: every story must use all of its card's words
missing={i:[w['t'] for w in c if not any(f in ''.join(z for z,_ in E.get(i,[])) for f in forms(w['t']))] for i,c in enumerate(cards,1)}
missing={i:m for i,m in missing.items() if m}
if missing:
    for i,m in missing.items(): print(f'Card {i} story is missing:',' '.join(m))
    raise SystemExit('Fix content/essays.txt so every story uses all 20 words.')
print('Story check OK: all',len(cards),'stories use all their words.')
words=[w for c in cards for w in c]
# official reading map (multi-char forms only, unambiguous)
off={}
for w in words:
    fs=w['t'].split('/'); ps=w['p'].split('/')
    if len(fs)==len(ps):
        for f,p in zip(fs,ps):
            if '(' not in f and len(f)>1: off.setdefault(f,p)
for f in off: jieba.add_word(f)
fix={'垃圾':'lèsè','星期':'xīngqí','頭髮':'tóufǎ','和':'hé','誰':'shéi','一下':'yíxià','一共':'yígòng','一定':'yídìng','一樣':'yíyàng','一塊':'yíkuài','一半':'yíbàn','一切':'yíqiè','不客氣':'búkèqì','不錯':'búcuò','不要':'búyào','不是':'búshì','不過':'búguò','不用':'búyòng','不會':'búhuì','不必':'búbì','不夠':'búgòu','不見':'bújiàn','不太':'bútài','不到':'búdào'}
off.update(fix)
from pypinyin import load_phrases_dict
ph={'還給':'huán gěi','三行':'sān háng','長得':'zhǎng de','喂貓':'wèi māo','得馬上':'děi mǎ shàng','好美哪':'hǎo měi na','高興地':'gāo xìng de','還好':'hái hǎo','還是':'hái shì','還有':'hái yǒu','還要':'hái yào','還送':'hái sòng','還買':'hái mǎi','還下':'hái xià','還住':'hái zhù','還在':'hái zài'}
for v in ['說','開','念','打掃','跑','香','變','睡','講','流','寫','吃','做','唱','長','好']:
    pass
for v in ['說得','開得','打掃得','跑得','香得','變得','睡得','講得','流得','寫得','吃得']:
    ph[v]=' '.join([x[0] for x in pinyin(v[0:-1],style=Style.TONE)])+' de'
load_phrases_dict({k:[[x] for x in v.split()] for k,v in ph.items()})
for k in ph: jieba.add_word(k)
P=re.compile(r'[一-鿿]')
def py(s):
    out=[]
    for seg in jieba.cut(s):
        if not P.search(seg): out.append(seg); continue
        if seg in off: out.append(off[seg]); continue
        out.append(''.join(x[0] for x in pinyin(seg,style=Style.TONE)))
    # join: space between pinyin words, attach punctuation
    res=''
    for o in out:
        if re.match(r'^[，。！？：；、「」…（）]+$',o):
            o=o.translate(str.maketrans('，。！？：；、「」','，。!?:;,""')).replace('，',',').replace('。','.')
            res=res.rstrip()+o+' '
        else: res+=o+' '
    res=re.sub(r'\s+',' ',res).strip()
    res=res.replace('"',' " ')
    # pair quotes
    out2='';q=0
    for ch in re.split(r'( " )',res):
        if ch==' " ':
            out2+=(' “' if q==0 else '” ');q^=1
        else: out2+=ch
    res=re.sub(r'\s+',' ',out2).replace('“ ','“').replace(' ”','”').strip()
    res=re.sub(r'([.!?]”?\s+“?)([a-zāáǎàēéěèīíǐìōóǒòūúǔù])',lambda m:m.group(1)+m.group(2).upper(),res)
    return res
data=[]
for i,c in enumerate(cards,1):
    data.append(dict(n=i,words=[dict(t=w['t'],p=w['p'],en=w['en'],lv=w['lv'],pos=w['pos'],cat=w['cat'],f=forms(w['t'])) for w in c],
      essay=[dict(zh=z,py=py(z),en=e) for z,e in E[i]]))
G={('在','Adv'):'(be) in the middle of doing',('在','Prep/Vst'):'at; in; to be at',('得','Ptc'):'(particle linking verb + degree/manner)',('得','Vpt'):'must; have to',('過','Ptc'):'(particle: have done before)',('過','V'):'to cross; to pass; to spend (time)',('可能','N'):'possibility',('哪','Ptc'):'(particle, like 啊 after -n)',('長','Vs'):None,('還','V'):'to return (sth); give back',('地','N'):'ground; land; earth',('地','Ptc'):'(particle: adjective + 地 + verb = -ly)',('喂','Ptc'):None,('行','M'):'row; line (measure word)',('空','Vs'):None}
for c in data:
    for w in c['words']:
        k=(w['t'],w['pos'])
        if w['t']=='長': w['en']='to be long' if w['p']=='cháng' else 'to grow; to look (長得)'
        elif w['t']=='喂': w['en']='hello? (on the phone)' if w['p']=='wéi' else 'to feed'
        elif w['t']=='空': w['en']='empty; sky' if w['p']=='kōng' else 'free time (有空)'
        elif w['t']=='行' and w['p']=='xíng': w['en']='OK; capable; will do'
        elif k in G and G[k]: w['en']=G[k]
PF=[('dé mǎshàng','děi mǎshàng'),('hái gěi péngyǒu','huán gěi péngyǒu'),('wèi māo','wèi māo'),('sān xíng zì','sān háng zì'),('hǎoměi nǎ','hǎo měi na'),('hǎo měi nǎ','hǎo měi na'),('gāoxìng dì','gāoxìng de'),('zhǎngde','zhǎng de')]
import re
for c in data:
    for s in c['essay']:
        for a,b in PF: s['py']=s['py'].replace(a,b)
        s['py']=re.sub(r'^([^a-zA-Zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]*)(.)',lambda m:m.group(1)+m.group(2).upper(),s['py'])
json.dump(data,open(BUILD/'deck.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
for n,k in [(8,'得馬上'),(34,'還給'),(26,'高興地'),(28,'哪'),(31,'喂貓'),(36,'三行'),(32,'長得')]:
    print([s['py'] for s in data[n-1]['essay'] if k in s['zh']])
