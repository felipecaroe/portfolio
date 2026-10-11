from pathlib import Path
from html.parser import HTMLParser
from html import unescape
from urllib.parse import urlsplit, unquote
import json,re,shutil

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT.parent/'.release/public'
MANIFEST=json.loads((ROOT/'site.json').read_text())
BASE=MANIFEST['base_url'].replace('/beta/','/')
PAGES={p['path'] for p in MANIFEST['pages'] if p['path'] not in {'cases/drafts/index.html','cases/drafts/mi-mundo/index.html'}}
FORBIDDEN={'reviews','templates','scripts','content'}
queue=list(PAGES);seen=set();missing=[]
class References(HTMLParser):
    def __init__(self):super().__init__();self.refs=[]
    def handle_starttag(self,tag,attrs):
        attributes=dict(attrs)
        for key,value in attrs:
            if not value:continue
            if key in ('href','src','poster'):self.refs.append(value)
            elif key=='srcset':self.refs.extend(x.strip().split()[0] for x in value.split(','))
            elif key=='data-prototype-flow':self.refs.extend(f['src'] for f in json.loads(value))
        if tag=='meta' and attributes.get('property') in ('og:image','twitter:image'):
            self.refs.append(attributes.get('content',''))
def local(ref,parent):
    u=urlsplit(ref)
    if not u.path:return None
    if u.scheme or u.netloc:
        base_url=urlsplit(BASE)
        if u.netloc!=base_url.netloc or not u.path.startswith(base_url.path):return None
        relative=u.path[len(base_url.path):]
        p=(ROOT/unquote(relative)).resolve()
    else:
        p=(parent.parent/unquote(u.path)).resolve()
    if p.is_dir():p=p/'index.html'
    try:rel=p.relative_to(ROOT)
    except ValueError:return None
    if rel.parts[0] in FORBIDDEN:return None
    if p.suffix=='.html' and str(rel) not in PAGES:return None
    return p
while queue:
    rel=queue.pop();src=ROOT/rel
    if rel in seen:continue
    if not src.is_file():missing.append(rel);continue
    seen.add(rel);dst=OUTPUT/rel;dst.parent.mkdir(parents=True,exist_ok=True)
    if src.suffix in ('.html','.css','.js','.svg'):
        s=src.read_text();refs=[]
        if src.suffix in ('.html','.svg'):
            s=s.replace(MANIFEST['base_url'],BASE)
            parser=References();parser.feed(s);refs=parser.refs
            refs.extend(re.findall(r'url\([\'\"]?([^\)\'\"]+)',s))
            s=re.sub(r'<meta name="robots" content="[^"]*">','<meta name="robots" content="index,follow">',s)
        elif src.suffix=='.css':refs=re.findall(r'url\([\'\"]?([^\)\'\"]+)',s)
        dst.write_text(s)
        for ref in refs:
            p=local(unescape(ref),src)
            if p:queue.append(str(p.relative_to(ROOT)))
    else:shutil.copy2(src,dst)
if missing:raise SystemExit('Missing release dependencies: '+', '.join(missing))
urls=[BASE+('' if p=='index.html' else p.removesuffix('index.html')) for p in sorted(PAGES)]
(OUTPUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+u+'</loc></url>' for u in urls)+'</urlset>')
(OUTPUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'sitemap.xml\n')
report={'base_url':BASE,'pages':sorted(PAGES),'files':len(seen),'missing':missing,'excluded':['reviews','templates','scripts','content','cases/drafts/index.html','cases/drafts/mi-mundo/index.html'],'note':'Prepared locally only. Beta remains noindex. Deploy this directory, never the whole repository.'}
(OUTPUT.parent/'manifest.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
