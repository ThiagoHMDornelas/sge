# AGENTS.md — sge

> Gerado automaticamente na clonagem para a VPS (21/10/2026). **Revisar**: ajuste o que não bater com a realidade do projeto.

## Visão geral
**Sistema de Gestão de Estoque**: API REST (Django + DRF) com autenticação JWT, documentação OpenAPI e fluxos de entrada/saída de produtos.

**Stack:** Django 5.0.14 · DRF 3.16 · SimpleJWT · drf-spectacular · Python 3.12 · SQLite (dev) ou PostgreSQL · Docker

## Contexto em camadas
`~/.hermes/SOUL.md` (regras globais) → `~/projetos/python/AGENTS.md` (regras da linguagem) → este arquivo (particularidades do projeto).
Em conflito, vale o mais específico (este arquivo), exceto em regras de segurança/global.

## Estrutura
- `app/` — projeto Django (`app/settings.py`)
- `authentication/` — login JWT
- `core/` — base compartilhada
- `brands/`, `category/`, `supplier/`, `product/` — cadastros
- `inflow/`, `outflow/` — movimentações de estoque

## Como rodar
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements_dev.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```
No Docker o `CMD` já roda `migrate` antes do `runserver`.

## Testes e lint
```bash
python manage.py test
flake8
```

## Banco de dados
`DB_ENV=dev` + `ACTIVE_DB=sqlite` por padrão (nenhum serviço extra). Para PostgreSQL: `ACTIVE_DB=postgresql` + `POSTGRES_*`; para Docker, descomentar o bloco `prd` do `.env.example`.

## Particularidades
- Cookies de sessão/CSRF usam prefixo `sge_` (`SESSION_COOKIE_NAME`, `CSRF_COOKIE_NAME`).
- Documentação da API via drf-spectacular.
- Estoque só deve mudar por `inflow`/`outflow`, não por edição direta de `product`.

## Convenções
- Secrets **sempre** em `.env` (nunca hardcode); mantenha o `.env.example` atualizado e o `.env` fora do versionamento.
- Migrações que apagam ou tornam campo obrigatório sem `default` precisam de aviso antes de rodar em produção.
- Mensagens de UI/validação em português do Brasil, revisadas (acentuação e concordância).
- Não commitar/pushar por conta própria: as alterações ficam prontas para o usuário revisar e commitar.
- Preservar encoding dos arquivos ao editar (não converter ANSI ↔ UTF-8 sem pedido explícito).
