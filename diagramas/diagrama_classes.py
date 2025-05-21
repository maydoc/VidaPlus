from graphviz import Digraph

def criar_diagrama_classes():
    dot = Digraph(comment='Diagrama de Classes - VidaPlus')
    dot.attr(rankdir='TB')
    
    # Configurações do grafo
    dot.attr('node', shape='record')
    dot.attr('edge', dir='forward')
    
    # Classe Usuario
    dot.node('Usuario', '''{Usuario|
        + id: Integer
        + nome: String
        + email: String
        + senha: String
        + tipo: String
        + created_at: DateTime
        |
        + registrar()
        + autenticar()
        + atualizar()
        + deletar()
    }''')
    
    # Classe Paciente
    dot.node('Paciente', '''{Paciente|
        + id: Integer
        + usuario_id: Integer
        + cpf: String
        + data_nascimento: Date
        + telefone: String
        + endereco: String
        |
        + cadastrar()
        + atualizar()
        + consultar_prontuario()
        + agendar_consulta()
    }''')
    
    # Classe Medico
    dot.node('Medico', '''{Medico|
        + id: Integer
        + usuario_id: Integer
        + crm: String
        + especialidade: String
        |
        + cadastrar()
        + atualizar()
        + gerenciar_agenda()
        + registrar_prontuario()
    }''')
    
    # Classe Consulta
    dot.node('Consulta', '''{Consulta|
        + id: Integer
        + paciente_id: Integer
        + medico_id: Integer
        + data_hora: DateTime
        + tipo: String
        + status: String
        |
        + agendar()
        + confirmar()
        + cancelar()
        + realizar()
    }''')
    
    # Classe Prontuario
    dot.node('Prontuario', '''{Prontuario|
        + id: Integer
        + consulta_id: Integer
        + paciente_id: Integer
        + descricao: Text
        + prescricao: Text
        + created_at: DateTime
        |
        + criar()
        + atualizar()
        + consultar()
        + arquivar()
    }''')
    
    # Relacionamentos
    dot.edge('Usuario', 'Paciente', '1..1')
    dot.edge('Usuario', 'Medico', '1..1')
    dot.edge('Paciente', 'Consulta', '1..*')
    dot.edge('Medico', 'Consulta', '1..*')
    dot.edge('Consulta', 'Prontuario', '1..1')
    dot.edge('Paciente', 'Prontuario', '1..*')
    
    # Salvar o diagrama
    dot.render('diagrama_classes', format='png', cleanup=True)

if __name__ == '__main__':
    criar_diagrama_classes() 