#!/usr/bin/env python3
"""build.py - Converte o dossie markdown em site HTML estatico bonito.

Uso:
    python3 build.py

Le:  /opt/NAIA-MASTER/knowledge/sdr/dossie-treinamento-agente-instagram.md
Escreve: /opt/NAIA-MASTER/workspace/dossie-agente-sdr/index.html
         /opt/NAIA-MASTER/workspace/dossie-agente-sdr/style.css
         /opt/NAIA-MASTER/workspace/dossie-agente-sdr/script.js
"""
import os
import re
import html as html_lib
from pathlib import Path

ROOT = Path('/opt/NAIA-MASTER/workspace/dossie-agente-sdr')
SRC = Path('/opt/NAIA-MASTER/knowledge/sdr/dossie-treinamento-agente-instagram.md')


def slugify(text: str) -> str:
    import unicodedata
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')


def render_inline(text: str) -> str:
    """Converte marcacao inline: **bold**, *italic*, `code`, [link](url)."""
    # Escape primeiro
    text = html_lib.escape(text, quote=False)
    # links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
    # bold
    text = re.sub(r'\*\*([^*\n]+)\*\*', r'<strong>\1</strong>', text)
    # italic (tomar cuidado pra nao casar com bold)
    text = re.sub(r'(?<![*])\*([^*\n]+)\*(?![*])', r'<em>\1</em>', text)
    # inline code
    text = re.sub(r'`([^`\n]+)`', r'<code>\1</code>', text)
    return text


