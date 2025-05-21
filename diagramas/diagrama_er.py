from graphviz import Digraph

def criar_diagrama_er():
    dot = Digraph(comment='Diagrama ER - VidaPlus')
    dot.attr(rankdir='TB')
    
    # Configurações do grafo
    dot.attr('node', shape='record')
    dot.attr('edge', dir='forward')
    
    # Tabela usuarios
    dot.node('usuarios', '''{usuarios|
        id (PK)
        nome
        email
        senha
        tipo
        created_at
    }''')
    
    # Tabela pacientes
    dot.node('pacientes', '''{pacientes|
        id (PK)
        usuario_id (FK)
        cpf
        data_nascimento
        telefone
        endereco
    }''')
    
    # Tabela medicos
    dot.node('medicos', '''{medicos|
        id (PK)
        usuario_id (FK)
        crm
        especialidade
    }''')
    
    # Tabela consultas
    dot.node('consultas', '''{consultas|
        id (PK)
        paciente_id (FK)
        medico_id (FK)
        data_hora
        tipo
        status
    }''')
    
    # Tabela prontuarios
    dot.node('prontuarios', '''{prontuarios|
        id (PK)
        consulta_id (FK)
        paciente_id (FK)
        descricao
        prescricao
        created_at
    }''')
    
    # Tabela agenda
    dot.node('agenda', '''{agenda|
        id (PK)
        medico_id (FK)
        data
        hora_inicio
        hora_fim
        disponivel
    }''')
    
    # Relacionamentos
    dot.edge('usuarios', 'pacientes', '1:1')
    dot.edge('usuarios', 'medicos', '1:1')
    dot.edge('pacientes', 'consultas', '1:N')
    dot.edge('medicos', 'consultas', '1:N')
    dot.edge('consultas', 'prontuarios', '1:1')
    dot.edge('pacientes', 'prontuarios', '1:N')
    dot.edge('medicos', 'agenda', '1:N')
    
    # Salvar o diagrama
    dot.render('diagrama_er', format='png', cleanup=True)

if __name__ == '__main__':
    criar_diagrama_er() 