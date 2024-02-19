from flask import jsonify, Request, request

from db import db
from models.product import Products
from models.category import Categories


def add_product(req: Request):
    post_data = request.form if request.form else request.get_json()

    fields = ['product_name', 'description', 'price', 'company_id', 'active']
    required_fields = ['product_name', 'company_id']

    values = {}

    for field in fields:
        field_data = post_data.get(field)
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400

        values[field] = field_data

    new_product = Products(values['product_name'], values['description'], values['price'], values['company_id'], values['active'])

    try:
        db.session.add(new_product)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    query = db.session.query(Products).filter(Products.product_name == values['product_name']).first()

    product = {
        "product_id": query.product_id,
        "product_name": query.product_name,
        "description": query.description,
        "price": query.price,
        "company_id": query.company_id,
        "active": query.active
    }

    return jsonify({"message": "product created", "result": product}), 200


def get_product_by_id(req: Request, product_id):
    query = db.session.query(Products).filter(Products.product_id == product_id).first()
    if not query:
        return jsonify({"message": f"product does not exist"}), 404

    categories_list = []

    for category in query.categories:
        categories_list.append({
            "category_id": category.category_id,
            "category_name": category.category_name
        })

    company_dict = {
        "company_id": query.company.company_id,
        "company_name": query.company.company_name
    }

    product = {
        'product_id': query.product_id,
        'product_name': query.product_name,
        'description': query.description,
        'price': query.price,
        'active': query.active,
        'company': company_dict,
        'categories': categories_list,
    }

    return jsonify({"message": "product found", "results": product}), 200


def get_all_products(req: Request):
    query = db.session.query(Products).all()

    product_list = []

    for product in query:
        categories_list = []

        for category in product.categories:
            categories_list.append({
                "category_id": category.category_id,
                "category_name": category.category_name
            })

        company_dict = {
            "company_id": product.company.company_id,
            "company_name": product.company.company_name
        }

        product_dict = {
            'product_id': product.product_id,
            'product_name': product.product_name,
            'description': product.description,
            'price': product.price,
            'active': product.active,
            'company': company_dict,
            'categories': categories_list,
        }

        product_list.append(product_dict)

    return jsonify({"message": "product found", "results": product_list}), 200


def create_product_category(req: Request):
    post_data = request.form if request.form else request.get_json()
    product_id = post_data.get('product_id')
    category_id = post_data.get('category_id')

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    print(product_query)
    print(category_query)

    if product_query:
        if category_query:
            product_query.categories.append(category_query)

            db.session.commit()

        categories_list = []

        for category in product_query.categories:
            categories_list.append({
                "category_id": category.category_id,
                "category_name": category.category_name
            })

        company_dict = {
            "company_id": product_query.company.company_id,
            "company_name": product_query.company.company_name
        }

        product_dict = {
            'product_id': product_query.product_id,
            'product_name': product_query.product_name,
            'description': product_query.description,
            'price': product_query.price,
            'active': product_query.active,
            'company': company_dict,
            'categories': categories_list,
        }

    return jsonify({"message": "category added to product", "result": product_dict}), 200


def update_product(req: Request, product_id):
    post_data = request.form if request.form else request.get_json()
    query = db.session.query(Products).filter(Products.product_id == product_id).first()

    query.product_name = post_data.get("product_name", query.product_name)
    query.description = post_data.get("description", query.description)
    query.price = post_data.get("price", query.price)
    query.company_id = post_data.get("company_id", query.company_id)
    query.active = post_data.get("active", query.active)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    categories_list = []

    for category in query.categories:
        categories_list.append({
            "category_id": category.category_id,
            "category_name": category.category_name
        })

    company_dict = {
        "company_id": query.company.company_id,
        "company_name": query.company.company_name
    }

    product_dict = {
        'product_id': query.product_id,
        'product_name': query.product_name,
        'description': query.description,
        'price': query.price,
        'active': query.active,
        'company': company_dict,
        'categories': categories_list,
    }

    return jsonify({"message": "product updated", "results": product_dict}), 200


def delete_product(req: Request, product_id):
    query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not query:
        return jsonify({"message": f"product does not exist"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "product deleted"}), 200
