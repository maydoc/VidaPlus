from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from datetime import datetime, timedelta
import bcrypt
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configurações
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///vidaplus.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'chave-secreta-padrao')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Modelos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # paciente, medico, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(200))
    prontuarios = db.relationship('Prontuario', backref='paciente', lazy=True)

class Medico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    crm = db.Column(db.String(20), unique=True, nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    agenda = db.relationship('Agenda', backref='medico', lazy=True)

class Consulta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medico.id'), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # presencial, telemedicina
    status = db.Column(db.String(20), nullable=False)  # agendada, realizada, cancelada
    prontuario = db.relationship('Prontuario', backref='consulta', lazy=True)

class Prontuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    consulta_id = db.Column(db.Integer, db.ForeignKey('consulta.id'), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    prescricao = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Agenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medico_id = db.Column(db.Integer, db.ForeignKey('medico.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)
    disponivel = db.Column(db.Boolean, default=True)

# Rotas de autenticação
@app.route('/api/auth/registro', methods=['POST'])
def registro():
    dados = request.get_json()
    
    if Usuario.query.filter_by(email=dados['email']).first():
        return jsonify({'erro': 'Email já cadastrado'}), 400
    
    senha_hash = bcrypt.hashpw(dados['senha'].encode('utf-8'), bcrypt.gensalt())
    
    novo_usuario = Usuario(
        nome=dados['nome'],
        email=dados['email'],
        senha=senha_hash.decode('utf-8'),
        tipo=dados['tipo']
    )
    
    db.session.add(novo_usuario)
    db.session.commit()
    
    return jsonify({'mensagem': 'Usuário registrado com sucesso'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    dados = request.get_json()
    usuario = Usuario.query.filter_by(email=dados['email']).first()
    
    if not usuario or not bcrypt.checkpw(dados['senha'].encode('utf-8'), usuario.senha.encode('utf-8')):
        return jsonify({'erro': 'Credenciais inválidas'}), 401
    
    access_token = create_access_token(identity=usuario.id)
    return jsonify({'token': access_token}), 200

# Rotas de pacientes
@app.route('/api/pacientes', methods=['GET'])
@jwt_required()
def listar_pacientes():
    pacientes = Paciente.query.all()
    return jsonify([{
        'id': p.id,
        'usuario_id': p.usuario_id,
        'cpf': p.cpf,
        'data_nascimento': p.data_nascimento.strftime('%Y-%m-%d'),
        'telefone': p.telefone,
        'endereco': p.endereco
    } for p in pacientes]), 200

@app.route('/api/pacientes/<int:id>', methods=['GET'])
@jwt_required()
def obter_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    return jsonify({
        'id': paciente.id,
        'usuario_id': paciente.usuario_id,
        'cpf': paciente.cpf,
        'data_nascimento': paciente.data_nascimento.strftime('%Y-%m-%d'),
        'telefone': paciente.telefone,
        'endereco': paciente.endereco
    }), 200

@app.route('/api/pacientes', methods=['POST'])
@jwt_required()
def criar_paciente():
    dados = request.get_json()
    usuario_id = get_jwt_identity()
    
    novo_paciente = Paciente(
        usuario_id=usuario_id,
        cpf=dados['cpf'],
        data_nascimento=datetime.strptime(dados['data_nascimento'], '%Y-%m-%d').date(),
        telefone=dados.get('telefone'),
        endereco=dados.get('endereco')
    )
    
    db.session.add(novo_paciente)
    db.session.commit()
    
    return jsonify({'mensagem': 'Paciente cadastrado com sucesso'}), 201

@app.route('/api/pacientes/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    dados = request.get_json()
    
    if 'cpf' in dados:
        paciente.cpf = dados['cpf']
    if 'data_nascimento' in dados:
        paciente.data_nascimento = datetime.strptime(dados['data_nascimento'], '%Y-%m-%d').date()
    if 'telefone' in dados:
        paciente.telefone = dados['telefone']
    if 'endereco' in dados:
        paciente.endereco = dados['endereco']
    
    db.session.commit()
    return jsonify({'mensagem': 'Paciente atualizado com sucesso'}), 200

@app.route('/api/pacientes/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    return jsonify({'mensagem': 'Paciente removido com sucesso'}), 200

# Rotas de consultas
@app.route('/api/consultas', methods=['GET'])
@jwt_required()
def listar_consultas():
    consultas = Consulta.query.all()
    return jsonify([{
        'id': c.id,
        'paciente_id': c.paciente_id,
        'medico_id': c.medico_id,
        'data_hora': c.data_hora.strftime('%Y-%m-%d %H:%M:%S'),
        'tipo': c.tipo,
        'status': c.status
    } for c in consultas]), 200

@app.route('/api/consultas/<int:id>', methods=['GET'])
@jwt_required()
def obter_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    return jsonify({
        'id': consulta.id,
        'paciente_id': consulta.paciente_id,
        'medico_id': consulta.medico_id,
        'data_hora': consulta.data_hora.strftime('%Y-%m-%d %H:%M:%S'),
        'tipo': consulta.tipo,
        'status': consulta.status
    }), 200

@app.route('/api/consultas', methods=['POST'])
@jwt_required()
def agendar_consulta():
    dados = request.get_json()
    
    nova_consulta = Consulta(
        paciente_id=dados['paciente_id'],
        medico_id=dados['medico_id'],
        data_hora=datetime.strptime(dados['data_hora'], '%Y-%m-%d %H:%M:%S'),
        tipo=dados['tipo'],
        status='agendada'
    )
    
    db.session.add(nova_consulta)
    db.session.commit()
    
    return jsonify({'mensagem': 'Consulta agendada com sucesso'}), 201

@app.route('/api/consultas/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    dados = request.get_json()
    
    if 'data_hora' in dados:
        consulta.data_hora = datetime.strptime(dados['data_hora'], '%Y-%m-%d %H:%M:%S')
    if 'tipo' in dados:
        consulta.tipo = dados['tipo']
    if 'status' in dados:
        consulta.status = dados['status']
    
    db.session.commit()
    return jsonify({'mensagem': 'Consulta atualizada com sucesso'}), 200

@app.route('/api/consultas/<int:id>', methods=['DELETE'])
@jwt_required()
def cancelar_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    consulta.status = 'cancelada'
    db.session.commit()
    return jsonify({'mensagem': 'Consulta cancelada com sucesso'}), 200

# Rotas de prontuários
@app.route('/api/prontuarios', methods=['GET'])
@jwt_required()
def listar_prontuarios():
    prontuarios = Prontuario.query.all()
    return jsonify([{
        'id': p.id,
        'consulta_id': p.consulta_id,
        'paciente_id': p.paciente_id,
        'descricao': p.descricao,
        'prescricao': p.prescricao,
        'created_at': p.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for p in prontuarios]), 200

@app.route('/api/prontuarios/<int:id>', methods=['GET'])
@jwt_required()
def obter_prontuario(id):
    prontuario = Prontuario.query.get_or_404(id)
    return jsonify({
        'id': prontuario.id,
        'consulta_id': prontuario.consulta_id,
        'paciente_id': prontuario.paciente_id,
        'descricao': prontuario.descricao,
        'prescricao': prontuario.prescricao,
        'created_at': prontuario.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }), 200

@app.route('/api/prontuarios', methods=['POST'])
@jwt_required()
def criar_prontuario():
    dados = request.get_json()
    
    novo_prontuario = Prontuario(
        consulta_id=dados['consulta_id'],
        paciente_id=dados['paciente_id'],
        descricao=dados['descricao'],
        prescricao=dados.get('prescricao')
    )
    
    db.session.add(novo_prontuario)
    db.session.commit()
    
    return jsonify({'mensagem': 'Prontuário criado com sucesso'}), 201

@app.route('/api/prontuarios/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_prontuario(id):
    prontuario = Prontuario.query.get_or_404(id)
    dados = request.get_json()
    
    if 'descricao' in dados:
        prontuario.descricao = dados['descricao']
    if 'prescricao' in dados:
        prontuario.prescricao = dados['prescricao']
    
    db.session.commit()
    return jsonify({'mensagem': 'Prontuário atualizado com sucesso'}), 200

@app.route('/api/prontuarios/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_prontuario(id):
    prontuario = Prontuario.query.get_or_404(id)
    db.session.delete(prontuario)
    db.session.commit()
    return jsonify({'mensagem': 'Prontuário removido com sucesso'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 