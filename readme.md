# Fazendo uma API Do Zero em Python com Anotações
---

## 1° Etapa - Configurando Ambiente da API

*1ª - Criar a pasta `app.py` no vscode*
-
COMANDO: (pelo terminal opcional)

-> `touch app.py`

*2ª - Abrir o terminal e criar um ambiente virtual*
-
COMANDO:

-> `python -m venv venv`

*3ª - O ambiente será criado e mostrará uma pasta venv, e irá precisar ativar esse ambiente*
-
COMANDO:

-> `source venv/Scripts/activate`

OBS: **Lembrando que quando querer fechar o vscode sempre desativar usando**

COMANDO: 

-> `deactivate`

*4ª - Baixar o flask no terminal*
-
COMANDO:

-> `pip install Flask`

*5ª - No terminal colocar o requirements.txt (opcional)*
-   
- O requiments é opcional mas seria interessante colocar em caso de querer compartilhar seu código ou pra quando trabalhar em grupo para saberem as versões dos pacotes

COMANDO:

-> `pip freeze > requirements.txt`

*6ª - Para colocar para rodar pelo navegador colocar no terminal o comando*

COMANDO:

-> `python app.py`

---
---

## 2° Etapa - Iniciando a importação do Flask, SQLite3 e a Contrução do banco de dados e tabela 

```python
# Importando a classe Flask para criar nossa aplicação
from flask import Flask

# Importar o módulo sqlLite3 para manipulação do banco de dados SQLite 
import sqlite3

# Criar uma instância do Flask e armazenamos na variável que foi criado o "app"
app = Flask(__name__)

# Criando uma rota para o endpoint "/"
# OBS: uma rota só com "/" será a rota inicial de quando acessar no navegador 
@app.route("/")

#Criar uma função para executar o que estará dentro dessa rota (endpoint)
def inicial():
    return "<h1> Sistema de livros VAI NA WEB</h1>"

# Função para inicializar o banco de dados SQLite

def init_db():
    
    with sqlite3.connect("database.db") as conn:
        conn.execute(
            
            # #Criar uma tabela da mesma forma que no banco de dados
            """
                CREATE TABLE IF NOT EXISTS LIVROS(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    image_url TEXT NOT NULL
                ) 
            """
        )

# É chamada a função para inicializar o banco de dados quando o programa for executado
init_db()

if __name__ == "__main__":
    # Inicia o servidor Flask no modo de depuração (nesse modo a API responde automaticamente a qualquer atualização que fizer no código)
    app.run(debug = True)

```

---
---
## 3° Etapa - Criação do POST e Enviando Dados para API

```python

# ------------------------- MUDANÇAS -------------------------
# # Funcionalidades do Flask = request e jsonify 
from flask import Flask, request, jsonify

import sqlite3

app = Flask(__name__)

@app.route("/")

def inicial():
    return "<h1> Sistema de livros VAI NA WEB</h1>"

def init_db():
    with sqlite3.connect("database.db") as conn:

        conn.execute(

            """
                CREATE TABLE IF NOT EXISTS LIVROS(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    image_url TEXT NOT NULL
                ) 
            """
        )

init_db()

# ------------------------- MUDANÇAS -------------------------

# Criando uma rota "/doar" que recebe dados de um novo livro e os armazena no banco de dados
@app.route("/doar", methods=["POST"])
def doar():

    # Captura os dados enviados pelo usuário na requisição HTTP
    # Esses dados devem estar no formato JSON e contêm informações do livro que será cadastrado  
    dados = request.get_json()

    #Extrair as informações do JSON recebido
    # O método .get() obtém o valor associado a cada chave do dicionário JSON
    titulo = dados.get("titulo")
    categoria = dados.get("categoria")
    autor = dados.get("autor")
    image_url = dados.get("image_url")
    
    # Verificando se todos os campos obrigatórios foram preenchidos
    # Se algum campo estiver vazio, retornamos um erro 400(Bas Request), informando ao usuário que os campos são obrigatórios
    if not titulo or not categoria or not autor or not image_url:
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

# Conectamos ao banco de dados SQLite 
# O comando "with" garante que a conexão será fechada corretamente após a execução do bloco
    with sqlite3.connect("database.db") as conn:
        
        # Inserimos os dados do novo livro na tabela "LIVROS"
        # Essa query SQL adiciona os valores de título, categoria, autor e imagem_url na tabela
        
        conn.execute(
            f"""
                INSERT INTO LIVROS (titulo, categoria, autor, image_url) VALUES ("{titulo}", "{categoria}", "{autor}", "{image_url}")
            """
        )
        
        # Confirma a inserção dos dados no banco de dados para que eles sejam armazenados permanentemente
        conn.commit()
        
        # Retornar uma respota em formato JSON confirmando que o livro foi cadastrado com sucesso 
        
        # `jsonify()` transforma um dicionário Python em JSON válido para ser retornado na resposta HTTP
        # O código HTTP 201 indica que um novo recurso (livro) foi criado com sucesso
        return jsonify({"mensagem": "Livro cadastrado com sucesso"}), 201

if __name__ == "__main__":

    app.run(debug = True)
```

