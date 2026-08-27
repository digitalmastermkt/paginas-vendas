# -*- coding: utf-8 -*-
"""
render_stories.py — STORIES 1080x1920 (9:16) no padrao Master Point Cursos.

Reaproveita a engine mp_carousel.py (paleta, fontes Plus Jakarta/Inter/JetBrains,
logo, helpers de wrap/fit). Adapta canvas pra formato STORY 9:16.

3 paletas coerentes (Yan pediu variedade de cor):
  - "gold"  : preto/grafite + dourado (padrao da marca)
  - "teal"  : verde-escuro/petroleo + dourado suave (WCAG OK)
  - "wine"  : bordo/vinho profundo + dourado (WCAG OK)

Tipos de story:
  - alerta   : urgencia forte (vagas, ultima turma). badge pill + headline gigante + sub + CTA.
  - leve     : curiosidade / "voce sabia" / dica. badge contorno + headline + corpo + CTA.
  - hero     : palavra-heroi gigante dourada + watermark fantasma + sub + CTA.
  - cta      : story dedicado ao "chama no WhatsApp" (fundo do acento da paleta).

Todo texto vem pronto e ACENTUADO (o autor do queue garante PT-BR correto).
Area segura de story: margens generosas no topo (perfil/mute) e base (barra de resposta).
Design construido (Pillow puro), custo R$0. NUNCA "facao".
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageChops

# importa a engine irma (fontes, logo, helpers, marca)
ENGINE_DIR = Path("/opt/NAIA-MASTER/workspace/paginas-vendas/masterpoint-cards/render-v2")
sys.path.insert(0, str(ENGINE_DIR))
import mp_carousel as E  # noqa: E402

# ---------- Canvas STORY 9:16 ----------
W, H = 1080, 1920
MARGIN = 90
SAFE_W = W - 2 * MARGIN
# area segura vertical: topo livre p/ nome do perfil / botao mute;
# base livre p/ barra "enviar mensagem" e stickers de link.
SAFE_TOP = 250
SAFE_BOTTOM = H - 230           # nada de texto/CTA abaixo disso

# ---------- Paletas ----------
# Cada paleta define fundo (top/bottom do gradiente), glow e um acento.
# GOLD_TEXT / INK / MUTED / PRETO_QUENTE herdados da engine (funcionam em fundo escuro).
PALETTES = {
    "gold": {
        "bg_top": (18, 17, 14),
        "bg_bottom": (10, 10, 9),
        "glow": (70, 52, 20),
        "accent": (224, 179, 74),        # dourado solido (E.GOLD)
        "accent_text": (230, 189, 86),   # dourado texto (E.GOLD_TEXT)
        "on_accent": (20, 18, 16),        # texto sobre o acento
        "line": (60, 55, 44),
    },
    "teal": {
        "bg_top": (12, 34, 33),          # petroleo profundo
        "bg_bottom": (6, 20, 20),
        "glow": (16, 66, 60),
        "accent": (224, 179, 74),        # dourado como acento (contrasta no teal)
        "accent_text": (233, 198, 110),
        "on_accent": (10, 26, 25),
        "line": (34, 68, 64),
    },
    "wine": {
        "bg_top": (46, 16, 24),          # bordo profundo
        "bg_bottom": (26, 9, 14),
        "glow": (96, 32, 44),
        "accent": (224, 179, 74),
        "accent_text": (236, 200, 118),
        "on_accent": (30, 12, 16),
        "line": (78, 40, 48),
    },
}

INK = E.INK
MUTED = E.MUTED


def _palette(name):
    return PALETTES.get(name, PALETTES["gold"])


# ---------- Fundo do story ----------
def make_bg(pal, with_grid=True):
    base = Image.new("RGB", (W, H), pal["bg_bottom"])
    top = Image.new("RGB", (W, H), pal["bg_top"])
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    for y in range(H):
        md.line([(0, y), (W, y)], fill=int(255 * (1 - y / H)))
    base = Image.composite(top, base, mask)
    # glow do acento no topo
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W * 0.05, -H * 0.22, W * 0.95, H * 0.28], fill=pal["glow"])
    glow = glow.filter(ImageFilter.GaussianBlur(200))
    base = ImageChops.screen(base, glow)
    if with_grid:
        grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gr = ImageDraw.Draw(grid)
        step = 96
        for x in range(0, W, step):
            gr.line([(x, 0), (x, H)], fill=(255, 255, 255, 6))
        for y in range(0, H, step):
            gr.line([(0, y), (W, y)], fill=(255, 255, 255, 6))
        base = Image.alpha_composite(base.convert("RGBA"), grid).convert("RGB")
    return base


# ---------- helpers de texto ----------
def _tsize(d, t, f):
    return E.tsize(d, t, f)


def _wrap(d, t, f, maxw):
    return E.wrap(d, t, f, maxw)


def _fit(d, text, path, start, minsize, maxw, maxlines):
    return E.fit_font(d, text, path, start, minsize, maxw, maxlines)


def _centered_block(d, lines, f, y, fill, line_gap=0, shadow=False):
    lh = _tsize(d, "Ag", f)[1] + line_gap
    for ln in lines:
        lw, _ = _tsize(d, ln, f)
        x = (W - lw) // 2
        if shadow:
            d.text((x + 3, y + 3), ln, font=f, fill=(0, 0, 0))
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


# ---------- componentes ----------
def _logo_top(canvas, pal):
    E.paste_logo(canvas, 130, ((W - 130) // 2, SAFE_TOP - 130))


def _badge(d, text, y, pal, kind="alerta"):
    text = text.upper()
    bf = E.font(E.F_HEAD2, 30)
    tw, th = _tsize(d, text, bf)
    pad_x, pad_y = 48, 24
    pw, ph = tw + pad_x * 2, th + pad_y * 2
    px = (W - pw) // 2
    if kind == "alerta":
        d.rounded_rectangle([px, y, px + pw, y + ph], ph // 2, fill=pal["accent"])
        d.text((px + pad_x, y + pad_y - 4), text, font=bf, fill=pal["on_accent"])
    else:
        d.rounded_rectangle([px, y, px + pw, y + ph], ph // 2,
                            outline=pal["accent"], width=3)
        d.text((px + pad_x, y + pad_y - 4), text, font=bf, fill=pal["accent_text"])
    return y + ph


def _cta_pill(d, y, pal, text=None):
    """Pill de CTA (LINK NA BIO), ancorada perto da base (mas dentro da area segura)."""
    text = (text or "LINK NA BIO").upper()
    cf = E.font(E.F_HEAD2, 38)
    cw, ch = _tsize(d, text, cf)
    pw, ph = cw + 96, ch + 52
    px = (W - pw) // 2
    d.rounded_rectangle([px, y, px + pw, y + ph], ph // 2, fill=pal["accent"])
    d.text((px + 48, y + 22), text, font=cf, fill=pal["on_accent"])
    # numero do whatsapp discreto abaixo
    wf = E.font(E.F_BODYS, 30)
    wt = E.WHATSAPP
    ww, _ = _tsize(d, wt, wf)
    d.text(((W - ww) // 2, y + ph + 22), wt, font=wf, fill=INK)
    return y + ph


def _footer(d, pal):
    """Rodape discreto: handle + marca, dentro da area segura de baixo."""
    handle = E.HANDLE
    marca = E.NOME_MARCA
    fy = SAFE_BOTTOM + 60
    hf = E.font(E.F_BODYS, 30)
    mf = E.font(E.F_MONO, 24)
    hw, _ = _tsize(d, handle, hf)
    d.text(((W - hw) // 2, fy), handle, font=hf, fill=INK)
    mw, _ = _tsize(d, marca, mf)
    d.text(((W - mw) // 2, fy + 42), marca, font=mf, fill=pal["accent_text"])


# ---------- renderers por tipo ----------
def render_alerta(slide, pal):
    c = make_bg(pal)
    d = ImageDraw.Draw(c)
    _logo_top(c, pal)

    y = SAFE_TOP + 90
    y = _badge(d, slide["badge"], y, pal, kind="alerta")
    y += 90

    hf, hl = _fit(d, slide["headline"], E.F_HEAD, 132, 72, SAFE_W, 6)
    y = _centered_block(d, hl, hf, y, INK, line_gap=26, shadow=True)

    if slide.get("sub"):
        y += 44
        sf = E.font(E.F_BODYS, 44)
        sl = _wrap(d, slide["sub"], sf, SAFE_W - 20)
        _centered_block(d, sl, sf, y, pal["accent_text"], line_gap=18)

    cta_y = SAFE_BOTTOM - 200
    _cta_pill(d, cta_y, pal, slide.get("cta_pill"))
    _footer(d, pal)
    return c


def render_leve(slide, pal):
    c = make_bg(pal)
    d = ImageDraw.Draw(c)
    _logo_top(c, pal)

    y = SAFE_TOP + 80
    y = _badge(d, slide["badge"], y, pal, kind="leve")
    y += 80

    hf, hl = _fit(d, slide["headline"], E.F_HEAD, 104, 60, SAFE_W, 6)
    y = _centered_block(d, hl, hf, y, INK, line_gap=22)

    y += 48
    bf = E.font(E.F_BODY, 42)
    for para in slide.get("body", []):
        pl = _wrap(d, para, bf, SAFE_W - 10)
        y = _centered_block(d, pl, bf, y, MUTED, line_gap=16)
        y += 30

    cta_y = SAFE_BOTTOM - 200
    _cta_pill(d, cta_y, pal, slide.get("cta_pill"))
    _footer(d, pal)
    return c


def render_hero(slide, pal):
    c = make_bg(pal)
    d = ImageDraw.Draw(c)

    # blob do acento no canto
    blob = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(blob)
    ar, ag, ab = pal["accent"]
    bd.ellipse([W * 0.45, H * 0.18, W * 1.2, H * 0.62],
               fill=(ar, ag, ab, 55))
    blob = blob.filter(ImageFilter.GaussianBlur(90))
    c = Image.alpha_composite(c.convert("RGBA"), blob).convert("RGB")
    d = ImageDraw.Draw(c)

    # watermark fantasma
    ghost = slide.get("ghost", slide["hero"].split()[0]).upper()
    gf = E.font(E.F_HEAD, 300)
    d.text((-40, 360), ghost, font=gf, fill=(
        min(pal["bg_top"][0] + 18, 255),
        min(pal["bg_top"][1] + 16, 255),
        min(pal["bg_top"][2] + 12, 255),
    ))

    _logo_top(c, pal)

    y = SAFE_TOP + 150
    if slide.get("eyebrow"):
        ef = E.font(E.F_SEMI, 50)
        el = _wrap(d, slide["eyebrow"], ef, SAFE_W)
        y = _centered_block(d, el, ef, y, MUTED, line_gap=14)
        y += 24

    hf, hl = _fit(d, slide["hero"], E.F_HEAD, 180, 96, SAFE_W, 3)
    y = _centered_block(d, hl, hf, y, pal["accent"], line_gap=10)

    if slide.get("sub"):
        y += 50
        sf = E.font(E.F_BODY, 42)
        sl = _wrap(d, slide["sub"], sf, SAFE_W - 40)
        _centered_block(d, sl, sf, y, INK, line_gap=14)

    cta_y = SAFE_BOTTOM - 200
    _cta_pill(d, cta_y, pal, slide.get("cta_pill"))
    _footer(d, pal)
    return c


def render_cta(slide, pal):
    """Story dedicado ao CTA: fundo do acento + box escuro central."""
    c = Image.new("RGB", (W, H), pal["accent"])
    d = ImageDraw.Draw(c)
    # textura sutil
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gr = ImageDraw.Draw(grid)
    for x in range(0, W, 96):
        gr.line([(x, 0), (x, H)], fill=(0, 0, 0, 12))
    for y in range(0, H, 96):
        gr.line([(0, y), (W, y)], fill=(0, 0, 0, 12))
    c = Image.alpha_composite(c.convert("RGBA"), grid).convert("RGB")
    d = ImageDraw.Draw(c)

    # logo topo
    E.paste_logo(c, 130, ((W - 130) // 2, SAFE_TOP - 60))

    # box escuro central
    bx0, by0 = MARGIN, 560
    bx1, by1 = W - MARGIN, 1420
    d.rounded_rectangle([bx0, by0, bx1, by1], 36, fill=(16, 15, 12))

    y = by0 + 80
    hf, hl = _fit(d, slide["headline"], E.F_HEAD, 92, 56, SAFE_W - 120, 5)
    y = _centered_block(d, hl, hf, y, pal["accent_text"], line_gap=16)

    if slide.get("body"):
        y += 34
        bf = E.font(E.F_BODYS, 40)
        for para in slide["body"]:
            pl = _wrap(d, para, bf, SAFE_W - 140)
            y = _centered_block(d, pl, bf, y, INK, line_gap=14)
            y += 20

    # pill dentro do box
    cta = (slide.get("cta_pill", "LINK NA BIO")).upper()
    cf = E.font(E.F_HEAD2, 40)
    cw, ch = _tsize(d, cta, cf)
    pw, ph = cw + 96, ch + 52
    px = (W - pw) // 2
    py = by1 - ph - 70
    d.rounded_rectangle([px, py, px + pw, py + ph], ph // 2, fill=pal["accent"])
    d.text((px + 48, py + 22), cta, font=cf, fill=pal["on_accent"])
    wf = E.font(E.F_BODYS, 32)
    wt = E.WHATSAPP
    ww, _ = _tsize(d, wt, wf)
    d.text(((W - ww) // 2, py - 52), wt, font=wf, fill=INK)

    # rodape sobre o acento
    hf2 = E.font(E.F_BODYB, 30)
    handle = E.HANDLE
    hw, _ = _tsize(d, handle, hf2)
    d.text(((W - hw) // 2, SAFE_BOTTOM + 60), handle, font=hf2, fill=pal["on_accent"])
    mf = E.font(E.F_BODYS, 28)
    marca = f"{E.NOME_MARCA}  -  {E.CIDADE}"
    mw, _ = _tsize(d, marca, mf)
    d.text(((W - mw) // 2, SAFE_BOTTOM + 102), marca, font=mf,
           fill=(pal["on_accent"][0], pal["on_accent"][1], pal["on_accent"][2]))
    return c


RENDERERS = {
    "alerta": render_alerta,
    "leve": render_leve,
    "hero": render_hero,
    "cta": render_cta,
}


def render_story(slide, out_path):
    """slide = {tipo, palette, ...}. Renderiza e salva 1080x1920 PNG."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pal = _palette(slide.get("palette", "gold"))
    img = RENDERERS[slide["tipo"]](slide, pal)
    img.save(out_path, "PNG", optimize=True)
    return str(out_path)


if __name__ == "__main__":
    # smoke test: 1 de cada tipo/paleta
    import tempfile
    t = Path(tempfile.mkdtemp())
    render_story({"tipo": "alerta", "palette": "gold", "badge": "Ultima vaga",
                  "headline": "A turma esta fechando esta semana",
                  "sub": "Nao fique de fora da proxima turma."}, t / "alerta.png")
    render_story({"tipo": "leve", "palette": "teal", "badge": "Voce sabia",
                  "headline": "Excel abre portas no mercado",
                  "body": ["E a habilidade que quase toda vaga de escritorio pede."]},
                 t / "leve.png")
    render_story({"tipo": "hero", "palette": "wine", "eyebrow": "Comece agora",
                  "hero": "Sua vaga te espera", "sub": "Qualificacao com certificado."},
                 t / "hero.png")
    render_story({"tipo": "cta", "palette": "gold",
                  "headline": "Bora comecar?",
                  "body": ["Fala com a gente e garanta sua matricula."]}, t / "cta.png")
    print("OK ->", t)
