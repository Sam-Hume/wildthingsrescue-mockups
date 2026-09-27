import re,base64,subprocess,os,urllib.parse
import pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
SRC=str(ROOT/'src')+'/'; OUT=str(ROOT/'mockups')+'/'
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'
cache={}
def get(u):
    if u in cache: return cache[u]
    b=subprocess.run(['curl','-gsSL','-A',UA,'--retry','5','--retry-all-errors','--retry-delay','2',u],capture_output=True,check=True).stdout
    cache[u]=b; return b
def b64(b,mime): return f'data:{mime};base64,'+base64.b64encode(b).decode()
MIME={'webp':'image/webp','woff2':'font/woff2','woff':'font/woff','ttf':'font/ttf','jpg':'image/jpeg','png':'image/png'}
def inline_css(css,base):
    if 'fonts.googleapis' in base:
        blocks=re.findall(r'/\* ([\w-]+) \*/\s*(@font-face\s*{[^}]*})',css)
        css='\n'.join(b for sub,b in blocks if sub in('latin','latin-ext')) or css
    def rep(m):
        u=m.group(1).strip('\'"')
        if u.startswith('data:'): return m.group(0)
        full=urllib.parse.urljoin(base,u); ext=full.split('?')[0].rsplit('.',1)[-1]
        if ext not in('woff2','woff','ttf'): return m.group(0)
        return f'url({b64(get(full),MIME[ext])})'
    # drop non-woff2 fallbacks to save weight
    css=re.sub(r'url\(([^)]+)\)\s*format\(["\'](?:woff|truetype|embedded-opentype|svg)["\']\)\s*,?','',css)
    css=re.sub(r',\s*;',';',css)
    return re.sub(r'url\(([^)]+)\)',rep,css)
for f in sorted(os.listdir(SRC)):
    if not f.endswith('.html'): continue
    s=open(SRC+f).read()
    s=re.sub(r'<link rel="preconnect"[^>]*>\n?','',s)
    s=re.sub(r'<link (?:href="([^"]+)" rel="stylesheet"|rel="stylesheet" href="([^"]+)")>',lambda m:'<style>'+inline_css(get((m.group(1) or m.group(2)).replace('&amp;','&')).decode(),(m.group(1) or m.group(2)))+'</style>',s)
    s=re.sub(r'<script src="([^"]+)"></script>',lambda m:'<script>'+get(m.group(1)).decode()+'</script>',s)
    def img(m):
        p=m.group(2); return m.group(1)+b64(open(SRC+p,'rb').read(),MIME[p.rsplit('.',1)[-1]])
    s=re.sub(r'(src=")(img/[\w-]+\.(?:jpg|png|webp))',img,s)
    s=re.sub(r'(url\()(img/[\w-]+\.(?:jpg|png|webp))',img,s)
    s=re.sub(r'(src:")(img/[\w-]+\.(?:jpg|png|webp))',img,s)
    # JS strings like img:"img/x.jpg"
    s=re.sub(r'(img:")(img/[\w-]+\.(?:jpg|png|webp))',img,s)
    assert 'img/' not in re.sub(r'data:[^"\')]+','',s), f
    assert 'https://fonts' not in s and 'cdnjs' not in s.split('<script>')[0][:0]+'' , f
    open(OUT+f,'w').write(s); print(f, round(len(s)/1024),'KB')
