"""Check the knowledge base and pack it into hypoxia_kb.zip.

    python make_zip.py                          check hypoxia_kb/, then zip it
    python make_zip.py --from-chat cards.txt    first unpack cards a chat assistant wrote

--from-chat reads a text file in which each card starts with a line like
    === FILE: genes/NDRG1.md ===
and writes each card into hypoxia_kb/. (Optional: for cards written outside an agent.)
"""
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
KB = HERE / "hypoxia_kb"
OUT = HERE / "hypoxia_kb.zip"
MARK = re.compile(r"^=+\s*FILE:\s*(.+?)\s*=*\s*$")


def unpack(chat_file):
    text = Path(chat_file).read_text(encoding="utf-8")
    name, buf, written = None, [], []

    def flush():
        if name is None:
            return
        rel = Path(name.strip().strip("`"))
        if rel.is_absolute() or ".." in rel.parts or rel.suffix != ".md":
            print(f"  skipped {name}: must be a .md path inside the knowledge base")
            return
        body = "\n".join(buf).strip()
        dst = KB / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(body + "\n", encoding="utf-8")
        written.append(str(rel))

    for line in text.splitlines():
        m = MARK.match(line.strip())
        if m:
            flush()
            name, buf = m.group(1), []
        elif re.match(r"^\s*```", line):
            flush()                    # a closing code fence ends the file; chat text after it is not part of it
            name, buf = None, []
        elif name is not None:
            buf.append(line)
    flush()
    print(f"Unpacked {len(written)} files into {KB.name}/")
    for w in written:
        print("  ", w)


def main():
    args = sys.argv[1:]
    if args[:1] == ["--from-chat"]:
        if len(args) < 2:
            sys.exit("Say which file: python make_zip.py --from-chat cards.txt")
        unpack(args[1])

    own = HERE.parent / "1_proteomics" / "results.csv"
    results = own if own.exists() else HERE / "results_reference.csv"
    if not (KB / "my_results.csv").exists() and results.exists():
        shutil.copy(results, KB / "my_results.csv")
        print(f"Copied {results.name} to hypoxia_kb/my_results.csv")

    print("\nRunning the check...\n", flush=True)
    subprocess.run([sys.executable, str(KB / "tools" / "check_kb.py")])

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(KB.rglob("*")):
            if p.name.startswith(".") or "__pycache__" in p.parts:
                continue
            z.write(p, Path(KB.name) / p.relative_to(KB))
    print(f"\nWrote {OUT.name} ({OUT.stat().st_size / 1e6:.1f} MB).")
    print("hypoxia_kb.zip is in this folder: a copy of the knowledge base to share or archive.")
    print("Unzip it, then open the hypoxia_kb folder in Obsidian (Open folder as vault).")


if __name__ == "__main__":
    main()
