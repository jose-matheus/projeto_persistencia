import csv
import os
from typing import List, Optional
from hashlib import sha256
from io import BytesIO
from zipfile import ZipFile
from models.consultas import Consulta

# Caminho para o arquivo CSV
CSV_FILE = "consultas.csv"

# Função para verificar se o arquivo CSV existe, caso contrário, cria o cabeçalho
def verificar_arquivo_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["id", "paciente_id", "medico_id", "data_hora", "status", "observacoes"])
            writer.writeheader()

# Função para adicionar consulta no CSV
def adicionar_consulta_csv(consulta: Consulta) -> Consulta:
    verificar_arquivo_csv()
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "paciente_id", "medico_id", "data_hora", "status", "observacoes"])
        writer.writerow({
            "id": consulta.id,
            "paciente_id": consulta.paciente_id,
            "medico_id": consulta.medico_id,
            "data_hora": consulta.data_hora,
            "status": consulta.status,
            "observacoes": consulta.observacoes
        })
    return consulta

# Função para listar todas as consultas no CSV e contar a quantidade delas
def listar_consultas_csv() -> dict:
    verificar_arquivo_csv()
    consultas = []
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            consultas.append(Consulta(**row))
    
    # Retorna um dicionário com a lista de consultas e a contagem
    return {
        "consultas": consultas,
        "quantidade": len(consultas)
    }


# Função para buscar consulta por ID
def buscar_consulta_por_id(id: int) -> Optional[Consulta]:
    consultas = listar_consultas_csv()
    return next((consulta for consulta in consultas if consulta.id == id), None)

# Função para atualizar consulta no CSV
def atualizar_consulta_csv(id: int, consulta_atualizada: Consulta) -> Optional[Consulta]:
    consultas = listar_consultas_csv()
    for idx, consulta in enumerate(consultas):
        if consulta.id == id:
            consultas[idx] = consulta_atualizada
            break
    else:
        return None

    # Reescreve o CSV com as consultas atualizadas
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "paciente_id", "medico_id", "data_hora", "status", "observacoes"])
        writer.writeheader()
        for consulta in consultas:
            writer.writerow({
                "id": consulta.id,
                "paciente_id": consulta.paciente_id,
                "medico_id": consulta.medico_id,
                "data_hora": consulta.data_hora,
                "status": consulta.status,
                "observacoes": consulta.observacoes
            })
    return consulta_atualizada

# Função para excluir consulta
def excluir_consulta_csv(id: int) -> bool:
    consultas = listar_consultas_csv()
    consultas_filtradas = [consulta for consulta in consultas if consulta.id != id]
    if len(consultas_filtradas) == len(consultas):
        return False  # Nenhuma consulta foi excluída

    # Reescreve o CSV sem a consulta excluída
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "paciente_id", "medico_id", "data_hora", "status", "observacoes"])
        writer.writeheader()
        for consulta in consultas_filtradas:
            writer.writerow({
                "id": consulta.id,
                "paciente_id": consulta.paciente_id,
                "medico_id": consulta.medico_id,
                "data_hora": consulta.data_hora,
                "status": consulta.status,
                "observacoes": consulta.observacoes
            })
    return True

# Função para compactar o arquivo CSV em ZIP
def compactar_csv_em_zip() -> BytesIO:
    zip_buffer = BytesIO()
    
    # Verifique se o arquivo CSV existe e tem conteúdo
    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError(f"O arquivo {CSV_FILE} não foi encontrado.")
    
    with ZipFile(zip_buffer, mode="w") as zip_file:
        zip_file.write(CSV_FILE, os.path.basename(CSV_FILE))  # Adiciona o arquivo CSV no ZIP
    
    zip_buffer.seek(0)
    return zip_buffer



# Função para obter o hash SHA256 do CSV
def obter_hash_sha256_csv() -> str:
    sha256_hash = sha256()
    with open(CSV_FILE, "rb") as f:
        # Lê o arquivo em blocos de 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

