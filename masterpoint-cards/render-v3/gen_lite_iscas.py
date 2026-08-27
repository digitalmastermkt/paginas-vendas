# -*- coding: utf-8 -*-
"""
gen_lite_iscas.py — Gera criativos de "CURSO GRATIS" (isca) pros cursos LITE
do catalogo Master Point, formato "comenta pra ganhar acesso".

- FEED: cards single 1080x1350 (render_singles.py) tipo 'alerta' (badge CURSO GRATIS
  dourado, headline do curso, sub "e rapido e com certificado", CTA pill isca).
- STORIES: 1080x1920 (render_stories.py) tipo 'alerta'/'hero' com paletas variadas.

Escreve os itens em STAGING (nao toca nas filas vivas):
  queue/mp_ig_queue_LITE_staging.json
  stories/queue/mp_ig_stories_LITE_staging.json

Hospeda imagens em:
  insta-masterpoint-linkbio/posts/<slug>/card.png
  insta-masterpoint-linkbio/stories/<slug>/story.png

CTA isca padrao: "Comenta EU QUERO que eu te envio como garantir sua vaga gratis".
Deixa claro que e curso LITE/rapido (nao promete o completo de graca).
PT-BR acentuado. Sem inventar preco/estatistica.
"""
import json
from pathlib import Path

import render_singles as RS
import render_stories as ST

LINKBIO = Path("/opt/NAIA-MASTER/workspace/insta-masterpoint-linkbio")
POSTS_DIR = LINKBIO / "posts"
STORIES_DIR = LINKBIO / "stories"
FEED_STAGING = LINKBIO / "queue" / "mp_ig_queue_LITE_staging.json"
STORIES_STAGING = LINKBIO / "stories" / "queue" / "mp_ig_stories_LITE_staging.json"

BASE = "https://insta.masterpointcursos.com.br"
WA_LINK = "https://wa.me/5586998046242"
WA_NUM = "(86) 99804-6242"

HASH_BASE = "#masterpointcursos #casteloDoPiaui #piaui"

# CTA isca padrao (curto p/ caber na pill do card)
CTA_ISCA = "COMENTA EU QUERO"


def caption(gancho_curso, corpo, palavra, tema_hashtags):
    """Monta legenda isca completa, acentuada, com regra de comentario."""
    return (
        f"CURSO GRÁTIS: {gancho_curso} \U0001f381\n\n"
        f"{corpo}\n\n"
        f"É a versão LITE (rápida e direta ao ponto) e você sai com CERTIFICADO. "
        f"Não é o curso completo, é o conteúdo essencial pra você começar HOJE, de graça.\n\n"
        f"COMO GARANTIR SUA VAGA GRÁTIS:\n"
        f"Comenta \"{palavra}\" aqui embaixo (ou o nome do curso) que a gente te manda no directo "
        f"o passo a passo pra liberar seu acesso.\n\n"
        f"Prefere adiantar? Chama no WhatsApp {WA_NUM}.\n"
        f"\U0001f4f2 {WA_LINK}\n.\n.\n"
        f"{tema_hashtags} {HASH_BASE}"
    )


