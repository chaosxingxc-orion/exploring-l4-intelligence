# -*- coding: utf-8 -*-
import json, os

BASE = "/mnt/c/Users/35686/AppData/Local/Temp/claude/D--chao-workspace-exploring-l4-intelligence-projects-speech-mllm-training-free-rl/cbe193a3-c6e4-4827-9482-f4379759edd9"
INFILE = BASE + "/tasks/wm13eoo4d.output"
OUT = "/mnt/d/chao_workspace/exploring-l4-intelligence/papers/agent-level-tfrl"
os.makedirs(OUT + "/sections", exist_ok=True)

data = json.load(open(INFILE, encoding="utf-8"))
root = data.get("result", data)
sections = root.get("sections", [])
sections = sorted(sections, key=lambda s: s.get("key",""))

PREAMBLE = r"""\documentclass[10pt]{article}

% Self-contained NeurIPS-approximating preamble (robust; no external .sty).
\usepackage[letterpaper,margin=1in]{geometry}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage{amsmath,amssymb,amsfonts,amsthm,mathtools}

% ---- map literal Unicode math symbols to LaTeX (robustness for writer output) ----
\DeclareUnicodeCharacter{03B1}{\ensuremath{\alpha}}
\DeclareUnicodeCharacter{03B2}{\ensuremath{\beta}}
\DeclareUnicodeCharacter{03B3}{\ensuremath{\gamma}}
\DeclareUnicodeCharacter{03B4}{\ensuremath{\delta}}
\DeclareUnicodeCharacter{03B5}{\ensuremath{\varepsilon}}
\DeclareUnicodeCharacter{03B8}{\ensuremath{\theta}}
\DeclareUnicodeCharacter{03BA}{\ensuremath{\kappa}}
\DeclareUnicodeCharacter{03BB}{\ensuremath{\lambda}}
\DeclareUnicodeCharacter{03BC}{\ensuremath{\mu}}
\DeclareUnicodeCharacter{03BD}{\ensuremath{\nu}}
\DeclareUnicodeCharacter{03C0}{\ensuremath{\pi}}
\DeclareUnicodeCharacter{03C1}{\ensuremath{\rho}}
\DeclareUnicodeCharacter{03C3}{\ensuremath{\sigma}}
\DeclareUnicodeCharacter{03C4}{\ensuremath{\tau}}
\DeclareUnicodeCharacter{03C6}{\ensuremath{\varphi}}
\DeclareUnicodeCharacter{03C8}{\ensuremath{\psi}}
\DeclareUnicodeCharacter{03C9}{\ensuremath{\omega}}
\DeclareUnicodeCharacter{0394}{\ensuremath{\Delta}}
\DeclareUnicodeCharacter{0398}{\ensuremath{\Theta}}
\DeclareUnicodeCharacter{039B}{\ensuremath{\Lambda}}
\DeclareUnicodeCharacter{03A0}{\ensuremath{\Pi}}
\DeclareUnicodeCharacter{03A3}{\ensuremath{\Sigma}}
\DeclareUnicodeCharacter{03A6}{\ensuremath{\Phi}}
\DeclareUnicodeCharacter{03A8}{\ensuremath{\Psi}}
\DeclareUnicodeCharacter{03A9}{\ensuremath{\Omega}}
\DeclareUnicodeCharacter{2211}{\ensuremath{\sum}}
\DeclareUnicodeCharacter{220F}{\ensuremath{\prod}}
\DeclareUnicodeCharacter{222B}{\ensuremath{\int}}
\DeclareUnicodeCharacter{221E}{\ensuremath{\infty}}
\DeclareUnicodeCharacter{221D}{\ensuremath{\propto}}
\DeclareUnicodeCharacter{221A}{\ensuremath{\sqrt{}}}
\DeclareUnicodeCharacter{2264}{\ensuremath{\leq}}
\DeclareUnicodeCharacter{2265}{\ensuremath{\geq}}
\DeclareUnicodeCharacter{2260}{\ensuremath{\neq}}
\DeclareUnicodeCharacter{2248}{\ensuremath{\approx}}
\DeclareUnicodeCharacter{2208}{\ensuremath{\in}}
\DeclareUnicodeCharacter{2209}{\ensuremath{\notin}}
\DeclareUnicodeCharacter{2282}{\ensuremath{\subset}}
\DeclareUnicodeCharacter{2286}{\ensuremath{\subseteq}}
\DeclareUnicodeCharacter{2200}{\ensuremath{\forall}}
\DeclareUnicodeCharacter{2203}{\ensuremath{\exists}}
\DeclareUnicodeCharacter{2207}{\ensuremath{\nabla}}
\DeclareUnicodeCharacter{2202}{\ensuremath{\partial}}
\DeclareUnicodeCharacter{2192}{\ensuremath{\rightarrow}}
\DeclareUnicodeCharacter{21A6}{\ensuremath{\mapsto}}
\DeclareUnicodeCharacter{00D7}{\ensuremath{\times}}
\DeclareUnicodeCharacter{2297}{\ensuremath{\otimes}}
\DeclareUnicodeCharacter{2295}{\ensuremath{\oplus}}
\DeclareUnicodeCharacter{2225}{\ensuremath{\|}}
\DeclareUnicodeCharacter{00B7}{\ensuremath{\cdot}}
\DeclareUnicodeCharacter{22C5}{\ensuremath{\cdot}}
\DeclareUnicodeCharacter{00B1}{\ensuremath{\pm}}
\DeclareUnicodeCharacter{211D}{\ensuremath{\mathbb{R}}}
\DeclareUnicodeCharacter{2115}{\ensuremath{\mathbb{N}}}
\DeclareUnicodeCharacter{2124}{\ensuremath{\mathbb{Z}}}
\DeclareUnicodeCharacter{211A}{\ensuremath{\mathbb{Q}}}
\DeclareUnicodeCharacter{2113}{\ensuremath{\ell}}
\DeclareUnicodeCharacter{2605}{\ensuremath{\star}}
\DeclareUnicodeCharacter{22C6}{\ensuremath{\star}}
\DeclareUnicodeCharacter{2227}{\ensuremath{\land}}
\DeclareUnicodeCharacter{2228}{\ensuremath{\lor}}
\DeclareUnicodeCharacter{00AC}{\ensuremath{\neg}}
\DeclareUnicodeCharacter{2308}{\ensuremath{\lceil}}
\DeclareUnicodeCharacter{2309}{\ensuremath{\rceil}}
\DeclareUnicodeCharacter{230A}{\ensuremath{\lfloor}}
\DeclareUnicodeCharacter{230B}{\ensuremath{\rfloor}}
\DeclareUnicodeCharacter{2026}{\ldots}
\DeclareUnicodeCharacter{2212}{\ensuremath{-}}
\DeclareUnicodeCharacter{2032}{\ensuremath{\prime}}
\DeclareUnicodeCharacter{2080}{\ensuremath{_{0}}}
\DeclareUnicodeCharacter{2081}{\ensuremath{_{1}}}
\DeclareUnicodeCharacter{2082}{\ensuremath{_{2}}}
\DeclareUnicodeCharacter{2083}{\ensuremath{_{3}}}
\DeclareUnicodeCharacter{2084}{\ensuremath{_{4}}}
\DeclareUnicodeCharacter{2096}{\ensuremath{_{k}}}
\DeclareUnicodeCharacter{1D62}{\ensuremath{_{i}}}
\DeclareUnicodeCharacter{2C7C}{\ensuremath{_{j}}}
\DeclareUnicodeCharacter{2070}{\ensuremath{^{0}}}
\DeclareUnicodeCharacter{00B9}{\ensuremath{^{1}}}
\DeclareUnicodeCharacter{00B2}{\ensuremath{^{2}}}
\DeclareUnicodeCharacter{00B3}{\ensuremath{^{3}}}
\DeclareUnicodeCharacter{2061}{}
\DeclareUnicodeCharacter{2062}{}
\usepackage{natbib}
\usepackage{booktabs}
\usepackage{microtype}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{caption}
\usepackage{enumitem}
\usepackage{listings}
\usepackage[colorlinks=true,linkcolor=blue,citecolor=blue,urlcolor=blue]{hyperref}
\usepackage{url}
\usepackage[capitalize]{cleveref}
\usepackage{setspace}

\bibliographystyle{plainnat}
\setlength{\parskip}{2pt}

% ---- theorem environments ----
\theoremstyle{plain}
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\newtheorem{corollary}{Corollary}
\newtheorem{proposition}{Proposition}
\newtheorem{conjecture}{Conjecture}
\theoremstyle{definition}
\newtheorem{definition}{Definition}
\newtheorem{assumption}{Assumption}
\theoremstyle{remark}
\newtheorem{remark}{Remark}

% cleveref names for custom theorem-like environments
\crefname{assumption}{Assumption}{Assumptions}
\Crefname{assumption}{Assumption}{Assumptions}
\crefname{definition}{Definition}{Definitions}
\Crefname{definition}{Definition}{Definitions}
\crefname{proposition}{Proposition}{Propositions}
\Crefname{proposition}{Proposition}{Propositions}
\crefname{conjecture}{Conjecture}{Conjectures}
\Crefname{conjecture}{Conjecture}{Conjectures}
\crefname{remark}{Remark}{Remarks}
\Crefname{remark}{Remark}{Remarks}

% ---- shared notation macros (\ensuremath so they work in text OR math mode) ----
\newcommand{\cZ}{\ensuremath{\mathcal{Z}}}
\newcommand{\cZA}{\ensuremath{\mathcal{Z}_{\mathrm{A}}}}
\newcommand{\cZB}{\ensuremath{\mathcal{Z}_{\mathrm{B}}}}
\newcommand{\qo}{\ensuremath{q_{0}}}
\newcommand{\qz}{\ensuremath{q}}
\newcommand{\qs}{\ensuremath{q^{\star}}}
\newcommand{\Rwd}{\ensuremath{R}}
\newcommand{\Zpart}{\ensuremath{Z}}
\newcommand{\gain}{\ensuremath{\mathcal{G}}}
\newcommand{\spread}{\ensuremath{\mathrm{spread}}}
\newcommand{\Exp}{\ensuremath{\mathbb{E}}}
\newcommand{\KL}[2]{\ensuremath{\mathrm{KL}\!\left(#1 \,\|\, #2\right)}}
\newcommand{\Fobj}[1]{\ensuremath{F\!\left(#1\right)}}
\newcommand{\R}{\ensuremath{\mathbb{R}}}
% safety aliases sometimes used by writers
\providecommand{\E}{\ensuremath{\mathbb{E}}}
\providecommand{\reals}{\ensuremath{\mathbb{R}}}
\providecommand{\bbR}{\ensuremath{\mathbb{R}}}
\providecommand{\bbN}{\ensuremath{\mathbb{N}}}
\providecommand{\bbZ}{\ensuremath{\mathbb{Z}}}
\providecommand{\bbQ}{\ensuremath{\mathbb{Q}}}
\providecommand{\bbE}{\ensuremath{\mathbb{E}}}
\providecommand{\bbP}{\ensuremath{\mathbb{P}}}
\providecommand{\Tr}{\ensuremath{\mathrm{Tr}}}
\providecommand{\diag}{\ensuremath{\mathrm{diag}}}
\providecommand{\sgn}{\ensuremath{\mathrm{sgn}}}
\providecommand{\eqdef}{\ensuremath{\coloneqq}}
\DeclareMathOperator*{\argmax}{arg\,max}
\DeclareMathOperator*{\argmin}{arg\,min}

\lstset{basicstyle=\ttfamily\footnotesize,breaklines=true,columns=fullflexible,
  keepspaces=true,showstringspaces=false,frame=single,framesep=3pt}

\title{Training-Free RL as Verifiable-Reward Selection on a Single Frozen
Speech Model:\\[2pt]
\large Content and Intent Gains, a Scoped Paralinguistic Negative, and a Reward-Spread Lens}

\author{Exploring-L4-Intelligence Project}
\date{}

\begin{document}
\maketitle
"""

