from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from models.data.sqlalchemy_data import Usuario
from repository.users import UsersRepository
from models.request.users import UserReq
from typing import List
from db_config.sqlalchemy_connect import sess_db

from models.data.sqlalchemy_data import UsuarioSchema

from fastapi.security import OAuth2PasswordRequestForm
from security.secure import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user, authenticate

usuarioSchema=UsuarioSchema()

router = APIRouter()
        

@router.post("/signup/add")
def add_signup(req: UserReq, sess:Session = Depends(sess_db)):
    repo:UsersRepository = UsersRepository(sess)
    user = Usuario(id=req.id, nombre=req.nombre, password=req.password, tipo=req.tipo)
    result = repo.insert_user(user)
    json_user=jsonable_encoder(user)
    if result == True:
        return JSONResponse(content=json_user, status_code=201)
    else: 
        return JSONResponse(content={'message':'create user problem encountered'}, status_code=500)

@router.get("/signup/list", response_model=List[UserReq])
def list_users(current_user: Usuario = Depends(get_current_user), sess:Session = Depends(sess_db)):
    print("/signup/list")
    repo:UsersRepository = UsersRepository(sess)
    result = repo.get_all_users()
    return result

@router.post("/login/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), sess:Session = Depends(sess_db)):
    print("inicio login")
    username = form_data.username
    password = form_data.password
    print(username)
    print(password)
    userrepo = UsersRepository(sess)
    usuario = userrepo.get_all_login_username(username)     
    if usuario==None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    elif authenticate(username, password, usuario):
        access_token = create_access_token(
            data={"sub": username}, 
            expires_after=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {"access_token": access_token, "token_type": "Bearer"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

