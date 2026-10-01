#!/usr/bin/env python3
"""Copia el formato canónico de session-handoff a resume-from-handoff.

Uso:  python sync_format.py [--check]
  sin flags : copia references/handoff-format.md al skill hermano resume-from-handoff
  --check   : solo verifica que ambas copias sean idénticas (exit 1 si difieren)
Busca resume-from-handoff como carpeta hermana de session-handoff.
"""
import pathlib
import shutil
import sys

here = pathlib.Path(__file__).resolve().parent.parent  # session-handoff/
src = here / "references" / "handoff-format.md"
dst = here.parent / "resume-from-handoff" / "references" / "handoff-format.md"

if not dst.parent.parent.exists():
    sys.exit(f"No encuentro {dst.parent.parent}; ¿están las dos skills en la misma carpeta?")
if "--check" in sys.argv:
    same = dst.exists() and src.read_bytes() == dst.read_bytes()
    print("OK: formatos idénticos" if same else "DIFIEREN: ejecuta sync_format.py")
    sys.exit(0 if same else 1)
dst.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(src, dst)
print(f"Copiado {src} -> {dst}")
