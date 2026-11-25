from paths import CONTENT
import re,json
def forms(t):
    out=[]
    for f in t.split('/'):
        if '(' in f:
            out+= [re.sub(r'[()]','',f), re.sub(r'\(.*?\)','',f)]
        else: out.append(f)
    out=[o for o in out if o]
    return sorted(dict.fromkeys(out),key=len,reverse=True)
def load_essays():
    E={};cur=None
    for line in open(CONTENT/'essays.txt',encoding='utf-8'):
        line=line.strip()
        if line.startswith('## '): cur=int(line[3:]);E[cur]=[]
        elif line: zh,en=line.split('|',1);E[cur].append([zh,en])
    return E
