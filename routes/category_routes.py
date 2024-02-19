from flask import request, Blueprint

import controllers

category = Blueprint('category', __name__)


@category.route('/category', methods=['POST'])
def add_category():
    return controllers.add_category(request)


@category.route('/category/<category_id>', methods=["GET"])
def get_category_by_id(category_id):
    return controllers.get_category_by_id(request, category_id)


@category.route('/categories', methods=["GET"])
def get_all_categories():
    return controllers.get_all_categories(request)


@category.route('/category/<category_id>', methods=['PUT'])
def update_category(category_id):
    return controllers.update_category(request, category_id)


@category.route('/category/delete/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    return controllers.delete_category(request, category_id)
