# -*- coding: utf-8 -*-
"""
Engine de carrossel Master Point Cursos (Feed 1080x1350 / 4:5).
Identidade: fundo escuro grafite + acento dourado #e0b34a + logo MP.
Reaproveita o design system (safe area 80px, fontes Plus Jakarta/Inter/JetBrains).
Pillow puro, custo R$0.
"""
import os, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ---------- Identidade Master Point ----------
NOME_MARCA   = "MASTER POINT CURSOS"
HANDLE       = "@masterpointcursos"
WHATSAPP     = "(86) 99804-6242"
CIDADE       = "Castelo do Piaui - PI"

# Paleta (do linkbio da marca)
BG_TOP       = (18, 17, 14)      # grafite quente topo
BG_BOTTOM    = (10, 10, 9)       # quase preto base
CARD         = (26, 24, 20)
GOLD         = (224, 179, 74)    # #e0b34a acento solido
GOLD_TEXT    = (230, 189, 86)    # #e6bd56 dourado p/ texto (WCAG AA no escuro)
GOLD_DEEP    = (168, 128, 46)
INK          = (242, 239, 230)   # #f2efe6 texto claro
MUTED        = (179, 173, 160)   # #b3ada0
PRETO_QUENTE = (20, 18, 16)      # texto sobre dourado
LINE         = (60, 55, 44)

# ---------- Canvas ----------
W, H = 1080, 1350
MARGIN = 80
SAFE_W = W - 2*MARGIN
SAFE_H = H - 2*MARGIN
SAFE_TOP = 100
SAFE_BOTTOM_EDGE = H - 80

# ---------- Fontes ----------
FBASE = Path("/opt/NAIA-MASTER/assets/fonts")
F_HEAD  = str(FBASE/"plus_jakarta"/"PlusJakartaSans-ExtraBold.ttf")
F_HEAD2 = str(FBASE/"plus_jakarta"/"PlusJakartaSans-Bold.ttf")
F_SEMI  = str(FBASE/"plus_jakarta"/"PlusJakartaSans-SemiBold.ttf")
F_BODYB = str(FBASE/"inter"/"Inter-Bold.ttf")
F_BODYS = str(FBASE/"inter"/"Inter-SemiBold.ttf")
F_BODY  = str(FBASE/"inter"/"Inter-Medium.ttf")
F_MONO  = str(FBASE/"jetbrains_mono"/"JetBrainsMono-Variable.ttf")

LOGO_PATH = "/opt/NAIA-MASTER/workspace/insta-masterpoint-linkbio/assets/logo.png"

_fcache = {}
def font(path, size):
    k=(path,size)
    if k not in _fcache: _fcache[k]=ImageFont.truetype(path, size)
    return _fcache[k]

def tsize(draw, text, fnt):
    b=draw.textbbox((0,0), text, font=fnt); return b[2]-b[0], b[3]-b[1]

