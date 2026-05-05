# Paginas de Venda — Digital Master

Repositorio das paginas de venda da Digital Master, servidas via GitHub Pages.

## Estrutura

Cada pagina em uma subpasta. URL final: `https://paginas.salatielbatista.com.br/<slug-projeto>/`

```
paginas-vendas/
├── maquina-de-influence/
│   ├── index.html
│   └── images/
└── (outras paginas)
```

## Como rodar localmente

Abrir o `index.html` da subpasta no navegador, ou servir com:

```
python -m http.server 8000
```

E acessar `http://localhost:8000/<slug>/`.

## Deploy

Automatico via GitHub Pages na branch `main`. Push pra main = pagina no ar em ~30s.

Em producao, paginas geradas pela skill `skill-pagina-vendas` da Naia sao commitadas automaticamente neste repo.
