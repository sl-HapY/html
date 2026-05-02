import os, sys, subprocess as sp, re, zipfile, shutil, time as t, requests as rq
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup as BS

def l(msg):
    print(f"[{t.strftime('%H:%M:%S')}] {msg}", flush=True)

def r(c, d=None):
    l(f"run: {' '.join(c)}")
    sp.run(c, check=True, cwd=d)

def d(url, fn=None, hdrs=None):
    f = fn or os.path.basename(urlparse(url).path) or 'f'
    l(f"dl {url} -> {f}")
    s = rq.Session()
    s.headers.update(hdrs or {})
    s.headers.setdefault('User-Agent', 'Mozilla/5.0')
    rs = s.get(url, stream=True, timeout=30)
    rs.raise_for_status()
    total = int(rs.headers.get('content-length', 0))
    done = 0
    with open(f, 'wb') as fh:
        for ck in rs.iter_content(chunk_size=8192):
            if ck:
                fh.write(ck)
                done += len(ck)
                if total:
                    pct = done * 100 // total
                    l(f"  {pct}% ({done}/{total})")
    l(f"done {done} -> {f}")
    return f

def g(repo, branch=None, dest=None, depth=1, lfs=True):
    d_ = dest or os.path.basename(repo.rstrip('/').split('/')[-1].replace('.git', ''))
    cmd = ['git', 'clone']
    if depth:
        cmd += ['--depth', str(depth)]
    if branch:
        cmd += ['--branch', branch, '--single-branch']
    cmd += [repo, d_]
    r(cmd)
    if lfs:
        try:
            r(['git', 'lfs', 'pull'], cwd=d_)
        except:
            l("lfs skip")
    l(f"cloned {repo} -> {d_}")
    return d_

def m(url, out='site_mirror', depth=1000):
    l(f"mirror {url}")
    sess = rq.Session()
    sess.headers.update({'User-Agent': 'Mozilla/5.0'})
    dom = urlparse(url).netloc
    vis = set()
    q = [(url, 0)]
    os.makedirs(out, exist_ok=True)
    css_re = re.compile(r'url\([\'"]?([^\'")\s]+)[\'"]?\)')

    def lp(u):
        p = urlparse(u).path.lstrip('/')
        if not p or p.endswith('/'):
            p += 'index.html'
        return os.path.join(out, dom, p)

    def dl(u):
        if u in vis:
            return None
        vis.add(u)
        try:
            rs = sess.get(u, timeout=10)
            if rs.status_code != 200:
                return None
            ph = lp(u)
            os.makedirs(os.path.dirname(ph), exist_ok=True)
            with open(ph, 'wb') as f:
                f.write(rs.content)
            l(f"  got {u}")
            return ph, rs
        except Exception as e:
            l(f"  fail {u}: {e}")
            return None

    def rw(u, base):
        if not u or u.startswith('data:'):
            return u
        if urlparse(u).netloc and urlparse(u).netloc != dom:
            return u
        ab = urljoin(base, u)
        dl(ab)
        return '/' + urlparse(ab).path.lstrip('/')

    while q:
        u, d_ = q.pop(0)
        if d_ > depth or u in vis:
            continue
        res = dl(u)
        if not res:
            continue
        ph, rs = res
        if 'text/html' not in rs.headers.get('content-type', ''):
            continue
        sps = BS(rs.content, 'lxml')
        base = rs.url
        for tag in sps.find_all(['a','link','script','img','source']):
            try:
                if tag.name == 'a' and tag.has_attr('href'):
                    href = tag['href']
                    if not urlparse(href).netloc or urlparse(href).netloc == dom:
                        ah = urljoin(base, href)
                        if urlparse(ah).netloc == dom and ah not in vis:
                            q.append((ah, d_+1))
                            tag['href'] = '/' + urlparse(ah).path.lstrip('/')
                elif tag.name == 'link' and tag.has_attr('href'):
                    tag['href'] = rw(tag['href'], base)
                elif tag.name == 'script' and tag.has_attr('src'):
                    tag['src'] = rw(tag['src'], base)
                elif tag.name == 'img' and tag.has_attr('src'):
                    tag['src'] = rw(tag['src'], base)
                elif tag.name == 'source' and tag.has_attr('srcset'):
                    srcset = tag['srcset']
                    pts = []
                    for pt in srcset.split(','):
                        pt = pt.strip()
                        if pt:
                            up = pt.split(' ')[0]
                            nw = rw(up, base)
                            pts.append(pt.replace(up, nw, 1))
                    tag['srcset'] = ', '.join(pts)
            except:
                pass
        with open(ph, 'wb') as f:
            f.write(sps.prettify('utf-8'))
        for ct in sps.find_all('link', rel='stylesheet'):
            ch = ct.get('href')
            if ch:
                ca = urljoin(base, ch) if (not urlparse(ch).netloc or urlparse(ch).netloc == dom) else None
                if ca and urlparse(ca).netloc == dom:
                    cp = lp(ca)
                    if os.path.exists(cp):
                        with open(cp, 'r', encoding='utf-8') as f:
                            cssc = f.read()
                        def rpl(m):
                            u_ = m.group(1)
                            return f"url({rw(u_, ca)})"
                        ncss = css_re.sub(rpl, cssc)
                        with open(cp, 'w', encoding='utf-8') as f:
                            f.write(ncss)
    l("mirror done")

