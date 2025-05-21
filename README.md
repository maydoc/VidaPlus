# 🏥 Sistema de Gestão Hospitalar VidaPlus

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+"/>
  <img src="https://img.shields.io/badge/Flask-2.0.1-green.svg" alt="Flask 2.0.1"/>
  <img src="https://img.shields.io/badge/Licença-MIT-yellow.svg" alt="Licença MIT"/>
  <img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange.svg" alt="Status"/>
</div>

## 📋 Sobre o Projeto

O VidaPlus é um sistema moderno de gestão hospitalar desenvolvido para centralizar e otimizar todas as operações relacionadas à saúde. Nossa solução integra hospitais, clínicas, laboratórios e equipes de home care em uma única plataforma.

### ✨ Principais Funcionalidades

- 👤 **Gestão de Pacientes**
  - Cadastro completo
  - Histórico médico
  - Agendamento de consultas
  - Prontuários eletrônicos

- 👨‍⚕️ **Gestão de Profissionais**
  - Cadastro de médicos
  - Controle de agendas
  - Prescrições digitais
  - Histórico de atendimentos

- 🏥 **Administração Hospitalar**
  - Controle de leitos
  - Gestão de suprimentos
  - Relatórios financeiros
  - Indicadores de desempenho

- 💻 **Telemedicina**
  - Consultas online
  - Prescrições digitais
  - Agendamento remoto
  - Prontuários eletrônicos

## 🚀 Começando

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Postman (para testes da API)

### 🔧 Instalação

1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/vidaplus.git
cd vidaplus
```

2. Crie e ative o ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
DATABASE_URL=sqlite:///vidaplus.db
JWT_SECRET_KEY=sua-chave-secreta-aqui
FLASK_ENV=development
FLASK_APP=app.py
```

5. Execute o sistema
```bash
python app.py
```

## 📡 Endpoints da API

### 🔐 Autenticação
- `POST /api/auth/registro` - Registro de novo usuário
- `POST /api/auth/login` - Login de usuário

### 👤 Pacientes
- `POST /api/pacientes` - Cadastro de novo paciente
- `GET /api/pacientes/{id}` - Consulta de paciente
- `PUT /api/pacientes/{id}` - Atualização de dados

### 📅 Consultas
- `POST /api/consultas` - Agendamento de consulta
- `GET /api/consultas/{id}` - Detalhes da consulta
- `PUT /api/consultas/{id}` - Atualização de status

### 📋 Prontuários
- `POST /api/prontuarios` - Criação de prontuário
- `GET /api/prontuarios/{id}` - Consulta de prontuário
- `PUT /api/prontuarios/{id}` - Atualização de prontuário

## 🛡️ Segurança

- 🔒 Autenticação via JWT
- 🔐 Senhas criptografadas com bcrypt
- 👥 Controle de acesso por perfil
- 📜 Conformidade com LGPD
- 🔍 Registro de auditoria

## 📊 Banco de Dados

O sistema utiliza SQLite como banco de dados principal, com suporte para migração para PostgreSQL em ambiente de produção.

## 🧪 Testes

Para executar os testes:
```bash
python -m pytest
```

## 📝 Documentação

A documentação completa do sistema está disponível em:
- [Documentação Técnica](DOCUMENTACAO.md)
- [Guia de API](API.md)
- [Manual do Usuário](MANUAL.md)

## 🤝 Contribuindo

1. Faça o fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 Suporte

Para suporte, envie um email para suporte@vidaplus.com ou abra uma issue no GitHub.

## 🙏 Agradecimentos

- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [JWT](https://jwt.io/)
- [Postman](https://www.postman.com/)

---
<div align="center">
  <p>Desenvolvido com ❤️ pela equipe VidaPlus</p>
  <p>© 2024 VidaPlus - Todos os direitos reservados</p>
</div> 