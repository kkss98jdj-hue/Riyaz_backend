from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import os
from dotenv import load_dotenv

load_dotenv()


class AuthHandler:
    def __init__(self, data: dict = None):
        self.data = data or {}  # store incoming data
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 24 * 60  

    def get_password_hash(self) -> str:
        return self.pwd_context.hash(self.data.get("password", ""))

    def verify_password(self) -> bool:
        return self.pwd_context.verify(
            self.data.get("password", ""),
            self.data.get("hashed_password", "")
        )

    def create_access_token(self) -> str:
        to_encode = self.data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    

    def decode_token(self) -> dict:
        try:
            payload = jwt.decode(
                self.data.get("token", ""),
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
