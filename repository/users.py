
from typing import Dict, Any
from sqlalchemy.orm import Session
from models.data.sqlalchemy_data import Usuario
from sqlalchemy import desc

class UsersRepository: 
    def __init__(self, sess:Session):
        self.sess: Session = sess
    
    def insert_user(self, user: Usuario) -> bool: 
        try:
            self.sess.add(user)
            self.sess.commit()
        except Exception as e:
            print(e) 
            return False 
        return True
    
    def update_user(self, id:int, details:Dict[str, Any]) -> bool: 
       try:
             self.sess.query(Usuario).filter(Usuario.id == id).update(details)     
             self.sess.commit() 
       except: 
           return False 
       return True
   
    def delete_user(self, id:int) -> bool: 
        try:
           user = self.sess.query(Usuario).filter(Usuario.id == id).delete()
           self.sess.commit()
        except: 
            return False 
        return True
    
    def get_all_users(self):
        return self.sess.query(Usuario).all() 
    
    def get_all_login_username(self, username:str):
        return self.sess.query(Usuario).filter(Usuario.nombre == username).one_or_none()
    
    def get_all_users_sorted_desc(self):
        return self.sess.query(Usuario.nombre, Usuario.password).order_by(desc(Usuario.username)).all() 
    
    def get_users(self, id:int): 
        return self.sess.query(Usuario).filter(Usuario.id == id).one_or_none()
