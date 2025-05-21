from graphviz import Digraph

def criar_diagrama_caso_uso():
    dot = Digraph(comment='Diagrama de Caso de Uso - VidaPlus')
    dot.attr(rankdir='TB')
    
    # Configurações do grafo
    dot.attr('node', shape='ellipse')
    dot.attr('edge', dir='forward')
    
    # Atores
    dot.node('paciente', 'Paciente', shape='circle')
    dot.node('medico', 'Médico', shape='circle')
    dot.node('admin', 'Administrador', shape='circle')
    
    # Casos de Uso - Gestão de Usuários
    dot.node('registro', 'Registro de Usuário')
    dot.node('login', 'Login')
    dot.node('recuperar_senha', 'Recuperar Senha')
    dot.node('gerenciar_perfil', 'Gerenciar Perfil')
    
    # Casos de Uso - Gestão de Pacientes
    dot.node('cadastrar_paciente', 'Cadastrar Paciente')
    dot.node('visualizar_prontuario', 'Visualizar Prontuário')
    dot.node('gerenciar_documentos', 'Gerenciar Documentos')
    
    # Casos de Uso - Gestão de Consultas
    dot.node('agendar_consulta', 'Agendar Consulta')
    dot.node('telemedicina', 'Telemedicina')
    dot.node('cancelar_consulta', 'Cancelar Consulta')
    
    # Casos de Uso - Gestão Administrativa
    dot.node('gerar_relatorios', 'Gerar Relatórios')
    dot.node('gerenciar_recursos', 'Gerenciar Recursos')
    dot.node('monitorar_sistema', 'Monitorar Sistema')
    
    # Relacionamentos - Paciente
    dot.edge('paciente', 'registro')
    dot.edge('paciente', 'login')
    dot.edge('paciente', 'recuperar_senha')
    dot.edge('paciente', 'gerenciar_perfil')
    dot.edge('paciente', 'agendar_consulta')
    dot.edge('paciente', 'telemedicina')
    dot.edge('paciente', 'cancelar_consulta')
    dot.edge('paciente', 'visualizar_prontuario')
    
    # Relacionamentos - Médico
    dot.edge('medico', 'registro')
    dot.edge('medico', 'login')
    dot.edge('medico', 'gerenciar_perfil')
    dot.edge('medico', 'agendar_consulta')
    dot.edge('medico', 'telemedicina')
    dot.edge('medico', 'cancelar_consulta')
    dot.edge('medico', 'gerenciar_documentos')
    
    # Relacionamentos - Administrador
    dot.edge('admin', 'registro')
    dot.edge('admin', 'login')
    dot.edge('admin', 'gerenciar_perfil')
    dot.edge('admin', 'gerar_relatorios')
    dot.edge('admin', 'gerenciar_recursos')
    dot.edge('admin', 'monitorar_sistema')
    
    # Salvar o diagrama
    dot.render('diagrama_caso_uso', format='png', cleanup=True)

if __name__ == '__main__':
    criar_diagrama_caso_uso() 