from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"],deprecated="auto")


def hash(password):
    return pwd_context.hash(password)


def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)


# name = hash("Ayush")
# print(verify("Ayush",name))