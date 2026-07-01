# -*- coding: utf-8 -*-
# Apply a revision-workflow JSON to the on-disk section files, then assemble main.tex
# from the section files (the section files are the source of truth from now on).
import json, os, sys, glob

BASE = "/mnt/c/Users/35686/AppData/Local/Temp/claude/D--chao-workspace-exploring-l4-intelligence-projects-speech-mllm-training-free-rl/cbe193a3-c6e4-4827-9482-f4379759edd9"
OUT = "/mnt/d/chao_workspace/exploring-l4-intelligence/papers/agent-level-tfrl"
SECT = OUT + "/sections"

# read the preamble from the canonical (repo) assemble.py so it stays in sync
# (the scratchpad copy is ephemeral across sessions; the repo _build copy is durable)
import re
asm = open(OUT + "/_build/assemble.py", encoding="utf-8").read()
PREAMBLE = asm.split('PREAMBLE = r"""', 1)[1].split('"""', 1)[0]
FOOTER = "\n\n\\bibliography{references}\n\n\\end{document}\n"

def postproc(tex):
    tex = tex.replace("\\qs^", "{\\qs}^").replace("\\qs'", "{\\qs}'").replace("\\qs{}^", "{\\qs}^")
    tex = tex.replace("sec:theory", "sec:osa")
    return tex

# 1. apply revisions (if a revision JSON path is given)
if len(sys.argv) > 1:
    rev = json.load(open(sys.argv[1], encoding="utf-8"))
    root = rev.get("result", rev)
    for s in root.get("sections", []):
        key = s.get("key"); tex = s.get("latex", "")
        if key and tex:
            open(f"{SECT}/{key}.tex", "w", encoding="utf-8").write(postproc(tex))
            print(f"  applied revision -> {key}.tex ({len(tex)} chars)")

# 2. assemble main.tex from ALL section files on disk
files = sorted(glob.glob(f"{SECT}/*.tex"))
parts = [PREAMBLE]
total = 0
for f in files:
    tex = open(f, encoding="utf-8").read()
    key = os.path.basename(f)[:-4]
    parts.append(f"\n\n% ===== section {key} =====\n")
    parts.append(tex)
    total += len(tex)
parts.append(FOOTER)
main = "".join(parts)
open(f"{OUT}/main.tex", "w", encoding="utf-8").write(main)
print(f"assembled {len(files)} sections; main.tex {len(main)} chars (~{len(main)//4} tokens)")
