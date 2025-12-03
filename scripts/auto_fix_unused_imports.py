#!/usr/bin/env python3
"""Simple heuristic script to remove clearly unused top-level imports.

Rules:
- Parses top-level import and from-import statements until first non-import
  statement.
- For each imported name, check if it appears elsewhere in the file (naive
  substring search excluding the import lines). If not found, remove the
  import clause or the whole import line for simple cases.

This is a best-effort automated fix (may produce false-positives). It
commits changes on a new git branch so you can review them before merging.
"""

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

IMPORT_RE = re.compile(
    r'^(from\s+([\w\.]+)\s+import\s+(.*)|import\s+(.*))' )


def analyze_file(path: Path) -> tuple[bool, str]:
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()

    # collect top-level import lines
    import_lines_idx = []
    for i, line in enumerate(lines):
        if line.strip() == '' or line.lstrip().startswith('#'):
            continue
        if IMPORT_RE.match(line):
            import_lines_idx.append(i)
            continue
        # stop at first non-import
        break

    if not import_lines_idx:
        return False, text

    imports = []  # (idx, line, type, names:list[str])
    for i in import_lines_idx:
        line = lines[i]
        m = IMPORT_RE.match(line)
        if not m:
            continue
        if m.group(2):
            # from X import a, b as c
            raw = m.group(3)
            names = [p.strip().split(' as ')[-1] for p in raw.split(',')]
            imports.append((i, line, 'from', names))
        else:
            raw = m.group(4)
            names = [p.strip().split(' as ')[-1] for p in raw.split(',')]
            imports.append((i, line, 'import', names))

    body = '\n'.join([l for idx, l in enumerate(lines)
                      if idx not in import_lines_idx])

    remove_idxs = set()
    for idx, line, itype, names in imports:
        unused = []
        for name in names:
            # naive check: word boundary search in body
            if re.search(rf'\b{re.escape(name)}\b', body) is None:
                unused.append(name)
        if unused:
            # if all names unused -> remove whole line
            if set(unused) == set(names):
                remove_idxs.add(idx)
            else:
                # partial: rewrite line removing unused names
                kept = [n for n in names if n not in unused]
                if itype == 'import':
                    new_line = 'import ' + ', '.join(kept)
                else:
                    new_line = re.sub(
                        r'import\s+.*$',
                        'import ' + ', '.join(kept),
                        line,
                    )
                lines[idx] = new_line

    if not remove_idxs:
        return False, text

    new_lines = [l for i, l in enumerate(lines)
                 if i not in remove_idxs]
    new_text = '\n'.join(new_lines) + (
        '\n' if text.endswith('\n') else '' )
    return True, new_text


def main():
    py_files = [
        p for p in ROOT.rglob('*.py')
        if '.venv' not in p.parts and p.is_file()
    ]
    modified = []
    for p in py_files:
        ok, new_text = analyze_file(p)
        if ok:
            backup = p.with_suffix(p.suffix + '.bak')
            p.rename(backup)
            p.write_text(new_text, encoding='utf-8')
            modified.append((p, backup))

    if not modified:
        print('No changes made (no unused imports found).')
        return

    print(f'Updated {len(modified)} files:')
    for p, b in modified:
        print(f' - {p}  (backup: {b.name})')

    # Commit changes on a new branch
    branch = 'fix/auto-unused-imports'
    os.system(f'git checkout -b {branch} >/dev/null 2>&1 '
              f'|| git checkout {branch}')
    os.system('git add -A')
    msg = 'chore: remove unused imports (auto-fixed)'
    rc = os.system(f'git commit -m "{msg}" || true')
    if rc == 0:
        print('Committed changes.')
    else:
        print('No commit created (nothing staged).')


if __name__ == '__main__':
    main()
