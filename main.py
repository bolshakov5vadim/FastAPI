from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import  Column, Integer, String
from sqlalchemy.orm import Session
import psycopg2 # Иногда требуется для postgres
# Бибилотеки SQL

from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse

from decouple import Config, RepositoryEnv
ENV_FILE = 'e.env'
config = Config(RepositoryEnv(ENV_FILE))
# Подключение конфиг-файла

# Создаем модель бд

class Base(DeclarativeBase): pass
class Person(Base):
   __tablename__ = config('TABLE_NAME')

   id = Column(Integer, primary_key=True, index=True)
   name = Column(String)
   surname = Column(String)
   birthday = Column(Integer)
   status = Column(String)

engine = create_engine(config('DB_LINK'))
SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine) # Создание таблиц, если их нет
 
# API + описание 4-х его действий
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
   
@app.get("/api")
def read_all(db: Session = Depends(get_db)):
    return db.query(Person).all()
  
@app.get("/api/{id}")
def read(id, db: Session = Depends(get_db)):
    person = db.query(Person).filter(Person.id == id).first() # Запрос

    if person==None:  
        return JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})
    # Если пользователь найден, отправляем его
    return person
  
  
@app.post("/api")
def create(data  = Body(), db: Session = Depends(get_db)):

    person = Person(name=data["name"], surname=data["surname"], status=data["status"]) # запрос

    db.add(person)
    db.commit()
    db.refresh(person)
    return person
  
@app.put("/api")
def update(data  = Body(), db: Session = Depends(get_db)):
   
    person = db.query(Person).filter(Person.id == data["id"]).first() # Запрос

    if person == None: 
        return JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})

    # Если пользователь найден, обновляем его
    person.name = data["name"]
    person.surname = data["surname"]
    person.status=data["status"]
    db.commit()
    db.refresh(person)
    return person
  
  
@app.delete("/api/{id}")
def delete(id, db: Session = Depends(get_db)):

    person = db.query(Person).filter(Person.id == id).first() # Запрос

    if person == None:
        return JSONResponse( status_code=404, content={ "message": "Пользователь не найден"})
   
    # Если пользователь найден, удаляем его
    db.delete(person)
    db.commit()
    return person
