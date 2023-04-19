from passlib.context import CryptContext
passwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def hash(passwd: str):
    return passwd_context.hash(passwd)

def verify(plain_passwd: str, hashed_passwd: str):
    return passwd_context.verify(plain_passwd, hashed_passwd)