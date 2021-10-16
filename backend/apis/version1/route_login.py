from db.repository.login import get_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends,HTTPException,status
from fastapi import APIRouter

from sqlalchemy.orm import Session

from db.session import get_db
from core.config import settings
from datetime import timedelta
from core.security import create_access_token
from core.hashing import Hasher

router = APIRouter()


def authenticate_user(username:str,password:str,db:Session):
    user = get_user(username=username,db=db)
    print(user)
    if not user :
        False
    if not Hasher.verify_password(password,user.hashed_password):
        return False
    
    return user




@router.post("/token")
def login_for_acces_token(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail="Incorrect username or password")
    
    acces_token_expire = timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_IN_MINUTES)
    acces_token = create_access_token(data = {"sub":user.email},expires_delta = acces_token_expire)

    return {"acces_token":acces_token,"token_type":"bearer"}