def wrap(draw, text, fnt, maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if tsize(draw,t,fnt)[0] <= maxw: cur=t
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

from PIL import ImageChops

def make_bg(with_grid=True):
    base=Image.new("RGB",(W,H),BG_BOTTOM)
    top=Image.new("RGB",(W,H),BG_TOP)
    mask=Image.new("L",(W,H),0); md=ImageDraw.Draw(mask)
    for y in range(H):
        md.line([(0,y),(W,y)], fill=int(255*(1-y/H)))
    base=Image.composite(top,base,mask)
    # glow dourado topo
    glow=Image.new("RGB",(W,H),(0,0,0)); gd=ImageDraw.Draw(glow)
    gd.ellipse([W*0.10,-H*0.30,W*0.90,H*0.30], fill=(70,52,20))
    glow=glow.filter(ImageFilter.GaussianBlur(180))
    base=ImageChops.screen(base,glow)
    if with_grid:
        grid=Image.new("RGBA",(W,H),(0,0,0,0)); gr=ImageDraw.Draw(grid)
        step=90
        for x in range(0,W,step): gr.line([(x,0),(x,H)], fill=(255,255,255,6))
        for y in range(0,H,step): gr.line([(0,y),(W,y)], fill=(255,255,255,6))
        base=Image.alpha_composite(base.convert("RGBA"),grid).convert("RGB")
    return base

_logo=None
def logo_img():
    global _logo
    if _logo is None: _logo=Image.open(LOGO_PATH).convert("RGBA")
    return _logo

def paste_logo(canvas, size, xy):
    lg=logo_img().resize((size,size), Image.LANCZOS)
    canvas.paste(lg,xy,lg)

# ---------- Logos de software por curso (Yan 2026-08-12) ----------
LOGO_DIR = Path(__file__).resolve().parent/"assets"/"logos"/"png"

# Mapa palavra-chave -> arquivo de logo. Ordem importa: primeiro match (leftmost
# no texto) vence, pra so 1 logo por item de lista e evitar poluicao visual.
# Chaves em minusculo, casadas por substring no item ja em minusculo.
SW_LOGO_KEYS = [
    ("photoshop",  "photoshop.png"),
    ("illustrator","illustrator.png"),
    ("coreldraw",  "coreldraw.png"),
    ("indesign",   "indesign.png"),
    ("canva",      "canva.png"),
    ("power bi",   "powerbi.png"),
    ("powerbi",    "powerbi.png"),
    ("powerpoint", "powerpoint.png"),
    ("excel",      "excel.png"),
    ("word",       "word.png"),      # cuidado: 'wordpress' tratado antes
    ("windows",    "windows.png"),
    ("wordpress",  "wordpress.png"),
    ("google ads", "googleads.png"),
    ("google",     "google.png"),
    ("meta",       "meta.png"),
    ("facebook",   "facebook.png"),
    ("whatsapp",   "whatsapp.png"),
    ("chatgpt",    "openai.png"),
    ("n8n",        "n8n.png"),
]

_logo_cache={}
def _sw_logo(fname, size):
    k=(fname,size)
    if k not in _logo_cache:
        im=Image.open(LOGO_DIR/fname).convert("RGBA")
        b=im.getbbox()
        if b: im=im.crop(b)  # tira padding transparente pra logo encher a caixa
        # encaixa mantendo proporcao num quadrado size x size
        w,h=im.size; scale=size/max(w,h)
        im=im.resize((max(1,int(w*scale)),max(1,int(h*scale))), Image.LANCZOS)
        _logo_cache[k]=im
    return _logo_cache[k]

def logo_for_item(item):
    """Retorna nome de arquivo do logo pro item, ou None se nenhum reconhecido.
    Casa pelo software mencionado mais a esquerda no texto."""
    low=item.lower()
    best=None; best_pos=10**9
    for key,fname in SW_LOGO_KEYS:
        pos=low.find(key)
        if pos==-1: continue
        # 'word' nao deve casar dentro de 'wordpress'
        if key=="word" and "wordpress" in low and low.find("wordpress")<=pos<=low.find("wordpress")+9:
            # 'word' encontrado dentro de wordpress; ignora esse match
            alt=low.replace("wordpress","         ").find("word")
            if alt==-1: continue
            pos=alt
        if pos<best_pos:
            best_pos=pos; best=fname
    return best

def paste_item_logo(canvas, fname, x, y_center, size):
    """Cola o logo do software centralizado verticalmente em y_center, no x dado."""
    lg=_sw_logo(fname, size)
    w,h=lg.size
    px=x+(size-w)//2
    py=int(y_center-h/2)
    canvas.paste(lg,(px,py),lg)

def draw_kicker(draw, text, y=SAFE_TOP-20, color=GOLD_TEXT):
    # REMOVIDO (Yan 2026-08-12): kicker "// CATALOGO 2026" no topo-esquerdo.
    return y+50

def draw_indicator(draw, idx, total, y=SAFE_TOP-20):
    # REMOVIDO (Yan 2026-08-12): numeracao "01 / 05" no topo-direito.
    return

def draw_footer(canvas, draw, cta=None):
    # divisor + handle + marca + whatsapp
    label_y = SAFE_BOTTOM_EDGE-24
    handle_y = label_y-34
    div_y = handle_y-26
    draw.line([(MARGIN,div_y),(W-MARGIN,div_y)], fill=LINE, width=2)
    fnt_h=font(F_BODYS,23); fnt_l=font(F_MONO,20)
    draw.text((MARGIN,handle_y), HANDLE, font=fnt_h, fill=INK)
    draw.text((MARGIN,label_y), NOME_MARCA, font=fnt_l, fill=GOLD_TEXT)
    # whatsapp a direita
    fnt_wa=font(F_BODYS,22); wtxt=f"WhatsApp  {WHATSAPP}"
    tw,_=tsize(draw,wtxt,fnt_wa)
    draw.text((W-MARGIN-tw,handle_y), wtxt, font=fnt_wa, fill=MUTED)
    # REMOVIDO (Yan 2026-08-12): logo pequeno no canto inf direito que tampava o numero do WhatsApp.
    if cta:
        fnt_c=font(F_HEAD2,26)
        cw,_=tsize(draw,cta,fnt_c)
        cy=div_y-56
        draw.text((W-MARGIN-cw-40,cy), cta, font=fnt_c, fill=GOLD)
        # seta
        ax=W-MARGIN-30
        draw.line([(ax-6,cy+16),(ax+8,cy+16)], fill=GOLD, width=4)
        draw.line([(ax+2,cy+9),(ax+8,cy+16)], fill=GOLD, width=4)
        draw.line([(ax+2,cy+23),(ax+8,cy+16)], fill=GOLD, width=4)

def fit_font(draw, text, path, start, minsize, maxw, maxlines):
    size=start
    while size>=minsize:
        fnt=font(path,size)
        lines=wrap(draw,text,fnt,maxw)
        if len(lines)<=maxlines and all(tsize(draw,l,fnt)[0]<=maxw for l in lines):
            return fnt,lines
        size-=4
    fnt=font(path,minsize); return fnt, wrap(draw,text,fnt,maxw)

# ---------------- Templates ----------------
def render_capa(slide, idx, total):
    c=make_bg(); d=ImageDraw.Draw(c)
    draw_kicker(d, slide.get("kicker","// CATALOGO"))
    draw_indicator(d,idx,total)
    # logo grande no topo
    paste_logo(c,150,((W-150)//2,190))
    # headline central
    head=slide["headline"]
    fnt,lines=fit_font(d,head,F_HEAD,86,54,SAFE_W,5)
    lh=tsize(d,"Ag",fnt)[1]+22
    total_h=lh*len(lines)
    y=430
    for ln in lines:
        lw,_=tsize(d,ln,fnt)
        x=(W-lw)//2
        d.text((x+3,y+3),ln,font=fnt,fill=(0,0,0))
        d.text((x,y),ln,font=fnt,fill=INK)
        y+=lh
    # sub
    if slide.get("sub"):
        sf=font(F_BODYS,32); sl=wrap(d,slide["sub"],sf,SAFE_W-40)
        y+=20
        for ln in sl:
            lw,_=tsize(d,ln,sf); d.text(((W-lw)//2,y),ln,font=sf,fill=GOLD_TEXT); y+=48
    draw_footer(c,d,cta=slide.get("cta","ARRASTA"))
    return c

def render_lista(slide, idx, total):
    """Card com headline + lista de itens (cursos) em pill dourado."""
    c=make_bg(); d=ImageDraw.Draw(c)
    draw_kicker(d, slide.get("kicker","// PACOTE"))
    draw_indicator(d,idx,total)
    y=SAFE_TOP+70
    if slide.get("eyebrow"):
        ef=font(F_MONO,24); d.text((MARGIN,y),slide["eyebrow"].upper(),font=ef,fill=GOLD_TEXT); y+=46
    hf,hl=fit_font(d,slide["headline"],F_HEAD,60,40,SAFE_W,3)
    lh=tsize(d,"Ag",hf)[1]+14
    for ln in hl:
        d.text((MARGIN,y),ln,font=hf,fill=INK); y+=lh
    y+=14
    if slide.get("sub"):
        sf=font(F_BODY,28); sl=wrap(d,slide["sub"],sf,SAFE_W)
        for ln in sl: d.text((MARGIN,y),ln,font=sf,fill=MUTED); y+=40
        y+=18
    # itens
    itf=font(F_BODYS,32)
    LOGO_SZ=46           # caixa do logo do software
    TXT_X=MARGIN+LOGO_SZ+22   # texto alinhado depois da caixa do logo/bullet
    max_y = SAFE_BOTTOM_EDGE-150
    line_h=42
    for it in slide["itens"]:
        if y>max_y: break
        lg=logo_for_item(it)
        il=wrap(d,it,itf,W-TXT_X-MARGIN)
        block_h=line_h*len(il)
        y_center=y+ (tsize(d,"Ag",itf)[1])/2 + 2   # centro da 1a linha
        if lg:
            paste_item_logo(c, lg, MARGIN, y_center, LOGO_SZ)
        else:
            # bullet quadrado dourado centralizado na caixa do logo
            bx=MARGIN+(LOGO_SZ-14)//2
            d.rectangle([bx,int(y_center-7),bx+14,int(y_center+7)], fill=GOLD)
        for ln in il:
            d.text((TXT_X,y),ln,font=itf,fill=INK); y+=line_h
        y+=8
    draw_footer(c,d,cta=slide.get("cta"))
    return c

def render_texto(slide, idx, total):
    c=make_bg(); d=ImageDraw.Draw(c)
    draw_kicker(d, slide.get("kicker","// MASTER POINT"))
    draw_indicator(d,idx,total)
    y=SAFE_TOP+90
    if slide.get("headline"):
        hf,hl=fit_font(d,slide["headline"],F_HEAD,64,44,SAFE_W,4)
        lh=tsize(d,"Ag",hf)[1]+16
        for ln in hl: d.text((MARGIN,y),ln,font=hf,fill=INK); y+=lh
        y+=30
    bf=font(F_BODY,34)
    for para in slide.get("body",[]):
        pl=wrap(d,para,bf,SAFE_W)
        for ln in pl: d.text((MARGIN,y),ln,font=bf,fill=INK); y+=48
        y+=26
    draw_footer(c,d,cta=slide.get("cta"))
    return c

def render_cta(slide, idx, total):
    """Slide final: fundo dourado + box escuro."""
    c=Image.new("RGB",(W,H),GOLD); d=ImageDraw.Draw(c)
    # textura sutil
    grid=Image.new("RGBA",(W,H),(0,0,0,0)); gr=ImageDraw.Draw(grid)
    for x in range(0,W,90): gr.line([(x,0),(x,H)],fill=(0,0,0,10))
    for y in range(0,H,90): gr.line([(0,y),(W,y)],fill=(0,0,0,10))
    c=Image.alpha_composite(c.convert("RGBA"),grid).convert("RGB"); d=ImageDraw.Draw(c)
    # REMOVIDO (Yan 2026-08-12): numeracao "01 / 05" no topo-direito do slide CTA.
    # logo topo
    paste_logo(c,120,((W-120)//2,150))
    # box preto central
    bx0,by0,bx1,by1=MARGIN,430,W-MARGIN,1080
    d.rounded_rectangle([bx0,by0,bx1,by1],28,fill=(16,15,12))
    y=by0+60
    hf,hl=fit_font(d,slide["headline"],F_HEAD,64,44,SAFE_W-100,4)
    lh=tsize(d,"Ag",hf)[1]+14
    for ln in hl:
        lw,_=tsize(d,ln,hf); d.text(((W-lw)//2,y),ln,font=hf,fill=GOLD_TEXT); y+=lh
    y+=24
    bf=font(F_BODYS,32)
    for para in slide.get("body",[]):
        pl=wrap(d,para,bf,SAFE_W-120)
        for ln in pl:
            lw,_=tsize(d,ln,bf); d.text(((W-lw)//2,y),ln,font=bf,fill=INK); y+=46
        y+=16
    # pill CTA
    cta=slide.get("cta_pill","LINK NA BIO")
    cf=font(F_HEAD2,34); cw,ch=tsize(d,cta,cf)
    pill_w=cw+80; pill_h=ch+42
    px=(W-pill_w)//2; py=by1-pill_h-46
    d.rounded_rectangle([px,py,px+pill_w,py+pill_h],pill_h//2,fill=GOLD)
    d.text((px+40,py+18),cta,font=cf,fill=PRETO_QUENTE)
    # rodape marca sobre dourado
    lf=font(F_MONO,22); wf=font(F_BODYS,24)
    d.text((MARGIN,SAFE_BOTTOM_EDGE-58),HANDLE,font=font(F_BODYB,26),fill=PRETO_QUENTE)
    d.text((MARGIN,SAFE_BOTTOM_EDGE-24),f"{WHATSAPP}  -  {CIDADE}",font=wf,fill=(40,34,20))
    return c

RENDERERS={"capa":render_capa,"lista":render_lista,"texto":render_texto,"cta":render_cta}

def render_slide(slide, idx, total):
    return RENDERERS[slide["tipo"]](slide, idx, total)

def render_carrossel(carrossel, out_dir):
    out_dir=Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    slides=carrossel["slides"]; n=len(slides); paths=[]
    for i,s in enumerate(slides,1):
        img=render_slide(s,i,n)
        p=out_dir/f"slide_{i:02d}.png"
        img.save(p,"PNG",optimize=True)
        paths.append(str(p))
    return paths
