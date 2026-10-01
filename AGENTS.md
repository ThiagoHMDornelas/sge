# SGE - Sistema de Gestão de Estoque

Django 5 + DRF + SimpleJWT. Locale pt-br.

## Comandos
<!-- Os comandos exatos para rodar o projeto. O ponto-chave é que
não existe suite de testes, então não tente rodar pytest ou manage.py test. -->

```bash
python manage.py migrate          # aplicar migrações
python manage.py runserver        # servidor de desenvolvimento :8000
flake8                            # lint (ignora E501, exclui .venv)
pip install -r requirements_dev.txt  # deps de dev (flake8)
```

Ainda não existe suite de testes.

## Arquitetura
<!-- Arquitetura — Três pegadinhas principais:
  1. O módulo de settings é `app.settings`, não `sge.settings` (padrão Django).
     Se errar isso, nada funciona.
  2. Todos os modelos herdam de `BaseModel`, que adiciona automaticamente
     created_at, updated_at, user_created e user_updated. Nunca use
     models.Model diretamente.
  3. O `CurrentUserMiddleware` guarda o usuário em thread-local para preencher
     user_created/user_updated sem precisar passar o request pelo form. -->

- **Módulo de settings**: `app.settings` (não é o padrão Django `sge.settings`)
- **Modelo base**: `core.models.BaseModel` — todos os models de negócio herdam dele. Fornece `created_at`, `updated_at`, `user_created`, `user_updated` (auto-preenchidos via `core.middleware.CurrentUserMiddleware`)
- **Troca de banco**: Controlada pelo `.env` — `DB_ENV=prd` → PostgreSQL; caso contrário `ACTIVE_DB=sqlite|postgresql` seleciona o backend. Padrão é SQLite (`db.sqlite3`).
- **Carregamento de env**: `python-dotenv` carrega `.env` na importação do settings. Copiar `.env.example` para `.env` antes de rodar.

## Apps Django
<!-- Apps Django — Tabela com o propósito de cada app e suas particularidades.
  - `core` é abstrato (sem tabela no banco).
  - `authentication` cria `Profile` automaticamente via signal. -->

| App | Finalidade | Observações |
|---|---|---|
| `app` | Config do projeto, URLs raiz, home, templates | `app/templates/` tem layout base e componentes |
| `core` | BaseModel, middleware, permissions, context processors | Sem tabela — `BaseModel` é abstrato |
| `authentication` | Perfil de usuário (avatar), endpoints JWT | Signal cria `Profile` automaticamente ao criar `User` |
| `brands` | CRUD de marcas (HTML + API) | Views duplas: CBV + DRF generics |
| `category` | CRUD de categorias (HTML + API) | Mesmo padrão de views duplas |
| `supplier` | CRUD de fornecedores (HTML + API) | Mesmo padrão de views duplas |
| `product` | CRUD de produtos (HTML + API) | Depende de `brands` + `category` |
| `inflow` | CRUD de entradas de estoque (HTML + API) | `signals.py` soma quantidade ao produto ao criar |
| `outflow` | CRUD de saídas de estoque (HTML + API) | `signals.py` subtrai quantidade do produto ao criar |

## Padrões importantes
<!-- Padrões importantes — Padrões que não são óbvios só olhando os nomes:
  - Interface dupla: cada app de negócio tem views HTML (CBV com login +
    permissão) E endpoints API (DRF em api/v1/). Ao criar um novo CRUD,
    precisa seguir esse padrão duplo.
  - Signals de estoque: `inflow` soma quantidade ao produto, `outflow`
    subtrai. Ambos rodam no post_save e são importados no apps.py via ready().
  - DETAIL_LAYOUT: configuração que controla como os templates de detail
    renderizam. -->

- **Interface dupla**: Cada app de negócio serve HTML (CBV Django com `LoginRequiredMixin` + `PermissionRequiredMixin`) e API REST (DRF generics em `api/v1/`). A API usa `core.permissions.ModelPermissionsByMethod` para verificação de permissão por método HTTP.
- **Signals de estoque**: `inflow` e `outflow` têm signal `post_save` que atualiza `Product.quantity`. Os apps importam seus signals no `apps.py` via `ready()`.
- **CurrentUserMiddleware**: Armazena `request.user` em thread-local para que `BaseModel.save()` preencha `user_created`/`user_updated` sem precisar passar o request pelos forms.
- **DETAIL_LAYOUT** (valores: `minimal`, `table`, `cards`, `fine`, `badges`) controla a renderização do template de detail via context processor.

## Docker
<!-- Docker — O entrypoint já roda migrate + runserver. Superuser é criado com
variáveis de ambiente DJANGO_SUPERUSER_*. -->

```bash
docker compose up        # inicia sge_web (:8000) + sge_db (PostgreSQL 17)
```

O entrypoint do Docker roda `migrate` e depois `runserver`. Criação de superuser usa variáveis `DJANGO_SUPERUSER_*` com `createsuperuser --noinput`.

## Convenções
<!-- Convenções — Convenções que diferem do padrão Django: locale pt-br,
ordenação com Lower() para campos de texto, JWT com lifetime longo
(1 dia access / 7 dias refresh). -->

- Locale: `pt-br` / `America/Sao_Paulo`
- Todos os models usam `BaseModel` de `core.models` (nunca `models.Model` direto)
- Ordenação padrão: campos de texto usam `Lower()` para ordenação case-insensitive; inflow/outflow ordenam por `-created_at`
- Arquivos estáticos: `static/` → coletados em `staticfiles/`; mídia em `media/`
- JWT: access token 1 dia; refresh 7 dias
