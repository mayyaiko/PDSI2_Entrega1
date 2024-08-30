from fastapi import FastAPI, status, Depends
from sqlalchemy.orm import Session
import classes
from database import engine, get_db, MenuItem
from model import Base
import model
from scraping import scrape_menu
from datetime import datetime

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "lala"}

@app.post("/criar", status_code=status.HTTP_201_CREATED)
def criar_valores(nova_mensagem: classes.Mensagem, db: Session = Depends(get_db)):
    mensagem_criada = model.Model_Mensagem(**nova_mensagem.model_dump())
    db.add(mensagem_criada)
    db.commit()
    db.refresh(mensagem_criada)
    return {"Mensagem": mensagem_criada}

@app.get("/quadrado/{num}")
def square(num: int):
    return num ** 2

@app.get("/menu", status_code=status.HTTP_201_CREATED)
def get_menu_data(db: Session = Depends(get_db)):
    url = "https://ufu.br"
    lista_textos, lista_links = scrape_menu(url)

    print("Textos:", lista_textos)
    print("Links:", lista_links)

    try:
        for texto, link in zip(lista_textos, lista_links):
            new_menu_item = MenuItem(menuNav=texto, link=link, created_at=datetime.utcnow())
            db.add(new_menu_item)
        db.commit()
        return {"message": "Dados inseridos com sucesso!"}
    except Exception as e:
        db.rollback()  # Reverte a transação em caso de erro
        print(f"Erro ao inserir dados: {e}")
        return {"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
