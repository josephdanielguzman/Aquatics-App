from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashify(password: str):
    """Returns hashed password."""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """Returns True if password matches hashed password."""
    return pwd_context.verify(plain_password, hashed_password)