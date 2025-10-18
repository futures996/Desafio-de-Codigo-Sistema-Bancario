from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "sua-chave-secreta"
ALGORITHM = "HS256"

def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        cpf = payload.get("sub")
        if cpf is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return cpf
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