def md_to_html(md: str) -> tuple[str, list[dict]]:
    """Converte markdown pra HTML. Retorna (html, lista_de_blocos_para_sidebar)."""
    lines = md.split('\n')
    out = []
    sidebar = []  # lista de {id, label, sub: [...] }
    current_block = None  # ultimo bloco h2 pra colocar h3 dentro

    i = 0
    in_table = False
    in_code = False
    in_blockquote = False
    in_list = False
    list_type = None  # 'ul' ou 'ol'
    table_rows = []
    table_align = []
    code_buf = []
    code_lang = ''

    def close_list():
        nonlocal in_list, list_type
        if in_list:
            out.append(f'</{list_type}>')
            in_list = False
            list_type = None

    def close_blockquote():
        nonlocal in_blockquote
        if in_blockquote:
            out.append('</blockquote>')
            in_blockquote = False

    def close_table():
        nonlocal in_table, table_rows, table_align
        if in_table:
            # primeira linha = header, segunda = align (ja consumida), demais = body
            html_t = ['<div class="table-wrap"><table>']
            if table_rows:
                header = table_rows[0]
                body = table_rows[1:]
                html_t.append('<thead><tr>')
                for j, cell in enumerate(header):
                    align = table_align[j] if j < len(table_align) else ''
                    style = f' style="text-align:{align}"' if align else ''
                    html_t.append(f'<th{style}>{render_inline(cell.strip())}</th>')
                html_t.append('</tr></thead>')
                html_t.append('<tbody>')
                for row in body:
                    html_t.append('<tr>')
                    for j, cell in enumerate(row):
                        align = table_align[j] if j < len(table_align) else ''
                        style = f' style="text-align:{align}"' if align else ''
                        html_t.append(f'<td{style}>{render_inline(cell.strip())}</td>')
                    html_t.append('</tr>')
                html_t.append('</tbody>')
            html_t.append('</table></div>')
            out.append(''.join(html_t))
            table_rows = []
            table_align = []
            in_table = False

    while i < len(lines):
        line = lines[i]

        # Code fence
        if line.startswith('```'):
            if in_code:
                # fecha
                code_html = html_lib.escape('\n'.join(code_buf), quote=False)
                lang_class = f' class="lang-{code_lang}"' if code_lang else ''
                out.append(f'<pre><code{lang_class}>{code_html}</code></pre>')
                code_buf = []
                code_lang = ''
                in_code = False
            else:
                close_list(); close_blockquote(); close_table()
                code_lang = line[3:].strip()
                in_code = True
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        # Tabela: detecta separador "|---|---|"
        if re.match(r'^\s*\|.*\|\s*$', line):
            # checa se a proxima linha eh o separador
            if not in_table:
                if i + 1 < len(lines) and re.match(r'^\s*\|[\s:|-]+\|\s*$', lines[i+1]):
                    close_list(); close_blockquote()
                    in_table = True
                    # parse alinhamento da proxima linha
                    sep = lines[i+1].strip().strip('|').split('|')
                    table_align = []
                    for s in sep:
                        s = s.strip()
                        if s.startswith(':') and s.endswith(':'):
                            table_align.append('center')
                        elif s.endswith(':'):
                            table_align.append('right')
                        elif s.startswith(':'):
                            table_align.append('left')
                        else:
                            table_align.append('')
                    cells = line.strip().strip('|').split('|')
                    table_rows.append(cells)
                    i += 2
                    continue
                else:
                    pass  # nao eh tabela
            else:
                cells = line.strip().strip('|').split('|')
                table_rows.append(cells)
                i += 1
                continue
        else:
            if in_table:
                close_table()

        # Linha vazia
        if line.strip() == '':
            close_list()
            close_blockquote()
            i += 1
            continue

        # Heading h1
        m = re.match(r'^# (.+)$', line)
        if m:
            close_list(); close_blockquote(); close_table()
            text = m.group(1).strip()
            # h1 do dossie nao vai pro corpo (vai pro hero)
            i += 1
            continue

        # Heading h2 - cria bloco/section
        m = re.match(r'^## (.+)$', line)
        if m:
            close_list(); close_blockquote(); close_table()
            text = m.group(1).strip()
            slug = slugify(text)
            # Fecha section anterior se existir
            if current_block is not None:
                out.append('</div></section>')
            out.append(f'<section id="{slug}" class="block"><div class="block-inner">')
            out.append(f'<h2>{render_inline(text)}</h2>')
            current_block = {'id': slug, 'label': text, 'sub': []}
            sidebar.append(current_block)
            i += 1
            continue

        # Heading h3
        m = re.match(r'^### (.+)$', line)
        if m:
            close_list(); close_blockquote(); close_table()
            text = m.group(1).strip()
            slug = slugify(text)
            out.append(f'<h3 id="{slug}">{render_inline(text)}</h3>')
            if current_block is not None:
                current_block['sub'].append({'id': slug, 'label': text})
            i += 1
            continue

        # Heading h4
        m = re.match(r'^#### (.+)$', line)
        if m:
            close_list(); close_blockquote(); close_table()
            text = m.group(1).strip()
            out.append(f'<h4>{render_inline(text)}</h4>')
            i += 1
            continue

        # Horizontal rule
        if re.match(r'^---+$', line.strip()):
            close_list(); close_blockquote(); close_table()
            # nao renderiza HR, sections ja separam
            i += 1
            continue

        # Blockquote
        m = re.match(r'^> ?(.*)$', line)
        if m:
            close_list(); close_table()
            if not in_blockquote:
                out.append('<blockquote>')
                in_blockquote = True
            content = m.group(1)
            if content.strip():
                out.append(f'<p>{render_inline(content)}</p>')
            i += 1
            continue
        else:
            close_blockquote()

        # Lista ordenada
        m = re.match(r'^(\d+)\.\s+(.+)$', line)
        if m:
            close_table()
            if not in_list or list_type != 'ol':
                close_list()
                out.append('<ol>')
                in_list = True
                list_type = 'ol'
            out.append(f'<li>{render_inline(m.group(2))}</li>')
            i += 1
            continue

        # Lista nao ordenada
        m = re.match(r'^[-*]\s+(.+)$', line)
        if m:
            close_table()
            if not in_list or list_type != 'ul':
                close_list()
                out.append('<ul>')
                in_list = True
                list_type = 'ul'
            out.append(f'<li>{render_inline(m.group(1))}</li>')
            i += 1
            continue
        else:
            close_list()

        # Italic-only line (ultima linha "Documento vivo...")
        m = re.match(r'^\*([^*]+)\*$', line.strip())
        if m:
            out.append(f'<p class="footer-note"><em>{render_inline(m.group(1))}</em></p>')
            i += 1
            continue

        # Paragrafo normal
        close_table()
        out.append(f'<p>{render_inline(line)}</p>')
        i += 1

    # Fecha pendencias
    close_list()
    close_blockquote()
    close_table()
    if current_block is not None:
        out.append('</div></section>')

    return '\n'.join(out), sidebar


