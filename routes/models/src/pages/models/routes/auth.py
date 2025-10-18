from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "sua-chave-secreta"
ALGORITHM = "HS256"
EXPIRATION_MINUTES = 30

def criar_token(dados: dict):
    dados_copia = dados.copy()
    expira = datetime.utcnow() + timedelta(minutes=EXPIRATION_MINUTES)
    dados_copia.update({"exp": expira})
    return jwt.encode(dados_copia, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
