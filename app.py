from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():

    logado = True

    user = {
        'nome' : "Eumesmo",
        'xp' : 9999,
        'esmeraldas' : 20000
    }

    itens = [
    {"nome": "Calabresa", "preco": 2.50},
    {"nome": "Presunto", "preco": 2.00},
    {"nome": "Frango", "preco": 2.50},
    {"nome": "Mussarela", "preco": 2.00},
    {"nome": "Pepperoni", "preco": 3.00},
    {"nome": "Tomate", "preco": 1.00},
    {"nome": "Cebola", "preco": 1.00},
    {"nome": "Azeitona", "preco": 1.50},
    {"nome": "Milho", "preco": 1.00},
    {"nome": "Bacon", "preco": 3.00},
    {"nome": "Champignon", "preco": 2.50},
    {"nome": "Catupiry", "preco": 2.50},
    {"nome": "Rúcula", "preco": 1.50},
    {"nome": "Parmesão", "preco": 2.00},
    {"nome": "Provolone", "preco": 2.50},
    {"nome": "Pimentão", "preco": 1.00},
    {"nome": "Ovo de cobra", "preco": 10.00},  
    {"nome": "Gorgonzola", "preco": 3.50},
    {"nome": "Manjericão", "preco": 0.75},
    {"nome": "Orégano", "preco": 0.50}
]
    return render_template('index.html', itens=itens, logado=logado, user=user)

@app.route('/processar', methods=['POST'])
def processar():
    data = request.get_json()  # Obtém os dados do frontend
    precoTotal = data['precoTotal']  # Acessa o preço total
    ingredientes_pedido = data['ingredientesPedido']  # Acessa a lista de ingredientes
    nomesFiltrados = [celula['item'] for celula in ingredientes_pedido if celula['item'] is not None]

    pedido = {
        "ingredientes": nomesFiltrados,
        "preco":precoTotal
    }
    print("Dados recebidos do frontend:")
    print(pedido["ingredientes"])  # Aqui você pode fazer o que quiser com os dados
    print(pedido["preco"])
    if not ingredientes_pedido:
        return jsonify({'status': 'ok', 'mensagem': 'Adicione ao menos um igrediente!'}), 200
    else:
        print(f'enviando o pedido{nomesFiltrados} para o BD')
        return jsonify({'status': 'ok', 'mensagem': 'Pedido recebidos com sucesso! Sua pizza já está sendo preparada!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
