"""
P4A Mirror Bootstrap - automatically patches python-for-android recipe URLs
to use mirrors (USTC) instead of GNU/savannah/sourceforge which often 502.

This module is loaded via .pth file at Python startup, so it works in
buildozer subprocesses too.
"""
import os
import sys

def patch_p4a_recipes():
    """Patch all p4a recipe URLs to use mirrors."""
    try:
        import pythonforandroid
        p4a_dir = os.path.dirname(pythonforandroid.__file__)
        recipes_dir = os.path.join(p4a_dir, 'recipes')
        if not os.path.isdir(recipes_dir):
            return

        # URL replacements: (original, mirror)
        replacements = [
            # freetype from savannah
            ('download.savannah.gnu.org/releases/freetype',
             'mirrors.ustc.edu.cn/gnu/freetype'),
            # generic GNU
            ('ftp.gnu.org/gnu', 'mirrors.ustc.edu.cn/gnu'),
            ('ftp.gnu.org/pub/gnu', 'mirrors.ustc.edu.cn/gnu'),
            ('ftp.gnu.org/gnu/', 'mirrors.ustc.edu.cn/gnu/'),
            # libpng from sourceforge
            ('download.sourceforge.net/project/libpng',
             'mirrors.ustc.edu.cn/gnu/libpng'),
            ('sourceforge.net/projects/libpng/files',
             'mirrors.ustc.edu.cn/gnu/libpng'),
            # libjpeg-turbo
            ('sourceforge.net/projects/libjpeg-turbo/files',
             'github.com/libjpeg-turbo/libjpeg-turbo/releases/download'),
        ]

        patched = 0
        for root, dirs, files in os.walk(recipes_dir):
            for f in files:
                if f.endswith('.py'):
                    filepath = os.path.join(root, f)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as fp:
                            content = fp.read()
                        original = content
                        for old, new in replacements:
                            content = content.replace(old, new)
                        if content != original:
                            with open(filepath, 'w', encoding='utf-8') as fp:
                                fp.write(content)
                            patched += 1
                    except Exception:
                        pass
        if patched > 0:
            print(f"[p4a_mirror] Patched {patched} recipe files with mirror URLs")
    except ImportError:
        # p4a not installed yet, will be patched when imported later
        pass
    except Exception as e:
        print(f"[p4a_mirror] Patch failed: {e}", file=sys.stderr)

# Execute at import time (called from .pth)
patch_p4a_recipes()
