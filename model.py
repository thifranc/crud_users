
from sqlalchemy import String, Column, Integer, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


from marshmallow_sqlalchemy import ModelSchema

psql = {
    'user': 'roger_cli',
    'pw': '82uSNy5CQzR=3;n?t',
    'db': 'roger',
    'host': 'localhost',
    'port': '5432',
}

engine = create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
                          psql['user'], psql['pw'], psql['host'], psql['port'], psql['db']))
Session = sessionmaker(bind=engine)

Base = declarative_base()

class Role(Base):
  __tablename__ = 'role'
  id=Column('id', Integer, primary_key=True)
  name=Column('name', String(255))
  users = relationship("User")


  def __init__(self, name):
    self.name = name

class User(Base):
  __tablename__ = 'users'
  id=Column('id', Integer, primary_key=True)
  login=Column('login', String(255))
  password=Column('password', String(255))
  id_role = Column('id_role', Integer, ForeignKey("role.id"))

  def __init__(self, login, password, id_role):
    self.login = login
    self.password = password
    self.id_role = id_role

  @classmethod
  def exists_and_is_unique(self, res):
    if len(res) == 0:
      raise ValueError('User not found')
    if len(res) != 1:
      raise ValueError("Too many users found : {}".format(len(res)))
    return True

class UserSchema(ModelSchema):
  class Meta:
    model = User
    #fields = ("login", "id_role")

class RoleSchema(ModelSchema):
  class Meta:
    model = Role

