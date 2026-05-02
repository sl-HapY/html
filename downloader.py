import os, sys, json, subprocess, re, zipfile, shutil, time
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

def run(cmd, cwd=None):
    log(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True, cwd=cwd)

def download_direct(url, filename, headers=None):
    local = filename or os.path.basename(urlparse(url).path) or 'downloaded_file'
    log(f"Downloading {url} -> {local}")
    sess = requests.Session()
    sess.headers.update(headers or {})
    sess.headers.setdefault('User-Agent', 'Mozilla/5.0')
    r = sess.get(url, stream=True, timeout=30)
    r.raise_for_status()
    total = int(r.headers.get('content-length', 0))
    downloaded = 0
    with open(local, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded * 100 // total
                    log(f"  {pct}% ({downloaded}/{total} bytes)")
    log(f"Downloaded {downloaded} bytes to {local}")
    return local

def git_clone(repo, branch=None, dest=None, depth=1, lfs=True):
    dest = dest or os.path.basename(repo.rstrip('/').split('/')[-1].replace('.git', ''))
    cmd = ['git', 'clone']
    if depth:
        cmd += ['--depth', str(depth)]
    if branch:
        cmd += ['--branch', branch, '--single-branch']
    cmd += [repo, dest]
    run(cmd)
    if lfs:
        try:
            run(['git', 'lfs', 'pull'], cwd=dest)
        except:
            log("git lfs not available, skipping LFS pull")
    log(f"Cloned {repo} into {dest}")
    return dest

def mirror_website(start_url, output_dir='site_mirror', max_depth=1000):
    log(f"Mirroring website: {start_url}")
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (compatible; SiteMirror/1.0)'})
    domain = urlparse(start_url).netloc
    visited = set()
    queue = [(start_url, 0)]
    os.makedirs(output_dir, exist_ok=True)
    css_url_pattern = re.compile(r'url\([\'"]?([^\'")\s]+)[\'"]?\)')

    def local_path(url):
        parsed = urlparse(url)
        path = parsed.path.lstrip('/')
        if not path or path.endswith('/'):
            path += 'index.html'
        return os.path.join(output_dir, domain, path)

    def download_file(url):
        if url in visited:
            return None
        visited.add(url)
        try:
            resp = session.get(url, timeout=10)
            if resp.status_code != 200:
                return None
            path = local_path(url)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'wb') as f:
                f.write(resp.content)
            log(f"  Downloaded: {url}")
            return path, resp
        except Exception as e:
            log(f"  Failed: {url} - {e}")
            return None

    def rewrite_asset_url(url, base_url):
        if not url or url.startswith('data:'):
            return url
        if urlparse(url).netloc and urlparse(url).netloc != domain:
            return url
        abs_url = urljoin(base_url, url)
        dl = download_file(abs_url)
        return '/' + urlparse(abs_url).path.lstrip('/')

    while queue:
        url, depth = queue.pop(0)
        if depth > max_depth or url in visited:
            continue
        dl = download_file(url)
        if not dl:
            continue
        path, resp = dl
        if 'text/html' not in resp.headers.get('content-type', ''):
            continue
        soup = BeautifulSoup(resp.content, 'lxml')
        base_url = resp.url
        for tag in soup.find_all(['a','link','script','img','source']):
            if tag.name == 'a' and tag.has_attr('href'):
                href = tag['href']
                if not urlparse(href).netloc or urlparse(href).netloc == domain:
                    abs_href = urljoin(base_url, href)
                    if urlparse(abs_href).netloc == domain and abs_href not in visited:
                        queue.append((abs_href, depth+1))
                        tag['href'] = '/' + urlparse(abs_href).path.lstrip('/')
            elif tag.name == 'link' and tag.has_attr('href'):
                tag['href'] = rewrite_asset_url(tag['href'], base_url)
            elif tag.name == 'script' and tag.has_attr('src'):
                tag['src'] = rewrite_asset_url(tag['src'], base_url)
            elif tag.name == 'img' and tag.has_attr('src'):
                tag['src'] = rewrite_asset_url(tag['src'], base_url)
            elif tag.name == 'source' and tag.has_attr('srcset'):
                srcset = tag['srcset']
                parts = []
                for part in srcset.split(','):
                    part = part.strip()
                    if part:
                        url_part = part.split(' ')[0]
                        new_url = rewrite_asset_url(url_part, base_url)
                        parts.append(part.replace(url_part, new_url, 1))
                tag['srcset'] = ', '.join(parts)
        with open(path, 'wb') as f:
            f.write(soup.prettify('utf-8'))
        for css_tag in soup.find_all('link', rel='stylesheet'):
            css_href = css_tag.get('href')
            if css_href:
                css_abs = urljoin(base_url, css_href) if (not urlparse(css_href).netloc or urlparse(css_href).netloc == domain) else None
                if css_abs and urlparse(css_abs).netloc == domain:
                    css_path = local_path(css_abs)
                    if os.path.exists(css_path):
                        with open(css_path, 'r', encoding='utf-8') as f:
                            css_content = f.read()
                        def replace_url(m):
                            u = m.group(1)
                            return f"url({rewrite_asset_url(u, css_abs)})"
                        new_css = css_url_pattern.sub(replace_url, css_content)
                        with open(css_path, 'w', encoding='utf-8') as f:
                            f.write(new_css)
    log("Website mirror completed")

def main():
    tasks_json = os.environ.get('TASKS_JSON', '[]')
    try:
        tasks = json.loads(tasks_json)
    except Exception as e:
        log(f"Invalid TASKS_JSON: {e}")
        sys.exit(1)
    if not tasks:
        log("No tasks defined in TASKS_JSON")
        sys.exit(0)
    out_root = os.environ.get('OUTPUT_DIR', 'downloads')
    os.makedirs(out_root, exist_ok=True)
    for i, task in enumerate(tasks):
        log(f"Task {i+1}/{len(tasks)}: {task.get('type')}")
        t = task.get('type')
        try:
            if t == 'direct':
                url = task['url']
                filename = task.get('filename')
                headers = task.get('headers')
                dest_path = os.path.join(out_root, filename or os.path.basename(urlparse(url).path) or 'file')
                download_direct(url, dest_path, headers)
            elif t == 'git':
                repo = task['repo']
                branch = task.get('branch')
                depth = task.get('depth', 1)
                lfs = task.get('lfs', True)
                dest = task.get('dest')
                if dest:
                    dest = os.path.join(out_root, dest)
                else:
                    dest = os.path.join(out_root, os.path.basename(repo.rstrip('/').split('/')[-1].replace('.git', '')))
                git_clone(repo, branch=branch, dest=dest, depth=depth, lfs=lfs)
            elif t == 'website':
                url = task['url']
                site_dir = os.path.join(out_root, task.get('output_dir', 'site_mirror'))
                mirror_website(url, output_dir=site_dir)
            else:
                log(f"Unknown task type: {t}")
        except Exception as e:
            log(f"Task failed: {e}")
    log("All tasks completed. Creating final ZIP...")
    zip_name = os.environ.get('ZIP_NAME', 'final_download.zip')
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(out_root):
            for file in files:
                full = os.path.join(root, file)
                arcname = os.path.relpath(full, out_root)
                zf.write(full, arcname)
    log(f"ZIP created: {zip_name}")

if __name__ == '__main__':
    main()