def build_sidebar_html(sidebar: list[dict]) -> str:
    items = []
    for i, block in enumerate(sidebar, start=1):
        items.append(f'<li class="sidebar-item"><a href="#{block["id"]}" class="sidebar-link"><span class="sidebar-num">{i:02d}</span><span class="sidebar-label">{html_lib.escape(block["label"])}</span></a></li>')
    return '<ol class="sidebar-list">' + ''.join(items) + '</ol>'


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dossie de Treinamento, Agente SDR Instagram | Salatiel Batista</title>
<meta name="description" content="Manual operacional do agente IA que atende as DMs do Salatiel Batista e da Digital Master. Documento interno.">
<meta name="robots" content="noindex, nofollow">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,800;1,400;1,700&family=IBM+Plex+Sans:wght@300;400;500;600;700&family=Crimson+Pro:ital,wght@0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

<link rel="stylesheet" href="style.css">
</head>
<body>

<a href="#bloco-1-identidade-do-mentor" class="skip-link">Pular para o conteudo</a>

<button class="menu-toggle" id="menuToggle" aria-label="Abrir indice">
  <span></span><span></span><span></span>
</button>

<aside class="sidebar" id="sidebar">
  <div class="sidebar-header">
    <div class="sidebar-brand">
      <span class="sb-mark">DM</span>
      <span class="sb-text">Documento Interno</span>
    </div>
    <h2 class="sidebar-title">Indice</h2>
  </div>
  <nav class="sidebar-nav" aria-label="Indice do dossie">
    __SIDEBAR__
  </nav>
  <div class="sidebar-footer">
    <p>13 blocos</p>
    <p>1137 linhas</p>
    <p>Atualizado 06/05/2026</p>
  </div>
</aside>

<div class="overlay" id="overlay"></div>

<main class="main">

  <header class="hero">
    <div class="hero-inner">
      <div class="hero-eyebrow"><span class="dot"></span> Documento interno, Naia Master</div>
      <h1 class="hero-title">Dossie de Treinamento <em>do</em> Agente SDR Instagram</h1>
      <p class="hero-sub">Manual operacional do agente IA que atende as DMs do <strong>@salatielbatistaoficial</strong> e <strong>@digitalmastermkt</strong>. Cerebro do agente: vira system prompt na plataforma de execucao.</p>
      <div class="hero-meta">
        <div class="meta-item"><span class="meta-num">13</span><span class="meta-label">Blocos</span></div>
        <div class="meta-divider"></div>
        <div class="meta-item"><span class="meta-num">10</span><span class="meta-label">Objecoes mapeadas</span></div>
        <div class="meta-divider"></div>
        <div class="meta-item"><span class="meta-num">5</span><span class="meta-label">Perguntas BANT</span></div>
        <div class="meta-divider"></div>
        <div class="meta-item"><span class="meta-num">3</span><span class="meta-label">Cenarios de abordagem</span></div>
      </div>
      <div class="hero-byline">
        <span>Salatiel Batista</span>
        <span class="sep">/</span>
        <span>Digital Master</span>
        <span class="sep">/</span>
        <span>Atualizado 06/05/2026</span>
      </div>
    </div>
  </header>

  <article class="content">
    __CONTENT__
  </article>

  <footer class="site-footer">
    <div class="footer-inner">
      <p class="footer-brand">Salatiel Batista <span>/</span> Digital Master</p>
      <p class="footer-meta">Documento interno gerado por Naia. Nao distribuir externamente.</p>
      <p class="footer-meta">Movimento gera resultado.</p>
    </div>
  </footer>

</main>

<button class="back-top" id="backTop" aria-label="Voltar ao topo">^</button>

<script src="script.js"></script>
</body>
</html>
"""


CSS = r"""
:root {
  --bg: #0a0a0a;
  --bg-soft: #111111;
  --bg-card: #161616;
  --bg-card-hover: #1c1c1c;
  --line: rgba(255, 255, 255, 0.08);
  --line-strong: rgba(255, 255, 255, 0.18);
  --text: #f5f3ee;
  --text-muted: #b8b4ab;
  --text-soft: #8a857c;
  --accent: #3A9E9C;
  --accent-soft: rgba(58, 158, 156, 0.12);
  --accent-strong: #4FB8B6;
  --gold: #c9a96e;
  --gold-soft: rgba(201, 169, 110, 0.12);
  --serif: 'Playfair Display', Georgia, serif;
  --serif-body: 'Crimson Pro', Georgia, serif;
  --sans: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --mono: 'JetBrains Mono', 'Courier New', monospace;
  --sidebar-w: 320px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; scroll-padding-top: 24px; }
