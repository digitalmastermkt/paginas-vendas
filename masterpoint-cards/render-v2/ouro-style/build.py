# -*- coding: utf-8 -*-
"""Gera 3 cards AMOSTRA no estilo do marketing Ouro Moderno, adaptado
a identidade Master Point (preto + dourado #e0b34a). Feed 1080x1350.

Estilo Ouro Moderno destilado das refs do portal /marketing:
- fundo de cor solida forte + textura de linhas sutil
- pill/badge "MATERIAL DE MARKETING"
- headline em dois pesos (eyebrow leve + palavra gigante bold)
- palavra-fantasma gigante no fundo (watermark)
- elemento heroi a direita (aqui: bloco/mockup + shape organico)
- chip toast de notificacao
Render via chromium headless (screenshot 1080x1350).
"""
import base64, pathlib

BASE = pathlib.Path(__file__).resolve().parent
FONTS = pathlib.Path("/opt/NAIA-MASTER/assets/fonts")

def b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

logo_b64 = b64("/opt/NAIA-MASTER/workspace/insta-masterpoint-linkbio/assets/logo.png")
jak_xb = b64(FONTS/"plus_jakarta"/"PlusJakartaSans-ExtraBold.ttf")
jak_b  = b64(FONTS/"plus_jakarta"/"PlusJakartaSans-Bold.ttf")
jak_m  = b64(FONTS/"plus_jakarta"/"PlusJakartaSans-Medium.ttf")
inter_sb = b64(FONTS/"inter"/"Inter-SemiBold.ttf")
inter_m  = b64(FONTS/"inter"/"Inter-Medium.ttf")

FONT_CSS = f"""
@font-face{{font-family:'Jak';src:url(data:font/ttf;base64,{jak_xb}) format('truetype');font-weight:800}}
@font-face{{font-family:'Jak';src:url(data:font/ttf;base64,{jak_b}) format('truetype');font-weight:700}}
@font-face{{font-family:'Jak';src:url(data:font/ttf;base64,{jak_m}) format('truetype');font-weight:500}}
@font-face{{font-family:'Int';src:url(data:font/ttf;base64,{inter_sb}) format('truetype');font-weight:600}}
@font-face{{font-family:'Int';src:url(data:font/ttf;base64,{inter_m}) format('truetype');font-weight:500}}
"""

# paleta Master Point
GOLD="#e0b34a"; GOLD_SOFT="#e6bd56"; INK="#f2efe6"; MUTED="#b3ada0"
BG1="#12110e"; BG2="#0a0a09"; PRETO="#141210"

