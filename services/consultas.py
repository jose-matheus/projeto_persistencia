from bson import ObjectId
from fastapi import HTTPException
from datetime import datetime
from models.consultas import ConsultaCreate, ConsultaResponse
from models.medicos import Medico
from models.paciente import Paciente
from models.consultas import Consulta
from beanie import PydanticObjectId

# Função para adicionar consulta no banco de dados
async def adicionar_consulta_db(consulta_data: ConsultaCreate):
    # Criar nova consulta
    nova_consulta = Consulta(**consulta_data.dict())
    await nova_consulta.save()

    # Obter paciente e médico
    paciente = await Paciente.get(nova_consulta.paciente_id)
    medico = await Medico.get(nova_consulta.medico_id)

    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")

    # Adicionar consulta ao paciente e ao médico
    paciente.consultas.append(nova_consulta.id)
    medico.consultas.append(nova_consulta.id)

    await paciente.save()
    await medico.save()

    return nova_consulta

# Função para listar todas as consultas
async def listar_consultas_db():
    consultas = await Consulta.find().to_list()
    return ConsultaResponse(consultas=consultas, quantidade=len(consultas))

# Função para buscar consulta por ID
async def buscar_consulta_por_id_db(id: str):
    consulta = await Consulta.get(id)
    return consulta

# Função para atualizar consulta no banco de dados
async def atualizar_consulta_db(id: str, consulta: ConsultaCreate):
    medico = await Medico.get(consulta.medico_id)
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")

    update_data = {k: v for k, v in consulta.dict(exclude_unset=True).items()}
    update_data["paciente_id"] = str(update_data["paciente_id"])
    update_data["medico_id"] = str(update_data["medico_id"])

    consulta_atualizada = await Consulta.get(id)
    if not consulta_atualizada:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")

    await consulta_atualizada.update({"$set": update_data})
    return await Consulta.get(id)

# Função para excluir consulta no banco de dados
async def excluir_consulta_db(id: str):
    consulta = await Consulta.get(id)
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    
    # Obter paciente e médico associados à consulta
    paciente = await Paciente.get(consulta.paciente_id)
    medico = await Medico.get(consulta.medico_id)

    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    # Remover a consulta das listas de consultas do paciente e do médico
    paciente.consultas = [consulta_id for consulta_id in paciente.consultas if consulta_id != consulta.id]
    medico.consultas = [consulta_id for consulta_id in medico.consultas if consulta_id != consulta.id]

    # Salvar as alterações no paciente e no médico
    await paciente.save()
    await medico.save()

    # Excluir a consulta
    await consulta.delete()

    return True

# Função para listar consultas de um paciente
async def listar_consultas_por_paciente_db(paciente_id: str):
    consultas = await Consulta.find({"paciente_id": str(paciente_id)}).to_list()
    return consultas

# Função para listar pacientes sem consultas
async def listar_pacientes_sem_consultas_db():
    pacientes = await Paciente.find().to_list()
    pacientes_sem_consultas = []
    for paciente in pacientes:
        consultas = await Consulta.find({"paciente_id": paciente.id}).to_list()
        if not consultas:
            pacientes_sem_consultas.append(paciente)

    return pacientes_sem_consultas

# Função para listar todas as consultas dentro de um período
async def listar_consultas_por_periodo_db(inicio: datetime, fim: datetime):
    consultas = await Consulta.find({
        "data_hora": {"$gte": inicio, "$lte": fim}
    }).to_list()
    return consultas

# Função para listar consultas com pacientes para um médico
async def listar_consultas_com_pacientes(medico_id: str):
    consultas = await Consulta.find({"medico_id": str(medico_id)}).to_list()
    resultado = []
    for consulta in consultas:
        paciente = await Paciente.get(consulta.paciente_id)
        consulta_info = {
            "consulta_id": str(consulta.id),
            "paciente": paciente.nome if paciente else "Desconhecido",
            "status": consulta.status,
            "data": consulta.data_hora
        }
        resultado.append(consulta_info)

    return resultado
