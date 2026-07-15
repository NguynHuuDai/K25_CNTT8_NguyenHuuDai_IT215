from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column,Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel
DATABASE_URL = "mysql+pymysql://HuuDai:123456@localhost:3306/connent_db"
app = FastAPI()
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine
)
Base = declarative_base()
def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable= False)

@app.get("/")
def home():
    return{
        "message": "api đang chạy"
    }
@app.get("/products")
def get_all_products(db: Session= Depends(get_db)):
    products = db.query(Product).all()
    return{
        "message": "Lay ds sp tc",
        "data": products
    }

@app.get("/product/{product_id}")
def get_product_detail(product_id: int, db: Session= Depends(get_db)):
    product = db.query(Product).filter(Product.id ==product_id).first()
    if product is None:
        raise HTTPException(
            status_code= 404,
            detail="Khong tim thay san pham"
        )
    return{
        "message":"Lay chi tiet san pham thanh cong",
        "data": product
    }

class ProductCreate:
    name: str
    pricr: float


@app.post("/products")
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    print("sản phẩm vừa thêm vào", product)

    new_product = Product(
        name=product.name,
        price=product.price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message": "thêm sản phẩm thành công",
        "data": new_product
    }


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="không tìm thấy sản phẩm để xóa!"
        )
    db.delete(product)
    db.commit()
    return {
        "message": "xóa sản phẩm thành công!",
        "data": product
    }


@app.put("/products/{product_id}")
def update_product(product_id: int, update_product: ProductCreate,
                   db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="không tìm thấy sản phẩm để cập nhật"
        )
    product["name"] = update_product.name
    product["price"] = update_product.price
    db.commit()
    db.refresh()
    return{
        "message":"cập nhậm sp tc",
        "data": product
    }