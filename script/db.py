from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import random
import string

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    userid = Column(Integer, primary_key=True)
    username = Column(String)
    role = Column(String)
    tutorcode = Column(String, nullable=True)
    subscribe = Column(String, nullable=True)
    extra = Column(String, nullable=True)

    def __repr__(self):
        return f"<User(userid={self.userid}, username={self.username}, role={self.role})>"

engine = create_engine('sqlite:///bot.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def generate_tutor_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))