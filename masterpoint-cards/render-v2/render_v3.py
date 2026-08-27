# -*- coding: utf-8 -*-
"""Re-renderiza os 7 carrosseis MP com logos de software (Yan 2026-08-12) em render-v3/."""
import json
from pathlib import Path
import mp_carousel as mp
from render_posts import POSTS

OUT = Path(__file__).resolve().parent.parent / "render-v3"
OUT.mkdir(parents=True, exist_ok=True)

# relatorio de quais itens receberam logo
report = {}
for slug, carr in POSTS.items():
    hits = []
    for s in carr["slides"]:
        if s.get("tipo") == "lista":
            for it in s["itens"]:
                lg = mp.logo_for_item(it)
                hits.append((it, lg))
    report[slug] = hits

manifest = {}
for slug, carr in POSTS.items():
    dst = OUT / slug
    paths = mp.render_carrossel(carr, dst)
    manifest[slug] = {"n_slides": len(paths), "arquivos": [p.split("/")[-1] for p in paths]}
    print(f"OK {slug}: {len(paths)} slides")

json.dump(manifest, open(OUT / "manifest.json", "w"), ensure_ascii=False, indent=2)

print("\n===== LOGOS POR ITEM DE LISTA =====")
for slug, hits in report.items():
    print(f"\n# {slug}")
    for it, lg in hits:
        mark = lg if lg else "-- (sem logo)"
        print(f"  [{mark:>16}]  {it}")

print("\nTOTAL posts:", len(POSTS), "| total slides:", sum(m["n_slides"] for m in manifest.values()))
