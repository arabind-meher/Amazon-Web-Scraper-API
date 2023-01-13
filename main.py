from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from amazon import AmazonProduct
from database import connect_db
from model import Products

app = FastAPI()


@app.get('/products')
async def read_all_products(db: Session = Depends(connect_db)):
    products = db.query(Products).all()

    if products is None:
        return HTTPException(status_code=404, detail='Product Not Found')
    return products


@app.get('/products/{product_id}')
async def read_product(product_id: int, db: Session = Depends(connect_db)):
    product = db.query(Products).filter(Products.id == product_id).first()

    if product is None:
        return HTTPException(status_code=404, detail='Product Not Found')
    return product


@app.post('/products/add')
async def add_product(url: str, target_price: float, db: Session = Depends(connect_db)):
    amazon_product = AmazonProduct()
    product_details = amazon_product.get_product_details(url)

    if product_details.get('status') == 'error':
        return HTTPException(status_code=408, detail='Request Timeout Error')

    amazon_product.close_driver()

    product = Products()
    product.url = url
    product.title = product_details['title']
    product.current_price = product_details['current_price']
    product.target_price = target_price
    product.image_url = product_details['image_url']

    db.add(product)
    db.commit()

    return HTTPException(status_code=201, detail='Product Created')


@app.put('/products/update')
async def update_all_products(db: Session = Depends(connect_db)):
    amazon_product = AmazonProduct()
    products = db.query(Products).all()

    if products is None:
        HTTPException(status_code=404, detail='Product Not Found')

    for product in products:
        updated_product = amazon_product.get_product_details(product.url)
        db.query(Products).filter(Products.id == product.id).update({'current_price': updated_product['current_price']})

    db.commit()
    amazon_product.close_driver()

    return HTTPException(status_code=204, detail='All Products Updated')


@app.put('/products/update/{product_id}')
async def update_product(product_id: int, db: Session = Depends(connect_db)):
    amazon_product = AmazonProduct()
    product = db.query(Products).filter(Products.id == product_id).first()

    if product is None:
        return HTTPException(status_code=404, detail='Product Not Found')

    updated_product = amazon_product.get_product_details(product.url)
    db.query(Products).filter(Products.id == product.id).update({'current_price': updated_product['current_price']})

    db.commit()
    amazon_product.close_driver()

    return HTTPException(status_code=204, detail='Product Updated')


@app.delete('/products/delete/{product_id}')
async def delete_product(product_id: int, db: Session = Depends(connect_db)):
    db.query(Products).filter(Products.id == product_id).delete()
    db.commit()

    return HTTPException(status_code=204, detail='Product Deleted')