# ============================================================
# FEED — 8 criativos single (tipo alerta), 1 curso LITE cada
# ============================================================
# Cada item: slug, badge, headline, sub, cta_pill, palavra (a de comentar),
#            corpo (legenda), hashtags do tema.
FEED = [
    {
        "slug": "lite-excel-gratis",
        "headline": "Excel do zero, de graça",
        "sub": "Rápido, prático e com certificado.",
        "palavra": "EU QUERO",
        "corpo": (
            "Planilha é a habilidade que quase TODA vaga de escritório pede. "
            "No Excel Fundamental LITE você aprende o essencial pra montar suas primeiras "
            "planilhas e parar de travar na hora que o chefe pede um relatório."
        ),
        "tags": "#excel #cursodeexcel #informatica #planilhas #qualificacaoprofissional #cursogratis",
    },
    {
        "slug": "lite-ia-gratis",
        "headline": "Aprenda Inteligência Artificial de graça",
        "sub": "Comece a usar IA hoje, com certificado.",
        "palavra": "EU QUERO",
        "corpo": (
            "IA parou de ser coisa do futuro. No Inteligência Artificial LITE você entende "
            "de forma simples como usar as ferramentas de IA no dia a dia pra trabalhar mais "
            "rápido e se destacar, mesmo começando do zero."
        ),
        "tags": "#inteligenciaartificial #ia #chatgpt #produtividade #cursogratis #tecnologia",
    },
    {
        "slug": "lite-marketing-digital-gratis",
        "headline": "Marketing Digital do zero, grátis",
        "sub": "O primeiro passo pra vender pela internet.",
        "palavra": "EU QUERO",
        "corpo": (
            "Todo negócio hoje precisa aparecer na internet. No Marketing Digital LITE você "
            "aprende os fundamentos pra começar a divulgar, atrair clientes e entender como "
            "funciona a venda online, sem enrolação."
        ),
        "tags": "#marketingdigital #marketing #vendasonline #empreendedorismo #cursogratis",
    },
    {
        "slug": "lite-photoshop-gratis",
        "headline": "Photoshop do zero, de graça",
        "sub": "Edite imagens como profissional. Com certificado.",
        "palavra": "EU QUERO",
        "corpo": (
            "Quer aprender a editar fotos e criar artes que impressionam? O Adobe Photoshop "
            "LITE te dá a base pra dominar a ferramenta de edição mais usada do mundo e sair "
            "criando desde já."
        ),
        "tags": "#photoshop #design #edicaodeimagem #designgrafico #cursogratis #adobe",
    },
    {
        "slug": "lite-capcut-gratis",
        "headline": "Edite vídeos no CapCut, de graça",
        "sub": "Do celular pro feed. Rápido e com certificado.",
        "palavra": "EU QUERO",
        "corpo": (
            "Quer editar vídeos pro Instagram e TikTok que prendem a atenção? No CapCut LITE "
            "você aprende a cortar, legendar e finalizar seus vídeos direto do celular, do "
            "jeito que os criadores fazem."
        ),
        "tags": "#capcut #edicaodevideo #reels #tiktok #criadordeconteudo #cursogratis",
    },
    {
        "slug": "lite-powerbi-gratis",
        "headline": "Power BI do zero, grátis",
        "sub": "Transforme dados em dashboard. Com certificado.",
        "palavra": "EU QUERO",
        "corpo": (
            "Empresa nenhuma decide no achismo. No Power BI Desktop LITE você dá o primeiro "
            "passo pra transformar planilhas em painéis visuais e virar aquela pessoa que "
            "entrega relatório de respeito."
        ),
        "tags": "#powerbi #dados #dashboard #businessintelligence #excel #cursogratis",
    },
    {
        "slug": "lite-ilustrador-gratis",
        "headline": "Illustrator do zero, de graça",
        "sub": "Crie logos e artes vetoriais. Com certificado.",
        "palavra": "EU QUERO",
        "corpo": (
            "Sonha em criar logotipos e artes que não perdem qualidade? O Adobe Illustrator "
            "LITE te ensina a base do desenho vetorial, a ferramenta que todo designer "
            "profissional usa."
        ),
        "tags": "#illustrator #design #logotipo #designgrafico #vetor #cursogratis #adobe",
    },
    {
        "slug": "lite-financeira-gratis",
        "headline": "Educação Financeira, de graça",
        "sub": "Assuma o controle do seu dinheiro. Com certificado.",
        "palavra": "EU QUERO",
        "corpo": (
            "Não é quanto você ganha, é como você organiza. No Educação Financeira LITE você "
            "aprende de forma simples a controlar gastos, sair do vermelho e começar a "
            "guardar dinheiro de verdade."
        ),
        "tags": "#educacaofinanceira #financas #dinheiro #organizacaofinanceira #cursogratis",
    },
]


