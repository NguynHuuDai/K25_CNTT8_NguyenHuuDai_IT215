from sqlalchemy import Integer, String,Column ,Float, ForeignKey
from src.database.base import Base

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(100), nullable=False)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey("category.id"))