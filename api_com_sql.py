import pyodbc 
from flask import Flask, jsonify, request
import json 

#inicia app flask
app = Flask(__name__)

dados_conexao = (
    "Driver={SQL Server Native Client RDA 11.0};"
    "Server=DESKTOP-1698A6Q\SQLEXPRESS;"
    "Database=VendasProdutos;"
  
    "Trusted_connection=YES;"
)

conexao = pyodbc.connect(dados_conexao)
cursor = conexao.cursor()

cursor.commit()

teste_q = cursor.execute('SELECT * FROM Vendas')
teste_q = teste_q.fetchall()
for x in teste_q:
    for y in x:
        print(y)




@app.route('/produtos', methods = ['GET'])
def obter_livros():
    dados_get = cursor.execute('SELECT * FROM Vendas')
    dados_get = dados_get.fetchall()
    data = []
    for x in dados_get:
        data.append({
            'id': x[0],
            'cliente': x[1],
            'produto': x[2]
        
        })
    return jsonify(message = "Esses são os dados solicitados", data = data)

@app.route('/produtos', methods = ['POST'])
def adicionar_produto():
    novo_prod = request.get_json(force=True)
    id_cliente = novo_prod['id']
    cliente = novo_prod['cliente']
    produto = novo_prod['produto']
    print("chegou aqui o código")
    cursor.execute(f"INSERT INTO Vendas (id, cliente, produto) VALUES ({id_cliente}, '{cliente}', '{produto}')")
    cursor.commit()
    return jsonify(
        message = "Produto cadastrado com sucesso"
    )

@app.route('/produtos/<id_linha>', methods = ['DELETE'])
def deletar_dado(id_linha):
    db = cursor.execute(f"DELETE FROM Vendas WHERE id=?", (id_linha))
    cursor.commit()
    return jsonify(message = "Item deletado")



#roda o app  
app.run(debug=True)



