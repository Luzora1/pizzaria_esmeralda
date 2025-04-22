from flask import Flask, render_template, jsonify, session, redirect, url_for, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = "sua_chave_secreta"


# Banco falso
usuarios = {'emailteste@email.com': {'nome': 'ADM', 'senha': 'scrypt:32768:8:1$qz4eXywBRQIcyaTs$c6e561005157ca7f657f3f716f395eaea8a5ff9b36879cde0f22ec6e1a5422e17ac53c4ad123f02ac1b929cfc6d750c6e9024aa56c6c26b5fd142322f02c5e85', 'xp': 3000, 'esmeraldas': 2000000}}

@app.route('/')
def loginRegister():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']

    if email in usuarios and check_password_hash(usuarios[email]['senha'], senha): # faz uma busca no 'BD falso'
        session['user'] = usuarios[email]
        return redirect('/home')
    else:
        return redirect('/')
    
@app.route('/register', methods=['POST'])
def register():
    nome = request.form['nome'] # pegando do form
    email = request.form['email'] # pegando do form
    senha = generate_password_hash(request.form['senha']) # pegando do form e criptografando
    xp = 0 # iniciando zerado
    esmeraldas = 0 # iniciando zerado 

    if email in usuarios:
        return "Usuário já existe"

    usuarios[email] = {'nome': nome, 'senha': senha, 'xp': xp, 'esmeraldas': esmeraldas} # criando o user e adicionando no 'BD falso'
    print(usuarios)
    return redirect('/')




@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')



@app.route('/home')
def home():


    user = session.get('user')

    level = user["xp"] // 100

    desconto = 0

    if level >=5:
        desconto = 0.05

    if level >=15:
        desconto = 0.15

    if level >=30:
        desconto = 0.30

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
    return render_template('index.html', itens=itens, desconto=desconto, user=user)

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


@app.route('/adicionar-carrinho', methods=['POST'])
def adicionar_carrinho():
    data = request.get_json()
    nome_pizza = data.get("pizza")

    if "carrinho" not in session:
        session["carrinho"] = []

    session["carrinho"].append(nome_pizza)
    session.modified = True  # Para garantir que o Flask detecte a modificação

    print(session["carrinho"])

    return jsonify({"mensagem": f"{nome_pizza} adicionada ao carrinho!"})





if __name__ == '__main__':
    app.run(debug=True)
