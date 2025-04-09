# Importando a classe Flask para criar nossa aplicação
# Funcionalidades do Flask = request e jsonify

# request: permite capturar os dados enviados pelo cliente
#jsonify: é usado para transformar os dados em formato JSON para resposta
from flask import Flask, request, jsonify

from flask_cors import CORS

# Importar o módulo sqlLite3 para manipulação do banco de dados SQLite 
import sqlite3

# Criar uma instância do Flask e armazenamos na variável que foi criado o "app"
app = Flask(__name__)
CORS(app)

# Criando uma rota para o endpoint "/"
# Quando acessarmos http://127.0.0.1:5000/, a função abaixo será executada
# OBS: uma rota só com "/" será a rota inicial de quando acessar no navegador 
@app.route("/")

#Criar uma função para executar o que estará dentro dessa rota (endpoint)
def inicial():
    return "<h1> Sistema de livros VAI NA WEB</h1>"

# Função para inicializar o banco de dados SQLite

def init_db():

    # Cria uma conexão com o banco de dados chamado 'database.db'
    # Se por acaso não criar o banco de dados ele irá ser criado automaticamente
    
    # Para conectar o banco de dados SQLite é usado o with garantindo que a conexão seja fechada corretamente após a execução
    
    with sqlite3.connect("database.db") as conn:

        #Executa um comando SQL para criar a tabela LIVROS, caso ele ainda não exista
        conn.execute(
            #Criar uma tabela da mesma forma que no banco de dados 
            
            # PRIMARY KEY = um identificador para cada livro
            # AUTOINCREMENT = gera o id automaticamente
            # NOT NULL = Para que a coluna seja armazenada automaticamente
            
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

        # A execução desse comando cria a tabela caso ela ainda não exista, garantindo que a estrutura de banco esteja configurada

# É chamada a função para inicializar o banco de dados quando o programa for executado
init_db()

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

# Fazer uma verificação se o script está sendo executado diretamente e não importado como módulo
if __name__ == "__main__":
    
    # Inicia o servidor Flask no modo de depuração (nesse modo a API responde automaticamente a qualquer atualização que fizer no código)
    app.run(debug = True)

