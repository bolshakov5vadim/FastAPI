from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import  Column, Integer, String
from sqlalchemy.orm import Session
import psycopg2 # Иногда требуется для postgres
# Бибилотеки SQL

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
