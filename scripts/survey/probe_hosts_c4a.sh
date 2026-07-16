#!/usr/bin/env bash
# C4A P0-R4 connectivity probe (temporary helper; audit canon = sf_t1_routes_status_audit.py)
set -u
for u in \
  "https://aclanthology.org/events/acl-2026/" \
  "https://papers.nips.cc/paper_files/paper/2026" \
  "https://proceedings.mlr.press/" \
  "https://openreview.net/group?id=ICLR.cc/2026/Conference" \
  "https://openaccess.thecvf.com/menu" \
  "https://www.isca-archive.org/interspeech_2026/index.html" \
  "https://dl.acm.org/conference/mm" \
  "https://ieeexplore.ieee.org/xpl/conhome/1000002/all-proceedings" \
; do
  code=$(curl -sL -o /dev/null -w "%{http_code}" --max-time 20 -A "Mozilla/5.0 (survey-audit)" "$u" 2>/dev/null) || code="CURL_ERR_$?"
  echo "$code $u"
  sleep 1
done