FOOTER = "\n\n\\bibliography{references}\n\n\\end{document}\n"

parts = [PREAMBLE]
total_words = 0
manifest = []
for s in sections:
    key = s.get("key","?")
    tex = s.get("latex","") or ""
    # fix double-superscript from \qs (=q^{\star}) followed by ^ or ': group it.
    tex = tex.replace("\\qs^", "{\\qs}^").replace("\\qs'", "{\\qs}'").replace("\\qs{}^", "{\\qs}^")
    tex = tex.replace("sec:theory", "sec:osa")  # alias: theory section is labeled sec:osa
    wc = s.get("wordcount",0) or 0
    total_words += wc
    # write section file
    open(f"{OUT}/sections/{key}.tex","w",encoding="utf-8").write(tex)
    parts.append(f"\n\n% ===== section {key} (writer wordcount {wc}) =====\n")
    parts.append(tex)
    manifest.append((key, wc, len(tex)))

parts.append(FOOTER)
main = "".join(parts)
open(f"{OUT}/main.tex","w",encoding="utf-8").write(main)

print("sections:", len(sections))
for k,wc,n in manifest:
    print(f"  {k}: words={wc} chars={n}")
print("total writer words:", total_words)
print("main.tex chars:", len(main), "approx tokens:", len(main)//4)
