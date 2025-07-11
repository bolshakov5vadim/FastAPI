from SQLsession import SessionLocal

from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse


# API + описание 4-х действий
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