def main():
    raw = os.environ.get('CMDS', '')
    lines = [ln.strip() for ln in raw.split('\n') if ln.strip() and not ln.strip().startswith('#')]
    if not lines:
        l("no cmds")
        return
    out_root = os.environ.get('OUT_DIR', 'dl')
    os.makedirs(out_root, exist_ok=True)
    for ln in lines:
        parts = ln.split()
        if not parts:
            continue
        cmd = parts[0].lower()
        url = parts[1] if len(parts) > 1 else ''
        kwargs = {}
        for p in parts[2:]:
            if '=' in p:
                k, v = p.split('=', 1)
                kwargs[k] = v
        try:
            if cmd == 'wget':
                fn = kwargs.get('o', kwargs.get('output', None))
                if fn:
                    fn = os.path.join(out_root, fn)
                else:
                    fn = os.path.join(out_root, os.path.basename(urlparse(url).path) or 'f')
                d(url, fn)
            elif cmd == 'git':
                repo = url
                branch = kwargs.get('b', kwargs.get('branch'))
                depth = int(kwargs.get('depth', '1'))
                lfs = kwargs.get('lfs', 'true').lower() in ('1', 'true', 'yes')
                dest = kwargs.get('d', kwargs.get('dest'))
                if dest:
                    dest = os.path.join(out_root, dest)
                else:
                    dest = os.path.join(out_root, os.path.basename(repo.rstrip('/').split('/')[-1].replace('.git', '')))
                g(repo, branch=branch, dest=dest, depth=depth, lfs=lfs)
            elif cmd == 'mirror':
                site_dir = os.path.join(out_root, kwargs.get('o', kwargs.get('out', 'mirror')))
                md = int(kwargs.get('depth', '1000'))
                m(url, out=site_dir, depth=md)
            else:
                l(f"unknown cmd: {cmd}")
        except Exception as e:
            l(f"fail: {e}")
    l("zip...")
    zip_n = os.environ.get('ZIP', 'out.zip')
    with zipfile.ZipFile(zip_n, 'w', zipfile.ZIP_DEFLATED) as zf:
        for rt, _, fs in os.walk(out_root):
            for fn in fs:
                fl = os.path.join(rt, fn)
                arc = os.path.relpath(fl, out_root)
                zf.write(fl, arc)
    l(f"zip: {zip_n}")

if __name__ == '__main__':
    main()