BASE_CSS = FONT_CSS + f"""
*{{margin:0;padding:0;box-sizing:border-box}}
.card{{width:1080px;height:1350px;position:relative;overflow:hidden;
  font-family:'Int',sans-serif;color:{INK}}}
/* textura de linhas topografica sutil (estilo ouro moderno) */
.lines{{position:absolute;inset:0;opacity:.05;
  background-image:repeating-linear-gradient(0deg,#fff 0 1px,transparent 1px 92px),
                   repeating-linear-gradient(90deg,#fff 0 1px,transparent 1px 92px)}}
.glow{{position:absolute;left:50%;top:-18%;width:820px;height:520px;transform:translateX(-50%);
  background:radial-gradient(ellipse at center,rgba(224,179,74,.28),transparent 70%);filter:blur(30px)}}
.ghost{{position:absolute;font-family:'Jak';font-weight:800;color:rgba(224,179,74,.05);
  font-size:300px;line-height:.82;letter-spacing:-8px;text-transform:uppercase;white-space:nowrap}}
.pill{{display:inline-flex;align-items:center;gap:14px;border:2px solid {GOLD};
  border-radius:999px;padding:14px 30px;font-family:'Int';font-weight:600;font-size:24px;
  letter-spacing:4px;color:{GOLD_SOFT};text-transform:uppercase}}
.pill .dot{{width:12px;height:12px;border-radius:50%;background:{GOLD}}}
.eyebrow{{font-family:'Jak';font-weight:500;font-size:46px;color:{MUTED};line-height:1.05}}
.eyebrow b{{color:{INK};font-weight:800}}
.big{{font-family:'Jak';font-weight:800;font-size:170px;line-height:.9;letter-spacing:-4px;
  text-transform:lowercase}}
.big .g{{color:{GOLD}}}
.blob{{position:absolute;border-radius:44% 56% 60% 40%/48% 40% 60% 52%;
  background:linear-gradient(140deg,{GOLD},#a8802e)}}
.toast{{display:flex;align-items:center;gap:18px;background:rgba(224,179,74,.14);
  border:1px solid rgba(224,179,74,.4);border-radius:20px;padding:20px 26px;
  backdrop-filter:blur(4px);max-width:640px}}
.toast .bell{{width:44px;height:44px;border-radius:12px;background:{GOLD};
  display:flex;align-items:center;justify-content:center;font-size:24px;flex-shrink:0}}
.toast p{{font-family:'Int';font-weight:500;font-size:26px;color:{INK};line-height:1.25}}
.foot{{position:absolute;left:80px;right:80px;bottom:70px;display:flex;
  align-items:center;justify-content:space-between;
  border-top:2px solid rgba(255,255,255,.1);padding-top:26px}}
.foot .h{{font-family:'Int';font-weight:600;font-size:26px;color:{INK}}}
.foot .wa{{font-family:'Int';font-weight:500;font-size:24px;color:{MUTED}}}
.logo{{width:120px;height:120px}}
"""

LOGO_IMG = f'<img class="logo" src="data:image/png;base64,{logo_b64}">'
FOOT = f'''<div class="foot"><div><div class="h">@masterpointcursos</div></div>
  <div class="wa">WhatsApp&nbsp;&nbsp;(86)&nbsp;99804-6242</div></div>'''

# ---------- CARD 1: "novo curso" (estilo do banner azul, adaptado) ----------
card1 = f'''
<div class="card" style="background:linear-gradient(160deg,{BG1},{BG2})">
  <div class="lines"></div><div class="glow"></div>
  <div class="ghost" style="left:-30px;top:120px">NOVO</div>
  <div class="ghost" style="left:-30px;top:400px">CURSO</div>
  <!-- shape organico + mockup a direita -->
  <div class="blob" style="width:560px;height:640px;right:-150px;top:300px;opacity:.9"></div>
  <div style="position:absolute;right:70px;top:360px;width:360px;height:520px;
    background:{PRETO};border:8px solid rgba(255,255,255,.9);border-radius:44px;
    box-shadow:0 30px 80px rgba(0,0,0,.5);display:flex;flex-direction:column;
    align-items:center;justify-content:center;gap:24px;padding:40px">
    {LOGO_IMG.replace('width:120px;height:120px','width:150px;height:150px')}
    <div style="font-family:'Jak';font-weight:800;font-size:40px;color:{GOLD};text-align:center;line-height:1.1">Excel<br>Avançado</div>
  </div>
  <div style="position:absolute;left:80px;top:150px">
    <div class="pill"><span class="dot"></span>MATERIAL DE MARKETING</div>
  </div>
  <div style="position:absolute;left:80px;top:520px">
    <div class="eyebrow">Materiais de <b>divulgação</b></div>
    <div class="big" style="margin-top:20px">novo<br><span class="g">curso</span></div>
  </div>
  <div style="position:absolute;left:80px;top:1010px">
    <div class="toast"><div class="bell">🔔</div>
      <p>Materiais completos e editáveis pra sua escola divulgar e vender mais.</p></div>
  </div>
  {FOOT}
</div>'''

