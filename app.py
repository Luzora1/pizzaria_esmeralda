from flask import Flask, render_template, jsonify, session, redirect, url_for, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

##########################
# atenção: O session é um dicionário que armazena os dados do usuário logado, ele é armazenado no navegador do usuário e é usado para manter o estado da sessão entre as requisições.
##########################


app = Flask(__name__)
app.secret_key = "sua_chave_secreta"


# Banco falso esse aqui, só para teste
usuarios = {'emailteste@email.com': {'nome': 'Eumesmo', 'senha': 'scrypt:32768:8:1$qz4eXywBRQIcyaTs$c6e561005157ca7f657f3f716f395eaea8a5ff9b36879cde0f22ec6e1a5422e17ac53c4ad123f02ac1b929cfc6d750c6e9024aa56c6c26b5fd142322f02c5e85', 'xp': 3000, 'esmeraldas': 50, 'endereco': 'Rua teste, 123','email': 'emailteste@email.com'}}
admin = {'ADM-1': {'senha': 'scrypt:32768:8:1$qz4eXywBRQIcyaTs$c6e561005157ca7f657f3f716f395eaea8a5ff9b36879cde0f22ec6e1a5422e17ac53c4ad123f02ac1b929cfc6d750c6e9024aa56c6c26b5fd142322f02c5e85'}}
pedidos = {} 
id_contador  = 1

@app.route('/')
def loginRegister():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    # Pegando os dados do form
    email = request.form['email']
    senha = request.form['senha']

    # aqui você pode fazer a verificação com o banco de dados real, esse só está sendo usado pq nao temos um banco de dados real
    if email in usuarios and check_password_hash(usuarios[email]['senha'], senha): # verificando se o email existe e se a senha está correta
        # Se o login for bem-sucedido, armazene as informações do usuário na sessão
        session['user'] = usuarios[email]
        return redirect('/home') # Redireciona para a página inicial ou outra página após o login bem-sucedido
    else:
        return redirect('/')
    
@app.route('/register', methods=['POST'])
def register():
    # Pegando os dados do form
    nome = request.form['nome'] 
    email = request.form['email'] 
    endereco = request.form['endereco'] 
    senha = generate_password_hash(request.form['senha']) # pegando do form e criptografando
    xp = 0 # iniciando zerado
    esmeraldas = 0 # iniciando zerado 

    # Verificando se o email já existe no "banco de dados", fazer isso com o banco de dados real
    if email in usuarios:
        return "Usuário já existe"
    
    # Se o email não existir, armazene as informações do usuário na sessão
    usuarios[email] = {'nome': nome, 'senha': senha, 'xp': xp, 'esmeraldas': esmeraldas, 'endereco': endereco, 'email': email} # criando o user e adicionando no 'BD falso'
    print(usuarios)
    return redirect('/')




@app.route('/logout')
def logout():
    # Limpa a sessão do usuário
    session.pop('user', None)
    return redirect('/')



@app.route('/home')
def home():

    if 'user' not in session:
        return redirect('/')
    
    user = session.get('user')

    level = 0
    if user and 'xp' in user:
        level = user['xp'] // 100
        
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
        if "carrinho" not in session:
            session["carrinho"] = []

        pizzaNome = 'Pizza craftada - ' + ", ".join(pedido["ingredientes"])
        pizza = [pizzaNome, pedido["preco"]]
        session["carrinho"].append(pizza)
        session.modified = True 

        return jsonify({'status': 'ok', 'mensagem': 'Pizza craftada! Siga para o carrinho ou continue comprando!'}), 200


@app.route('/adicionar-carrinho', methods=['POST'])
def adicionar_carrinho():
    data = request.get_json()
    nomePizza = data.get("pizza")
    precoPizza = data.get("preco")

    if "carrinho" not in session:
        session["carrinho"] = []
    
    pizza = [nomePizza, precoPizza]

    session["carrinho"].append(pizza)
    session.modified = True  

    print(session["carrinho"])

    return jsonify({"mensagem": f"{nomePizza} adicionada ao carrinho!"})


@app.route('/carrinho')
def carrinho():
    if 'user' not in session:
        return redirect('/')
    
    user = session.get('user')
    if "carrinho" not in session:
        session["carrinho"] = []
    carrinho = session["carrinho"]
    total = sum([i[1] for i in carrinho])

    return render_template("carrinho.html", carrinho=carrinho, total=total, user=user)


@app.route("/deletar-item", methods=["POST"])
def deletar_item():
    data = request.get_json()
    nome_pizza = data.get("pizza")
    user = session.get('user')
    if "carrinho" not in session:
        session["carrinho"] = []
    carrinho = session["carrinho"]

    # Exemplo de como deletar do carrinho (suponha que seja uma lista global ou de sessão)
    for i in carrinho:
        if i[0] == nome_pizza:
            carrinho.remove(i)
            break
    

    session["carrinho"] = carrinho
    
    total = sum([i[1] for i in carrinho])

    print(session["carrinho"])
    
    return jsonify({"mensagem": f"{nome_pizza} removida do carrinho."})


