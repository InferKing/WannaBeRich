from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, and_
from sqlalchemy.orm import declarative_base, mapped_column, relationship, sessionmaker
from main import app_config
from datetime import datetime

engine = create_engine(app_config.SQLALCHEMY_DATABASE_URI)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String)
    initial_balance = mapped_column(Integer)
    created_date = mapped_column(String, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    children_categories = relationship("Category", back_populates="parent_user")
    children_economy = relationship("Economy", back_populates="parent_user")


class Category(Base):
    __tablename__ = "categories"
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"))
    name = mapped_column(String)
    created_date = mapped_column(String, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_date = mapped_column(String, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    children_economy = relationship("Economy", back_populates="parent_category")
    parent_user = relationship("User", back_populates="children_categories")


class Economy(Base):
    __tablename__ = "economy"
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"))
    category_id = mapped_column(Integer, ForeignKey("categories.id"))
    amount = mapped_column(Integer)
    created_date = mapped_column(String, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    parent_user = relationship("User", back_populates="children_economy")
    parent_category = relationship("Category", back_populates="children_economy")


# Should be in main.py or in __init__.py after creating models
Base.metadata.create_all(engine)


async def find_user_by_id(user_id: int) -> User | None:
    with Session() as session:
        return session.query(User).filter(User.id == user_id).first()


async def create_user(user_id: int, username: str, balance: int) -> User:
    with Session(expire_on_commit=False) as session:
        user = User(id=user_id, username=username, initial_balance=balance)
        session.add(user)
        session.commit()
        return user


async def create_category(user_id: int, name: str) -> Category:
    with Session(expire_on_commit=False) as session:
        category = Category(user_id=user_id, name=name)
        session.add(category)
        session.commit()
        return category


async def get_categories(user_id: int) -> list[Category]:
    with Session() as session:
        return session.query(Category).filter(Category.user_id == user_id).all()


async def create_economy(user_id: int, category_id: int, amount: int) -> Economy:
    with Session(expire_on_commit=False) as session:
        expense = Economy(user_id=user_id, category_id=category_id, amount=amount)
        session.add(expense)
        session.commit()
        return expense



async def get_economy(user_id: int) -> list[Economy]:
    with Session() as session:
        return session.query(Economy).filter(Economy.user_id == user_id).all()

async def get_expenses(user_id: int) -> list[Economy]:
    with Session() as session:
        return session.query(Economy).filter(and_(Economy.user_id == user_id, Economy.amount < 0)).all()

async def get_incomes(user_id: int) -> list[Economy]:
    with Session() as session:
        return session.query(Economy).filter(and_(Economy.user_id == user_id, Economy.amount > 0)).all()
