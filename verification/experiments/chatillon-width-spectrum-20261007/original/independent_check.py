import json
from collections import Counter
from pathlib import Path
P=Path(__file__).parent
d=json.loads((P/'config.json').read_text()); results=json.loads((P/'RESULTS.json').read_text())
checked=0
for row in results:
 s=next(s for s in d['scenarios'] if s['reference_id']==row['reference_id'] and s['grouping_id']==row['grouping_id'])
 text=s['reference']; key={k:v for k,v in d['active_mapping'].items() if k!='N2'}
 if row['control']=='rotate':text=text[1:]+text[:1]
 if row['control']=='reverse':text=text[::-1]
 if row['control']=='swap':key['S_c_open']='u';key['S_h']='e'
 paths=[(0,[])]; target=next(i for i,t in enumerate(s['tokens']) if t['id']==d['targets'][1]); ni=next(i for i,t in enumerate(s['tokens']) if t['shape']=='N2')
 for t in s['tokens']:
  new=[]; val=key.get(t['shape']) if not t['mapping_masked'] else None
  for pos,ss in paths:
   for width in ([len(val)] if val is not None else [row['width']] if t['shape']=='N2' else t['widths']):
    piece=text[pos:pos+width]
    if len(piece)==width and (val is None or piece==val):new.append((pos+width,ss+[piece]))
  paths=new
 assert len(paths)==row['count']
 assert dict(Counter(ss[target] for p,ss in paths))==row['closed']
 assert dict(Counter(ss[ni] for p,ss in paths))==row['n2']
 checked+=1
print('Independently enumerated all',checked,'cases with exact matching path and substring counts.')
# Six equivalence classes because later spelling variation lies beyond the consumed prefix.
a=[r for r in results if r['control']=='original' and r['count']]
print('endpoints',min(int(k) for r in a for k in r['ends']),max(int(k) for r in a for k in r['ends']))
print('references',[(s['reference_id'],len(s['reference'])) for s in d['scenarios'][::3]])
