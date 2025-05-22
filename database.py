from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
import random
import string

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///bot.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    userid = Column(Integer, primary_key=True)
    username = Column(String)
    role = Column(String)  # 'teacher' or 'student'
    tutorcode = Column(String, nullable=True)  # код преподавателя
    subscribe = Column(String, nullable=True)  # имя преподавателя, на которого подписан
    extra = Column(String, nullable=True)

    def __repr__(self):
        return f"<User(userid={self.userid}, username={self.username}, role={self.role})>"


# Инициализация базы данных
engine = create_engine('sqlite:///bot.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def generate_tutor_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))