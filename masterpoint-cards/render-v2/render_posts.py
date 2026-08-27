# -*- coding: utf-8 -*-
"""Renderiza o 1o lote de posts do Master Point Cursos."""
import json
from pathlib import Path
import mp_carousel as mp

OUT = Path(__file__).resolve().parent
OUT.mkdir(exist_ok=True)

# ================= CARROSSEIS =================
POSTS = {}

# ---- 00 CATALOGO GERAL ----
POSTS["00-catalogo-geral"] = {"slides":[
 {"tipo":"capa","kicker":"// CATALOGO 2026","headline":"+180 CURSOS PRA VOCÊ APRENDER E CRESCER",
  "sub":"Certificado reconhecido, aqui em Castelo do Piauí.","cta":"ARRASTA"},
 {"tipo":"lista","kicker":"// AREAS 01","eyebrow":"O QUE VOCÊ VAI ENCONTRAR","headline":"Um curso pra cada objetivo",
  "sub":"Tudo em um só lugar, do básico ao avançado.",
  "itens":["Informática e Office (Excel, Word, Windows)","Design, Vídeo e Computação Gráfica",
           "Marketing Digital, IA e Programação","Inglês, Espanhol e Profissionalizantes"],"cta":"CONTINUA"},
 {"tipo":"lista","kicker":"// AREAS 02","eyebrow":"MAIS AREAS","headline":"Do escritório ao mercado de trabalho",
  "itens":["CAD e Projetos 3D (AutoCAD, Revit)","Gestão, RH e Educação Financeira",
           "Cursos Kids pra crianças e adolescentes","NRs e Segurança do Trabalho"],"cta":"CONTINUA"},
 {"tipo":"texto","kicker":"// POR QUE MASTER POINT","headline":"Por que estudar com a gente?",
  "body":["Aulas práticas, no seu ritmo, do zero ao avançado.",
          "Certificado que fortalece o seu currículo.",
          "Atendimento de perto, presencial em Castelo do Piauí."],"cta":"QUASE LA"},
 {"tipo":"cta","headline":"Escolha o seu curso hoje","body":["São +180 opções esperando por você.","Fale com a gente e garanta sua vaga."],
  "cta_pill":"LINK NA BIO"},
]}

# ---- 01 OFFICE ----
POSTS["01-office-escritorio"] = {"slides":[
 {"tipo":"capa","kicker":"// PACOTE OFFICE","headline":"DOMINE O COMPUTADOR DO ZERO AO AVANÇADO",
  "sub":"Os programas que o mercado mais pede.","cta":"ARRASTA"},
 {"tipo":"texto","kicker":"// A REAL","headline":"Saber Office abre porta de emprego",
  "body":["Toda vaga de escritório pede Excel, Word e PowerPoint.",
          "Quem domina essas ferramentas se destaca na hora da contratação."],"cta":"CONTINUA"},
 {"tipo":"lista","kicker":"// O QUE TEM","eyebrow":"CURSOS DO PACOTE","headline":"O essencial de informática",
  "itens":["Excel Fundamental, Avançado e Dashboard","Word e PowerPoint completos","Windows 10 e 11",
           "Power BI, Digitação e Nuvem","Google for Education e Normas ABNT"],"cta":"VER TODOS"},
 {"tipo":"texto","kicker":"// RESULTADO","headline":"O que você vai conseguir fazer",
  "body":["Montar planilhas e relatórios que impressionam.",
          "Criar apresentações profissionais.",
          "Se virar em qualquer computador com segurança."],"cta":"QUASE LA"},
 {"tipo":"cta","headline":"Comece pelo Office","body":["A base que todo profissional precisa.","Fale com a gente e escolha sua turma."],
  "cta_pill":"LINK NA BIO"},
]}

