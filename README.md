# Sistema de Gestão de Estoque (SGE)

![Testes](https://github.com/ThiagoHMDornelas/sge/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Django](https://img.shields.io/badge/django-5.0-092E20)
![DRF](https://img.shields.io/badge/DRF-3.16-red)

Sistema de gestão de estoque desenvolvido com Django e Django REST Framework. Controla produtos, marcas, categorias e fornecedores, além de entradas e saídas de estoque com atualização automática das quantidades. Oferece interface web (templates) e API REST autenticada por JWT.

## Sumário

- [Visão geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Instalação e execução](#instalação-e-execução)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Banco de dados](#banco-de-dados)
- [Executar com Docker](#executar-com-docker)
- [API REST](#api-rest)
- [Testes](#testes)
- [Principais rotas](#principais-rotas)
- [Painel administrativo](#painel-administrativo)
- [Licença](#licença)

## Visão geral

O **SGE** é um sistema web e de API para gerenciamento de estoque. Usuários autenticados e com permissão podem cadastrar, listar, alterar e remover marcas, categorias, fornecedores e produtos. Cada movimento de **entrada** soma e cada **saída** subtrai automaticamente a quantidade do produto em estoque, via *signals* do Django. A tela inicial apresenta indicadores e gráficos de produtos e vendas.

## Funcionalidades

- CRUD de produtos, marcas, categorias e fornecedores
- Entradas e saídas de estoque com atualização automática da quantidade
- Dashboard com métricas de estoque, vendas e gráficos
- Cadastro e edição de perfil de usuário (com avatar)
- Autenticação de usuários e controle de permissões por ação
- API REST autenticada por JWT (tokens de acesso e atualização)
- Busca, filtro e ordenação nas listagens
- Painel administrativo do Django

## Tecnologias

- Python
- Django 5.0
- Django REST Framework + SimpleJWT
- drf-spectacular (documentação da API)
- python-decouple (variáveis de ambiente)
- SQLite e PostgreSQL (via psycopg2)
- Bootstrap 5
- Docker e Docker Compose
- flake8 (desenvolvimento)
- GitHub Actions (CI)

## Estrutura do projeto

```
sge/
├── app/                # configurações, urls raiz, home e templates base
├── core/               # BaseModel, middleware, permissões e template tags
├── authentication/     # perfil de usuário e autenticação JWT
├── brands/             # CRUD de marcas (HTML + API)
├── category/           # CRUD de categorias (HTML + API)
├── supplier/           # CRUD de fornecedores (HTML + API)
├── product/            # CRUD de produtos (HTML + API)
├── inflow/             # entradas de estoque (HTML + API)
├── outflow/            # saídas de estoque (HTML + API)
├── static/             # arquivos estáticos de origem
├── .github/workflows/  # pipeline de CI (GitHub Actions)
├── Dockerfile
├── docker-compose.yml
├── .env.example        # exemplo de variáveis de ambiente
├── manage.py
├── requirements.txt
└── requirements_dev.txt
```

## Instalação e execução

Pré-requisitos:

- Python 3.11 ou superior instalado

Crie um ambiente virtual:

    python -m venv .venv

No Windows, ative o ambiente virtual:

    .venv\Scripts\activate

No Linux ou macOS, ative o ambiente virtual:

    source .venv/bin/activate

Instale as dependências:

    pip install -r requirements.txt

Opcionalmente, para desenvolvimento (lint), instale também:

    pip install -r requirements_dev.txt

Crie o arquivo de ambiente (veja [Variáveis de ambiente](#variáveis-de-ambiente)):

    copy .env.example .env        # Windows
    cp .env.example .env          # Linux/macOS

Aplique as migrações:

    python manage.py migrate

Crie um usuário administrador:

    python manage.py createsuperuser

Inicie o servidor:

    python manage.py runserver

A aplicação estará disponível em:

    http://127.0.0.1:8000/

## Variáveis de ambiente

Copie o `.env.example` para `.env` e ajuste os valores:

    # Django
    SECRET_KEY=troque-por-uma-chave-secreta
    DEBUG=True
    ALLOWED_HOSTS=0.0.0.0,127.0.0.1,localhost

    # Cookies
    SESSION_COOKIE_NAME=sge_sessionid
    CSRF_COOKIE_NAME=sge_csrf

    # Superusuário (usado com createsuperuser --noinput)
    DJANGO_SUPERUSER_USERNAME=
    DJANGO_SUPERUSER_EMAIL=
    DJANGO_SUPERUSER_PASSWORD=

    # Banco de dados (veja a seção "Banco de dados")
    DB_ENV=dev
    ACTIVE_DB=sqlite
    POSTGRES_DB=sge
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432

## Banco de dados

O projeto pode rodar com dois bancos, controlados pelas variáveis `DB_ENV` e `ACTIVE_DB`:

- `DB_ENV=dev` + `ACTIVE_DB=sqlite` → SQLite (`db.sqlite3`)
- `DB_ENV=dev` + `ACTIVE_DB=postgresql` → PostgreSQL
- `DB_ENV=prd` → força PostgreSQL (usado no Docker)

## Executar com Docker

Com o Docker e o Docker Compose instalados, é possível subir a aplicação e o PostgreSQL sem configurar o ambiente Python manualmente:

    docker compose up --build

Serviços:

- `sge_web` → aplicação Django em `http://localhost:8000/`
- `sge_db` → PostgreSQL 17 (dados persistidos em volume)

As migrações são aplicadas automaticamente na inicialização. Para criar um superusuário no container:

    docker compose exec sge_web python manage.py createsuperuser

Para parar e remover os containers:

    docker compose down

## API REST

A API é autenticada por **JWT** (`djangorestframework-simplejwt`) e as permissões são verificadas por método HTTP (`view`, `add`, `change`, `delete`). A documentação interativa (Swagger/OpenAPI) está disponível em `/api/docs/` (schema em `/api/schema/`).

Obter o token:

    POST /api/v1/authentication/token/
    { "username": "seu_usuario", "password": "sua_senha" }

Utilize o token nas requisições:

    Authorization: Bearer <access_token>

Endpoints principais (por recurso):

| Recurso | Listar / Criar | Detalhe / Alterar / Excluir |
|---|---|---|
| Marcas | `GET/POST /api/v1/brands/` | `GET/PUT/PATCH/DELETE /api/v1/brands/<id>/` |
| Categorias | `GET/POST /api/v1/categories/` | `GET/PUT/PATCH/DELETE /api/v1/categories/<id>/` |
| Fornecedores | `GET/POST /api/v1/supplier/` | `GET/PUT/PATCH/DELETE /api/v1/supplier/<id>/` |
| Produtos | `GET/POST /api/v1/products/` | `GET/PUT/PATCH/DELETE /api/v1/products/<id>/` |
| Entradas | `GET/POST /api/v1/inflows/` | `GET /api/v1/inflows/<id>/` |
| Saídas | `GET/POST /api/v1/outflows/` | `GET/PUT/PATCH/DELETE /api/v1/outflows/<id>/` |

## Testes

A suíte cobre modelos, formulários, views, *signals* de estoque e endpoints da API. Execute:

    python manage.py test

O **lint** do código é feito com `flake8` (configuração em `.flake8`):

    flake8

A suíte e o lint também rodam automaticamente a cada `push` e `pull request` via **GitHub Actions** (`.github/workflows/tests.yml`): o pipeline executa o **lint (flake8)** e os testes em **SQLite** e também em **PostgreSQL**. O resultado é exibido no badge no topo deste README.

## Principais rotas

| Rota | Descrição |
|---|---|
| `/` | Dashboard (requer login) |
| `/login/`, `/logout/` | Autenticação |
| `/profile/` | Perfil do usuário |
| `/products/list/`, `/products/create/` | Listagem e cadastro de produtos |
| `/products/<id>/detail/`, `/products/<id>/update/`, `/products/<id>/delete/` | Detalhe, edição e exclusão de produto |
| `/brands/list/`, `/brands/create/`, `/brands/<id>/detail/`, `/brands/<id>/update/`, `/brands/<id>/delete/` | CRUD de marcas |
| `/categories/list/`, `/categories/create/`, `/categories/<id>/detail/`, `/categories/<id>/update/`, `/categories/<id>/delete/` | CRUD de categorias |
| `/suppliers/list/`, `/suppliers/create/`, `/suppliers/<id>/detail/`, `/suppliers/<id>/update/`, `/suppliers/<id>/delete/` | CRUD de fornecedores |
| `/inflows/list/`, `/inflows/create/`, `/inflows/<id>/detail/` | Entradas de estoque |
| `/outflows/list/`, `/outflows/create/`, `/outflows/<id>/detail/` | Saídas de estoque |
| `/api/v1/...` | API REST |
| `/api/docs/` | Documentação interativa da API (Swagger) |
| `/admin/` | Painel administrativo |

## Painel administrativo

Acesse `/admin/` com o superusuário criado. Todos os recursos (produtos, marcas, categorias, fornecedores, entradas e saídas) ficam disponíveis para gerenciamento.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
