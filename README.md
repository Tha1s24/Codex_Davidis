# 📜 Codex Davidis: Desafio do Rei

> **Status do Projeto:** 🟢 Concluído / Em Produção

O **Codex Davidis** é uma aplicação web interativa de gamificação focada na decifração de pergaminhos antigos (versículos bíblicos). O projeto integra um sistema completo de autenticação de usuários, níveis de progressão e uma lógica de criptografia dinâmica no backend.

---

## 🚀 Tecnologias Utilizadas

O projeto foi construído utilizando as melhores práticas de desenvolvimento fullstack:

* **Frontend:** HTML5, CSS3 (Design Responsivo), JavaScript (ES6+).
* **Backend:** Python 3, Flask (Framework Web).
* **Banco de Dados:** SQLite com SQLAlchemy (ORM).
* **Segurança:** * **Flask-Bcrypt:** Hashing de senhas.
* **Regex:** Validação complexa de credenciais.
* **CORS:** Gerenciamento de compartilhamento de recursos entre origens.



---

## 🛠️ Funcionalidades Principais

* **Sistema de Autenticação Robusto:**
* Registro de novos usuários com validação de senha (mínimo 6 caracteres, letras maiúsculas/minúsculas, números e símbolos).
* Login seguro com armazenamento de sessão local (`localStorage`).


* **Gamificação:**
* 5 níveis de desafios progressivos.
* Sistema de vidas (escudos) 🛡️: o jogador tem 5 chances por nível.
* Interface dinâmica que exibe o nome do "Escriba" logado.


* **Criptografia Dinâmica:**
* O servidor processa o texto original e gera um código numérico único baseado no nível atual do jogador.



---

## 📁 Estrutura do Projeto

```text
/projeto-davi
├── /backend
│   ├── app.py              # Ponto de entrada da aplicação
│   ├── auth.py             # Blueprint de autenticação
│   ├── database.py         # Configuração e inicialização do DB
│   ├── models.py           # Definição das tabelas do banco de dados
│   ├── cipher_logic.py     # Lógica de criptografia dos versículos
│   └── database.db         # Banco de dados SQLite
├── /frontend
│   ├── /css
│   │   └── style.css       # Estilização visual e animações
│   ├── /js
│   │   ├── auth.js         # Lógica de autenticação (fetch)
│   │   └── game.js         # Lógica do jogo e manipulação do DOM
│   ├── index.html          # Página de Login/Cadastro
│   └── game.html           # Interface principal do jogo
└── README.md

```

---

## 🔧 Como Executar o Projeto

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/codex-davidis.git

```


2. **Instale as dependências:**
```bash
pip install flask flask-sqlalchemy flask-bcrypt flask-cors

```


3. **Inicie o servidor Flask:**
```bash
python app.py

```


4. **Acesse o Frontend:**
Abra o arquivo `index.html` utilizando a extensão **Live Server** no VS Code para garantir que o gerenciamento de rotas funcione corretamente.

---

## 🛡️ Segurança Implementada

O projeto demonstra conhecimentos sólidos em segurança da informação para web:

* **Proteção de Dados:** As senhas nunca são salvas em texto puro, sendo transformadas em hashes criptográficos via `Bcrypt`.
* **Validação de Input:** O sistema impede o cadastro de senhas fracas tanto no lado do cliente (JS) quanto no servidor (Python) utilizando expressões regulares.
* **Arquitetura:** O uso de **Blueprints** no Flask garante a modularidade e evita vazamento de escopo entre rotas.

---

## ✒️ Autor

Desenvolvido por **Seu Nome** – [Seu LinkedIn](https://www.google.com/search?q=https://www.linkedin.com/in/seu-perfil) | [Seu GitHub](https://www.google.com/search?q=https://github.com/seu-usuario)

---

