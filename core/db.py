from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.settings import DATABASE_URL
from core.user.models import User

engine = create_engine(DATABASE_URL, echo=False)
User.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

def get_user_by_telegram_id(
    telegram_id: int
) -> User:
    session = SessionLocal()
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    session.close()
    return user

def create_user(
    telegram_id: int, 
    username: str, 
    first_name: str, 
    last_name: str,
    access_token: str,
    refresh_token: str
) -> None:
    session = SessionLocal()
    if not get_user_by_telegram_id(telegram_id):
        new_user: User = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            access_token=access_token,
            refresh_token=refresh_token  
        )
        session.add(new_user)
        session.commit()
    session.close()
