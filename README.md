# 🍽️ Sabor & Arte — Sistema de Gerenciamento de Restaurante

Sistema de gerenciamento de restaurante desenvolvido em Python, com arquitetura **MVC (Model-View-Controller)**, banco de dados **SQLite** e aplicação de princípios de **Orientação a Objetos** e **SOLID**.

> 📚 Projeto desenvolvido como Atividade de Portfólio da disciplina de **Desenvolvimento Orientado a Objetos e Padrões de Projeto** — Curso de Análise e Desenvolvimento de Sistemas (ADS).

---

## 🚀 Funcionalidades

- ✅ Cadastro e listagem de garçons (com matrícula única)
- ✅ Cadastro e listagem de produtos do cardápio (nome, preço, categoria)
- ✅ Abertura de pedidos por mesa, com vínculo a um garçom responsável
- ✅ Adição de múltiplos produtos a um pedido
- ✅ Verificação automática de mesa já ocupada
- ✅ Exibição de pedidos com produtos e total calculado
- ✅ Persistência de dados em banco SQLite
- ✅ Tratamento de exceções em múltiplas camadas

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| Python 3.12+ | Linguagem principal |
| SQLite | Banco de dados relacional |
| Módulo `sqlite3` | Interface nativa Python com SQLite |

---

## 🏗️ Arquitetura MVC

O projeto segue o padrão **Model-View-Controller**, com separação clara de responsabilidades:

```
Portifolio_python/
├── models/
│   ├── garcom.py         # Entidade Garçom
│   ├── produto.py        # Entidade Produto
│   ├── pedido.py         # Entidade Pedido (agrega Produtos)
│   ├── restaurante.py    # Entidade central (agrega Garçons e Pedidos)
│   └── __init__.py
├── controllers/
│   └── restaurant_controller.py  # Lógica de negócio e acesso ao banco
├── views/
│   └── restaurant_view.py        # Interface com o usuário (terminal)
├── main.py               # Ponto de entrada da aplicação
└── banco.sql             # Schema do banco de dados
```

- **Model:** representa as entidades do domínio, sem conhecimento da interface ou do banco
- **Controller:** gerencia a persistência (SQLite) e coordena as entidades
- **View:** cuida exclusivamente da entrada e saída pelo terminal

---

## 🔗 Relacionamentos entre Classes

| Relação | Classes | Tipo |
|---|---|---|
| Restaurante → Garçom | Um restaurante agrega vários garçons | **Agregação** |
| Restaurante → Pedido | Pedidos pertencem ao restaurante | **Composição** |
| Pedido → Produto | Um pedido agrega vários produtos | **Agregação** |
| Pedido → Garçom | Referência por `id_garcom` | **Associação** |

---

## ▶️ Como Executar

### Pré-requisitos

- Python 3.12 ou superior
- Sem dependências externas — apenas biblioteca padrão do Python

### Passos

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/sabor-e-arte.git
cd sabor-e-arte

# Execute o sistema
python main.py
```

O banco de dados `banco.db` é criado automaticamente na primeira execução.

---

## 💡 Conceitos Aplicados

- **Encapsulamento:** atributos privados com `__` (name mangling) e acesso via getters/setters
- **Polimorfismo:** método `__str__` implementado em todas as classes de modelo
- **Princípios SOLID:** responsabilidade única por classe, injeção de dependência via construtor
- **Convenções PEP 8:** PascalCase para classes, snake_case para métodos e variáveis
- **Tratamento de exceções:** `try/except` em múltiplas camadas (view e controller)
- **Arquitetura MVC:** separação total entre dados, lógica e interface

---

## 📋 Contexto Acadêmico

Este projeto foi desenvolvido no segundo semestre do curso de **Análise e Desenvolvimento de Sistemas**, como atividade de portfólio da disciplina de Desenvolvimento Orientado a Objetos e Padrões de Projeto.

O tema escolhido foi o Sistema de Restaurante, com o cenário fictício **Sabor & Arte**. O objetivo foi aplicar na prática os conceitos de OOP, MVC e SOLID estudados ao longo da disciplina.

---

## 📁 Entregáveis Acadêmicos

Além do código-fonte, o projeto inclui:

- 📄 Documentação Técnica Acadêmica (ABNT)
- 📊 Diagrama de Classes UML (PDF)

---

*Desenvolvido por [Seu Nome] — ADS, Campo Grande - MS*
