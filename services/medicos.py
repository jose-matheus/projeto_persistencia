from fastapi import HTTPException
from models.medicos import Medico, MedicoCreate
from models.paciente import Paciente
from typing import List, Dict
from beanie import PydanticObjectId
from bson import ObjectId

# Função para criar um médico
async def criar_medico_db(medico: MedicoCreate) -> Medico:
    db_medico = Medico(**medico.dict())
    await db_medico.insert()
    return db_medico

# Função para listar todos os médicos
async def listar_medicos_db():
    return await Medico.find().to_list()

# Função para obter um médico pelo ID
async def obter_medico_db(id: str) -> Medico:
    db_medico = await Medico.get(id)
    if not db_medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    return db_medico

# Função para atualizar um médico
async def atualizar_medico_db(id: str, medico: MedicoCreate) -> Medico:
    result = await Medico.get(id)
    if not result:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    await result.update({"$set": medico.dict(exclude_unset=True)})
    return result

# Função para deletar um médico
async def deletar_medico_db(id: str) -> bool:
    medico = await Medico.get(id)
    if not medico:
        return False
    await medico.delete()
    return True

# Função para obter médicos pelo nome
async def obter_medico_por_nome_db(nome: str):
    return await Medico.find({"nome": {"$regex": nome, "$options": "i"}}).to_list()

# Função para listar os médicos por especialidade
async def listar_medicos_por_especialidade_db(especialidade: str):
    return await Medico.find({"especialidade": {"$regex": especialidade, "$options": "i"}}).to_list()

# Função para listar os pacientes de um médico
async def listar_pacientes_por_medico(medico_id: str) -> List[Dict]:
    pacientes = await Paciente.find({"medicos": str(medico_id)}).to_list()
    return [{"paciente_id": str(paciente.id), "nome": paciente.nome} for paciente in pacientes]

# Função que vai associar o paciente ao médico da sua consulta
async def associar_paciente_a_medico(paciente_id: str, medico_id: str):
    paciente = await Paciente.get(paciente_id)
    medico = await Medico.get(medico_id)

    if not paciente:
        raise HTTPException(status_code=404, detail=f"Paciente com ID {paciente_id} não encontrado.")
    if not medico:
        raise HTTPException(status_code=404, detail=f"Médico com ID {medico_id} não encontrado.")
    
    # Associa paciente ao médico
    paciente.medicos.append(medico.id)
    medico.pacientes.append(paciente.id)

    # Atualiza os documentos de paciente e médico
    await paciente.save()
    await medico.save()

    return {"paciente_id": paciente.id,
        "medico_id": medico.id,
        "paciente_nome": paciente.nome,  # Adicionando nome do paciente
        "medico_nome": medico.nome       # Adicionando nome do médico
        }