html, body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--sans);
  font-size: 17px;
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body { overflow-x: hidden; }

a { color: var(--accent); text-decoration: none; transition: color .2s; }
a:hover { color: var(--accent-strong); text-decoration: underline; text-underline-offset: 3px; }

::selection { background: var(--accent); color: #051817; }

.skip-link {
  position: absolute;
  left: -9999px;
  top: 0;
  background: var(--accent);
  color: #000;
  padding: 8px 16px;
  z-index: 1000;
}
.skip-link:focus { left: 16px; top: 16px; }

/* SIDEBAR */
.sidebar {
  position: fixed;
  top: 0; left: 0; bottom: 0;
  width: var(--sidebar-w);
  background: var(--bg-soft);
  border-right: 1px solid var(--line);
  overflow-y: auto;
  padding: 32px 24px 24px;
  z-index: 40;
  transition: transform .3s ease;
}
.sidebar-header { margin-bottom: 24px; padding-bottom: 20px; border-bottom: 1px solid var(--line); }
.sidebar-brand { display: flex; align-items: center; gap: 12px; margin-bottom: 18px; }
.sb-mark {
  font-family: var(--serif);
  font-weight: 800;
  font-size: 18px;
  color: var(--accent);
  letter-spacing: 1px;
  background: var(--accent-soft);
  padding: 4px 10px;
  border-radius: 3px;
  border: 1px solid var(--accent);
}
.sb-text {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--text-soft);
  font-weight: 500;
}
.sidebar-title {
  font-family: var(--serif);
  font-size: 28px;
  font-weight: 700;
  color: var(--text);
  letter-spacing: -0.01em;
}
.sidebar-list { list-style: none; }
.sidebar-item { margin-bottom: 2px; }
.sidebar-link {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 12px 12px;
  color: var(--text-muted);
  border-radius: 4px;
  transition: all .2s;
  border-left: 2px solid transparent;
}
.sidebar-link:hover {
  background: var(--bg-card);
  color: var(--text);
  text-decoration: none;
  border-left-color: var(--accent);
}
.sidebar-link.active {
  background: var(--accent-soft);
  color: var(--text);
  border-left-color: var(--accent);
}
.sidebar-num {
  font-family: var(--mono);
  font-size: 11px;
  color: var(--text-soft);
  font-weight: 500;
  letter-spacing: 1px;
  min-width: 24px;
  padding-top: 3px;
}
.sidebar-link.active .sidebar-num { color: var(--accent); }
.sidebar-label {
  font-size: 13px;
  line-height: 1.4;
  font-weight: 500;
}
.sidebar-footer {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid var(--line);
  font-family: var(--mono);
  font-size: 11px;
  color: var(--text-soft);
  letter-spacing: 1px;
}
.sidebar-footer p { margin-bottom: 4px; }

/* MENU TOGGLE (mobile) */
.menu-toggle {
  display: none;
  position: fixed;
  top: 16px; right: 16px;
  z-index: 60;
  width: 48px; height: 48px;
  background: var(--bg-card);
  border: 1px solid var(--line-strong);
  border-radius: 4px;
  cursor: pointer;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 5px;
  padding: 0;
}
.menu-toggle span {
  display: block;
  width: 22px; height: 2px;
  background: var(--text);
  transition: all .25s;
}
.menu-toggle.active span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
.menu-toggle.active span:nth-child(2) { opacity: 0; }
.menu-toggle.active span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }

.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  z-index: 35;
  opacity: 0;
  pointer-events: none;
  transition: opacity .3s;
}
.overlay.active { opacity: 1; pointer-events: auto; }

/* MAIN */
.main {
  margin-left: var(--sidebar-w);
  min-height: 100vh;
}

