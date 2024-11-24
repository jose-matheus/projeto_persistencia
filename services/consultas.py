from fastapi import APIRouter, HTTPException
import csv
import os
from typing import List, Optional
from hashlib import sha256
from io import BytesIO
from zipfile import ZipFile
from models.consultas import Consulta

# Caminho para o arquivo CSV
CSV_FILE = "consultas.csv"

def verificar_arquivo_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["id", "paciente_id", "medico_id", "data_hora", "status", "observacoes"])
            writer.writeheader()

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

def listar_consultas_csv(retornar_dicionario=True):
    verificar_arquivo_csv()
    consultas = []
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            consultas.append(Consulta(**row))
    
    if retornar_dicionario:
        return {
            "consultas": consultas,
            "quantidade": len(consultas)
        }
    return consultas

def buscar_consulta_por_id(id: int) -> Consulta:
    try:
        consultas = listar_consultas_csv(retornar_dicionario=False)
        for consulta in consultas:
            if consulta.id == id:
                return consulta
        return None  # ID não encontrado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar consulta: {str(e)}")

def atualizar_consulta_csv(id: int, consulta: Consulta) -> Consulta:
    try:
        linhas_atualizadas = []
        consulta_encontrada = False
        with open(CSV_FILE, mode="r", newline="") as arquivo:
            reader = csv.DictReader(arquivo)
            for linha in reader:
                if int(linha["id"]) == id:
                    consulta_encontrada = True
                    linhas_atualizadas.append(consulta.dict())
                else:
                    linhas_atualizadas.append(linha)

        if not consulta_encontrada:
            return None

        with open(CSV_FILE, mode="w", newline="") as arquivo:
            fieldnames = ["id", "paciente_id", "medico_id", "data_hora", "status", "observacoes"]
            writer = csv.DictWriter(arquivo, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(linhas_atualizadas)

        return consulta
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar CSV: {str(e)}")

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

def excluir_consulta_csv(id: int) -> bool:
    consultas = listar_consultas_csv(retornar_dicionario=False)
    consultas_filtradas = [consulta for consulta in consultas if consulta.id != id]
    
    if len(consultas_filtradas) == len(consultas):
        return False  # Nenhuma consulta foi excluída

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

def compactar_csv_em_zip() -> BytesIO:
    zip_buffer = BytesIO()
    
    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError(f"O arquivo {CSV_FILE} não foi encontrado.")
    
    with ZipFile(zip_buffer, mode="w") as zip_file:
        zip_file.write(CSV_FILE, os.path.basename(CSV_FILE))  # Adiciona o arquivo CSV no ZIP
    
    zip_buffer.seek(0)
    return zip_buffer

def obter_hash_sha256_csv() -> str:
    sha256_hash = sha256()
    with open(CSV_FILE, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

