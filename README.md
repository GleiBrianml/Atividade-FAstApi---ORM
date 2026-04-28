# 📦 StockManager

Sistema de gestão de estoque desenvolvido com **FastAPI**, **SQLAlchemy** e **Jinja2**, com interface em **HTML + Tailwind CSS**.

---

## 🗂️ Estrutura do Projeto

```
stockmanager/
├── main.py               # Rotas e lógica da aplicação (FastAPI)
├── models.py             # Modelos do banco de dados (SQLAlchemy)
├── database.py           # Configuração da conexão com o banco
└── templates/
    ├── index.html            # Painel de controle (Dashboard)
    ├── categorias.html       # Listagem de categorias
    ├── cadastrar_categoria.html  # Formulário de nova categoria
    ├── produtos.html         # Listagem de produtos
    └── cadastrar_produto.html    # Formulário de novo produto
```

---

## ⚙️ Instalação

### Pré-requisitos

- Python 3.10+
- pip

### Passos

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/stockmanager.git
cd stockmanager

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows

# Instale as dependências
pip install fastapi uvicorn sqlalchemy jinja2 python-multipart
```

### Rodando o servidor

```bash
uvicorn main:app --reload
```

Acesse em: [http://localhost:8000](http://localhost:8000)

---

## 🗃️ Banco de Dados

O projeto usa **SQLite** por padrão via SQLAlchemy, e o **Alembic** para criação e gerenciamento de migrações.

### Configuração inicial do Alembic

```bash
# Instale o Alembic
pip install alembic

# Inicialize na raiz do projeto
alembic init migrations
```

No arquivo `migrations/env.py`, aponte para os seus modelos:

```python
from models import Base
target_metadata = Base.metadata
```

### Criando as tabelas pela primeira vez

```bash
# Gera o arquivo de migração inicial
alembic revision --autogenerate -m "criar tabelas iniciais"

# Aplica a migração no banco
alembic upgrade head
```

### Atualizando o banco após alterar um modelo

Sempre que adicionar ou remover colunas/tabelas nos modelos, gere uma nova migração:

```bash
# Gera a migração com as diferenças detectadas
alembic revision --autogenerate -m "descricao da alteracao"

# Aplica no banco sem perder os dados existentes
alembic upgrade head
```

### Outros comandos úteis

```bash
alembic current          # Versão atual do banco
alembic history          # Histórico de migrações
alembic downgrade -1     # Desfaz a última migração
```

> ✅ Com o Alembic, não é necessário recriar as tabelas manualmente nem perder dados ao alterar os modelos.

---

## 🧩 Modelos (`models.py`)

### `Categoria`

| Campo      | Tipo    | Obrigatório | Descrição                        |
|------------|---------|-------------|----------------------------------|
| `id`       | Integer | Sim (PK)    | Identificador único (autoincrement) |
| `nome`     | String  | Sim         | Nome da categoria                |
| `descricao`| String  | Não         | Descrição opcional               |
| `produtos` | Relação | —           | Produtos vinculados à categoria  |

### `Produto`

| Campo         | Tipo       | Obrigatório | Descrição                          |
|---------------|------------|-------------|-------------------------------------|
| `id`          | Integer    | Sim (PK)    | Identificador único (autoincrement) |
| `nome`        | String     | Sim         | Nome do produto                     |
| `preco`       | Numeric    | Sim         | Preço com 2 casas decimais          |
| `estoque`     | Integer    | Sim         | Quantidade em estoque               |
| `descricao`   | String     | Não         | Descrição ou especificações         |
| `categoria_id`| Integer    | Sim (FK)    | Referência à tabela `categorias`    |
| `categoria`   | Relação    | —           | Objeto da categoria vinculada       |

---

## 🛣️ Rotas (`main.py`)

### Páginas

| Método | Rota                    | Descrição                          |
|--------|-------------------------|------------------------------------|
| GET    | `/`                     | Painel de controle (Dashboard)     |
| GET    | `/categorias`           | Lista todas as categorias          |
| GET    | `/categorias/cadastro`  | Exibe formulário de nova categoria |
| GET    | `/produtos`             | Lista todos os produtos            |
| GET    | `/produtos/cadastro`    | Exibe formulário de novo produto   |

### Ações

| Método | Rota                          | Descrição                          |
|--------|-------------------------------|------------------------------------|
| POST   | `/categorias/salvar`          | Salva nova categoria no banco      |
| POST   | `/produtos/salvar`            | Salva novo produto no banco        |
| GET    | `/categorias/excluir/{id}`    | Exclui uma categoria pelo ID       |
| GET    | `/produtos/excluir/{id}`      | Exclui um produto pelo ID          |

> As rotas de exclusão usam `GET` com redirecionamento via `HTTP 303 See Other` após a operação.

---

## 🖥️ Templates (`templates/`)

### `index.html` — Dashboard
Página inicial com cards de acesso rápido para **Categorias** e **Produtos**, e um banner de configuração inicial.

### `categorias.html` — Listagem de Categorias
Tabela com `ID`, `Nome` e `Descrição` de cada categoria, com botão de exclusão com confirmação via `confirm()`.

### `cadastrar_categoria.html` — Nova Categoria
Formulário com os campos `nome` (obrigatório) e `descrição` (opcional). Envia via `POST` para `/categorias/salvar`.

### `produtos.html` — Listagem de Produtos
Tabela com `ID`, `Nome`, `Categoria`, `Preço`, `Estoque` e `Descrição` de cada produto, com botão de exclusão.

### `cadastrar_produto.html` — Novo Produto
Formulário com os campos `nome`, `categoria` (select dinâmico), `preço`, `descrição` (opcional). Envia via `POST` para `/produtos/salvar`.

---

## 🔗 Relacionamentos

```
Categoria (1) ───── (N) Produto
```

Cada produto pertence a **uma categoria**. Uma categoria pode ter **vários produtos**.  
O relacionamento é definido via `ForeignKey` no modelo `Produto` e `relationship()` em ambos os modelos.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia      | Uso                                      |
|-----------------|------------------------------------------|
| FastAPI         | Framework web e roteamento               |
| SQLAlchemy      | ORM para acesso ao banco de dados        |
| SQLite          | Banco de dados relacional local          |
| Jinja2          | Renderização de templates HTML           |
| Tailwind CSS    | Estilização da interface                 |
| Font Awesome    | Ícones da interface                      |
| python-multipart| Leitura de dados de formulários HTML     |
| Alembic         | Criação e versionamento de migrações     |

---

## 📌 Observações

- O campo `estoque` é salvo com valor padrão `0` caso não seja informado no formulário.
- Ao excluir uma categoria que possui produtos vinculados, pode ocorrer erro de integridade referencial dependendo da configuração do banco. Considere adicionar `cascade="all, delete"` no relacionamento futuramente.
- O módulo **Relatórios** está previsto na interface mas ainda não implementado.

---

© 2026 StockManager — Sistema de Gestão Interna