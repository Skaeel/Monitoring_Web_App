from fastapi import FastAPI
from parser.main import GetProductInfo
from sqlalchemy import (Table, MetaData, Column, Integer, String, create_engine,
                         ForeignKey, delete, select, Float)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

metadata = MetaData()
Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    link = Column(String)
    rating = Column(Float)
    prices = relationship("Price", back_populates="products")

    def to_dict(self):
        return {
            'name': self.name,
            'link': self.link,
            'rating': self.rating
        }

class Price(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    price = Column(Float)
    products = relationship("Product", back_populates="prices")

Session = sessionmaker(bind=engine)
session = Session()

try:
    conn = engine.connect()
    print('DB connected')
    print(f'Connection object is : {conn}')
except:
    print('DB not connected')

app = FastAPI()

@app.on_event('startup')
async def startup():
    Base.metadata.create_all(engine)

@app.on_event('shutdown')
async def shutdown():
    session.close()

@app.post('/new_product')
async def add_new_product(url):
    product = Product(
        name=GetProductInfo.get_product_name(url),
        link=url,
        rating=GetProductInfo.get_product_rating(url)
    )
    session.add(product)

    current_price = float(GetProductInfo.get_product_price(url).replace('₽', '')
                        .replace(',', '.').replace(' ', '').strip())
    price = Price(
        products=product,
        price=current_price
    )
    session.add(price)

    session.commit()
    return 'You added a new product successfully'

@app.get('/del_product')
async def del_product(id):
    del_prices = session.query(Price) \
        .filter(Price.product_id == id).delete()
    del_product = session.query(Product) \
        .filter(Product.id == id).delete()
    
    session.commit()
    return 'You deleted a product successfully'

@app.get('/monitoring_products')
async def monitoring_products_list():
    sel = session.query(Product).all()

    return sel

# @app.get('/select_product')
# async def select_product(offset, limit):
#     products = session.query(Product).limit(limit).offset(offset).all()

#     return products[0].link
