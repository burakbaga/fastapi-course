from jose.constants import ALGORITHMS
from sqlalchemy.sql.functions import user
from db.repository.login import get_user
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from fastapi import APIRouter
from jose import jwt,JWTError
from sqlalchemy.orm import Session

from db.session import get_db
from core.config import settings
from datetime import timedelta
from core.security import create_access_token
from core.hashing import Hasher

router = APIRouter()


def authenticate_user(username:str, password:str, db:Session):
    user = get_user(username=username, db=db)
    print(user)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user




@router.post("/token")
def login_for_access_token(form_data:OAuth2PasswordRequestForm = Depends(),
                            db:Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")
    access_token_expire = timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub":user.email}, expires_delta=access_token_expire)
    # response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return {"access_token":access_token, "token_type": "bearer"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

def get_current_user_from_token(token : str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail = "Could not validate credentials")
    try : 
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        print("aaaaaa")
        username :str = payload.get("sub")
        print("e mail is ",username)

        if username is None:
            print("username is none")
            raise credentials_exceptions
    except JWTError:
        print("jwt error")
        raise credentials_exceptions
    user = get_user(username=username,db=db)
    if user is None:
        print("db error")
        raise credentials_exceptions
    return user