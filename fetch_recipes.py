#!/usr/bin/env python3
"""
Fetch recipe source tarballs from multiple mirrors and save to prebuilt/.
Priority: GitHub > USTC mirror > GNU official > Savannah
"""
import os
import sys
import urllib.request
import ssl
import tarfile
import io

# Recipe filename -> list of mirror URLs (try in order)
RECIPES = {
    "freetype-2.14.1.tar.gz": [
        # GitHub tag archive (most reliable on Actions runners)
        "https://github.com/freetype/freetype/archive/refs/tags/VER-2-14-1.tar.gz",
        # USTC mirror
        "https://mirrors.ustc.edu.cn/gnu/freetype/freetype-2.14.1.tar.gz",
        # GNU official
        "https://ftp.gnu.org/gnu/freetype/freetype-2.14.1.tar.gz",
        # Savannah
        "https://download.savannah.gnu.org/releases/freetype/freetype-2.14.1.tar.gz",
    ],
}

def fetch_file(filename, urls):
    """Try downloading from multiple URLs. Returns True on success."""
    os.makedirs("prebuilt", exist_ok=True)
    filepath = os.path.join("prebuilt", filename)
    if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
        print(f"[OK] {filename} already exists ({os.path.getsize(filepath)} bytes)")
        return True

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    for url in urls:
        try:
            print(f"[TRY] {url}")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=120, context=ctx) as response:
                data = response.read()
                if len(data) > 1000:
                    # GitHub tag archives have different internal dir name, repackage if needed
                    if 'github.com' in url and 'freetype' in filename:
                        data = repackage_github_tarball(data, filename)
                    with open(filepath, 'wb') as f:
                        f.write(data)
                    print(f"[SUCCESS] {filename} downloaded from {url} ({len(data)} bytes)")
                    return True
                else:
                    print(f"[SKIP] {url} returned too small data ({len(data)} bytes)")
        except Exception as e:
            print(f"[FAIL] {url}: {e}")
    return False

def repackage_github_tarball(data, target_filename):
    """
    GitHub tag archives extract to 'freetype-VER-2-14-1/' but p4a expects 'freetype-2.14.1/'.
    Repackage with correct top-level dir name.
    """
    try:
        # Determine expected dir name from filename
        base = target_filename.replace('.tar.gz', '')
        # Read input tarball
        with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as tar:
            members = tar.getmembers()
            if not members:
                return data
            old_prefix = members[0].name.split('/')[0]
            if old_prefix == base:
                return data  # already correct
            print(f"[REPACKAGE] renaming '{old_prefix}' -> '{base}'")
            # Create new tarball
            out_buf = io.BytesIO()
            with tarfile.open(fileobj=out_buf, mode='w:gz') as out_tar:
                for member in members:
                    # Rewrite path
                    member.name = member.name.replace(old_prefix, base, 1)
                    if member.linkname:
                        member.linkname = member.linkname.replace(old_prefix, base, 1)
                    # Extract file content
                    f = tar.extractfile(member)
                    if f:
                        out_tar.addfile(member, f)
                    else:
                        out_tar.addfile(member)
            return out_buf.getvalue()
    except Exception as e:
        print(f"[REPACKAGE WARN] failed: {e}, using original")
        return data

def main():
    all_ok = True
    for filename, urls in RECIPES.items():
        if not fetch_file(filename, urls):
            print(f"[ERROR] Failed to download {filename}")
            all_ok = False
    if all_ok:
        print("\n=== All recipes downloaded successfully ===")
    else:
        print("\n=== Some recipes failed to download ===")
        sys.exit(1)

if __name__ == "__main__":
    main()
