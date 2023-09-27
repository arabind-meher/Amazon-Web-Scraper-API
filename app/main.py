from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from amazon.products import AmazonProduct
from database.models import Products
from database.schemas import connect_db


app = FastAPI()


@app.get('/products', status_code=status.HTTP_200_OK)
async def read_all_products(db: Session = Depends(connect_db)):
    try:
        products = db.query(Products).all()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=error)

    if products is None:
        raise HTTPException(status_code=404, detail='Product Not Found')
    elif not products:
        raise HTTPException(status_code=404, detail='Product Not Found')

    return JSONResponse(content=jsonable_encoder(products))


@app.get('/products/{product_id}', status_code=status.HTTP_200_OK)
async def read_product(product_id: int, db: Session = Depends(connect_db)):
    try:
        product = db.query(Products).filter(
            Products.id == product_id
        ).first()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=error)

    if product is None:
        raise HTTPException(status_code=404, detail='Product Not Found')

    return JSONResponse(content=jsonable_encoder(product))


@app.post('/products/add', status_code=status.HTTP_201_CREATED)
async def add_product(url: str, target: float, db: Session = Depends(connect_db)):
    amazon_product = AmazonProduct()
    result = amazon_product.get_product_details(url)
    amazon_product.close()

    if result.get('status') == 'error':
        raise HTTPException(status_code=500, detail=result.get('error'))

    product_details = result.get('data')

    product = Products()
    product.url = url
    product.title = product_details['title']
    product.price = product_details['price']
    product.target = target
    product.image_url = product_details['image_url']

    try:
        db.add(product)
        db.commit()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=error)


@app.put('/products/update', status_code=status.HTTP_204_NO_CONTENT)
async def update_all_products(db: Session = Depends(connect_db)):
    try:
        products = db.query(Products).all()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=error)

    if products is None:
        raise HTTPException(status_code=404, detail='Product Not Found')
    elif not products:
        raise HTTPException(status_code=404, detail='Product Not Found')

    amazon_product = AmazonProduct()

    for product in products:
        result = amazon_product.get_product_details(product.url)

        if result.get('status') == 'error':
            raise HTTPException(status_code=500, detail=result.get('error'))

        updated_product = result.get('data')

        try:
            db.query(Products).filter(Products.id == product.id).update({
                'price': updated_product.get('price')
            })
        except SQLAlchemyError as error:
            raise HTTPException(status_code=500, detail=error)

    try:
        db.commit()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=error)

    amazon_product.close()


@app.put('/products/update/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
def update_product(product_id: int, db: Session = Depends(connect_db)):
    try:
        product = db.query(Products).filter(
            Products.id == product_id
        ).first()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=error)

    if product is None:
        raise HTTPException(status_code=404, detail='Product Not Found')

    amazon_product = AmazonProduct()
    result = amazon_product.get_product_details(product.url)
    amazon_product.close

    if result.get('status') == 'error':
        raise HTTPException(status_code=500, detail=result.get('error'))

    updated_product = result.get('data')

    try:
        db.query(Products).filter(Products.id == product.id).update({
            'price': updated_product.get('price')
        })
        db.commit()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=error)


@app.delete('/products/delete/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(connect_db)):
    try:
        product = db.query(Products).filter(
            Products.id == product_id
        ).first()

        if product is None:
            raise HTTPException(status_code=404, detail='Product Not Found')

        db.query(Products).filter(Products.id == product_id).delete()
        db.commit()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=error)
