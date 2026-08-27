# -*- coding: utf-8 -*-
"""
render_singles.py — Cards SINGLE 1080x1350 (4:5) no padrao Master Point (preto+dourado).
Reaproveita a engine mp_carousel.py (mesma paleta, fontes, logo, footer, glow, grid).

Dois tipos:
  - ALERTA: chamada forte de atencao (vaga aberta, ultima turma, matriculas abertas...),
            com badge dourado no topo, headline gigante, subtexto e CTA WhatsApp em pill.
  - LEVE:   curiosidade / "voce sabia" / dica rapida, com badge suave, headline media,
            corpo explicativo e CTA WhatsApp discreto.

Design construido (blocos solidos, tipografia real Plus Jakarta/Inter), NUNCA "facao".
Custo R$0 (Pillow puro).
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

# importa a engine irma
ENGINE_DIR = Path("/opt/NAIA-MASTER/workspace/paginas-vendas/masterpoint-cards/render-v2")
sys.path.insert(0, str(ENGINE_DIR))
import mp_carousel as E  # noqa: E402


def _badge(draw, canvas, text, y, kind="alerta"):
    """Pill dourado (alerta) ou contorno dourado (leve) no topo, centralizado."""
    text = text.upper()
    bf = E.font(E.F_HEAD2, 26)
    tw, th = E.tsize(draw, text, bf)
    pad_x, pad_y = 42, 22
    pw, ph = tw + pad_x * 2, th + pad_y * 2
    px = (E.W - pw) // 2
    if kind == "alerta":
        draw.rounded_rectangle([px, y, px + pw, y + ph], ph // 2, fill=E.GOLD)
        draw.text((px + pad_x, y + pad_y - 4), text, font=bf, fill=E.PRETO_QUENTE)
    else:
        draw.rounded_rectangle([px, y, px + pw, y + ph], ph // 2,
                               outline=E.GOLD, width=3)
        draw.text((px + pad_x, y + pad_y - 4), text, font=bf, fill=E.GOLD_TEXT)
    return y + ph


def _cta_pill(draw, canvas, y, text=None):
    text = text or "LINK NA BIO"
    cf = E.font(E.F_HEAD2, 32)
    cw, ch = E.tsize(draw, text, cf)
    pw, ph = cw + 84, ch + 44
    px = (E.W - pw) // 2
    draw.rounded_rectangle([px, y, px + pw, y + ph], ph // 2, fill=E.GOLD)
    draw.text((px + 42, y + 20), text, font=cf, fill=E.PRETO_QUENTE)
    return y + ph


def render_alerta(slide):
    """
    slide = {tipo:'alerta', badge, headline, sub (opcional), cta_pill (opcional)}
    Layout: logo -> badge -> headline gigante -> sub -> CTA pill -> footer.
    """
    c = E.make_bg()
    d = ImageDraw.Draw(c)

    # logo topo
    E.paste_logo(c, 118, ((E.W - 118) // 2, 130))

    y = 300
    y = _badge(d, c, slide["badge"], y, kind="alerta")
    y += 60

    # headline gigante centralizada
    hf, hl = E.fit_font(d, slide["headline"], E.F_HEAD, 96, 56, E.SAFE_W, 5)
    lh = E.tsize(d, "Ag", hf)[1] + 22
    for ln in hl:
        lw, _ = E.tsize(d, ln, hf)
        x = (E.W - lw) // 2
        d.text((x + 3, y + 3), ln, font=hf, fill=(0, 0, 0))
        d.text((x, y), ln, font=hf, fill=E.INK)
        y += lh

    # sub
    if slide.get("sub"):
        y += 26
        sf = E.font(E.F_BODYS, 34)
        for ln in E.wrap(d, slide["sub"], sf, E.SAFE_W - 30):
            lw, _ = E.tsize(d, ln, sf)
            d.text(((E.W - lw) // 2, y), ln, font=sf, fill=E.GOLD_TEXT)
            y += 50

    # CTA pill (ancorada acima do footer)
    cta_y = E.SAFE_BOTTOM_EDGE - 190
    _cta_pill(d, c, cta_y, slide.get("cta_pill"))

    E.draw_footer(c, d, cta=None)
    return c


def render_leve(slide):
    """
    slide = {tipo:'leve', badge, headline, body:[..], cta_pill (opcional)}
    Layout: logo -> badge -> headline media -> corpo -> CTA -> footer.
    """
    c = E.make_bg()
    d = ImageDraw.Draw(c)

    E.paste_logo(c, 110, ((E.W - 110) // 2, 130))

    y = 288
    y = _badge(d, c, slide["badge"], y, kind="leve")
    y += 54

    hf, hl = E.fit_font(d, slide["headline"], E.F_HEAD, 74, 46, E.SAFE_W, 5)
    lh = E.tsize(d, "Ag", hf)[1] + 18
    for ln in hl:
        lw, _ = E.tsize(d, ln, hf)
        d.text(((E.W - lw) // 2, y), ln, font=hf, fill=E.INK)
        y += lh

    y += 34
    bf = E.font(E.F_BODY, 34)
    for para in slide.get("body", []):
        for ln in E.wrap(d, para, bf, E.SAFE_W - 20):
            lw, _ = E.tsize(d, ln, bf)
            d.text(((E.W - lw) // 2, y), ln, font=bf, fill=E.MUTED)
            y += 48
        y += 22

    cta_y = E.SAFE_BOTTOM_EDGE - 180
    _cta_pill(d, c, cta_y, slide.get("cta_pill"))

    E.draw_footer(c, d, cta=None)
    return c


def render_hero(slide):
    """
    Estilo 'Ouro Moderno' em Pillow: watermark fantasma gigante ao fundo,
    eyebrow leve + palavra-heroi dourada gigante, blob dourado, CTA.
    slide = {tipo:'hero', eyebrow, hero (palavra/expr gigante dourada),
             sub (opcional), badge (opcional), cta_pill (opcional)}
    """
    c = E.make_bg()
    d = ImageDraw.Draw(c)

    # blob dourado organico no canto (elipse desfocada)
    blob = Image.new("RGBA", (E.W, E.H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(blob)
    bd.ellipse([E.W * 0.52, E.H * 0.20, E.W * 1.15, E.H * 0.78],
               fill=(224, 179, 74, 60))
    blob = blob.filter(E.ImageFilter.GaussianBlur(70))
    c = Image.alpha_composite(c.convert("RGBA"), blob).convert("RGB")
    d = ImageDraw.Draw(c)

    # watermark fantasma (palavra do hero em maiuscula, bem sutil)
    ghost_word = slide.get("ghost", slide["hero"].split()[0]).upper()
    gf = E.font(E.F_HEAD, 260)
    d.text((-30, 210), ghost_word, font=gf, fill=(30, 26, 18))

    # logo topo
    E.paste_logo(c, 96, (E.MARGIN, 130))

    # badge opcional
    y = 250
    if slide.get("badge"):
        bf = E.font(E.F_MONO, 24)
        bt = slide["badge"].upper()
        tw, th = E.tsize(d, bt, bf)
        d.rounded_rectangle([E.MARGIN, y, E.MARGIN + tw + 60, y + th + 30], (th + 30) // 2,
                            outline=E.GOLD, width=3)
        d.text((E.MARGIN + 30, y + 12), bt, font=bf, fill=E.GOLD_TEXT)
        y += th + 30

    # eyebrow leve
    y = 500
    if slide.get("eyebrow"):
        ef = E.font(E.F_SEMI, 42)
        for ln in E.wrap(d, slide["eyebrow"], ef, E.SAFE_W):
            d.text((E.MARGIN, y), ln, font=ef, fill=E.MUTED)
            y += 56
        y += 8

    # hero gigante dourado (max 2 linhas pra caber sub + CTA)
    hf, hl = E.fit_font(d, slide["hero"], E.F_HEAD, 140, 74, E.SAFE_W, 2)
    lh = E.tsize(d, "Ag", hf)[1] + 8
    for ln in hl:
        d.text((E.MARGIN, y), ln, font=hf, fill=E.GOLD)
        y += lh

    # sub / toast (fica acima da CTA; nao invade a pill)
    cta_top = E.SAFE_BOTTOM_EDGE - 180
    if slide.get("sub"):
        y += 34
        sf = E.font(E.F_BODY, 32)
        sub_lines = E.wrap(d, slide["sub"], sf, E.SAFE_W - 60)
        box_h = 48 * len(sub_lines) + 44
        # se colidir com a CTA, sobe a caixa pra terminar ~40px antes
        if y + box_h > cta_top - 40:
            y = cta_top - 40 - box_h
        d.rounded_rectangle([E.MARGIN, y, E.W - E.MARGIN, y + box_h], 20,
                            fill=(30, 27, 20))
        yy = y + 22
        for ln in sub_lines:
            d.text((E.MARGIN + 26, yy), ln, font=sf, fill=E.INK)
            yy += 48

    _cta_pill(d, c, cta_top, slide.get("cta_pill"))
    E.draw_footer(c, d, cta=None)
    return c


# ============================================================
# NOVOS FORMATOS DE ENGAJAMENTO (Yan, 2026-08-12, ref @lucureau)
# ============================================================
# Cor "antes" (cinza frio, apagado) e "depois" (dourado da marca).
_ANTES_INK = (150, 145, 135)   # cinza morno, "vida apagada"
_DEPOIS_INK = E.GOLD_TEXT


def _split_card(slide, side):
    """
    Card do formato COMPARACAO ANTES x DEPOIS (1 dos 2 slides do carrossel).
    side = 'antes' | 'depois'.
    slide = {tag, titulo, itens:[..], (opcional) rodape_cta}
    ANTES: badge/titulo em cinza apagado, lista com "x". Sem CTA.
    DEPOIS: badge/titulo dourado, lista com check dourado. CTA discreto.
    """
    is_depois = (side == "depois")
    accent = _DEPOIS_INK if is_depois else _ANTES_INK
    mark_color = E.GOLD if is_depois else (110, 104, 94)
    c = E.make_bg()
    d = ImageDraw.Draw(c)

    E.paste_logo(c, 104, ((E.W - 104) // 2, 128))

    # badge topo (ANTES / DEPOIS)
    y = 288
    y = _badge(d, c, slide["tag"], y, kind=("alerta" if is_depois else "leve"))
    y += 52

    # titulo
    hf, hl = E.fit_font(d, slide["titulo"], E.F_HEAD, 78, 48, E.SAFE_W, 4)
    lh = E.tsize(d, "Ag", hf)[1] + 18
    for ln in hl:
        lw, _ = E.tsize(d, ln, hf)
        d.text(((E.W - lw) // 2, y), ln, font=hf, fill=(E.INK if is_depois else _ANTES_INK))
        y += lh
    y += 40

    # itens com marcador (x apagado antes / check dourado depois)
    itf = E.font(E.F_BODYS, 36)
    left = E.MARGIN + 30
    for it in slide["itens"]:
        lines = E.wrap(d, it, itf, E.SAFE_W - 90)
        yc = y + E.tsize(d, "Ag", itf)[1] / 2
        if is_depois:
            # check dourado
            d.line([(left, yc), (left + 12, yc + 12)], fill=mark_color, width=6)
            d.line([(left + 12, yc + 12), (left + 34, yc - 16)], fill=mark_color, width=6)
        else:
            # x cinza
            d.line([(left, yc - 12), (left + 26, yc + 14)], fill=mark_color, width=6)
            d.line([(left + 26, yc - 12), (left, yc + 14)], fill=mark_color, width=6)
        tx = left + 56
        for ln in lines:
            d.text((tx, y), ln, font=itf, fill=(E.INK if is_depois else accent))
            y += 50
        y += 22

    if is_depois and slide.get("rodape_cta"):
        cta_y = E.SAFE_BOTTOM_EDGE - 180
        _cta_pill(d, c, cta_y, slide.get("rodape_cta"))

    E.draw_footer(c, d, cta=None)
    return c


def render_antes(slide):
    return _split_card(slide, "antes")


def render_depois(slide):
    return _split_card(slide, "depois")


def render_binaria(slide):
    """
    Card unico de PERGUNTA BINARIA (engajamento). Divide a arte em dois
    "times" (A e B), com a pergunta binaria em destaque e um CTA de COMENTARIO
    que NAO usa nenhuma palavra que o matcher EU QUERO reconheca.
    slide = {badge, pergunta, opcao_a, opcao_b, cta_comentario}
    """
    c = E.make_bg()
    d = ImageDraw.Draw(c)

    E.paste_logo(c, 104, ((E.W - 104) // 2, 128))

    y = 288
    y = _badge(d, c, slide.get("badge", "Responde aí"), y, kind="leve")
    y += 54

    # pergunta grande
    hf, hl = E.fit_font(d, slide["pergunta"], E.F_HEAD, 78, 46, E.SAFE_W, 4)
    lh = E.tsize(d, "Ag", hf)[1] + 18
    for ln in hl:
        lw, _ = E.tsize(d, ln, hf)
        d.text(((E.W - lw) // 2, y), ln, font=hf, fill=E.INK)
        y += lh
    y += 50

    # duas caixas: opcao A (dourado contornado) e opcao B (dourado solido)
    box_w = E.SAFE_W
    box_h = 150
    gap = 34
    for i, (label, texto, solid) in enumerate([
        ("A", slide["opcao_a"], False),
        ("B", slide["opcao_b"], True),
    ]):
        bx0 = E.MARGIN
        by0 = y
        bx1 = E.MARGIN + box_w
        by1 = y + box_h
        if solid:
            d.rounded_rectangle([bx0, by0, bx1, by1], 26, fill=E.GOLD)
            letter_fill = E.PRETO_QUENTE
            txt_fill = E.PRETO_QUENTE
        else:
            d.rounded_rectangle([bx0, by0, bx1, by1], 26, outline=E.GOLD, width=4)
            letter_fill = E.GOLD
            txt_fill = E.INK
        # letra A/B grande na esquerda
        lf = E.font(E.F_HEAD, 76)
        d.text((bx0 + 44, by0 + 30), label, font=lf, fill=letter_fill)
        # texto da opcao
        of = E.font(E.F_BODYS, 40)
        ol = E.wrap(d, texto, of, box_w - 200)
        oth = 50 * len(ol)
        ty = by0 + (box_h - oth) // 2
        for ln in ol:
            d.text((bx0 + 170, ty), ln, font=of, fill=txt_fill)
            ty += 50
        y = by1 + gap

    # CTA de comentario (SEM "quero"/"interesse" — nao dispara o matcher DM)
    cta_y = E.SAFE_BOTTOM_EDGE - 168
    cf = E.font(E.F_HEAD2, 34)
    ctxt = slide.get("cta_comentario", "Comenta A ou B aqui embaixo")
    cl = E.wrap(d, ctxt, cf, E.SAFE_W - 40)
    for ln in cl:
        lw, _ = E.tsize(d, ln, cf)
        d.text(((E.W - lw) // 2, cta_y), ln, font=cf, fill=E.GOLD_TEXT)
        cta_y += 46

    E.draw_footer(c, d, cta=None)
    return c


RENDERERS = {"alerta": render_alerta, "leve": render_leve, "hero": render_hero,
             "antes": render_antes, "depois": render_depois,
             "binaria": render_binaria}


def render_single(slide, out_path):
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img = RENDERERS[slide["tipo"]](slide)
    img.save(out_path, "PNG", optimize=True)
    return str(out_path)


if __name__ == "__main__":
    # smoke test: 1 alerta + 1 leve
    import tempfile
    t = Path(tempfile.mkdtemp())
    render_single({"tipo": "alerta", "badge": "Vagas abertas",
                   "headline": "Ultima turma do mes esta abrindo",
                   "sub": "Garanta sua vaga antes de fechar."}, t / "a.png")
    render_single({"tipo": "leve", "badge": "Voce sabia",
                   "headline": "Saber Excel abre portas no mercado",
                   "body": ["Planilha e a ferramenta que quase toda vaga de escritorio pede.",
                            "Quem domina, se destaca na hora da contratacao."]},
                  t / "l.png")
    print("OK ->", t)
