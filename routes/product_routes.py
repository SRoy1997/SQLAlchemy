from flask import request, Blueprint

import controllers

product = Blueprint('product', __name__)


@product.route('/product', methods=['POST'])
def add_product():
    return controllers.add_product(request)


@product.route('/product/<product_id>', methods=["GET"])
def get_product_by_id(product_id):
    return controllers.get_product_by_id(request, product_id)


@product.route('/products', methods=["GET"])
def get_all_products():
    return controllers.get_all_products(request)


@product.route('/product/category', methods=['POST'])
def create_product_category():
    return controllers.create_product_category(request)


@product.route('/product/<product_id>', methods=['PUT'])
def update_product(product_id):
    return controllers.update_product(request, product_id)


@product.route('/product/delete/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    return controllers.delete_product(request, product_id)
