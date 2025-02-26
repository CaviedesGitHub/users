from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, Text, Unicode, UUID, Enum
from sqlalchemy.orm import relationship
from db_config.sqlalchemy_connect import Base

import enum
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy import DateTime, Date
from sqlalchemy.sql import func
##from werkzeug.security import generate_password_hash, check_password_hash



class Signup(Base):
    __tablename__ = "signup"

    id = Column(Integer, primary_key=True, index=True)
    username = Column('username', String, unique=False, index=False)
    password = Column('password',String, unique=False, index=False)
    
class Login(Base): 
    __tablename__ = "login"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=False, index=False)
    password = Column(String, unique=False, index=False)
    passphrase = Column(String, unique=False, index=False)
    approved_date = Column(Date, unique=False, index=False)
       
    profiles = relationship('Profile', back_populates="login", uselist=False)
    permission_sets = relationship('PermissionSet', back_populates="login")

class Permission(Base):
    __tablename__ = "permission"
    id = Column(Integer, primary_key=True, index=True, )
    name = Column(String, unique=False, index=False)
    description = Column(String, unique=False, index=False)
        
    permission_sets = relationship('PermissionSet', back_populates="permission")
    
class PermissionSet(Base): 
    __tablename__ = "permission_set"
    id = Column(Integer,  primary_key=True, index=True)
    login_id = Column(Integer, ForeignKey('login.id'), unique=False, index=False)
    permission_id = Column(Integer, ForeignKey('permission.id'), unique=False, index=False)
        
    login = relationship('Login', back_populates="permission_sets")
    permission = relationship('Permission', back_populates="permission_sets")

class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, unique=False, index=False)
    lastname = Column(String, unique=False, index=False)
    age = Column(Integer, unique=False, index=False)
    membership_date = Column(Date, unique=False, index=False)
    member_type = Column(String, unique=False, index=False)
    login_id = Column(Integer, ForeignKey('login.id'), unique=False, index=False)
    status = Column(Integer, unique=False, index=False)
    
    login = relationship('Login', back_populates="profiles")

       

class UserType(enum.Enum):
    EMPRESA = "Empresa"
    CANDIDATO = "Candidato"
    EMPLEADO_ABC = "Empleado"

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Unicode(128), nullable=False, default='MISSING', unique=True)
    password = Column(Unicode(256))
    tipo = Column(Enum(UserType), nullable=False)  

    ##def __init__(self, *args, **kw): 
    ##    super(Usuario, self).__init__(*args, **kw) 


class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        else:
            return value.name #{'llave':value.name, 'valor':value.value} #{value.name}  #{'llave':value.name, 'valor':value.value}
    
class UsuarioSchema(SQLAlchemyAutoSchema):
    tipo=EnumADiccionario(attribute=('tipo'))
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True

usuario_schema = UsuarioSchema()