/* HERO */
.hero {
  padding: 80px 64px 64px;
  border-bottom: 1px solid var(--line);
  background:
    radial-gradient(ellipse at 80% 0%, rgba(58, 158, 156, 0.08), transparent 50%),
    linear-gradient(180deg, var(--bg-soft), var(--bg));
}
.hero-inner { max-width: 880px; }
.hero-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 3px;
  color: var(--accent);
  margin-bottom: 28px;
}
.hero-eyebrow .dot {
  width: 8px; height: 8px;
  background: var(--accent);
  border-radius: 50%;
  box-shadow: 0 0 12px var(--accent);
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
.hero-title {
  font-family: var(--serif);
  font-weight: 700;
  font-size: clamp(36px, 5.5vw, 72px);
  line-height: 1.02;
  letter-spacing: -0.02em;
  margin-bottom: 28px;
}
.hero-title em {
  font-style: italic;
  font-weight: 400;
  color: var(--accent);
}
.hero-sub {
  font-family: var(--serif-body);
  font-size: clamp(18px, 1.6vw, 22px);
  line-height: 1.5;
  color: var(--text-muted);
  margin-bottom: 40px;
  max-width: 720px;
}
.hero-sub strong { color: var(--text); font-weight: 600; }
.hero-meta {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
  margin-bottom: 36px;
  padding: 20px 24px;
  background: var(--bg-card);
  border: 1px solid var(--line);
  border-radius: 6px;
}
.meta-item { display: flex; flex-direction: column; }
.meta-num {
  font-family: var(--serif);
  font-size: 32px;
  font-weight: 700;
  color: var(--accent);
  line-height: 1;
}
.meta-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--text-soft);
  font-weight: 500;
  margin-top: 4px;
}
.meta-divider {
  width: 1px;
  height: 36px;
  background: var(--line);
}
.hero-byline {
  font-size: 13px;
  color: var(--text-soft);
  letter-spacing: 0.5px;
}
.hero-byline .sep { color: var(--line-strong); margin: 0 10px; }

/* CONTENT */
.content {
  padding: 0;
}
.block {
  padding: 64px 64px 72px;
  border-bottom: 1px solid var(--line);
  position: relative;
  scroll-margin-top: 24px;
}
.block:nth-child(odd) { background: var(--bg-soft); }
.block-inner {
  max-width: 880px;
  margin: 0 auto;
}
.block::before {
  content: "";
  position: absolute;
  top: 0; left: 0;
  width: 4px; height: 80px;
  background: linear-gradient(180deg, var(--accent), transparent);
}

.content h2 {
  font-family: var(--serif);
  font-weight: 700;
  font-size: clamp(28px, 3.5vw, 44px);
  line-height: 1.1;
  letter-spacing: -0.01em;
  margin-bottom: 36px;
  color: var(--text);
  padding-bottom: 16px;
  border-bottom: 1px solid var(--line);
}
.content h3 {
  font-family: var(--serif);
  font-weight: 600;
  font-size: clamp(20px, 2.2vw, 26px);
  line-height: 1.25;
  letter-spacing: -0.005em;
  margin: 40px 0 18px;
  color: var(--text);
}
.content h4 {
  font-family: var(--sans);
  font-weight: 600;
  font-size: 16px;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--accent);
  margin: 28px 0 14px;
}

.content p {
  margin-bottom: 18px;
  color: var(--text);
  font-size: 17px;
  line-height: 1.7;
}
.content p strong { color: var(--text); font-weight: 600; }
.content p em { color: var(--text-muted); }

.content ul, .content ol {
  margin: 16px 0 24px 24px;
  padding-left: 4px;
}
.content li {
  margin-bottom: 10px;
  line-height: 1.65;
  padding-left: 6px;
}
.content ul li::marker { color: var(--accent); }
.content ol li::marker { color: var(--accent); font-weight: 600; }

/* BLOCKQUOTE: estilizado como bolha do Salatiel ou destaque */
.content blockquote {
  margin: 24px 0;
  padding: 22px 26px;
  background: var(--bg-card);
  border-left: 3px solid var(--accent);
  border-radius: 0 6px 6px 0;
  position: relative;
  box-shadow: 0 6px 20px rgba(0,0,0,0.25);
}
.content blockquote::before {
  content: '"';
  position: absolute;
  top: -8px; left: 14px;
  font-family: var(--serif);
  font-size: 60px;
  color: var(--accent);
  opacity: 0.35;
  line-height: 1;
}
.content blockquote p {
  font-family: var(--serif-body);
  font-size: 18px;
  font-style: italic;
  color: var(--text);
  line-height: 1.55;
  margin-bottom: 8px;
}
.content blockquote p:last-child { margin-bottom: 0; }

