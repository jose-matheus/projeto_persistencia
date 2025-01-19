# projeto_persistencia
Projeto de Desenvolvimento para a disciplina de "Desenvolvimento para Persistência da UFC "




```mermaid
classDiagram
    class Paciente {
        +String nome
        +String telefone
        +String email
        +String sexo
        +Float peso
        +Float altura
        +String problemas_de_saude
    }

    class Consulta {
        +Int paciente_id
        +Int medico_id
        +Date data_hora
        +String status
        +String observações
    }

    class Medico {
        +String nome
        +String especialidade
        +String CRM
        +String email
        +String telefone
    }

    Paciente "1" --> "1..*" Consulta
    Medico "1" --> "1..*" Consulta
    Paciente "1..*" --> "1..*" Medico