# ---- 02 DESIGN ----
POSTS["02-design-criacao"] = {"slides":[
 {"tipo":"capa","kicker":"// PACOTE DESIGN","headline":"CRIE ARTES QUE VENDEM E CHAMAM ATENÇÃO",
  "sub":"Do Canva ao Photoshop profissional.","cta":"ARRASTA"},
 {"tipo":"texto","kicker":"// A REAL","headline":"Design é uma profissão que paga bem",
  "body":["Empresas precisam de posts, logos e materiais o tempo todo.",
          "Quem sabe criar arte tem trabalho sobrando como freelancer."],"cta":"CONTINUA"},
 {"tipo":"lista","kicker":"// O QUE TEM","eyebrow":"CURSOS DO PACOTE","headline":"Ferramentas de criação visual",
  "itens":["Adobe Photoshop e Illustrator","CorelDRAW e InDesign","Canva do básico ao avançado",
           "CapCut pra edição rápida","Vitrinismo pra vitrines que vendem"],"cta":"VER TODOS"},
 {"tipo":"texto","kicker":"// RESULTADO","headline":"O que você vai criar",
  "body":["Logos, posts e artes pra redes sociais.",
          "Materiais gráficos pra empresas e clientes.",
          "Seu portfólio pra começar a faturar."],"cta":"QUASE LA"},
 {"tipo":"cta","headline":"Vire criador de artes","body":["Transforme criatividade em renda.","Fale com a gente e comece agora."],
  "cta_pill":"LINK NA BIO"},
]}

# ---- 03 MARKETING & WEB ----
POSTS["03-marketing-web"] = {"slides":[
 {"tipo":"capa","kicker":"// PACOTE MARKETING","headline":"APRENDA A VENDER E DIVULGAR NA INTERNET",
  "sub":"Marketing digital do jeito certo.","cta":"ARRASTA"},
 {"tipo":"texto","kicker":"// A REAL","headline":"Todo negócio precisa aparecer online",
  "body":["Quem sabe marketing digital consegue cliente pra qualquer negócio.",
          "É uma das habilidades mais procuradas hoje."],"cta":"CONTINUA"},
 {"tipo":"lista","kicker":"// O QUE TEM","eyebrow":"CURSOS DO PACOTE","headline":"Do tráfego ao site",
  "itens":["Marketing Digital completo","Google Ads e Meta Business","Facebook e WhatsApp Business",
           "Mídias Sociais e Marketing Pessoal","WordPress pra criar sites"],"cta":"VER TODOS"},
 {"tipo":"texto","kicker":"// RESULTADO","headline":"O que você vai conseguir fazer",
  "body":["Criar campanhas que trazem clientes.",
          "Gerenciar redes sociais de empresas.",
          "Montar e publicar sites profissionais."],"cta":"QUASE LA"},
 {"tipo":"cta","headline":"Domine o marketing digital","body":["A habilidade que gera renda de qualquer lugar.","Fale com a gente e comece."],
  "cta_pill":"LINK NA BIO"},
]}

# ---- 04 IA & AUTOMACAO ----
POSTS["04-ia-automacao"] = {"slides":[
 {"tipo":"capa","kicker":"// PACOTE IA","headline":"SAIA NA FRENTE USANDO INTELIGÊNCIA ARTIFICIAL",
  "sub":"IA e automação no trabalho e nos negócios.","cta":"ARRASTA"},
 {"tipo":"texto","kicker":"// A REAL","headline":"Quem usa IA trabalha melhor e mais rápido",
  "body":["A inteligência artificial já mudou o mercado de trabalho.",
          "Quem domina essas ferramentas larga na frente da concorrência."],"cta":"CONTINUA"},
 {"tipo":"lista","kicker":"// O QUE TEM","eyebrow":"CURSOS DO PACOTE","headline":"IA aplicada de verdade",
  "itens":["ChatGPT do básico ao avançado","Inteligência Artificial e IA Fast","Empreendendo com IA nos Negócios",
           "Fundamentos do N8N (automação)","Lovable AI pra criar aplicativos"],"cta":"VER TODOS"},
 {"tipo":"texto","kicker":"// RESULTADO","headline":"O que você vai conseguir fazer",
  "body":["Usar IA pra produzir mais em menos tempo.",
          "Automatizar tarefas repetitivas do dia a dia.",
          "Criar soluções pro seu negócio com IA."],"cta":"QUASE LA"},
 {"tipo":"cta","headline":"Domine a IA agora","body":["O futuro do trabalho já começou.","Fale com a gente e garanta sua vaga."],
  "cta_pill":"LINK NA BIO"},
]}