@app.route('/pagar', methods=['POST'])
def pagar():
    global id_contador  # Para acessar e modificar a variável global
    data = request.get_json()
    total = data.get('total')

    if 'user' in session and session['user']['esmeraldas'] >= total:
        session['user']['esmeraldas'] -= total

        carrinho = session.get("carrinho", [])
        # criando o pedido com os dados do carrinho e do usuario
        pedido = {
            "pizzas": [i[0] for i in carrinho],
            "preco": total,
            "endereco": session['user']['endereco'],
            "email": session['user']['email'],
            "data": str(date.today()),
            "status": "Pendente"
        }
        # Adicionando o pedido ao "banco de dados" 
        # Aqui você pode adicionar o pedido ao banco de dados real, esse só está sendo usado pq nao temos um banco de dados real
        pedidos[id_contador] = pedido       
        id_contador += 1 
        print(pedidos)

        # Limpa o carrinho após o pagamento
        session["carrinho"] = []
        # Atualiza o XP do usuário
        session['user']['xp'] += 55
        session.modified = True

        return jsonify({
            'mensagem': 'Pagamento realizado com sucesso!',
            'novo_saldo': session['user']['esmeraldas']
        })
    else:
        return jsonify({'mensagem': 'Saldo insuficiente ou usuário não logado.'}), 400



@app.route('/user')
def user():
    if 'user' not in session:
        return redirect('/')
    
    user = session.get('user')

    return render_template("user.html", user=user)


@app.route('/userEdit', methods=['POST'])
def userEdit():
    # Pegando os dados do form
    nome = request.form['nome'] 
    email = request.form['email'] 
    endereco = request.form['endereco']
    
    user = session.get('user')
    # Atualizando o user no session, aqui voce tem que pegar as modificações e atualizar no banco de dados real, esse só está sendo usado pq nao temos um banco de dados real
    session['user'] = {'nome': nome, 'senha': user['senha'], 'xp': user['xp'], 'esmeraldas': user['esmeraldas'], 'endereco': endereco, 'email': email} 
    session.modified = True  
    user = session.get('user')

    return render_template("user.html", user=user)


@app.route('/shop')
def shop():
    if 'user' not in session:
        return redirect('/')
    
    user = session.get('user')

    return render_template("shop.html", user=user)


@app.route('/buyEsmeraldas', methods=['POST'])
def buyEsmeraldas():
    # Pegando os dados do form
    quantidade = int(request.form['quantidade'])
    user = session.get('user')
    # Atualizando o user no session, aqui voce tem que pegar as modificações e atualizar no banco de dados real, esse só está sendo usado pq nao temos um banco de dados real
    session['user']['esmeraldas'] += quantidade 
    session['user']['xp'] += quantidade // 5 
    session.modified = True  
    user = session.get('user')

    return render_template("shop.html", user=user)


@app.route('/loginAdmin')
def loginAdmin():
    return render_template('loginAdmin.html')


@app.route('/loginAdmAuthenticator', methods=['POST'])
def loginAdmAuthenticator():
    # Pegando os dados do form
    nome = request.form['nome']
    senha = request.form['senha']

    # aqui você pode fazer a verificação com o banco de dados real, esse só está sendo usado pq nao temos um banco de dados real
    if nome in admin and check_password_hash(admin[nome]['senha'], senha): # verificando se o email existe e se a senha está correta
        session['liberar_adm'] = True
        return redirect('/adm') # Redireciona para a página inicial ou outra página após o login bem-sucedido
    else:
        return redirect('/loginAdmin')
    
@app.route('/logoutAdmin', methods=['POST'])
def logoutAdmin():  
    return redirect('/loginAdmin')

@app.route('/adm')
def adm():
    if not session.get('liberar_adm'):
        return redirect('/loginAdmin')  # Ou retornar 403
    session.pop('liberar_adm')  # remove o acesso após uso
    return render_template('adm.html', pedidos=pedidos)

@app.route('/atualizarPedido', methods=['POST'])
def atualizarPedido():
    
    id = request.form['pedido_id']
    pedidoType = request.form['pedido_type']

    if pedidoType == "upgrade":
        for pedido in pedidos:
            if pedido == int(id):
                print(pedido)
                # Verificando o status atual e atualizando ou removendo conforme necessário
                if pedidos[pedido]["status"] == "Pendente":
                    pedidos[pedido]["status"] = "Enviado"
                elif pedidos[pedido]["status"] == "Enviado":
                    pedidos[pedido]["status"] = "Finalizado"
                elif pedidos[pedido]["status"] == "Finalizado":
                    # Deletando o pedido do dicionário
                    del pedidos[pedido]
                else:
                    print("Status inválido", pedidos[pedido]["status"])
                break
    elif pedidoType == "downgrade":
        for pedido in pedidos:
            if pedido == int(id):
                print(pedido)
                # Verificando o status atual e atualizando ou removendo conforme necessário
                if pedidos[pedido]["status"] == "Enviado":
                    pedidos[pedido]["status"] = "Pendente"
                elif pedidos[pedido]["status"] == "Finalizado":
                    pedidos[pedido]["status"] = "Enviado"
                else:
                    print("Status inválido", pedidos[pedido]["status"])
                break

    return render_template('adm.html', pedidos=pedidos)

if __name__ == '__main__':
    app.run(debug=True)
