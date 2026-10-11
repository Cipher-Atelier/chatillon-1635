import json,hashlib
from collections import Counter,defaultdict
from functools import lru_cache
from pathlib import Path
P=Path(__file__).parent
d=json.loads((P/'config.json').read_text())
fixed={k:v for k,v in d['active_mapping'].items() if k!='N2'}
def run(s,w,control='original'):
 r=s['reference']; f=dict(fixed)
 if control=='rotate':r=r[1:]+r[:1]
 if control=='reverse':r=r[::-1]
 if control=='swap':f['S_c_open'],f['S_h']=f['S_h'],f['S_c_open']
 ts=s['tokens']; L=len(r)
 def edges(i,p):
  t=ts[i];v=None if t['mapping_masked'] else f.get(t['shape'])
  ws=[len(v)] if v is not None else ([w] if t['shape']=='N2' else t['widths'])
  return [(p+x,r[p:p+x]) for x in ws if p+x<=L and (v is None or r[p:p+x]==v)]
 states={(0,'',''):1}
 for i,t in enumerate(ts):
  nxt=defaultdict(int)
  for (p,c,n),count in states.items():
   for q,txt in edges(i,p):nxt[q,txt if t['id']==d['targets'][1] else c,txt if t['shape']=='N2' else n]+=count
  states=nxt
 total=sum(states.values());closed=Counter();n2=Counter();ends=Counter()
 for (p,c,n),count in states.items():closed[c]+=count;n2[n]+=count;ends[p]+=count
 @lru_cache(None)
 def dfs(i,p):
  if i==len(ts):return 1
  return sum(dfs(i+1,q) for q,_ in edges(i,p))
 assert dfs(0,0)==total
 return dict(count=total,closed=dict(closed),n2=dict(n2),ends=dict(ends),full_endpoint_count=sum(n for (p,c,q),n in states.items() if p==L))
out=[]
for s in d['scenarios']:
 for w in range(1,9):
  for control in ('original','rotate','reverse','swap'):
   out.append(dict(reference_id=s['reference_id'],grouping_id=s['grouping_id'],width=w,control=control,**run(s,w,control)))
(P/'RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
for c in ('original','rotate','reverse','swap'):
 print(c)
 for w in range(1,9):
  a=[x for x in out if x['control']==c and x['width']==w]; print(w,sum(x['count'] for x in a),sorted(set(v for x in a for v in x['closed'])),sorted(set(v for x in a for v in x['n2'])),sum(x['full_endpoint_count'] for x in a))
print('config sha256',hashlib.sha256((P/'config.json').read_bytes()).hexdigest())