/* TABELA */
.table-wrap {
  margin: 24px 0 32px;
  overflow-x: auto;
  border: 1px solid var(--line);
  border-radius: 6px;
  background: var(--bg-card);
}
.content table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}
.content thead th {
  text-align: left;
  padding: 14px 18px;
  background: var(--bg-soft);
  font-family: var(--sans);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-size: 11px;
  color: var(--accent);
  border-bottom: 1px solid var(--line-strong);
}
.content tbody td {
  padding: 14px 18px;
  border-bottom: 1px solid var(--line);
  vertical-align: top;
  color: var(--text-muted);
  line-height: 1.5;
}
.content tbody tr:last-child td { border-bottom: none; }
.content tbody tr:hover { background: var(--bg-card-hover); }
.content tbody td strong { color: var(--text); }

/* CODE */
.content code {
  font-family: var(--mono);
  font-size: 0.88em;
  background: var(--bg-card);
  border: 1px solid var(--line);
  padding: 2px 7px;
  border-radius: 3px;
  color: var(--accent-strong);
}
.content pre {
  margin: 24px 0;
  padding: 22px 24px;
  background: #0d0d0d;
  border: 1px solid var(--line);
  border-radius: 6px;
  overflow-x: auto;
  position: relative;
}
.content pre::before {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--accent), transparent);
}
.content pre code {
  background: transparent;
  border: none;
  padding: 0;
  color: var(--text);
  font-size: 13px;
  line-height: 1.55;
  white-space: pre;
}

/* FOOTER NOTE (italic-only line at end) */
.content .footer-note {
  margin-top: 32px;
  padding: 18px 22px;
  background: var(--gold-soft);
  border-left: 3px solid var(--gold);
  border-radius: 0 4px 4px 0;
  color: var(--text-muted);
  font-size: 14px;
}

/* SITE FOOTER */
.site-footer {
  background: var(--bg-soft);
  border-top: 1px solid var(--line);
  padding: 48px 64px;
}
.footer-inner {
  max-width: 880px;
  margin: 0 auto;
  text-align: center;
}
.footer-brand {
  font-family: var(--serif);
  font-size: 22px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 12px;
  letter-spacing: 0.5px;
}
.footer-brand span { color: var(--accent); margin: 0 8px; font-weight: 400; }
.footer-meta {
  font-size: 13px;
  color: var(--text-soft);
  margin-bottom: 4px;
  letter-spacing: 0.3px;
}
.footer-meta:last-child {
  margin-top: 16px;
  font-family: var(--serif);
  font-style: italic;
  font-size: 15px;
  color: var(--gold);
}

/* BACK TO TOP */
.back-top {
  position: fixed;
  bottom: 24px; right: 24px;
  width: 44px; height: 44px;
  background: var(--accent);
  color: #051817;
  border: none;
  border-radius: 50%;
  font-family: var(--mono);
  font-weight: 700;
  font-size: 18px;
  cursor: pointer;
  z-index: 30;
  opacity: 0;
  pointer-events: none;
  transition: all .25s;
  box-shadow: 0 8px 24px rgba(0,0,0,0.4);
}
.back-top.visible {
  opacity: 1;
  pointer-events: auto;
}
.back-top:hover { background: var(--accent-strong); transform: translateY(-2px); }

/* RESPONSIVE */
@media (max-width: 1024px) {
  :root { --sidebar-w: 280px; }
  .hero { padding: 64px 40px 48px; }
  .block { padding: 56px 40px 64px; }
  .site-footer { padding: 40px; }
}

@media (max-width: 768px) {
  html { font-size: 16px; }
  .sidebar {
    transform: translateX(-100%);
    width: 88%;
    max-width: 340px;
    box-shadow: 4px 0 30px rgba(0,0,0,0.5);
  }
  .sidebar.open { transform: translateX(0); }
  .menu-toggle { display: flex; }
  .main { margin-left: 0; }
  .hero { padding: 88px 24px 40px; }
  .hero-title { font-size: clamp(30px, 9vw, 44px); }
  .hero-sub { font-size: 17px; }
  .hero-meta { padding: 16px 18px; gap: 14px; }
  .meta-num { font-size: 26px; }
  .meta-divider { display: none; }
  .meta-item { flex: 1 0 40%; }
  .block { padding: 44px 24px 52px; }
  .content h2 { font-size: 26px; margin-bottom: 24px; }
  .content h3 { font-size: 19px; margin: 28px 0 14px; }
  .content h4 { font-size: 14px; }
  .content p { font-size: 16px; }
  .content blockquote { padding: 18px 20px; }
  .content blockquote p { font-size: 16px; }
  .content pre { padding: 16px 18px; font-size: 12px; }
  .content table { font-size: 13px; }
  .content thead th, .content tbody td { padding: 10px 12px; }
  .site-footer { padding: 32px 24px; }
  .back-top { bottom: 16px; right: 16px; width: 40px; height: 40px; }
}