---
## 4° Etapa - API Completa com POST e GET

```python

# request: permite capturar os dados enviados pelo cliente
#jsonify: é usado para transformar os dados em formato JSON para resposta
from flask import Flask, request, jsonify
# ------------------------- MUDANÇAS -------------------------
from flask_cors import CORS

import sqlite3

app = Flask(__name__)
# ------------------------- MUDANÇAS -------------------------
CORS(app)

@app.route("/")

def inicial():
    return "<h1> Sistema de livros VAI NA WEB</h1>"

def init_db():

    with sqlite3.connect("database.db") as conn:

        conn.execute(

            """
                CREATE TABLE IF NOT EXISTS LIVROS(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    image_url TEXT NOT NULL
                ) 
            """
        )

init_db()

@app.route("/doar", methods=["POST"])
def doar():
  
    dados = request.get_json()

    titulo = dados.get("titulo")
    categoria = dados.get("categoria")
    autor = dados.get("autor")
    image_url = dados.get("image_url")

    if not titulo or not categoria or not autor or not image_url:
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    with sqlite3.connect("database.db") as conn:

        conn.execute(
            f"""
                INSERT INTO LIVROS (titulo, categoria, autor, image_url) VALUES ("{titulo}", "{categoria}", "{autor}", "{image_url}")
            """
        )

        conn.commit()
        
        return jsonify({"mensagem": "Livro cadastrado com sucesso"}), 201

# ------------------------- MUDANÇAS -------------------------
# Criando uma endpoint para listar os livros cadastrados no banco de dados
# Esse endpoint será acessado através de uma requisição HTTP do tipo "GET"

@app.route("/livros", methods=["GET"]) 

def listar_livros():
    with sqlite3.connect("database.db") as conn:
        
        #Executando um comando SQL para buscar todos os livros na tabela LIVROS
        livros = conn.execute("SELECT * FROM LIVROS").fetchall()
        
        #Criando uma lista vazia para armazenar os livros em formato de dicionário
        livros_formatados = []
        
        # Percorre cada item da lista retornada do banco de dados
        for item in livros:
            dicionario_livros = {
                "id": item[0], # Pegandp o ID livro 
                "titulo": item[1], # Pegando o título do livro
                "categoria": item[2], # Pegando a categoria do livro
                "autor": item[3], # Pegando o autor do livro
                "image_url": item[4] # Pegando a imagem do livro
            }
            
            # Adiciona esse dicionário à lista de livros formatados
            livros_formatados.append(dicionario_livros)
    
    # Retornando a lista de livros no formato JSON com o código de status 200 (OK)
    return jsonify(livros_formatados), 200

if __name__ == "__main__":    
    app.run(debug = True)

```

## 5° Etapa - Deploy da API 

### Render para colocar API no ar
- Acesse o [link do Render](https://dashboard.render.com/)

---
### Database Cliente uma extensão do vscode para poder manipular o banco de dados
---

OBS: Antes de fazer o deploy no Render, certificar que o ambiente virtual esteja ativado

1ª Adicione seu código no Github 
-

2ª Ativar o ambiente virtual
-

`source venv/Scripts/activate`

3ª Instalar o flask cors
- 

- **Flask-CORS** é uma extensão para o framework Flask que habilita o CORS nas rotas

- **CORS** é um mecanismo de segurança que os navegadores usam para restringir requisições feitas por scripts entre sites diferentes.

`pip install flask-cors`

4ª Instalar o gunicorn 
-

- Gunicorn é um servidor HTTP para aplicações Python, ele é muito usado para rodar aplicações Flask, Django e outras em produção. 

`pip install gunicorn`

5ª Adicionar o requirements
-

- Em caso de não ter adicionado no início

    `pip freeze > requirements.txt`

#### Depois só atualizar no Github e pode fazer o deploy no render.