# ============================================================
# STORIES — 6 criativos (paletas variadas), 1 curso LITE cada
# ============================================================
# tipo alerta/hero; palette gold/teal/wine. CTA aponta pro comentario/directo.
STORIES = [
    {
        "slug": "lite-excel-gratis-story",
        "tipo": "alerta", "palette": "gold",
        "badge": "Curso grátis",
        "headline": "Excel do zero, de graça",
        "sub": "Comenta EU QUERO no post que eu te mando o acesso.",
        "cta_pill": "COMENTA EU QUERO",
        "curso": "Excel Fundamental LITE",
    },
    {
        "slug": "lite-ia-gratis-story",
        "tipo": "hero", "palette": "teal",
        "eyebrow": "Curso grátis com certificado",
        "hero": "IA de graça",
        "sub": "Comenta EU QUERO no post e libere seu acesso ao IA LITE.",
        "cta_pill": "COMENTA EU QUERO",
        "curso": "Inteligência Artificial LITE",
    },
    {
        "slug": "lite-marketing-gratis-story",
        "tipo": "alerta", "palette": "wine",
        "badge": "Curso grátis",
        "headline": "Marketing Digital do zero",
        "sub": "Comenta EU QUERO no post que a gente libera o acesso.",
        "cta_pill": "COMENTA EU QUERO",
        "curso": "Marketing Digital LITE",
    },
    {
        "slug": "lite-photoshop-gratis-story",
        "tipo": "alerta", "palette": "teal",
        "badge": "Curso grátis",
        "headline": "Photoshop do zero, grátis",
        "sub": "Comenta EU QUERO no post e receba o passo a passo.",
        "cta_pill": "COMENTA EU QUERO",
        "curso": "Adobe Photoshop LITE",
    },
    {
        "slug": "lite-capcut-gratis-story",
        "tipo": "hero", "palette": "wine",
        "eyebrow": "Curso grátis com certificado",
        "hero": "Edite vídeos de graça",
        "sub": "CapCut LITE. Comenta EU QUERO no post e libere seu acesso.",
        "cta_pill": "COMENTA EU QUERO",
        "curso": "CapCut LITE",
    },
    {
        "slug": "lite-powerbi-gratis-story",
        "tipo": "alerta", "palette": "gold",
        "badge": "Curso grátis",
        "headline": "Power BI do zero, grátis",
        "sub": "Comenta EU QUERO no post que eu te mando o acesso.",
        "cta_pill": "COMENTA EU QUERO",
        "curso": "Power BI Desktop LITE",
    },
]


def build_feed():
    items = []
    for f in FEED:
        slug = f["slug"]
        out = POSTS_DIR / slug / "card.png"
        slide = {
            "tipo": "alerta",
            "badge": "Curso grátis",
            "headline": f["headline"],
            "sub": f["sub"],
            "cta_pill": CTA_ISCA,
        }
        RS.render_single(slide, out)
        url = f"{BASE}/posts/{slug}/card.png"
        cap = caption(f["headline"], f["corpo"], f["palavra"], f["tags"])
        items.append({
            "slug": slug,
            "tipo": "alerta",
            "urls": [url],
            "caption": cap,
            "status": "pending",
        })
    FEED_STAGING.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    return items


def build_stories():
    items = []
    for s in STORIES:
        slug = s["slug"]
        out = STORIES_DIR / slug / "story.png"
        slide = {k: v for k, v in s.items() if k not in ("slug", "curso")}
        ST.render_story(slide, out)
        url = f"{BASE}/stories/{slug}/story.png"
        items.append({
            "slug": slug,
            "tipo": s["tipo"],
            "palette": s["palette"],
            "url": url,
            "status": "pending",
        })
    STORIES_STAGING.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    return items


if __name__ == "__main__":
    fi = build_feed()
    si = build_stories()
    print(f"FEED  : {len(fi)} cards")
    for it in fi:
        print("  -", it["slug"], "->", it["urls"][0])
    print(f"STORIES: {len(si)} cards")
    for it in si:
        print("  -", it["slug"], "(", it["palette"], ") ->", it["url"])
    print("STAGING FEED   :", FEED_STAGING)
    print("STAGING STORIES:", STORIES_STAGING)