@media (max-width: 480px) {
  .hero-byline { font-size: 12px; }
  .hero-byline .sep { display: block; opacity: 0; height: 0; margin: 0; }
}

/* PRINT */
@media print {
  :root { --bg: #fff; --bg-soft: #fff; --bg-card: #f7f7f4; --text: #111; --text-muted: #333; --text-soft: #555; --line: #ddd; --line-strong: #999; }
  body { background: #fff; color: #111; font-size: 11pt; }
  .sidebar, .menu-toggle, .overlay, .back-top { display: none !important; }
  .main { margin-left: 0; }
  .hero, .block, .site-footer { padding: 24pt 0; page-break-inside: avoid; }
  .block { border-bottom: 1px solid #ddd; }
  .content h2 { color: #000; }
  .content h3 { color: #000; }
  .content blockquote { background: #f7f7f4; box-shadow: none; }
  .content pre { background: #f4f4f0; border: 1px solid #ddd; }
  a { color: #000; text-decoration: underline; }
  .hero-title em { color: #555; }
}
"""


JS = r"""
(function() {
  var menuBtn = document.getElementById('menuToggle');
  var sidebar = document.getElementById('sidebar');
  var overlay = document.getElementById('overlay');
  var backTop = document.getElementById('backTop');

  function closeSidebar() {
    sidebar.classList.remove('open');
    overlay.classList.remove('active');
    menuBtn.classList.remove('active');
    document.body.style.overflow = '';
  }
  function openSidebar() {
    sidebar.classList.add('open');
    overlay.classList.add('active');
    menuBtn.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  menuBtn.addEventListener('click', function() {
    if (sidebar.classList.contains('open')) closeSidebar();
    else openSidebar();
  });
  overlay.addEventListener('click', closeSidebar);

  // Fecha menu ao clicar em link no mobile
  document.querySelectorAll('.sidebar-link').forEach(function(a) {
    a.addEventListener('click', function() {
      if (window.innerWidth <= 768) closeSidebar();
    });
  });

  // Active link tracking via IntersectionObserver
  var sections = document.querySelectorAll('section.block');
  var links = {};
  document.querySelectorAll('.sidebar-link').forEach(function(a) {
    var href = a.getAttribute('href');
    if (href && href.charAt(0) === '#') links[href.slice(1)] = a;
  });

  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        var id = entry.target.id;
        var link = links[id];
        if (!link) return;
        if (entry.isIntersecting) {
          Object.keys(links).forEach(function(k) { links[k].classList.remove('active'); });
          link.classList.add('active');
        }
      });
    }, { rootMargin: '-30% 0px -60% 0px', threshold: 0 });
    sections.forEach(function(s) { observer.observe(s); });
  }

  // Back to top
  window.addEventListener('scroll', function() {
    if (window.scrollY > 600) backTop.classList.add('visible');
    else backTop.classList.remove('visible');
  }, { passive: true });
  backTop.addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // Esc fecha sidebar
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && sidebar.classList.contains('open')) closeSidebar();
  });
})();
"""


def main():
    md = SRC.read_text(encoding='utf-8')
    content_html, sidebar = md_to_html(md)
    sidebar_html = build_sidebar_html(sidebar)

    html = HTML_TEMPLATE.replace('__SIDEBAR__', sidebar_html).replace('__CONTENT__', content_html)

    (ROOT / 'index.html').write_text(html, encoding='utf-8')
    (ROOT / 'style.css').write_text(CSS, encoding='utf-8')
    (ROOT / 'script.js').write_text(JS, encoding='utf-8')

    print(f'OK: {len(sidebar)} blocos renderizados')
    print(f'  - {ROOT}/index.html')
    print(f'  - {ROOT}/style.css')
    print(f'  - {ROOT}/script.js')


if __name__ == '__main__':
    main()
