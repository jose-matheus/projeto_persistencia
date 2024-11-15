from fastapi import FastAPI
from routes.paciente import router as paciente_router

app = FastAPI()

 # Inclui as rotas
app.include_router(paciente_router)

@app.get('/amote')
def te_amo(amor):
    return {"message" : "te amo"}