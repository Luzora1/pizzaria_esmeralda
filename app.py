from flask import Flask, render_template, jsonify, session, redirect, url_for, render_template, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

##########################
# atenção: O session é um dicionário que armazena os dados do usuário logado, ele é armazenado no navegador do usuário e é usado para manter o estado da sessão entre as requisições.
##########################


app = Flask(__name__)
app.secret_key = "sua_chave_secreta"


# "banco de dados"
usuarios = {'emailteste@email.com': {'nome': 'Eumesmo', 'senha': 'scrypt:32768:8:1$qz4eXywBRQIcyaTs$c6e561005157ca7f657f3f716f395eaea8a5ff9b36879cde0f22ec6e1a5422e17ac53c4ad123f02ac1b929cfc6d750c6e9024aa56c6c26b5fd142322f02c5e85', 'xp': 3000, 'esmeraldas': 50000, 'endereco': 'Rua teste, 123','email': 'emailteste@email.com'}}
admin = {'ADM-1': {'senha': 'scrypt:32768:8:1$qz4eXywBRQIcyaTs$c6e561005157ca7f657f3f716f395eaea8a5ff9b36879cde0f22ec6e1a5422e17ac53c4ad123f02ac1b929cfc6d750c6e9024aa56c6c26b5fd142322f02c5e85'}}
pedidos = {} 
motoboys = []
id_contador  = 1

@app.route('/loginRegister')
def loginRegister():
    return render_template('login.html')
    
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
    session['user'] = usuarios[email]
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    # Pegando os dados do form
    email = request.form['email']
    senha = request.form['senha']

    
    if email in usuarios and check_password_hash(usuarios[email]['senha'], senha): # verificando se o email existe e se a senha está correta
        # Se o login for bem-sucedido, armazene as informações do usuário na sessão
        session['user'] = usuarios[email]
        return redirect('/') # Redireciona para a página inicial
    else:
        return redirect('/loginRegister')



@app.route('/logout')
def logout():
    # Limpa a sessão do usuário
    session.pop('user', None)
    return redirect('/')



@app.route('/')
def home():

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
    return render_template('index.html', itens=itens, desconto=desconto, user=user, carrinho=session.get("carrinho", []))

@app.route('/processar', methods=['POST'])
def processar():
    if 'user' not in session:
        return jsonify({'status': 'ok', 'mensagem': 'Faça o login antes de fazer um pedido!'}), 200
    
    data = request.get_json()  # Obtém os dados do frontend
    precoTotal = data['precoTotal']  # preço total
    ingredientes_pedido = data['ingredientesPedido']  # lista de ingredientes
    nomesFiltrados = [grid['item'] for grid in ingredientes_pedido if grid['item'] is not None]

    pedido = {
        "ingredientes": nomesFiltrados,
        "preco":precoTotal
    }
    print("Dados recebidos do frontend:")
    print(pedido["ingredientes"])  
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
    if 'user' not in session:
        return jsonify({'status': 'ok', 'mensagem': 'Faça o login antes de fazer um pedido!'}), 200
    
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
    print("Entrou na rota de pagamento")
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

        
        # Adicionando o pedido à fila
        novo_pedido = Pedido(id_contador, pedido["pizzas"], pedido["endereco"], pedido["email"], pedido["status"], pedido["preco"])
        fila['contador'] += 1

        if fila['inicio'] is None:
            fila['inicio'] = novo_pedido
            fila['fim'] = novo_pedido
        else:
            fila['fim'].proximo = novo_pedido
            fila['fim'] = novo_pedido

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

    pedidosUser = {k: v for k, v in pedidos.items() if v['email'] == user["email"]}
    print(pedidosUser)
    return render_template("user.html", user=user, carrinho=session.get("carrinho", []), pedidosUser=pedidosUser)


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

@app.route('/cancelarPedido', methods=['POST'])
def cancelarPedido():
    idPedido = request.form["pedido_id"]
    user = session.get('user')

    # Verificando se o pedido existe
    if int(idPedido) in pedidos:
        del pedidos[int(idPedido)]  # Removendo o pedido do dicionário
        flash("Pedido cancelado com sucesso!", "success")
    else:
        flash("Pedido não encontrado.", "error")

    # Atualizando os pedidos do usuário após a exclusão
    pedidosUser = {k: v for k, v in pedidos.items() if v['email'] == user["email"]}

    return render_template("user.html", user=user, carrinho=session.get("carrinho", []), pedidosUser=pedidosUser)




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
        return redirect('/loginAdmin')  
    session.pop('liberar_adm')  

    if fila['inicio'] is None:
        return render_template('adm.html', pedidos=pedidos, motoboys=motoboys, pedido=None)
    return render_template('adm.html', pedidos=pedidos, motoboys=motoboys, pedido=fila['inicio'])

@app.route('/EnviarPedido', methods=['POST'])
def atualizarPedido():
    
    id = request.form['pedido_id']

    if request.form.get('motoboys'):
        motoboy = request.form['motoboys']
    else:
        motoboy = "noMotoboy"


    if motoboy == "noMotoboy":
        if fila['inicio'] is None:
            return render_template('adm.html', pedidos=pedidos, motoboys=motoboys, pedido='nada')
        return render_template('adm.html', pedidos=pedidos, motoboys=motoboys, pedido=fila['inicio'])

    print(pedidos)
    
    pedidos[int(id)]['status'] = "Enviado"
    pedidos[int(id)]['motoboy'] = motoboy      

    fila['inicio'] = fila['inicio'].proximo  
    if fila['inicio'] is None:
        fila['fim'] = None

    if fila['inicio'] is None:
        return render_template('adm.html', pedidos=pedidos, motoboys=motoboys, pedido=None)
    return render_template('adm.html', pedidos=pedidos, motoboys=motoboys, pedido=fila['inicio'])

@app.route('/adicionarMotoboy', methods=['POST'])
def adicionarMotoboy():
    
    nomeMotoboy = request.form["motoboy_nome"]

    if nomeMotoboy in motoboys:
            
        if fila['inicio'] is None:
            return render_template('adm.html', pedidos=pedidos, motoboys=motoboys, pedido=None)
        return render_template('adm.html', pedidos=pedidos, motoboys=motoboys, pedido=fila['inicio'])
    else:
        motoboys.append(nomeMotoboy) 

    
    if fila['inicio'] is None:
        return render_template('adm.html', pedidos=pedidos, motoboys=motoboys, pedido=None)
    return render_template('adm.html', pedidos=pedidos, motoboys=motoboys, pedido=fila['inicio'])


fila = {
    'inicio': None,
    'fim': None,	
    'contador': 0,
}

class Pedido:
    def __init__(self, id, pizzas, endereco, email, status, preco):  
        self.id = id
        self.pizzas = pizzas
        self.endereco = endereco
        self.email = email,
        self.data = str(date.today())
        self.status = status
        self.preco = preco
        self.motoboy = None
        self.proximo = None

if __name__ == '__main__':
    app.run(debug=True)