# ---------- CARD 2: badge/escudo bold (estilo "SOFT SKILLS" / "COPA DO FUTURO") ----------
card2 = f'''
<div class="card" style="background:{GOLD}">
  <div class="lines" style="opacity:.08;filter:invert(1)"></div>
  <!-- faixa inferior escura com label -->
  <div style="position:absolute;left:0;right:0;bottom:0;height:300px;background:{PRETO}"></div>
  <div style="position:absolute;left:0;right:0;bottom:150px;text-align:center;
    font-family:'Int';font-weight:600;font-size:30px;letter-spacing:5px;color:{GOLD_SOFT};
    text-transform:uppercase">Material de Marketing</div>
  <!-- escudo central -->
  <div style="position:absolute;left:50%;top:270px;transform:translateX(-50%);
    width:560px;height:640px;background:{PRETO};
    clip-path:polygon(50% 0,100% 12%,100% 70%,50% 100%,0 70%,0 12%);
    display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;
    border:0;box-shadow:0 24px 60px rgba(0,0,0,.35)">
    <div style="width:150px;height:150px;border-radius:50%;background:{GOLD};
      display:flex;align-items:center;justify-content:center;margin-bottom:10px">
      {LOGO_IMG.replace('width:120px;height:120px','width:120px;height:120px;filter:brightness(0)')}
    </div>
    <div style="font-family:'Jak';font-weight:800;font-size:120px;line-height:.85;color:{GOLD};
      text-align:center;text-transform:uppercase;letter-spacing:-2px">SOFT<br>SKILLS</div>
    <div style="font-family:'Int';font-weight:600;font-size:28px;letter-spacing:8px;color:{INK};
      text-transform:uppercase;margin-top:8px">Profissionais</div>
  </div>
  <!-- eyebrow topo -->
  <div style="position:absolute;left:0;right:0;top:130px;text-align:center">
    <div style="font-family:'Jak';font-weight:500;font-size:40px;color:{PRETO}">Trilhas do</div>
    <div style="font-family:'Jak';font-weight:800;font-size:56px;color:{PRETO}">conhecimento</div>
  </div>
</div>'''

# ---------- CARD 3: mascote/tema + pill (estilo "marketing com automação") ----------
card3 = f'''
<div class="card" style="background:linear-gradient(160deg,{BG1},{BG2})">
  <div class="lines"></div><div class="glow"></div>
  <!-- shape organico a direita 2 tons -->
  <div style="position:absolute;right:-60px;top:220px;width:520px;height:620px;
    border-radius:0 0 0 260px;background:{GOLD};opacity:.16"></div>
  <div style="position:absolute;right:-60px;top:520px;width:520px;height:320px;
    border-radius:260px 0 0 0;background:{GOLD};opacity:.28"></div>
  <!-- 'tema' central grande a direita: cap dourado -->
  <div style="position:absolute;right:80px;top:300px;width:330px;height:330px;
    border-radius:50%;background:radial-gradient(circle at 40% 35%,#1c1a15,#0a0a09);
    border:3px solid rgba(224,179,74,.5);display:flex;align-items:center;justify-content:center">
    {LOGO_IMG.replace('width:120px;height:120px','width:210px;height:210px')}
  </div>
  <div style="position:absolute;left:80px;top:170px">
    <div class="eyebrow">Trilha do<br><b>conhecimento</b></div>
  </div>
  <div style="position:absolute;left:80px;top:700px">
    <div class="big" style="font-size:132px">marketing<br><span class="g" style="font-size:84px">com automação</span></div>
  </div>
  <div style="position:absolute;left:80px;top:940px">
    <div class="pill">Material de Marketing</div>
  </div>
  <div style="position:absolute;left:80px;top:1080px">
    <div class="toast"><div class="bell">⚡</div>
      <p>Aprenda a usar IA e automação pra divulgar e escalar sua escola.</p></div>
  </div>
  {FOOT}
</div>'''

CARDS = {"amostra_01_novo_curso": card1,
         "amostra_02_badge_soft_skills": card2,
         "amostra_03_mascote_automacao": card3}

for name, body in CARDS.items():
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE_CSS}</style></head><body>{body}</body></html>"
    (BASE/f"{name}.html").write_text(html, encoding="utf-8")
    print("wrote", name)
print("done")