# ---- 05 PROFISSIONALIZANTES ----
POSTS["05-profissionalizantes"] = {"slides":[
 {"tipo":"capa","kicker":"// PACOTE PROFISSOES","headline":"QUALIFICAÇÃO RÁPIDA PRA ENTRAR NO MERCADO",
  "sub":"Cursos práticos pra conseguir emprego.","cta":"ARRASTA"},
 {"tipo":"texto","kicker":"// A REAL","headline":"Empresa contrata quem tem qualificação",
  "body":["Um certificado faz a diferença na hora da vaga.",
          "Nossos cursos profissionalizantes preparam você pro trabalho de verdade."],"cta":"CONTINUA"},
 {"tipo":"lista","kicker":"// O QUE TEM","eyebrow":"CURSOS DO PACOTE","headline":"Profissões com demanda real",
  "itens":["Operador de Caixa e Atendente","Cuidador de Idosos","Agente de Portaria e Síndico",
           "Logística e Telemarketing","Técnicas de Vendas e Hotelaria"],"cta":"VER TODOS"},
 {"tipo":"texto","kicker":"// RESULTADO","headline":"Pronto pra sua próxima vaga",
  "body":["Certificado que fortalece o currículo.",
          "Conhecimento prático pra começar a trabalhar.",
          "Mais chances de conseguir emprego rápido."],"cta":"QUASE LA"},
 {"tipo":"cta","headline":"Se qualifique agora","body":["Sua próxima vaga começa com um curso.","Fale com a gente e escolha o seu."],
  "cta_pill":"LINK NA BIO"},
]}

# ---- 06 IDIOMAS ----
POSTS["06-idiomas"] = {"slides":[
 {"tipo":"capa","kicker":"// PACOTE IDIOMAS","headline":"APRENDA INGLÊS E ESPANHOL DO SEU JEITO",
  "sub":"Pra trabalho, viagem e negócios.","cta":"ARRASTA"},
 {"tipo":"texto","kicker":"// A REAL","headline":"Falar outra língua abre portas",
  "body":["Inglês e espanhol valem pontos em qualquer currículo.",
          "E te preparam pra viajar e fazer negócios com o mundo."],"cta":"CONTINUA"},
 {"tipo":"lista","kicker":"// O QUE TEM","eyebrow":"CURSOS DO PACOTE","headline":"Do introdutório ao avançado",
  "itens":["Inglês Básico, Intermediário e Avançado","Inglês pra Negócios, Viagens e Turismo","Inglês Kids pras crianças",
           "Espanhol completo (vários níveis)","Cursos técnicos também em espanhol"],"cta":"VER TODOS"},
 {"tipo":"texto","kicker":"// RESULTADO","headline":"O que você vai conquistar",
  "body":["Mais confiança pra falar e entender.",
          "Um diferencial no mercado de trabalho.",
          "Preparo pra viagens e oportunidades novas."],"cta":"QUASE LA"},
 {"tipo":"cta","headline":"Comece a falar hoje","body":["O idioma que vai mudar sua vida profissional.","Fale com a gente e escolha o curso."],
  "cta_pill":"LINK NA BIO"},
]}

# ================= RENDER =================
if __name__ == "__main__":
    manifest={}
    for slug, carr in POSTS.items():
        dst=OUT/slug
        paths=mp.render_carrossel(carr, dst)
        manifest[slug]={"n_slides":len(paths),"arquivos":[p.split('/')[-1] for p in paths]}
        print(f"OK {slug}: {len(paths)} slides")
    json.dump(manifest, open(OUT/"manifest.json","w"), ensure_ascii=False, indent=2)
    print("\nTOTAL posts:", len(POSTS), "| total slides:", sum(m['n_slides'] for m in manifest.values()))
